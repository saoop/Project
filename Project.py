import sys
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QInputDialog
from PyQt5.QtWidgets import QLCDNumber, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from projform import Ui_Dialog


class Example(QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Шестая программа')

        self.uploadBtn.clicked.connect(self.start)

        self.pushButton.clicked.connect(self.rotl)
        self.pushButton_2.clicked.connect(self.rotr)

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
                    pixels[i - 10, j - 12] = (0, 0, 0)
                except Exception:
                    pass

        self.img = im
        self.paint()

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
            print('ok')
            self.pixels_array = np.asarray(self.img)
            self.pix = self.img.load()
            self.paint()
            print('ok')
            self.ok = True

    def paint(self):
        pix = QPixmap.fromImage(ImageQt(self.img.convert("RGBA")))
        self.MainLabel.setPixmap(pix)
        print('ok')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
