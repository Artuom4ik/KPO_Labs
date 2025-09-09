import customtkinter as ctk

from pottern.fabric import Fabric

class CalculatorUI:
    def __init__(self, root, result_var):
        self.root = root
        self.result_var = result_var
        self.create_widgets()

    def create_widgets(self):
        self.result_entry = ctk.CTkEntry(
            self.root,
            textvariable=self.result_var,
            font=("Segoe UI Black", 18),
            justify='right'
        )
        self.result_entry.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky='nsew',
            padx=10,
            pady=10
        )

        Fabric.button_fabric(self.root, ctk.CTkButton, self.result_var)#TODO: ПЕРЕСТИ РАСТАВЛЕНИЕ КНОПОК СЮДА



