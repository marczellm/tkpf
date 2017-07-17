import tkinter as tk
from tkinter import ttk
from tkpf import Component

_windows = []


class Window(Component):
    @classmethod
    def new_window(cls):
        if _windows:
            window = tk.Toplevel()
        else:
            window = tk.Tk()
            window.style = ttk.Style()
            if window.style.theme_use() == 'default' and 'clam' in window.style.theme_names():
                window.style.theme_use('clam')

        _windows.append(window)
        return window

    def __init__(self, model):
        super().__init__(self.new_window(), None, model)
        self.title = ''

    def show(self):
        self.parent_widget.wm_title(self.title)
        self.root_widget.mainloop()
