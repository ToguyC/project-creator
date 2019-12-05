import sys, os, subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UIElements.PicButton import PicButton
from UIElements.Palette import Palette
from UIElements.Button import Button
from login import LoginGUIDialog
from security.crypto import Crypto

class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Project creator GUI'
        self.left = 100
        self.right = 100
        self.width = 350
        self.height = 150
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.crypto = Crypto(os.path.join(self.path, '..\\user.conf'))

        self.initUI()

    def initUI(self):
        self.initControls()

        self.setStyleSheet("QToolTip { font: sans-serif; font-size: 12px; color: #ffffff; background-color: #545454; border: 1px solid white; }")
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.oldPos = self.pos()
        self.show()

    def initControls(self):
        createButton = Button('Create')
        createButton.clicked.connect(self.createProject)
        cancelButton = Button('Cancel')
        cancelButton.clicked.connect(self.btnQuit_click)
        loginButton = Button('Login', self)
        loginButton.resize(40, 18)
        loginButton.move(5, 5)
        loginButton.clicked.connect(self.login)

        main_folder = QLabel('Project parent folder', self)
        name = QLabel('Project name', self)
        language = QLabel('Project language', self)

        self.main_folder_edit = QLineEdit()

        self.name_edit = QLineEdit()
        self.language_edit = QLineEdit()

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
        grid.addWidget(main_folder, 1, 0)
        grid.addWidget(self.main_folder_edit, 1, 1, 1, 4)

        grid.addWidget(name, 2, 0)
        grid.addWidget(self.name_edit, 2, 1, 1, 4)

        grid.addWidget(language, 3, 0)
        grid.addWidget(self.language_edit, 3, 1, 1, 4)

        grid.addWidget(createButton, 4, 4)
        grid.addWidget(cancelButton, 4, 3)

        grid.setContentsMargins(10, 30, 10, 10)
        self.setLayout(grid)

    @pyqtSlot()
    def btnQuit_click(self):
        exit()

    @pyqtSlot()
    def btnMin_click(self):
        self.showMinimized()

    @pyqtSlot()
    def createProject(self):
        user_infos = self.crypto.decrypt()
        
        if (user_infos != []):
            if (self.name_edit.text() != "" and self.main_folder_edit.text() != "" and self.language_edit.text() != ""):
                if (os.path.isdir(self.main_folder_edit.text())):
                    if ((not ' ' in self.name_edit.text()) and (not ' ' in self.language_edit.text())):
                        subprocess.call([sys.executable, os.path.join(self.path, 'setup-github.py'), '--project', self.name_edit.text(), '--folder', os.path.join(self.path, '..\\')])
                        
                        main_path = self.main_folder_edit.text() + "\\" + self.language_edit.text().capitalize()
                        if (not os.path.isdir(main_path)):
                            os.mkdir(main_path)
                        os.mkdir(main_path + "\\" + self.name_edit.text())
                        os.chdir(main_path + "\\" + self.name_edit.text())
                        os.system('git init')
                        os.system(f'git remote add origin https://github.com/{self.crypto.decrypt()[0]}/{self.name_edit.text()}.git')
                        os.system('type nul > README.md')
                        os.system('git add .')
                        os.system('git commit -m "Initial commit')
                        os.system('git push -u origin master')
                        os.chdir(self.path)
                    else:
                        QMessageBox.critical(self, 'Spaces error', 'The project name and language cannot contains spaces', QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, 'Main folder error', 'The main folder seems to not be a folder', QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Project error', 'Some informations seems to be missing', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Login error', 'No user infos stored.\nPlease login before create a new project', QMessageBox.Ok)

    @pyqtSlot()
    def login(self):
        loginDialog = LoginGUIDialog()
        if loginDialog.exec_():
            subprocess.call([
                sys.executable,
                os.path.join(self.path, 'save-user-infos.py'), 
                '--conf', os.path.join(self.path, '..\\user.conf'),
                '--name', loginDialog.user_name,
                '--password', loginDialog.user_password
            ])

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    dark_palette = Palette()
    app.setPalette(dark_palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    ex = GUI()
    sys.exit(app.exec_())