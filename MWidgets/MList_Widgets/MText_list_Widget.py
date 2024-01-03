from PySide6.QtWidgets import QInputDialog, QListWidgetItem, QWidget

from .Modified_list_widget import Modified_list_widget


class MText_list_Widget(Modified_list_widget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
    
    def addItem(self, item: QListWidgetItem | str | None = None, ):
        """
        :param item: QListWidgetItem | str | None = None
        
        :return: None
        """
        if item is None:
            self.add_text()
        else:
            super().addItem(item)
    
    def add_text(self, text: str | None = None, user_input_text: str = ''):
        """
        :param user_input_text:
        :param text:
        :return: None
        :raises TypeError:
        """
        if not isinstance(user_input_text, str):
            raise TypeError("The text must be a string")
        if isinstance(text, str):
            accepted = True
        elif text is None:
            text, accepted = QInputDialog.getText(self.parent(), "Добавление", "", text = user_input_text)
        else:
            raise TypeError("The text must be a string")
        if accepted:
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
            if accepted:
                item.setText(item_text)
    
    def get_texts(self) -> tuple[str]:
        # noinspection PyTypeChecker
        return tuple(item.text() for item in self.getitems())
