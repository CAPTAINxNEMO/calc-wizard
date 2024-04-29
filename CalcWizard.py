# GUI
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

CalcWizard = QApplication([])

# Window Attributes
window = QMainWindow()
window.setWindowTitle('CalcWizard')
window.setGeometry(660, 60, 600, 960)
window.setFixedSize(600, 960)

# Font Attributes
# Main Label & Switch Button Font
mainLabel_switchButtonFont = QFont('Aptos')
mainLabel_switchButtonFont.setPixelSize(52)
mainLabel_switchButtonFont.setBold(True)
# Input Field Font
inputFieldFont = QFont('Aptos')
inputFieldFont.setPixelSize(28)
inputFieldFont.setBold(False)
# Output Field Font
outputFieldFont = QFont('Aptos')
outputFieldFont.setPixelSize(28)
outputFieldFont.setBold(True)
# Advanced & Basic Buttons
advanced_basicButtonFont = QFont('Aptos')
advanced_basicButtonFont.setPixelSize(48)
advanced_basicButtonFont.setBold(True)
# Number Pad
numberPadFont = QFont('Aptos')
numberPadFont.setPixelSize(36)
numberPadFont.setBold(True)

# Switch between Modes Button
switchButton = QPushButton('⇄', window)
switchButton.setFixedSize(60, 60)
switchButton.move(510, 30)
switchButton.setFont(mainLabel_switchButtonFont)
def switchMode():
    print('Switch')
switchButton.clicked.connect(switchMode)

# Calculator Page Main Label
calculatorLabel = QLabel('CALCULATOR', window)
calculatorLabel.setFixedSize(540, 60)
calculatorLabel.move(30, 120)
calculatorLabel.setFont(mainLabel_switchButtonFont)
calculatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

# Input Field
inputField = QLineEdit(window)
inputField.setPlaceholderText('Input')
inputField.setFixedSize(540, 60)
inputField.move(30, 210)
inputField.setFont(inputFieldFont)
inputField.setAlignment(Qt.AlignmentFlag.AlignRight)
inputField.setStyleSheet('padding-right: 15px')
inputField.setReadOnly(True)

# Output Field
outputField = QLineEdit(window)
outputField.setFixedSize(540, 60)
outputField.move(30, 300)
outputField.setFont(outputFieldFont)
outputField.setAlignment(Qt.AlignmentFlag.AlignRight)
outputField.setStyleSheet('padding-right: 15px')
outputField.setPlaceholderText('Output')
outputField.setReadOnly(True)

# Advanced Mode Button
advancedButton = QPushButton('∞', window)
advancedButton.setFixedSize(90, 90)
advancedButton.move(30, 390)
advancedButton.setFont(advanced_basicButtonFont)
advancedButton.setVisible(True)
def advancedMode():
    advancedButton.setVisible(False)
    basicButton.setVisible(True)
advancedButton.clicked.connect(advancedMode)

# Basic Mode Button
basicButton = QPushButton('±', window)
basicButton.setFixedSize(90, 90)
basicButton.move(30, 390)
basicButton.setFont(advanced_basicButtonFont)
basicButton.setVisible(False)
def basicMode():
    advancedButton.setVisible(True)
    basicButton.setVisible(False)
basicButton.clicked.connect(basicMode)

# Number Pad
# Nine (9)
nineButton = QPushButton('9', window)
nineButton.setFixedSize(90, 90)
nineButton.move(300, 570)
nineButton.setFont(numberPadFont)
nineButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def nine():
    inputField.setText(inputField.text() + '9')
nineButton.clicked.connect(nine)
# Eight (8)
eightButton = QPushButton('8', window)
eightButton.setFixedSize(90, 90)
eightButton.move(210, 570)
eightButton.setFont(numberPadFont)
eightButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def eight():
    inputField.setText(inputField.text() + '8')
eightButton.clicked.connect(eight)
# Seven (7)
sevenButton = QPushButton('7', window)
sevenButton.setFixedSize(90, 90)
sevenButton.move(120, 570)
sevenButton.setFont(numberPadFont)
sevenButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def seven():
    inputField.setText(inputField.text() + '7')
sevenButton.clicked.connect(seven)
# Six (6)
sixButton = QPushButton('6', window)
sixButton.setFixedSize(90, 90)
sixButton.move(300, 660)
sixButton.setFont(numberPadFont)
sixButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def six():
    inputField.setText(inputField.text() + '6')
sixButton.clicked.connect(six)
# Five (5)
fiveButton = QPushButton('5', window)
fiveButton.setFixedSize(90, 90)
fiveButton.move(210, 660)
fiveButton.setFont(numberPadFont)
fiveButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def five():
    inputField.setText(inputField.text() + '5')
fiveButton.clicked.connect(five)
# Four (4)
fourButton = QPushButton('4', window)
fourButton.setFixedSize(90, 90)
fourButton.move(120, 660)
fourButton.setFont(numberPadFont)
fourButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def four():
    inputField.setText(inputField.text() + '4')
fourButton.clicked.connect(four)
# Three (3)
threeButton = QPushButton('3', window)
threeButton.setFixedSize(90, 90)
threeButton.move(300, 750)
threeButton.setFont(numberPadFont)
threeButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def three():
    inputField.setText(inputField.text() + '3')
threeButton.clicked.connect(three)
# Two (2)
twoButton = QPushButton('2', window)
twoButton.setFixedSize(90, 90)
twoButton.move(210, 750)
twoButton.setFont(numberPadFont)
twoButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def two():
    inputField.setText(inputField.text() + '2')
twoButton.clicked.connect(two)
# One (1)
oneButton = QPushButton('1', window)
oneButton.setFixedSize(90, 90)
oneButton.move(120, 750)
oneButton.setFont(numberPadFont)
oneButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def one():
    inputField.setText(inputField.text() + '1')
oneButton.clicked.connect(one)
# Zero (0)
zeroButton = QPushButton('0', window)
zeroButton.setFixedSize(90, 90)
zeroButton.move(210, 840)
zeroButton.setFont(numberPadFont)
zeroButton.setStyleSheet('background-color: rgb(185, 195, 205)')
def zero():
    inputField.setText(inputField.text() + '0')
zeroButton.clicked.connect(zero)

window.show()

CalcWizard.exec()