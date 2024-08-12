import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.118/build/three.module.js';
import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.118/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/loaders/GLTFLoader.js";
import { Earcut } from "https://cdn.jsdelivr.net/npm/three@0.121.1/src/extras/Earcut.js";
import { Timer } from 'https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/misc/Timer.js';
import { WS } from './static/js/websocket.js';


var camera_position
var timer = new Timer();
const _WS = new WS();

class Warehouse{
  constructor(Warehouse) {
    this._Initialize();
  }

  _Initialize() {
    this._threejs = new THREE.WebGLRenderer({
      antialias: true,
    });
    this._threejs.shadowMap.enabled = true;
    this._threejs.shadowMap.type = THREE.PCFSoftShadowMap;
    this._threejs.setPixelRatio(window.devicePixelRatio);

    this._threejs.setSize( window.innerWidth, window.innerHeight); 
    document.getElementById("app").appendChild(this._threejs.domElement);

    window.addEventListener('resize', () => {
      this._OnWindowResize();
      this._threejs.setSize( window.innerWidth, window.innerHeight ); 
    }, false);

    this._scene = new THREE.Scene();

    const fov = {{ camera.fild_of_view }};
    const aspect = {{ camera.aspect_ratio }};
    const near = {{ camera.clipping_plane_near }};
    const far = {{ camera.clipping_plane_far }};
    this._camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
      this._camera.position.set(
        {{ camera.position['x'] }},
        {{ camera.position['y'] }},
        {{ camera.position['z'] }}
      );


    const controls = new OrbitControls(
      this._camera, this._threejs.domElement);
    controls.target.set(0, 20, 0);
    controls.update();

    const loader = new THREE.CubeTextureLoader();
    const textur = loader.load([
        '{{ url_for('static', filename='textures/skybox/posx.png') }}',
        '{{ url_for('static', filename='textures/skybox/negx.png') }}',
        '{{ url_for('static', filename='textures/skybox/posy.png') }}',
        '{{ url_for('static', filename='textures/skybox/negy.png') }}',
        '{{ url_for('static', filename='textures/skybox/posz.png') }}',
        '{{ url_for('static', filename='textures/skybox/negz.png') }}'
    ]);

    this._scene.background = textur;

    //const box = new THREE.Mesh(
      //new THREE.BoxGeometry(5, 5, 5),
      //new THREE.MeshStandardMaterial({
          //color: 0xFFFFFF,
      //}));
    //box.position.set(54.43783, 10, 85.1159569);
    //box.castShadow = true;
    //box.receiveShadow = true;
    //this._scene.add(box);
    
    this._LoadLight( {{ light }} );
    // this._LoadModel( {{ model }} );
    this._DrawEdges( {{ line }} );
    this._LoadEntity( {{ entity }} );
    this._DrawFigure( {{ figure }} );
    this._DrawArch( {{ arch }} );
    //this._DrawTriangls( {{ figure }} );
    this._RAF();
  };

    _DrawArch(data){
        for (const [key, value] of Object.entries(data)) {
            
          const vertices = new Float32Array( value.vertices );
          
          const indices = value.faces;


          const material = new THREE[value.material_type](value.material);

          const geometry = new THREE.BufferGeometry();
          geometry.setIndex( indices );

          geometry.setAttribute( 'position', new THREE.BufferAttribute( vertices, 3 ) );

          const mesh = new THREE.Mesh( geometry, material );
          mesh.rotation.set(...Object.values(value.rotation));
          this._scene.add( mesh )
        
        }
    };

    _DrawTriangls(data){
        for (const [key, value] of Object.entries(data)) {
            var vertices = new Float32Array(value.vertices.flat())
            var holes = [];
            var geometry = new THREE.BufferGeometry();
            
            var indices = Earcut.triangulate(vertices, [], 3);
            
            geometry.setAttribute( 'position', new THREE.BufferAttribute( vertices, 2 ) );
            geometry.setIndex(indices);
            //console.log('indices', indices)
            const material = new THREE[value.material_type](value.material);
            const mesh = new THREE.Mesh( geometry, material );
            //console.log(geometry)
            this._scene.add( mesh )

                
        }
    };
    _DrawFigure( data ) {

        for (const [key, value] of Object.entries(data)) {
          var points3d = [];
          value.vertices.forEach((raw) => {
            raw.forEach((coord) => {
              points3d.push(new THREE.Vector3(coord[0], coord[1], coord[2]));  
            })
          })
          
          var geom = new THREE.BufferGeometry().setFromPoints(points3d);
          var cloud = new THREE.Points(
            geom,
            new THREE.PointsMaterial({ color: 0x99ccff, size: 2 })
          );
          this._scene.add( cloud );

          // triangulate x, z
          var indexDelaunay = Delaunator.from(
            points3d.map(v => {
              return [v.x, v.z];
            })
          );

          var meshIndex = []; // delaunay index => three.js index
          for (let i = 0; i < indexDelaunay.triangles.length; i++){
            meshIndex.push(indexDelaunay.triangles[i]);
          }

          geom.setIndex(meshIndex); // add three.js index to the existing geometry
          geom.computeVertexNormals();
          var mesh = new THREE.Mesh(
            geom, // re-use the existing geometry
            new THREE.MeshLambertMaterial({ color: "purple", wireframe: true })
          );
          this._scene.add(mesh);

        }
    }

  _LoadModel_v1(data) {
    for (const [key, value] of Object.entries(data)) {
      const model_loader = new GLTFLoader();
      model_loader.load(
          value.path
            , (gltf) => {
        gltf.scene.traverse(c => {
          c.castShadow = value.castShadow;
          c.receiveShadow = value.receiveShadow;
          c.name = key;
        });
        gltf.scene.position.set(...Object.values(value.position));
        gltf.scene.rotation.set(...Object.values(value.rotation));
        this._scene.add(gltf.scene);
      });
    }
  }

  _LoadModel(data) {
    for (const [name, coordinates] of Object.entries(data)) {

      
      const model = this._scene.getObjectByName(name)
      console.log(this._scene.getObjectByName(name))

      if (model){
        console.log('update')
        model.position.set(...Object.values(coordinates.position));
        model.rotation.set(...Object.values(coordinates.rotation));

      }else{

        console.log('create')
        const model_loader = new GLTFLoader();
        model_loader.load(
          './static/3d_models/cat/scene.gltf'
            , (gltf) => {
        gltf.scene.traverse(c => {
          c.castShadow = true;
          c.receiveShadow = true;
          c.name = name;
        });
        gltf.scene.position.set(...Object.values(coordinates.position));
        gltf.scene.rotation.set(...Object.values(coordinates.rotation));
        this._scene.add(gltf.scene);
        });
      };
    };
  };

  _LoadModel_v3(coordinates) {
    const model_loader = new GLTFLoader();
    model_loader.load(
        './static/3d_models/cat/scene.gltf'
          , (gltf) => {
      gltf.scene.traverse(c => {
        // c.castShadow = true;
        // c.receiveShadow = true;
        c.name = "model";
      });
      gltf.scene.position.set(...Object.values(coordinates));
      // gltf.scene.rotation.set(...Object.values(value.rotation));
      this._scene.add(gltf.scene);
    });
  }

    _DrawEdges(data) {
        for (const [key, value] of Object.entries(data)) {
            const points = [];

            const material = new THREE[value.material_type]({
                color: value.color 
            });

            points.push( new THREE.Vector3( ...Object.values(value.position1)) );
            points.push( new THREE.Vector3( ...Object.values(value.position2)) );

            const geometry = new THREE[value.geometry_type]().setFromPoints( points );

            const line = new THREE.Line( geometry, material );
            this._scene.add( line );
            
         }
    }

     //create light from json
    _LoadLight(data) {
         //draw all shapes from source
        for (const [key, value] of Object.entries(data)) {
            const light = new THREE[value.light_type](
                value.color, 
                value.intencity
            ); 
            light.name = key;

            if (value.light_type == 'DirectionalLight') {
                light.position.set(...Object.values(value.position));
                light.target.position.set(...Object.values(value.target_position));
                light.castShadow = value.castShadow;
                

                light.shadow.bias = light.shadow.bias;
                light.shadow.mapSize = light.shadow.mapSize;
                light.shadow.bias = value.shadow.bias;
                light.shadow.mapSize.width = value.shadow.mapSize.width;
                light.shadow.mapSize.height = value.shadow.mapSize.height;
                light.shadow.camera.near = value.shadow.camera.near;
                light.shadow.camera.far = value.shadow.camera.far;
                light.shadow.camera.left = value.shadow.camera.left;
                light.shadow.camera.right = value.shadow.camera.right;
                light.shadow.camera.top = value.shadow.camera.top;
                light.shadow.camera.bottom = value.shadow.camera.bottom;

                this._scene.add(light);
            }else if (value.light_type == 'AmbientLight'){
                this._scene.add(light);
            }
        }
    }
     //create shapes from json
    _LoadEntity(data) {
         //draw all shapes from source
        for (const [key, value] of Object.entries(data)) {
             //draw color or texture
            let material;
            if ('texture' in value.material){
                material = 
                    new THREE[value.material_type]
                  ({ map: new THREE.TextureLoader().load('{{ url_for('static', filename='textures/blueprint.jpg') }}'),
                  side: THREE.DoubleSide,
                  //encoding: THREE.sRGBEncoding,
                  transparent: true,
                  opacity: 0.8,
                  //color: 0x004F00
                  }); // put it to python platform_class
                
            }else{
                material = new THREE[value.material_type](value.material);
            }

            const figure = new THREE[value.geometry_type](...Object.values(value.geometry));
            const mesh = new THREE.Mesh(figure, material);
            mesh.name = key;
            mesh.castShadow = value.castShadow
            mesh.receiveShadow = value.receiveShadow
            this._scene.add(mesh);

             //add mesh position
            mesh.position.set(...Object.values(value.position));

             //add mesh rotation
            mesh.rotation.set(...Object.values(value.rotation));
        }
    }

  _OnWindowResize() {
    this._camera.aspect = {{ camera.aspect_ratio }};
    this._camera.updateProjectionMatrix();

    document.getElementById('control').width = 38
    this._threejs.setSize(innerWidth, innerHeight - document.getElementById('control').width);
  }

  _RemoveEntitys() {
    // console.log(this._scene.children);
    while(this._scene.children.length > 0){ 
      this._scene.remove(this._scene.children[0]); 
    };
  };

  _RAF() {
    timer.update();

    async function get_entities() {
      let url_entitys = 'http://127.0.0.1:8200/entitys'
      let response = await fetch(url_entitys)

      if (response.ok) { // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа (см. про этот метод ниже)
        let entities = await response.json();

        return entities;

      } else {
        console.log('Error!')
        alert("Ошибка HTTP: " + response.status);
      }
    };

    requestAnimationFrame(async () => {

      // Send camera position for draw enother plaers avatars
      if (camera_position != JSON.stringify(this._camera.position)){
        _WS._sendMessage(JSON.stringify({'user_position': {'{{ user }}': {'position': this._camera.position, 'rotation': this._camera.rotation}}}));
        camera_position = JSON.stringify(this._camera.position)
      };

      const receivedData = _WS.getReceivedData();
      if (receivedData && receivedData != "{}"){
        // console.log("Accessed received data:", receivedData);
        var coords = JSON.parse(receivedData)
        this._LoadModel( coords );
      }

      this._threejs.render(this._scene, this._camera);
      this._RAF();
    });
  };
};

let _APP = null;

window.addEventListener('DOMContentLoaded', () => {

  _APP = new Warehouse();

  // Пример отправки сообщения
  document.getElementById('mylink').addEventListener('click', function() {
    var message = "Привет1"
    _WS._sendMessage(message);
  });
});
