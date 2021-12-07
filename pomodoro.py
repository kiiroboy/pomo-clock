import tkinter as tk
import time
import threading
import sys
import pygame
from configparser import ConfigParser


class Application(tk.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack(anchor=tk.CENTER, expand=1, fill=tk.BOTH)

        # init variables
        self.modes = {}
        self.config_parsing()
        self.curr_timer = None
        self.remaining = self.modes["pomodoro"]*60
        self.timer_paused = False
        pygame.init()
        self.mixer = pygame.mixer
        self.thread_running = False
        self.create_widgets() 

    def create_widgets(self):
        # StringVar for radio_buttons
        self.timer_var = tk.StringVar()
        self.timer_var.set("pomodoro")

        # TOP FRAME
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(anchor=tk.CENTER, side=tk.TOP, fill=tk.BOTH, expand=1)

        # Display current time
        self.clock_text = tk.Label(self.top_frame, text="00:00:00", font=("", 10), bg="black", fg="white")
        self.clock_text.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.clock_f()
        
        # Timer Mode
        self.main_mode = tk.Radiobutton(self.top_frame, text="Working", variable=self.timer_var, value="pomodoro",
                                        indicatoron=0, command=self.start_timer)
        self.main_mode.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.short_mode = tk.Radiobutton(self.top_frame, text="Short Break", variable=self.timer_var, value="short",
                                         indicatoron=0, command=self.start_timer)
        self.short_mode.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.long_mode = tk.Radiobutton(self.top_frame, text="Long Break", variable=self.timer_var, value="long",
                                        indicatoron=0, command=self.start_timer)
        self.long_mode.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.radio_buttons = [self.main_mode, self.short_mode, self.long_mode]
        self.disabled_when_selected(self.timer_var.get())

        # MIDDLE FRAME
        self.middle_frame = tk.Frame(self)
        self.middle_frame.pack(anchor=tk.CENTER, side=tk.TOP, fill=tk.BOTH, expand=1)

        # Timer text
        minute, second = divmod(self.remaining, 60)
        hour, minute = divmod(minute, 60) 
        time_format = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
        self.timer_text = tk.Label(self.middle_frame, text=time_format, font=("", 55))
        self.timer_text.config(bg="gray")
        self.timer_text.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Start button
        self.timer_start = tk.Button(self.middle_frame, text="Start", command=self.start, font=("", 30))
        self.timer_start.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Pause button
        self.timer_pause = tk.Button(self.middle_frame, text="Pause", command=self.pause, font=("", 30))
        self.timer_pause.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Reset button
        self.timer_pause = tk.Button(self.middle_frame, text="Reset", command=self.reset, font=("", 30))
        self.timer_pause.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # SECOND FRAME
        self.second_frame = tk.Frame(self)
        self.second_frame.pack(anchor=tk.CENTER, side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        
        # setting button
        self.setting = tk.Button(self.second_frame, text="Settings", command=self.open_setting_window, font=("", 20))
        self.setting.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # quit button
        self.quit = tk.Button(self.second_frame, text="Quit", fg="red", command=self.master.destroy, font=("", 10))
        self.quit.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def config_parsing(self):
        config = ConfigParser()
        config.read('config.ini')
        self.modes['pomodoro'] = int(config['time']['pomodoro_time'])
        self.modes['long'] = int(config['time']['long_time'])
        self.modes['short'] = int(config['time']['short_time'])

    def save_config(self):
        config = ConfigParser()
        config.read('config.ini')
        config.set('time', 'pomodoro_time', str(self.modes['pomodoro']))
        config.set('time', 'short_time', str(self.modes['short']))
        config.set('time', 'long_time', str(self.modes['long']))
        with open('config.ini', 'w') as cf:
            config.write(cf)

    def disabled_when_selected(self, mode):
        for i in self.radio_buttons:
            if i['value'] == mode:
                i['state'] = 'disabled'
            else:
                i['state'] = 'normal'

    def open_setting_window(self):
        self.timer_paused = True

        setting_window = tk.Toplevel(self)
        setting_window.geometry("400x300+10+10")
        setting_window.resizable(0, 0)
        setting_window.grab_set()

        def save():

            self.modes['pomodoro'] = int(setting_window.working_entry.get())
            self.modes['long'] = int(setting_window.long_entry.get())
            self.modes['short'] = int(setting_window.short_entry.get())
            self.remaining = self.modes[self.timer_var.get()] * 60
            self.save_config()
            self.reset()
            minute, second = divmod(self.remaining, 60)
            hour, minute = divmod(minute, 60)
            time_format = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
            app.timer_text.config(text=time_format)
            setting_window.destroy()

        # Working Label and Entry
        setting_window.working_label = tk.Label(setting_window, text="Working time (in minutes)")
        setting_window.working_label.place(x=10, y=30)
        setting_window.pomodoro_val = tk.StringVar(setting_window, value=str(self.modes['pomodoro']))
        setting_window.working_entry = tk.Entry(setting_window, textvariable=setting_window.pomodoro_val)
        setting_window.working_entry.place(x=10, y=50)

        # Short Label and Entry
        setting_window.short_label = tk.Label(setting_window, text="Short Break time (in minutes)")
        setting_window.short_label.place(x=10, y=80)
        setting_window.short_val = tk.StringVar(setting_window, value=str(self.modes['short']))
        setting_window.short_entry = tk.Entry(setting_window, textvariable=setting_window.short_val)
        setting_window.short_entry.place(x=10, y=100)

        # Long Label and Entry
        setting_window.long_label = tk.Label(setting_window, text="Long Break time (in minutes)")
        setting_window.long_label.place(x=10, y=130)
        setting_window.long_val = tk.StringVar(setting_window, value=str(self.modes['long']))
        setting_window.long_entry = tk.Entry(setting_window, textvariable=setting_window.long_val)
        setting_window.long_entry.place(x=10, y=150)

        # Save button
        setting_window.save_button = tk.Button(setting_window, text="Save", command=save)
        setting_window.save_button.place(x=170, y=200)

    def start(self):
        self.timer_paused = False
        if self.curr_timer is None:
            self.timer_f(self.remaining)

    def pause(self):
        if self.curr_timer is not None:
            self.timer_paused = True

    def reset(self):
        if self.curr_timer is not None:
            self.master.after_cancel(self.curr_timer)
            self.curr_timer = None
            self.timer_paused = False
            self.timer_f(self.remaining)
            self.timer_paused = True
            self.thread_running = False

    def start_timer(self):
        self.thread_running = False
        mode = self.timer_var.get()
        self.disabled_when_selected(mode)
        if self.curr_timer is not None:
            self.master.after_cancel(self.curr_timer)
        self.timer_paused = False
        self.timer_f(self.modes[mode]*60)
        self.timer_paused = True

    def clock_f(self):
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        self.clock_text.config(text=hour + ":" + minute + ":" + second)
        self.master.after(1000, self.clock_f)

    def thread_music_stop(self, after=5):
        while after >= 0:
            if not self.thread_running:
                break
            time.sleep(1)
            after -= 1
        self.mixer.music.stop()

    def timer_f(self, seconds, started=True):
        if seconds >= 0:
            if started:
                self.remaining = seconds
            if self.timer_paused:
                self.curr_timer = self.master.after(1000, self.timer_f, seconds, False)
            else:
                minute, second = divmod(seconds, 60)
                hour, minute = divmod(minute, 60) 
                time_format = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
                app.timer_text.config(text=time_format)
                self.curr_timer = self.master.after(1000, self.timer_f, seconds - 1, False)
        else:
            self.timer_paused = True
            self.mixer.music.load('sounds/default.ogg')
            self.mixer.music.play()

            thread = threading.Thread(target=lambda: self.thread_music_stop(after=7))
            thread.daemon = True
            self.thread_running = True
            thread.start()


root = tk.Tk()
root.title("PomodoroClock")
app = Application(master=root)
app.mainloop()
