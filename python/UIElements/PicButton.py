from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_leave = pixmap
        self.pixmap_hover = pixmap_hover

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.pixmap = self.pixmap_hover
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.pixmap = self.pixmap_leave
        self.setCursor(QCursor(Qt.ArrowCursor))

    def sizeHint(self):
        return self.pixmap.size()