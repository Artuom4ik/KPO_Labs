from states import InitialState

class CalculatorModel:
    def __init__(self):
        self.current_value = "0"
        self.previous_value = None
        self.operation = None
        self.state = InitialState(self)

    def set_state(self, new_state):
        self.state = new_state

    def clear(self):
        self.current_value = "0"
        self.previous_value = None
        self.operation = None
        self.set_state(InitialState(self))

    def append_digit(self, digit):
        self.state.handle_digit(digit)

    def set_operation(self, operation):
        self.state.handle_operation(operation)

    def calculate(self):
        try:
            prev = float(self.previous_value)
            current = float(self.current_value)
            
            if self.operation == "+":
                result = prev + current
            elif self.operation == "-":
                result = prev - current
            elif self.operation == "*":
                result = prev * current
            elif self.operation == "/":
                if current == 0:
                    raise ZeroDivisionError
                result = prev / current
            else:
                return

            self.current_value = str(result)
            self.previous_value = None
            self.operation = None

        except (ValueError, ZeroDivisionError):
            self.current_value = "Error"
            self.clear()

    def get_current_value(self):
        return self.current_value 