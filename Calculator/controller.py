class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_equation_mode_handler(self.handle_equation_mode_change)

    def handle_button_click(self, button_text):
        if button_text == "C":
            self.model.clear()
        elif button_text == "=":
            self.model.calculate()
        elif button_text in "+-*/":
            self.model.set_operation(button_text)
        else:
            self.model.append_digit(button_text)

        self.view.update_display(self.model.get_current_value())

    def handle_equation_mode_change(self, show_equation):
        self.model.toggle_equation_mode()
        self.view.update_display(self.model.get_current_value()) 