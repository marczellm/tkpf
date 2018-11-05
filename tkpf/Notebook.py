import sys
from tkinter import ttk

from tkpf import Directive


class Notebook(Directive.Structural):
    def create(self, parent):
        if parent.tk.call('tk', 'windowingsystem') == 'aqua':
            s = ttk.Style()
            s.configure('TNotebook.Tab', padding=(12, 8, 12, 0))
        return ttk.Notebook(parent)

    def add_child(self, parent, classname, attrib, text=None):
        tab_args = {k[4:]: v for k, v in attrib.items() if k.startswith('tab-')}
        attrib = {k: v for k, v in attrib.items() if not k.startswith('tab-')}
        directive, widget = super().add_child(parent, classname, attrib, text)
        if parent is self.root_widget:
            self.root_widget.add(widget, **tab_args)
        return directive, widget

    @property
    def named_widgets(self):
        return self.parent_directive.named_widgets


if sys.version_info < (3, 6):
    Directive.Registry.register(Notebook)
