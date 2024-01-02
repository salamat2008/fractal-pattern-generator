from typing import Optional

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMenu,
    QWidget,
)


class Modified_list_widget(QListWidget):
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
