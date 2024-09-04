class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
    }

    // This method processes the audio data
    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input.length > 0) {
            // Get the first channel's data
            const channelData = input[0];

            // Send the audio data to the main thread
            this.port.postMessage(channelData);
        }
        return true; // Keep the processor alive
    }
}

registerProcessor('audio-processor', AudioProcessor);