import tkinter as tk


class CustomButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg='green')
        self.grid()
        self.update_idletasks()
        print('On_Enter')

    def on_leave(self, e):
        self.configure(bg='white')
        self.grid()
        print('On_Leave')