const O = globalThis, D = O.ShadowRoot && (O.ShadyCSS === void 0 || O.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype, j = /* @__PURE__ */ Symbol(), F = /* @__PURE__ */ new WeakMap();
let st = class {
  constructor(t, e, s) {
    if (this._$cssResult$ = !0, s !== j) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
    this.cssText = t, this.t = e;
  }
  get styleSheet() {
    let t = this.o;
    const e = this.t;
    if (D && t === void 0) {
      const s = e !== void 0 && e.length === 1;
      s && (t = F.get(e)), t === void 0 && ((this.o = t = new CSSStyleSheet()).replaceSync(this.cssText), s && F.set(e, t));
    }
    return t;
  }
  toString() {
    return this.cssText;
  }
};
const lt = (r) => new st(typeof r == "string" ? r : r + "", void 0, j), dt = (r, ...t) => {
  const e = r.length === 1 ? r[0] : t.reduce((s, i, n) => s + ((o) => {
    if (o._$cssResult$ === !0) return o.cssText;
    if (typeof o == "number") return o;
    throw Error("Value passed to 'css' function must be a 'css' function result: " + o + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
  })(i) + r[n + 1], r[0]);
  return new st(e, r, j);
}, ut = (r, t) => {
  if (D) r.adoptedStyleSheets = t.map((e) => e instanceof CSSStyleSheet ? e : e.styleSheet);
  else for (const e of t) {
    const s = document.createElement("style"), i = O.litNonce;
    i !== void 0 && s.setAttribute("nonce", i), s.textContent = e.cssText, r.appendChild(s);
  }
}, V = D ? (r) => r : (r) => r instanceof CSSStyleSheet ? ((t) => {
  let e = "";
  for (const s of t.cssRules) e += s.cssText;
  return lt(e);
})(r) : r;
const { is: pt, defineProperty: $t, getOwnPropertyDescriptor: ft, getOwnPropertyNames: _t, getOwnPropertySymbols: gt, getPrototypeOf: mt } = Object, M = globalThis, W = M.trustedTypes, yt = W ? W.emptyScript : "", vt = M.reactiveElementPolyfillSupport, w = (r, t) => r, L = { toAttribute(r, t) {
  switch (t) {
    case Boolean:
      r = r ? yt : null;
      break;
    case Object:
    case Array:
      r = r == null ? r : JSON.stringify(r);
  }
  return r;
}, fromAttribute(r, t) {
  let e = r;
  switch (t) {
    case Boolean:
      e = r !== null;
      break;
    case Number:
      e = r === null ? null : Number(r);
      break;
    case Object:
    case Array:
      try {
        e = JSON.parse(r);
      } catch {
        e = null;
      }
  }
  return e;
} }, it = (r, t) => !pt(r, t), Z = { attribute: !0, type: String, converter: L, reflect: !1, useDefault: !1, hasChanged: it };
Symbol.metadata ??= /* @__PURE__ */ Symbol("metadata"), M.litPropertyMetadata ??= /* @__PURE__ */ new WeakMap();
let b = class extends HTMLElement {
  static addInitializer(t) {
    this._$Ei(), (this.l ??= []).push(t);
  }
  static get observedAttributes() {
    return this.finalize(), this._$Eh && [...this._$Eh.keys()];
  }
  static createProperty(t, e = Z) {
    if (e.state && (e.attribute = !1), this._$Ei(), this.prototype.hasOwnProperty(t) && ((e = Object.create(e)).wrapped = !0), this.elementProperties.set(t, e), !e.noAccessor) {
      const s = /* @__PURE__ */ Symbol(), i = this.getPropertyDescriptor(t, s, e);
      i !== void 0 && $t(this.prototype, t, i);
    }
  }
  static getPropertyDescriptor(t, e, s) {
    const { get: i, set: n } = ft(this.prototype, t) ?? { get() {
      return this[e];
    }, set(o) {
      this[e] = o;
    } };
    return { get: i, set(o) {
      const l = i?.call(this);
      n?.call(this, o), this.requestUpdate(t, l, s);
    }, configurable: !0, enumerable: !0 };
  }
  static getPropertyOptions(t) {
    return this.elementProperties.get(t) ?? Z;
  }
  static _$Ei() {
    if (this.hasOwnProperty(w("elementProperties"))) return;
    const t = mt(this);
    t.finalize(), t.l !== void 0 && (this.l = [...t.l]), this.elementProperties = new Map(t.elementProperties);
  }
  static finalize() {
    if (this.hasOwnProperty(w("finalized"))) return;
    if (this.finalized = !0, this._$Ei(), this.hasOwnProperty(w("properties"))) {
      const e = this.properties, s = [..._t(e), ...gt(e)];
      for (const i of s) this.createProperty(i, e[i]);
    }
    const t = this[Symbol.metadata];
    if (t !== null) {
      const e = litPropertyMetadata.get(t);
      if (e !== void 0) for (const [s, i] of e) this.elementProperties.set(s, i);
    }
    this._$Eh = /* @__PURE__ */ new Map();
    for (const [e, s] of this.elementProperties) {
      const i = this._$Eu(e, s);
      i !== void 0 && this._$Eh.set(i, e);
    }
    this.elementStyles = this.finalizeStyles(this.styles);
  }
  static finalizeStyles(t) {
    const e = [];
    if (Array.isArray(t)) {
      const s = new Set(t.flat(1 / 0).reverse());
      for (const i of s) e.unshift(V(i));
    } else t !== void 0 && e.push(V(t));
    return e;
  }
  static _$Eu(t, e) {
    const s = e.attribute;
    return s === !1 ? void 0 : typeof s == "string" ? s : typeof t == "string" ? t.toLowerCase() : void 0;
  }
  constructor() {
    super(), this._$Ep = void 0, this.isUpdatePending = !1, this.hasUpdated = !1, this._$Em = null, this._$Ev();
  }
  _$Ev() {
    this._$ES = new Promise((t) => this.enableUpdating = t), this._$AL = /* @__PURE__ */ new Map(), this._$E_(), this.requestUpdate(), this.constructor.l?.forEach((t) => t(this));
  }
  addController(t) {
    (this._$EO ??= /* @__PURE__ */ new Set()).add(t), this.renderRoot !== void 0 && this.isConnected && t.hostConnected?.();
  }
  removeController(t) {
    this._$EO?.delete(t);
  }
  _$E_() {
    const t = /* @__PURE__ */ new Map(), e = this.constructor.elementProperties;
    for (const s of e.keys()) this.hasOwnProperty(s) && (t.set(s, this[s]), delete this[s]);
    t.size > 0 && (this._$Ep = t);
  }
  createRenderRoot() {
    const t = this.shadowRoot ?? this.attachShadow(this.constructor.shadowRootOptions);
    return ut(t, this.constructor.elementStyles), t;
  }
  connectedCallback() {
    this.renderRoot ??= this.createRenderRoot(), this.enableUpdating(!0), this._$EO?.forEach((t) => t.hostConnected?.());
  }
  enableUpdating(t) {
  }
  disconnectedCallback() {
    this._$EO?.forEach((t) => t.hostDisconnected?.());
  }
  attributeChangedCallback(t, e, s) {
    this._$AK(t, s);
  }
  _$ET(t, e) {
    const s = this.constructor.elementProperties.get(t), i = this.constructor._$Eu(t, s);
    if (i !== void 0 && s.reflect === !0) {
      const n = (s.converter?.toAttribute !== void 0 ? s.converter : L).toAttribute(e, s.type);
      this._$Em = t, n == null ? this.removeAttribute(i) : this.setAttribute(i, n), this._$Em = null;
    }
  }
  _$AK(t, e) {
    const s = this.constructor, i = s._$Eh.get(t);
    if (i !== void 0 && this._$Em !== i) {
      const n = s.getPropertyOptions(i), o = typeof n.converter == "function" ? { fromAttribute: n.converter } : n.converter?.fromAttribute !== void 0 ? n.converter : L;
      this._$Em = i;
      const l = o.fromAttribute(e, n.type);
      this[i] = l ?? this._$Ej?.get(i) ?? l, this._$Em = null;
    }
  }
  requestUpdate(t, e, s, i = !1, n) {
    if (t !== void 0) {
      const o = this.constructor;
      if (i === !1 && (n = this[t]), s ??= o.getPropertyOptions(t), !((s.hasChanged ?? it)(n, e) || s.useDefault && s.reflect && n === this._$Ej?.get(t) && !this.hasAttribute(o._$Eu(t, s)))) return;
      this.C(t, e, s);
    }
    this.isUpdatePending === !1 && (this._$ES = this._$EP());
  }
  C(t, e, { useDefault: s, reflect: i, wrapped: n }, o) {
    s && !(this._$Ej ??= /* @__PURE__ */ new Map()).has(t) && (this._$Ej.set(t, o ?? e ?? this[t]), n !== !0 || o !== void 0) || (this._$AL.has(t) || (this.hasUpdated || s || (e = void 0), this._$AL.set(t, e)), i === !0 && this._$Em !== t && (this._$Eq ??= /* @__PURE__ */ new Set()).add(t));
  }
  async _$EP() {
    this.isUpdatePending = !0;
    try {
      await this._$ES;
    } catch (e) {
      Promise.reject(e);
    }
    const t = this.scheduleUpdate();
    return t != null && await t, !this.isUpdatePending;
  }
  scheduleUpdate() {
    return this.performUpdate();
  }
  performUpdate() {
    if (!this.isUpdatePending) return;
    if (!this.hasUpdated) {
      if (this.renderRoot ??= this.createRenderRoot(), this._$Ep) {
        for (const [i, n] of this._$Ep) this[i] = n;
        this._$Ep = void 0;
      }
      const s = this.constructor.elementProperties;
      if (s.size > 0) for (const [i, n] of s) {
        const { wrapped: o } = n, l = this[i];
        o !== !0 || this._$AL.has(i) || l === void 0 || this.C(i, void 0, n, l);
      }
    }
    let t = !1;
    const e = this._$AL;
    try {
      t = this.shouldUpdate(e), t ? (this.willUpdate(e), this._$EO?.forEach((s) => s.hostUpdate?.()), this.update(e)) : this._$EM();
    } catch (s) {
      throw t = !1, this._$EM(), s;
    }
    t && this._$AE(e);
  }
  willUpdate(t) {
  }
  _$AE(t) {
    this._$EO?.forEach((e) => e.hostUpdated?.()), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(t)), this.updated(t);
  }
  _$EM() {
    this._$AL = /* @__PURE__ */ new Map(), this.isUpdatePending = !1;
  }
  get updateComplete() {
    return this.getUpdateComplete();
  }
  getUpdateComplete() {
    return this._$ES;
  }
  shouldUpdate(t) {
    return !0;
  }
  update(t) {
    this._$Eq &&= this._$Eq.forEach((e) => this._$ET(e, this[e])), this._$EM();
  }
  updated(t) {
  }
  firstUpdated(t) {
  }
};
b.elementStyles = [], b.shadowRootOptions = { mode: "open" }, b[w("elementProperties")] = /* @__PURE__ */ new Map(), b[w("finalized")] = /* @__PURE__ */ new Map(), vt?.({ ReactiveElement: b }), (M.reactiveElementVersions ??= []).push("2.1.2");
const B = globalThis, J = (r) => r, N = B.trustedTypes, G = N ? N.createPolicy("lit-html", { createHTML: (r) => r }) : void 0, rt = "$lit$", g = `lit$${Math.random().toFixed(9).slice(2)}$`, nt = "?" + g, At = `<${nt}>`, v = document, P = () => v.createComment(""), U = (r) => r === null || typeof r != "object" && typeof r != "function", I = Array.isArray, bt = (r) => I(r) || typeof r?.[Symbol.iterator] == "function", z = `[ 	
\f\r]`, x = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g, Q = /-->/g, X = />/g, m = RegExp(`>|${z}(?:([^\\s"'>=/]+)(${z}*=${z}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`, "g"), Y = /'/g, tt = /"/g, ot = /^(?:script|style|textarea|title)$/i, Et = (r) => (t, ...e) => ({ _$litType$: r, strings: t, values: e }), p = Et(1), E = /* @__PURE__ */ Symbol.for("lit-noChange"), c = /* @__PURE__ */ Symbol.for("lit-nothing"), et = /* @__PURE__ */ new WeakMap(), y = v.createTreeWalker(v, 129);
function at(r, t) {
  if (!I(r) || !r.hasOwnProperty("raw")) throw Error("invalid template strings array");
  return G !== void 0 ? G.createHTML(t) : t;
}
const St = (r, t) => {
  const e = r.length - 1, s = [];
  let i, n = t === 2 ? "<svg>" : t === 3 ? "<math>" : "", o = x;
  for (let l = 0; l < e; l++) {
    const a = r[l];
    let d, u, h = -1, f = 0;
    for (; f < a.length && (o.lastIndex = f, u = o.exec(a), u !== null); ) f = o.lastIndex, o === x ? u[1] === "!--" ? o = Q : u[1] !== void 0 ? o = X : u[2] !== void 0 ? (ot.test(u[2]) && (i = RegExp("</" + u[2], "g")), o = m) : u[3] !== void 0 && (o = m) : o === m ? u[0] === ">" ? (o = i ?? x, h = -1) : u[1] === void 0 ? h = -2 : (h = o.lastIndex - u[2].length, d = u[1], o = u[3] === void 0 ? m : u[3] === '"' ? tt : Y) : o === tt || o === Y ? o = m : o === Q || o === X ? o = x : (o = m, i = void 0);
    const _ = o === m && r[l + 1].startsWith("/>") ? " " : "";
    n += o === x ? a + At : h >= 0 ? (s.push(d), a.slice(0, h) + rt + a.slice(h) + g + _) : a + g + (h === -2 ? l : _);
  }
  return [at(r, n + (r[e] || "<?>") + (t === 2 ? "</svg>" : t === 3 ? "</math>" : "")), s];
};
class k {
  constructor({ strings: t, _$litType$: e }, s) {
    let i;
    this.parts = [];
    let n = 0, o = 0;
    const l = t.length - 1, a = this.parts, [d, u] = St(t, e);
    if (this.el = k.createElement(d, s), y.currentNode = this.el.content, e === 2 || e === 3) {
      const h = this.el.content.firstChild;
      h.replaceWith(...h.childNodes);
    }
    for (; (i = y.nextNode()) !== null && a.length < l; ) {
      if (i.nodeType === 1) {
        if (i.hasAttributes()) for (const h of i.getAttributeNames()) if (h.endsWith(rt)) {
          const f = u[o++], _ = i.getAttribute(h).split(g), H = /([.?@])?(.*)/.exec(f);
          a.push({ type: 1, index: n, name: H[2], strings: _, ctor: H[1] === "." ? wt : H[1] === "?" ? Ct : H[1] === "@" ? Pt : R }), i.removeAttribute(h);
        } else h.startsWith(g) && (a.push({ type: 6, index: n }), i.removeAttribute(h));
        if (ot.test(i.tagName)) {
          const h = i.textContent.split(g), f = h.length - 1;
          if (f > 0) {
            i.textContent = N ? N.emptyScript : "";
            for (let _ = 0; _ < f; _++) i.append(h[_], P()), y.nextNode(), a.push({ type: 2, index: ++n });
            i.append(h[f], P());
          }
        }
      } else if (i.nodeType === 8) if (i.data === nt) a.push({ type: 2, index: n });
      else {
        let h = -1;
        for (; (h = i.data.indexOf(g, h + 1)) !== -1; ) a.push({ type: 7, index: n }), h += g.length - 1;
      }
      n++;
    }
  }
  static createElement(t, e) {
    const s = v.createElement("template");
    return s.innerHTML = t, s;
  }
}
function S(r, t, e = r, s) {
  if (t === E) return t;
  let i = s !== void 0 ? e._$Co?.[s] : e._$Cl;
  const n = U(t) ? void 0 : t._$litDirective$;
  return i?.constructor !== n && (i?._$AO?.(!1), n === void 0 ? i = void 0 : (i = new n(r), i._$AT(r, e, s)), s !== void 0 ? (e._$Co ??= [])[s] = i : e._$Cl = i), i !== void 0 && (t = S(r, i._$AS(r, t.values), i, s)), t;
}
class xt {
  constructor(t, e) {
    this._$AV = [], this._$AN = void 0, this._$AD = t, this._$AM = e;
  }
  get parentNode() {
    return this._$AM.parentNode;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  u(t) {
    const { el: { content: e }, parts: s } = this._$AD, i = (t?.creationScope ?? v).importNode(e, !0);
    y.currentNode = i;
    let n = y.nextNode(), o = 0, l = 0, a = s[0];
    for (; a !== void 0; ) {
      if (o === a.index) {
        let d;
        a.type === 2 ? d = new T(n, n.nextSibling, this, t) : a.type === 1 ? d = new a.ctor(n, a.name, a.strings, this, t) : a.type === 6 && (d = new Ut(n, this, t)), this._$AV.push(d), a = s[++l];
      }
      o !== a?.index && (n = y.nextNode(), o++);
    }
    return y.currentNode = v, i;
  }
  p(t) {
    let e = 0;
    for (const s of this._$AV) s !== void 0 && (s.strings !== void 0 ? (s._$AI(t, s, e), e += s.strings.length - 2) : s._$AI(t[e])), e++;
  }
}
class T {
  get _$AU() {
    return this._$AM?._$AU ?? this._$Cv;
  }
  constructor(t, e, s, i) {
    this.type = 2, this._$AH = c, this._$AN = void 0, this._$AA = t, this._$AB = e, this._$AM = s, this.options = i, this._$Cv = i?.isConnected ?? !0;
  }
  get parentNode() {
    let t = this._$AA.parentNode;
    const e = this._$AM;
    return e !== void 0 && t?.nodeType === 11 && (t = e.parentNode), t;
  }
  get startNode() {
    return this._$AA;
  }
  get endNode() {
    return this._$AB;
  }
  _$AI(t, e = this) {
    t = S(this, t, e), U(t) ? t === c || t == null || t === "" ? (this._$AH !== c && this._$AR(), this._$AH = c) : t !== this._$AH && t !== E && this._(t) : t._$litType$ !== void 0 ? this.$(t) : t.nodeType !== void 0 ? this.T(t) : bt(t) ? this.k(t) : this._(t);
  }
  O(t) {
    return this._$AA.parentNode.insertBefore(t, this._$AB);
  }
  T(t) {
    this._$AH !== t && (this._$AR(), this._$AH = this.O(t));
  }
  _(t) {
    this._$AH !== c && U(this._$AH) ? this._$AA.nextSibling.data = t : this.T(v.createTextNode(t)), this._$AH = t;
  }
  $(t) {
    const { values: e, _$litType$: s } = t, i = typeof s == "number" ? this._$AC(t) : (s.el === void 0 && (s.el = k.createElement(at(s.h, s.h[0]), this.options)), s);
    if (this._$AH?._$AD === i) this._$AH.p(e);
    else {
      const n = new xt(i, this), o = n.u(this.options);
      n.p(e), this.T(o), this._$AH = n;
    }
  }
  _$AC(t) {
    let e = et.get(t.strings);
    return e === void 0 && et.set(t.strings, e = new k(t)), e;
  }
  k(t) {
    I(this._$AH) || (this._$AH = [], this._$AR());
    const e = this._$AH;
    let s, i = 0;
    for (const n of t) i === e.length ? e.push(s = new T(this.O(P()), this.O(P()), this, this.options)) : s = e[i], s._$AI(n), i++;
    i < e.length && (this._$AR(s && s._$AB.nextSibling, i), e.length = i);
  }
  _$AR(t = this._$AA.nextSibling, e) {
    for (this._$AP?.(!1, !0, e); t !== this._$AB; ) {
      const s = J(t).nextSibling;
      J(t).remove(), t = s;
    }
  }
  setConnected(t) {
    this._$AM === void 0 && (this._$Cv = t, this._$AP?.(t));
  }
}
class R {
  get tagName() {
    return this.element.tagName;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  constructor(t, e, s, i, n) {
    this.type = 1, this._$AH = c, this._$AN = void 0, this.element = t, this.name = e, this._$AM = i, this.options = n, s.length > 2 || s[0] !== "" || s[1] !== "" ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = c;
  }
  _$AI(t, e = this, s, i) {
    const n = this.strings;
    let o = !1;
    if (n === void 0) t = S(this, t, e, 0), o = !U(t) || t !== this._$AH && t !== E, o && (this._$AH = t);
    else {
      const l = t;
      let a, d;
      for (t = n[0], a = 0; a < n.length - 1; a++) d = S(this, l[s + a], e, a), d === E && (d = this._$AH[a]), o ||= !U(d) || d !== this._$AH[a], d === c ? t = c : t !== c && (t += (d ?? "") + n[a + 1]), this._$AH[a] = d;
    }
    o && !i && this.j(t);
  }
  j(t) {
    t === c ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, t ?? "");
  }
}
class wt extends R {
  constructor() {
    super(...arguments), this.type = 3;
  }
  j(t) {
    this.element[this.name] = t === c ? void 0 : t;
  }
}
class Ct extends R {
  constructor() {
    super(...arguments), this.type = 4;
  }
  j(t) {
    this.element.toggleAttribute(this.name, !!t && t !== c);
  }
}
class Pt extends R {
  constructor(t, e, s, i, n) {
    super(t, e, s, i, n), this.type = 5;
  }
  _$AI(t, e = this) {
    if ((t = S(this, t, e, 0) ?? c) === E) return;
    const s = this._$AH, i = t === c && s !== c || t.capture !== s.capture || t.once !== s.once || t.passive !== s.passive, n = t !== c && (s === c || i);
    i && this.element.removeEventListener(this.name, this, s), n && this.element.addEventListener(this.name, this, t), this._$AH = t;
  }
  handleEvent(t) {
    typeof this._$AH == "function" ? this._$AH.call(this.options?.host ?? this.element, t) : this._$AH.handleEvent(t);
  }
}
class Ut {
  constructor(t, e, s) {
    this.element = t, this.type = 6, this._$AN = void 0, this._$AM = e, this.options = s;
  }
  get _$AU() {
    return this._$AM._$AU;
  }
  _$AI(t) {
    S(this, t);
  }
}
const kt = B.litHtmlPolyfillSupport;
kt?.(k, T), (B.litHtmlVersions ??= []).push("3.3.3");
const Tt = (r, t, e) => {
  const s = e?.renderBefore ?? t;
  let i = s._$litPart$;
  if (i === void 0) {
    const n = e?.renderBefore ?? null;
    s._$litPart$ = i = new T(t.insertBefore(P(), n), n, void 0, e ?? {});
  }
  return i._$AI(r), i;
};
const K = globalThis;
class C extends b {
  constructor() {
    super(...arguments), this.renderOptions = { host: this }, this._$Do = void 0;
  }
  createRenderRoot() {
    const t = super.createRenderRoot();
    return this.renderOptions.renderBefore ??= t.firstChild, t;
  }
  update(t) {
    const e = this.render();
    this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Do = Tt(e, this.renderRoot, this.renderOptions);
  }
  connectedCallback() {
    super.connectedCallback(), this._$Do?.setConnected(!0);
  }
  disconnectedCallback() {
    super.disconnectedCallback(), this._$Do?.setConnected(!1);
  }
  render() {
    return E;
  }
}
C._$litElement$ = !0, C.finalized = !0, K.litElementHydrateSupport?.({ LitElement: C });
const Ht = K.litElementPolyfillSupport;
Ht?.({ LitElement: C });
(K.litElementVersions ??= []).push("4.2.2");
const Ot = /* @__PURE__ */ new Set(["unknown", "unavailable"]);
function $(r, t = "—") {
  return typeof r == "string" && r.trim() ? r.trim() : t;
}
function A(r, t = "") {
  const e = Number(r);
  return Number.isFinite(e) ? `${new Intl.NumberFormat().format(e)}${t}` : "—";
}
function ht(r) {
  return String(r ?? "").replace(/[&<>\"']/g, (t) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" })[t] ?? t);
}
class ct extends C {
  static styles = dt`
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
  _config = {};
  _hass;
  _error;
  _selectedKey;
  setConfig(t) {
    !t || typeof t.entity != "string" || !t.entity.trim() ? (this._error = "Eine Entity muss ausgewählt werden.", this._config = { ...t }) : (this._error = void 0, this._config = { title: "Air Traffic", max_items: 50, show_status: !0, show_debug: !1, ...t }), this.requestUpdate();
  }
  set hass(t) {
    this._hass = t, this.requestUpdate();
  }
  get hass() {
    return this._hass;
  }
  getCardSize() {
    return 6;
  }
  static getConfigElement() {
    return document.createElement("air-traffic-card-editor");
  }
  static getStubConfig() {
    return { type: "custom:air-traffic-card", show_status: !0, max_items: 50 };
  }
  render() {
    if (this._error) return p`<ha-card><div class="error">${this._error}</div></ha-card>`;
    if (!this._hass || !this._config.entity) return p`<ha-card><div class="empty">Keine Daten verfügbar.</div></ha-card>`;
    const t = this._hass.states[this._config.entity];
    if (!t) return p`<ha-card><div class="error">Entity nicht gefunden: ${this._config.entity}</div></ha-card>`;
    if (Ot.has(t.state)) return p`<ha-card><div class="empty">Entity ist nicht verfügbar.</div></ha-card>`;
    const e = t.attributes ?? {}, s = Array.isArray(e.flights) ? e.flights.slice(0, Number(this._config.max_items) || 50) : [], i = e.data_stale === !0;
    return p`<ha-card>
      <div class="header"><div><h2>${this._config.title ?? "Air Traffic"}</h2><div class="muted">${A(t.state)} Flugzeuge</div></div><div class="muted">${i ? "⚠ Veraltete Quelldaten" : "● Aktualisiert"}</div></div>
      ${this._config.show_status !== !1 ? p`<div class="status">FR24: ${A(e.fr24_count)} · ADS-B: ${A(e.adsb_count)} · Zusammengeführt: ${A(e.merged_count)}</div>` : c}
      ${e.source_errors && Object.keys(e.source_errors).length ? p`<div class="error">${ht(JSON.stringify(e.source_errors))}</div>` : c}
      ${this._detail(s)}
      ${s.length ? p`<div class="list">${s.map((n) => this._flight(n))}</div>` : p`<div class="empty">Keine Flugzeuge vorhanden.</div>`}
      ${this._config.show_debug ? p`<pre>${JSON.stringify(e, null, 2)}</pre>` : c}
    </ha-card>`;
  }
  _flight(t) {
    const e = String(t.key ?? `${t.registration ?? ""}:${t.callsign ?? ""}`);
    return p`<article class="flight" tabindex="0" role="button" @click=${() => this._selectFlight(e)} @keydown=${(s) => {
      (s.key === "Enter" || s.key === " ") && (s.preventDefault(), this._selectFlight(e));
    }}><div class="top"><span class="name">${$(t.callsign, $(t.registration, "Unbekannt"))}</span><span class="badge">${$(t.source)}</span></div><div class="muted">${$(t.airline)} · ${$(t.aircraft_model)}</div><div class="metrics">
      ${this._metric("Registrierung", t.registration)}${this._metric("Höhe", t.alt_m, " m")}${this._metric("Geschwindigkeit", t.spd_kmh, " km/h")}${this._metric("Kurs", t.dir_deg, "°")}
    </div>${t.tracked ? p`<div class="muted">★ Beobachtet: ${$(t.tracked_target)}</div>` : c}</article>`;
  }
  _detail(t) {
    if (!this._selectedKey) return c;
    const e = t.find((s) => String(s.key ?? `${s.registration ?? ""}:${s.callsign ?? ""}`) === this._selectedKey);
    return e ? p`<section class="detail" aria-live="polite"><div class="detail-head"><strong>${$(e.callsign, $(e.registration, "Flugzeugdetails"))}</strong><button class="close" aria-label="Details schließen" @click=${() => {
      this._selectedKey = void 0;
    }}>×</button></div><div class="muted">${$(e.airline)} · ${$(e.aircraft_model)} · HEX ${$(e.hex)}</div><div class="muted">Position: ${$(e.latitude)} / ${$(e.longitude)} · Datenalter: ${e.position_age_s == null ? "—" : A(e.position_age_s, " s")}</div></section>` : c;
  }
  _selectFlight(t) {
    this._selectedKey = t, this.requestUpdate();
  }
  _metric(t, e, s = "") {
    return p`<div class="metric"><span class="muted">${t}</span><strong>${typeof e == "number" ? A(e, s) : $(e)}</strong></div>`;
  }
}
class Nt extends HTMLElement {
  _config = {};
  setConfig(t) {
    this._config = { ...t }, this.innerHTML = `<label>Entity <input value="${ht(this._config.entity ?? "")}" /></label>`;
    const e = this.querySelector("input");
    e?.addEventListener("change", () => {
      this._config.entity = e.value, this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: this._config }, bubbles: !0, composed: !0 }));
    });
  }
}
function q(r, t) {
  customElements.get(r) || customElements.define(r, t);
}
class Mt extends ct {
}
q("air-traffic-card", ct);
q("air-traffic-merge-card", Mt);
q("air-traffic-card-editor", Nt);
window.customCards ??= [];
for (const r of [
  { type: "air-traffic-card", name: "Air Traffic Card", description: "Zeigt zusammengeführte Flugverkehrsdaten.", documentationURL: "https://github.com/balronu/ha-air-traffic" },
  { type: "air-traffic-merge-card", name: "Air Traffic Card (Legacy)", description: "Kompatibler Legacy-Kartentyp.", documentationURL: "https://github.com/balronu/ha-air-traffic" }
]) window.customCards.some((t) => t.type === r.type) || window.customCards.push(r);
export {
  ct as AirTrafficCard
};
