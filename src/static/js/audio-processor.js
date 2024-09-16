class AudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.buffer = []; // Array to accumulate audio data
    this.chunkSize = 4096; // Adjust chunk size to your desired value (e.g., 4096 samples)
  }

  process(inputs, outputs, parameters) {
    // inputs[0][0] contains the audio data (first input channel)
    if (inputs[0] && inputs[0][0]) {
      const inputData = inputs[0][0];

      // Accumulate audio data in the buffer
      this.buffer.push(...inputData);

      // If the buffer reaches the chunk size, send the data to the main thread
      if (this.buffer.length >= this.chunkSize) {
        const chunk = this.buffer.slice(0, this.chunkSize);
        this.port.postMessage(chunk); // Send the chunk to the main thread
        this.buffer = this.buffer.slice(this.chunkSize); // Remove the sent chunk from the buffer
      }
    }

    return true; // Keep the processor running
  }
}

registerProcessor('audio-processor', AudioProcessor);
