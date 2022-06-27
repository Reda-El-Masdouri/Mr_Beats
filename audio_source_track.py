from array import array

from audiostream.sources.thread import ThreadSource


class AudioSourceTrack(ThreadSource):
    steps = ()
    step_nb_samples = 0

    def __init__(self, output_stream, wav_samples, bpm, sample_rate, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.chunk_nb_samples = 32
        self.current_sample_index = 0
        self.wav_samples = wav_samples
        self.nb_wav_samples = len(wav_samples)
        self.sample_rate = sample_rate
        self.bpm = bpm
        self.buf = array('h', b"\x00\x00" * self.chunk_nb_samples)
        self.compute_step_nb_samples()
    # 1step = (44100 * 15) / bpm  <->  step_nb_samples = (sample_rate * 15)/bpm

    def set_steps(self, steps):
        self.steps = steps

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.compute_step_nb_samples()

    def compute_step_nb_samples(self):
        self.step_nb_samples = int(self.sample_rate * 15 / self.bpm)

    def get_bytes(self, *args, **kwargs):
        if self.nb_wav_samples > 0:
            for i in range(0, self.chunk_nb_samples):
                if self.current_sample_index < self.nb_wav_samples:
                    self.buf[i] = self.wav_samples[self.current_sample_index]
                else:
                    self.buf[i] = 0
                self.current_sample_index += 1
        return self.buf.tostring()
