import random
import sqlite3

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QWidget, QVBoxLayout, \
    QPushButton, QMessageBox
from Five_letters import Five_letters


class Game(QWidget):

    def __init__(self):
        super().__init__()
        self.words = self.generate_word()
        self.word = random.choice(self.words)[0]
        self.uses_words = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.guess_the_word())

        rules = QPushButton('правила')
        rules.setStyleSheet("color: white;background-color: black;"
                            "border-style: outset;"
                            "font-size: 18pt; font-family: Courier;"
                            "border-radius: 10px;"
                            "padding: 6px;"
                            "border: 1px solid yellow;")
        check = QPushButton('Проверить')

        check.setStyleSheet("color: white;background-color: black;"
                            "border-style: outset;"
                            "font-size: 18pt; font-family: Courier;"
                            "border-radius: 10px;"
                            "padding: 6px;"
                            "border: 1px solid yellow;")
        check.clicked.connect(self.check_click)
        check.setCheckable(True)
        rules.setCheckable(True)
        layout.addWidget(check)
        layout.addWidget(rules)
        rules.clicked.connect(self.print_rules)

    def check_in_base(self, word):
        return word in dict(self.words)

    def print_rules(self):
        QMessageBox.about(self, "Правила", "Вам нужно одгадать слово из пяти букв в единственном числе. На разгадку вам"
                                           " дается 6 попыток. После каждой попытки цвет букв меняется."
                                           "Белый цвет означает, что буквы есть в загаданном слове, но стоят в других "
                                           "местах "
                                           " Серый цвет означает, что буквы отсутствуют в загаданном слове. "
                                           "Желтый цвет означает, что буквы есть в загаданном слове и стоят на нужных "
                                           "местах. "
                                           "Когда вы угадаете слово, все буквы окрасятся в желтый.")

    def check_click(self):
        a = ''
        if self.window_five_letters.ch == 5 * (6 - self.window_five_letters.att) - 1 and \
                len(self.window_five_letters.layout.itemAt(self.window_five_letters.ch).widget().text()) == 1:

            for i in range(self.window_five_letters.ch - 4,
                           5 * (6 - self.window_five_letters.att)):
                a += self.window_five_letters.layout.itemAt(i).widget().text()

            if self.check_in_base(a.lower()):
                if a not in self.uses_words:
                    if self.check_word(a):
                        return
                    self.nextdown()
                    self.window_five_letters.att -= 1
                    if self.window_five_letters.ch == 29 and self.word != a:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.resize(500, 500)
                        msg.setWindowTitle('Игра окончена')
                        msg.setText('Вы проиграли, правильное слово: ' + self.word)
                        msg.setStyleSheet("color: white;background-color: black;"
                                          "border-style: outset;"
                                          "font-size: 25pt; font-family: Courier;"
                                          "border-radius: 10px;"
                                          "padding: 6px;"
                                          "border: 1px solid yellow;")
                        yes_button = msg.addButton('Хотите сыграть снова?', QtWidgets.QMessageBox.YesRole)
                        yes_button.clicked.disconnect()
                        yes_button.clicked.connect(self.restart)
                        yes_button.clicked.connect(msg.done)
                        msg.exec_()

                    else:
                        self.window_five_letters.ch += 1
                        self.window_five_letters.layout.itemAt(self.window_five_letters.ch).widget().setReadOnly(False)
                        self.uses_words.append(a)

                else:
                    for i in range(len(a)):
                        self.window_five_letters.layout.itemAt(self.window_five_letters.ch - i).widget().setText('')
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.resize(500, 500)
                    msg.setWindowTitle('Ошибка!')
                    msg.setText('Нельзя повторно использовать слова')
                    msg.setStyleSheet("color: white;background-color: black;"
                                      "border-style: outset;"
                                      "font-size: 25pt; font-family: Courier;"
                                      "border-radius: 10px;"
                                      "padding: 6px;"
                                      "border: 1px solid yellow;")
                    msg.exec_()
            elif a != '':
                for i in range(len(a)):
                    self.window_five_letters.layout.itemAt(self.window_five_letters.ch - i).widget().setText('')

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.resize(500, 500)
                msg.setWindowTitle('Ошибка')
                msg.setText('Такого существительного нет в игре.')
                msg.setStyleSheet("color: white;background-color: black;"
                                  "border-style: outset;"
                                  "font-size: 25pt; font-family: Courier;"
                                  "border-radius: 10px;"
                                  "padding: 6px;"
                                  "border: 1px solid yellow;")
                msg.exec_()
        elif self.window_five_letters.ch != 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.resize(500, 500)
            msg.setWindowTitle('Ошибка')
            msg.setText('Введите полностью слово!')
            msg.setStyleSheet("color: white;background-color: black;"
                              "border-style: outset;"
                              "font-size: 25pt; font-family: Courier;"
                              "border-radius: 10px;"
                              "padding: 6px;"
                              "border: 1px solid yellow;")
            msg.exec_()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.resize(500, 500)
            msg.setWindowTitle('Ошибка')
            msg.setText('Вы не ввели слово!!!')
            msg.setStyleSheet("color: white;background-color: black;"
                              "border-style: outset;"
                              "font-size: 25pt; font-family: Courier;"
                              "border-radius: 10px;"
                              "padding: 6px;"
                              "border: 1px solid yellow;")
            msg.exec_()

    def enter(self, key):
        if key == QtCore.Qt.Key_Return:
            self.check_click()

    def check_word(self, word):
        word = word.lower()
        if word == self.word:
            for i in range(len(word)):
                self.window_five_letters.layout.itemAt(self.window_five_letters.ch - i).widget().setStyleSheet(
                    "color: black;background-color: yellow;"
                    "border-style: outset;"
                    "font-size: 18pt; font-family: Courier;"
                    "border-radius: 10px;"
                    "padding: 6px;"
                    "border: 1px solid yellow;")
                self.window_five_letters.layout.itemAt(self.window_five_letters.ch - i).widget().setReadOnly(True)

            msg = QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.resize(500, 500)
            msg.setWindowTitle('Победитель')
            msg.setText('Вы выиграли!!!')
            msg.setStyleSheet("color: white;background-color: black;"
                              "border-style: outset;"
                              "font-size: 25pt; font-family: Courier;"
                              "border-radius: 10px;"
                              "padding: 6px;"
                              "border: 1px solid yellow;")

            yes_button = msg.addButton('Хотите сыграть снова?', QtWidgets.QMessageBox.YesRole)
            yes_button.clicked.disconnect()
            yes_button.clicked.connect(self.restart)
            yes_button.clicked.connect(msg.done)
            msg.exec_()

            return True

        else:
            for i in range(len(word)):
                if word.lower()[i] in self.word.lower():
                    if word[i] == self.word[i]:
                        self.window_five_letters.layout.itemAt(
                            self.window_five_letters.ch - 4 + i).widget().setStyleSheet(
                            "color: black;background-color: rgb(255, 255, 0);"
                            "border-style: outset;"
                            "font-size: 18pt; font-family: Courier;"
                            "border-radius: 10px;"
                            "padding: 6px;"
                            "border: 1px solid yellow;")
                        self.window_five_letters.layout.itemAt(
                            self.window_five_letters.ch - i).widget().setReadOnly(
                            True)
                    else:
                        self.window_five_letters.layout.itemAt(
                            self.window_five_letters.ch - 4 + i).widget().setStyleSheet(
                            "color: black;background-color: white;"
                            "border-style: outset;"
                            "font-size: 18pt; font-family: Courier;"
                            "border-radius: 10px;"
                            "padding: 6px;"
                            "border: 1px solid yellow;")
                        self.window_five_letters.layout.itemAt(
                            self.window_five_letters.ch - i).widget().setReadOnly(
                            True)

                else:
                    self.window_five_letters.layout.itemAt(self.window_five_letters.ch - 4 + i).widget().setStyleSheet(
                        "color: white;background-color: grey;"
                        "border-style: outset;"
                        "font-size: 18pt; font-family: Courier;"
                        "border-radius: 10px;"
                        "padding: 6px;"
                        "border: 1px solid yellow;")
                    self.window_five_letters.layout.itemAt(
                        self.window_five_letters.ch - i).widget().setReadOnly(
                        True)
            for i in range(len(word)):
                if word.count(word[i]) > 1:
                    if word[i] != self.word[i] and word[i:len(word)].count(word[i]) > 1:
                        self.window_five_letters.layout.itemAt(
                            self.window_five_letters.ch - 4 + i).widget().setStyleSheet(
                            "color: white;background-color: grey;"
                            "border-style: outset;"
                            "font-size: 18pt; font-family: Courier;"
                            "border-radius: 10px;"
                            "padding: 6px;"
                            "border: 1px solid yellow;")
        return False

    def nextdown(self):
        if self.window_five_letters.ch != 29 and self.window_five_letters.att > 0:
            QTest.mouseClick(self.window_five_letters.layout.itemAt(self.window_five_letters.ch + 1).widget(),
                             Qt.LeftButton)

    def guess_the_word(self):
        self.window_five_letters = Five_letters()
        for i in range(30):
            self.window_five_letters.layout.itemAt(i).widget().keyPressed.connect(self.enter)
        return self.window_five_letters

    def generate_word(self):
        con = sqlite3.connect('data.sqlite')

        cur = con.cursor()
        result = cur.execute('SELECT word, LENGTH(word) as length FROM nouns WHERE LENGTH(word) = 5').fetchall()

        con.close()
        return result

    def restart(self):
        for i in range(0, 30):
            self.window_five_letters.layout.itemAt(i).widget().setText('')
            self.window_five_letters.layout.itemAt(i).widget().setReadOnly(True)
            self.window_five_letters.layout.itemAt(i).widget().setStyleSheet(
                "color: white;background-color: black;"
                "border-style: outset;"
                "font-size: 18pt; font-family: Courier;"
                "border-radius: 10px;"
                "padding: 6px;"
                "border: 1px solid yellow;")

        self.window_five_letters.ch = 0
        self.word = random.choice(self.words)[0]
        self.uses_words = []
        self.window_five_letters.layout.itemAt(0).widget().setReadOnly(False)
        self.window_five_letters.att = 5
