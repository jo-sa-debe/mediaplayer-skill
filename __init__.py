from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.messagebus import Message
from mycroft.skills.audioservice import AudioService
import os


class Mediaplayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self): 
        super().initialize()
        self.playlists = []

        self.add_event('mycroft.audio.service.next', self.play_next)
        self.add_event('mycroft.audio.service.prev', self.play_prev)
        self.add_event('mycroft.audio.service.resume', self.play_resume)
        self.add_event('mycroft.audio.service.pause', self.play_pause)
        self.add_event('mycroft.audio.service.stop', self.play_stop)
        self.add_event('mycroft.audio.service.track_info', self.track_info)
        self.add_event('mycroft.audio.service.track_info_reply', self.track_info_reply)
        
        self.audio_service = AudioService(self.bus)
        
        self.vlc_audio_path = str(self.settings.get('vlc_audio_path'))
        self.vlc_all_tracks = self.load_files_in_audio_path(self.vlc_audio_path)




    @intent_handler('mediaplayer.info.intent')
    def handle_mediaplayer_info(self, message):
        self.speak_dialog('mediaplayer')
        self.speak("looking for backends.")
        for backend in self.audio_service.available_backends().keys():
            backend_text = "found " + str(backend)
            self.speak(backend_text)

    @intent_handler('mediaplayer.next.intent')
    def handle_mediaplayer_next(self, message):        
        self.bus.emit(Message('mycroft.audio.service.next'))

    @intent_handler('mediaplayer.play.intent')
    def handle_mediaplayer_play(self, message):
        self.play(message)

    def load_files_in_audio_path(self, path):
        self.speak("looking for files in " + path)
        tracks = []
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                self.speak("adding track " + file)
                tracks.append((file, 'mp3'))
        return tracks

    def add_track_to_list(self, track, list):
        pass

    def add_tracks_to_list(self, tracks, list):
        pass

    def play(self, message):
        self.speak("Start Playing")
        for track in self.vlc_all_tracks[0]:
            self.speak('track : ' + track )
        self.speak("end of tracklist : all")
        self.audio_service.play(self.vlc_all_tracks)

    def play_next(self, message):
        self.speak("this is the play next method")
        pass

    def play_prev(self, message):
        pass

    def play_random(self, message):
        pass

    def play_resume(self, message):
        pass

    def play_stop(self, message):
        pass

    def play_pause(self, message):
        pass

    def track_info(self, message):
        pass
    
    def track_info_reply(self, message):
        pass

    def queue_track(self, message):
        pass

    def is_playing(self, message):
        pass






def create_skill():
    return Mediaplayer()

def stop(self):
    pass

