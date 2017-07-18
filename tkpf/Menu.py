import sys
import functools
import tkinter as tk
from warnings import warn

from tkpf import Directive


class Menu(Directive.Structural):
    """ Translates the XML hierarchy into proper method calls when constructing a menu """

    def create(self, parent):
        menu = tk.Menu(parent)
        if not isinstance(parent, tk.Menu):
            parent.winfo_toplevel().config(menu=menu)
        return menu

    def add_child(self, parent, classname, attrib, text=None):
        name = attrib.pop('name', None)
        if text:
            attrib['label'] = text
        if classname == 'Menu':
            directive, widget = super().inflate(parent, classname)
            widget.config(tearoff=0)
            self.root_widget.add_cascade(menu=widget, **self.resolve_bindings(widget, attrib))
            self.named_widgets[name] = directive or widget
            return directive, widget
        else:
            last = 1 + (self.root_widget.index('end') or 0)
            pseudo_name = str(self.root_widget) + '.Tkpf_menuitem:' + str(last)
            config_method = functools.partial(self.root_widget.entryconfig, last)
            self.root_widget.add(classname.lower(), **self.resolve_bindings(None, attrib,
                                                                            widget_name=pseudo_name,
                                                                            widget_config_method=config_method))
            if name:
                warn('Menu items cannot be named')
            return None, self.root_widget

    @property
    def named_widgets(self):
        return self.parent_directive.named_widgets


if sys.version_info < (3, 6):
    Directive.Registry.register(Menu)
