import customtkinter as ctk


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

        buttons = [
            '(', ')', '%', '+',
            '7', '8', '9', 'C',
            '4', '5', '6', '/',
            '1', '2', '3', '*',
            '0', '.', '=', '-',
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            b = ctk.CTkButton(
                self.root,
                text=button,
                command=lambda x=button: self.on_button_click(x),
                font=("Segoe UI Black", 18)
            )
            b.grid(
                row=row_val,
                column=col_val,
                sticky='nsew',
                padx=5,
                pady=5,
                ipady=20
            )

            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

        self.root.grid_rowconfigure(0, weight=1)

        for i in range(1, row_val):
            self.root.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == 'C':
            self.result_var.set("")
        elif char == '=':
            try:
                result = eval(self.result_var.get())
                self.result_var.set(result)
            except Exception:
                ctk.CTkMessageBox.show_error("Error", "Invalid Input!")
                self.result_var.set("")
        else:
            self.result_var.set(self.result_var.get() + char)
