"""
v.1.0.6
main_update: ресурсы
author: [
    'Herasimau Artsem',
    'Shaplavskiy Mikita'
]
group: 10701323
"""

import customtkinter as ctk
from tkinter import StringVar, Menu, messagebox
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


class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x600")

        # Инициализация pygame для звука
        pygame.mixer.init()
        
        # Создаем компоненты MVC
        self.model = CalculatorModel()
        self.view = CalculatorView(self)
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


if __name__ == "__main__":
    ctk.set_appearance_mode("system")  # Установка темы
    ctk.set_default_color_theme("green")  # Установка цветовой темы
    app = Calculator()
    app.mainloop()
