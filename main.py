from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty, Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from Mr_Beats.audio_engine import AudioEngine
from Mr_Beats.sound_kit_service import SoundKitService
from Mr_Beats.track import TrackWidget

Builder.load_file("track.kv")
Builder.load_file("play_indicator.kv")

TRACK_NB_STEPS = 16
MIN_BPM = 80
MAX_BPM = 160

class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()
    play_indicator_widget = ObjectProperty()
    TRACK_STEPS_LEFT_ALIGN = NumericProperty(dp(100))
    step_index = 0
    bpm = NumericProperty(120)
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.sound_kit_service = SoundKitService()
        #kick_sound = self.sound_kit_service.get_sound_at(0)
        self.audio_engine = AudioEngine()
        #self.audio_engine.create_track(kick_sound.samples, 200)
        #self.audio_engine.play_sound(kick_sound.samples)
        self.mixer = self.audio_engine.create_mixer(self.sound_kit_service.soundkit.get_all_samples(), 120, TRACK_NB_STEPS, self.on_mixer_current_step_changed, MIN_BPM)

    def on_parent(self, widget, parent):
        self.play_indicator_widget.set_nb_steps(TRACK_NB_STEPS)
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_at(i)
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio_engine, TRACK_NB_STEPS, self.mixer.tracks[i], self.TRACK_STEPS_LEFT_ALIGN))

    def on_mixer_current_step_changed(self, step_index):
        self.step_index = step_index
        Clock.schedule_once(self.update_play_indicator_cbk, 0)


    def update_play_indicator_cbk(self, dt):
        if self.play_indicator_widget is not None:
            self.play_indicator_widget.set_current_step_index(self.step_index)

    def on_play_button_pressed(self):
        self.mixer.audio_play()

    def on_stop_button_pressed(self):
        self.mixer.audio_stop()

    def on_bpm(self, widget, value):
        if value > MAX_BPM:
            self.bpm = MAX_BPM
            return
        if value < MIN_BPM:
            self.bpm = MIN_BPM
            return
        self.mixer.set_bpm(self.bpm)

class MrBeatApp(App):
    pass


MrBeatApp().run()
