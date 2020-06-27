from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.messagebus import Message
from mycroft.skills.audioservice import AudioService
import os
from pathlib import Path


class Mediaplayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self): 
        super().initialize()
        self.playlists = []
        self.vlc_all_tracks = []

        self.add_event('mycroft.audio.service.next', self.play_next)
        self.add_event('mycroft.audio.service.prev', self.play_prev)
        self.add_event('mycroft.audio.service.resume', self.play_resume)
        self.add_event('mycroft.audio.service.pause', self.play_pause)
        self.add_event('mycroft.audio.service.stop', self.play_stop)
        self.add_event('mycroft.audio.service.track_info', self.track_info)
        self.add_event('mycroft.audio.service.track_info_reply', self.track_info_reply)
        
        self.audio_service = AudioService(self.bus)
        
        
        #self.vlc_audio_path = Path(os.path.abspath(str(self.settings.get('vlc_audio_path'))))
        
        self.vlc_audio_path = Path(str(self.settings.get('vlc_audio_path')))
        self.vlc_all_tracks = self.load_files_in_audio_path(self.vlc_audio_path.resolve())

        self.current_track = []
        self.other_track_requested = False
       



    @intent_handler('mediaplayer.info.intent')
    def handle_mediaplayer_info(self, message):
        self.speak_dialog('mediaplayer')
        self.speak("looking for backends.")
        for backend in self.audio_service.available_backends().keys():
            backend_text = "found " + str(backend)
            self.speak(backend_text)

    @intent_handler('mediaplayer.next.intent')
    def handle_mediaplayer_next(self, message): 
        self.play_next(message)       
        

    @intent_handler('mediaplayer.prev.intent')
    def handle_mediaplayer_prev(self, message):   
        self.play_prev(message)     
        
    @intent_handler('mediaplayer.stop.intent')
    def handle_mediaplayer_stop(self, message):  
        self.play_stop(message)      
        

    @intent_handler('mediaplayer.pause.intent')
    def handle_mediaplayer_pause(self, message):    
        self.play_pause(message)
        

    @intent_handler('mediaplayer.play.intent')
    def handle_mediaplayer_play(self, message):
        self.play(message)

    def load_files_in_audio_path(self, path):
        self.speak("looking for files in " + str(path))
        tracks = []
        
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                track_path = Path(dirpath)
                track_path = track_path / file
                track_path.resolve()
                track_uri = str(track_path.as_uri())
                #track_path = "file://" + str( os.path.join(dirpath, file))
                track_data = (track_uri , 'mp3')
                tracks.append(track_data)

        self.speak("Number of records found " + str(len(tracks)))

        return tracks

    def add_track_to_list(self, track, list):
        pass

    def add_tracks_to_list(self, tracks, list):
        pass

    def play(self, message):
        self.speak("Start Playing")
        self.speak(str(self.vlc_all_tracks[0]))
        #self.audio_service.play('file:///home/jsauwen/Musik/01 Mars.mp3')

        self.audio_service.play(self.vlc_all_tracks )

    def play_next(self, message):
        self.speak("jumping to next track")

        if self.audio_service.is_playing :
            old_track = self.current_track
            cur_track = self.track_info(message)
            if not self.other_track_requested:
                self.audio_service.next()
                self.other_track_requested = True
            elif old_track != cur_track:
                self.other_track_requested = False 
        

    def play_prev(self, message):
        self.speak("jumping to previous track")
        #self.audio_service.prev()
        #self.bus.emit(Message('mycroft.audio.service.prev'))
        

    def play_random(self, message):
        pass

    def play_resume(self, message):
        pass

    def play_stop(self, message):
        if self.audio_service.is_playing:
            self.audio_service.stop()
            self.speak("stopping playback")
        else:
            self.speak("nothing playing")
        
        #self.audio_service.stop()
        #self.bus.emit(Message('mycroft.audio.service.stop'))
    

    def play_pause(self, message):
        self.speak("pausing playback")
        #self.audio_service.pause()
        #self.bus.emit(Message('mycroft.audio.service.pause'))


    def track_info(self, message):
        return self.audio_service.track_info()
        
    
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

