from abc import ABC, abstractmethod

class CalculatorState(ABC):
    def __init__(self, context):
        self.context = context

    @abstractmethod
    def handle_digit(self, digit):
        pass

    @abstractmethod
    def handle_operation(self, operation):
        pass

    @abstractmethod
    def handle_equals(self):
        pass

    @abstractmethod
    def handle_clear(self):
        pass


class InitialState(CalculatorState):
    def handle_digit(self, digit):
        self.context.current_value = digit
        self.context.set_state(InputState(self.context))

    def handle_operation(self, operation):
        self.context.operation = operation
        self.context.set_state(OperationState(self.context))

    def handle_equals(self):
        pass

    def handle_clear(self):
        self.context.clear()


class InputState(CalculatorState):
    def handle_digit(self, digit):
        self.context.current_value += digit

    def handle_operation(self, operation):
        if self.context.operation and self.context.previous_value:
            self.context.calculate()
            self.context.previous_value = self.context.current_value
        else:
            self.context.previous_value = self.context.current_value
        
        self.context.operation = operation
        self.context.set_state(OperationState(self.context))

    def handle_equals(self):
        if self.context.operation and self.context.previous_value:
            self.context.calculate()
            self.context.set_state(ResultState(self.context))

    def handle_clear(self):
        self.context.clear()
        self.context.set_state(InitialState(self.context))


class OperationState(CalculatorState):
    def handle_digit(self, digit):
        self.context.current_value = digit
        self.context.set_state(InputState(self.context))

    def handle_operation(self, operation):
        self.context.operation = operation

    def handle_equals(self):
        if self.context.operation and self.context.previous_value:
            self.context.calculate()
            self.context.set_state(ResultState(self.context))

    def handle_clear(self):
        self.context.clear()
        self.context.set_state(InitialState(self.context))


class ResultState(CalculatorState):
    def handle_digit(self, digit):
        self.context.current_value = digit
        self.context.set_state(InputState(self.context))

    def handle_operation(self, operation):
        self.context.operation = operation
        self.context.set_state(OperationState(self.context))

    def handle_equals(self):
        if self.context.operation and self.context.previous_value:
            self.context.calculate()

    def handle_clear(self):
        self.context.clear()
        self.context.set_state(InitialState(self.context)) 