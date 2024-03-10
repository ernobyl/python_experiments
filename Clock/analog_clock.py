import tkinter as tk
import time
from math import cos, sin, pi
import requests
from bs4 import BeautifulSoup
import random

class analog_clock(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=400, bg="black")
        self.canvas.pack(expand=True, fill="both")
        self.draw_clock()

    def draw_clock(self):
        self.canvas.create_oval(50, 50, 350, 350, outline="purple", width=2)

        for i in range(12):
            angle = i * (2 * pi) / 12 - pi / 2
            x1 = 200 + 120 * cos(angle)
            y1 = 200 + 120 * sin(angle)
            x2 = 200 + 140 * cos(angle)
            y2 = 200 + 140 * sin(angle)
            if i == 0 or i % 3 == 0:
                self.canvas.create_line(x1, y1, x2, y2, fill="yellow", width=4)
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2)

        self.hour_hand = self.canvas.create_line(200, 200, 200, 270, width=5, fill="pink")
        self.minute_hand = self.canvas.create_line(200, 200, 200, 300, width=3, fill="magenta")
        self.second_hand = self.canvas.create_line(200, 200, 200, 320, width=2, fill="purple")

    def update_clock(self):

        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        hour_angle = (hours % 12 + minutes / 60) * (2 * pi) / 12 - pi / 2
        self.canvas.coords(self.hour_hand, 200, 200, 200 + 70 * cos(hour_angle), 200 + 70 * sin(hour_angle))

        minute_angle = (minutes + seconds / 60) * (2 * pi) / 60 - pi / 2
        self.canvas.coords(self.minute_hand, 200, 200, 200 + 100 * cos(minute_angle), 200 + 100 * sin(minute_angle))

        second_angle = (seconds % 60) * (2 * pi) / 60 - pi / 2
        self.canvas.coords(self.second_hand, 200, 200, 200 + 120 * cos(second_angle), 200 + 120 * sin(second_angle))

        self.after(1000, self.update_clock)

class digital_clock(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        self.time_label = tk.Label(self, font=("Helvetica", 48), bg="black", fg="white")
        self.time_label.pack()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_clock)

class bar_clock(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        self.canvas=tk.Canvas(self, width=700, height=500, bg="black")
        self.canvas.pack(expand=True, fill="both")
        self.draw_clock()

    def draw_clock(self):
        self.canvas.create_rectangle(0, 0, 600, 20, outline="white", width=2)
        self.canvas.create_rectangle(0, 30, 600, 50, outline="white", width=2)
        self.canvas.create_rectangle(0, 60, 600, 80, outline="white", width=2)

    def update_clock(self):
        self.canvas.delete("all")
        current_time = time.localtime()
        hours = current_time.tm_hour
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        for h in range(hours):
            x1 = h * (600 / 23)
            y1 = 20
            x2 = (h + 1) * (600 / 23)
            y2 = 40
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill="violet")

        self.canvas.create_text(7 * (600 / 23), 10, text="get up", font=("Helvetica", 11), fill="white")
        self.canvas.create_text(21 * (600 / 23), 10, text="go to sleep", font=("Helvetica", 11), fill="white")
        self.canvas.create_rectangle(0, 0, 600, 120, outline="white", width=2)

        for m in range(minutes):
            x1 = m * (600 / 59)
            y1 = 60
            x2 = (m + 1) * (600 / 59)
            y2 = 80
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="magenta", width=2)

        for s in range(seconds):
            x1 = s * (600 / 59)
            y1 = 100
            x2 = (s + 1) * (600 / 59)
            y2 = 120
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="purple", width=2)

        self.after(1000, self.update_clock)

class ClockApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Clock App")
        self.geometry("700x500")

        self.clock_frame = None
        self.create_widgets()

    def create_widgets(self):

        self.digital_button = tk.Button(self, text="Digital Clock", command=self.show_digital_clock)
        self.digital_button.pack()

        self.analog_button = tk.Button(self, text="Analog Clock", command=self.show_analog_clock)
        self.analog_button.pack()

        self.digital_button = tk.Button(self, text="Whatever Clock", command=self.show_bar_clock)
        self.digital_button.pack()

    def show_analog_clock(self):
        if self.clock_frame:
            self.clock_frame.destroy()
        self.clock_frame = analog_clock(self)
        self.clock_frame.pack()

    def show_digital_clock(self):
        if self.clock_frame:
            self.clock_frame.destroy()
        self.clock_frame = digital_clock(self)
        self.clock_frame.pack()

    def show_bar_clock(self):
        if self.clock_frame:
            self.clock_frame.destroy()
        self.clock_frame = bar_clock(self)
        self.clock_frame.pack()

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()