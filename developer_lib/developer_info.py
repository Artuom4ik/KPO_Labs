class DeveloperInfo:
    """
    Класс, предоставляющий информацию о разработчиках калькулятора.
    """
    
    @staticmethod
    def get_developers():
        """
        Возвращает список разработчиков, работавших над калькулятором.
        """
        return [
            'Herasimau Artsem',
            'Shaplavskiy Mikita'
        ]
    
    @staticmethod
    def get_group():
        """
        Возвращает номер группы разработчиков.
        """
        return '10701323'
    
    @staticmethod
    def get_version():
        """
        Возвращает текущую версию калькулятора.
        """
        return 'v.1.0.8'
    
    @staticmethod
    def get_project_description():
        """
        Возвращает описание проекта калькулятора.
        """
        return "Калькулятор с поддержкой сложных математических выражений, включая скобки и приоритет операций."
    
    @staticmethod
    def get_features():
        """
        Возвращает список реализованных в калькуляторе функций.
        """
        return [
            "Базовые арифметические операции (+, -, *, /)",
            "Сложные выражения с скобками",
            "Приоритет операций",
            "Настраиваемый интерфейс через конфигурационные файлы",
            "Поддержка различных пользовательских интерфейсов на основе доступности, пола и возраста",
            "Мультимедийные ресурсы (изображения, звуки, видео)"
        ]
    
    @staticmethod
    def get_about_text():
        """
        Возвращает форматированный текст о разработчиках с всей информацией.
        """
        developers = ", ".join(DeveloperInfo.get_developers())
        version = DeveloperInfo.get_version()
        group = DeveloperInfo.get_group()
        description = DeveloperInfo.get_project_description()
        
        about_text = f"""
        Калькулятор {version}
        
        Разработано: {developers}
        Группа: {group}
        
        {description}
        """
        
        return about_text
