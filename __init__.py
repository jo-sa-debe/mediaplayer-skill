from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.messagebus import Message
from mycroft.skills.audioservice import AudioService
from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.audio.services import vlc
import random
import os
from pathlib import Path


class Mediaplayer(CommonPlaySkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self): 
        super().initialize()
        self.playlists = []
        self.vlc_all_tracks = []

        #self.add_event('mycroft.audio.service.next', self.play_next)
        #self.add_event('mycroft.audio.service.prev', self.play_prev)
        self.add_event('mycroft.audio.service.resume', self.play_resume)
        self.add_event('mycroft.audio.service.pause', self.play_pause)
        self.add_event('mycroft.audio.service.stop', self.play_stop)
        
        self.audio_service = AudioService(self.bus) 
        self.vlc_audio_path = Path(str(self.settings.get('vlc_audio_path')))
        self.current_track = []
        self.track_change_request_in_progress = False
        self.is_playing = False
       

    @intent_handler('mediaplayer.info.intent')
    def handle_mediaplayer_info(self, message):
        self.speak_dialog('mediaplayer')
        self.speak("looking for backends.")
        for backend in self.audio_service.available_backends().keys():
            backend_text = "found " + str(backend)
            self.speak(backend_text)

    @intent_handler('mediaplayer.next.intent')
    def handle_mediaplayer_next(self, message): 
        if self.is_playing:
            if not self.is_track_change_request_in_progress():
                self.play_next(message)  
        else:
            self.speak("Nothing playing")     
        

    @intent_handler('mediaplayer.prev.intent')
    def handle_mediaplayer_prev(self, message): 
        if self.is_playing:
            self.play_prev(message)     
        else:
            self.speak("Nothing playing")
        
    @intent_handler('mediaplayer.stop.intent')
    def handle_mediaplayer_stop(self, message):  
        if self.is_playing:
            self.play_stop(message)
        else:
            self.speak("Nothing playing")   
        

    @intent_handler('mediaplayer.pause.intent')
    def handle_mediaplayer_pause(self, message):    
        if self.is_playing:
            self.play_pause(message)
        else:
            self.speak("Nothing playing")
        

    # @intent_handler('mediaplayer.play.intent')
    # def handle_mediaplayer_play(self, message):
    #     if not self.is_playing:
    #         self.play(message)
    #     else:
    #         self.speak("Already playing")

    def load_files_in_audio_path(self, path):
        tracks = []
        
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                track_path = Path(dirpath)
                track_path = track_path / file
                track_uri = 'file://' + str(track_path.resolve())
                track_data = (track_uri , 'mp3')
                tracks.append(track_data)
        return tracks

    def init_vlc_audio_list(self):
        self.vlc_all_tracks = self.load_files_in_audio_path(self.vlc_audio_path)
        self.queue_tracks(self.vlc_all_tracks)    
        self.current_track = []

    def get_vlc_track_info(self):
        pass
        

    def queue_tracks(self, tracks):
        self.audio_service.queue(tracks)


    def add_track_to_list(self, track, list):
        pass

    def add_tracks_to_list(self, tracks, list):
        pass

    #def play(self, message):
    def play(self):
        if not self.is_playing:
            if not self.vlc_all_tracks:
                self.init_vlc_audio_list()
            #self.audio_service.play()
            self.audio_service.play(self.vlc_all_tracks, 'vlc')
            self.is_playing = True
            self.set_init_track()


    def play_next(self, message):
        if self.is_playing:
            if not self.is_track_change_request_in_progress():
                self.start_track_change_request()
                self.audio_service.next()
        pass
        

    def play_prev(self, message):
        pass
        

    def play_random(self, message):
        pass

    def play_resume(self, message):
        if not self.is_playing:
            self.audio_service.resume()
            self.is_playing = True

    def play_stop(self, message):
        if self.is_playing:
            self.audio_service.stop()
            self.is_playing = False


    def play_pause(self, message):
        if self.is_playing:
            self.audio_service.pause()
            self.is_playing = False



    def track_info(self, message):
        self.speak("request: track_info")
        return self.audio_service.track_info()
        
    
    def track_info_reply(self, message):
        self.speak("request: track_info_reply")
        #return self.audio_service.track_info()

    def queue_track(self, message):
        self.speak("event: queue_track")
        pass

    def set_init_track(self):
        self.current_track = self.audio_service.track_info()

    def is_track_change_request_in_progress(self):
        if self.track_change_request_in_progress == True:
            if self.current_track != self.audio_service.track_info():
                self.complete_track_change_request()

        return self.track_change_request_in_progress 

    def start_track_change_request(self):
        self.track_change_request_in_progress = True

    def complete_track_change_request(self):   
        self.current_track = self.audio_service.track_info()
        self.track_change_request_in_progress = False

    def CPS_match_query_phrase(self, phrase):
        self.speak("phrase : " + str(phrase))
        self.play()
        level = CPSMatchLevel.MULTI_KEY
        track = self.current_track
        return phrase, level, track

    def CPS_start(self, phrase, data):
        self.speak("phrase : " + str(phrase))
        self.speak("data : " + str(data))
        pass


    def CPS_send_status(self, artist='', track='', image=''):
        data = {'skill': self.name,
                'artist': artist,
                'track': track,
                'image': image,
                'status': None  # TODO Add status system
                }
        self.bus.emit(Message('play:status', data))


def create_skill():
    return Mediaplayer()

def stop(self):
    pass

