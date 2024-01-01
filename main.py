import sys

from Mainwindow.Window import MainWindow

if __name__ == '__main__':
    try:
        ui = MainWindow()
        sys.exit(ui.exec())
    except Exception as e:
        print(e)
        raise e
