import sys
from typing import Callable, Iterable

import numpy as np
from PySide6.QtCore import QLineF, QPoint, QPointF
from PySide6.QtGui import QColor, QGradient, QPainter, QPixmap, Qt
from PySide6.QtWidgets import QApplication, QDoubleSpinBox, QWidget

from Lsystems.Lsystem import LSystem


class MTurtle:
    line_length: int | float = 10
    rotation: int | float = 0
    position = QPointF(0, 0)
    commands: dict[str, Callable] = {}
    rotate_angle: int | float = 0
    lines_array: np.array = np.array([])
    lines_array.resize(lines_array.size // 2, 2, 2)
    colors: Iterable = []
    selected_colors: dict[str, list] = {
        "lines": [],
        "circles": [],
        "squares": [],
        "triangles": [],
    }
    selected_color_index: int = 0
    
    def __init__(self, commands: Iterable[Iterable[str]], colors: Iterable[QColor]):
        self.turtle_actions = (
            self.forward,
            self.backward,
            self.left,
            self.right,
            self.move_forward,
            self.move_backward,
            self.draw_triangle,
            self.draw_square,
            self.draw_circle,
            self.change_pencolor,
        )
        self.colors = colors
        for value, key in zip(self.turtle_actions, commands):
            self.commands[key[0]] = value
    
    def getlines(self, line_length: int | float, start_pos: QPointF | QPoint) -> list[QLineF]:
        lines: np.array = np.array(self.lines_array)
        lines *= abs(line_length) / self.line_length
        lines += start_pos.toTuple()
        lines.resize(lines.size // 4, 4)
        return [QLineF(*line) for line in lines]
    
    def draw_fracture(self, pattern: tuple[tuple[str, int], ...]):
        self.lines_array: np.array = np.array([])
        self.lines_array.resize(self.lines_array.size // 2, 2, 2)
        for command, quantity in pattern:
            self.commands[command](quantity)
        self.position = QPointF(0, 0)
        self.rotation = 0
    
    def maxsize(self, line_length: int | float):
        if len(self.lines_array) > 0:
            max_width = abs(
                    np.max(self.lines_array[:, :, 0])
            ) + abs(
                    np.min(self.lines_array[:, :, 0])
            )
            max_width *= abs(line_length) / self.line_length
            max_height = abs(
                    np.max(self.lines_array[:, :, 1])
            ) + abs(
                    np.min(self.lines_array[:, :, 1])
            )
            max_height *= abs(line_length) / self.line_length
            return round(max_width + 3), round(max_height + 3)
        return 1, 1
    
    def forward(self, quantity: int | float):
        line = QLineF(self.position, QPointF(100, 0))
        line.setAngle(self.rotation)
        line.setLength(self.line_length * quantity)
        self.position = QPointF(line.p2())
        line: np.array = np.array(line.toTuple())
        line.shape = (1, 2, 2)
        line = np.round(line, 4)
        self.lines_array = np.append(self.lines_array, line, axis = 0)
    
    def backward(self, quantity: int | float):
        line = QLineF(self.position, QPointF(100, 0))
        line.setAngle(180 + self.rotation)
        line.setLength(self.line_length * quantity)
        self.position = QPointF(line.p2())
        line: np.array = np.array(line.toTuple())
        line.shape = (1, 2, 2)
        line = np.round(line, 4)
        self.lines_array = np.append(self.lines_array, line, axis = 0)
    
    def right(self, quantity: int | float):
        self.rotation -= self.rotate_angle * quantity
    
    def left(self, quantity: int | float):
        self.rotation += self.rotate_angle * quantity
    
    def move_forward(self, quantity: int | float):
        line = QLineF(self.position, QPointF(100, 0))
        line.setAngle(self.rotation)
        line.setLength(self.line_length * quantity)
        self.position = QPointF(line.p2())
    
    def move_backward(self, quantity: int | float):
        line = QLineF(self.position, QPointF(100, 0))
        line.setAngle(180 + self.rotation)
        line.setLength(self.line_length * quantity)
        self.position = QPointF(line.p2())
    
    def change_pencolor(self, factor: int):
        pass
    
    def draw_square(self, factor: int):
        pass
    
    def draw_triangle(self, factor: int):
        pass
    
    def draw_circle(self, factor: int):
        pass


class Widget(QWidget):
    startpoint = QPointF(0, 0)
    pixmap_pos = QPointF(0, 0)
    sval: int = -10
    n_iter: int = 0
    line_lenght_value = -10
    
    def __init__(self, parent = None):
        super().__init__(parent)
        # noinspection SpellCheckingInspection
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
            # noinspection SpellCheckingInspection
            self.tut.draw_fracture(self.lsys.generate_action_string("FLLFLLF", self.n_iter))
        if self.line_lenght_value != self.line_lenght.value() or self.n_iter != self.sval:
            self.line_lenght_value = self.line_lenght.value()
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
        gradient = QGradient(QGradient.Preset.PhoenixStart)
        
        pen1 = painter.pen()
        pen1.setWidth(3)
        pen1.setColor(QColor(0, 0, 0, 0))
        painter.setPen(pen1)
        painter.setBrush(gradient)
        painter.drawPixmap(self.pixmap_pos, self.pixmap)
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
        rect.setX(self.pixmap_pos.x())
        rect.setY(self.pixmap_pos.y())
        endpoint = self.mapToParent(endpoint)
        self.pixmap_pos.setX(self.pixmap_pos.x() + endpoint.x() - self.startpoint.x())
        self.pixmap_pos.setY(self.pixmap_pos.y() + endpoint.y() - self.startpoint.y())
        self.startpoint = QPointF(endpoint)
        self.update()
        super().mouseMoveEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Widget()
    win.show()
    app.exec()
