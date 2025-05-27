import customtkinter as ctk
from tkinter import StringVar

class CalculatorView:
    def __init__(self, root, config=None):
        self.root = root
        self.result_var = StringVar(value="0")
        self.config = config
        self.create_ui()

    def create_ui(self):
        # Получаем значения из конфигурации или используем значения по умолчанию
        font_family = self.config["font"]["family"] if self.config else "Arial"
        font_size = self.config["font"]["size"] if self.config else 24
        button_font_size = self.config["font"]["button_size"] if self.config else 20
        button_color = self.config["appearance"]["button_color"] if self.config else None
        button_hover_color = self.config["appearance"]["button_hover_color"] if self.config else None
        text_color = self.config["appearance"]["text_color"] if self.config else None
        
        # Вычисляем размер кнопок на основе размера окна
        window_width = self.config["window"]["width"] if self.config else 400
        window_height = self.config["window"]["height"] if self.config else 600
        
        # Вычисляем размер кнопок (масштабируем с размером окна)
        button_width = max(80, int(window_width / 5))
        button_height = max(80, int(window_height / 8))
        
        # Создаем чекбокс для режима отображения уравнения
        self.equation_mode_var = ctk.BooleanVar(value=False)
        self.equation_mode = ctk.CTkCheckBox(
            self.root,
            text="Показывать уравнение",
            variable=self.equation_mode_var,
            command=self.on_equation_mode_changed,
            text_color=text_color,
            font=(font_family, int(button_font_size * 0.8))
        )
        self.equation_mode.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="w")

        # Создаем дисплей
        self.display = ctk.CTkEntry(
            self.root,
            textvariable=self.result_var,
            font=(font_family, font_size),
            justify="right",
            state="readonly",
            text_color=text_color
        )
        self.display.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Кнопки
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        self.buttons = {}
        for i, text in enumerate(buttons):
            row = i // 4 + 2  # Сдвигаем строки на 2 из-за чекбокса и дисплея
            col = i % 4
            self.buttons[text] = ctk.CTkButton(
                self.root,
                text=text,
                width=button_width,
                height=button_height,
                font=(font_family, button_font_size),
                fg_color=button_color,
                hover_color=button_hover_color,
                text_color=text_color
            )
            self.buttons[text].grid(row=row, column=col, padx=5, pady=5)

        # Кнопка очистки
        self.clear_button = ctk.CTkButton(
            self.root,
            text="C",
            width=button_width * 4 + 15,  # Width of all 4 buttons plus padding
            height=button_height,
            font=(font_family, button_font_size),
            fg_color=button_color,
            hover_color=button_hover_color,
            text_color=text_color
        )
        self.clear_button.grid(row=7, column=0, columnspan=4, padx=5, pady=5)

        # Настройка сетки
        for i in range(8):  # Увеличиваем количество строк
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def set_button_handlers(self, handler):
        for text, button in self.buttons.items():
            button.configure(command=lambda t=text: handler(t))
        self.clear_button.configure(command=lambda: handler("C"))

    def update_display(self, value):
        self.result_var.set(value)

    def on_equation_mode_changed(self):
        self.equation_mode_handler(self.equation_mode_var.get())

    def set_equation_mode_handler(self, handler):
        self.equation_mode_handler = handler
        
    def update_config(self, config):
        """Обновляем представление с новыми настройками конфигурации."""
        self.config = config
        
        # Обновляем шрифт и цвета для всех элементов
        font_family = config["font"]["family"]
        font_size = config["font"]["size"]
        button_font_size = config["font"]["button_size"]
        button_color = config["appearance"]["button_color"]
        button_hover_color = config["appearance"]["button_hover_color"]
        text_color = config["appearance"]["text_color"]
        
        # Вычисляем размер кнопок на основе размера окна
        window_width = config["window"]["width"]
        window_height = config["window"]["height"]
        
        # Вычисляем размер кнопок (масштабируем с размером окна)
        button_width = max(80, int(window_width / 5))
        button_height = max(80, int(window_height / 8))
        
        try:
            # Обновляем дисплей
            self.display.configure(
                font=(font_family, font_size),
                text_color=text_color
            )
            
            # Обновляем чекбокс для режима отображения уравнения
            self.equation_mode.configure(
                font=(font_family, int(button_font_size * 0.8)),
                text_color=text_color
            )
            
            # Обновляем все кнопки
            for button_text, button in self.buttons.items():
                button.configure(
                    font=(font_family, button_font_size),
                    fg_color=button_color,
                    hover_color=button_hover_color,
                    text_color=text_color,
                    width=button_width,
                    height=button_height
                )
                
            # Обновляем кнопку очистки
            self.clear_button.configure(
                font=(font_family, button_font_size),
                fg_color=button_color,
                hover_color=button_hover_color,
                text_color=text_color,
                width=button_width * 4 + 15,
                height=button_height
            )
            
            # Обновляем UI
            self.root.update_idletasks()
        except Exception as e:
            print(f"View: Ошибка при обновлении конфигурации: {str(e)}")
            import traceback
            traceback.print_exc() 