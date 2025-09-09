
class Fabric:
    @classmethod
    def button_fabric(cls, window, obj, result):
        buttons = [
            'C', '%', 'del', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '+-', '0', '.', '=',
        ]
        row_val = 1
        col_val = 0
        for button in buttons:
            b = obj(
                window,
                text=button,
                command=lambda x=button: cls.on_button_click(x, result),
                corner_radius=10,
                font=("Segoe UI Black", 18),
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
            window.grid_columnconfigure(i, weight=1)

        window.grid_rowconfigure(0, weight=1)

        for i in range(1, row_val):
            window.grid_rowconfigure(i, weight=1)

    @classmethod
    def on_button_click(cls,  char, result_var):
        if char == 'C':
            result_var.set("")
        elif char == '=':
            try:
                result = eval(result_var.get())
                result_var.set(result)
            except Exception:
                result_var.set("АЯ ЯЙ, ПАЛЬЦЫ КРИВЫЕ")
        elif char == 'del':
            result_var.set(result_var.get()[:-1])
        elif char == '+-':
            if result_var.get().startswith('-'):
                result_var.set(result_var.get()[1:])
            else:
                result_var.set('-' + result_var.get())
        else:
            result_var.set(result_var.get() + char)
