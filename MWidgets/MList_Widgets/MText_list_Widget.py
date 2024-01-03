from PySide6.QtWidgets import QInputDialog, QListWidgetItem, QWidget

from .Modified_list_widget import Modified_list_widget


class MText_list_widgetWidget(Modified_list_widget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
    
    def addItem(self, *args: QListWidgetItem | str):
        """
        If no arguments are passed, the self.add_text method is called
        :param args:
        :return: None
        """
        if len(args) == 0:
            self.add_text()
        else:
            super().addItem(*args)
    
    def add_text(self, text: str = None):
        """
        If the text parameter is None then QInputDialog is called,
        If the claim button is not pressed or the length of the entered text is zero
        Nothing is added
        otherwise, if the text is a string
        then it is added by the self.additem method
        and becomes current
        otherwise
        TypeError rises
        :raises TypeError:
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
            item_text, accepted = QInputDialog.getText(
                    self.parent(), "Изменение", "", text = item.text()
            )
            if len(item_text) > 0 and accepted:
                item.setText(item_text)
    
    def get_texts(self) -> tuple[str]:
        # noinspection PyTypeChecker
        return tuple(item.text() for item in self.getitems())
