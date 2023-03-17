import * as THREE from "/../../node_modules/three/build/three.module.js"; /* Import the three.js module */
import { OBJLoader } from "/../../node_modules/three/examples/jsm/loaders/OBJLoader.js"; /* Import the OBJLoader module */
import { OrbitControls } from "/../../node_modules/three/examples/jsm/controls/OrbitControls.js"; /* Import the OrbitControls module */
import { MTLLoader } from "/../../node_modules/three/examples/jsm/loaders/MTLLoader.js"; /* Import the MTLLoader module */

export default
class modelManagement {

    constructor(canvasID, width=600, height=400) {
        /* CanvasID validation */
        if (typeof canvasID !== "string") {
            throw new Error("The canvasID must be a string");
        }
        var canvas = document.getElementById(canvasID);
        if (canvas === null) {
            throw new Error("The canvasID must be the ID of an existing element");
        }
        
        /* Width validation */
        if (typeof width !== "number") {
            throw new Error("The width must be a number");
        }
        if (width <= 0) {
            throw new Error("The width must be more than 0");
        }
        this.width = width;

        /* Height validation */
        if (typeof height !== "number") {
            throw new Error("The height must be a number");
        }
        if (height <= 0) {
            throw new Error("The height must be more than 0");
        }
        this.height = height;

        /* Set up the scene */
        this.scene = new THREE.Scene();
        this.renderer = new THREE.WebGLRenderer({
            antialiasing: true,
            canvas: canvas
        });
        this.renderer.setSize(width, height);
        this.renderer.setClearColor(0x000000, 1);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

        /* Set up the light */
        var light = new THREE.DirectionalLight(0xffffff,1);
        light.position.set(5, 10, 8);
        light.castShadow = true;
        light.shadow.mapSize = new THREE.Vector2(2048, 2048);
        light.shadow.camera.near = 0.5;
        light.shadow.camera.far = 500;
        this.scene.add(light);

        /* Set up the camera*/
        this.camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 100);
        this.camera.position.set(0, 5, 10);

        /* Define controller for rotating around objects and zooming */
        this.controls = new OrbitControls(this.camera, canvas);
        this.controls.enableZoom = true; /* enable zooming */

        /* Define the ground */
        var ground = new THREE.Mesh(
            new THREE.PlaneGeometry(25, 25),
            new THREE.MeshStandardMaterial({
                color: 0xe1e1e1,
            })
        );
        ground.castShadow = false;
        ground.receiveShadow = true;
        ground.rotation.x = -Math.PI / 2;
        this.scene.add(ground);

        /* Define the model reference and put it to null */
        this.model = null;

        this.animate();
    }

    animate() {
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
        requestAnimationFrame(this.animate);
    }

    applyTextureToModelFromMTL(modelURL, mtlURL) {
    }

    applyTextureToModelFromImage(modelURL, imageURL) {
    }

    applyTextureToModelFromColor(modelURL, colorHex) {
    }
    

    removeModelFromScene() {
        if (this.model !== null) {
            this.scene.remove(this.model);
            this.model = null;
        }
    }

    loadModelInScene(modelURL) {
        var loader = new OBJLoader();
        loader.load(
            modelURL,
            (model) => {
                this.model = model;
                var refBox = new THREE.Box3().setFromObject(this.model);
                var translateVector = new THREE.Vector3(
                    refBox.min.x + (refBox.max.x - refBox.min.x) / 2,
                    refBox.min.y,
                    refBox.min.z + (refBox.max.z - refBox.min.z) / 2
                );
                this.model.traverse((obj) => {
                    if (obj instanceof THREE.Mesh) {
                        obj.castShadow = true;
                        obj.translateX(-translateVector.x);
                        obj.translateY(-translateVector.y);
                        obj.translateZ(-translateVector.z);
                    }
                });
                this.scene.add(this.model);
            },
            (xhr) => {
                console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
            },
            (error) => {
                throw new Error("An error occured while loading the model");
            }
        );
    }
}