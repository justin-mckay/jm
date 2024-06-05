import sys
import numpy as np
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
                             QWidget, QPushButton, QFileDialog, QTextEdit)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class SteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('DCT Steganography')

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.imageLabel)

        self.textEdit = QTextEdit(self)
        self.textEdit.setPlaceholderText('Enter the message to hide...')
        self.layout.addWidget(self.textEdit)

        self.loadButton = QPushButton('Load Image', self)
        self.loadButton.clicked.connect(self.loadImage)
        self.layout.addWidget(self.loadButton)

        self.saveButton = QPushButton('Save Image with Hidden Message', self)
        self.saveButton.clicked.connect(self.saveImage)
        self.layout.addWidget(self.saveButton)

        self.extractButton = QPushButton('Extract Hidden Message', self)
        self.extractButton.clicked.connect(self.extractMessage)
        self.layout.addWidget(self.extractButton)

        self.image = None

    def loadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                  "Images (*.png *.jpg *.bmp)", options=options)
        if fileName:
            self.image = cv2.imread(fileName)
            self.displayImage(self.image)

    def displayImage(self, image):
        scaled_image = self.scaleImage(image, width=600)
        qformat = QImage.Format_RGB888
        img = QImage(scaled_image, scaled_image.shape[1], scaled_image.shape[0], scaled_image.strides[0], qformat)
        img = img.rgbSwapped()
        self.imageLabel.setPixmap(QPixmap.fromImage(img))

    def scaleImage(self, image, width=None, height=None):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        scaled = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return scaled

    def saveImage(self):
        if self.image is not None:
            message = self.textEdit.toPlainText()
            image_with_message = self.hideMessageInImage(self.image, message)
            if image_with_message is not None:
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getSaveFileName(self, "Save Image File", "",
                                                          "Images (*.png *.jpg *.bmp)", options=options)
                if fileName:
                    cv2.imwrite(fileName, image_with_message)
                    self.displayImage(image_with_message)

    def hideMessageInImage(self, image, message):
        if not message:
            return None

        # Convert the image to YCbCr color space
        ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        y, cb, cr = cv2.split(ycbcr)

        # Apply DCT to the Y channel
        dct = cv2.dct(np.float32(y))

        # Embed the message into the DCT coefficients
        message += chr(0)  # Append a null character to denote end of message
        msg_index = 0
        msg_len = len(message)

        for i in range(dct.shape[0]):
            for j in range(dct.shape[1]):
                if msg_index < msg_len:
                    dct[i, j] = ord(message[msg_index])
                    msg_index += 1
                else:
                    break

        # Perform inverse DCT to get the Y channel back
        y = cv2.idct(dct).clip(0, 255).astype(np.uint8)

        # Merge the channels and convert back to BGR color space
        ycbcr = cv2.merge([y, cb, cr])
        image_with_message = cv2.cvtColor(ycbcr, cv2.COLOR_YCrCb2BGR)
        return image_with_message

    def extractMessage(self):
        if self.image is not None:
            hidden_message = self.extractMessageFromImage(self.image)
            if hidden_message:
                self.textEdit.setText(hidden_message)
            else:
                self.textEdit.setText('No hidden message found.')

    def extractMessageFromImage(self, image):
        # Convert the image to YCbCr color space
        ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        y, _, _ = cv2.split(ycbcr)

        # Apply DCT to the Y channel
        dct = cv2.dct(np.float32(y))

        # Extract the message from the DCT coefficients
        message = ''
        for i in range(dct.shape[0]):
            for j in range(dct.shape[1]):
                char = chr(int(dct[i, j]))
                if char == chr(0):  # Null character denotes end of message
                    return message
                message += char
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SteganographyApp()
    ex.show()
    sys.exit(app.exec_())
