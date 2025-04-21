"""
v.1.0.2
author: [
    'Herasimau Artsem',
    'Shaplavskiy Mikita'
]
group: 10701323
"""

import customtkinter as ctk
from tkinter import StringVar
from design import CalculatorUI


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x600")

        self.result_var = StringVar()
        self.ui = CalculatorUI(self, self.result_var)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # Установка темы
    ctk.set_default_color_theme("blue")  # Установка цветовой темы
    app = Calculator()
    app.mainloop()
