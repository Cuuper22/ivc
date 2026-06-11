/* IVC site — interactions with graceful degradation.
   Reveals/progress/dial/count-up are pure vanilla (work with no CDN).
   GSAP, if it loads, only enhances the hero seal, marquee, and scan.    */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.classList.add("js");

  /* ---- Scroll progress + sticky nav -------------------------------- */
  var progress = document.getElementById("progress");
  var nav = document.getElementById("nav");
  function onScroll() {
    var st = window.scrollY || document.documentElement.scrollTop;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var p = h > 0 ? st / h : 0;
    if (progress) progress.style.transform = "scaleX(" + p + ")";
    if (nav) nav.classList.toggle("is-stuck", st > 48);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---- Reveal on scroll (IntersectionObserver, no dependency) ------ */
  var reveals = [].slice.call(document.querySelectorAll(".reveal"));
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---- Expertise dials (zip each .dial with each .levels by order) -- */
  var dials = [].slice.call(document.querySelectorAll(".dial"));
  var levelSets = [].slice.call(document.querySelectorAll(".levels"));
  dials.forEach(function (dial, i) {
    var levels = levelSets[i];
    if (!levels) return;
    var btns = [].slice.call(dial.querySelectorAll("button"));
    dial.addEventListener("click", function (ev) {
      var btn = ev.target.closest("button");
      if (!btn) return;
      var lvl = btn.getAttribute("data-level");
      btns.forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
      [].slice.call(levels.querySelectorAll(".level")).forEach(function (panel) {
        panel.classList.toggle("is-active", panel.getAttribute("data-level") === lvl);
      });
    });
  });

  /* ---- Count-up on the scoreboard ---------------------------------- */
  var board = document.getElementById("scoreboard");
  function runCount() {
    [].slice.call(board.querySelectorAll("[data-count]")).forEach(function (el) {
      var target = parseInt(el.getAttribute("data-count"), 10) || 0;
      if (reduce || target === 0) { el.textContent = String(target); return; }
      var start = performance.now(), dur = 900;
      function step(now) {
        var t = Math.min(1, (now - start) / dur);
        var eased = 1 - Math.pow(1 - t, 3);
        el.textContent = String(Math.round(eased * target));
        if (t < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }
  if (board) {
    if (reduce || !("IntersectionObserver" in window)) { runCount(); }
    else {
      var bo = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { runCount(); bo.disconnect(); } });
      }, { threshold: 0.4 });
      bo.observe(board);
    }
  }

  /* ---- GSAP enhancements (optional) -------------------------------- */
  window.addEventListener("load", function () {
    if (reduce || typeof window.gsap === "undefined") return;
    var gsap = window.gsap;

    // hero seal: tokens settle into place like a seal pressing into clay
    var seal = document.querySelectorAll("#heroSeal .glyph");
    if (seal.length) {
      gsap.from(seal, {
        y: 14, opacity: 0, scale: 0.94, duration: 0.7, ease: "expo.out",
        stagger: 0.08, delay: 0.15
      });
      var verified = document.querySelectorAll("#heroSeal .glyph.is-verified");
      gsap.to(verified, {
        boxShadow: "inset 0 1px 0 rgba(255,255,255,0.06), 0 0 22px rgba(120,220,210,0.35)",
        duration: 1.4, delay: 0.9, ease: "sine.inOut", yoyo: true, repeat: -1
      });
    }

    // scan sweep across the hero
    var scan = document.getElementById("scan");
    var hero = document.getElementById("hero");
    if (scan && hero) {
      gsap.set(scan, { top: 0 });
      gsap.to(scan, {
        top: "100%", duration: 5.5, ease: "none", repeat: -1,
        yoyo: true
      });
    }

    // seamless marquee
    var track = document.getElementById("marquee");
    if (track && track.firstElementChild) {
      var clone = track.firstElementChild.cloneNode(true);
      clone.setAttribute("aria-hidden", "true");
      track.appendChild(clone);
      var w = track.firstElementChild.getBoundingClientRect().width;
      gsap.to(track, { x: -w, duration: 26, ease: "none", repeat: -1 });
    }

    // faint parallax on the hero grid
    if (window.ScrollTrigger) {
      gsap.registerPlugin(window.ScrollTrigger);
      gsap.to(".hero-grid", {
        yPercent: 14, ease: "none",
        scrollTrigger: { trigger: "#hero", start: "top top", end: "bottom top", scrub: true }
      });
    }
  });
})();
