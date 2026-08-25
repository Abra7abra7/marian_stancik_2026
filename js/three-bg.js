
import * as THREE from 'three';
const canvas = document.getElementById('three-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
const count = 1800;
const positions = new Float32Array(count * 3);
const colors = new Float32Array(count * 3);
for (let i = 0; i < count; i++) {
const r = 30 + Math.random() * 40;
const theta = Math.random() * Math.PI * 2;
const phi = Math.acos(2 * Math.random() - 1);
positions[i*3] = r * Math.sin(phi) * Math.cos(theta);
positions[i*3+1] = r * Math.cos(phi) * Math.sin(theta * 0.5);
positions[i*3+2] = r * Math.sin(phi) * Math.sin(theta);
const bronze = new THREE.Color().setHSL(0.08, 0.4, 0.3 + Math.random() * 0.35);
colors[i*3] = bronze.r; colors[i*3+1] = bronze.g; colors[i*3+2] = bronze.b;
}
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
const material = new THREE.PointsMaterial({
size: 0.12, vertexColors: true, transparent: true, opacity: 0.6,
blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true,
});
const particles = new THREE.Points(geometry, material);
scene.add(particles);
const linePositions = [];
for (let i = 0; i < count; i++) {
for (let j = i + 1; j < count; j++) {
if (Math.random() > 0.997) {
const dx = positions[i*3] - positions[j*3];
const dy = positions[i*3+1] - positions[j*3+1];
const dz = positions[i*3+2] - positions[j*3+2];
if (Math.sqrt(dx*dx + dy*dy + dz*dz) < 12) {
linePositions.push(positions[i*3], positions[i*3+1], positions[i*3+2]);
linePositions.push(positions[j*3], positions[j*3+1], positions[j*3+2]);
}
}
}
}
const lineGeo = new THREE.BufferGeometry();
lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
const lines = new THREE.LineSegments(lineGeo, new THREE.LineBasicMaterial({ color: 0xCD7F32, transparent: true, opacity: 0.06 }));
scene.add(lines);
camera.position.z = 45;
const nodeMat = new THREE.MeshBasicMaterial({ color: 0xCD7F32, transparent: true, opacity: 0.12 });
const nodeGeom = new THREE.SphereGeometry(0.3, 8, 8);
const nodes = [];
for (let i = 0; i < 40; i++) {
const mesh = new THREE.Mesh(nodeGeom, nodeMat.clone());
const idx = Math.floor(Math.random() * count);
mesh.position.set(positions[idx*3], positions[idx*3+1], positions[idx*3+2]);
mesh.userData = { baseX: positions[idx*3], baseY: positions[idx*3+1], baseZ: positions[idx*3+2], speed: 0.2 + Math.random() * 0.5 };
scene.add(mesh);
nodes.push(mesh);
}
let mouseX = 0, mouseY = 0;
document.addEventListener('mousemove', (e) => {
mouseX = (e.clientX / window.innerWidth) * 2 - 1;
mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
});
window.addEventListener('resize', () => {
camera.aspect = window.innerWidth / window.innerHeight;
camera.updateProjectionMatrix();
renderer.setSize(window.innerWidth, window.innerHeight);
});
let time = 0;
let isAnimating = true;
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function animate() {
if (!isAnimating) return;
requestAnimationFrame(animate);
time += 0.001;
particles.rotation.y += 0.0003;
lines.rotation.y += 0.0003;
nodes.forEach((node, i) => {
const d = node.userData;
node.position.x = d.baseX + Math.sin(time * d.speed + i) * 1.5;
node.position.y = d.baseY + Math.cos(time * d.speed * 0.7 + i * 0.5) * 1.5;
node.position.z = d.baseZ + Math.sin(time * d.speed * 0.5 + i * 0.3) * 1.5;
node.material.opacity = 0.08 + Math.sin(time * 2 + i) * 0.06;
});
particles.rotation.x += (mouseY * 0.02 - particles.rotation.x) * 0.02;
particles.rotation.y += (mouseX * 0.02 - particles.rotation.y) * 0.02;
lines.rotation.x = particles.rotation.x;
lines.rotation.y = particles.rotation.y;
renderer.render(scene, camera);
}
document.addEventListener('visibilitychange', () => {
if (document.hidden) {
isAnimating = false;
} else {
if (!isAnimating && !prefersReducedMotion) {
isAnimating = true;
animate();
}
}
});
if (prefersReducedMotion) {
renderer.render(scene, camera);
} else {
animate();
}
