import customtkinter as ctk
from tkinter import StringVar

class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.result_var = StringVar(value="0")
        self.create_ui()

    def create_ui(self):
        # Создаем чекбокс для режима отображения уравнения
        self.equation_mode_var = ctk.BooleanVar(value=False)
        self.equation_mode = ctk.CTkCheckBox(
            self.root,
            text="Показывать уравнение",
            variable=self.equation_mode_var,
            command=self.on_equation_mode_changed
        )
        self.equation_mode.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")

        # Создаем дисплей
        self.display = ctk.CTkEntry(
            self.root,
            textvariable=self.result_var,
            font=("Arial", 24),
            justify="right",
            state="readonly"
        )
        self.display.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Кнопки
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        self.buttons = {}
        for i, text in enumerate(buttons):
            row = i // 4 + 2  # Сдвигаем строки на 2 из-за чекбокса и дисплея
            col = i % 4
            self.buttons[text] = ctk.CTkButton(
                self.root,
                text=text,
                width=80,
                height=80,
                font=("Arial", 20)
            )
            self.buttons[text].grid(row=row, column=col, padx=5, pady=5)

        # Кнопка очистки
        self.clear_button = ctk.CTkButton(
            self.root,
            text="C",
            width=80,
            height=80,
            font=("Arial", 20)
        )
        self.clear_button.grid(row=7, column=0, columnspan=4, padx=5, pady=5)

        # Настройка сетки
        for i in range(8):  # Увеличиваем количество строк
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def set_button_handlers(self, handler):
        for text, button in self.buttons.items():
            button.configure(command=lambda t=text: handler(t))
        self.clear_button.configure(command=lambda: handler("C"))

    def update_display(self, value):
        self.result_var.set(value)

    def on_equation_mode_changed(self):
        self.equation_mode_handler(self.equation_mode_var.get())

    def set_equation_mode_handler(self, handler):
        self.equation_mode_handler = handler 