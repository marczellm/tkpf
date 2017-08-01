from copy import copy

import tkinter as tk
from tkinter import ttk

from tkpf.NumericEntry import NumericEntry
from tkpf.OptionMenu import OptionMenu


class Registry:
    widgets = copy(tk.__dict__)
    widgets.update(ttk.__dict__)
    widgets.update({'NumericEntry': NumericEntry, 'OptionMenu': OptionMenu})
    directives = {}
    attributes = {}

    @classmethod
    def register(cls, typ: type):
        from tkpf.Directive import Directive
        name = typ.__name__
        if issubclass(typ, Directive):
            if typ.attribute:
                cls.attributes[typ.attribute] = typ
            else:
                cls.directives[name] = typ
        elif issubclass(cls, tk.Widget):
            cls.widgets[name] = typ

