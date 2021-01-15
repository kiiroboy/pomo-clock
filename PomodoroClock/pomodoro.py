import tkinter as tk
import time

class Application(tk.Frame):
    def __init__(self, master=None, dim="0x0"):
        super().__init__(master)
        self.master = master
        master.geometry(dim)
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        self.e1 = tk.Entry(self)
        self.e1.pack(side="top")
        self.e2 = tk.Entry(self)
        self.e2.pack(side="top")
        self.remaining = 500
        self.state = False

        self.start_button = tk.Button(self, text="start", command=self.start)
        self.start_button.pack(side="left")

        self.pause_button =  tk.Button(self, text="pause", command=self.pause)
        self.pause_button.pack(side="right")

        self.timer_label = tk.Label(self)

        self.timer_label["text"] = str(self.remaining)
        self.timer_label.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="RED",command=self.master.destroy)
        self.quit.pack(side="bottom")
    
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
dimension = "1000x1000"
app = Application(master=root, dim=dimension)
app.mainloop()




