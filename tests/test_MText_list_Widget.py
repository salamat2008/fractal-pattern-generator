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
        self.widget = MText_list_Widget()
    
    @mock.patch.object(QInputDialog, "getText")
    def test_addItem_with_no_arguments(self, mock_gettext: mock.MagicMock):
        mock_gettext.return_value = ('Some item', True)
        self.widget.addItem()
        self.assertEqual(1, self.widget.count())
        item_text = self.widget.currentItem().text()
        self.assertEqual("Some item", item_text)
    
    def test_addItem_with_string_argument(self):
        self.widget.addItem("Item 1")
        self.assertEqual(1, self.widget.count())
        item_text = self.widget.currentItem().text()
        self.assertEqual("Item 1", item_text)
    
    def test_addItem_with_listwidgetitem_argument(self):
        item = QListWidgetItem("Item 1")
        self.widget.addItem(item)
        self.assertEqual(1, self.widget.count())
        item_text = self.widget.currentItem().text()
        self.assertEqual("Item 1", item_text)
    
    def test_add_text_with_valid_text(self):
        self.widget.add_text("Item 1")
        self.assertEqual(1, self.widget.count())
        item_text = self.widget.currentItem().text()
        self.assertEqual("Item 1", item_text)
    
    def test_add_text_with_empty_text(self):
        self.widget.add_text("")
        self.assertEqual(1, self.widget.count())
    
    @mock.patch.object(QInputDialog, "getText")
    def test_add_text_with_no_text(self, mock_gettext: mock.MagicMock):
        mock_gettext.return_value = ("Some item", True)
        self.widget.add_text()
        self.assertEqual(1, self.widget.count())
        item_text = self.widget.currentItem().text()
        self.assertEqual("Some item", item_text)
    
    def test_add_text_with_invalid_argument(self):
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            self.widget.add_text(123)
    
    @mock.patch.object(QInputDialog, "getText")
    def test_edit_current_item_with_valid_text(self, mock_gettext: mock.MagicMock):
        mock_gettext.return_value = ("Edited item", True)
        self.widget.addItem("Item 1")
        self.widget.edit_current_item()
        self.assertEqual("Edited item", self.widget.currentItem().text())
    
    def test_get_texts(self):
        self.widget.addItem("Item 1")
        self.widget.addItem("Item 2")
        texts = self.widget.get_texts()
        self.assertEqual(2, len(texts))
        self.assertEqual("Item 1", texts[0])
        self.assertEqual("Item 2", texts[1])
    
    def test_addItem_positive(self):
        self.widget.addItem("test")
        self.assertEqual(1, self.widget.count())
        self.assertEqual(self.widget.item(0).text(), "test")
    
    def test_raise_item_positive(self):
        self.widget.addItem("item1")
        self.widget.addItem("item2")
        self.widget.setCurrentRow(1)
        self.widget.raise_item()
        self.assertEqual(0, self.widget.currentRow())
        self.assertEqual(self.widget.item(0).text(), "item2")
        self.assertEqual(self.widget.item(1).text(), "item1")
    
    def test_raise_item_negative(self):
        self.widget.raise_item()
        self.assertEqual(0, self.widget.count())
    
    def test_omit_item_positive(self):
        self.widget.addItem("item1")
        self.widget.addItem("item2")
        self.widget.setCurrentRow(0)
        self.widget.omit_item()
        self.assertEqual(1, self.widget.currentRow())
        self.assertEqual(self.widget.item(0).text(), "item2")
        self.assertEqual(self.widget.item(1).text(), "item1")
    
    def test_omit_item_negative(self):
        self.widget.omit_item()
        self.assertEqual(0, self.widget.count())
    
    def test_take_current_item_positive(self):
        self.widget.addItem("test")
        item = self.widget.take_current_item()
        self.assertEqual(item.text(), "test")
        self.assertEqual(0, self.widget.count())
    
    def test_take_current_item_negative(self):
        item = self.widget.take_current_item()
        self.assertIsNone(item)
    
    def test_clear(self):
        self.widget.addItem("test")
        self.widget.clear()
        self.assertEqual(0, self.widget.count())


if __name__ == "__main__":
    unittest.main()
