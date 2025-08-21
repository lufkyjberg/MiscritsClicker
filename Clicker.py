import pyautogui
import time
import keyboard
import tkinter as tk
from threading import Thread

class AutoClicker:
    def __init__(self):
        self.running = False
        self.coordinates = []
        self.click_interval = 1.0
        
        self.root = tk.Tk()
        self.root.title("Автокликер по координатам")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Поле для ввода координат
        tk.Label(self.root, text="Координаты (x1,y1 x2,y2 ...):").pack(padx=10, pady=5)
        self.coords_entry = tk.Entry(self.root, width=50)
        self.coords_entry.pack(padx=10, pady=5)
        
        # Интервал
        tk.Label(self.root, text="Интервал (секунды):").pack(padx=10, pady=5)
        self.interval_entry = tk.Entry(self.root, width=10)
        self.interval_entry.insert(0, "1.0")
        self.interval_entry.pack(padx=10, pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="Старт", command=self.start_clicker, bg="green")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(btn_frame, text="Стоп", command=self.stop_clicker, bg="red", state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для получения текущих координат
        tk.Button(self.root, text="Получить текущие координаты", command=self.get_current_coords).pack(pady=5)
        
        # Статус
        self.status_label = tk.Label(self.root, text="Готов к работе", fg="blue")
        self.status_label.pack(pady=10)
        
    def get_current_coords(self):
        x, y = pyautogui.position()
        self.coords_entry.insert(tk.END, f" {x},{y}")
        self.status_label.config(text=f"Добавлены координаты: {x},{y}")
        
    def start_clicker(self):
        try:
            # Парсинг координат
            coords_text = self.coords_entry.get().strip()
            if not coords_text:
                self.status_label.config(text="Введите координаты!", fg="red")
                return
                
            self.coordinates = []
            for coord in coords_text.split():
                x, y = map(int, coord.split(','))
                self.coordinates.append((x, y))
                
            # Парсинг интервала
            self.click_interval = float(self.interval_entry.get())
            
            self.running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Работает...", fg="green")
            
            # Запуск в отдельном потоке
            self.thread = Thread(target=self.click_loop)
            self.thread.daemon = True
            self.thread.start()
            
        except Exception as e:
            self.status_label.config(text=f"Ошибка: {e}", fg="red")
            
    def stop_clicker(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Остановлено", fg="blue")
        
    def click_loop(self):
        try:
            while self.running:
                for x, y in self.coordinates:
                    if not self.running:
                        break
                        
                    pyautogui.click(x, y)
                    time.sleep(self.click_interval)
                    
        except Exception as e:
            self.status_label.config(text=f"Ошибка в потоке: {e}", fg="red")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    clicker = AutoClicker()
    clicker.run()