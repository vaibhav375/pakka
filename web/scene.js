/* The rule constellation.

   Twenty nodes, one per rule, sitting on a sphere. Idle, they drift dim. Run a
   scan and the rules that fired ignite and wire themselves back to the core, so
   the picture is the pipeline doing its job rather than an ornament bolted to
   the page. */
(() => {
  const host = document.getElementById('scene');
  if (!host || !window.THREE || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const RULES = window.PAKKA_RULES || [];
  const N = RULES.length || 20;
  const DIM = new THREE.Color('#3a3a46');
  const HOT = new THREE.Color('#ff5d47');
  const CORE = new THREE.Color('#c6ff3d');

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(46, 1, 0.1, 100);
  camera.position.z = 5.2;
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  host.appendChild(renderer.domElement);

  const group = new THREE.Group();
  scene.add(group);

  /* evenly spread points — a fibonacci sphere, so nothing clumps */
  const pos = [], base = [];
  for (let i = 0; i < N; i++) {
    const y = 1 - (i / (N - 1)) * 2;
    const r = Math.sqrt(Math.max(0, 1 - y * y));
    const th = Math.PI * (3 - Math.sqrt(5)) * i;
    const v = new THREE.Vector3(Math.cos(th) * r, y, Math.sin(th) * r).multiplyScalar(1.85);
    base.push(v); pos.push(v.x, v.y, v.z);
  }

  const nodeGeo = new THREE.BufferGeometry();
  nodeGeo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  const colors = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) DIM.toArray(colors, i * 3);
  nodeGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const nodes = new THREE.Points(nodeGeo, new THREE.PointsMaterial({
    size: 0.16, vertexColors: true, transparent: true, opacity: 0.95,
    sizeAttenuation: true, depthWrite: false,
  }));
  group.add(nodes);

  /* faint shell so the sphere reads as a volume, not scattered dots */
  group.add(new THREE.LineSegments(
    new THREE.EdgesGeometry(new THREE.IcosahedronGeometry(1.85, 1)),
    new THREE.LineBasicMaterial({ color: '#1e1e26', transparent: true, opacity: 0.6 })
  ));

  const core = new THREE.Points(
    new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0], 3)),
    new THREE.PointsMaterial({ size: 0.34, color: CORE, transparent: true, opacity: 0.95, depthWrite: false })
  );
  group.add(core);

  let wires = null;
  const clearWires = () => { if (wires) { group.remove(wires); wires.geometry.dispose(); wires = null; } };

  /* light the rules that fired, and wire them home */
  window.PakkaScene = {
    light(firedIds = []) {
      const fired = new Set(firedIds);
      const pts = [];
      for (let i = 0; i < N; i++) {
        const on = RULES[i] && fired.has(RULES[i].id);
        (on ? HOT : DIM).toArray(colors, i * 3);
        if (on) pts.push(0, 0, 0, base[i].x, base[i].y, base[i].z);
      }
      nodeGeo.attributes.color.needsUpdate = true;
      clearWires();
      if (pts.length) {
        const g = new THREE.BufferGeometry();
        g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
        wires = new THREE.LineSegments(g, new THREE.LineBasicMaterial({
          color: HOT, transparent: true, opacity: 0.55,
        }));
        group.add(wires);
      }
      spin = 0.055;               /* a kick, which eases back to the idle drift */
    },
  };

  let mx = 0, my = 0, spin = 0.0022;
  host.addEventListener('mousemove', (e) => {
    const r = host.getBoundingClientRect();
    mx = ((e.clientX - r.left) / r.width - 0.5) * 0.6;
    my = ((e.clientY - r.top) / r.height - 0.5) * 0.6;
  });

  const size = () => {
    const w = host.clientWidth, h = host.clientHeight || 420;
    camera.aspect = w / h; camera.updateProjectionMatrix(); renderer.setSize(w, h, false);
  };
  size();
  addEventListener('resize', size, { passive: true });

  let visible = true;
  new IntersectionObserver((es) => (visible = es[0].isIntersecting)).observe(host);

  (function loop() {
    requestAnimationFrame(loop);
    if (!visible) return;
    spin += (0.0022 - spin) * 0.04;
    group.rotation.y += spin;
    group.rotation.x += (my - group.rotation.x) * 0.04;
    group.rotation.y += (mx - group.rotation.y) * 0.004;
    core.material.size = 0.3 + Math.sin(performance.now() / 420) * 0.05;
    renderer.render(scene, camera);
  })();
})();
