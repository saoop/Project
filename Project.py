import sys
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QColorDialog
from PyQt5.QtGui import QPixmap
from projform import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 900, 700)
        self.setWindowTitle('Шестая программа')

        self.MainLabel = QtWidgets.QLabel(self)
        self.MainLabel.setGeometry(QtCore.QRect(40, 70, 800, 421))
        self.MainLabel.setText("")

        self.uploadBtn = QtWidgets.QPushButton(self)
        self.uploadBtn.setGeometry(QtCore.QRect(40, 530, 151, 51))
        self.uploadBtn.setText('Upload')

        self.saveBtn = QPushButton(self)
        self.saveBtn.setGeometry(40, 585, 151, 51)
        self.saveBtn.setText('Save')
        self.saveBtn.clicked.connect(self.save_result)

        self.rotLeft = QtWidgets.QPushButton(self)
        self.rotLeft.setGeometry(QtCore.QRect(214, 530, 61, 23))
        self.rotLeft.setText('rot Left')

        self.rotRight = QtWidgets.QPushButton(self)
        self.rotRight.setGeometry(QtCore.QRect(280, 530, 61, 23))
        self.rotRight.setText('rot right')

        self.setColorButton = QPushButton(self)
        self.setColorButton.setGeometry(400, 530, 80, 30)
        self.setColorButton.setText('Change Color')
        self.setColorButton.clicked.connect(self.changeColor)

        self.uploadBtn.clicked.connect(self.start)

        self.rotLeft.clicked.connect(self.rotl)
        self.rotRight.clicked.connect(self.rotr)

        self.brushColor = (0, 0, 0)

        self.ok = None
        self.click = None

        self.show()

    def mouseMoveEvent(self, event):
        if self.click:
            self.draw(event.x(), event.y())

    def mousePressEvent(self, event):
        if self.ok:
            self.click = True
            self.draw(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        if self.ok:
            self.click = False

    def draw(self, x, y):
        for i in range(x, x + 5):
            for j in range(y, y + 5):
                try:
                    self.pixels[i - 42, j - 42] = self.brushColor
                except IndexError:
                    pass
        self.paint()

    def changeColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.brushColor = color.red(), color.green(), color.blue()
            print(self.brushColor)

    def rotr(self):
        rotate = np.asarray(self.img)
        rotate = np.rot90(rotate, -1)
        self.img = Image.fromarray(rotate)
        self.paint()

    def rotl(self):
        rotate = np.asarray(self.img)
        rotate = np.rot90(rotate, 1)
        self.img = Image.fromarray(rotate)
        self.paint()

    def start(self):
        i, okBtnPressed = QInputDialog.getText(
            self, "Input name", "Name"
        )
        if okBtnPressed:
            self.img = Image.open(i)
            self.pixels_array = np.asarray(self.img)
            self.pix = self.img.load()
            self.paint()
            self.ok = True
            self.pixels = self.img.load()

    def paint(self):
        pix = QPixmap.fromImage(ImageQt(self.img.convert("RGBA")))
        self.MainLabel.setPixmap(pix)

    def save_result(self):
        i, okBtnPressed = QInputDialog.getText(
            self, "Input name", "Name"
        )
        if okBtnPressed:
            self.img.save(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
