import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
import sys

class GifApp:
    def __init__(self, root, gif_path, speed=50):
        self.root = root
        self.root.title("GIF приложение")

        # Полноэкранный режим
        self.root.attributes("-fullscreen", True)

        # Канва на весь экран
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Загружаем гифку
        self.gif = Image.open(gif_path)
        self.frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA"))
                       for frame in ImageSequence.Iterator(self.gif)]

        self.frame_index = 0
        self.animation = None
        self.speed = speed  # скорость в мс (меньше = быстрее)
        self.animate()

        # Горячие клавиши выхода
        self.root.bind("<Control-q>", self.exit_app)  # Ctrl+Q
        self.root.bind("<Escape>", self.exit_app)     # Esc

    def animate(self):
        frame = self.frames[self.frame_index]
        self.canvas.delete("all")
        self.canvas.create_image(self.screen_width // 2, self.screen_height // 2,
                                 image=frame, anchor="center")
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.animation = self.root.after(self.speed, self.animate)

    def exit_app(self, event=None):
        if self.animation:
            self.root.after_cancel(self.animation)
        self.root.destroy()


if __name__ == "__main__":
    # Определяем папку, где лежит exe/py
    if getattr(sys, 'frozen', False):
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    gif_path = os.path.join(BASE_DIR, "cat.gif")  # ⚡ гифка рядом с exe

    root = tk.Tk()
    app = GifApp(root, gif_path, speed=50)  # speed=50 → быстрее (20 fps)
    root.mainloop()
