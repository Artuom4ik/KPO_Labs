from states import InitialState
from operations import BasicOperation, LoggingDecorator, ValidationDecorator, RoundingDecorator


class CalculatorModel:
    def __init__(self):
        self.current_value = "0"
        self.previous_value = None
        self.operation = None
        self.state = InitialState(self)
        self.show_equation = False
        self.equation = "0"
        self.last_was_operation = False
        self._setup_operations()

    def _setup_operations(self):
        # Create decorated operations
        self.operations = {
            "+": RoundingDecorator(ValidationDecorator(LoggingDecorator(BasicOperation("+")))),
            "-": RoundingDecorator(ValidationDecorator(LoggingDecorator(BasicOperation("-")))),
            "*": RoundingDecorator(ValidationDecorator(LoggingDecorator(BasicOperation("*")))),
            "/": RoundingDecorator(ValidationDecorator(LoggingDecorator(BasicOperation("/"))))
        }

    def set_state(self, new_state):
        self.state = new_state

    def clear(self):
        self.current_value = "0"
        self.previous_value = None
        self.operation = None
        self.equation = "0"
        self.last_was_operation = False
        self.set_state(InitialState(self))

    def append_digit(self, digit):
        if self.show_equation:
            if self.equation == "0" or self.equation == "Error":
                self.equation = digit
            else:
                if self.last_was_operation:
                    self.equation += digit
                    self.last_was_operation = False
                else:
                    self.equation += digit
            self.current_value = self.equation
        else:
            self.state.handle_digit(digit)

    def set_operation(self, operation):
        if self.show_equation:
            if self.equation == "0" or self.equation == "Error":
                self.equation = "0"
            else:
                if not self.last_was_operation:
                    self.equation += f" {operation} "
                else:
                    # Если последним была операция, заменяем её
                    parts = self.equation.rsplit(" ", 2)
                    if len(parts) >= 2:
                        self.equation = parts[0] + f" {operation} "
            self.last_was_operation = True
            self.current_value = self.equation
        else:
            self.state.handle_operation(operation)

    def calculate(self):
        if self.show_equation:
            try:
                # Вычисляем всё уравнение
                result = eval(self.equation)
                self.equation = str(result)
                self.current_value = str(result)
                self.last_was_operation = False
            except:
                self.equation = "Error"
                self.current_value = "Error"
                self.clear()
        else:
            try:
                prev = float(self.previous_value)
                current = float(self.current_value)
                
                if self.operation in self.operations:
                    result = self.operations[self.operation].execute(prev, current)
                    self.current_value = str(result)
                    self.previous_value = None
                    self.operation = None
                else:
                    return

            except (ValueError, ZeroDivisionError):
                self.current_value = "Error"
                self.clear()

    def get_current_value(self):
        if self.show_equation:
            return self.equation
        return self.current_value

    def toggle_equation_mode(self):
        self.show_equation = not self.show_equation
        if self.show_equation:
            # При включении режима уравнения, показываем текущее состояние
            if self.operation is None:
                self.equation = self.current_value
            else:
                self.equation = f"{self.previous_value} {self.operation} {self.current_value}"
            self.current_value = self.equation
        else:
            self.equation = self.current_value
