from PySide6.QtWidgets import QApplication, QMainWindow

from untitled import Ui_MainWindow

if __name__ == '__main__':
    app = QApplication()
    win = QMainWindow()
    Ui_MainWindow().setupUi(win)
    win.show()
    app.exec()
