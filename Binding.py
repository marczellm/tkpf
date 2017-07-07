import tkinter as tk
from tkpf import ViewModel, BindableProperty


_type_mapping = {
    int: tk.IntVar,
    str: tk.StringVar,
    bool: tk.BooleanVar,
    float: tk.DoubleVar
}


class Binding:
    def __init__(self,
                 source: ViewModel, source_prop: BindableProperty,
                 target: tk.Widget, target_prop: str,
                 to_model: bool, to_view: bool):
        self.source = source
        self.source_property = source_prop
        self.var = _type_mapping[source_prop.dtype]()
        self.target = target
        self.target_property = target_prop
        if source_prop.default_value is not None:
            self.var.set(source_prop.default_value)
        self.to_view = to_view
        self.to_model = to_model
        self.add_observer(self.observer)

    def add_observer(self, observer):
        """
        Register a callback to be called when the value of ``self.var`` changes.
        :param observer: a callable accepting one parameter. The new value will be passed in that.
        """
        self.var.trace_add('write', lambda *_: observer(self.safe_get()))

    def safe_get(self):
        try:
            return self.source_property.dtype(self.var.get())
        except tk.TclError:
            return self.source_property.dtype()

    def observer(self, val):
        if self.to_model:
            self.source_property.bindings.remove(self)
            self.source_property.fset(self.source, val)
            self.source_property.bindings.append(self)

