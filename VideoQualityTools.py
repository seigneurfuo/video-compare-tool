import sys
from classes.application import Application


def main():
    application = Application(sys.argv)
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
