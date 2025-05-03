class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_button_click(self, button_text):
        if button_text == "C":
            self.model.state.handle_clear()
        elif button_text == "=":
            self.model.state.handle_equals()
        elif button_text in "+-*/":
            self.model.state.handle_operation(button_text)
        else:
            self.model.state.handle_digit(button_text)

        self.view.update_display(self.model.get_current_value()) 