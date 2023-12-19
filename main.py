from Window import MainWindow
import sys

if __name__ == '__main__':
    try:
        ui = MainWindow()
        sys.exit(ui.exec())
    except Exception as e:
        print(e)
        raise e
