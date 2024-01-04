from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMenu,
    QWidget,
)


class Modified_list_widget(QListWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setDragDropMode(self.DragDropMode.InternalMove)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)
    
    @Slot(QPoint)
    def show_menu(self, position: QPoint):
        menu = QMenu(self)
        menu.addAction("Добавить", self.addItem)
        menu.addAction("Изменить", self.edit_current_item)
        menu.addAction("Вверх", self.raise_item)
        menu.addAction("Вниз", self.omit_item)
        menu.addAction("Удалить", self.take_current_item)
        menu.addAction("Очистить", self.clear)
        menu.exec(self.mapToGlobal(position))
    
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
    
    def getitems(self) -> tuple[QListWidgetItem, ...]:
        return tuple(self.item(index) for index in range(self.count()))
    
    def __repr__(self):
        return f'{self.__class__.__name__}{tuple(item.text() for item in self.getitems())}'
