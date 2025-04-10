"""
v.1.0.1
author: [
    'Gerasimov Artem',
    'Shaplavskiy Mikita'
]
group: 10701323
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
from ex_design import Ui_MainWindow  # Импортируйте сгенерированный класс


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.RezultEdit.setReadOnly(True)

        self.ui.pushButton_zero.clicked.connect(lambda x: self.write_text(self.ui.pushButton_zero.text()))

        for i in range(1, 10):
            eval(f"self.ui.pushButton_{i}.setGeometry(QtCore.QRect(100*((i-1)%3), 190 + 100*((i-1)//3), 100, 100))")

        for i in range(1,10):
            button = getattr(self.ui, f"pushButton_{i}")
            button.clicked.connect(lambda _, b=button: self.write_text(b.text()))

        self.ui.pushButton_plus.clicked.connect(lambda x: self.write_text(self.ui.pushButton_plus.text()))
        self.ui.pushButton_minus.clicked.connect(lambda x: self.write_text(self.ui.pushButton_minus.text()))
        self.ui.pushButton_mul.clicked.connect(lambda x: self.write_text("*"))
        self.ui.pushButton_div.clicked.connect(lambda x: self.write_text("/"))
        self.ui.pushButton_rezult.clicked.connect(self.write_rezult)
        self.ui.pushButton_clear.clicked.connect(self.clear_text)
        self.ui.pushButton_delete.clicked.connect(self.delete_last_sumbol)
        self.ui.pushButton_point.clicked.connect(lambda x: self.write_text("."))

    def write_text(self, text):
        self.ui.RezultEdit.setText(self.ui.RezultEdit.text() + text)

    def write_rezult(self):
        try:
            self.ui.RezultEdit.setText(str(eval(self.ui.RezultEdit.text())))
        except ZeroDivisionError:
            self.ui.RezultEdit.setText("Деление на ноль!")
        except Exception as e:
            self.ui.RezultEdit.setText("Неправильный ввод!")
            print(e) #отладка

    def delete_last_sumbol(self):
        self.ui.RezultEdit.setText(self.ui.RezultEdit.text()[:-1])

    def clear_text(self):
        self.ui.RezultEdit.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
