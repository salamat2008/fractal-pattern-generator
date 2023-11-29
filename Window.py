import os
import re
import sys

from PyQt5.QtCore import QSize, Qt, QMetaObject
from PyQt5.QtGui import QColor, QCursor, QImage, QPainter
from PyQt5.QtWidgets import (QFileDialog, QMainWindow,
                             QApplication, QSizePolicy,
                             QWidget, QGridLayout, QMenuBar, QMenu,
                             QDockWidget, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLabel, QSpinBox, QLineEdit,
                             QListWidget, QPushButton, QGroupBox, QInputDialog, QColorDialog)

from myView import View
from myhelp import Helpwin
from settingdial import Settingdialog


class Mainwindowqt(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.resize(1000, 800)
        size_polic = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setMinimumSize(QSize(400, 560))
        self.setMaximumSize(QSize(4000, 3000))
        self.setWindowTitle("Генератор фрактальных узоров")
        self.centralwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.canvas = View(self.centralwidget)
        self.gridLayout.addWidget(self.canvas, 0, 0, 1, 2)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.file = QMenu(self.menubar)
        self.settings = QMenu(self.menubar)
        self.help = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.dockWidget_1 = QDockWidget(self)
        self.dockWidgetContents_2 = QWidget()
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_2)
        self.formLayout_2 = QFormLayout()
        self.label = QLabel(self.dockWidgetContents_2)
        self.linewidthsb = QSpinBox(self.dockWidgetContents_2)
        self.label_3 = QLabel(self.dockWidgetContents_2)
        self.depthsb = QSpinBox(self.dockWidgetContents_2)
        self.label_4 = QLabel(self.dockWidgetContents_2)
        self.sizesb = QSpinBox(self.dockWidgetContents_2)
        self.label_5 = QLabel(self.dockWidgetContents_2)
        self.anglesb = QSpinBox(self.dockWidgetContents_2)
        self.label_9 = QLabel(self.dockWidgetContents_2)
        self.lensb = QSpinBox(self.dockWidgetContents_2)
        self.label_8 = QLabel(self.dockWidgetContents_2)
        self.patternsb = QLineEdit(self.dockWidgetContents_2)
        self.groupBox2 = QGroupBox(self.dockWidgetContents_2)
        self.horizontalLayout1 = QHBoxLayout(self.groupBox2)
        self.rules_list = QListWidget(self.groupBox2)
        self.verticalLayout__ = QVBoxLayout()
        self.radd_Button = QPushButton(self.groupBox2)
        self.redit_Button = QPushButton(self.groupBox2)
        self.rup_Button = QPushButton(self.groupBox2)
        self.rdown_Button = QPushButton(self.groupBox2)
        self.rdelete_Button = QPushButton(self.groupBox2)
        self.rclear_Button = QPushButton(self.groupBox2)
        self.color_groupBox = QGroupBox(self.dockWidgetContents_2)
        self.horizontalLayout = QHBoxLayout(self.color_groupBox)
        self.color_list = QListWidget(self.color_groupBox)
        self.verticalLayout_3 = QVBoxLayout()
        self.add_Button = QPushButton(self.color_groupBox)
        self.edit_Button = QPushButton(self.color_groupBox)
        self.up_Button = QPushButton(self.color_groupBox)
        self.down_Button = QPushButton(self.color_groupBox)
        self.delete_Button = QPushButton(self.color_groupBox)
        self.clear_Button = QPushButton(self.color_groupBox)
        self.start_button = QPushButton(self.dockWidgetContents_2)
        self.clear_button = QPushButton(self.dockWidgetContents_2)
        self.verticalLayout__.setSpacing(0)
        self.verticalLayout_3.setSpacing(0)
        self.menubar.setCursor(QCursor(Qt.ArrowCursor))
        self.menubar.setFocusPolicy(Qt.NoFocus)
        self.dockWidget_1.setMinimumSize(QSize(223, 670))
        self.dockWidget_1.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.dockWidget_1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dockWidget_1.setSizePolicy(size_polic)
        self.dockWidgetContents_2.setSizePolicy(size_polic)
        self.radd_Button.setSizePolicy(size_policy)
        self.redit_Button.setSizePolicy(size_policy)
        self.rup_Button.setSizePolicy(size_policy)
        self.rdown_Button.setSizePolicy(size_policy)
        self.rdelete_Button.setSizePolicy(size_policy)
        self.rclear_Button.setSizePolicy(size_policy)
        self.add_Button.setSizePolicy(size_policy)
        self.edit_Button.setSizePolicy(size_policy)
        self.up_Button.setSizePolicy(size_policy)
        self.down_Button.setSizePolicy(size_policy)
        self.delete_Button.setSizePolicy(size_policy)
        self.clear_Button.setSizePolicy(size_policy)
        self.canvas.setBackgroundBrush(QColor('white'))
        self.actions_setter()
        self.spinboxs()
        self.widget_placer()
        self.text_setter()
        self.comdict = {"F": self.canvas.forward,
                        "B": self.canvas.back,
                        "L": self.canvas.rleft,
                        "R": self.canvas.rright,
                        "V": self.canvas.vforward,
                        "N": self.canvas.vback,
                        "C": self.canvas.change_color,
                        "S": self.canvas.square,
                        "E": self.canvas.circle,
                        "T": self.canvas.triangle
                        }
        self.show()
        QMetaObject.connectSlotsByName(self)

    def actions_setter(self):
        self.file.addAction("Открыть файл", self.open_file)
        self.file.addAction("Сохранить алгоритм", self.fsavealg)
        self.file.addAction("Сохранить изображение", self.fsaveimg)
        self.file.addAction("Выход", sys.exit)
        self.settings.addAction("Шрифты и обозначения", self.settings_win)
        self.settings.addAction("Фон", self.backgr)
        self.help.addAction("Что делать?", self.helpwi)
        self.help.addSeparator()
        self.help.addAction("Кривая Коха", self.kkoh)
        self.help.addAction("С-кривая Леви", self.klevi)
        self.help.addAction("Треуголник Серпинского", self.sertria)
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.settings.menuAction())
        self.menubar.addAction(self.help.menuAction())

    def spinboxs(self):
        self.linewidthsb.setMinimum(1)
        self.linewidthsb.setMaximum(999999999)
        self.linewidthsb.setProperty("value", 1)
        self.depthsb.setMaximum(999999999)
        self.anglesb.setMaximum(360)
        self.anglesb.setSingleStep(5)
        self.anglesb.setProperty("value", 60)
        self.lensb.setMaximum(999999999)
        self.lensb.setSingleStep(10)
        self.sizesb.setMinimum(1)
        self.sizesb.setMaximum(999999999)
        self.sizesb.setSingleStep(10)
        self.sizesb.setProperty("value", 100)

    def widget_placer(self):
        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)
        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.linewidthsb)
        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.depthsb)
        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_4)
        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.sizesb)
        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_5)
        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.anglesb)
        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_9)
        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.lensb)
        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_8)
        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.patternsb)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.horizontalLayout1.addWidget(self.rules_list)
        self.verticalLayout__.addWidget(self.radd_Button)
        self.verticalLayout__.addWidget(self.redit_Button)
        self.verticalLayout__.addWidget(self.rup_Button)
        self.verticalLayout__.addWidget(self.rdown_Button)
        self.verticalLayout__.addWidget(self.rdelete_Button)
        self.verticalLayout__.addWidget(self.rclear_Button)
        self.horizontalLayout1.addLayout(self.verticalLayout__)
        self.horizontalLayout.addWidget(self.color_list)
        self.verticalLayout.addWidget(self.groupBox2)
        self.verticalLayout_3.addWidget(self.add_Button)
        self.verticalLayout_3.addWidget(self.edit_Button)
        self.verticalLayout_3.addWidget(self.up_Button)
        self.verticalLayout_3.addWidget(self.down_Button)
        self.verticalLayout_3.addWidget(self.delete_Button)
        self.verticalLayout_3.addWidget(self.clear_Button)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.color_groupBox)
        self.verticalLayout.addWidget(self.start_button)
        self.verticalLayout.addWidget(self.clear_button)
        self.dockWidget_1.setWidget(self.dockWidgetContents_2)
        self.addDockWidget(Qt.DockWidgetArea(1), self.dockWidget_1)
        self.dockWidget_1.raise_()

    def text_setter(self):
        self.color_list.addItem("#000000")
        self.color_list.item(0).setData(3, QColor.fromRgb(4278190080))
        self.rules_list.addItem("F FLFRRFLF")
        self.file.setTitle("Файл")
        self.settings.setTitle("Настройки")
        self.help.setTitle("Помощь")
        self.dockWidget_1.setWindowTitle("Параметры")
        self.label.setText("Толщина")
        self.label_3.setText("Глубина")
        self.label_4.setText("Размер")
        self.label_5.setText("Угол поворота")
        self.anglesb.setSuffix("°")
        self.label_9.setText("Длинна перемещения")
        self.label_8.setText("Шаблон")
        self.patternsb.setText("F")
        self.groupBox2.setTitle('Список правил')
        self.radd_Button.setText("Добавить")
        self.redit_Button.setText("Изменить")
        self.rup_Button.setText("Вверх")
        self.rdown_Button.setText("Вниз")
        self.rdelete_Button.setText("Удалить")
        self.rclear_Button.setText("Очистить")
        self.color_groupBox.setTitle("Список цветов")
        self.add_Button.setText("Добавить")
        self.edit_Button.setText("Изменить")
        self.up_Button.setText("Вверх")
        self.down_Button.setText("Вниз")
        self.delete_Button.setText("Удалить")
        self.clear_Button.setText("Очистить")
        self.start_button.setText("Старт")
        self.clear_button.setText("Очистить")
        self.btn_fnc_setter()

    def btn_fnc_setter(self):
        self.add_Button.clicked.connect(self.add_clr)
        self.edit_Button.clicked.connect(self.edit_clr)
        self.up_Button.clicked.connect(self.up_clr)
        self.delete_Button.clicked.connect(self.delclr)
        self.clear_Button.clicked.connect(self.clear_clr)
        self.down_Button.clicked.connect(self.dn_clr)
        self.radd_Button.clicked.connect(self.add_rule)
        self.redit_Button.clicked.connect(self.edit_rule)
        self.rup_Button.clicked.connect(self.up_rule)
        self.rdelete_Button.clicked.connect(self.del_rule)
        self.rclear_Button.clicked.connect(self.clear_rule)
        self.rdown_Button.clicked.connect(self.dn_rule)
        self.start_button.clicked.connect(self.start_)
        self.clear_button.clicked.connect(self.canvas.rreset)

    def start_(self):
        pattern = self.patternsb.text()
        lenght = self.sizesb.value()
        angle = self.anglesb.value()
        travel_length = self.lensb.value()
        pencilling = (
            self.canvas.forward, self.canvas.back, self.canvas.square, self.canvas.circle, self.canvas.triangle)
        turns = (self.canvas.rleft, self.canvas.rright)
        travels = (self.canvas.vforward, self.canvas.vback)
        rules = {}
        self.canvas.set_clr_list(self.color_list)
        self.canvas.rreset()
        self.canvas.pen.setWidth(self.linewidthsb.value())
        res = []
        le = []
        for i in self.comdict.keys():
            res += re.findall(i + r"\(\d+\)", pattern)
        for i in res:
            pattern = pattern.replace(f'{i}', f'{i[0] * int(i.replace(")", "")[2:])}')
        res.clear()
        for j in range(self.rules_list.count()):
            l = self.rules_list.item(j).text().split()
            for i in self.comdict.keys():
                le += re.findall(i + r"\(\d+\)", l[1])
            for i in le:
                l[1] = l[1].replace(f'{i}', f'{i[0] * int(i.replace(")", "")[2:])}')
            for i in self.comdict.keys():
                le += re.findall(i + r"\(\d+\)", l[0])
            for i in le:
                l[0] = l[0].replace(f'{i}', f'{i[0] * int(i.replace(")", "")[2:])}')
            if len(l) > 1:
                rules[l[0]] = l[1]
        for i in self.comdict.keys():
            res += re.findall(i + r"\(\d+\)", pattern)
        for i in res:
            pattern = pattern.replace(f'{i}', f'{i[0] * int(i.replace(")", "")[2:])}')
        for i in range(self.depthsb.value()):
            for key, value in rules.items():
                pattern = pattern.replace(f'{key}', f'{value}')
        for i in range(len(pattern)):
            if pattern[i] in self.comdict:
                if self.comdict[pattern[i]] in pencilling:
                    self.comdict[pattern[i]](lenght)
                elif self.comdict[pattern[i]] in turns:
                    self.comdict[pattern[i]](angle)
                elif self.comdict[pattern[i]] in travels:
                    self.comdict[pattern[i]](travel_length)
                else:
                    self.comdict[pattern[i]]()

    def backgr(self):
        self.canvas.setBackgroundBrush(QColorDialog().getColor())

    def clear_clr(self):
        self.color_list.clear()

    def delclr(self):
        self.color_list.takeItem(self.color_list.currentRow())

    def up_clr(self):
        ind = self.color_list.currentRow()
        if ind > 0:
            item = self.color_list.takeItem(ind)
            self.color_list.insertItem(ind - 1, item)
            self.color_list.setCurrentItem(item)

    def dn_clr(self):
        ind = self.color_list.currentRow()
        if ind < self.color_list.count():
            item = self.color_list.takeItem(ind)
            self.color_list.insertItem(ind + 1, item)
            self.color_list.setCurrentItem(item)

    def edit_clr(self):
        item = self.color_list.item(self.color_list.currentRow())
        if item is not None:
            clr = QColorDialog().getColor()
            item.setText(f'#{hex(clr.rgb()).upper()[4:]}')
            item.setData(3, clr)

    def add_clr(self):
        c = QColorDialog.getColor()
        self.color_list.insertItem(self.color_list.count(), f'#{hex(c.rgb()).upper()[4:]}')
        self.color_list.item(self.color_list.count() - 1).setData(3, c)

    def add_rule(self):
        ind = self.rules_list.currentRow()
        item, ok = QInputDialog.getText(self, 'Новое правило', 'правило')
        if item and ok is not None:
            self.rules_list.insertItem(ind, item)

    def edit_rule(self):
        item = self.rules_list.item(self.rules_list.currentRow())
        if item is not None:
            txt, ok = QInputDialog.getText(self, 'Изменение правила', 'правило')
            if item and ok is not None:
                item.setText(f'{txt}')

    def up_rule(self):
        ind = self.rules_list.currentRow()
        if ind > 0:
            item = self.rules_list.takeItem(ind)
            self.rules_list.insertItem(ind - 1, item)
            self.rules_list.setCurrentItem(item)

    def del_rule(self):
        self.rules_list.takeItem(self.rules_list.currentRow())

    def clear_rule(self):
        self.rules_list.clear()

    def dn_rule(self):
        ind = self.rules_list.currentRow()
        if ind < self.rules_list.count():
            item = self.rules_list.takeItem(ind)
            self.rules_list.insertItem(ind + 1, item)
            self.rules_list.setCurrentItem(item)

    def settings_win(self):
        settings = Settingdialog(self.sizesb.font(),
                                 self.patternsb.font(),
                                 self.label.font(),
                                 self.rules_list.font(),
                                 self.color_list.font(),
                                 self.start_button.font())
        settings.show()
        settings.exec_()
        sb = settings.fnt_for_sb
        le = settings.fnt_for_le
        lb = settings.fnt_for_lb
        rlw = settings.fnt_fr_rlw
        clw = settings.fnt_fr_clw
        btn = settings.fnt_fr_btn
        self.comdict.clear()
        self.comdict = {settings.forw: self.canvas.forward,
                        settings.back: self.canvas.back,
                        settings.left: self.canvas.rleft,
                        settings.righ: self.canvas.rright,
                        settings.vfor: self.canvas.vforward,
                        settings.vbac: self.canvas.vback,
                        settings.colb: self.canvas.change_color,
                        settings.scvr: self.canvas.square,
                        settings.circ: self.canvas.circle,
                        settings.tria: self.canvas.triangle}
        self.sizesb.setFont(sb)
        self.lensb.setFont(sb)
        self.anglesb.setFont(sb)
        self.linewidthsb.setFont(sb)
        self.depthsb.setFont(sb)
        self.patternsb.setFont(le)
        self.label.setFont(lb)
        self.label_3.setFont(lb)
        self.label_4.setFont(lb)
        self.label_5.setFont(lb)
        self.label_8.setFont(lb)
        self.label_9.setFont(lb)
        self.rules_list.setFont(rlw)
        self.color_list.setFont(clw)
        self.clear_button.setFont(btn)
        self.start_button.setFont(btn)
        self.up_Button.setFont(btn)
        self.add_Button.setFont(btn)
        self.down_Button.setFont(btn)
        self.edit_Button.setFont(btn)
        self.rup_Button.setFont(btn)
        self.rdown_Button.setFont(btn)
        self.radd_Button.setFont(btn)
        self.rclear_Button.setFont(btn)
        self.rdelete_Button.setFont(btn)
        self.redit_Button.setFont(btn)
        self.delete_Button.setFont(btn)
        self.clear_Button.setFont(btn)

    @staticmethod
    def helpwi():
        h = Helpwin()
        h.exec_()

    def kkoh(self):
        self.patternsb.setText('F')
        self.rules_list.clear()
        self.rules_list.addItem("F FLFRRFLF")
        self.sizesb.setValue(20)
        self.anglesb.setValue(60)
        self.depthsb.setValue(3)
        self.linewidthsb.setValue(3)

    def klevi(self):
        self.patternsb.setText('F')
        self.rules_list.clear()
        self.rules_list.addItem("F LFRRFL")
        self.sizesb.setValue(40)
        self.anglesb.setValue(45)
        self.depthsb.setValue(3)
        self.linewidthsb.setValue(3)

    def sertria(self):
        self.patternsb.setText('T')
        self.rules_list.clear()
        self.rules_list.addItem("V VV")
        self.rules_list.addItem("N NN")
        self.rules_list.addItem("T TVTNLVRTLNR")
        self.sizesb.setValue(25)
        self.anglesb.setValue(60)
        self.depthsb.setValue(3)
        self.lensb.setValue(25)
        self.linewidthsb.setValue(1)

    def open_file(self):
        filename = QFileDialog.getOpenFileName()[0]
        if os.path.isfile(filename) and filename[-4:] == '.txt':
            file = open(filename, encoding='cp1251')
            with file:
                data = str(file.read()).replace('=', ' ').replace('\n', ' ').split()
                datalist = ["Pensize", "Depth", "Size", "Angle", "Lenght"]
                blist = [self.linewidthsb, self.depthsb,
                         self.sizesb, self.anglesb, self.lensb]
                for i in range(len(datalist)):
                    if datalist[i] in data:
                        blist[i].setValue(int(data[data.index(datalist[i]) + 1:data.index(datalist[i]) + 2][0]))
                if "Pattern" in data:
                    self.patternsb.setText(str(data[data.index("Pattern") + 1:data.index("Pattern") + 2][0]))
                if "Rules" in data:
                    self.rules_list.clear()
                    _ruls = data[data.index('Rules') + 1:data.index("Rules_end")]
                    for i in range(0, len(_ruls), 2):
                        self.rules_list.addItem(f'{_ruls[i]} {_ruls[i + 1]}')
                if 'Colorlist' in data:
                    self.color_list.clear()
                    _clrlst = data[data.index('Colorlist') + 1:data.index("Colorlist_end")]
                    for i in range(len(_clrlst)):
                        if _clrlst[i].isdigit():
                            self.color_list.insertItem(i, f'#{hex(int(_clrlst[i])).upper()[4:]}')
                            self.color_list.item(i).setData(3, QColor.fromRgb(int(_clrlst[i])))

    def fsavealg(self):
        filename = QFileDialog.getSaveFileName()[0]
        if len(filename) != 0:
            if filename[-4:] != '.txt':
                filename += '.txt'
            file = open(filename, 'w', encoding='cp1251')
            c = ''
            r = ''
            with file:
                for i in range(self.color_list.count()):
                    c += " " + str(self.color_list.item(i).data(3).rgb())
                for i in range(self.rules_list.count()):
                    r += " " + self.rules_list.item(i).text()
                text = (f'Pensize={self.linewidthsb.value()}\n'
                        f'Depth={self.depthsb.value()}\n'
                        f'Size={self.sizesb.value()}\n'
                        f'Angle={self.anglesb.value()}\n'
                        f'Lenght={self.lensb.value()}\n'
                        f'Pattern={self.patternsb.text()}\n'
                        f'Rules={r}\nRules_end\n'
                        f'Colorlist={c}\nColorlist_end')
                file.write(text)

    def fsaveimg(self):
        filename = QFileDialog.getSaveFileName()[0]
        if len(filename) != 0:
            if filename[-4:] != '.png':
                filename += '.png'
            photo = QImage(self.canvas.size(), QImage.Format_ARGB32)
            painter = QPainter(photo)
            self.canvas.render(painter)
            painter.end()
            photo.save(filename)


if __name__ == "__main__":
    ui = Mainwindowqt()
    ui.app.exec()
