"""
print(f'Этот кодер просто {input()}')
"""
import json
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QDockWidget, QDoubleSpinBox, QFileDialog, QFormLayout, QGroupBox,
                               QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenu, QMenuBar, QMessageBox,
                               QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

from MWidgets import MButton, MColorlistwidget, MHelpwin, MTextlistwidget, MCanvas


class MainWindow(QMainWindow):
    """
    Does this really work?
    """
    formLayout_labels = ('Толщина', 'Глубина', 'Размер', 'Отклонения размера', 'Угол поворота',
                         'Отклонения угла поворота', 'Длинна перемещения', 'Шаблон')
    formLayout_fields = {}

    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()
        self.resize(1000, 800)
        self.setWindowTitle("Генератор фрактальных узоров")
        self.setCentralWidget(QWidget(self))
        self.setMenuBar(QMenuBar(self))

        lay = QVBoxLayout(self.centralWidget())
        self.canvas = MCanvas(self.centralWidget())
        lay.addWidget(self.canvas)
        self.centralWidget().setLayout(lay)

        self.file = QMenu("Файл", self.menuBar())
        self.file.addAction("Открыть файл", self.open_file)
        self.file.addAction("Сохранить алгоритм", self.save_algorithm)
        self.file.addAction("Сохранить изображение")

        self.settings = QMenu("Настройки", self.menuBar())
        self.settings.addAction("Обозначения", self.settings_win)

        self.help = QMenu("Помощь", self.menuBar())
        self.help.addAction("Что делать?", self.show_help)
        self.help.addSeparator()
        self.help.addAction("Кривая Коха", self.koh_curve)
        self.help.addAction("С-кривая Леви", self.levi_c_curve)
        self.help.addAction("Треуголник Серпинского", self.sierpinski_triangle)

        self.options_dockWidget = QDockWidget("Параметры", self)
        self.options_dWContent = QWidget(self.options_dockWidget)
        self.options_dockWidget.setWidget(self.options_dWContent)

        self.options_dWContent_vLayout = QVBoxLayout(self.options_dWContent)
        self.options_formLayout = QFormLayout(self.options_dWContent)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.options_dockWidget)

        for row, text in enumerate(self.formLayout_labels):
            self.options_formLayout.setWidget(row, QFormLayout.ItemRole.LabelRole, QLabel(text, self.options_dWContent))
            if text in ('Толщина', 'Глубина'):
                field = QSpinBox(self.options_dWContent)
                field.setMaximum(1_000_000)
            elif text == 'Шаблон':
                field = QLineEdit('F', self.options_dWContent)
            else:
                field = QDoubleSpinBox(self.options_dWContent)
                field.setMaximum(1_000_000)
            if text == 'Толщина':
                field.setMinimum(1)
            elif text == 'Размер':
                field.setValue(100)
            elif text == 'Угол поворота':
                field.setValue(60)
            self.formLayout_fields[text] = field
            self.options_formLayout.setWidget(row, QFormLayout.ItemRole.FieldRole, field)

        self.rules_gBox = QGroupBox('Список правил', self.options_dWContent)
        self.rules_hLayout = QHBoxLayout(self.rules_gBox)
        self.rules_list = MTextlistwidget(self.rules_gBox)
        self.rules_list.addItem('F FLFRRFLF')
        self.ruleslist_vLayout = QVBoxLayout(self.rules_gBox)
        self.ruleslist_vLayout.setSpacing(0)

        self.colorlist_gBox = QGroupBox('Список цветов', self.options_dWContent)
        self.colorlist_hLayout = QHBoxLayout(self.colorlist_gBox)
        self.colorlist = MColorlistwidget(self.colorlist_gBox)
        self.colorlist.addItem(QColor(4278190080))
        self.colorlist_vLayout = QVBoxLayout(self.colorlist_gBox)
        self.colorlist_vLayout.setSpacing(0)

        spolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        temporary = zip(MColorlistwidget.buttons, self.colorlist.getfunctions(), self.rules_list.getfunctions())
        for text, cfunc, rfunc in temporary:
            self.ruleslist_vLayout.addWidget(MButton(text, self.rules_gBox, func = rfunc, sizepolicy = spolicy))
            self.colorlist_vLayout.addWidget(MButton(text, self.colorlist_gBox, func = cfunc, sizepolicy = spolicy))

        self.start_button = MButton('Старт', self.options_dWContent, func = self.start_)
        self.clear_button = MButton('Очистить', self.options_dWContent)
        self.options_dockWidget.setMinimumSize(223, 670)
        self.options_dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.menuBar().addAction(self.file.menuAction())
        self.menuBar().addAction(self.settings.menuAction())
        self.menuBar().addAction(self.help.menuAction())

        self.options_dWContent_vLayout.addLayout(self.options_formLayout)
        self.rules_hLayout.addWidget(self.rules_list)
        self.rules_hLayout.addLayout(self.ruleslist_vLayout)
        self.colorlist_hLayout.addWidget(self.colorlist)
        self.options_dWContent_vLayout.addWidget(self.rules_gBox)
        self.colorlist_hLayout.addLayout(self.colorlist_vLayout)
        self.options_dWContent_vLayout.addWidget(self.colorlist_gBox)
        self.options_dWContent_vLayout.addWidget(self.start_button)
        self.options_dWContent_vLayout.addWidget(self.clear_button)
        self.options_dockWidget.raise_()

        self.show()

    def start_(self):
        """
        :return: None
        """
        comm = tuple('FBLRVNST')
        self.canvas.start(self.rules_list.gettextlist(),
                          self.formLayout_fields['Шаблон'].text(),
                          self.formLayout_fields['Глубина'].value(),
                          self.formLayout_fields['Размер'],
                          self.formLayout_fields['Угол поворота'],
                          (self.formLayout_fields['Отклонения угла поворота'].value(),
                           self.formLayout_fields['Отклонения размера'].value()),
                          self.formLayout_fields['Толщина'],
                          self.formLayout_fields['Длинна перемещения'],
                          comm,
                          self.colorlist.getcolorlist())
        self.canvas.update()

    def settings_win(self):
        """
        :return: None
        """
        pass
        # settings = Settingdialog(self, binds = tuple(self.command_dict.keys()))
        # settings.exec_()

    def koh_curve(self) -> None:
        """

        :return: None
        """
        self.formLayout_fields['Шаблон'].setText('F')
        self.rules_list.clear()
        self.rules_list.addtext("F FLFRRFLF")
        self.formLayout_fields['Угол поворота'].setValue(60)
        self.formLayout_fields['Глубина'].setValue(3)
        self.formLayout_fields['Толщина'].setValue(3)

    def levi_c_curve(self):
        """

        :return: None
        """
        self.formLayout_fields['Шаблон'].setText('F')
        self.rules_list.clear()
        self.rules_list.addtext("F LFRRFL")
        self.formLayout_fields['Угол поворота'].setValue(45)
        self.formLayout_fields['Глубина'].setValue(3)
        self.formLayout_fields['Толщина'].setValue(3)

    def sierpinski_triangle(self):
        """

        :return: None
        """
        self.formLayout_fields['Шаблон'].setText('T')
        self.rules_list.clear()
        self.rules_list.addtext("V VV")
        self.rules_list.addtext("N NN")
        self.rules_list.addtext("T TVTNLVRTLNR")
        self.formLayout_fields['Угол поворота'].setValue(60)
        self.formLayout_fields['Глубина'].setValue(3)
        self.formLayout_fields['Длинна перемещения'].setValue(25)
        self.formLayout_fields['Толщина'].setValue(1)

    def open_file(self):
        """

        :return: None
        """
        filename, _ = QFileDialog.getOpenFileName(filter = 'JSON(*.json)')
        if os.path.isfile(filename) and filename.endswith('.json'):
            try:
                with json.load(open(filename, encoding = 'utf-8')) as data:
                    data: dict
                    fields = (self.formLayout_fields.values())
                    if len(data) > 0:
                        for field, key in zip(fields, data[list(data.keys())[0]]):
                            if isinstance(field, QDoubleSpinBox | QSpinBox):
                                field.setValue(data[key])
                            elif isinstance(field, QLineEdit):
                                field.setText(data[key])
                            elif isinstance(field, QLineEdit):
                                self.rules_list.clear()
                                for rule in data['Rules']:
                                    self.rules_list.addtext(rule)

                        if 'Colorlist' in data:
                            self.colorlist.clear()
                            for item in data['Colorlist']:
                                color = QColor(int(item))
                                self.colorlist.addcolor(color)

            except Exception as e:
                self.show_warning('Файл поврежден')
                raise e
            finally:
                return

    def save_algorithm(self):
        """

        :return: None
        """
        filename, _ = QFileDialog.getSaveFileName(filter = "JSON (*.json)")
        if len(filename) != 0:
            with open(filename, mode = 'rw') as file:
                data: dict = json.load(file)
                fractal_name, result = 1, 1  # dialogs.ComboboxDialog.gettext(self, data.keys())
                if result:
                    data[fractal_name] = {
                        'Pensize': self.formLayout_fields['Толщина'].value(),
                        'Depth': self.formLayout_fields['Глубина'].value(),
                        'Size': self.formLayout_fields['Размер'].value(),
                        'Angle': self.formLayout_fields['Угол поворота'].value(),
                        'Length': self.formLayout_fields['Длинна перемещения'].value(),
                        'Pattern': self.formLayout_fields['Шаблон'].text(),
                        'Rules': [self.rules_list.item(i).text() for i in range(self.rules_list.count())],
                        'Colors': [self.colorlist.item(i).data(3).rgb() for i in range(self.colorlist.count())]}
                    json.dump(data, file)

    @staticmethod
    def show_help():
        """
        :return: None
        """
        h = MHelpwin()
        h.exec_()

    def show_warning(self, message):
        """
        :return: None
        """
        QMessageBox().critical(self, 'Внимание', message)

    def exec(self):
        """
        :return: None
        """
        self.app.exec_()


if __name__ == "__main__":
    print('completed')
