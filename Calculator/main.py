"""
v.1.0.3
author: [
    'Herasimau Artsem',
    'Shaplavskiy Mikita'
]
group: 10701323
"""

import customtkinter as ctk
from tkinter import StringVar
from model import CalculatorModel
from view import CalculatorView
from controller import CalculatorController


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x600")

        # Создаем компоненты MVC
        self.model = CalculatorModel()
        self.view = CalculatorView(self)
        self.controller = CalculatorController(self.model, self.view)

        # Настраиваем обработчики событий
        self.view.set_button_handlers(self.controller.handle_button_click)


if __name__ == "__main__":
    ctk.set_appearance_mode("system")  # Установка темы
    ctk.set_default_color_theme("green")  # Установка цветовой темы
    app = Calculator()
    app.mainloop()
