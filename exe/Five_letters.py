from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit
from PyQt5 import QtCore


class Five_letters(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.ch = 0
        self.att = 5
        for i in range(0, 6):
            for j in range(0, 5):
                label = QLineEdit('', self)
                label.setReadOnly(True)
                label.setMaxLength(1)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setStyleSheet("color: white;background-color: black;"
                                    "border-style: outset;"
                                    "font-size: 18pt; font-family: Courier;"
                                    "border-radius: 10px;"
                                    "padding: 6px;"
                                    "border: 1px solid yellow;")
                self.layout.addWidget(label, i, j)
                label.setFocusPolicy(Qt.StrongFocus)
                label.keyPressed.connect(self.back)
                label.keyPressed.connect(self.arrow)
                label.textChanged.connect(self.nextWidg)
        self.setLayout(self.layout)
        self.layout.itemAt(0).widget().setReadOnly(False)

    def nextWidg(self):
        if self.ch < self.layout.count() - 1 - self.att * 5 and self.ch <= 28 and\
                len(self.layout.itemAt(self.ch).widget().text()):
            self.ch += 1
            self.layout.itemAt(self.ch).widget().setReadOnly(False)
            QTest.mouseClick(self.layout.itemAt(self.ch).widget(), Qt.LeftButton)

    def back(self, key):
        if self.ch != 0 and key == QtCore.Qt.Key_Backspace and not self.layout.itemAt(
                self.ch - 1).widget().isReadOnly():
            self.layout.itemAt(self.ch).widget().setText('')
            if self.ch > 0:
                self.ch -= 1
                QTest.mouseClick(self.layout.itemAt(self.ch).widget(), Qt.LeftButton)

    def arrow(self, key):
        if self.ch != 0 and self.ch != 29 and key == QtCore.Qt.Key_Left and not self.layout.itemAt(
                self.ch - 1).widget().isReadOnly():
            self.ch -= 1
            QTest.mouseClick(self.layout.itemAt(self.ch).widget(), Qt.LeftButton)
        if key == QtCore.Qt.Key_Right and not self.layout.itemAt(
                self.ch + 1).widget().isReadOnly() and self.ch != 29:
            self.ch += 1
            QTest.mouseClick(self.layout.itemAt(self.ch).widget(), Qt.LeftButton)


class QLineEdit(QLineEdit):
    keyPressed = QtCore.pyqtSignal(int)

    def keyPressEvent(self, event):
        super(QLineEdit, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())
