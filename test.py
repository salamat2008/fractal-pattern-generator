import sys
import unittest
import uuid

from PySide6.QtWidgets import QApplication

from MWidgets import MColorlistwidget, MTextlistwidget, QColor

app = QApplication(sys.argv)


class TestMTextlistwidget(unittest.TestCase):
    widget = MTextlistwidget()
    textlist = [str(uuid.uuid4()) for _ in range(100)]

    def testaddtext(self):
        for text in self.textlist:
            self.assertIsNone(self.widget.addtext(text))
        self.assertListEqual(self.widget.gettextlist(), self.textlist)
        self.assertIsNone(self.widget.clear())

    def testtakecurrentitem(self):
        for text in self.textlist:
            self.assertIsNone(self.widget.addtext(text))
        for text in self.textlist[:len(self.textlist) // 2]:
            self.assertEqual(self.widget.takecurrentitem().text(), text)
        self.assertListEqual(self.widget.gettextlist(), self.textlist[len(self.textlist) // 2:])


class TestMColorlistwidget(unittest.TestCase):
    widget = MColorlistwidget()
    colorlist = QColor.colorNames()

    def testaddcolor(self):
        for color in self.colorlist:
            self.assertIsNone(self.widget.addcolor(QColor(color)))
        self.assertListEqual(self.widget.getcolorlist(), self.colorlist)
        self.assertIsNone(self.widget.clear())

    def testtakecurrentitem(self):
        for color in self.colorlist:
            self.assertIsNone(self.widget.addItem(QColor(color)))
        for color in self.colorlist[:len(self.colorlist) // 2]:
            self.assertEqual(self.widget.takecurrentitem().text(),f'#{hex(QColor(color).rgb()).upper()[4:]}')
        self.assertListEqual(self.widget.getcolorlist(), self.colorlist[len(self.colorlist) // 2:])


if __name__ == '__main__':
    unittest.main()
