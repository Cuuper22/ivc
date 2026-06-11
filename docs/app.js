/* =========================================================================
   IVC experience — custom interactions, all vanilla (no CDN dependency so it
   works offline and degrades gracefully).
   Modules: nav/progress, reveals, expertise dials, scoreboard count-up,
   excavation torch (canvas), site map (SVG), branch ecology (SVG),
   null-distribution stats (SVG), decipherer's game.
   ========================================================================= */
(function () {
  "use strict";
  var D = window.IVC;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.classList.add("js");

  /* ---- tiny DOM/SVG helpers ---------------------------------------- */
  var SVGNS = "http://www.w3.org/2000/svg";
  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    apply(e, attrs); add(e, kids); return e;
  }
  function s(tag, attrs, kids) {
    var e = document.createElementNS(SVGNS, tag);
    apply(e, attrs, true); add(e, kids); return e;
  }
  function apply(e, attrs, ns) {
    if (!attrs) return;
    for (var k in attrs) {
      if (k === "text") e.textContent = attrs[k];
      else if (k === "html") e.innerHTML = attrs[k];
      else if (k.indexOf("on") === 0) e.addEventListener(k.slice(2), attrs[k]);
      else if (ns) e.setAttribute(k, attrs[k]);
      else if (k in e && k !== "class" && k !== "list") { try { e[k] = attrs[k]; } catch (x) { e.setAttribute(k, attrs[k]); } }
      else e.setAttribute(k, attrs[k]);
    }
  }
  function add(e, kids) {
    if (kids == null) return;
    if (!Array.isArray(kids)) kids = [kids];
    kids.forEach(function (k) { if (k != null) e.appendChild(typeof k === "string" ? document.createTextNode(k) : k); });
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  /* ---- progress + sticky nav --------------------------------------- */
  var progress = document.getElementById("progress"), nav = document.getElementById("nav");
  function onScroll() {
    var st = window.scrollY, hgt = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.transform = "scaleX(" + (hgt > 0 ? st / hgt : 0) + ")";
    if (nav) nav.classList.toggle("is-stuck", st > 40);
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---- reveal on scroll -------------------------------------------- */
  var reveals = [].slice.call(document.querySelectorAll(".reveal"));
  if (reduce || !("IntersectionObserver" in window)) reveals.forEach(function (e) { e.classList.add("is-in"); });
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { threshold: 0.14, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach(function (e) { io.observe(e); });
  }
  // generic "run once when visible" helper
  function whenVisible(el, cb, threshold) {
    if (!el) return;
    if (reduce || !("IntersectionObserver" in window)) { cb(); return; }
    var o = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { cb(); o.disconnect(); } });
    }, { threshold: threshold || 0.3 });
    o.observe(el);
  }

  /* ---- expertise dials --------------------------------------------- */
  [].slice.call(document.querySelectorAll(".dial")).forEach(function (dial) {
    var levels = document.querySelector('.levels[data-for="' + dial.getAttribute("data-dial") + '"]');
    if (!levels) return;
    var btns = [].slice.call(dial.querySelectorAll("button"));
    dial.addEventListener("click", function (ev) {
      var b = ev.target.closest("button"); if (!b) return;
      var lvl = b.getAttribute("data-level");
      btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      [].slice.call(levels.querySelectorAll(".level")).forEach(function (p) {
        p.classList.toggle("is-active", p.getAttribute("data-level") === lvl);
      });
    });
  });

  /* ---- scoreboard -------------------------------------------------- */
  (function () {
    var board = document.getElementById("scoreboard"); if (!board) return;
    D.LEDGER.forEach(function (it) {
      board.appendChild(h("div", { class: "tile reveal" + (it.verified ? " is-verified" : ""), role: "listitem" }, [
        h("span", { class: "tile-n", "data-count": it.n, text: "0" }),
        h("span", { class: "tile-l", text: it.label })
      ]));
    });
    whenVisible(board, function () {
      [].slice.call(board.querySelectorAll("[data-count]")).forEach(function (el) {
        var target = +el.getAttribute("data-count");
        if (reduce || !target) { el.textContent = String(target); return; }
        var t0 = performance.now();
        (function step(now) {
          var t = clamp((now - t0) / 800, 0, 1), e = 1 - Math.pow(1 - t, 3);
          el.textContent = String(Math.round(e * target));
          if (t < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, 0.4);
  })();

  /* ---- EXCAVATION TORCH (canvas) ----------------------------------- */
  (function () {
    var cv = document.getElementById("torch"); if (!cv) return;
    var ctx = cv.getContext("2d");
    var paths = {}; D.GLYPH_KEYS.forEach(function (k) { paths[k] = new Path2D(D.GLYPHS[k]); });
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var items = [], W = 0, H = 0;
    var light = { x: 0, y: 0, tx: 0, ty: 0, has: false };

    function layout() {
      var r = cv.getBoundingClientRect();
      W = r.width; H = r.height;
      cv.width = W * dpr; cv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var density = Math.max(36, Math.round(W * H / 14000));
      items = [];
      for (var i = 0; i < density; i++) {
        items.push({
          x: Math.random() * W, y: Math.random() * H,
          s: 0.26 + Math.random() * 0.5,
          rot: (Math.random() - 0.5) * 0.5,
          key: D.GLYPH_KEYS[(Math.random() * D.GLYPH_KEYS.length) | 0]
        });
      }
      if (!light.has) { light.x = light.tx = W * 0.5; light.y = light.ty = H * 0.46; }
    }
    layout();
    window.addEventListener("resize", layout);

    var R = 170;
    cv.addEventListener("pointermove", function (e) {
      var r = cv.getBoundingClientRect();
      light.tx = e.clientX - r.left; light.ty = e.clientY - r.top; light.has = true;
    });
    cv.addEventListener("pointerleave", function () { light.has = false; });

    var t = 0;
    function render() {
      t += 0.016;
      // when no pointer, the lamp drifts on its own (an unmanned dig)
      if (!light.has) { light.tx = W * (0.5 + 0.32 * Math.cos(t * 0.5)); light.ty = H * (0.5 + 0.28 * Math.sin(t * 0.7)); }
      light.x += (light.tx - light.x) * 0.12; light.y += (light.ty - light.y) * 0.12;

      ctx.clearRect(0, 0, W, H);
      // soft lamp glow
      var g = ctx.createRadialGradient(light.x, light.y, 0, light.x, light.y, R * 1.4);
      g.addColorStop(0, "rgba(120,210,196,0.10)");
      g.addColorStop(1, "rgba(120,210,196,0)");
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);

      for (var i = 0; i < items.length; i++) {
        var it = items[i];
        var d = Math.hypot(it.x - light.x, it.y - light.y);
        var rev = clamp(1 - d / R, 0, 1);
        var op = 0.05 + rev * 0.92;
        // colour ramps muted -> patina as it is "uncovered"
        var rr = Math.round(150 + rev * (120 - 150));
        var gg = Math.round(140 + rev * (220 - 140));
        var bb = Math.round(130 + rev * (200 - 130));
        ctx.save();
        ctx.translate(it.x, it.y); ctx.scale(it.s, it.s); ctx.rotate(it.rot); ctx.translate(-32, -32);
        ctx.lineWidth = 2.4 / it.s; ctx.lineJoin = "round"; ctx.lineCap = "round";
        ctx.strokeStyle = "rgba(" + rr + "," + gg + "," + bb + "," + op + ")";
        ctx.stroke(paths[it.key]);
        ctx.restore();
      }
      requestAnimationFrame(render);
    }
    if (!reduce) requestAnimationFrame(render);
    else { // static: reveal a central pool
      light.x = W * 0.5; light.y = H * 0.45; light.has = true; render();
    }
  })();

  /* ---- SITE MAP (SVG) ---------------------------------------------- */
  (function () {
    var host = document.getElementById("mapHost"); if (!host) return;
    var VB = { w: 1000, h: 470 };
    var B = { lonMin: 44, lonMax: 78, latMin: 21.5, latMax: 33.5 };
    function px(lon) { return (lon - B.lonMin) / (B.lonMax - B.lonMin) * VB.w; }
    function py(lat) { return (B.latMax - lat) / (B.latMax - B.latMin) * VB.h; }

    var svg = s("svg", { viewBox: "0 0 " + VB.w + " " + VB.h, class: "map-svg", role: "img", "aria-label": "Map of Indus Valley sites and their Mesopotamian trade link" });

    // graticule
    var grat = s("g", { class: "grat" });
    for (var lon = 45; lon <= 78; lon += 5) grat.appendChild(s("line", { x1: px(lon), y1: 0, x2: px(lon), y2: VB.h }));
    for (var lat = 22; lat <= 33; lat += 4) grat.appendChild(s("line", { x1: 0, y1: py(lat), x2: VB.w, y2: py(lat) }));
    svg.appendChild(grat);

    // Indus river (approximate)
    var river = [[74.4,34.0],[73.2,32.4],[71.6,30.4],[70.4,28.4],[69.0,27.2],[68.3,25.6],[67.5,24.0]];
    var rd = river.map(function (p, i) { return (i ? "L" : "M") + px(p[0]).toFixed(1) + " " + py(p[1]).toFixed(1); }).join(" ");
    svg.appendChild(s("path", { d: rd, class: "river" }));
    svg.appendChild(s("text", { x: px(69.4), y: py(29.4), class: "map-rivlabel", text: "Indus R." }));

    // trade arc Meluhha -> Ur
    var byId = {}; D.SITES.forEach(function (n) { byId[n.id] = n; });
    var arc = D.TRADE.map(function (id, i) { var n = byId[id]; return (i ? "L" : "M") + px(n.lon).toFixed(1) + " " + py(n.lat).toFixed(1); }).join(" ");
    svg.appendChild(s("path", { d: arc, class: "trade", id: "tradeArc" }));

    // sites
    var tip = host.parentNode.querySelector(".map-tip") || h("div", { class: "map-tip" });
    if (!tip.parentNode) host.appendChild(tip);
    var gSites = s("g", {});
    D.SITES.forEach(function (n) {
      var x = px(n.lon), y = py(n.lat);
      var cls = "site site-" + n.tag;
      var node = s("g", { class: cls, tabindex: "0", role: "button", "aria-label": n.name + ": " + n.note });
      node.appendChild(s("circle", { cx: x, cy: y, r: 16, class: "site-halo" }));
      node.appendChild(s("circle", { cx: x, cy: y, r: 5.5, class: "site-dot" }));
      node.appendChild(s("text", { x: x + 11, y: y + 4, class: "site-label", text: n.name }));
      function show() {
        tip.innerHTML = "<b>" + n.name + "</b><span class='tip-tag'>" + n.tag + "</span><p>" + n.note + "</p>";
        tip.classList.add("on");
        var rx = x / VB.w, ry = y / VB.h;
        tip.style.left = (rx * 100) + "%";
        tip.style.top = (ry * 100) + "%";
        tip.dataset.side = rx > 0.62 ? "left" : "right";
        gSites.querySelectorAll(".site").forEach(function (e2) { e2.classList.remove("active"); });
        node.classList.add("active");
      }
      node.addEventListener("pointerenter", show);
      node.addEventListener("focus", show);
      node.addEventListener("click", show);
      gSites.appendChild(node);
    });
    svg.appendChild(gSites);
    svg.addEventListener("pointerleave", function () { tip.classList.remove("on"); gSites.querySelectorAll(".site").forEach(function (e2) { e2.classList.remove("active"); }); });

    host.insertBefore(svg, tip);

    // animate the trade arc drawing in
    whenVisible(svg, function () {
      var arcEl = svg.getElementById ? svg.getElementById("tradeArc") : svg.querySelector("#tradeArc");
      if (arcEl && !reduce) {
        var len = arcEl.getTotalLength();
        arcEl.style.strokeDasharray = len; arcEl.style.strokeDashoffset = len;
        arcEl.getBoundingClientRect();
        arcEl.style.transition = "stroke-dashoffset 2.4s var(--ease-expo)";
        arcEl.style.strokeDashoffset = "0";
      }
      svg.classList.add("drawn");
    }, 0.25);
  })();

  /* ---- BRANCH ECOLOGY (SVG) ---------------------------------------- */
  (function () {
    var host = document.getElementById("branch"); if (!host) return;
    var info = document.getElementById("branchInfo");
    var B = D.BRANCH, VB = { w: 940, h: 430 };
    function cx(x) { return 70 + x * 205; }
    function cy(y) { return 36 + y * 74; }
    var byId = {}; B.nodes.forEach(function (n) { byId[n.id] = n; });

    var svg = s("svg", { viewBox: "0 0 " + VB.w + " " + VB.h, class: "branch-svg", role: "img", "aria-label": "The 002 sign-structure branch ecology" });

    var gL = s("g", { class: "blinks" });
    B.links.forEach(function (lk) {
      var a = byId[lk[0]], b = byId[lk[1]];
      var x1 = cx(a.x) + 46, y1 = cy(a.y), x2 = cx(b.x) - 46, y2 = cy(b.y);
      var mx = (x1 + x2) / 2;
      var d = "M" + x1 + " " + y1 + " C" + mx + " " + y1 + " " + mx + " " + y2 + " " + x2 + " " + y2;
      gL.appendChild(s("path", { d: d, class: "blink to-" + b.status, "data-to": b.id }));
    });
    svg.appendChild(gL);

    var gN = s("g", {});
    B.nodes.forEach(function (n, i) {
      var x = cx(n.x), y = cy(n.y);
      var g = s("g", { class: "bnode is-" + n.status, transform: "translate(" + x + "," + y + ")", tabindex: "0", role: "button", "aria-label": n.label + ": " + n.info, style: "--i:" + i });
      var w = Math.max(78, n.label.length * 13 + 30);
      g.appendChild(s("rect", { x: -w / 2, y: -22, width: w, height: 44, rx: 11, class: "bbox" }));
      g.appendChild(s("text", { x: 0, y: 6, class: "blabel", text: n.label }));
      if (n.status === "verified") g.appendChild(s("circle", { cx: w / 2 - 6, cy: -22, r: 5, class: "bcheck" }));
      function focus() {
        gN.querySelectorAll(".bnode").forEach(function (e) { e.classList.remove("sel"); });
        g.classList.add("sel");
        if (info) info.innerHTML = "<span class='bi-label'>" + n.label + "</span><span class='bi-status s-" + n.status + "'>" + n.status + "</span><p>" + n.info + "</p>";
      }
      g.addEventListener("pointerenter", focus);
      g.addEventListener("focus", focus);
      g.addEventListener("click", focus);
      gN.appendChild(g);
    });
    svg.appendChild(gN);
    host.appendChild(svg);

    // default selection = the verified node
    whenVisible(svg, function () {
      svg.classList.add("drawn");
      var sel = gN.querySelector(".bnode.is-verified");
      if (sel) sel.dispatchEvent(new Event("pointerenter"));
    }, 0.25);
  })();

  /* ---- NULL DISTRIBUTION (SVG) ------------------------------------- */
  (function () {
    var host = document.getElementById("nulls"); if (!host) return;
    var VB = { w: 760, h: 320 }, pad = { l: 28, r: 20, t: 20, b: 40 };
    var n = 46, bars = [];
    var mu = n * 0.42, sd = n * 0.12, peak = 0;
    for (var i = 0; i < n; i++) { var v = Math.exp(-0.5 * Math.pow((i - mu) / sd, 2)); bars.push(v); peak = Math.max(peak, v); }
    var bw = (VB.w - pad.l - pad.r) / n;
    var svg = s("svg", { viewBox: "0 0 " + VB.w + " " + VB.h, class: "nulls-svg", role: "img", "aria-label": "Distribution of the pattern's strength across 10,000 randomized shuffles, with the observed value far in the tail" });
    // baseline
    svg.appendChild(s("line", { x1: pad.l, y1: VB.h - pad.b, x2: VB.w - pad.r, y2: VB.h - pad.b, class: "axis" }));
    var gB = s("g", {});
    bars.forEach(function (v, i) {
      var hgt = (v / peak) * (VB.h - pad.t - pad.b);
      var x = pad.l + i * bw, y = VB.h - pad.b - hgt;
      gB.appendChild(s("rect", { x: x + 1, y: VB.h - pad.b, width: Math.max(1, bw - 2), height: 0, class: "nbar", "data-h": hgt, "data-y": y, style: "--i:" + i }));
    });
    svg.appendChild(gB);
    // observed marker far in the right tail
    var ox = pad.l + (n - 2.5) * bw;
    var marker = s("g", { class: "nmark" });
    marker.appendChild(s("line", { x1: ox, y1: pad.t, x2: ox, y2: VB.h - pad.b, class: "nmark-line" }));
    marker.appendChild(s("circle", { cx: ox, cy: pad.t + 6, r: 5, class: "nmark-dot" }));
    marker.appendChild(s("text", { x: ox - 8, y: pad.t + 4, class: "nmark-lab", "text-anchor": "end", text: "observed" }));
    marker.appendChild(s("text", { x: ox - 8, y: pad.t + 22, class: "nmark-sub", "text-anchor": "end", text: "p = 0.0002" }));
    svg.appendChild(marker);
    svg.appendChild(s("text", { x: pad.l, y: VB.h - 10, class: "naxis-lab", text: "pattern strength across 10,000 random shuffles  ->" }));
    host.appendChild(svg);
    whenVisible(svg, function () {
      svg.classList.add("drawn");
      [].slice.call(gB.querySelectorAll(".nbar")).forEach(function (b) {
        var hgt = +b.getAttribute("data-h"), y = +b.getAttribute("data-y");
        if (reduce) { b.setAttribute("height", hgt); b.setAttribute("y", y); return; }
        var i = +b.style.getPropertyValue("--i"), t0 = performance.now() + i * 14;
        (function step(now) {
          if (now < t0) { requestAnimationFrame(step); return; }
          var t = clamp((now - t0) / 500, 0, 1), e = 1 - Math.pow(1 - t, 3);
          b.setAttribute("height", hgt * e); b.setAttribute("y", (VB.h - pad.b) - hgt * e);
          if (t < 1) requestAnimationFrame(step);
        })(t0);
      });
    }, 0.3);
  })();

  /* ---- DECIPHERER'S GAME ------------------------------------------- */
  (function () {
    var host = document.getElementById("game"); if (!host) return;
    var P = D.PUZZLE;
    var rowsWrap = host.querySelector("[data-rows]");
    var opts = host.querySelector("[data-options]");
    var feedback = host.querySelector("[data-feedback]");

    // render the sequences as glyph-coded chips
    P.rows.forEach(function (row, ri) {
      var line = h("div", { class: "seqline", "data-row": ri });
      row.forEach(function (code, ci) { line.appendChild(h("span", { class: "seqtok", "data-r": ri, "data-c": ci, text: code })); });
      rowsWrap.appendChild(line);
    });

    var solved = false;
    P.options.forEach(function (opt) {
      var b = h("button", { class: "opt", text: opt, onclick: function () { pick(opt, b); } });
      opts.appendChild(b);
    });

    function pick(opt, btn) {
      if (solved) return;
      [].slice.call(opts.querySelectorAll(".opt")).forEach(function (x) { x.classList.remove("wrong"); });
      if (opt !== P.answer) {
        btn.classList.add("wrong");
        feedback.className = "game-feedback miss";
        feedback.textContent = "Not quite. That unit also shows up mid-line. Look for the one that is always last.";
        return;
      }
      solved = true;
      btn.classList.add("right");
      // light up every terminal-tail occurrence
      P.rows.forEach(function (row, ri) {
        var tail = P.tail[ri];
        if (!tail) return;
        for (var c = tail[0]; c <= tail[1]; c++) {
          var tok = rowsWrap.querySelector('.seqtok[data-r="' + ri + '"][data-c="' + c + '"]');
          if (tok) tok.classList.add("tail");
        }
        var last = rowsWrap.querySelector('.seqline[data-row="' + ri + '"]');
        if (last && tail) last.classList.add("ends");
      });
      feedback.className = "game-feedback hit";
      feedback.innerHTML = "Exactly. <b>533-717</b> closes every line it appears in, and never sits in the middle. That is the project's one accepted finding: a position, not a meaning. You just did epigraphy.";
    }
  })();

  /* ---- LAMP CURSOR (desktop, motion-allowed only) -------------------- */
  (function () {
    if (reduce || !window.matchMedia("(pointer: fine)").matches) return;
    var lamp = h("div", { class: "lamp", "aria-hidden": "true" });
    document.body.appendChild(lamp);
    var x = innerWidth / 2, y = innerHeight / 2, tx = x, ty = y, big = false, shown = false;
    document.addEventListener("pointermove", function (e) {
      tx = e.clientX; ty = e.clientY;
      if (!shown) { shown = true; lamp.classList.add("on"); }
      var t = e.target.closest && e.target.closest("a,button,.bnode,.site,.seal,.grave,[tabindex]");
      if (!!t !== big) { big = !!t; lamp.classList.toggle("big", big); }
    }, { passive: true });
    document.addEventListener("pointerleave", function () { lamp.classList.remove("on"); shown = false; });
    (function loop() {
      x += (tx - x) * 0.22; y += (ty - y) * 0.22;
      lamp.style.transform = "translate(" + x + "px," + y + "px)";
      requestAnimationFrame(loop);
    })();
  })();

  /* ---- TIMELINE: a century of attempts ------------------------------- */
  (function () {
    var host = document.getElementById("timeline"); if (!host) return;
    var track = h("div", { class: "tl-track" });
    D.TIMELINE.forEach(function (ev, i) {
      track.appendChild(h("article", { class: "tl-item" + (i === D.TIMELINE.length - 1 ? " tl-now" : ""), style: "--i:" + i }, [
        h("span", { class: "tl-year mono", text: ev.y }),
        h("span", { class: "tl-tick", "aria-hidden": "true" }),
        h("h3", { text: ev.t }),
        h("p", { text: ev.d })
      ]));
    });
    host.appendChild(track);
    var down = false, sx = 0, sl = 0;
    host.addEventListener("pointerdown", function (e) { down = true; sx = e.clientX; sl = host.scrollLeft; host.classList.add("grab"); });
    window.addEventListener("pointerup", function () { down = false; host.classList.remove("grab"); });
    window.addEventListener("pointermove", function (e) { if (down) host.scrollLeft = sl - (e.clientX - sx); });
    whenVisible(host, function () { host.classList.add("drawn"); }, 0.2);
  })();

  /* ---- GRAVEYARD: the retracted claims ------------------------------- */
  (function () {
    var host = document.getElementById("graves"); if (!host) return;
    D.GRAVES.forEach(function (g, i) {
      var card = h("button", { class: "grave", style: "--i:" + i, "aria-expanded": "false" }, [
        h("span", { class: "grave-rip mono", text: "retracted" }),
        h("h3", { text: g.title }),
        h("p", { class: "grave-death", text: g.death }),
        h("span", { class: "grave-id mono", text: g.id })
      ]);
      card.addEventListener("click", function () {
        var open = card.classList.toggle("open");
        card.setAttribute("aria-expanded", String(open));
      });
      host.appendChild(card);
    });
    whenVisible(host, function () { host.classList.add("drawn"); }, 0.15);
  })();

  /* ---- SEAL GALLERY: real corpus rows as tilting clay seals ---------- */
  (function () {
    var host = document.getElementById("seals"); if (!host) return;
    var fine = window.matchMedia("(pointer: fine)").matches;
    D.SEALS.forEach(function (sl, i) {
      var cut = sl.tail ? sl.text.length - sl.tail : -1;
      var band = s("svg", { viewBox: "0 0 " + (sl.text.length * 40) + " 48", class: "seal-band", "aria-hidden": "true" });
      sl.text.forEach(function (code, j) {
        var key = D.GLYPH_KEYS[(parseInt(code, 10) || j) % D.GLYPH_KEYS.length];
        var g = s("g", { transform: "translate(" + (j * 40 + 4) + ",6) scale(0.56)", class: "seal-glyph" + (cut >= 0 && j >= cut ? " tail" : "") });
        g.appendChild(s("path", { d: D.GLYPHS[key] }));
        band.appendChild(g);
      });
      var codes = cut >= 0
        ? h("div", { class: "seal-codes mono" }, [
            h("span", { text: "+" + sl.text.slice(0, cut).join("-") + "-" }),
            h("span", { class: "tailseg", text: sl.text.slice(cut).join("-") + "+" })
          ])
        : h("div", { class: "seal-codes mono", text: "+" + sl.text.join("-") + "+" });
      var card = h("article", { class: "seal is-" + sl.status, style: "--i:" + i, tabindex: "0" }, [
        h("div", { class: "seal-face" }, [
          band,
          codes,
          h("div", { class: "seal-meta" }, [
            h("b", { text: sl.obj }),
            h("span", { class: "mono", text: sl.site + " · " + sl.row })
          ]),
          h("span", { class: "seal-status mono", text: sl.status })
        ]),
        h("p", { class: "seal-note", text: sl.note })
      ]);
      if (fine && !reduce) {
        var face = card.querySelector(".seal-face");
        card.addEventListener("pointermove", function (e) {
          var r = card.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width - 0.5, py = (e.clientY - r.top) / r.height - 0.5;
          face.style.transform = "rotateX(" + (-py * 9) + "deg) rotateY(" + (px * 11) + "deg)";
        });
        card.addEventListener("pointerleave", function () { face.style.transform = ""; });
      }
      host.appendChild(card);
    });
    whenVisible(host, function () { host.classList.add("drawn"); }, 0.12);
  })();

  /* ---- EASTER EGG: type "dig" anywhere ------------------------------- */
  (function () {
    if (reduce) return;
    var buf = "", veil = null;
    document.addEventListener("keydown", function (e) {
      if (e.target && /input|textarea|select/i.test(e.target.tagName)) return;
      if (e.key === "Escape" && veil) { off(); return; }
      buf = (buf + (e.key || "").toLowerCase()).slice(-3);
      if (buf === "dig") { veil ? off() : on(); buf = ""; }
    });
    function on() {
      veil = h("div", { class: "veil", "aria-hidden": "true" });
      var note = h("div", { class: "veil-note mono", text: "site lamp on — move to survey · type DIG or press ESC to stop digging" });
      veil._note = note;
      document.body.appendChild(veil);
      document.body.appendChild(note);
      document.addEventListener("pointermove", track, { passive: true });
      requestAnimationFrame(function () { veil.classList.add("on"); note.classList.add("on"); });
    }
    function off() {
      document.removeEventListener("pointermove", track);
      if (veil) {
        var v = veil, n = veil._note; veil = null;
        v.classList.remove("on"); n.classList.remove("on");
        setTimeout(function () { v.remove(); n.remove(); }, 450);
      }
    }
    function track(e) {
      if (veil) { veil.style.setProperty("--lx", e.clientX + "px"); veil.style.setProperty("--ly", e.clientY + "px"); }
    }
  })();

  /* ---- console gift -------------------------------------------------- */
  try {
    console.log(
      "%c  +002-861-533-717+  %c\n" +
      "One structure earned. Zero readings claimed.\n" +
      "Every gate, every retraction, every dead end: github.com/Cuuper22/ivc\n" +
      "(psst - type the word 'dig' on the page.)",
      "font-family:monospace;font-size:14px;padding:6px 10px;background:#143;color:#7fd9cb;border-radius:6px", ""
    );
  } catch (e) {}

})();
