import unittest

from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import QApplication, QListWidgetItem

from MWidgets.MList_Widgets.MColor_list_Widget import MColor_list_Widget, MColorDialog


class TestMColorDialog(unittest.TestCase):
    def setUp(self):
        try:
            QApplication()
        except RuntimeError:
            pass
    
    def test_get_color_positive(self):
        dialog = MColorDialog(QColor(Qt.GlobalColor.red))
        color, accepted = dialog.get_color()
        self.assertEqual(QColor(Qt.GlobalColor.red), color)
        self.assertTrue(accepted)


class TestMColor_list_widgetWidget(unittest.TestCase):
    def setUp(self):
        try:
            QApplication()
        except RuntimeError:
            pass
        self.widget = MColor_list_Widget()
    
    def test_edit_current_item_positive(self):
        item = QListWidgetItem()
        item.setData(self.widget.ColorRole, QColor(Qt.GlobalColor.red))
        self.widget.addItem(item)
        self.widget.edit_current_item()
        updated_item = self.widget.currentItem()
        self.assertEqual("#FF0000", updated_item.text())
        self.widget.clear()
    
    def test_edit_current_item_negative(self):
        self.widget.edit_current_item()
        self.assertIsNone(self.widget.currentItem())
    
    def test_add_color_with_color(self):
        self.widget.add_color(QColor(Qt.GlobalColor.red))
        item = self.widget.currentItem()
        self.assertIsNotNone(item)
        self.assertEqual("#FF0000", item.text())
        self.widget.clear()
    
    def test_add_color_with_none(self):
        self.widget.add_color()
        item = self.widget.currentItem()
        self.assertIsNotNone(item)
    
    def test_add_color_with_invalid_color(self):
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            self.widget.add_color("invalid color")
    
    def test_draw_icon_for_item(self):
        color = QColor('red')
        icon = self.widget.draw_icon_for_item(color)
        self.assertEqual(30, icon.height())
        self.assertEqual(30, icon.width())
    
    def test_get_colors(self):
        expected_colors = tuple(QColor(color) for color in QColor.colorNames()[:10])
        for color in expected_colors:
            self.widget.add_color(color)
        actual_colors = self.widget.get_colors()
        print(actual_colors)
        print(expected_colors)
        print(self.widget.count())
        self.assertTupleEqual(expected_colors, actual_colors)
    
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


if __name__ == '__main__':
    unittest.main()
