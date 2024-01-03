import unittest
from unittest import mock

from PySide6.QtWidgets import QInputDialog, QListWidgetItem

from MWidgets.MList_Widgets.MText_list_Widget import MText_list_Widget


class MText_list_WidgetTests(unittest.TestCase):
    def test_addItem_with_no_arguments(self):
        widget = MText_list_Widget()
        widget.addItem()
        self.assertEqual(widget.count(), 1)
        item_text = widget.item(0).text()
        self.assertEqual(item_text, "")
    
    def test_addItem_with_string_argument(self):
        widget = MText_list_Widget()
        widget.addItem("Item 1")
        self.assertEqual(widget.count(), 1)
        item_text = widget.item(0).text()
        self.assertEqual(item_text, "Item 1")
    
    def test_addItem_with_listwidgetitem_argument(self):
        widget = MText_list_Widget()
        item = QListWidgetItem("Item 1")
        widget.addItem(item)
        self.assertEqual(widget.count(), 1)
        item_text = widget.item(0).text()
        self.assertEqual(item_text, "Item 1")
    
    def test_add_text_with_valid_text(self):
        widget = MText_list_Widget()
        widget.add_text("Item 1")
        self.assertEqual(widget.count(), 1)
        item_text = widget.item(0).text()
        self.assertEqual(item_text, "Item 1")
    
    def test_add_text_with_empty_text(self):
        widget = MText_list_Widget()
        widget.add_text("")
        self.assertEqual(widget.count(), 1)
    
    def test_add_text_with_no_text(self):
        widget = MText_list_Widget()
        widget.add_text()
        self.assertEqual(widget.count(), 1)
        item_text = widget.item(0).text()
        self.assertEqual(item_text, "")
    
    def test_add_text_with_invalid_argument(self):
        widget = MText_list_Widget()
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            widget.add_text(123)
    
    def test_edit_current_item_with_valid_text(self):
        widget = MText_list_Widget()
        item = QListWidgetItem("Item 1")
        widget.addItem(item)
        widget.setCurrentItem(item)
        with mock.patch.object(QInputDialog, "getText", return_value = ("Item 2", True)):
            widget.edit_current_item()
            self.assertEqual(widget.count(), 1)
            item_text = widget.item(0).text()
            self.assertEqual(item_text, "Item 2")
    
    def test_edit_current_item_with_empty_text(self):
        widget = MText_list_Widget()
        item = QListWidgetItem("Item 1")
        widget.addItem(item)
        widget.setCurrentItem(item)
        with mock.patch.object(QInputDialog, "getText", return_value = ("Item 1", True)):
            widget.edit_current_item()
            self.assertEqual(widget.count(), 1)
            item_text = widget.item(0).text()
            self.assertEqual(item_text, "Item 1")
    
    def test_edit_current_item_with_no_current_item(self):
        widget = MText_list_Widget()
        with mock.patch.object(QInputDialog, "getText"):
            widget.edit_current_item()
    
    def test_get_texts(self):
        widget = MText_list_Widget()
        widget.addItem("Item 1")
        widget.addItem("Item 2")
        texts = widget.get_texts()
        self.assertEqual(len(texts), 2)
        self.assertEqual(texts[0], "Item 1")
        self.assertEqual(texts[1], "Item 2")


if __name__ == "__main__":
    unittest.main()
