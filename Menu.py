import tkinter as tk
from . import Directive


class Menu(Directive.Structural):
    """ Translates the XML hierarchy into proper method calls when constructing a menu """

    def create(self, parent):
        menu = tk.Menu(parent)
        if not isinstance(parent, tk.Menu):
            parent.winfo_toplevel().config(menu=menu)
        return menu

    def add_child(self, parent, classname, attrib):
        if classname == 'Menu':
            component, widget = super().inflate(parent, classname)
            widget.config(tearoff=0)
            self.root_widget.add_cascade(menu=widget, **attrib)
            return component, widget
        else:
            self.root_widget.add(classname.lower(), **attrib)
        return None, self.root_widget
