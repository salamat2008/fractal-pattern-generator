import json
import os
import re
import sys
from random import randint

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QCursor, QImage, QPainter
from PyQt5.QtWidgets import (QFileDialog, QMainWindow,
                             QApplication, QSizePolicy,
                             QWidget, QGridLayout, QMenuBar, QMenu,
                             QDockWidget, QVBoxLayout, QHBoxLayout,
                             QFormLayout, QLabel, QSpinBox, QLineEdit,
                             QListWidget, QPushButton, QGroupBox, QInputDialog, QColorDialog,
                             QDoubleSpinBox)

from myView import Mycanvas
from myhelp import Helpwin
from settingdial import Settingdialog


class Mainwindowqt(QMainWindow):

    def __init__(self):
        """Эта функция определяет класс Mainwindowqt, который создает главное окно приложения.
            Он наследуется от класса QMainWindow из библиотеки PyQt5.
            В конструкторе класса определены все элементы интерфейса,
            такие как меню, виджеты, кнопки, их размещение и настройки.
            В методе __init__ создается экземпляр класса QApplication и устанавливаются размеры и заголовок главного окна.
            Затем создаются и настраиваются все необходимые виджеты, такие как холст (MyCanvas), меню, кнопки и т.д.
            Затем создаются различные методы для настройки виджетов и обработчиков событий,
            такие как actions_setter, spinboxs, widget_placer, text_setter.
            В конце, создается экземпляр класса Mainwindowqt и вызывается метод show, чтобы отобразить окно приложения."""
        self.app = QApplication(sys.argv)
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.resize(1000, 800)
        size_polic = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setMinimumSize(QSize(400, 560))
        self.setWindowTitle("Генератор фрактальных узоров")
        self.centralwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.canvas = Mycanvas(self.centralwidget)
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
        self.label_linewidthsb = QLabel(self.dockWidgetContents_2)
        self.linewidthsb = QSpinBox(self.dockWidgetContents_2)
        self.label_3 = QLabel(self.dockWidgetContents_2)
        self.depthsb = QSpinBox(self.dockWidgetContents_2)
        self.label_4 = QLabel(self.dockWidgetContents_2)
        self.sizesb = QDoubleSpinBox(self.dockWidgetContents_2)
        self.label_anglesb = QLabel(self.dockWidgetContents_2)
        self.anglesb = QSpinBox(self.dockWidgetContents_2)
        self.label_9 = QLabel(self.dockWidgetContents_2)
        self.lensb = QDoubleSpinBox(self.dockWidgetContents_2)
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
        self.label_ranglesb = QLabel(self.dockWidgetContents_2)
        self.label_rsizesb = QLabel(self.dockWidgetContents_2)
        self.rsizesb = QDoubleSpinBox(self.dockWidgetContents_2)
        self.ranglesb = QDoubleSpinBox(self.dockWidgetContents_2)
        self.formLayout_2_label_tuple = (
            self.label_linewidthsb, self.label_3, self.label_4, self.label_rsizesb, self.label_anglesb,
            self.label_ranglesb, self.label_9, self.label_8)
        self.formLayout_2_field_tuple = (
            self.linewidthsb, self.depthsb, self.sizesb, self.rsizesb, self.anglesb, self.ranglesb, self.lensb,
            self.patternsb)
        self.comdict = {"F": self.canvas.forward,
                        "B": self.canvas.back,
                        "L": self.canvas.rleft,
                        "R": self.canvas.rright,
                        "V": self.canvas.vforward,
                        "N": self.canvas.vback,
                        "C": self.canvas.change_color,
                        "S": self.canvas.square,
                        "E": self.canvas.circle,
                        "T": self.canvas.triangle,
                        "X": self.canvas.set_start,
                        "Z": self.canvas.go_to_start
                        }
        self.actions_setter()
        self.spinboxs_setter()
        self.widget_placer()
        self.text_setter()
        self.btn_fnc_setter()
        self.show()

    def actions_setter(self):
        """Добавляет действия в меню"""
        self.file.addAction("Открыть файл", self.open_file)
        self.file.addAction("Сохранить алгоритм", self.fsavealg)
        self.file.addAction("Сохранить изображение", self.fsaveimg)
        self.file.addAction("Выход", sys.exit)
        self.settings.addAction("Шрифты и обозначения", self.settings_win)
        self.settings.addAction("Фон", self.backgr_setter)
        self.help.addAction("Что делать?", self.helpwi)
        self.help.addSeparator()
        self.help.addAction("Кривая Коха", self.kkoh)
        self.help.addAction("С-кривая Леви", self.klevi)
        self.help.addAction("Треуголник Серпинского", self.sertria)
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.settings.menuAction())
        self.menubar.addAction(self.help.menuAction())

    def spinboxs_setter(self):
        """Настраивает числовые поля."""
        self.linewidthsb.setMinimum(1)
        self.linewidthsb.setMaximum(999999999)
        self.linewidthsb.setProperty("value", 1)
        self.depthsb.setMaximum(999999999)
        self.anglesb.setMaximum(360)
        self.anglesb.setSingleStep(5)
        self.anglesb.setProperty("value", 60)
        self.lensb.setMaximum(999999999)
        self.lensb.setSingleStep(5)
        self.sizesb.setMaximum(999999999)
        self.sizesb.setSingleStep(5)
        self.sizesb.setProperty("value", 100)
        self.ranglesb.setMaximum(100)
        self.ranglesb.setSingleStep(1)
        self.rsizesb.setMaximum(100)
        self.rsizesb.setSingleStep(1)

    def widget_placer(self):
        """Распологает виджеты и контейнеры."""
        for i in range(len(self.formLayout_2_label_tuple)):
            self.formLayout_2.setWidget(i, QFormLayout.LabelRole, self.formLayout_2_label_tuple[i])
            self.formLayout_2.setWidget(i, QFormLayout.FieldRole, self.formLayout_2_field_tuple[i])
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
        """Устанавливает текст для виджетов."""
        self.color_list.addItem("#000000")
        self.color_list.item(0).setData(3, QColor.fromRgb(4278190080))
        self.rules_list.addItem("F FLFRRFLF")
        self.file.setTitle("Файл")
        self.settings.setTitle("Настройки")
        self.help.setTitle("Помощь")
        self.dockWidget_1.setWindowTitle("Параметры")
        self.label_linewidthsb.setText("Толщина")
        self.label_3.setText("Глубина")
        self.label_4.setText("Размер")
        self.label_rsizesb.setText("Отклонения размера")
        self.label_anglesb.setText("Угол поворота")
        self.label_ranglesb.setText("Отклонения угла поворота")
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

    def btn_fnc_setter(self):
        """Устанавливает обработчики событий для различных кнопок и связывает их с соответствующими методами."""
        self.add_Button.clicked.connect(self.add_clr)
        self.edit_Button.clicked.connect(self.edit_clr)
        self.up_Button.clicked.connect(self.up_clr)
        self.delete_Button.clicked.connect(lambda: self.color_list.takeItem(self.color_list.currentRow()))
        self.clear_Button.clicked.connect(self.color_list.clear)
        self.down_Button.clicked.connect(self.dn_clr)
        self.radd_Button.clicked.connect(self.add_rule)
        self.redit_Button.clicked.connect(self.edit_rule)
        self.rup_Button.clicked.connect(self.up_rule)
        self.rdelete_Button.clicked.connect(lambda: self.rules_list.takeItem(self.rules_list.currentRow()))
        self.rclear_Button.clicked.connect(self.rules_list.clear)
        self.rdown_Button.clicked.connect(self.dn_rule)
        self.start_button.clicked.connect(self.start_)
        self.clear_button.clicked.connect(self.canvas.rreset)

    def start_(self):
        """Первоначально из виджетов пользовательского интерфейса(LineEdit, SpinBox)
        получаются значения атрибутов "pattern", "length", "angle", "random angle", "random length" и "travel length".
        Затем происходит обработка текста "pattern" с использованием регулярных выражений.
        Все совпадения шаблонов команд типа "a(n)"(где a - символ команды, n - целое число)
        заменяются на соответствующую последовательность символов a.
        Например, "F(3)" будет заменено на "FFF".
        Далее происходит обработка списка правил.
        Каждая строка списка разделяется на две части - "отправную" и "конечную" части правила.
        Для каждой части происходит замена шаблонов команд на последовательности символов(если они есть).
        Затем происходит последовательное применение всех правил к шаблону.
        Замена происходит до тех пор, пока в шаблоне остаются шаблоны команд(ключи словаря "rules").
        Далее происходит обработка каждого символа в полученном шаблоне.
        Если символ есть в словаре "comdict", то вызывается соответствующая функция, которая отрисовывает линию,
        поворачивает вектор движения пера или перемещает перо.
        После каждого шага отрисовки вызывается метод "update()", который принудительно перерисовывает виджет."""
        pattern = self.patternsb.text()
        length = self.sizesb.value()
        angle = self.anglesb.value()
        rand_angle = self.ranglesb.value() * angle / 100
        rand_length = self.rsizesb.value() * length / 100
        travel_length = self.lensb.value()
        pencilling = (
            self.canvas.forward, self.canvas.back, self.canvas.square, self.canvas.circle, self.canvas.triangle)
        turns = (self.canvas.rleft, self.canvas.rright)
        travels = (self.canvas.vforward, self.canvas.vback)
        rules = {}
        if self.color_list.count() < 1:
            c = QColorDialog.getColor()
            self.color_list.insertItem(self.color_list.count(), f'#{hex(c.rgb()).upper()[4:]}')
            self.color_list.item(self.color_list.count() - 1).setData(3, c)
        self.canvas.set_clr_list(self.color_list)
        self.canvas.rreset()
        self.canvas.pen.setWidth(self.linewidthsb.value())
        for i in self.comdict.keys():
            pattern = re.sub(f'{i}\(\d+\)', lambda x: i[0] * int(x.group(0).replace(")", "")[2:]), pattern)
        for j in range(self.rules_list.count()):
            l = self.rules_list.item(j).text().split()
            for i in self.comdict.keys():
                l[1] = re.sub(f'{i}\(\d+\)', lambda x: i[0] * int(x.group(0).replace(")", "")[2:]), l[1])
                l[0] = re.sub(f'{i}\(\d+\)', lambda x: i[0] * int(x.group(0).replace(")", "")[2:]), l[0])
            if len(l) > 1:
                rules[l[0]] = l[1]
        for _ in range(self.depthsb.value()):
            for key, value in rules.items():
                pattern = pattern.replace(key, value)
        for char in pattern:
            if char in self.comdict:
                command = self.comdict[char]
                if command in pencilling:
                    command(length + randint(-1, 1) * rand_length)
                elif command in turns:
                    command(angle + randint(-1, 1) * rand_angle)
                elif command in travels:
                    command(travel_length)
                else:
                    command()

            self.canvas.update()
            self.update()

    def backgr_setter(self):
        self.canvas.setBackgroundBrush(QColorDialog().getColor())

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
        """QColorDialog.getColor():
        Открывает диалог выбора цвета и возвращает выбранный цвет в формате QColor.
        self.color_list.insertItem(...):
        Вставляет новый элемент в виджет списка цветов (self.color_list).
        Формирует текстовую строку для цвета в формате #RRGGBB,
        где RR, GG, BB - шестнадцатеричные представления красного, зеленого и синего компонентов цвета.
        Вставляет эту строку в список цветов.
        self.color_list.item(...).setData(3, c):
        Получает последний вставленный элемент списка цветов.
        Устанавливает для данного элемента пользовательские данные с ключом 3 и значением выбранного цвета c(объект QColor)."""
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

    def dn_rule(self):
        ind = self.rules_list.currentRow()
        if ind < self.rules_list.count():
            item = self.rules_list.takeItem(ind)
            self.rules_list.insertItem(ind + 1, item)
            self.rules_list.setCurrentItem(item)

    def settings_win(self) -> None:
        """"Создается экземпляр класса Settingdialog с передачей
            текущих шрифтов элементов пользовательского интерфейса в качестве аргументов.
            Вызывается метод exec_() для открытия окна настроек.
            Из объекта settings получаются новые шрифты для каждого элемента пользовательского интерфейса
            и сохраняются в соответствующие переменные.
            Словарь comdict очищается и заполняется новыми значениями на основе выбранных настроек.
            Шрифты элементов пользовательского интерфейса обновляются, используя полученные новые шрифты.
            Возвращаемый тип: отсутствует"""
        settings = Settingdialog(self.sizesb.font(),
                                 self.patternsb.font(),
                                 self.label_linewidthsb.font(),
                                 self.rules_list.font(),
                                 self.color_list.font(),
                                 self.start_button.font())
        settings.exec_()
        font_for_spinboxs = settings.fnt_for_sb
        font_for_lineedit = settings.fnt_for_le
        font_for_label = settings.fnt_for_lb
        font_for_rulelist = settings.fnt_fr_rlw
        font_for_colorlist = settings.fnt_fr_clw
        font_for_button = settings.fnt_fr_btn
        self.comdict.clear()
        self.comdict = {settings.mybind_list[0]: self.canvas.forward,
                        settings.mybind_list[1]: self.canvas.back,
                        settings.mybind_list[2]: self.canvas.rleft,
                        settings.mybind_list[3]: self.canvas.rright,
                        settings.mybind_list[4]: self.canvas.vforward,
                        settings.mybind_list[5]: self.canvas.vback,
                        settings.mybind_list[6]: self.canvas.change_color,
                        settings.mybind_list[7]: self.canvas.square,
                        settings.mybind_list[8]: self.canvas.circle,
                        settings.mybind_list[9]: self.canvas.triangle,
                        settings.mybind_list[10]: self.canvas.set_start,
                        settings.mybind_list[11]: self.canvas.go_to_start}
        self.sizesb.setFont(font_for_spinboxs)
        self.lensb.setFont(font_for_spinboxs)
        self.anglesb.setFont(font_for_spinboxs)
        self.linewidthsb.setFont(font_for_spinboxs)
        self.depthsb.setFont(font_for_spinboxs)
        self.ranglesb.setFont(font_for_spinboxs)
        self.rsizesb.setFont(font_for_spinboxs)
        self.patternsb.setFont(font_for_lineedit)
        for i in range(len(self.formLayout_2_label_tuple)):
            self.formLayout_2_label_tuple[i].setFont(font_for_label)
        self.rules_list.setFont(font_for_rulelist)
        self.color_list.setFont(font_for_colorlist)
        self.clear_button.setFont(font_for_button)
        self.start_button.setFont(font_for_button)
        self.up_Button.setFont(font_for_button)
        self.add_Button.setFont(font_for_button)
        self.down_Button.setFont(font_for_button)
        self.edit_Button.setFont(font_for_button)
        self.rup_Button.setFont(font_for_button)
        self.rdown_Button.setFont(font_for_button)
        self.radd_Button.setFont(font_for_button)
        self.rclear_Button.setFont(font_for_button)
        self.rdelete_Button.setFont(font_for_button)
        self.redit_Button.setFont(font_for_button)
        self.delete_Button.setFont(font_for_button)
        self.clear_Button.setFont(font_for_button)

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
        """Сначала функция открывает диалоговое окно для выбора файла с помощью QFileDialog.getOpenFileName()[0].
        Затем она проверяет, является ли выбранный файл действительным файлом и имеет расширение .json.
        Если файл прошел проверку, то функция открывает его с помощью open(filename)
        и загружает содержимое файла в переменную data с помощью json.load(file).
        Функция устанавливает значения различных параметров, используя данные из переменной data.
        Например, значение Pensize устанавливается с помощью self.linewidthsb.setValue(data['Pensize']).
        Затем функция проверяет наличие ключей Pattern,
        Rules и Colorlist в переменной data и выполняет соответствующие действия.
        Например, если есть ключ Pattern, то значение этого ключа устанавливается
        в поле patternsb с помощью self.patternsb.setText(pattern_value).
        Для ключей Rules и Colorlist, функция очищает соответствующие списки rules_list и color_list,
        а затем добавляет элементы из rules_data и color_data в эти списки.
        В случае ключа Colorlist, функция также создает элементы списка с соответствующими цветами."""
        filename = QFileDialog.getOpenFileName()[0]
        if os.path.isfile(filename) and filename.endswith('.json'):
            with open(filename) as file:
                data = json.load(file)
            self.linewidthsb.setValue(data['Pensize'])
            self.depthsb.setValue(data['Depth'])
            self.sizesb.setValue(data['Size'])
            self.anglesb.setValue(data['Angle'])
            self.lensb.setValue(data['Lenght'])

            if 'Pattern' in data:
                pattern_value = data['Pattern']
                self.patternsb.setText(pattern_value)

            if 'Rules' in data:
                self.rules_list.clear()
                rules_data = data['Rules']
                for rule in rules_data:
                    self.rules_list.addItem(rule)

            if 'Colorlist' in data:
                self.color_list.clear()
                color_data = data['Colorlist']
                for item in color_data:
                    hex_value = hex(int(item)).upper()[4:]
                    color = QColor.fromRgb(int(item))
                    self.color_list.addItem(f'#{hex_value}')
                    self.color_list.item(self.color_list.count() - 1).setData(3, color)

    def fsavealg(self):
        filename = QFileDialog.getSaveFileName()[0]
        if len(filename) != 0:
            if filename[-5:] != '.json':
                filename += '.json'
        data = {
            'Pensize': self.linewidthsb.value(),
            'Depth': self.depthsb.value(),
            'Size': self.sizesb.value(),
            'Angle': self.anglesb.value(),
            'Lenght': self.lensb.value(),
            'Pattern': self.patternsb.text(),
            'Rules': [self.rules_list.item(i).text() for i in range(self.rules_list.count())],
            'Colorlist': [str(self.color_list.item(i).data(3).rgb()) for i in range(self.color_list.count())]
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def fsaveimg(self):
        filename, _ = QFileDialog.getSaveFileName(filter="PNG (*.png)")
        if filename:
            photo = QImage(self.canvas.size(), QImage.Format_ARGB32)
            painter = QPainter(photo)
            self.canvas.render(painter)
            painter.end()
            photo.save(filename)


if __name__ == "__main__":
    ui = Mainwindowqt()
    ui.app.exec()
