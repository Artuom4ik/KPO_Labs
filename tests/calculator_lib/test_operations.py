import unittest
from calculator_lib.calculator import *
from io import StringIO
from unittest import mock

class TestBasicOperation(unittest.TestCase):
    """
    Класс для тестирования класса BasicOperation, который выполняет
    основные арифметические операции.
    """

    def test_addition(self):
        self.assertEqual(BasicOperation("+").execute(5, 3), 8)

    def test_subtraction(self):
        self.assertEqual(BasicOperation("-").execute(5, 3), 2)

    def test_multiplication(self):
        self.assertEqual(BasicOperation("*").execute(5, 3), 15)

    def test_division(self):
        self.assertEqual(BasicOperation("/").execute(10, 2), 5)

        with self.assertRaises(ZeroDivisionError):
            BasicOperation("/").execute(10, 0)

    def test_unsupported_operation(self):
        """Проверяем, что неподдерживаемая операция вызывает `ValueError`."""
        # Используем `assertRaises` для проверки, что попытка
        # использования операции "^" (возведение в степень)
        # приводит к `ValueError`.
        with self.assertRaises(ValueError):
            BasicOperation("^").execute(5, 3)


# ---
# Класс для проверки декораторов
# ---

class TestDecorators(unittest.TestCase):
    """
    Класс для тестирования различных декораторов, которые
    модифицируют поведение операций.
    """

    def test_logging_decorator(self):
        # Используем StringIO для захвата вывода
        captured_output = StringIO()

        # Создаем "внутренний" объект для декоратора
        add_op = BasicOperation("+")

        # Создаем декоратор
        log_add_op = LoggingDecorator(add_op)

        # Временное перенаправление вывода с помощью контекстного менеджера
        with unittest.mock.patch('sys.stdout', new=captured_output):
            # Выполняем операцию, и весь print-вывод пойдет в captured_output
            result = log_add_op.execute(5, 5)

        self.assertEqual(result, 10)

        output_value = captured_output.getvalue()

        # Проверяем, что в вывод попали нужные строки
        self.assertIn("Performing operation with operands: 5 and 5", output_value)
        self.assertIn("Result: 10", output_value)

    def test_validation_decorator(self):
        add_op = BasicOperation("+")

        # Создаем декоратор
        decorator = ValidationDecorator(add_op)

        with self.assertRaises(ValueError):
            decorator.execute("w", 3)

    def test_rounding_decorator(self):
        add_op = BasicOperation("+")

        # Создаем декоратор
        decorator = RoundingDecorator(add_op, 2)

        self.assertEqual(decorator.execute(2.522, 2), 4.52)





if __name__ == '__main__':
    # Эта конструкция гарантирует, что тесты запустятся только тогда,
    # когда скрипт будет выполнен напрямую, а не импортирован как модуль.
    unittest.main()