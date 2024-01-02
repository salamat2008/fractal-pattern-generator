import unittest

from PySide6.QtGui import QColor, Qt
from PySide6.QtWidgets import QListWidgetItem

from MWidgets.MList_Widgets.MColor_list_Widget import MColor_list_widgetWidget, MColorDialog


class MColorDialogTest(unittest.TestCase):
    def test_getcolor_positive(self):
        dialog = MColorDialog(QColor(Qt.GlobalColor.red))
        color, accepted = dialog.getcolor()
        self.assertEqual(color, QColor(Qt.GlobalColor.red))
        self.assertTrue(accepted)
    
    def test_getcolor_negative(self):
        dialog = MColorDialog()
        color, accepted = dialog.getcolor()
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
    
    def test_addcolor_with_color(self):
        widget = MColor_list_widgetWidget()
        widget.addcolor(QColor(Qt.GlobalColor.red))
        
        item = widget.item(0)
        self.assertIsNotNone(item)
        self.assertEqual(item.text(), "#FF0000")
    
    def test_addcolor_with_none(self):
        widget = MColor_list_widgetWidget()
        widget.addcolor()
        
        item = widget.item(0)
        self.assertIsNotNone(item)
    
    def test_addcolor_with_invalid_color(self):
        widget = MColor_list_widgetWidget()
        with self.assertRaises(TypeError):
            widget.addcolor("invalid color")
    
    def test_drawiconforitem(self):
        widget = MColor_list_widgetWidget()
        color = QColor(Qt.GlobalColor.red)
        
        icon = widget.drawiconforitem(color)
        
        self.assertEqual(icon.width(), 30)
        self.assertEqual(icon.height(), 30)
    
    def test_getcolorlist(self):
        widget = MColor_list_widgetWidget()
        widget.addcolor(QColor(Qt.GlobalColor.red))
        widget.addcolor(QColor(Qt.GlobalColor.green))
        widget.addcolor(QColor(Qt.GlobalColor.blue))
        
        color_list = widget.getcolorlist()
        
        self.assertEqual(len(color_list), 3)
        self.assertIsInstance(color_list[0], QColor)
        self.assertEqual(color_list[0], QColor(Qt.GlobalColor.red))
    
    def test_getitems(self):
        widget = MColor_list_widgetWidget()
        widget.addcolor(QColor(Qt.GlobalColor.red))
        widget.addcolor(QColor(Qt.GlobalColor.green))
        widget.addcolor(QColor(Qt.GlobalColor.blue))
        
        items = widget.getitems()
        
        self.assertEqual(len(items), 3)
        self.assertIsInstance(items[0], QListWidgetItem)
        self.assertEqual(items[0].data(widget.ColorRole), QColor(Qt.GlobalColor.red))


if __name__ == '__main__':
    unittest.main()
