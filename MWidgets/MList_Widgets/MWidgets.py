from typing import Optional

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import (
    QInputDialog,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QWidget,
)


class Modified_list(QListWidget):
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
        self.menu.addAction("Изменить", self.edit_current_item)
        self.menu.addAction("Вверх", self.raise_item)
        self.menu.addAction("Вниз", self.omit_item)
        self.menu.addAction("Удалить", self.take_current_item)
        self.menu.addAction("Очистить", self.clear)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)
    
    def show_menu(self, position: QPoint):
        self.menu.exec(self.mapToGlobal(position))
    
    def addItem(self, item: QListWidgetItem | str):
        super().addItem(item)
        self.setCurrentRow(self.count() - 1)
    
    def edit_current_item(self):
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
    
    def take_current_item(self) -> QListWidgetItem:
        return self.takeItem(self.currentRow())
    
    @property
    def functions(self) -> tuple:
        return (
            self.addItem,
            self.edit_current_item,
            self.raise_item,
            self.omit_item,
            self.take_current_item,
            self.clear,
        )
    
    def getitems(self) -> list[QListWidgetItem]:
        return [self.item(index) for index in range(self.count())]


class MText_list_widget(Modified_list):
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
    
    def edit_current_item(self):
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
