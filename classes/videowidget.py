from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoWidget(QVideoWidget):
    """"
    Classe personalisée de QVideoWidget
    """

    def __init__(self):
        QVideoWidget.__init__(self)
        self.setMinimumSize(320, 180)