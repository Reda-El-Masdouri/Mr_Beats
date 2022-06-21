from audiostream import get_output

from Mr_Beats.audio_source_one_shot import AudioSourceOneShot


class AudioEngine:
    NB_CHANELS = 1
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 1024
    def __init__(self):
        self.output_stream = get_output(channels=self.NB_CHANELS, rate=self.SAMPLE_RATE, buffersize=self.BUFFER_SIZE)


    def ply_sound(self, wave_samples):
        audio_source = AudioSourceOneShot(self.output_stream, wave_samples)
        audio_source.start()