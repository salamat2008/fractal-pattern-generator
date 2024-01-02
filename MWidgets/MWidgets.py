from typing import Optional

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap, QRgba64
from PySide6.QtWidgets import (
    QColorDialog,
    QInputDialog,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QWidget,
)


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



