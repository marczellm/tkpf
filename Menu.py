import tkinter as tk
from tkpf import BaseComponent


class Menu(BaseComponent):
    """ Translates the XML hierarchy into proper method calls when constructing a menu """

    def __init__(self, *args, **kwargs):
        self.menu = None
        super().__init__(*args, **kwargs)

    def create(self, parent, **_):
        self.menu = tk.Menu(parent)
        parent.winfo_toplevel().config(menu=self.menu)
        return self.menu

    def add_child(self, parent, classname, attrib):
        self.menu.add(classname.lower(), **attrib)
        return None, self.menu
