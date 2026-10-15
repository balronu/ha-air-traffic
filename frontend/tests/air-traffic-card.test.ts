import { describe, expect, it } from "vitest";
import { AirTrafficCard } from "../src/air-traffic-card";

describe("Air Traffic Card", () => {
  it("registers the new and legacy card elements idempotently", async () => {
    await import("../src/air-traffic-card");
    expect(customElements.get("air-traffic-card")).toBe(AirTrafficCard);
    expect(customElements.get("air-traffic-merge-card")).toBeDefined();
    expect(customElements.get("air-traffic-merge-card")).not.toBe(AirTrafficCard);
    const entries = (window.customCards ?? []).filter((entry) => ["air-traffic-card", "air-traffic-merge-card"].includes(String(entry.type)));
    expect(entries).toHaveLength(2);
  });

  it("renders empty, error, stale and flight states", async () => {
    const card = new AirTrafficCard();
    document.body.append(card);
    card.setConfig({ entity: "sensor.air_traffic_merged" });
    (card as any).hass = { states: { "sensor.air_traffic_merged": { state: "1", attributes: { flights: [{ callsign: "TEST1", source: "ADSB", alt_m: 1000 }], data_stale: true } } } };
    await card.updateComplete;
    expect(card.shadowRoot?.textContent).toContain("TEST1");
    expect(card.shadowRoot?.textContent).toContain("Veraltete");
  });
});
