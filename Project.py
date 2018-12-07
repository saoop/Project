import sys
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QLCDNumber, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Шестая программа')
        self.hbox = QHBoxLayout(self)

        self.lbl = QLabel(self)
        self.hbox.addWidget(self.lbl)

        self.btn = QPushButton('start')
        self.hbox.addWidget(self.btn)
        self.btn.clicked.connect(self.start)

        self.text = QLineEdit(self)
        self.hbox.addWidget(self.text)

        self.rotleft = QPushButton('Left')
        self.hbox.addWidget(self.rotleft)
        self.rotleft.clicked.connect(self.rotl)

        self.ok = None
        self.click = None

        self.rotright = QPushButton('Right')
        self.hbox.addWidget(self.rotright)
        self.rotright.clicked.connect(self.rotr)

        self.show()

    def mouseMoveEvent(self, event):
        if self.click and self.ok:
            coordX = event.x()
            coordY = event.y()
            self.point(coordX, coordY)

    def mousePressEvent(self, event):
        if self.ok:
            self.click = True

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
        self.img = Image.open(self.text.text())
        self.pixels_array = np.asarray(self.img)
        self.pix = self.img.load()
        self.paint()
        self.ok = True

    def paint(self):
        pix = QPixmap.fromImage(ImageQt(self.img.convert("RGBA")))
        self.lbl.setPixmap(pix)
        self.setLayout(self.hbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
