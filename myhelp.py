from PyQt5.QtWidgets import QDialog, QTabWidget, QWidget, QHBoxLayout


class Helpwin(QDialog):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(360, 240)
        self.setWindowTitle('Помощь')
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.tabw = QTabWidget(self)
        self.wid = QWidget()
        self.wid2 = QWidget()
        self.tabw.addTab(self.wid, 'ничего')
        self.tabw.addTab(self.wid2, 'ничего')
        self.layout.addWidget(self.tabw)


if __name__ == '__main__':
    print("не написано")
