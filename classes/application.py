import os

from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import QUrl

from classes.floating_controls import FloatingControls
from classes.mediaplayer import MediaPlayer
from classes.videowidget import VideoWidget


class Application(QApplication):
    def __init__(self, args):
        super().__init__(args)

        self.name = "VideoCompareTool"
        self.version = "0.0.2"

        self.filename_a = None
        self.filename_b = None

        # TODO: Verifier si le fichier existe

        self.setApplicationName(self.name)
        self.setApplicationDisplayName(self.name)
        self.setApplicationVersion(self.version)

        self.mute_id = 0 # (0, 1, 2, 3)
        self.source_id = 0 # (0, 1, 2)

        self.init_widgets()
        self.init_events()
        self.init_media_player_objects()

        print(args)

        # Récupération des fichiers passés en paramètres
        if len(args) == 3:
            self.filename_a = args[1]
            self.filename_b = args[2]

            print(self.filename_b)

            self.set_media_player_a_media(QUrl.fromLocalFile(self.filename_a))
            self.set_media_player_b_media(QUrl.fromLocalFile(self.filename_b))

        self.show_widgets()

    def init_widgets(self):
        self.video_widget_a = VideoWidget()
        self.video_widget_a.setWindowTitle("Video A")

        self.video_widget_b = VideoWidget()
        self.video_widget_b.setWindowTitle("Video B")

        self.video_widget_c = VideoWidget()

        self.floating_controls = FloatingControls()
        self.floating_controls.setWindowTitle(self.name)

    def init_media_player_objects(self):
        self.media_player_a = MediaPlayer()
        self.media_player_b = MediaPlayer()

        self.media_player_a.setVideoOutput(self.video_widget_a)
        self.media_player_b.setVideoOutput(self.video_widget_b)

    def init_events(self):
        """

        :return: None
        """

        # Selecteur de fichiers
        self.floating_controls.file_open_button_a.clicked.connect(self.on_file_open_button_a_clicked)
        self.floating_controls.file_open_button_b.clicked.connect(self.on_file_open_button_b_clicked)

        # Play / Pause
        self.floating_controls.play_pause_button.clicked.connect(self.on_play_pause_button_clicked)

        self.floating_controls.switch_source_button.clicked.connect(self.on_switch_video_source_button)

        self.floating_controls.video_widget_a_mute_button.stateChanged.connect(self.on_video_widget_a_mute_button_changed)
        self.floating_controls.video_widget_b_mute_button.stateChanged.connect(self.on_video_widget_b_mute_button_changed)

        # Luminosité, Contrast et flou
        self.floating_controls.brightness_slider.sliderMoved.connect(self.on_brightness_slider_moved)
        self.floating_controls.contrast_slider.sliderMoved.connect(self.on_contrast_slider_moved)
        self.floating_controls.hue_slider.sliderMoved.connect(self.on_hue_slider_moved)


    def show_widgets(self):
        """

        :return: None
        """

        self.floating_controls.show()

        self.video_widget_a.show()
        self.video_widget_b.show()
        #self.video_widget_c.show()

    def open_file_browser(self):
        """

        :return:
        """

        filename, filter = QFileDialog.getOpenFileName(None, "Choisir un fichier", os.getcwd(),
                                                             "Fichiers vidéos (*.avi *.mov *.mkv *.mp4 *.ogg *.ogv")

        return QUrl.fromLocalFile(filename)

    def on_file_open_button_a_clicked(self):
        """

        :return:
        """

        filename = self.open_file_browser()
        self.set_media_player_a_media(filename)

    def set_media_player_a_media(self, filename):
        self.media_player_a.setMedia(QMediaContent(filename))
        self.floating_controls.video_widget_a_slider.setMaximum(self.media_player_a.duration())

    def on_file_open_button_b_clicked(self):
        """

        :return:
        """

        filename = self.open_file_browser()
        self.set_media_player_b_media(filename)

    def set_media_player_b_media(self, filename):
        self.media_player_b.setMedia(QMediaContent(filename))
        self.floating_controls.video_widget_b_slider.setMaximum(self.media_player_b.duration())

    def on_video_widget_a_slider_pressed(self):
        value = self.floating_controls.video_widget_a_slider.value()
        print(value)

    def on_video_widget_b_slider_pressed(self):
        value = self.floating_controls.video_widget_b_slider.value()
        print(value)

    def on_play_pause_button_clicked(self):
        """

        :return:
        """

        self.media_player_a.play_or_pause()
        self.media_player_b.play_or_pause()

    def on_switch_video_source_button(self):

        self.source_id += 1
        self.media_player_a.setVideoOutput(None)
        self.media_player_a.setVideoOutput(self.video_widget_c)

        #if self.source_id == 1:
            #self.media_player_a.setVideoOutput(self.video_widget_c)

        #elif self.source_id == 2:
            #self.media_player_b.setVideoOutput(self.video_widget_c)

            #self.source_id = 0

    def on_brightness_slider_moved(self, position):
        """

        :param position:
        :return: None
        """

        self.video_widget_a.setBrightness(position)
        self.video_widget_b.setBrightness(position)


    def on_contrast_slider_moved(self, position):
        """

        :param position:
        :return: None
        """

        self.video_widget_a.setContrast(position)
        self.video_widget_b.setContrast(position)

    def on_hue_slider_moved(self, position):
        """

        :param position:
        :return: None
        """

        self.video_widget_a.setHue(position)
        self.video_widget_b.setHue(position)

    def on_video_widget_a_mute_button_changed(self, state):
        map = {0: False, 2: True}
        self.media_player_a.setMuted(map[state])

    def on_video_widget_b_mute_button_changed(self, state):
        map = {0: False, 2: True}
        self.media_player_b.setMuted(map[state])
