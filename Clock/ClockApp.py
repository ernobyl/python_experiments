import tkinter as tk
from tkinter import simpledialog
import time
from LocationHandler import get_user_location, get_sunrise_sunset

class BarClock(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")

        self.vacation_mode = False

        # Get the user's location
        self.location = simpledialog.askstring("Location Input", "Enter your city:")
        if not self.location:
            self.location = "Espoo"  # Default location if none is provided
        self.sun_data = get_sunrise_sunset(self.location)

        # Extract sunrise and sunset hours
        self.sunrise_hour = self.sun_data['sunrise'].hour + self.sun_data['sunrise'].minute / 60
        self.sunset_hour = self.sun_data['sunset'].hour + self.sun_data['sunset'].minute / 60

        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        # Frame to hold the canvas and the button separately
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(expand=True, fill="both")
        
        self.canvas = tk.Canvas(self.canvas_frame, width=700, height=300, bg="black")
        self.canvas.pack(expand=True, fill="both")

        # Vacation Mode Button at the bottom
        self.vacation_button_frame = tk.Frame(self)
        self.vacation_button_frame.pack(side="bottom", fill="x")
        self.vacation_button = tk.Button(self.vacation_button_frame, text="Vacation Mode", command=self.toggle_vacation_mode)
        self.vacation_button.pack(pady=10)

        self.draw_clock()
    
    def toggle_vacation_mode(self):
        self.vacation_mode = not self.vacation_mode
        self.update_clock()

    def draw_clock(self):
        # Draw static components of the clock
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

        # Hourly meter
        for h in range(24):
            x1 = h * (600 / 24)
            y1 = 20
            x2 = (h + 1) * (600 / 24)
            y2 = 40
            fill_color = "violet" if h <= hours else "#404040"
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill=fill_color)

            if self.sunrise_hour <= h < self.sunrise_hour + 1:
                self.canvas.create_text(x1 + (600 / 24) / 2, 10, text="sunrise", font=("Helvetica", 10), fill="yellow")

            if self.sunset_hour <= h < self.sunset_hour + 1:
                self.canvas.create_text(x1 + (600 / 24) / 2, 10, text="sunset", font=("Helvetica", 10), fill="orange")

        # Minutes bar
        for m in range(minutes):
            x1 = m * (600 / 59)
            y1 = 60
            x2 = (m + 1) * (600 / 59)
            y2 = 80
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="magenta", width=2)

        # Seconds bar
        if not self.vacation_mode:
            for s in range(seconds):
                x1 = s * (600 / 59)
                y1 = 100
                x2 = (s + 1) * (600 / 59)
                y2 = 120
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="purple", width=2)

        # Days of the week
        for d in range(7):
            x1 = d * (600 / 7)
            y1 = 140
            x2 = (d + 1) * (600 / 7)
            y2 = 160
            fill_color = "green" if d == days else "grey"
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill=fill_color)

        # Weeks of the year
        for w in range(53):
            x1 = w * (592 / 52)
            y1 = 180
            x2 = (w + 1) * (592 / 52)
            y2 = 200
            fill_color = "blue" if w == current_week else "grey"
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill=fill_color)

        self.after(1000, self.update_clock)

class ClockApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Clock App")
        self.geometry("700x500")

        self.clock_frame = None
        self.create_widgets()

    def create_widgets(self):
        self.digital_button = tk.Button(self, text="Bar Clock", command=self.show_bar_clock)
        self.digital_button.pack()

    def show_bar_clock(self):
        if self.clock_frame:
            self.clock_frame.destroy()
        self.clock_frame = BarClock(self)
        self.clock_frame.pack()
        self.digital_button.pack_forget()

if __name__ == "__main__":
    app = ClockApp()
    app.mainloop()

# how about planning?
# logging work?