import { LitElement, css, html, nothing } from "lit";

type State = { state: string; attributes: Record<string, unknown> };
type Hass = { states: Record<string, State | undefined>; locale?: { language?: string } };
type Config = { type?: string; entity?: string; title?: string; max_items?: number; show_status?: boolean; show_debug?: boolean };
const unavailable = new Set(["unknown", "unavailable"]);

function text(value: unknown, fallback = "—"): string {
  return typeof value === "string" && value.trim() ? value.trim() : fallback;
}
function number(value: unknown, suffix = ""): string {
  const result = Number(value);
  return Number.isFinite(result) ? `${new Intl.NumberFormat().format(result)}${suffix}` : "—";
}
function escapeHtml(value: unknown): string {
  return String(value ?? "").replace(/[&<>\"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#039;" })[char] ?? char);
}

export class AirTrafficCard extends LitElement {
  static styles = css`
    :host { display:block; container-type:inline-size; }
    ha-card { padding:16px; color:var(--primary-text-color); background:var(--card-background-color); }
    .header { display:flex; justify-content:space-between; gap:12px; align-items:baseline; margin-bottom:12px; }
    h2 { margin:0; font-size:1.1rem; } .muted { color:var(--secondary-text-color); font-size:.88rem; }
    .status, .empty, .error { padding:10px 0; } .error { color:var(--error-color, #db4437); }
    .status { border-bottom:1px solid var(--divider-color); margin-bottom:8px; }
    .list { display:grid; gap:8px; } .flight { border:1px solid var(--divider-color); border-radius:12px; padding:10px; }
    .top { display:flex; justify-content:space-between; gap:8px; } .name { font-weight:600; }
    .badge { background:var(--secondary-background-color); border-radius:999px; padding:3px 7px; font-size:.72rem; }
    .metrics { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin-top:8px; }
    .metric { min-width:0; } .metric strong { display:block; overflow-wrap:anywhere; font-size:.88rem; }
    .flight { cursor:pointer; } .flight:focus-visible { outline:2px solid var(--primary-color); outline-offset:2px; }
    .detail { margin:0 0 10px; padding:12px; border-radius:12px; background:var(--secondary-background-color); }
    .detail-head { display:flex; justify-content:space-between; gap:8px; } .close { color:var(--primary-color); border:0; background:none; cursor:pointer; font-size:1.1rem; }
    @container (max-width:600px) { ha-card{padding:12px}.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}.header{align-items:flex-start;flex-direction:column} }
  `;
  private _config: Config = {};
  private _hass?: Hass;
  private _error?: string;
  private _selectedKey?: string;

  setConfig(config: Config): void {
    if (!config || typeof config.entity !== "string" || !config.entity.trim()) {
      this._error = "Eine Entity muss ausgewählt werden.";
      this._config = { ...config };
    } else {
      this._error = undefined;
      this._config = { title: "Air Traffic", max_items: 50, show_status: true, show_debug: false, ...config };
    }
    this.requestUpdate();
  }
  set hass(value: Hass) { this._hass = value; this.requestUpdate(); }
  get hass(): Hass | undefined { return this._hass; }
  getCardSize(): number { return 6; }
  static getConfigElement(): HTMLElement { return document.createElement("air-traffic-card-editor"); }
  static getStubConfig(): Config { return { type: "custom:air-traffic-card", show_status: true, max_items: 50 }; }

  render() {
    if (this._error) return html`<ha-card><div class="error">${this._error}</div></ha-card>`;
    if (!this._hass || !this._config.entity) return html`<ha-card><div class="empty">Keine Daten verfügbar.</div></ha-card>`;
    const state = this._hass.states[this._config.entity];
    if (!state) return html`<ha-card><div class="error">Entity nicht gefunden: ${this._config.entity}</div></ha-card>`;
    if (unavailable.has(state.state)) return html`<ha-card><div class="empty">Entity ist nicht verfügbar.</div></ha-card>`;
    const attrs = state.attributes ?? {};
    const flights = Array.isArray(attrs.flights) ? attrs.flights.slice(0, Number(this._config.max_items) || 50) as Record<string, unknown>[] : [];
    const stale = attrs.data_stale === true;
    return html`<ha-card>
      <div class="header"><div><h2>${this._config.title ?? "Air Traffic"}</h2><div class="muted">${number(state.state)} Flugzeuge</div></div><div class="muted">${stale ? "⚠ Veraltete Quelldaten" : "● Aktualisiert"}</div></div>
      ${this._config.show_status !== false ? html`<div class="status">FR24: ${number(attrs.fr24_count)} · ADS-B: ${number(attrs.adsb_count)} · Zusammengeführt: ${number(attrs.merged_count)}</div>` : nothing}
      ${attrs.source_errors && Object.keys(attrs.source_errors as object).length ? html`<div class="error">${escapeHtml(JSON.stringify(attrs.source_errors))}</div>` : nothing}
      ${this._detail(flights)}
      ${flights.length ? html`<div class="list">${flights.map((flight) => this._flight(flight))}</div>` : html`<div class="empty">Keine Flugzeuge vorhanden.</div>`}
      ${this._config.show_debug ? html`<pre>${JSON.stringify(attrs, null, 2)}</pre>` : nothing}
    </ha-card>`;
  }
  private _flight(flight: Record<string, unknown>) {
    const key = String(flight.key ?? `${flight.registration ?? ""}:${flight.callsign ?? ""}`);
    return html`<article class="flight" tabindex="0" role="button" @click=${() => this._selectFlight(key)} @keydown=${(event: KeyboardEvent) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); this._selectFlight(key); } }}><div class="top"><span class="name">${text(flight.callsign, text(flight.registration, "Unbekannt"))}</span><span class="badge">${text(flight.source)}</span></div><div class="muted">${text(flight.airline)} · ${text(flight.aircraft_model)}</div><div class="metrics">
      ${this._metric("Registrierung", flight.registration)}${this._metric("Höhe", flight.alt_m, " m")}${this._metric("Geschwindigkeit", flight.spd_kmh, " km/h")}${this._metric("Kurs", flight.dir_deg, "°")}
    </div>${flight.tracked ? html`<div class="muted">★ Beobachtet: ${text(flight.tracked_target)}</div>` : nothing}</article>`;
  }
  private _detail(flights: Record<string, unknown>[]) {
    if (!this._selectedKey) return nothing;
    const flight = flights.find((item) => String(item.key ?? `${item.registration ?? ""}:${item.callsign ?? ""}`) === this._selectedKey);
    if (!flight) return nothing;
    return html`<section class="detail" aria-live="polite"><div class="detail-head"><strong>${text(flight.callsign, text(flight.registration, "Flugzeugdetails"))}</strong><button class="close" aria-label="Details schließen" @click=${() => { this._selectedKey = undefined; }}>×</button></div><div class="muted">${text(flight.airline)} · ${text(flight.aircraft_model)} · HEX ${text(flight.hex)}</div><div class="muted">Position: ${text(flight.latitude)} / ${text(flight.longitude)} · Datenalter: ${flight.position_age_s == null ? "—" : number(flight.position_age_s, " s")}</div></section>`;
  }
  private _selectFlight(key: string) { this._selectedKey = key; this.requestUpdate(); }
  private _metric(label: string, value: unknown, suffix = "") { return html`<div class="metric"><span class="muted">${label}</span><strong>${typeof value === "number" ? number(value, suffix) : text(value)}</strong></div>`; }
}

class AirTrafficCardEditor extends HTMLElement {
  private _config: Config = {};
  setConfig(config: Config) { this._config = { ...config }; this.innerHTML = `<label>Entity <input value="${escapeHtml(this._config.entity ?? "")}" /></label>`; const input = this.querySelector("input"); input?.addEventListener("change", () => { this._config.entity = input.value; this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: this._config }, bubbles: true, composed: true })); }); }
}

function register(name: string, constructor: CustomElementConstructor) { if (!customElements.get(name)) customElements.define(name, constructor); }
class LegacyAirTrafficCard extends AirTrafficCard {}
register("air-traffic-card", AirTrafficCard);
register("air-traffic-merge-card", LegacyAirTrafficCard);
register("air-traffic-card-editor", AirTrafficCardEditor);
declare global { interface Window { customCards?: Array<Record<string, unknown>> } }
window.customCards ??= [];
for (const card of [
  { type: "air-traffic-card", name: "Air Traffic Card", description: "Zeigt zusammengeführte Flugverkehrsdaten.", documentationURL: "https://github.com/balronu/ha-air-traffic" },
  { type: "air-traffic-merge-card", name: "Air Traffic Card (Legacy)", description: "Kompatibler Legacy-Kartentyp.", documentationURL: "https://github.com/balronu/ha-air-traffic" },
]) if (!window.customCards.some((entry) => entry.type === card.type)) window.customCards.push(card);
