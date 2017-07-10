import tkinter as tk
from tkpf import Component


class Window(Component):
    @classmethod
    def new_window(cls):
        window = tk.Toplevel() if cls._windows else tk.Tk()
        cls._windows.append(window)
        return window

    def __init__(self, model):
        super().__init__(self.new_window(), model)
        self.title = ''

    def show(self):
        self.parent.wm_title(self.title)
        self.root_widget.mainloop()
