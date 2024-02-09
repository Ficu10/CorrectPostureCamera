import tkinter as tk
import cv2
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.selected_source = 0
        self.video_sources = self.detect_video_sources()

        self.vid = cv2.VideoCapture(self.selected_source)

        # Ramki dla widoków kamery i list rozwijanych
        self.left_frame = tk.Frame(window)
        self.left_frame.pack(side=tk.LEFT)
        self.right_frame = tk.Frame(window)
        self.right_frame.pack(side=tk.RIGHT)

        # Lewy widok kamery i lista rozwijana
        self.canvas_left = tk.Canvas(self.left_frame, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas_left.pack()
        self.create_dropdown(self.left_frame)

        # Prawy widok kamery i lista rozwijana
        self.canvas_right = tk.Canvas(self.right_frame, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas_right.pack()
        self.create_dropdown(self.right_frame)

        self.delay = 10
        self.update()

        self.window.mainloop()

    def create_dropdown(self, parent):
        # Tworzenie listy rozwijanej
        options = [f"Source {i}: {self.video_sources[i]}" for i in range(len(self.video_sources))]
        self.selected_source_var = tk.StringVar(parent)
        self.selected_source_var.set(options[0])  # Ustawienie domyślnej wartości
        dropdown = tk.OptionMenu(parent, self.selected_source_var, *options, command=self.change_source)
        dropdown.pack()

    def change_source(self, value):
        # Zmiana źródła kamery na wybrane przez użytkownika
        source_index = int(value.split(':')[0].split()[-1])
        self.selected_source = source_index

    def detect_video_sources(self):
        # Wykrywanie dostępnych źródeł wideo
        video_sources = []
        for i in range(10):  # Sprawdzamy pierwsze 10 potencjalnych źródeł wideo
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    video_sources.append(i)
            cap.release()
        return video_sources

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo_left = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas_left.create_image(0, 0, image=self.photo_left, anchor=tk.NW)

            self.photo_right = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas_right.create_image(0, 0, image=self.photo_right, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Użycie klasy do utworzenia aplikacji
CameraApp(tk.Tk(), "Aplikacja z kamerą")
