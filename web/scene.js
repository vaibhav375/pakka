/* Twenty rules as twenty points in space, and the verdict at the centre.
   When a scan runs, the checks that fired ignite and wire themselves to the
   middle. It is the rulebook seen from above rather than an ornament: the
   number of lit points is exactly the number of flags in the card below. */
(() => {
  const canvas = document.getElementById('gl');
  if (!canvas || !window.THREE || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const N = 20, ACID = 0xc6ff3d, BAD = 0xff5d47, DIM = 0x2a2a33;
  const scene = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(46, 2, 0.1, 100);
  cam.position.z = 7.2;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));

  const group = new THREE.Group();
  scene.add(group);

  /* fibonacci sphere: even spacing without clumping */
  const nodes = [];
  const golden = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < N; i++) {
    const y = 1 - (i / (N - 1)) * 2;
    const r = Math.sqrt(1 - y * y);
    const th = golden * i;
    const pos = new THREE.Vector3(Math.cos(th) * r, y, Math.sin(th) * r).multiplyScalar(2.6);
    const mesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.062, 14, 14),
      new THREE.MeshBasicMaterial({ color: DIM })
    );
    mesh.position.copy(pos);
    group.add(mesh);
    nodes.push({ mesh, pos, lit: false });
  }

  /* faint lattice between neighbours, so it reads as one structure */
  const lattice = [];
  for (let i = 0; i < N; i++)
    for (let j = i + 1; j < N; j++)
      if (nodes[i].pos.distanceTo(nodes[j].pos) < 2.15) lattice.push(nodes[i].pos, nodes[j].pos);
  group.add(new THREE.LineSegments(
    new THREE.BufferGeometry().setFromPoints(lattice),
    new THREE.LineBasicMaterial({ color: DIM, transparent: true, opacity: 0.45 })
  ));

  const core = new THREE.Mesh(
    new THREE.SphereGeometry(0.17, 20, 20),
    new THREE.MeshBasicMaterial({ color: ACID })
  );
  scene.add(core) && group.add(core);

  let wires = null;
  const clearWires = () => { if (wires) { group.remove(wires); wires.geometry.dispose(); wires = null; } };

  /* index of every rule id, so a fired rule always lights the same point */
  let order = [];
  fetch('rules.json').then((r) => r.json())
    .then((rs) => (order = rs.map((r) => r.id))).catch(() => {});

  window.pakkaScene = (firedIds, band) => {
    const hot = band === 'clear' ? ACID : BAD;
    nodes.forEach((n) => { n.lit = false; n.mesh.material.color.setHex(DIM); n.mesh.scale.setScalar(1); });
    const pts = [];
    firedIds.forEach((id) => {
      const idx = order.indexOf(id);
      const n = nodes[idx >= 0 ? idx : Math.abs(hash(id)) % N];
      n.lit = true;
      n.mesh.material.color.setHex(hot);
      n.mesh.scale.setScalar(1.9);
      pts.push(new THREE.Vector3(0, 0, 0), n.pos);
    });
    core.material.color.setHex(hot);
    clearWires();
    if (pts.length) {
      wires = new THREE.LineSegments(
        new THREE.BufferGeometry().setFromPoints(pts),
        new THREE.LineBasicMaterial({ color: hot, transparent: true, opacity: 0.75 })
      );
      group.add(wires);
    }
    const label = document.getElementById('glcount');
    if (label) label.textContent = firedIds.length;
  };

  const hash = (s) => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) | 0, 7);

  const size = () => {
    const r = canvas.getBoundingClientRect();
    if (!r.width) return;
    cam.aspect = r.width / r.height;
    cam.updateProjectionMatrix();
    renderer.setSize(r.width, r.height, false);
  };
  addEventListener('resize', size);
  size();

  let t = 0;
  (function loop() {
    t += 0.0042;
    group.rotation.y = t;
    group.rotation.x = Math.sin(t * 0.6) * 0.22;
    core.scale.setScalar(1 + Math.sin(t * 6) * 0.07);   /* a slow pulse, like a heartbeat */
    renderer.render(scene, cam);
    requestAnimationFrame(loop);
  })();
})();
