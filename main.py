import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDesktopWidget, QPushButton, QMessageBox

from Game import Game


class Main_window(QWidget):
    def __init__(self):
        super().__init__()

        self.game = Game()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Игра 5БУКВ')
        self.game_view = QVBoxLayout()
        self.start = QPushButton('НАЧАТЬ ИГРУ?')
        self.start.clicked.connect(self.stated)
        self.game_view.addWidget(self.start)
        self.start.setCheckable(True)
        self.start.setStyleSheet("color: white;background-color: black;"
                                 "border-style: outset;"
                                 "font-size: 18pt; font-family: Courier;"
                                 "border-radius: 10px;"
                                 "padding: 6px;"
                                 "border: 1px solid yellow;")
        self.setGeometry(300, 300, 500, 500)
        self.setStyleSheet("color: white;background-color: black;"
                           "border-style: outset;"
                           "font-size: 18pt; font-family: Courier;"
                           "border-radius: 10px;"
                           "padding: 6px;"
                           "border: 1px solid yellow;")
        self.setLayout(self.game_view)
        self.center()

    def closeEvent(self, event):
        choice = QMessageBox.question(
            self,
            "Quit",
            "Вы хотите выйти",
            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def stated(self):
        self.game_view.addWidget(self.game)
        self.start.setVisible(False)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_window()
    ex.show()
    sys.exit(app.exec())
