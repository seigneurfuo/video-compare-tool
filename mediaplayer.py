from PyQt5.QtMultimedia import QMediaPlayer


class MediaPlayer(QMediaPlayer):
    """"Classe personalisée de QMediaPlayer"""
    def __init__(self):
        QMediaPlayer.__init__(self)

    def play_or_pause(self):

        # state
        # 0: stop
        # 1: play
        # 2: pause

        if self.state() == 1: self.pause()
        else: self.play()

    def mute_or_unmute(self):
        if self.isMuted(): self.setMuted(False)
        else: self.setMuted(True)