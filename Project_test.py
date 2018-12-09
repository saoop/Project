import sys
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL.ImageEnhance import Brightness
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QColorDialog, QSlider, QLabel, QHBoxLayout, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 1000, 500)
        self.setWindowTitle('Шестая программа')
        self.mainHBox = QHBoxLayout(self)
        self.vbox = QVBoxLayout(self)
        self.filtersBox = QVBoxLayout(self)

        self.lbl = QLabel(self)
        self.mainHBox.addWidget(self.lbl)

        self.brightSlider = QSlider(Qt.Vertical, self)
        self.brightSlider.setFocusPolicy(Qt.NoFocus)

        self.brightSlider.sliderReleased.connect(self.change_bright)
        self.brightSlider.setMaximum(100)
        self.brightSlider.setMinimum(1)
        self.brightSlider.setValue(50)
        self.mainHBox.addWidget(self.brightSlider)

        self.btn = QPushButton('Upload')
        self.vbox.addWidget(self.btn)
        self.btn.clicked.connect(self.start)

        self.saveBtn = QPushButton(self)
        self.saveBtn.setText('Save')
        self.vbox.addWidget(self.saveBtn)
        self.saveBtn.clicked.connect(self.save_result)

        self.setColorButton = QPushButton(self)
        self.setColorButton.setText('Change Color')
        self.vbox.addWidget(self.setColorButton)
        self.setColorButton.clicked.connect(self.change_color)

        self.rotleft = QPushButton('Left')
        self.vbox.addWidget(self.rotleft)
        self.rotleft.clicked.connect(self.rotl)

        self.Filters = QPushButton(self)
        self.Filters.setText('Show Filters')
        self.Filters.clicked.connect(self.show_hide_filters)
        self.filtersBox.addWidget(self.Filters)

        self.negativeFilter = QPushButton(self)
        self.negativeFilter.setText('Negative')
        self.negativeFilter.hide()
        self.filtersBox.addWidget(self.negativeFilter)

        self.ok = None
        self.click = None

        self.brushColor = (0, 0, 0)

        self.rotright = QPushButton('Right')
        self.vbox.addWidget(self.rotright)
        self.rotright.clicked.connect(self.rotr)

        self.mainHBox.addLayout(self.vbox)
        self.mainHBox.addLayout(self.filtersBox)
        self.setLayout(self.mainHBox)

        self.show()

    def show_hide_filters(self):
        if self.Filters.text() == 'Show Filters':
            self.negativeFilter.setVisible(True)
            self.Filters.setText('Hide Filters')
        else:
            self.negativeFilter.hide()
            self.Filters.setText('Show Filters')

    def mouseMoveEvent(self, event):
        if self.click:
            self.point(event.x(), event.y())

    def mousePressEvent(self, event):
        if self.ok:
            self.point(event.x(), event.y())
            self.click = True

    def mouseReleaseEvent(self, event):
        self.click = False

    def point(self, x, y):
        for i in range(x, x + 5):
            for j in range(y, y + 5):
                try:
                    self.pixels[i - 10, j - 12] = self.brushColor
                except IndexError:
                    pass

        self.paint()

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.brushColor = color.red(), color.green(), color.blue()
            self.setColorButton.setStyleSheet(
                "background-color: {0}".format(color.name())
            )

    def change_bright(self):
        # !!!!! ПОСЛЕ ИЗМЕНЕНИЯ ЯРКОСТИ НЕ РАБОТАЕТ РИСОВАНИЕ
        if self.ok:
            try:
                val = self.brightSlider.value()
                self.img = Brightness(self.img).enhance(val / 50)
                # После изменения яркости не работало рисование, надо было обновить переменную self.pixels
                self.pixels = self.img.load()
                self.paint()
            except Exception:
                pass

    def rotr(self):
        rotate = np.asarray(self.img)
        rotate = np.rot90(rotate, -1)
        self.img = Image.fromarray(rotate)
        self.pixels = self.img.load()
        self.paint()

    def rotl(self):
        rotate = np.asarray(self.img)
        rotate = np.rot90(rotate, 1)
        self.img = Image.fromarray(rotate)
        self.pixels = self.img.load()
        self.paint()

    def start(self):
        name, okBtnPressed = QInputDialog.getText(
            self, "input name", "name"
        )
        if okBtnPressed:
            self.img = Image.open(name)
            self.pixels_array = np.asarray(self.img)
            self.pixels = self.img.load()
            self.paint()
            self.ok = True

    def paint(self):
        pix = QPixmap.fromImage(ImageQt(self.img.convert("RGBA")))
        self.lbl.setPixmap(pix)
        self.setLayout(self.mainHBox)

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
