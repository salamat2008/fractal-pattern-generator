from math import cos, radians, sin
from random import gauss, triangular
from typing import Callable, Optional

from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap, QRgba64
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from Lsystems.Lsystem import LSystem


class MButton(QPushButton):
    """
    MButton(self, icon: QIcon | QPixmap, text: str, parent: Optional[QWidget] = None,
    func: Optional[Callable], size_policy: Optional[QSizePolicy])

    MButton(self, parent: Optional[QWidget] = None, func: Optional[Callable], sizepolicy: Optional[QSizePolicy])

    MButton(self, text: str, parent: Optional[QWidget] = None,
    func: Optional[Callable], size_policy: Optional[QSizePolicy])
    :return: None
    """

    def __init__(
            self,
            *args,
            func: Optional[Callable] = ...,
            sizepolicy: Optional[QSizePolicy] = ...,
    ):
        super().__init__(*args)
        self.function = func
        if isinstance(sizepolicy, QSizePolicy):
            self.setSizePolicy(sizepolicy)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if e.button() == Qt.MouseButton.LeftButton and callable(self.function):
            self.function()


class MHelpwin(QDialog):
    """
    MHelpwin(self)
    :return: None
    """

    def __init__(self):
        super().__init__()
        self.setMinimumSize(360, 240)
        self.setMaximumSize(360, 240)
        self.setWindowTitle("Помощь")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.tabw = QTabWidget(self)
        self.wid = QWidget()
        self.wid2 = QWidget()
        self.tabw.addTab(self.wid, "ничего")
        self.tabw.addTab(self.wid2, "ничего")
        self.layout.addWidget(self.tabw)


class Modifiedlist(QListWidget):
    """
    QListWidget(self, parent: Optional[PySide6.QtWidgets.QWidget] = None)
    :return: None
    """

    buttons = ("Добавить", "Изменить", "Вверх", "Вниз", "Удалить", "Очистить")

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setDragDropMode(self.DragDropMode.InternalMove)
        self.menu = QMenu(self)
        self.menu.addAction("Добавить", self.addItem)
        self.menu.addAction("Изменить", self.editcurrentitem)
        self.menu.addAction("Вверх", self.raise_item)
        self.menu.addAction("Вниз", self.omit_item)
        self.menu.addAction("Удалить", self.takecurrentitem)
        self.menu.addAction("Очистить", self.clear)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def show_menu(self, position: QPoint):
        self.menu.exec(self.mapToGlobal(position))

    def addItem(self, aitem: QListWidgetItem | str):
        super().addItem(aitem)
        self.setCurrentRow(self.count() - 1)

    def editcurrentitem(self):
        print("Doesn't work, this is a function prototype")

    def raise_item(self):
        current = self.currentRow()
        if current > 0:
            item = self.takeItem(current)
            self.insertItem(current - 1, item)
            self.setCurrentItem(item)

    def omit_item(self):
        current = self.currentRow()
        if current < self.count():
            item = self.takeItem(current)
            self.insertItem(current + 1, item)
            self.setCurrentItem(item)

    def takecurrentitem(self) -> QListWidgetItem:
        return self.takeItem(self.currentRow())

    def getfunctions(self) -> tuple:
        return (
            self.addItem,
            self.editcurrentitem,
            self.raise_item,
            self.omit_item,
            self.takecurrentitem,
            self.clear,
        )

    def getitems(self) -> list[QListWidgetItem]:
        return [self.item(index) for index in range(self.count())]


class MTextlistwidget(Modifiedlist):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

    def addItem(self, *args: QListWidgetItem | str):
        """
        If no arguments are passed, the self.addtext method is called
        :param args:
        :return: None
        """
        if len(args) == 0:
            self.addtext()
        else:
            super().addItem(*args)

    def addtext(self, text: str = None):
        """
        If the text parameter is None then QInputDialog is called,
        If the claim button is not pressed or the length of the entered text is zero
        Nothing is added
        otherwise, if the text is a string
        then it is added by the self.additem method
        and becomes current
        otherwise
        TypeEror rises
        :raises TypeEror:
        :param text:
        :return: None
        """
        if isinstance(text, str):
            accepted = True
        elif text is None:
            text, accepted = QInputDialog.getText(self.parent(), "Добавление", "")
        else:
            raise TypeError("The argument must be a string")
        if len(text) > 0 and accepted:
            self.addItem(text)

    def editcurrentitem(self):
        """
        Only works with the current item, if it is not None,
        calls QInputDialog with the text of the current item,
        if the accept button is not clicked or the length of the new text is zero,
        the text remains the same.
        :return: None
        """
        item = self.item(self.currentRow())
        if item is not None:
            itemtext, accepted = QInputDialog.getText(
                    self.parent(), "Изменение", "", text = item.text()
            )
            if len(itemtext) > 0 and accepted:
                item.setText(itemtext)

    def gettextlist(self):
        return [item.text() for item in self.getitems()]


class MColorlistwidget(Modifiedlist):
    ColorRole = Qt.ItemDataRole.UserRole + 1

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.icon = QPixmap(30, 30)
        self.icon.fill(QColor(0, 0, 0, 0))

    def editcurrentitem(self):
        """
        Only works with the current item, if it is not None,
        calls MColorDialog with the color of the current item,
        if the accept button is not clicked,
        the color remains the same.
        :return: None
        """
        item = self.item(self.currentRow())
        if item is not None:
            color, accepted = MColorDialog(
                    item.data(self.ColorRole), self.parent()
            ).getcolor()
            if accepted:
                item.setIcon(QIcon(self.drawiconforitem(color)))
                item.setText(f"#{hex(color.rgb()).upper()[4:]}")
                item.setData(self.ColorRole, color)

    def addItem(self, *args: QListWidgetItem | QColor | str):
        if len(args) == 0:
            self.addcolor()
        elif isinstance(*args, QColor):
            self.addcolor(*args)
        else:
            super().addItem(*args)

    def addcolor(self, color: QColor = None):
        """
        If the color parameter is None then MColorDialog is called,
        If the claim button is not pressed,
        Nothing is added
        otherwise, if the color is a QColor
        then it is added by the self.additem method
        and becomes current
        otherwise
        TypeEror rises
        :raises TypeEror:
        :param color:
        :return: None
        """
        if isinstance(color, QColor):
            accepted = True
        elif color is None:
            color, accepted = MColorDialog(parent = self).getcolor()
        else:
            raise TypeError("The argument must be a QColor")
        if accepted:
            item = QListWidgetItem(
                    QIcon(self.drawiconforitem(color)),
                    f"#{hex(color.rgb()).upper()[4:]}",
                    self,
            )
            item.setData(self.ColorRole, color)
            self.addItem(item)

    def drawiconforitem(self, color: QColor) -> QPixmap:
        icon = self.icon.copy()
        with QPainter(icon) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor("black"), 2))
            painter.setBrush(color)
            painter.drawEllipse(1, 1, icon.height() - 2, icon.width() - 2)
        return icon

    def getcolorlist(self) -> list[QColor]:
        return [item.data(self.ColorRole) for item in self.getitems()]

    def getitems(self) -> list[QListWidgetItem]:
        """
        The color is stored in the MColorlistwidget.ColorRole
        following Qt.ItemDataRole.UserRole as a QColor object
        :return: list[QListWidgetItem]
        """
        return super().getitems()


class MColorDialog(QColorDialog):
    def __init__(
            self,
            initial: QColor | QRgba64 | Qt.GlobalColor | str | int = None,
            parent: QWidget | None = None,
    ):
        super().__init__(initial, parent)

    def getcolor(self) -> tuple[QColor, bool]:
        result = bool(self.exec())
        return self.selectedColor(), result


class MDialog(QDialog):
    def __init__(self, *args, widgets: tuple | list, layouts: tuple | list = None):
        super().__init__(*args)
        self.Vbox = QVBoxLayout(self)
        self.Hbox = QHBoxLayout(self)
        self.accept_button = MButton("Применить", self, func = self.accept)
        self.cancel_button = MButton("Отмена", self, func = self.reject)
        if layouts is not None:
            for layout in layouts:
                self.Vbox.addLayout(layout)
        for widget in widgets:
            self.Vbox.addWidget(widget)
        self.Vbox.addLayout(self.Hbox)
        self.Hbox.addWidget(self.accept_button)
        self.Hbox.addWidget(self.cancel_button)


class Settingdialog(MDialog):
    standart_binds = tuple("FBLRVNCSETXZ")
    labels = (
        "Вперед",
        "Назад",
        "Влево",
        "Вправо",
        "Перемещение вперед",
        "Перемещение назад",
        "Сменить цвет",
        "Квадрат",
        "Круг",
        "Треугольник",
        "Открыть ветку",
        "Закрыть ветку",
    )
    lineedit_list = []

    def __init__(self, *args, binds: tuple[str]):
        formLayout = QFormLayout()
        super().__init__(*args, widgets = (), layouts = (formLayout,))
        formLayout.setParent(self)
        self.setWindowTitle("Настройки")
        self.binds = [*binds]
        for standart, bind, label, row in zip(
                self.standart_binds, self.binds, self.labels, range(len(self.labels))
        ):
            lineedit = QLineEdit(self)
            lineedit.setPlaceholderText(
                    f'введите ключевой символ (стандарт "{standart}")'
            )
            lineedit.setText(f"{bind}")
            self.lineedit_list.append(lineedit)
            formLayout.setWidget(row, formLayout.ItemRole.LabelRole, QLabel(label))
            formLayout.setWidget(row, formLayout.ItemRole.FieldRole, lineedit)

    @staticmethod
    def show_warning(message):
        war = QMessageBox()
        war.setWindowTitle("Внимание")
        war.setText(message)
        war.setIcon(QMessageBox.Icon.Critical)
        war.exec()

    def accept(self):
        spec = set("()123456789\\")
        for lineedit, default_value in zip(self.lineedit_list, self.standart_binds):
            if len(lineedit.text()) < 1:
                lineedit.setText(default_value)
        for index, lineedit in enumerate(self.lineedit_list):
            if any(char in spec for char in lineedit.text()):
                self.show_warning("В обозначениях можно использовать не все символы")
                return
            else:
                self.binds[index] = lineedit.text()
        print(set(self.binds))
        if len(set(self.binds)) < len(self.standart_binds):
            self.show_warning("Обозначения не могут быть одинаковыми")
            return
        super().accept()

    @classmethod
    def getbinds(cls, binds: tuple[str], parent: QWidget = None):
        win = cls(parent, binds = binds)
        result = bool(win.exec())
        return win.binds, result


class SpinboxDialog(MDialog):
    def __init__(self, *args, value: int = 1, title: str = " "):
        self.spinbox = QSpinBox()
        super().__init__(*args, widgets = (self.spinbox,), layouts = ())
        self.value = value
        self.spinbox.setValue(value)
        self.spinbox.setParent(self)
        self.setWindowTitle(title)

    @classmethod
    def getvalue(
            cls, parent: QWidget = None, value: int = 1, title: str = " "
    ) -> tuple[any, bool]:
        win = cls(parent, value = value, title = title)
        result = bool(win.exec())
        return win.value, result

    def accept(self):
        self.value = self.spinbox.value()
        super().accept()


class MComboboxDialog(MDialog):
    def __init__(self, *args, texts):
        self.combobox = QComboBox()
        super().__init__(*args, widgets = (self.combobox,))
        self.combobox.setEditable(True)
        self.combobox.addItems(texts)
        if len(texts) > 0:
            self.combobox.setCurrentText(texts[0])
        self.currentitem = self.combobox.currentText()

    def accept(self):
        self.currentitem = self.combobox.currentText()
        super().accept()

    @classmethod
    def getitem(cls, *args, texts):
        win = cls(*args, texts = texts)
        result = bool(win.exec())
        return win.currentitem, result


class MCanvas(QWidget):
    penwidth = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.turtlestartpoint = QPointF(0, 0)
        self.startpoint = QPointF(0, 0)
        self.pressed = False
        self.colors = None
        self.commands = None
        self.travel_length = None
        self.deviations = None
        self.angle = None
        self.linelenght = None
        self.string = ()
        self.pixmap = None
        self.started = False

    def mousePressEvent(self, event):
        self.startpoint = self.mapToParent(event.position())
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        endpoint = self.mapToParent(event.position())
        if self.pressed:
            self.turtlestartpoint.setX(
                    self.turtlestartpoint.x() + endpoint.x() - self.startpoint.x()
            )
            self.turtlestartpoint.setY(
                    self.turtlestartpoint.y() + endpoint.y() - self.startpoint.y()
            )
            self.started = True
        self.startpoint = QPointF(endpoint)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.pressed = False
        super().mouseReleaseEvent(event)

    def start(
            self,
            rules: str,
            axiom: str,
            number_of_iterations: int,
            linelenght,
            angle: int,
            deviations: tuple[int, int],
            penwidth,
            travel_length,
            commandskeys: tuple[str, ...],
            colors: list[QColor],
    ):
        lsys = LSystem(rules, commandskeys)
        if len(self.string) == 0:
            self.turtlestartpoint = QPoint(self.width() // 20, self.height() // 20 * 19)
        self.string = lsys.generate_action_string(axiom, number_of_iterations)
        self.linelenght = linelenght
        self.angle = angle
        self.deviations = deviations
        self.penwidth = penwidth
        self.travel_length = travel_length
        self.commands = commandskeys
        self.colors = colors
        self.started = True

    def paintEvent(self, event = None):
        if self.pixmap is None or self.pixmap.size() != self.size():
            self.pixmap = QPixmap(self.size())
            self.started = True
        if self.started:
            pen = QPen(
                    QColor(self.colors[0]),
                    self.penwidth.value(),
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
            )
            painter = Turtle(
                    self.pixmap,
                    self.linelenght.value(),
                    self.angle.value(),
                    self.commands,
                    self.travel_length.value(),
                    self.colors,
                    self.deviations[0],
                    self.deviations[1],
                    pen
            )
            painter.fillRect(self.pixmap.rect(), QColor("white"))
            painter.draw(self.string, self.turtlestartpoint)
            painter.end()
            self.started = False
        painter = QPainter(self)
        painter.drawPixmap(QPoint(0, 0), self.pixmap)
        painter.end()
        self.update()
        super().paintEvent(event)

    def wheelEvent(self, event):
        if self.string is not None:
            value = event.angleDelta().y() / 240
            self.linelenght.setValue(self.linelenght.value() + value)
            self.travel_length.setValue(self.travel_length.value() + value)
            self.started = True
        super().wheelEvent(event)


class Turtle(QPainter):
    point = QPointF(0, 0)
    turtleangle = 0
    colorindex = 0

    def __init__(
            self,
            paintdevice,
            linelenght: float | int,
            angle: float | int,
            commandskeys: tuple[str, ...],
            travel_length: int,
            colors: list[QColor],
            random_rotation_percentage: int = 0,
            random_linelenght_percentage: int = 0,
            pen = QColor('black')
    ):
        super().__init__(paintdevice)
        self.mdevice = paintdevice
        self.linelenght = linelenght
        self.travel_length = travel_length
        self.colors = colors
        self.setPen(pen)
        self.rotateangle = angle
        self.random_rotation: float = (angle / 100) * random_rotation_percentage
        self.random_linelenght: float = (
                                                linelenght / 100
                                        ) * random_linelenght_percentage
        self.commandsdict = {
            "F": self.forward,
            "B": self.backward,
            "L": self.left,
            "R": self.right,
            "V": self.moveforward,
            "N": self.movebackward,
            "S": self.drawsquare,
            "T": self.drawtriangle,
        }
        if self.commandsdict.keys() != commandskeys and len(self.commandsdict):
            commands = list(self.commandsdict.values())
            self.commandsdict.clear()
            for index, newkey in enumerate(commandskeys):
                self.commandsdict[newkey] = commands[index]

    def draw(self, string: tuple[tuple[str, int], ...], startpoint: QPointF | QPoint = None):
        if startpoint is not None:
            self.point = QPointF(startpoint)
        for command, quantity in string:
            if command in self.commandsdict:
                # noinspection PyArgumentList
                self.commandsdict[command](quantity)

    def forward(self, quantity: int):
        x = self.point.x()
        y = self.point.y()
        lenght = self.linelenght
        rlenght = self.random_linelenght
        for _ in range(quantity):
            if rlenght > 0:
                randomchange = triangular(-rlenght, rlenght, gauss(0, 1))
            else:
                randomchange = 0
            x += (lenght + randomchange) * cos(radians(self.turtleangle))
            y -= (lenght + randomchange) * sin(radians(self.turtleangle))
        end = QPointF(x, y)
        start_in_rect = (
                self.mdevice.width() > self.point.x() > 0
                and self.mdevice.height() > self.point.y() > 0
        )
        end_in_rect = (
                self.mdevice.width() > end.x() > 0 and self.mdevice.height() > end.y() > 0
        )
        if start_in_rect or end_in_rect:
            self.drawLine(self.point, end)
        self.point.setX(x)
        self.point.setY(y)

    def backward(self, quantity: int):
        x = self.point.x()
        y = self.point.y()
        lenght = self.linelenght
        rlenght = self.random_linelenght
        for _ in range(quantity):
            if rlenght > 0:
                randomchange = triangular(-rlenght, rlenght, gauss(0, 1))
            else:
                randomchange = 0
            x -= (lenght + randomchange) * cos(radians(self.turtleangle))
            y += (lenght + randomchange) * sin(radians(self.turtleangle))
        end = QPointF(x, y)
        start_in_rect = (
                self.mdevice.width() > self.point.x() > 0
                and self.mdevice.height() > self.point.y() > 0
        )
        end_in_rect = (
                self.mdevice.width() > end.x() > 0 and self.mdevice.height() > end.y() > 0
        )
        if start_in_rect or end_in_rect:
            self.drawLine(self.point, end)
        self.point.setX(x)
        self.point.setY(y)

    def right(self, quantity: int):
        angle = self.rotateangle
        rangle = self.random_rotation
        for _ in range(quantity):
            if rangle > 0:
                randomchange = triangular(-rangle, rangle, gauss(0, 1))
            else:
                randomchange = 0
            self.turtleangle -= angle + randomchange

    def left(self, quantity: int):
        angle = self.rotateangle
        rangle = self.random_rotation
        for _ in range(quantity):
            if rangle > 0:
                randomchange = triangular(-rangle, rangle, gauss(0, 1))
            else:
                randomchange = 0
            self.turtleangle += angle + randomchange

    def moveforward(self, quantity: int):
        x = self.point.x()
        y = self.point.y()
        lenght = self.travel_length
        for _ in range(quantity):
            x += lenght * cos(radians(self.turtleangle))
            y -= lenght * sin(radians(self.turtleangle))
        self.point.setX(x)
        self.point.setY(y)

    def movebackward(self, quantity: int):
        x = self.point.x()
        y = self.point.y()
        lenght = self.travel_length
        for _ in range(quantity):
            x -= lenght * cos(radians(self.turtleangle))
            y += lenght * sin(radians(self.turtleangle))
        self.point.setX(x)
        self.point.setY(y)

    def changepencolor(self, quantity: int = 1):
        for _ in range(quantity):
            self.colorindex += 1
        self.colorindex %= len(self.colors)
        self.setPen(self.colors[self.colorindex])

    def drawsquare(self, quantity: int):
        lenght = self.linelenght
        point1 = QPointF(self.point)
        point2 = QPointF(
                point1.x() + lenght * cos(radians(self.turtleangle)),
                point1.y() - lenght * sin(radians(self.turtleangle)),
        )
        point3 = QPointF(
                point2.x() + lenght * cos(radians(self.turtleangle + 90)),
                point2.y() - lenght * sin(radians(self.turtleangle + 90)),
        )
        point4 = QPointF(
                point3.x() + lenght * cos(radians(self.turtleangle + 180)),
                point3.y() - lenght * sin(radians(self.turtleangle + 180)),
        )
        for _ in range(quantity):
            self.drawPolygon((point1, point2, point3, point4))

    def drawtriangle(self, quantity: int):
        lenght = self.linelenght
        point1 = QPointF(self.point)
        point2 = QPointF(
                point1.x() + lenght * cos(radians(self.turtleangle)),
                point1.y() - lenght * sin(radians(self.turtleangle)),
        )
        point3 = QPointF(
                point2.x() + lenght * cos(radians(self.turtleangle + 120)),
                point2.y() - lenght * sin(radians(self.turtleangle + 120)),
        )
        for _ in range(quantity):
            self.drawPolygon((point1, point2, point3))

    def drawcircle(self, quantity: int):
        for _ in range(quantity):
            self.drawEllipse(self.point, self.linelenght // 2, self.linelenght // 2)


if __name__ == "__main__":
    pass
