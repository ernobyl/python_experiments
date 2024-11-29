import tkinter as tk
import time
from math import cos, sin, pi
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime

class bar_clock(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.create_widgets()
        self.sunset_sunrise()
        self.update_clock()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=700, height=500, bg="black")
        self.canvas.pack(expand=True, fill="both")
        self.draw_clock()

    def sunset_sunrise(self):
        city = LocationInfo("Espoo", "Finland", "Europe/Helsinki", 60.205490, 24.655899)
        su = sun(city.observer, date=datetime.now())
        sunrise = su['sunrise']
        sunset = su['sunset']
        self.sunrise_hour = sunrise.hour + sunrise.minute / 60
        self.sunset_hour = sunset.hour + sunset.minute / 60

    def draw_clock(self):
        self.canvas.create_rectangle(0, 0, 600, 20, outline="white", width=2)
        self.canvas.create_rectangle(0, 30, 600, 50, outline="white", width=2)
        self.canvas.create_rectangle(0, 60, 600, 80, outline="white", width=2)

    def update_clock(self):
        self.canvas.delete("all")
        current_time = time.localtime()
        hours = current_time.tm_hour
        days = current_time.tm_wday
        current_week = current_time.tm_yday // 7
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        # Drawing the hourly meter
        for h in range(hours):
            x1 = h * (600 / 23)
            y1 = 20
            x2 = (h + 1) * (600 / 23)
            y2 = 40
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill="violet")

            if self.sunrise_hour <= h < self.sunrise_hour + 1:
                self.canvas.create_text(x1 + 5, 45, text="sunrise", font=("Helvetica", 8), fill="yellow")

            if self.sunset_hour <= h < self.sunset_hour + 1:
                self.canvas.create_text(x2 - 5, 45, text="sunset", font=("Helvetica", 8), fill="orange")

        self.canvas.create_text(7 * (600 / 23), 10, text="get up", font=("Helvetica", 11), fill="white")
        self.canvas.create_text(21 * (600 / 23), 10, text="go to sleep", font=("Helvetica", 11), fill="white")

        self.canvas.create_rectangle(0, 0, 600, 120, outline="white", width=2)

        # Draw the minutes bar
        for m in range(minutes):
            x1 = m * (600 / 59)
            y1 = 60
            x2 = (m + 1) * (600 / 59)
            y2 = 80
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="magenta", width=2)

        # Draw the seconds bar
        for s in range(seconds):
            x1 = s * (600 / 59)
            y1 = 100
            x2 = (s + 1) * (600 / 59)
            y2 = 120
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="purple", width=2)

        # Drawing days of the week
        for d in range(7):
            x1 = d * (600 / 7)
            y1 = 140
            x2 = (d + 1) * (600 / 7)
            y2 = 160

            fill_color = "grey" if d != days else "green"
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill=fill_color)

        # Drawing weeks of the year
        for w in range(53):
            x1 = w * (592 / 52)
            y1 = 180
            x2 = (w + 1) * (592 / 52)
            y2 = 200
            fill_color = "grey" if w != current_week else "blue"
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill=fill_color)

        # Call update_clock every 1000ms (1 second)
        self.after(1000, self.update_clock)

class ClockApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Clock App")
        self.geometry("700x500")

        self.clock_frame = None
        self.create_widgets()

    def create_widgets(self):
        self.digital_button = tk.Button(self, text="Whatever Clock", command=self.show_bar_clock)
        self.digital_button.pack()

    def show_bar_clock(self):
        if self.clock_frame:
            self.clock_frame.destroy()
        self.clock_frame = bar_clock(self)
        self.clock_frame.pack()

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()

# how about planning?
# holiday mode: remove seconds, remove "get up, go to sleep"
# logging work?