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
        #MycroftSkill.__init__(self)
        super().__init__(name="Mediaplayer")

    def initialize(self): 
        super().initialize()
        self.playlists = []
        self.vlc_all_tracks = []
        self.vlc_all_tracks_info = []
        self.audio_service = AudioService(self.bus) 
        self.vlc_audio_path = Path(str(self.settings.get('vlc_audio_path')))
        self.current_track = []
        self.track_change_request_in_progress = False

        self.register_all_intents()
    
    def register_all_intents(self):
        #self.register_intent_file('mediaplayer.next.intent', self.handle_mediaplayer_next)
        #self.register_intent_file('mediaplayer.prev.intent', self.handle_mediaplayer_prev)
        #self.register_intent_file('mediaplayer.stop.intent', self.handle_mediaplayer_stop)
        #self.register_intent_file('mediaplayer.pause.intent', self.handle_mediaplayer_pause)
        #self.register_intent_file('mediaplayer.resume.intent', self.handle_mediaplayer_resume)
        #self.register_intent_file('mediaplayer.info.intent', self.handle_mediaplayer_info)
        pass

    def enable_play_control_intents(self):
        self.enable_intent("mediaplayer.next.intent")
        self.enable_intent("mediaplayer.prev.intent")
        self.enable_intent("mediaplayer.stop.intent")
        self.enable_intent("mediaplayer.pause.intent")
        self.enable_intent("mediaplayer.resume.intent")

    def disable_play_controls(self):
        self.disable_intent("mediaplayer.next.intent")
        self.disable_intent("mediaplayer.prev.intent")
        self.disable_intent("mediaplayer.stop.intent")
        self.disable_intent("mediaplayer.pause.intent")
        self.disable_intent("mediaplayer.resume.intent")        


    def handle_mediaplayer_info(self, message):
        self.speak_dialog('mediaplayer')
        self.speak("looking for backends.")
        for backend in self.audio_service.available_backends().keys():
            backend_text = "found " + str(backend)
            self.speak(backend_text)

    def handle_mediaplayer_next(self, message): 
        if self.audio_service.is_playing:
            if not self.is_track_change_request_in_progress():
                self.play_next(message)  
        else:
            self.speak("Nothing playing")     
        

    def handle_mediaplayer_prev(self, message): 
        if self.audio_service.is_playing:
            self.play_prev(message)     
        else:
            self.speak("Nothing playing")
        
    def handle_mediaplayer_stop(self, message):  
        if self.audio_service.is_playing:
            self.play_stop(message)
        else:
            self.speak("Nothing playing")   
        

    def handle_mediaplayer_pause(self, message):  
        self.speak("pause")  
        self.play_pause(message)

    def handle_mediaplayer_resume(self, message):   
        self.speak("resume") 
        pass

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
                track_data = (track_uri )
                tracks.append(track_data)
        return tracks

    def init_vlc_audio_list(self):
        self.vlc_all_tracks = self.load_files_in_audio_path(self.vlc_audio_path)
        for track in self.vlc_all_tracks:
            self.audio_service.play(track)
            self.vlc_all_tracks_info.append([ track, self.audio_service.track_info()])
            self.audio_service.pause()
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

    def play(self, message):
        
        if not self.audio_service.is_playing:
            if not self.vlc_all_tracks:
                self.init_vlc_audio_list()
                self.set_init_track()
            else:
                self.speak("playing")
                self.audio_service.resume()
            #self.audio_service.play(self.audio_service.)
            #self.audio_service.play(self.vlc_all_tracks, 'vlc')
            
             

    def play_next(self, message):

        if self.audio_service.is_playing:
            self.audio_service.next()
            #if not self.is_track_change_request_in_progress():
            #    self.start_track_change_request()
            #    self.audio_service.next()
        pass
        

    def play_prev(self, message):
        pass
        

    def play_random(self, message):
        pass

    def play_resume(self, message):
        if self.audio_service.is_playing:
            self.audio_service.resume()

    def play_stop(self, message):
        if self.audio_service.is_playing:
            self.audio_service.stop()

    def play_pause(self, message):
        if self.audio_service.is_playing:
            self.audio_service.pause()



    def track_info(self, message):
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
        
        if self.voc_match(phrase, "mediaplayer"):
            level = CPSMatchLevel.GENERIC
            phrase = "mediaplayer"
        else:
            CPSMatchLevel.GENERIC
        return (phrase, level)

    def CPS_start(self, phrase, data):
        self.speak("CPS start")
        self.play(phrase)
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

