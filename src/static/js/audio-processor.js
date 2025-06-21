class AudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.buffer = [];
    this.chunkSize = 32768; // number of samples to send per chunk
  }

  process(inputs) {
    if (inputs[0] && inputs[0][0]) {
      const input = inputs[0][0];
      this.buffer.push(...input);

      if (this.buffer.length >= this.chunkSize) {
        const chunk = new Float32Array(this.buffer.slice(0, this.chunkSize));
        this.port.postMessage(chunk);
        this.buffer = this.buffer.slice(this.chunkSize);
      }
    }

    return true;
  }
}

registerProcessor('audio-processor', AudioProcessor);
