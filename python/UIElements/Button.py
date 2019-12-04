from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Button(QPushButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)
        self.setText(text)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setCursor(QCursor(Qt.ArrowCursor))