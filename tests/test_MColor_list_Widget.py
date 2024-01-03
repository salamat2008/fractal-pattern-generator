import unittest

from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import QListWidgetItem

from MWidgets.MList_Widgets.MColor_list_Widget import MColor_list_widgetWidget, MColorDialog


class MColorDialogTest(unittest.TestCase):
    def test_get_color_positive(self):
        dialog = MColorDialog(QColor(Qt.GlobalColor.red))
        color, accepted = dialog.get_color()
        self.assertEqual(color, QColor(Qt.GlobalColor.red))
        self.assertTrue(accepted)
    
    def test_get_color_negative(self):
        dialog = MColorDialog()
        color, accepted = dialog.get_color()
        self.assertIsNotNone(color)
        self.assertIsNotNone(accepted)


# noinspection PyTypeChecker
class MColor_list_widgetWidgetTest(unittest.TestCase):
    def test_edit_current_item_positive(self):
        widget = MColor_list_widgetWidget()
        item = QListWidgetItem()
        item.setData(widget.ColorRole, QColor(Qt.GlobalColor.red))
        widget.addItem(item)
        widget.setCurrentRow(0)
        
        widget.edit_current_item()
        
        updated_item = widget.item(0)
        self.assertEqual(updated_item.text(), "#FF0000")
    
    def test_edit_current_item_negative(self):
        widget = MColor_list_widgetWidget()
        widget.setCurrentRow(0)
        
        widget.edit_current_item()
        
        self.assertIsNone(widget.item(0))
    
    def test_add_color_with_color(self):
        widget = MColor_list_widgetWidget()
        widget.add_color(QColor(Qt.GlobalColor.red))
        
        item = widget.item(0)
        self.assertIsNotNone(item)
        self.assertEqual(item.text(), "#FF0000")
    
    def test_add_color_with_none(self):
        widget = MColor_list_widgetWidget()
        widget.add_color()
        
        item = widget.item(0)
        self.assertIsNotNone(item)
    
    def test_add_color_with_invalid_color(self):
        widget = MColor_list_widgetWidget()
        with self.assertRaises(TypeError):
            widget.add_color("invalid color")
    
    def test_draw_icon_for_item(self):
        widget = MColor_list_widgetWidget()
        color = QColor(Qt.GlobalColor.red)
        
        icon = widget.draw_icon_for_item(color)
        icon = icon.pixmap(30, mode = icon.Mode.Normal, state = icon.State.On)
        self.assertEqual(icon.height(), 30)
        self.assertEqual(icon.width(), 30)
    
    def test_get_colors(self):
        widget = MColor_list_widgetWidget()
        widget.add_color(QColor(Qt.GlobalColor.red))
        widget.add_color(QColor(Qt.GlobalColor.green))
        widget.add_color(QColor(Qt.GlobalColor.blue))
        
        color_list = widget.get_colors()
        
        self.assertEqual(len(color_list), 3)
        self.assertIsInstance(color_list[0], QColor)
        self.assertEqual(color_list[0], QColor(Qt.GlobalColor.red))
    
    def test_getitems(self):
        widget = MColor_list_widgetWidget()
        widget.add_color(QColor(Qt.GlobalColor.red))
        widget.add_color(QColor(Qt.GlobalColor.green))
        widget.add_color(QColor(Qt.GlobalColor.blue))
        
        items = widget.getitems()
        
        self.assertEqual(len(items), 3)
        self.assertIsInstance(items[0], QListWidgetItem)
        self.assertEqual(items[0].data(widget.ColorRole), QColor(Qt.GlobalColor.red))


if __name__ == '__main__':
    unittest.main()
