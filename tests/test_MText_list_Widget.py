import unittest
from unittest import mock

from PySide6.QtWidgets import QInputDialog, QListWidgetItem

from MWidgets.MList_Widgets.MText_list_Widget import MText_list_Widget


class MText_list_WidgetTests(unittest.TestCase):
    def test_addItem_with_no_arguments(self):
        widget = MText_list_Widget()
        widget.addItem()
        self.assertEqual(1, widget.count())  # Assert that the count is equal to 1
        item_text = widget.item(0).text()
        self.assertEqual("", item_text)  # Assert that the item text is an empty string
    
    def test_addItem_with_string_argument(self):
        widget = MText_list_Widget()
        widget.addItem("Item 1")
        self.assertEqual(1, widget.count())  # Assert that the count is equal to 1
        item_text = widget.item(0).text()
        self.assertEqual("Item 1", item_text)  # Assert that the item text is "Item 1"
    
    def test_addItem_with_listwidgetitem_argument(self):
        widget = MText_list_Widget()
        item = QListWidgetItem("Item 1")
        widget.addItem(item)
        self.assertEqual(1, widget.count())  # Assert that the count is equal to 1
        item_text = widget.item(0).text()
        self.assertEqual("Item 1", item_text)  # Assert that the item text is "Item 1"
    
    def test_add_text_with_valid_text(self):
        widget = MText_list_Widget()
        widget.add_text("Item 1")
        self.assertEqual(1, widget.count())  # Assert that the count is equal to 1
        item_text = widget.item(0).text()
        self.assertEqual("Item 1", item_text)  # Assert that the item text is "Item 1"
    
    def test_add_text_with_empty_text(self):
        widget = MText_list_Widget()
        widget.add_text("")
        self.assertEqual(1, widget.count())  # Assert that the count is equal to 1
    
    def test_add_text_with_no_text(self):
        widget = MText_list_Widget()
        widget.add_text()
        self.assertEqual(1, widget.count())  # Assert that the count is equal to 1
        item_text = widget.item(0).text()
        self.assertEqual("", item_text)  # Assert that the item text is an empty string
    
    def test_add_text_with_invalid_argument(self):
        widget = MText_list_Widget()
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            widget.add_text(123)
    
    @mock.patch.object(QInputDialog, "getText", return_value = ("Item 2", True))
    def test_edit_current_item_with_valid_text(self):
        widget = MText_list_Widget()
        item = QListWidgetItem("Item 1")
        widget.addItem(item)
        widget.setCurrentItem(item)
        widget.edit_current_item()
        self.assertEqual(1, widget.count())  # Assert that the count is equal to 1
        item_text = widget.item(0).text()
        self.assertEqual("Item 2", item_text)  # Assert that the item text is "Item 2"
    
    @mock.patch.object(QInputDialog, "getText", return_value = ("Item 1", True))
    def test_edit_current_item_with_empty_text(self, mock_gettext):
        widget = MText_list_Widget()
        item = QListWidgetItem("Item 1")
        widget.addItem(item)
        widget.setCurrentItem(item)
        widget.edit_current_item()
        self.assertEqual(1, widget.count())  # Assert that the count is equal to 1
        item_text = widget.item(0).text()
        self.assertEqual("Item 1", item_text)  # Assert that the item text is "Item 1"
    
    @mock.patch.object(QInputDialog, "getText", new_callable = print)
    @staticmethod
    def test_edit_current_item_with_no_current_item():
        widget = MText_list_Widget()
        widget.edit_current_item()
    
    def test_get_texts(self):
        widget = MText_list_Widget()
        widget.addItem("Item 1")
        widget.addItem("Item 2")
        texts = widget.get_texts()
        self.assertEqual(2, len(texts))  # Assert that the length of texts is equal to 2
        self.assertEqual("Item 1", texts[0])  # Assert that the first item in texts is "Item 1"
        self.assertEqual("Item 2", texts[1])  # Assert that the second item in texts is "Item 2"


if __name__ == "__main__":
    unittest.main()
