import tkinter as tk


class CustomButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = 'green'
        print('On_Enter')

    def on_leave(self, e):
        self['bg'] = 'grey'
        print('On_Leave')