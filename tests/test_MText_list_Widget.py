import unittest
from unittest import mock

from PySide6.QtWidgets import QApplication, QInputDialog, QListWidgetItem

from MWidgets.MList_Widgets.MText_list_Widget import MText_list_Widget


class MText_list_WidgetTests(unittest.TestCase):
    def setUp(self):
        try:
            QApplication()
        except RuntimeError:
            pass
    
    @mock.patch.object(QInputDialog, "getText")
    def test_addItem_with_no_arguments(self, mock_gettext: mock.MagicMock):
        mock_gettext.return_value = ('Some item', True)
        widget = MText_list_Widget()
        widget.addItem()
        self.assertEqual(1, widget.count())
        item_text = widget.currentItem().text()
        self.assertEqual("Some item", item_text)
    
    def test_addItem_with_string_argument(self):
        widget = MText_list_Widget()
        widget.addItem("Item 1")
        self.assertEqual(1, widget.count())
        item_text = widget.currentItem().text()
        self.assertEqual("Item 1", item_text)
    
    def test_addItem_with_listwidgetitem_argument(self):
        widget = MText_list_Widget()
        item = QListWidgetItem("Item 1")
        widget.addItem(item)
        self.assertEqual(1, widget.count())
        item_text = widget.currentItem().text()
        self.assertEqual("Item 1", item_text)
    
    def test_add_text_with_valid_text(self):
        widget = MText_list_Widget()
        widget.add_text("Item 1")
        self.assertEqual(1, widget.count())
        item_text = widget.currentItem().text()
        self.assertEqual("Item 1", item_text)
    
    def test_add_text_with_empty_text(self):
        widget = MText_list_Widget()
        widget.add_text("")
        self.assertEqual(1, widget.count())
    
    @mock.patch.object(QInputDialog, "getText")
    def test_add_text_with_no_text(self, mock_gettext: mock.MagicMock):
        mock_gettext.return_value = ("Some item", True)
        widget = MText_list_Widget()
        widget.add_text()
        self.assertEqual(1, widget.count())
        item_text = widget.currentItem().text()
        self.assertEqual("Some item", item_text)
    
    def test_add_text_with_invalid_argument(self):
        widget = MText_list_Widget()
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            widget.add_text(123)
    
    @mock.patch.object(QInputDialog, "getText")
    def test_edit_current_item_with_valid_text(self, mock_gettext: mock.MagicMock):
        mock_gettext.return_value = ("Edited item", True)
        widget = MText_list_Widget()
        widget.addItem("Item 1")
        widget.edit_current_item()
        self.assertEqual("Edited item", widget.currentItem().text())
    
    def test_get_texts(self):
        widget = MText_list_Widget()
        widget.addItem("Item 1")
        widget.addItem("Item 2")
        texts = widget.get_texts()
        self.assertEqual(2, len(texts))
        self.assertEqual("Item 1", texts[0])
        self.assertEqual("Item 2", texts[1])


if __name__ == "__main__":
    unittest.main()
