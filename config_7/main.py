"""
v.1.0.8
main_update: configuration system with memory
author: [
    'Herasimau Artsem',
    'Shaplavskiy Mikita'
]
group: 10701323
"""

import customtkinter as ctk
from tkinter import StringVar, Menu, messagebox, filedialog
from model import CalculatorModel
from view import CalculatorView
from controller import CalculatorController
import os
from PIL import Image, ImageTk
import pygame
import cv2
from pathlib import Path
import threading
import time
from config_manager import ConfigManager


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize configuration manager and load settings
        self.config_manager = ConfigManager()
        self.config_manager.load_config()
        
        # Apply initial configuration
        self.config_manager.apply_config(self)
        
        # Инициализация pygame для звука
        pygame.mixer.init()
        
        # Создаем компоненты MVC
        self.model = CalculatorModel()
        self.view = CalculatorView(self, self.config_manager.config)
        self.controller = CalculatorController(self.model, self.view)

        # Настраиваем обработчики событий
        self.view.set_button_handlers(self.controller.handle_button_click)
        
        # Создание меню
        self.create_menu()
        
        # Загрузка ресурсов
        self.load_resources()
        
        # Флаг для остановки видео
        self.stop_video = False
        
    def create_menu(self):
        menubar = Menu(self)
        
        # Меню File
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выйти", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        # Меню Resources
        resources_menu = Menu(menubar, tearoff=0)
        resources_menu.add_command(label="Покащать лого", command=self.show_image)
        resources_menu.add_command(label="Услышать голос разработчика", command=self.play_sound)
        resources_menu.add_command(label="поссмотреть туториал", command=self.show_video)
        menubar.add_cascade(label="Ресурсы", menu=resources_menu)
        
        # Меню Configuration
        config_menu = Menu(menubar, tearoff=0)
        config_menu.add_command(label="Загрузить конфигурацию", command=self.load_config_file)
        
        # Подменю для выбора типа интерфейса
        interface_menu = Menu(config_menu, tearoff=0)
        
        # Подменю для доступности
        accessibility_menu = Menu(interface_menu, tearoff=0)
        accessibility_menu.add_command(label="Высококонтрастный режим", 
                                      command=lambda: self.load_predefined_config("config_accessibility_high_contrast.json"))
        accessibility_menu.add_command(label="Светлый режим", 
                                      command=lambda: self.load_predefined_config("config_accessibility_light.json"))
        interface_menu.add_cascade(label="Доступность", menu=accessibility_menu)
        
        # Подменю для гендерного интерфейса
        gender_menu = Menu(interface_menu, tearoff=0)
        gender_menu.add_command(label="Мужской стиль", 
                               command=lambda: self.load_predefined_config("config_gender_male.json"))
        gender_menu.add_command(label="Женский стиль", 
                               command=lambda: self.load_predefined_config("config_gender_female.json"))
        interface_menu.add_cascade(label="Гендерный стиль", menu=gender_menu)
        
        # Подменю для возрастного интерфейса
        age_menu = Menu(interface_menu, tearoff=0)
        age_menu.add_command(label="Для детей", 
                            command=lambda: self.load_predefined_config("config_age_children.json"))
        age_menu.add_command(label="Для молодежи", 
                            command=lambda: self.load_predefined_config("config_age_youth.json"))
        age_menu.add_command(label="Для среднего возраста", 
                            command=lambda: self.load_predefined_config("config_age_middle.json"))
        age_menu.add_command(label="Для пожилых", 
                            command=lambda: self.load_predefined_config("config_age_elderly.json"))
        interface_menu.add_cascade(label="Возрастной стиль", menu=age_menu)
        
        config_menu.add_cascade(label="Тип интерфейса", menu=interface_menu)
        config_menu.add_command(label="Сбросить к настройкам по умолчанию", 
                               command=lambda: self.load_predefined_config("config.json"))
        
        menubar.add_cascade(label="Конфигурация", menu=config_menu)
        
        self.config(menu=menubar)
        
    def load_resources(self):
        # Пути к ресурсам
        self.resources_path = Path("resources")
        
        # Загрузка изображения (статический способ)
        try:
            self.image = Image.open(self.resources_path / "image.png")
            # Сохраняем оригинальный размер изображения
            self.original_image = self.image.copy()
            # Создаем уменьшенную версию для предпросмотра
            self.image.thumbnail((400, 400))
            self.photo = ImageTk.PhotoImage(self.image)
        except Exception as e:
            print(f"Could not load image: {str(e)}")
        
        # Загрузка звука (динамический способ)
        self.sound_file = str(self.resources_path / "sound.mp3")
        
        # Загрузка видео (динамический способ)
        self.video_file = str(self.resources_path / "video.mp4")
        
    def show_image(self):
        try:
            # Создаем новое окно для изображения
            image_window = ctk.CTkToplevel(self)
            image_window.title("Image Viewer")
            
            # Получаем размеры оригинального изображения
            width, height = self.original_image.size
            # Устанавливаем размер окна с учетом размеров изображения
            image_window.geometry(f"{width}x{height}")
            
            # Создаем фото из оригинального изображения
            photo = ImageTk.PhotoImage(self.original_image)
            
            # Отображение изображения
            label = ctk.CTkLabel(image_window, image=photo, text="")
            label.image = photo  # Сохраняем ссылку
            label.pack(padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Could not show image: {str(e)}")
        
    def play_sound(self):
        try:
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Error", f"Could not play sound: {str(e)}")
            
    def update_video_frame(self, cap, label, video_window):
        while not self.stop_video:
            ret, frame = cap.read()
            if ret:
                # Конвертация BGR в RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Конвертация в формат для tkinter
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                
                # Обновление изображения
                label.configure(image=frame)
                label.image = frame  # Сохраняем ссылку
                
                # Небольшая задержка для плавного воспроизведения
                time.sleep(1/30)  # 30 FPS
            else:
                # Если видео закончилось, начинаем сначала
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                
        cap.release()
            
    def show_video(self):
        try:
            cap = cv2.VideoCapture(self.video_file)
            if cap.isOpened():
                # Получаем размеры видео
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                # Создаем новое окно для видео
                video_window = ctk.CTkToplevel(self)
                video_window.title("Video Player")
                video_window.geometry(f"{width}x{height}")
                
                # Создаем метку для отображения видео
                label = ctk.CTkLabel(video_window, text="")
                label.pack(padx=10, pady=10)
                
                # Сбрасываем флаг остановки
                self.stop_video = False
                
                # Запускаем воспроизведение в отдельном потоке
                video_thread = threading.Thread(
                    target=self.update_video_frame,
                    args=(cap, label, video_window)
                )
                video_thread.daemon = True
                video_thread.start()
                
                # Обработчик закрытия окна
                def on_closing():
                    self.stop_video = True
                    video_window.destroy()
                
                video_window.protocol("WM_DELETE_WINDOW", on_closing)
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not play video: {str(e)}")
            
    def open_file(self):
        messagebox.showinfo("Уведомление", "Будет сделано позже, в следующей версии")
        
    def save_file(self):
        messagebox.showinfo("Уведомление","Будет сделано позже, в следующей версии")
        
    def load_config_file(self):
        """Load a custom configuration file."""
        try:
            file_path = filedialog.askopenfilename(
                title="Select Configuration File",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
            )
            
            if file_path:
                # Create a new config manager with the selected file
                temp_config_manager = ConfigManager(file_path)
                if temp_config_manager.load_config():
                    # If successful, update our config manager
                    self.config_manager = temp_config_manager
                    
                    # Apply the new configuration
                    self.apply_new_config()
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Error loading configuration: {str(e)}")
            
    def load_predefined_config(self, config_file):
        """Load a predefined configuration file."""
        try:
            # Get the directory of this script file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            configs_dir = os.path.join(base_dir, "configs")
            
            # Create a new config manager with the predefined file
            config_path = os.path.join(configs_dir, config_file)
            temp_config_manager = ConfigManager(config_path)
            if temp_config_manager.load_config():
                # If successful, update our config manager
                self.config_manager = temp_config_manager
                
                # Apply the new configuration
                self.apply_new_config()
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Error loading configuration: {str(e)}")
            
    def apply_new_config(self):
        """Apply new configuration immediately."""
        # Save current configuration for future use
        self.config_manager.save_config()
        
        # Apply the configuration to the window
        self.config_manager.apply_config(self)
        
        # Update the view with new configuration
        self.view.update_config(self.config_manager.config)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
