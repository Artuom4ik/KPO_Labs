class CalculatorModel:
    def __init__(self):
        self.current_value = "0"
        self.previous_value = None
        self.operation = None
        self.should_clear = False

    def clear(self):
        self.current_value = "0"
        self.previous_value = None
        self.operation = None
        self.should_clear = False

    def append_digit(self, digit):
        if self.should_clear:
            self.current_value = "0"
            self.should_clear = False
        if self.current_value == "0":
            self.current_value = digit
        else:
            self.current_value += digit

    def set_operation(self, operation):
        if self.operation is not None:
            self.calculate()
        self.previous_value = self.current_value
        self.operation = operation
        self.should_clear = True

    def calculate(self):
        if self.operation is None or self.previous_value is None:
            return

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
            self.should_clear = True

        except (ValueError, ZeroDivisionError):
            self.current_value = "Error"
            self.should_clear = True

    def get_current_value(self):
        return self.current_value 