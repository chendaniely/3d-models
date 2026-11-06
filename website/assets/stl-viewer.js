// Turns each <div class="stl-viewer" data-stl="..."> into a 3D view of that STL:
// drag to rotate, scroll to zoom, right-drag to pan. three.js 0.187.0 is served from
// website/assets/three/ (copied from npm's package), named by the page's import map.
import * as THREE from "three";
import { STLLoader } from "three/addons/STLLoader.js";
import { OrbitControls } from "three/addons/OrbitControls.js";

const BONE = 0xf4f1ec;
const OAK = 0xc9b79c;

function mount(element) {
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio);
  element.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(BONE);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8178, 2.0));

  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 10000);
  const key = new THREE.DirectionalLight(0xffffff, 1.8);
  key.position.set(1, 2, 3);
  camera.add(key); // the light follows the camera, so every side is lit as it turns
  scene.add(camera);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;

  const resize = () => {
    const width = element.clientWidth;
    const height = element.clientHeight || Math.round(width * 2 / 3);
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(resize).observe(element);
  resize();

  new STLLoader().load(
    element.dataset.stl,
    (geometry) => {
      geometry.computeVertexNormals();
      geometry.center();
      const material = new THREE.MeshStandardMaterial({ color: OAK, roughness: 0.85 });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.rotation.x = -Math.PI / 2; // SolidCraft is Z-up; three.js is Y-up
      scene.add(mesh);
      const size = new THREE.Box3().setFromObject(mesh).getSize(new THREE.Vector3()).length();
      camera.near = size / 100;
      camera.far = size * 100;
      camera.position.set(size * 0.7, size * 0.6, size * 0.9);
      camera.updateProjectionMatrix();
      controls.update();
      element.dataset.loaded = "true";
    },
    undefined,
    () => {
      element.classList.add("stl-viewer-failed");
      element.textContent = "The 3D view didn't load; the picture below shows the model.";
    },
  );

  renderer.setAnimationLoop(() => {
    controls.update();
    renderer.render(scene, camera);
  });
}

document.querySelectorAll(".stl-viewer[data-stl]").forEach(mount);
