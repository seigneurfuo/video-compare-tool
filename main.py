import sys
from mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()