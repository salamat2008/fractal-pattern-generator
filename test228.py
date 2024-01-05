from untitled import QApplication, QMainWindow, Ui_MainWindow

if __name__ == '__main__':
    app = QApplication()
    win = QMainWindow()
    Ui_MainWindow().setupUi(win)
    win.show()
    app.exec()
