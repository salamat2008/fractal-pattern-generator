from math import radians, cos, sin

from PyQt5.QtCore import QRectF, QPointF, Qt
from PyQt5.QtGui import QPen, QBrush, QPolygonF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene


class View(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setSceneRect(QRectF(self.viewport().rect()))
        self.mypoynt1 = QPointF(0, 0)
        self.mypoynt2 = QPointF(0, 0)
        self.start_point = QPointF(0, 0)
        self.lrotate, self.j = 0, 1
        self.pen = QPen()
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.done = True
        self.clr_list = None

    def mousePressEvent(self, event):
        if event.button() == 1 and self.done:
            self.mypoynt1 = self.mapToScene(event.pos())
            self.mypoynt2 = self.mapToScene(event.pos())
            self.start_point = self.mapToScene(event.pos())

    def set_start(self):
        self.start_point.setX(self.mypoynt1.x())
        self.start_point.setY(self.mypoynt1.y())

    def go_to_start(self):
        self.mypoynt1.setX(self.start_point.x())
        self.mypoynt1.setY(self.start_point.y())

    def vforward(self, lenght):
        x = self.mypoynt1.x() + lenght * cos(radians(self.lrotate))
        y = self.mypoynt1.y() - lenght * sin(radians(self.lrotate))
        self.mypoynt1.setX(x)
        self.mypoynt1.setY(y)

    def vback(self, lenght):
        x1 = self.mypoynt1.x() - lenght * cos(radians(self.lrotate))
        y1 = self.mypoynt1.y() + lenght * sin(radians(self.lrotate))
        self.mypoynt1.setX(x1)
        self.mypoynt1.setY(y1)

    def rreset(self):
        self.lrotate = 0
        self.scene().clear()
        self.j = 1
        if self.clr_list is not None:
            self.pen.setColor(self.clr_list.item(0).data(3))
        t = round(self.mypoynt1.x()) != round(self.mypoynt2.x()) or round(self.mypoynt1.y()) != round(
            self.mypoynt2.y())
        if t:
            self.mypoynt1.setX(self.mypoynt2.x())
            self.mypoynt1.setY(self.mypoynt2.y())

    def rright(self, rotate):
        self.lrotate -= rotate

    def rleft(self, rotate):
        self.lrotate += rotate

    def back(self, lenght):
        x1 = self.mypoynt1.x()
        y1 = self.mypoynt1.y()
        x2 = x1 - lenght * cos(radians(self.lrotate))
        y2 = y1 + lenght * sin(radians(self.lrotate))
        start_in_canv = x1 < (
                self.width() + 100) / 2 and x1 > -self.width() / 2 and y1 < self.height() / 2 and y1 > -self.height() / 2
        end_in_canv = x2 < self.width() / 2 and x2 > -self.width() / 2 and y2 < self.height() / 2 and y2 > -self.height() / 2
        if start_in_canv or end_in_canv:
            self.scene().addLine(self.mypoynt1.x(), self.mypoynt1.y(), x2, y2, self.pen)
        self.mypoynt1.setX(x2)
        self.mypoynt1.setY(y2)

    def forward(self, lenght):
        x1 = self.mypoynt1.x()
        y1 = self.mypoynt1.y()
        x2 = x1 + lenght * cos(radians(self.lrotate))
        y2 = y1 - lenght * sin(radians(self.lrotate))
        start_in_canv = x1 < (
                self.width() + 100) / 2 and x1 > -self.width() / 2 and y1 < self.height() / 2 and y1 > -self.height() / 2
        end_in_canv = x2 < self.width() / 2 and x2 > -self.width() / 2 and y2 < self.height() / 2 and y2 > -self.height() / 2
        if start_in_canv or end_in_canv:
            self.scene().addLine(self.mypoynt1.x(), self.mypoynt1.y(), x2, y2, self.pen)
        self.mypoynt1.setX(x2)
        self.mypoynt1.setY(y2)

    def square(self, lenght):
        self.scene().addRect(QRectF(self.mypoynt1.x(), self.mypoynt1.y() - lenght, lenght, lenght), self.pen,
                             QBrush(self.pen.color()))

    def circle(self, lenght):
        self.scene().addEllipse(QRectF(self.mypoynt1.x(), self.mypoynt1.y() - lenght, lenght, lenght), self.pen,
                                QBrush(self.pen.color()))

    def triangle(self, lenght):
        x1 = self.mypoynt1.x() + lenght * cos(radians(60))
        y1 = self.mypoynt1.y() - lenght * sin(radians(60))
        self.scene().addPolygon(
            QPolygonF([self.mypoynt1, QPointF(x1, y1), QPointF(self.mypoynt1.x() + lenght, self.mypoynt1.y())]),
            self.pen, QBrush(self.pen.color()))

    def change_color(self):
        c = self.j % self.clr_list.count()
        self.pen.setColor(self.clr_list.item(c).data(3))
        self.j += 1

    def set_clr_list(self, clr_list):
        self.clr_list = clr_list


if __name__ == '__main__':
    print("не написано")
