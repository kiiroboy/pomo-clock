import tkinter as tk
import time
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor=tk.CENTER,expand=1,fill=tk.BOTH)
        self.master = master
        self.master.resizable(False, False)

        # state for clock and timer
        self.timer_state = False
        self.clock_state = True
        
        self.display()
        
    def display(self):
        
        # FIRST FRAME
        self.first_frame = tk.Frame(self)

        # text displaying the time 
        self.prime_text = tk.Label(self.first_frame, text="Testing", font=("",60))
        self.prime_text.config(bg="gray")
        self.prime_text.pack(side=tk.TOP, fill=tk.BOTH)

        # timer buttons
        self.timer_start = tk.Button(self.first_frame, text="Start", command=self.start, font=("",50))
        self.timer_start.pack(side=tk.LEFT)
        self.timer_pause = tk.Button(self.first_frame, text="Pause", command=self.pause, font=("",50))
        self.timer_pause.pack(side=tk.LEFT)

        # display the first_frame
        self.first_frame.pack(anchor=tk.CENTER, side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # SECOND FRAME
        self.second_frame = tk.Frame(self)
        
        # setting button
        self.setting = tk.Button(self.second_frame, text="Settings", command=self.open_setting_window, font=("",20))
        self.setting.pack(side=tk.TOP, fill=tk.BOTH)
        
        # quit button
        self.quit = tk.Button(self.second_frame, text="Quit", fg="red", command=self.master.destroy, font=("",20))
        self.quit.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # display the second_frame
        self.second_frame.pack(anchor=tk.CENTER, side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        # run the clock
        self.clock_f()

    def open_setting_window(self):
        setting_window = tk.Toplevel(self)
        setting_window.grab_set()

    def clock_f(self):
        if self.clock_state:
            hour  = time.strftime("%I")
            minute = time.strftime("%M")
            second = time.strftime("%S")
            self.prime_text.config(text=hour + ":" + minute + ":" + second)
            self.prime_text.after(1000, self.clock_f)
         
    def timer_f(self):
        if self.state == True:
            if self.remaining <= 0:
                print(self.timer_label)
                self.timer_label.configure(text="time's up")
            else:
                self.timer_label.configure(text="%d" % self.remaining)
                self.remaining = self.remaining - 1 
                self.after(1000, self.timer_f)
    
    def start(self):
        if self.state == False:
            self.state = True
            self.timer_f()
    
    def pause(self):
        if self.state == True:
            self.state = False
            

root = tk.Tk()
app = Application(master=root)
app.mainloop()



