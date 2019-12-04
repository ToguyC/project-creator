import sys, os, subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UIElements.PicButton import PicButton
from UIElements.Palette import Palette
from security.crypto import Crypto

class LoginGUIDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(LoginGUIDialog, self).__init__(*args, **kwargs)

        self.title = 'Login into github'
        self.left = 200
        self.right = 200
        self.width = 300
        self.height = 150
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.user_name = ""
        self.user_password = ""

        self.initUI()

    def initUI(self):
        self.initControls()

        self.setStyleSheet("QToolTip { font: sans-serif; font-size: 12px; color: #ffffff; background-color: #545454; border: 1px solid white; }")
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.oldPos = self.pos()

    def initControls(self):
        self.loginButton = QPushButton('Login')
        self.loginButton.clicked.connect(self.loginGithub)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.btnQuit_click)

        name = QLabel('User name', self)
        password = QLabel('User password', self)

        self.name_edit = QLineEdit()
        self.password_edit = QLineEdit()

        btnQuit = PicButton(QPixmap(os.path.join(self.path, '..\\img\\quit-btn.png')), QPixmap(os.path.join(self.path, '..\\img\\quit-btn-hover.png')), self)
        btnQuit.resize(13, 13)
        btnQuit.move(self.width - 18, 7)
        btnQuit.clicked.connect(self.btnQuit_click)

        btnMin = PicButton(QPixmap(os.path.join(self.path, '..\\img\\small-btn.png')), QPixmap(os.path.join(self.path, '..\\img\\small-btn-hover.png')), self)
        btnMin.resize(13, 13)
        btnMin.move(self.width - 40, 7)
        btnMin.clicked.connect(self.btnMin_click)

        grid = QGridLayout()
        grid.setSpacing(10)

        # grid.addWidget(element, row, col, rowspan, colspan)
        grid.addWidget(name, 1, 0)
        grid.addWidget(self.name_edit, 1, 1, 1, 4)

        grid.addWidget(password, 2, 0)
        grid.addWidget(self.password_edit, 2, 1, 1, 4)

        grid.addWidget(self.loginButton, 3, 4)
        grid.addWidget(self.cancelButton, 3, 3)

        grid.setContentsMargins(10, 30, 10, 10)
        self.setLayout(grid)

    @pyqtSlot()
    def btnQuit_click(self):
        self.close()

    @pyqtSlot()
    def btnMin_click(self):
        self.showMinimized()

    @pyqtSlot()
    def loginGithub(self):
        self.user_name = self.name_edit.text()
        self.user_password = self.password_edit.text()
        self.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor(28, 27, 37), 1, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(28, 27, 37), Qt.SolidPattern))
        painter.drawRect(0, 0, self.width, 25)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, event):
        self.oldPos = event.globalPos()
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()