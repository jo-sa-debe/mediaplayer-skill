from mycroft import MycroftSkill, intent_file_handler


class Mediaplayer(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('mediaplayer.intent')
    def handle_mediaplayer(self, message):
        self.speak_dialog('mediaplayer')


def create_skill():
    return Mediaplayer()

