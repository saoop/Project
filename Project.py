import sys
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QColorDialog
from PyQt5.QtGui import QPixmap
from projform import Ui_Dialog


class Example(QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 900, 700)
        self.setWindowTitle('Шестая программа')

        self.setColorButton = QPushButton(self)
        self.setColorButton.setGeometry(400, 400, 80, 30)
        self.setColorButton.setText('Change Color')
        self.setColorButton.clicked.connect(self.changeColor)

        self.uploadBtn.clicked.connect(self.start)

        self.pushButton.clicked.connect(self.rotl)
        self.pushButton_2.clicked.connect(self.rotr)

        self.brushColor = (0, 0, 0)

        self.ok = None
        self.click = None

        self.show()

    def mouseMoveEvent(self, event):
        if self.click and self.ok:
            self.point(event.x(), event.y())

    def mousePressEvent(self, event):
        if self.ok:
            self.click = True
            self.point(event.x(), event.y())

    def mouseReleaseEvent(self, event):
        if self.ok:
            self.click = False

    def point(self, x, y):
        im = self.img.convert('RGB')
        pixels = im.load()
        for i in range(x, x + 5):
            for j in range(y, y + 5):
                try:
                    pixels[i - 42, j + 8] = self.brushColor
                except Exception:
                    pass

        self.img = im
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
            self, "Введите имя", "Как тебя зовут?"
        )
        if okBtnPressed:
            self.img = Image.open(i)
            self.pixels_array = np.asarray(self.img)
            self.pix = self.img.load()
            self.paint()
            self.ok = True

    def paint(self):
        pix = QPixmap.fromImage(ImageQt(self.img.convert("RGBA")))
        self.MainLabel.setPixmap(pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
