import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.121.1/build/three.module.js';
import {OrbitControls} from 'https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/loaders/GLTFLoader.js";
import { Earcut } from "https://cdn.jsdelivr.net/npm/three@0.121.1/src/extras/Earcut.js";
// import { Timer } from 'https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/misc/Timer.js';
import { WS } from './static/js/websocket.js';
import { PositionalRadio } from './static/js/positional_radio.js';
import dat from "https://cdn.skypack.dev/dat.gui";


var camera_position;

// World arrays
var users_pos = null;
var entity_state = null;
var light_state = null;
var line_state = null;
var figure_state = null;
var model_state = null;
var arch_state = null;
var all_3d_data = null;

// Audio arrays
var isRecording = false;
var audioProcessorNode;
var audioContext;


let lastSentTime = 0;
const throttleTime = 10000; // milliseconds



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

    this._threejs.setSize( window.innerWidth  - 15 , window.innerHeight - 20); 
    document.getElementById("app").appendChild(this._threejs.domElement);

    window.addEventListener('resize', () => {
      this._OnWindowResize();
    }, false);

    this._scene = new THREE.Scene();

    // Camera setup
    this._listener = new THREE.AudioListener();
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
    this._camera.add( this._listener );

    // Controls setup
    this._controls = new OrbitControls(
    this._camera, this._threejs.domElement);
    this._controls.target.set(0, 20, 0);

    // Optional: Configure controls for a more FPS-like experience
    this._controls.enableDamping = true; // smooth movement
    this._controls.dampingFactor = 0.1;
    this._controls.screenSpacePanning = false; // keep camera upright
    // this._controls.maxPolarAngle = Math.PI / 2; // limit vertical rotation to 90 degrees
    // this._controls.minPolarAngle = Math.PI / 2; // restrict to horizontal plane (optional)

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
    
    //this._LoadLight( {{ light }} );
    // // this._LoadModel( {{ model }} );
    // this._DrawEdges( {{ line }} );
    // this._LoadEntity( {{ entity }} );
    // this._DrawFigure( {{ figure }} );
    // this._DrawArch( {{ arch }} );
    // //this._DrawTriangls( {{ figure }} );
    this._RAF();
  };

  _RemoveEntitys() {
    while(_APP._scene.children.length > 0){ 
      _APP._scene.remove(_APP._scene.children[0]);
    };
  };

  _DrawArch(data){
    console.log('_DrawArch')
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
    console.log('_DrawTriangls')
      for (const [key, value] of Object.entries(data)) {
          var vertices = new Float32Array(value.vertices.flat())
          var holes = [];
          var geometry = new THREE.BufferGeometry();
          
          var indices = Earcut.triangulate(vertices, [], 3);
          
          geometry.setAttribute( 'position', new THREE.BufferAttribute( vertices, 3 ) );
          geometry.setIndex(indices);
          const material = new THREE[value.material_type](value.material);
          const mesh = new THREE.Mesh( geometry, material );
          this._scene.add( mesh )

              
      }
  };
  _DrawFigure( data ) {
    console.log('_DrawFigure')
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

  _LoadUserModel(data) {
    for (const [name, coordinates] of Object.entries(data)) {

      
      const model = this._scene.getObjectByName(name)

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

  _LoadModel(data) {
    console.log('_LoadModel')
    console.log(data)
    for (const [key, value] of Object.entries(data)) {
      const model_loader = new GLTFLoader();
      model_loader.load(
        value.path
        , (gltf) => {
        gltf.scene.traverse(c => {
        // c.castShadow = true;
        // c.receiveShadow = true;
        //c.name = "model";
        });
        gltf.scene.position.set(...Object.values(value.position));
        gltf.scene.rotation.set(...Object.values(value.rotation));
        gltf.scene.scale.set(...Object.values(value.scale));

        if (value['positional_audio']){
          const _PositionalRadio = new PositionalRadio(THREE, gltf.scene, value['positional_audio'], this._listener);
        }

        this._scene.add(gltf.scene);
      });
    };
  };

  _DrawEdges(data) {
    console.log('_DrawEdges')
      for (const [key, value] of Object.entries(data)) {
          const points = [];

          const material = new THREE[value.material_type](value.material);

          points.push( new THREE.Vector3( ...Object.values(value.position1)) );
          points.push( new THREE.Vector3( ...Object.values(value.position2)) );

          const geometry = new THREE[value.geometry_type]().setFromPoints( points );

          const line = new THREE.Line( geometry, material );
          this._scene.add( line );
          
        }
  }

    //create light from json
  _LoadLight(data) {
        console.log('_LoadLight')
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
      console.log('_LoadEntity')
      //draw all shapes from source
      for (const [key, value] of Object.entries(data)) {
            //draw color or texture
          let material;
          if ('texture' in value.material){
              material = 
                  new THREE[value.material_type]
                ({ map: new THREE.TextureLoader().load('{{ url_for('static', filename='textures/blueprint.jpg') }}'),
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.8,
                });
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
          if (value.geometry_type === 'PlaneGeometry') {
            // Домножаем x на -Math.PI/2 для горизонтального положения лицом вверх
            const rx = (value.rotation?.x || 0) - Math.PI / 2;
            mesh.rotation.set(rx, value.rotation?.y || 0, value.rotation?.z || 0);
          } else {
            mesh.rotation.set(...Object.values(value.rotation));
          }
      };
  };

  _OnWindowResize() {
    this._camera.aspect = {{ camera.aspect_ratio }};
    this._camera.updateProjectionMatrix();

    this._threejs.setSize(innerWidth, innerHeight);
  };

  _GetUsersPos(){
    if (_WS.getState() == 1){
      // Send camera (user) position
      if (camera_position != JSON.stringify(this._camera.position)){
        //console.log(camera_position, this._camera.position)
        _WS._sendMessage(JSON.stringify({'user_position': {'{{ user }}': {'position': this._camera.position, 'rotation': this._camera.rotation}}}));
        camera_position = JSON.stringify(this._camera.position)
      };
        // Send users state
        _WS._sendMessage(JSON.stringify({'users_pos': {'{{ user }}': users_pos}}));

        // echo from ws
        const receivedData = _WS.getReceivedData();

        var recivedDataJson = JSON.parse(receivedData)
        if (recivedDataJson && 'users_pos' in recivedDataJson){
            this._LoadUserModel(recivedDataJson["users_pos"])
            users_pos = recivedDataJson["users_pos"]
        };

    }

  }

  _SendRequest3D(){
    console.log('send all 3d request')
    if (_WS.getState() == 1){
      // Request for all_3d_data
      // if (all_3d_data == null){};
      _WS._sendMessage(JSON.stringify({'all_3d_data': {'{{ user }}': all_3d_data}}));
      
    };
  };

  _Get3DObjects(){
    if (_WS.getState() == 1){
        // echo from ws
        const receivedData = _WS.getReceivedData();
        console.log(receivedData)
        var recivedDataJson = JSON.parse(receivedData)
        if (recivedDataJson && recivedDataJson["all_3d_data"]){
          console.log(recivedDataJson["all_3d_data"]["line_state"])
          this._LoadEntity( recivedDataJson["all_3d_data"]["entity_state"] );
          this._LoadLight( recivedDataJson["all_3d_data"]["light_state"] );
          //this._DrawEdges( recivedDataJson["all_3d_data"]["line_state"] );
          //this._DrawFigure( recivedDataJson["all_3d_data"]["figure_state"] );
          this._LoadModel( recivedDataJson["all_3d_data"]["model_state"] );
          //this._DrawArch( recivedDataJson["all_3d_data"]["arch_state"] );
          all_3d_data = recivedDataJson["all_3d_data"]
          _WS.receivedData = null;
    };
};

  };

  async _startMicrophoneCapture() {
    try {
        // Check if getUserMedia is supported
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.error('getUserMedia not supported on your browser!');
            return;
        }

        const options = {
          mimeType: 'audio/webm;codecs=opus', // High-quality codec for voice
          audioBitsPerSecond: 256000 // Increase the bitrate (256 kbps)
        };

        // Access the microphone
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true
          }
        });

        // Initialize the AudioContext if not already done
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } else {
            audioContext.resume().then(() => {
                    console.log("Suspend context");
            });
        };

        // Load the AudioWorkletProcessor if not already done
        if (!audioProcessorNode) {
            await audioContext.audioWorklet.addModule('{{ url_for('static', filename='js/audio-processor.js') }}');
            audioProcessorNode = new AudioWorkletNode(audioContext, 'audio-processor');

            // Listen for audio data from the processor
            audioProcessorNode.port.onmessage = (event) => {
                const audioData = event.data;
                const base64_data = btoa(audioData)
                _WS._sendMessage(JSON.stringify({'voice': {'{{ user }}': base64_data}}));
                console.log(audioData)
            };
        }

        // Connect the audio nodes
        const source = audioContext.createMediaStreamSource(stream, options);
        source.connect(audioProcessorNode);

        isRecording = true;
        console.log('Microphone recording started');
    } catch (err) {
        console.error('Error accessing the microphone: ' + err);
    }
  }

  _stopMicrophoneCapture() {
    if (audioContext && isRecording) {
        // Stop the AudioContext
        audioContext.suspend();

        isRecording = false;
        console.log('Microphone recording stopped');
    }
  }

  async _VoicePlay(){
    
    if (_WS.getState() == 1){

      // echo from ws
      const receivedData = _WS.getReceivedData();
      const recivedDataJson = JSON.parse(receivedData)
      if (recivedDataJson && recivedDataJson["voice"]){
        for (const [user, base64Data] of Object.entries(recivedDataJson["voice"])) {

            const audioChunks = atob(base64Data);
            const float32Array = Float32Array.from(audioChunks.split(","), parseFloat);

            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const sampleRate = audioContext.sampleRate;

            console.log(float32Array)
            // Create an empty stereo AudioBuffer with the same length as the array
            const audioBuffer = audioContext.createBuffer(1, float32Array.length, sampleRate);

            // Copy the Float32Array data into the buffer's first channel
            audioBuffer.copyToChannel(float32Array, 0, 0);

            // Create an AudioBufferSourceNode to play the buffer
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;

            // Connect the source to the audio context's destination (speakers)
            source.connect(audioContext.destination);

            // Start playing the audio
            source.start();
            _WS.receivedData = null;
        };
      };
    };

  };

  _RAF() {
    requestAnimationFrame(async () => {
      const now = Date.now();
      if (now - lastSentTime >= throttleTime / 100) {
        this._GetUsersPos();
        lastSentTime = now;
      }
      this._controls.update();
      this._VoicePlay()
      this._Get3DObjects();
      
      
      this._threejs.render(this._scene, this._camera);
      this._RAF();
    });
  };
};

let _APP = null;

window.addEventListener('DOMContentLoaded', () => {

  _APP = new Warehouse();
  _APP._SendRequest3D()
  // const _PositionalRadio = new PositionalRadio(THREE, _APP._camera, _APP._scene, )

  const gui = new dat.GUI();
  const links_folder = gui.addFolder('Links');
  const world_folder = gui.addFolder('World');
  const audio_folder = gui.addFolder('Radio');
  function button_func() {
    window.location.href = '/logout';
  };

  links_folder.add({Logout: button_func}, 'Logout');
  world_folder.add({LoadWorld: _APP._SendRequest3D}, 'LoadWorld');
  world_folder.add({ClearWorld: _APP._RemoveEntitys}, 'ClearWorld');
  
  // audio_folder.add(_PositionalRadio._audio_controls, 'playAudio').name('Play Radio');
  // audio_folder.add(_PositionalRadio._audio_controls, 'pauseAudio').name('Pause Radio');

  const settings = {
    volume: 1  // Slider will control this property
  };
  // Add a slider to the folder
  audio_folder.add(settings, 'volume', 0, 1).name('Volume');
  //folder.open();

});

document.addEventListener('keydown', (event) => {
  if (event.code === 'Space' && !isRecording) { // Space key is pressed
    _APP._startMicrophoneCapture();
  }
});

document.addEventListener('keyup', (event) => {
  if (event.code === 'Space' && isRecording) { // Space key is released
    _APP._stopMicrophoneCapture();
  }
});
