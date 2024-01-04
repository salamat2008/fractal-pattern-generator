# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'untitled.ui'
#
# Created by: Qt User Interface Compiler version 6.6.1
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                               QWidget)

from MWidgets.MList_Widgets.MColor_list_Widget import MColor_list_Widget


class Ui_MainWindow(object):
    def __init__(self):
        self.listWidget = None
        self.horizontalLayout = None
        self.centralwidget = None
    
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget: MColor_list_Widget = MColor_list_Widget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.setSelectionMode(MColor_list_Widget.SelectionMode.MultiSelection)
        self.listWidget.setDragDropMode(self.listWidget.DragDropMode.DragDrop)
        self.listWidget.setDefaultDropAction(Qt.MoveAction)
        self.listWidget.addItem(QColor(0, 0, 0))
        self.listWidget.setEditTriggers(MColor_list_Widget)
        
        self.horizontalLayout.addWidget(self.listWidget)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        self.listWidget.customContextMenuRequested.connect(self.listWidget.show_menu)
        
        QMetaObject.connectSlotsByName(MainWindow)
    
    # setupUi
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
    # retranslateUi


if __name__ == '__main__':
    app = QApplication()
    win = QMainWindow()
    win2 = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(win)
    ui.setupUi(win2)
    win.show()
    win2.show()
    app.exec()
