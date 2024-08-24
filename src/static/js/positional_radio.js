class PositionalRadio {
    constructor(model, stream) {
        this._Initialize(model, stream);

    }

    _Initialize(positionalAudio, model, stream) {

        // const stream = 'http://192.168.31.92:8100/8bit'
        // const ambient = '{{ url_for('static', filename='sounds/ambient.mp3') }}'

        // create an AudioListener and add it to the camera
        // const listener = new THREE.AudioListener();
        // camera.add( listener );

        // Create a positional audio object and attach it to the cube
        // this._positionalAudio = new THREE.PositionalAudio(listener);
        model.add( this.positionalAudio);
        
        // Create an HTML audio element for streaming audio
        this._audioElement = document.createElement('audio');
        this._audioElement.src = stream
        this._audioElement.crossOrigin = 'anonymous'; // Enable cross-origin requests if needed
        this._audioElement.loop = true;

        // Wait for the audio element to be ready before playing
        this._audioElement.addEventListener('canplay', () => {
            this._audioElement.play().catch(error => {
                console.error('Error playing audio:', error);
            });
        });

        this._audio_controls = {
            playAudio: () => {
                this._audioElement.play().catch(error => {
                    console.error('Error playing audio:', error);
                });
            },
            pauseAudio: () => {
                this._audioElement.pause();
            }
        };
        
        // // Set the audio element as the source for the positional audio
        // this._positionalAudio.setMediaElementSource(this._audioElement);
        
        // // Set additional properties for positional audio
        // this._positionalAudio.setRefDistance(1); // Set the reference distance for max volume
        // this._positionalAudio.setRolloffFactor(1); // Determines how the audio volume decreases with distance
        // this._positionalAudio.setMaxDistance(20); // Maximum distance the audio will be heard
        // this._positionalAudio.setVolume(0.5); // Set the volume level

    }

    _PlayRadio(message) {
        this._audio_controls['playAudio']()
    }

    // Method to process the received data
    _PauseRadio(data) {
        this._audio_controls['pauseAudio']()
    }
}
export { PositionalRadio };

// _PlayRadio(){
//     const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
//     const audio = new Audio('http://localhost:8100/8bit');
//     audio.crossOrigin = "anonymous";
//     const track = audioCtx.createMediaElementSource(audio);
//     track.connect(audioCtx.destination);
//     audio.play();
// };

// _PlayRadio() {
//     // Load the audio stream
//     const listener = new THREE.AudioListener();
//     // _APP._camera.add(listener);

//     const audio = new THREE.Audio(listener);
//     const audioLoader = new THREE.AudioLoader();

//     // Load the stream from the Python server
//     audioLoader.load(
//     '{{ url_for('static', filename='sounds/ambient.mp3') }}',
//     function(buffer) {
//         audio.setBuffer(buffer);
//         audio.setLoop(true);
//         audio.setVolume(0.9)
//         audio.play();
//     }, undefined,
//     function(err){
//     console.error('An error occurred while loading the audio stream:', err)
//     });