"""
v.1.0.0
author: [
    'Gerasimov Artem',
    'Shaplavskiy Mikita'
]
group: 10701323
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ex_design import Ui_MainWindow  # Импортируйте сгенерированный класс


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.RezultEdit.setReadOnly(True)

        self.ui.pushButton_zero.clicked.connect(lambda x: self.write_text(self.ui.pushButton_zero.text()))
        self.ui.pushButton_1.clicked.connect(lambda x: self.write_text(self.ui.pushButton_1.text()))
        self.ui.pushButton_2.clicked.connect(lambda x: self.write_text(self.ui.pushButton_2.text()))
        self.ui.pushButton_3.clicked.connect(lambda x: self.write_text(self.ui.pushButton_3.text()))
        self.ui.pushButton_4.clicked.connect(lambda x: self.write_text(self.ui.pushButton_4.text()))
        self.ui.pushButton_5.clicked.connect(lambda x: self.write_text(self.ui.pushButton_5.text()))
        self.ui.pushButton_6.clicked.connect(lambda x: self.write_text(self.ui.pushButton_6.text()))
        self.ui.pushButton_7.clicked.connect(lambda x: self.write_text(self.ui.pushButton_7.text()))
        self.ui.pushButton_8.clicked.connect(lambda x: self.write_text(self.ui.pushButton_8.text()))
        self.ui.pushButton_9.clicked.connect(lambda x: self.write_text(self.ui.pushButton_9.text()))
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
