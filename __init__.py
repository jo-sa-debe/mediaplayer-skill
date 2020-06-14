from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus import message
from mycroft.skills.audioservice import AudioService


class Mediaplayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self): 
        super().initialize()
        self.add_event('mycroft.audio.service.next', self.play_next)
        self.add_event('mycroft.audio.service.prev', self.play_prev)
        self.add_event('mycroft.audio.service.resume', self.play_resume)
        self.add_event('mycroft.audio.service.pause', self.play_pause)
        self.add_event('mycroft.audio.service.stop', self.play_stop)
        self.add_event('mycroft.audio.service.track_info', self.track_info)
        self.add_event('mycroft.audio.service.track_info_reply', self.track_info_reply)


    @intent_file_handler('mediaplayer.intent')
    def handle_mediaplayer(self, message):
        self.speak_dialog('mediaplayer')
        self.bus.emit(Message('mycroft.audio.service.next'))


    def play_next(self, message):
        self.speak("this is the play next method")
        pass

    def play_prev(self, message):
        pass

    def play_random(self):
        pass

    def play_resume(self):
        pass

    def play_stop(self):
        pass

    def play_pause(self):
        pass

    def track_info(self):
        pass
    
    def track_info_reply(self):
        pass




def create_skill():
    return Mediaplayer()

def stop(self):
    pass

