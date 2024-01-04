# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QListView,
                               QMainWindow, QVBoxLayout,
                               QWidget)

from MWidgets.MList_Widgets.MColor_list_Widget import MColor_list_Widget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(507, 427)
        MainWindow.setContextMenuPolicy(Qt.NoContextMenu)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = MColor_list_Widget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.listWidget.setTabKeyNavigation(True)
        self.listWidget.setDragDropMode(QAbstractItemView.DragDrop)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setIconSize(QSize(50, 50))
        self.listWidget.setMovement(QListView.Free)
        
        self.verticalLayout.addWidget(self.listWidget)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        self.listWidget.customContextMenuRequested.connect(self.listWidget.show_menu)
        
        QMetaObject.connectSlotsByName(MainWindow)
    
    # setupUi
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi


if __name__ == '__main__':
    app = QApplication()
    win = QMainWindow()
    Ui_MainWindow().setupUi(win)
    win.show()
    app.exec()
