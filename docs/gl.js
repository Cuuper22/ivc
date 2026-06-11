/* =========================================================================
   Custom WebGL background: a slowly shifting eroded-clay / excavated-stone
   surface built from domain-warped fractal noise, tinted to the ink/clay/
   patina theme. Raw WebGL, no library. Falls back silently if unsupported
   or if the user prefers reduced motion.
   ========================================================================= */
(function () {
  var canvas = document.getElementById("gl");
  if (!canvas) return;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var gl = canvas.getContext("webgl", { antialias: false, alpha: true, premultipliedAlpha: false });
  if (!gl) { canvas.classList.add("gl-fallback"); return; }

  var vert = "attribute vec2 p; void main(){ gl_Position = vec4(p,0.0,1.0); }";

  var frag = [
    "precision highp float;",
    "uniform vec2 u_res; uniform float u_time; uniform float u_scroll; uniform vec2 u_mouse;",
    // hash + value noise
    "float hash(vec2 p){ p=fract(p*vec2(123.34,345.45)); p+=dot(p,p+34.345); return fract(p.x*p.y); }",
    "float noise(vec2 p){ vec2 i=floor(p); vec2 f=fract(p); vec2 u=f*f*(3.0-2.0*f);",
    "  float a=hash(i), b=hash(i+vec2(1,0)), c=hash(i+vec2(0,1)), d=hash(i+vec2(1,1));",
    "  return mix(mix(a,b,u.x),mix(c,d,u.x),u.y); }",
    "float fbm(vec2 p){ float v=0.0, a=0.5; mat2 m=mat2(1.6,1.2,-1.2,1.6);",
    "  for(int i=0;i<6;i++){ v+=a*noise(p); p=m*p; a*=0.5; } return v; }",
    "void main(){",
    "  vec2 uv = gl_FragCoord.xy/u_res.xy;",
    "  vec2 p = uv; p.x *= u_res.x/u_res.y;",
    "  float t = u_time*0.015;",
    // domain warp -> erosion/striation
    "  vec2 q = vec2(fbm(p*2.4 + t), fbm(p*2.4 + vec2(5.2,1.3) - t));",
    "  vec2 r = vec2(fbm(p*2.4 + 3.0*q + vec2(1.7,9.2) + 0.05*u_mouse), fbm(p*2.4 + 3.0*q + vec2(8.3,2.8)));",
    "  float f = fbm(p*2.4 + 3.5*r + u_scroll*0.4);",
    "  float strata = 0.5 + 0.5*sin( (uv.y*1.0 + f*1.2 + u_scroll*0.6)*9.0 );",
    "  strata = pow(strata, 3.0)*0.06;",
    // palette: deep ink -> fired clay in shadow -> faint patina veins.
    // kept dark on purpose so foreground text always stays legible.
    "  vec3 ink  = vec3(0.040,0.036,0.032);",
    "  vec3 clay = vec3(0.205,0.115,0.066);",
    "  vec3 patina = vec3(0.10,0.255,0.235);",
    "  vec3 col = mix(ink, clay, smoothstep(0.32,0.98,f));",
    "  col = mix(col, patina, smoothstep(0.62,0.90,r.x)*0.16);",
    "  col += strata;",
    // vignette + grain
    "  float vig = smoothstep(1.10,0.12,length(uv-0.5));",
    "  col *= 0.42 + 0.58*vig;",
    "  col += (hash(gl_FragCoord.xy+u_time)-0.5)*0.018;",
    "  gl_FragColor = vec4(col, 1.0);",
    "}"
  ].join("\n");

  function compile(type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { return null; }
    return s;
  }
  var vs = compile(gl.VERTEX_SHADER, vert), fs = compile(gl.FRAGMENT_SHADER, frag);
  if (!vs || !fs) { canvas.classList.add("gl-fallback"); return; }
  var prog = gl.createProgram();
  gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { canvas.classList.add("gl-fallback"); return; }
  gl.useProgram(prog);

  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 3,-1, -1,3]), gl.STATIC_DRAW);
  var loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

  var uRes = gl.getUniformLocation(prog, "u_res");
  var uTime = gl.getUniformLocation(prog, "u_time");
  var uScroll = gl.getUniformLocation(prog, "u_scroll");
  var uMouse = gl.getUniformLocation(prog, "u_mouse");

  var scale = 0.5; // render at half res for performance
  var mouse = [0, 0], scroll = 0;
  function resize() {
    var w = Math.floor(canvas.clientWidth * scale), h = Math.floor(canvas.clientHeight * scale);
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; gl.viewport(0, 0, w, h); }
  }
  window.addEventListener("resize", resize);
  window.addEventListener("scroll", function () {
    var max = document.documentElement.scrollHeight - window.innerHeight;
    scroll = max > 0 ? (window.scrollY / max) : 0;
  }, { passive: true });
  window.addEventListener("pointermove", function (e) {
    mouse = [(e.clientX / window.innerWidth - 0.5) * 2, (e.clientY / window.innerHeight - 0.5) * 2];
  }, { passive: true });

  resize();
  var start = performance.now();

  function frame(now) {
    resize();
    var t = (now - start) / 1000;
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uTime, reduce ? 12.0 : t);   // reduced motion: a single frozen frame look
    gl.uniform1f(uScroll, scroll);
    gl.uniform2f(uMouse, mouse[0], mouse[1]);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    if (!reduce) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
