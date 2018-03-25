import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QSlider
from PyQt5.uic import loadUi
from mediaplayer import MediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl
from pymediainfo import MediaInfo


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        """"""

        self.videofileLeft = QUrl()
        self.videofileRight = QUrl()

        QMainWindow.__init__(self, parent)
        self.setup_widgets()
        self.init_Ui()
        self.define_events()

        self.show()


    def setup_widgets(self):
        """"""

        # MediaPlayer
        self.mediaPlayerLeft = MediaPlayer()
        self.mediaPlayerRight = MediaPlayer()

        # VideoWidget
        self.videoWidgetLeft = QVideoWidget()
        self.videoWidgetRight = QVideoWidget()

        # Assignation du Widget aux players
        self.mediaPlayerLeft.setVideoOutput(self.videoWidgetLeft)
        self.mediaPlayerRight.setVideoOutput(self.videoWidgetRight)


    def init_Ui(self):
        """"""

        loadUi("mainwindow.ui", self)

        # Ajout des videowidgets sur la fenetre
        self.horizontalLayout_5.addWidget(self.videoWidgetLeft)
        self.horizontalLayout_5.addWidget(self.videoWidgetRight)


    def define_events(self):
        """"""

        self.browseLeftFileButton.clicked.connect(self.browseLeftFileButton_clicked)
        self.browseRightFileButton.clicked.connect(self.browseRightFileButton_clicked)
        self.actionButton.clicked.connect(self.actionButton_clicked)
        self.muteButton.clicked.connect(self.muteButton_clicked)

        self.mediaPlayerLeft.positionChanged.connect(self.set_slider_position)

        #self.slider.sliderPressed.connect(self.set_mediaplayer_position)
        self.saturationSlider.sliderMoved.connect(self.saturationSlider_valueChanged)


    def browseLeftFileButton_clicked(self):
        """"""

        filename = self.open_file_browser()
        self.mediaPlayerLeft.setMedia(QMediaContent(filename))

        details = self.get_file_details(filename)
        self.detailLabelLeft.setText(details)


    def browseRightFileButton_clicked(self):
        """"""

        filename = self.open_file_browser()
        self.mediaPlayerRight.setMedia(QMediaContent(filename))

        details = self.get_file_details(filename)
        self.detailLabelRight.setText(details)


    def set_slider_position(self, position):
        """"""

        percent = int((position * 100) / ((self.mediaPlayerLeft.duration() + self.mediaPlayerRight.duration()) / 2))
        self.slider.setValue(percent)


    def set_mediaplayer_position(self):
        """"""

        position = float((self.slider.value() * (self.mediaPlayerLeft.duration() + self.mediaPlayerRight.duration()) / 2) /100)
        self.mediaPlayerLeft.setPosition(position)
        self.mediaPlayerRight.setPosition(position)


    def actionButton_clicked(self):
        """"""

        self.mediaPlayerLeft.play_or_pause()
        self.mediaPlayerRight.play_or_pause()


    def saturationSlider_valueChanged(self):
        """"""

        position = self.saturationSlider.value()
        print(position)
        self.videoWidgetLeft.setBrightness(position)
        self.videoWidgetRight.setBrightness(position)


    def muteButton_clicked(self):
        """"""

        self.mediaPlayerLeft.mute_or_unmute()
        self.mediaPlayerRight.mute_or_unmute()


    def open_file_browser(self):
        """"""

        filename, filter = QFileDialog.getOpenFileName(self, "Choisir un fichier", os.getcwd(), "Fichiers vidéos (*.avi *.mov *.mkv *.mp4 *.ogg *.ogv")
        print(filename)
        return QUrl.fromLocalFile(filename)


    def get_file_details(self, filename):
        details = str()
        details += "Filename: {}\n".format(filename.path())
        media_info = MediaInfo.parse(filename.path())

        for track in media_info.tracks:
            if track.track_type == 'Video':
                if track.track_type == 'Video':
                    details += "Bitrate: {}\nBitrate mode: {}\nCodec: {}".format(track.bit_rate, track.bit_rate_mode, track.codec)

        return details