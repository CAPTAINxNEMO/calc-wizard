# GUI
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

CalcWizard = QApplication([])

# Window Attributes
window = QMainWindow()
window.setWindowTitle('CalcWizard')
window.setGeometry(660, 60, 600, 960)
window.setFixedSize(600, 960)

# Font Attributes
# Main Label
mainLabelFont = QFont('Aptos')
mainLabelFont.setPixelSize(48)
mainLabelFont.setBold(True)

# Calculator Page Main Label
calculatorLabel = QLabel('CALCULATOR', window)
calculatorLabel.setFixedSize(540, 60)
calculatorLabel.move(30, 120)
calculatorLabel.setFont(mainLabelFont)
calculatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)


window.show()

CalcWizard.exec()