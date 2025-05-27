from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class BasicOperation(Operation):
    def __init__(self, operation: str):
        self.operation = operation

    def execute(self, a: float, b: float) -> float:
        if self.operation == "+":
            return a + b
        elif self.operation == "-":
            return a - b
        elif self.operation == "*":
            return a * b
        elif self.operation == "/":
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        raise ValueError(f"Unknown operation: {self.operation}")

class OperationDecorator(Operation):
    def __init__(self, operation: Operation):
        self._operation = operation

    def execute(self, a: float, b: float) -> float:
        return self._operation.execute(a, b)

class LoggingDecorator(OperationDecorator):
    def execute(self, a: float, b: float) -> float:
        print(f"Performing operation with operands: {a} and {b}")
        result = super().execute(a, b)
        print(f"Result: {result}")
        return result

class ValidationDecorator(OperationDecorator):
    def execute(self, a: float, b: float) -> float:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Operands must be numbers")
        return super().execute(a, b)

class RoundingDecorator(OperationDecorator):
    def __init__(self, operation: Operation, decimals: int = 2):
        super().__init__(operation)
        self.decimals = decimals

    def execute(self, a: float, b: float) -> float:
        result = super().execute(a, b)
        return round(result, self.decimals)

class ExpressionEvaluator:
    def __init__(self):
        self.operations = {
            "+": RoundingDecorator(ValidationDecorator(LoggingDecorator(BasicOperation("+")))),
            "-": RoundingDecorator(ValidationDecorator(LoggingDecorator(BasicOperation("-")))),
            "*": RoundingDecorator(ValidationDecorator(LoggingDecorator(BasicOperation("*")))),
            "/": RoundingDecorator(ValidationDecorator(LoggingDecorator(BasicOperation("/"))))
        }
    
    def evaluate(self, expression: str) -> float:
        """
        Evaluates a mathematical expression string.
        Supports basic operations (+, -, *, /), parentheses, and follows order of operations.
        """
        try:
            # Using Python's built-in eval for expression evaluation
            # In a production environment, you might want to implement a custom parser
            # for security reasons
            result = eval(expression)
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def calculate(self, a: float, b: float, operation: str) -> float:
        """
        Performs a single calculation with two operands and an operation
        """
        if operation in self.operations:
            return self.operations[operation].execute(a, b)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
