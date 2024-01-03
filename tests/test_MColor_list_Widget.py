import unittest

from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import QApplication, QListWidgetItem

from MWidgets.MList_Widgets.MColor_list_Widget import MColor_list_widgetWidget, MColorDialog


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
    
    def test_edit_current_item_positive(self):
        widget = MColor_list_widgetWidget()
        item = QListWidgetItem()
        item.setData(widget.ColorRole, QColor(Qt.GlobalColor.red))
        widget.addItem(item)
        widget.edit_current_item()
        updated_item = widget.currentItem()
        self.assertEqual("#FF0000", updated_item.text())
    
    def test_edit_current_item_negative(self):
        widget = MColor_list_widgetWidget()
        widget.edit_current_item()
        self.assertIsNone(widget.currentItem())
    
    def test_add_color_with_color(self):
        widget = MColor_list_widgetWidget()
        widget.add_color(QColor(Qt.GlobalColor.red))
        item = widget.currentItem()
        self.assertIsNotNone(item)
        self.assertEqual("#FF0000", item.text())
    
    def test_add_color_with_none(self):
        widget = MColor_list_widgetWidget()
        widget.add_color()
        item = widget.currentItem()
        self.assertIsNotNone(item)
    
    def test_add_color_with_invalid_color(self):
        widget = MColor_list_widgetWidget()
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            widget.add_color("invalid color")
    
    def test_draw_icon_for_item(self):
        widget = MColor_list_widgetWidget()
        color = QColor(Qt.GlobalColor.red)
        icon = widget.draw_icon_for_item(color)
        icon = icon.pixmap(30, mode = icon.Mode.Normal, state = icon.State.On)
        self.assertEqual(30, icon.height())
        self.assertEqual(30, icon.width())
    
    def test_get_colors(self):
        widget = MColor_list_widgetWidget()
        expected_number_of_colors = 5
        expected_colors = tuple(QColor(color) for color in QColor.colorNames()[:expected_number_of_colors])
        for color in expected_colors:
            widget.add_color(color)
        actual_colors = widget.get_colors()
        self.assertEqual(expected_number_of_colors, len(actual_colors))
        self.assertTupleEqual(expected_colors, actual_colors)
    
    def test_getitems(self):
        widget = MColor_list_widgetWidget()
        expected_number_of_colors = 5
        expected_colors = tuple(QColor(color) for color in QColor.colorNames()[:expected_number_of_colors])
        for color in expected_colors:
            widget.add_color(color)
        items = widget.getitems()
        self.assertEqual(expected_number_of_colors, len(items))
        for item in items:
            self.assertIsInstance(item, QListWidgetItem)
        self.assertTupleEqual(expected_colors, tuple(item.data(widget.ColorRole) for item in items))


if __name__ == '__main__':
    unittest.main()
