import gui
import prefs


def main():
    prefs.check_prefs()
    gui.init_gui()


if __name__ == '__main__':
    main()
