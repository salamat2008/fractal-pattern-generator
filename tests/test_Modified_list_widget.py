import unittest

from PySide6.QtWidgets import QApplication, QListWidgetItem

from MWidgets.MList_Widgets.Modified_list_widget import Modified_list_widget


class TestModifiedListWidget(unittest.TestCase):
    
    def setUp(self):
        try:
            QApplication()
        except RuntimeError:
            pass
        self.widget = Modified_list_widget()
    
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
    
    def test_getitems(self):
        expected_items = ('item1', 'item2', 'item3')
        self.widget.addItems(expected_items)
        items = self.widget.getitems()
        for item in items:
            self.assertIsInstance(item, QListWidgetItem)
        self.assertTupleEqual(expected_items, tuple(item.text() for item in items))


if __name__ == '__main__':
    unittest.main()
