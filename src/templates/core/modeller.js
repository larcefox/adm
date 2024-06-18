import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.118/build/three.module.js';
import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.118/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/loaders/GLTFLoader.js";
import { Earcut } from "https://cdn.jsdelivr.net/npm/three@0.121.1/src/extras/Earcut.js";
import { Timer } from 'https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/misc/Timer.js';


var timer = new Timer();
var cur_tick;
var last_tick = 0;

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

    // document.getElementById('control').width = 38
    // this._threejs.setSize(innerWidth, innerHeight - document.getElementById('control').width);
    this._threejs.setSize( window.innerWidth / 1.3, window.innerHeight / 1.3 ); 

    document.getElementById("app").appendChild(this._threejs.domElement);

    window.addEventListener('resize', () => {
      this._OnWindowResize();
      this._threejs.setSize( window.innerWidth / 1.3, window.innerHeight / 1.3 ); 
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
        '{{ url_for('static', filename='textures/skybox/posx.jpg') }}',
        '{{ url_for('static', filename='textures/skybox/negx.jpg') }}',
        '{{ url_for('static', filename='textures/skybox/posy.jpg') }}',
        '{{ url_for('static', filename='textures/skybox/negy.jpg') }}',
        '{{ url_for('static', filename='textures/skybox/posz.jpg') }}',
        '{{ url_for('static', filename='textures/skybox/negz.jpg') }}'
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
    this._LoadModel( {{ model }} );
    this._DrawEdges( {{ line }} );
    //this._LoadEntity( {{ entity }} );
    //this._DrawFigure( {{ figure }} );
    //this._DrawShape( {{ figure }} );
    this._DrawTriangls( {{ figure }} );
    this._RAF();
  };

    _DrawShape(data){
        for (const [key, value] of Object.entries(data)) {
            //console.log(value.vertices)
            const path = new THREE.Path();

            path.moveTo( value.vertices[0][0], value.vertices[0][1] )
            value.vertices.forEach((coord) => {
                path.lineTo( coord[0], coord[1] );
                // console.log(coord[0], coord[1])
            })
            //path.quadraticCurveTo( 0, 1, 0.2, 1 );
            //path.lineTo( 1, 1 );
            //path.lineTo( 10, 10 );

            const points = path.getPoints();

            const geometry = new THREE.BufferGeometry().setFromPoints( points );
            const material = new THREE.LineBasicMaterial( { color: 0x00ff00 } );

            const line = new THREE.Line( geometry, material );
             //add mesh rotation
            line.rotation.set(...Object.values(value.rotation));
            this._scene.add( line )
        
        }
    };

    _DrawTriangls(data){
        for (const [key, value] of Object.entries(data)) {
            var vertices = new Float32Array(value.vertices.flat())
            var holes = [];
            var geometry = new THREE.BufferGeometry();
            
            var indices = Earcut.triangulate(vertices, [], 2);
            
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
            const shape = new THREE.Shape();

            shape.moveTo( value.vertices[0][0], value.vertices[0][1] )

            value.vertices.forEach((coord) => {
                shape.lineTo( coord[0], coord[1] );
            })
            //shape.lineTo( 0, width );
            //shape.lineTo( length, width );
            //shape.lineTo( length, 0 );
            //shape.lineTo( 0, 0 );

            const extrudeSettings = {
            steps: 4,
            depth: 16,
            bevelEnabled: true,
            bevelThickness: 1,
            bevelSize: 1,
            bevelOffset: 1,
            bevelSegments: 1
            };
            const geometry = new THREE.ExtrudeGeometry( shape, extrudeSettings );
            const material = new THREE[value.material_type](value.material);
            // console.log(indices)
            //const material = new THREE.MeshBasicMaterial( { color: value.color, wireframe: false, transparent: true, opacity: 0.5} );
            const mesh = new THREE.Mesh( geometry, material ) ;
            mesh.rotation.set(...Object.values(value.rotation));
            this._scene.add(mesh);

        }
    }

  _LoadModel(data) {
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
      let url_entitys = 'http://127.0.0.1:5000/entitys'
      let response = await fetch(url_entitys)

      if (response.ok) { // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа (см. про этот метод ниже)
        let entities = await response.json();

        console.log( entities );
        console.log( {{ entity }} );
        return entities;

      } else {
        console.log('Error!')
        alert("Ошибка HTTP: " + response.status);
      }
    };

    requestAnimationFrame(async () => {

      const cur_tick = parseInt(timer.getElapsed() / 10)
      if (cur_tick != last_tick){
        // console.log( cur_tick, last_tick )
        last_tick = cur_tick;
        const entitys = await get_entities();

        this._RemoveEntitys();

        this._LoadLight( {{ light }} );
        this._LoadEntity(entitys);
        this._LoadModel( {{ model }} );
        this._DrawEdges( {{ line }} );
        //this._DrawFigure( {{ figure }} );
        //this._DrawShape( {{ figure }} );
        this._DrawTriangls( {{ figure }} );
      };

      this._threejs.render(this._scene, this._camera);
      this._RAF();
    });
  };
};

class WS{
  constructor(WS) {
    this._Initialize();
  }
  _Initialize() {

          // Создаем новый экземпляр WebSocket
      this._websocket = new WebSocket('ws://localhost:8765');

      // Обработчик события открытия соединения
      this._websocket.onopen = function(event) {
          console.log("WebSocket соединение открыто");
      };

      // Обработчик сообщений
      this._websocket.onmessage = function(event) {
          console.log("Получено сообщение: " + event.data);
      };

      // Обработчик ошибок
      this._websocket.onerror = function(event) {
          console.log("Ошибка WebSocket: " + event.data);
      };

  }

  _sendMessage(message) {
      // Отправка сообщения на сервер
      if (this._websocket.readyState === WebSocket.OPEN) {
        this._websocket.send(message);
      } else {
          console.log("WebSocket не открыт");
      }
  }
};

let _APP = null;
let _WS = null;

window.addEventListener('DOMContentLoaded', () => {
  _APP = new Warehouse();
  _WS = new WS();

  // Пример отправки сообщения
  document.getElementById('mylink').addEventListener('click', function() {
    var message = "Привет1"
    _WS._sendMessage(message);
  });
});
