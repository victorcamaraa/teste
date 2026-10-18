// Processadores de áudio que rodam na thread de áudio.

// Noise gate: atenua o sinal quando o nível fica abaixo do limiar.
class NoiseGate extends AudioWorkletProcessor {
  static get parameterDescriptors() {
    return [
      { name: 'threshold', defaultValue: -60, minValue: -100, maxValue: 0, automationRate: 'k-rate' },
      { name: 'range', defaultValue: -40, minValue: -100, maxValue: 0, automationRate: 'k-rate' },
    ];
  }
  constructor() {
    super();
    const sr = sampleRate;
    this.env = 0;
    this.gain = 1;
    this.hold = 0;
    this.holdSamples = Math.round(0.08 * sr);
    this.envAtt = Math.exp(-1 / (0.001 * sr));
    this.envRel = Math.exp(-1 / (0.05 * sr));
    this.gOpen = 1 - Math.exp(-1 / (0.002 * sr));
    this.gClose = 1 - Math.exp(-1 / (0.15 * sr));
    this.reportEvery = Math.round(0.1 * sr);
    this.sinceReport = 0;
  }
  process(inputs, outputs, params) {
    const inp = inputs[0], out = outputs[0];
    if (!inp || !inp.length) return true;
    const thr = Math.pow(10, params.threshold[0] / 20);
    const floor = Math.pow(10, params.range[0] / 20);
    const n = inp[0].length;
    for (let i = 0; i < n; i++) {
      let x = 0;
      for (let c = 0; c < inp.length; c++) { const a = Math.abs(inp[c][i]); if (a > x) x = a; }
      this.env = x > this.env ? x + (this.env - x) * this.envAtt : x + (this.env - x) * this.envRel;
      if (this.env > thr) this.hold = this.holdSamples; else if (this.hold > 0) this.hold--;
      const target = this.hold > 0 ? 1 : floor;
      this.gain += (target - this.gain) * (target > this.gain ? this.gOpen : this.gClose);
      for (let c = 0; c < out.length; c++) out[c][i] = (inp[c] || inp[0])[i] * this.gain;
    }
    this.sinceReport += n;
    if (this.sinceReport >= this.reportEvery) { this.sinceReport = 0; this.port.postMessage(this.gain); }
    return true;
  }
}

// Gravador: mistura para mono e envia blocos de 4096 amostras para a thread principal.
class Recorder extends AudioWorkletProcessor {
  constructor() {
    super();
    this.buf = new Float32Array(4096);
    this.pos = 0;
  }
  process(inputs) {
    const inp = inputs[0];
    if (!inp || !inp.length) return true;
    const n = inp[0].length, ch = inp.length;
    for (let i = 0; i < n; i++) {
      let s = 0;
      for (let c = 0; c < ch; c++) s += inp[c][i];
      this.buf[this.pos++] = s / ch;
      if (this.pos === this.buf.length) {
        this.port.postMessage(this.buf, [this.buf.buffer]);
        this.buf = new Float32Array(4096);
        this.pos = 0;
      }
    }
    return true;
  }
}

registerProcessor('noise-gate', NoiseGate);
registerProcessor('recorder', Recorder);
