from sys import argv

from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap, QRgba64, Qt
from PySide6.QtWidgets import QApplication, QColorDialog

from .Modified_list_widget import Modified_list_widget, QListWidgetItem, QWidget

QApplication(argv)

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


class MColor_list_widgetWidget(Modified_list_widget):
    ColorRole = Qt.ItemDataRole.UserRole + 1
    
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.icon = QPixmap(30, 30)
        self.icon.fill(QColor(0, 0, 0, 0))
    
    def edit_current_item(self):
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
        The color is stored in the MColor_list_widgetWidget.ColorRole
        following Qt.ItemDataRole.UserRole as a QColor object
        :return: list[QListWidgetItem]
        """
        return super().getitems()
