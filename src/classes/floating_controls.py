from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class FloatingControls(QWidget):
    def __init__(self, parent=None):
        """"""

        QWidget.__init__(self, parent)
        loadUi("ui/floating_controls.ui", self)
