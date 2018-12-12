import sys
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL.ImageEnhance import Brightness, Sharpness, Contrast
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QColorDialog, QSlider, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap


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
        self.backNextBox = QHBoxLayout(self)

        self.lbl = QLabel(self)
        self.mainHBox.addWidget(self.lbl)

        brightBox = QVBoxLayout(self)

        self.brightSlider = QSlider(Qt.Vertical, self)
        self.brightSlider.setFocusPolicy(Qt.NoFocus)
        self.brightSlider.sliderReleased.connect(self.change_bright)
        self.brightSlider.setMaximum(100)
        self.brightSlider.setMinimum(1)
        self.brightSlider.setValue(50)
        brightBox.addWidget(self.brightSlider)

        self.brightImage = QLabel(self)
        self.brightImage.setPixmap(QPixmap('creative.png'))
        brightBox.addWidget(self.brightImage)

        self.mainHBox.addLayout(brightBox)

        sharpBox = QVBoxLayout(self)
        self.sharpSlider = QSlider(Qt.Vertical, self)
        self.sharpSlider.setFocusPolicy(Qt.NoFocus)
        self.sharpSlider.sliderReleased.connect(self.change_sharpness)
        self.sharpSlider.setMinimum(1)
        self.sharpSlider.setMaximum(250)
        self.sharpSlider.setValue(125)
        sharpBox.addWidget(self.sharpSlider)

        self.sharpImage = QLabel(self)
        self.sharpImage.setPixmap(QPixmap('cooking-knife.png'))
        sharpBox.addWidget(self.sharpImage)
        self.mainHBox.addLayout(sharpBox)

        contrastBox = QVBoxLayout(self)

        self.contrastSlider = QSlider(Qt.Vertical, self)
        self.contrastSlider.setFocusPolicy(Qt.NoFocus)
        self.contrastSlider.sliderReleased.connect(self.change_contrast)
        self.contrastSlider.setMinimum(1)
        self.contrastSlider.setMaximum(100)
        self.contrastSlider.setValue(50)
        contrastBox.addWidget(self.contrastSlider)

        self.contrastImage = QLabel(self)
        self.contrastImage.setPixmap(QPixmap('contrast.png'))
        contrastBox.addWidget(self.contrastImage)
        self.mainHBox.addLayout(contrastBox)

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
        self.negativeFilter.clicked.connect(self.make_negative)
        self.negativeFilter.hide()
        self.filtersBox.addWidget(self.negativeFilter)

        self.whiteBlackFilter = QPushButton(self)
        self.whiteBlackFilter.setText('White and Black')
        self.whiteBlackFilter.clicked.connect(self.make_black_white)
        self.whiteBlackFilter.hide()
        self.filtersBox.addWidget(self.whiteBlackFilter)

        self.grayFilter = QPushButton(self)
        self.grayFilter.setText('Gray Filter')
        self.grayFilter.clicked.connect(self.make_gray)
        self.grayFilter.hide()
        self.filtersBox.addWidget(self.grayFilter)

        self.sepiaFilter = QPushButton(self)
        self.sepiaFilter.setText('Sepia')
        self.sepiaFilter.clicked.connect(self.make_sepia)
        self.sepiaFilter.hide()
        self.filtersBox.addWidget(self.sepiaFilter)

        self.backButton = QPushButton(self)
        self.backButton.clicked.connect(self.back)
        self.backButton.setText('Back')
        self.backNextBox.addWidget(self.backButton)

        self.nextButton = QPushButton(self)
        self.nextButton.clicked.connect(self.next)
        self.nextButton.setText('Next')
        self.backNextBox.addWidget(self.nextButton)

        self.arrayOfImages = []
        self.currentIndex = None

        self.ok = None
        self.click = None

        self.brushColor = (0, 0, 0)

        self.rotright = QPushButton('Right')
        self.vbox.addWidget(self.rotright)
        self.rotright.clicked.connect(self.rotr)

        self.vbox.addLayout(self.backNextBox)

        self.mainHBox.addLayout(self.vbox)
        self.mainHBox.addLayout(self.filtersBox)
        self.setLayout(self.mainHBox)

        self.show()

    def update_array(self):
        if len(self.arrayOfImages) - 1 > self.currentIndex:
            self.arrayOfImages[self.currentIndex + 1] = self.img
            self.currentIndex += 1
        else:
            self.arrayOfImages.append(self.img)
            self.currentIndex += 1

    def next(self):
        if self.currentIndex < len(self.arrayOfImages) - 1:
            self.currentIndex += 1
            self.img = self.arrayOfImages[self.currentIndex]
            self.pixels = self.img.load()
            self.paint()

    def back(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.img = self.arrayOfImages[self.currentIndex]
            self.pixels = self.img.load()
            self.paint()

    def make_sepia(self):
        x, y = self.img.size
        working_img = self.img.copy()
        pix = working_img.load()
        for i in range(x):
            for j in range(y):
                r, g, b = pix[i, j]
                red = int(r * 0.393 + g * 0.769 + b * 0.189)
                green = int(r * 0.349 + g * 0.686 + b * 0.168)
                blue = int(r * 0.272 + g * 0.534 + b * 0.131)
                pix[i, j] = (red, green, blue)
        self.img = working_img.copy()
        self.update_array()

        self.paint()

    def make_gray(self):
        x, y = self.img.size
        working_img = self.img.copy()
        pix = working_img.load()
        for i in range(x):
            for j in range(y):
                r, g, b = pix[i, j]
                gray = int(r * 0.2126 + g * 0.7152 + b * 0.0722)
                pix[i, j] = (gray, gray, gray)
        self.img = working_img.copy()
        self.update_array()

        self.paint()

    def make_black_white(self):
        x, y = self.img.size
        s = 255 / 2 * 3
        working_img = self.img.copy()
        pix = working_img.load()
        for i in range(x):
            for j in range(y):
                r, g, b = pix[i, j]
                if r + g + b < s:
                    pix[i, j] = (0, 0, 0)
                else:
                    pix[i, j] = (255, 255, 255)
        self.img = working_img.copy()
        self.update_array()

        self.paint()

    def make_negative(self):
        # self.pixels = map(lambda x: (255 - x[0], 255 - x[1], 255 - x[2]), self.pixels) Не работает :(
        x, y = self.img.size
        working_img = self.img.copy()
        pix = working_img.load()
        for i in range(x):
            for j in range(y):
                r, g, b = pix[i, j]
                pix[i, j] = (255 - r, 255 - g, 255 - b)
        self.img = working_img.copy()
        self.update_array()

        self.paint()

    def show_hide_filters(self):

        if self.Filters.text() == 'Show Filters':
            self.negativeFilter.setVisible(True)
            self.whiteBlackFilter.setVisible(True)
            self.grayFilter.setVisible(True)
            self.sepiaFilter.setVisible(True)
            self.Filters.setText('Hide Filters')
        else:
            self.negativeFilter.hide()
            self.sepiaFilter.hide()
            self.whiteBlackFilter.hide()
            self.grayFilter.hide()
            self.Filters.setText('Show Filters')

    def mouseMoveEvent(self, event):
        if self.click:
            self.point(event.x(), event.y())

    def mousePressEvent(self, event):
        if self.ok:
            self.working_img = self.img.copy()
            self.pix = self.working_img.load()
            self.point(event.x(), event.y())
            self.click = True

    def mouseReleaseEvent(self, event):
        self.click = False
        self.img = self.working_img.copy()
        self.working_img = None
        self.update_array()

    def point(self, x, y):
        for i in range(x, x + 5):
            for j in range(y, y + 5):
                try:
                    self.pix[i - 10, j - 12] = self.brushColor
                except IndexError:
                    pass
        self.img = self.working_img.copy()
        self.paint()

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.brushColor = color.red(), color.green(), color.blue()
            self.setColorButton.setStyleSheet(
                "background-color: {0}".format(color.name())
            )

    def change_sharpness(self):
        if self.ok:
            try:
                val = self.sharpSlider.value()
                enhancer = Sharpness(self.img)
                self.img = enhancer.enhance(val / 50)
                self.pixels = self.img.load()
                self.update_array()
                self.paint()
            except Exception:
                pass

    def change_contrast(self):
        if self.ok:
            try:
                val = self.contrastSlider.value()
                self.img = Contrast(self.img).enhance(val / 50)
                self.pixels = self.img.load()
                self.update_array()

                self.paint()
            except Exception:
                pass

    def change_bright(self):
        # !!!!! ПОСЛЕ ИЗМЕНЕНИЯ ЯРКОСТИ НЕ РАБОТАЕТ РИСОВАНИЕ
        if self.ok:
            try:
                val = self.brightSlider.value()
                self.img = Brightness(self.img).enhance(val / 50)
                # После изменения яркости не работало рисование, надо было обновить переменную self.pixels
                self.pixels = self.img.load()
                self.update_array()

                self.paint()
            except Exception:
                pass

    def rotr(self):
        rotate = np.asarray(self.img)
        rotate = np.rot90(rotate, -1)
        self.img = Image.fromarray(rotate)
        self.pixels = self.img.load()
        self.update_array()

        self.paint()

    def rotl(self):
        rotate = np.asarray(self.img)
        rotate = np.rot90(rotate, 1)
        self.img = Image.fromarray(rotate)
        self.pixels = self.img.load()
        self.update_array()

        self.paint()

    def start(self):
        name, okBtnPressed = QInputDialog.getText(
            self, "input name", "name"
        )
        if okBtnPressed:
            self.img = Image.open(name)
            self.arrayOfImages.append(self.img)
            self.currentIndex = 0
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
