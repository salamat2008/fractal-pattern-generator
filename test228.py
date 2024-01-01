import sys
from typing import Callable, Iterable

import numpy as np
from PySide6.QtCore import QLineF, QPoint, QPointF
from PySide6.QtGui import QColor, QGradient, QPainter, QPixmap, Qt
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QDoubleSpinBox, QWidget

from Lsysems.Lsystem import *

class MTurtle:
    line_lenght: int | float = 10
    rotation: int | float = 0
    position = QPointF(0, 0)
    commands: dict[str, Callable] = {}
    rotate_angle: int | float = 0
    lines_array: np.array = np.array([])
    lines_array.resize(lines_array.size // 2, 2, 2)
    colors: Iterable = []
    selectedcolors: dict[str, list] = {
        "lines": [],
        "circles": [],
        "squares": [],
        "triangles": [],
    }
    selectedcolorindex: int = 0

    def __init__(self, commands: Iterable[Iterable[str]], colors: Iterable[QColor]):
        self.turtle_actions = (
            self.forward,
            self.backward,
            self.left,
            self.right,
            self.moveforward,
            self.movebackward,
            self.drawtriangle,
            self.drawsquare,
            self.drawcircle,
            self.changepencolor,
        )
        self.colors = colors
        for value, key in zip(self.turtle_actions, commands):
            self.commands[key[0]] = value

    def getlines(self, line_lenght: int | float, startpos: QPointF | QPoint) -> list[QLineF]:
        lines: np.array = np.array(self.lines_array)
        lines *= abs(line_lenght) / self.line_lenght
        lines += startpos.toTuple()
        lines.resize(lines.size // 4, 4)
        return [QLineF(*line) for line in lines]

    def drawfracture(self, patern: tuple[Coincidences, ...]):
        self.lines_array: np.array = np.array([])
        self.lines_array.resize(self.lines_array.size // 2, 2, 2)
        for command, quantity in patern:
            self.commands[command](quantity)
        self.position = QPointF(0, 0)
        self.rotation = 0

    def maxsize(self, line_lenght: int | float):
        if len(self.lines_array) > 0:
            maxwidth = abs(np.max(self.lines_array[:, :, 0])) + abs(
                np.min(self.lines_array[:, :, 0])
            )
            maxwidth *= abs(line_lenght) / self.line_lenght
            maxheith = abs(np.max(self.lines_array[:, :, 1])) + abs(
                np.min(self.lines_array[:, :, 1])
            )
            maxheith *= abs(line_lenght) / self.line_lenght
            return round(maxwidth + 3), round(maxheith + 4)
        return 1, 1

    def forward(self, quantity: int | float):
        line = QLineF(self.position, QPointF(100, 0))
        line.setAngle(self.rotation)
        line.setLength(self.line_lenght * quantity)
        self.position = QPointF(line.p2())
        line: np.array = np.array(line.toTuple())
        line.shape = (1, 2, 2)
        line = np.round(line, 4)
        self.lines_array = np.append(self.lines_array, line, axis=0)

    def backward(self, quantity: int | float):
        line = QLineF(self.position, QPointF(100, 0))
        line.setAngle(180 + self.rotation)
        line.setLength(self.line_lenght * quantity)
        self.position = QPointF(line.p2())
        line: np.array = np.array(line.toTuple())
        line.shape = (1, 2, 2)
        line = np.round(line, 4)
        self.lines_array = np.append(self.lines_array, line, axis=0)

    def right(self, quantity: int | float):
        self.rotation -= self.rotate_angle * quantity

    def left(self, quantity: int | float):
        self.rotation += self.rotate_angle * quantity

    def moveforward(self, quantity: int | float):
        line = QLineF(self.position, QPointF(100, 0))
        line.setAngle(self.rotation)
        line.setLength(self.line_lenght * quantity)
        self.position = QPointF(line.p2())

    def movebackward(self, quantity: int | float):
        line = QLineF(self.position, QPointF(100, 0))
        line.setAngle(180 + self.rotation)
        line.setLength(self.line_lenght * quantity)
        self.position = QPointF(line.p2())

    def changepencolor(self, factor: int):
        pass

    def drawsquare(self, factor: int):
        pass

    def drawtriangle(self, factor: int):
        pass

    def drawcircle(self, factor: int):
        pass


class Widget(QWidget):
    startpoint = QPointF(0, 0)
    pixmappos = QPointF(0, 0)
    sval: int = -10
    n_iter: int = 0
    lelt = -10

    def __init__(self, parent):
        super().__init__(parent)
        self.lsys = LSystem(
            {"F": "FLFRRFLF"},
            (
                ("F", "forward"),
                ("B", "back"),
                ("L", "left"),
                ("R", "right"),
                ("Mf", "mforward"),
                ("Mb", "mback"),
                ("T", 'triangle'),
                ("S", 'square'),
                ("E", 'circle'),
                ("C", 'change')
            ),
        )
        self.tut = MTurtle(
            self.lsys.keywords, [QColor("black"), QColor("pink"), QColor("blue")]
        )
        self.line_lenght: QDoubleSpinBox = QDoubleSpinBox(self)
        self.tut.rotate_angle = 60
        self.pixmap = QPixmap(100, 100)
        self.pixmap.fill(QColor(0, 0, 0, 0))
        self.setTabletTracking(True)
        #self.showFullScreen()

    def paintEvent(self, event):
        if self.n_iter != self.sval:
            self.sval = self.n_iter
            self.tut.drawfracture(self.lsys.generate_action_string("FLLFLLF", self.n_iter))
        if self.lelt != self.line_lenght.value() or self.n_iter != self.sval:
            self.lelt = self.line_lenght.value()
            self.pixmap = QPixmap(*self.tut.maxsize(self.line_lenght.value()))
            painter = QPainter(self.pixmap)
            painter.fillRect(self.pixmap.rect(), QColor("white"))
            painter.setRenderHint(painter.RenderHint.Antialiasing)
            pen1 = painter.pen()
            pen1.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            pen1.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen1.setStyle(Qt.PenStyle.SolidLine)
            pen1.setWidth(1)
            painter.setPen(pen1)
            pos = QPointF(
                self.pixmap.rect().bottomLeft().x() + painter.pen().width(),
                self.pixmap.rect().bottomLeft().y() - painter.pen().width(),
            )
            for line in self.tut.getlines(self.line_lenght.value(), pos):
                painter.drawLine(line)
            painter.drawRect(self.pixmap.rect())
            painter.end()
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("white"))
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        gradi = QGradient(QGradient.Preset.PhoenixStart)

        pen1 = painter.pen()
        pen1.setWidth(3)
        pen1.setColor(QColor(0,0,0,0))
        painter.setPen(pen1)
        painter.setBrush(gradi)
        painter.drawPixmap(self.pixmappos, self.pixmap)
        painter.end()
        super().paintEvent(event)

    def wheelEvent(self, event):
        val = event.angleDelta().y() / 1200
        if self.line_lenght.value() > 0 or val > 0:
            print(val)
            val += self.line_lenght.value()
            self.line_lenght.setValue(val)
            self.line_lenght.update()
        self.update()
        super().wheelEvent(event)

    def mousePressEvent(self, event):
        self.startpoint = self.mapToParent(event.position())
        self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        endpoint = event.position()
        rect = self.pixmap.rect().toRectF()
        rect.setX(self.pixmappos.x())
        rect.setY(self.pixmappos.y())
        endpoint = self.mapToParent(endpoint)
        self.pixmappos.setX(self.pixmappos.x() + endpoint.x() - self.startpoint.x())
        self.pixmappos.setY(self.pixmappos.y() + endpoint.y() - self.startpoint.y())
        self.startpoint = QPointF(endpoint)
        self.update()
        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    page = QWebEnginePage()
    page.setUrl('https://www.youtube.com')
    Web = QWebEngineView(page,window)
    Web.show()
    window.show()
    app.exec()
