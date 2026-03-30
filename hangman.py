import sys
from PyQt5 import QtWidgets, uic
import random
from_class = uic.loadUiType('hangman.ui')[0]
def find_letter(letter, a_string):
    locations = []
    start = 0
    while a_string.find(letter, start, len(a_string)) != -1:
        pos = a_string.find(letter, start, len(a_string))
        locations.append(pos)
        start = pos + 1
    return locations

def replace_letters(string, locations, letter):
    new_string = ''
    for i in range(0, len(string)):
        if i in locations:
            new_string = new_string + letter
        else:
            new_string = new_string + string[i]
    return new_string
def dashes(word):
    letter = 'abcdefghijklmnopqrstuvwxyz'
    new_string = ''
    for i in word:
        if i in letter:
            new_string += '-'
        else:
            new_string += i
    return new_string
class HangmanGame(QtWidgets.QMainWindow, from_class):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.btn_guess.clicked.connect(self.btn_guess_clicked)
        self.actionExit.triggered.connect(self.menuExit_selected)
        self.pieces = [self.head, self.body, self.leftarm, self.leftleg,
                       self.rightarm, self.rightleg]
        self.gallows = [self.line1, self.line2, self.line3, self.line4]
        self.piece_shown = 0
        self.currentword = ''
        f = open('personal information/words.txt', 'r')
        self.lines = f.readlines()
        f.close()
        self.new_game()
    def new_game(self):
        self.guesses.setText("")
        self.currentword = random.choice(self.lines)
        self.currentword = self.currentword.strip()
        for i in self.pieces:
            i.setFrameShadow(QtWidgets.QFrame.Plain)
            i.setHidden(True)
        for i in self.gallows:
            i.setFrameShadow(QtWidgets.QFrame.Plain)
        self.word.setText(dashes(self.currentword))
        self.piece_shown = 0
    def btn_guess_clicked(self):
        guess = str(self.guessBox.text())
        if str(self.guesses.text()) != '':
            self.guesses.setText(str(self.guesses.text()) + guess)
        else:
            self.guesses.setText(guess)
        if len(guess) == 1:
            if guess in self.currentword:
                locations = find_letter(guess, self.currentword)
                self.word.setText(replace_letters(str(self.word.text()),
                                                  locations,guess))
                if str(self.word.text()) == self.currentword:
                    self.win()
            else:
                self.wrong()
        else:
            if guess == self.currentword:
                self.win()
            else:
                self.wrong()
        self.guessBox.setText("")
    def win(self):
        QtWidgets.QMessageBox.information(self, "Hangman", "You win!")
        self.new_game()
    def wrong(self):
        self.piece_shown += 1
        # 显示gallows中存在的元素
        for i in range(min(self.piece_shown, len(self.gallows))):
            self.gallows[i].setHidden(False)
        # 显示对应的小人部分
        if self.piece_shown <= len(self.pieces):
            for i in range(min(self.piece_shown, len(self.pieces))):
                self.pieces[i].setHidden(False)
        if self.piece_shown == len(self.pieces):
            message = "You lose.  The word was " + self.currentword
            QtWidgets.QMessageBox.warning(self,"Hangman", message)
            self.new_game()
    def menuExit_selected(self):
        self.close()

app = QtWidgets.QApplication(sys.argv)
myapp = HangmanGame()
myapp.show()
app.exec_()

