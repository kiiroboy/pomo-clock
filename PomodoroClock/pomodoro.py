import tkinter as tk
import time
#def timer_f(self):
#    if self.state == True:
#        if self.remaining <= 0:
#            print(self.timer_label)
#            self.timer_label.configure(text="time's up")
#        else:
#            self.timer_label.configure(text="%d" % self.remaining)
#            self.remaining = self.remaining - 1 
#            self.after(1000, self.timer_f)
#
#def start(self):
#    if self.state == False:
#        self.state = True
#        self.timer_f()
#
#def pause(self):
#    if self.state == True:
#        self.state = False
#        
class Main(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.display()
    def display(self):
        self.setting = tk.Button(self, text="Settings", command=lambda :self.open_setting_window())
        self.setting.pack()
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack()
    def open_setting_window(self):
        setting_window = tk.Toplevel(self)
        

root = tk.Tk()
app = Main(master=root)
app.mainloop()



