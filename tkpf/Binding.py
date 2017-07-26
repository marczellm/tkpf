import tkinter as tk
from typing import Callable
from warnings import warn

from tkpf import Bindable
from tkpf.ViewModel import ViewModel

_type_mapping = {
    int: tk.IntVar,
    str: tk.StringVar,
    bool: tk.BooleanVar,
    float: tk.DoubleVar
}


class Binding:
    def __init__(self,
                 source: ViewModel, source_prop: Bindable,
                 target: tk.Widget, target_prop: str,
                 to_model: bool, to_view: bool,
                 config_method: Callable=None):
        self.source = source
        self.source_property = source_prop
        self.var = _type_mapping[source_prop.dtype]()
        self.target = target
        self.target_property = target_prop
        self.var.set(source_prop.fget(source))
        self.to_view = to_view
        self.to_model = to_model
        self._subscribe_to_var(self.notify_to_model)

        if 'variable' not in target_prop:
            if not config_method:
                config_method = target.config
            if to_view:
                self._subscribe_to_var(lambda val: config_method(**{target_prop: val}))
            if to_model:
                warn('Property "{}" is not a variable: binding back to model not supported'.format(target_prop))

    def _subscribe_to_var(self, observer):
        """
        Register a callback to be called when the value of ``self.var`` changes
        :param observer: a callable accepting one parameter. The new value will be passed in that.
        """
        if hasattr(self.var, 'trace_add'):
            self.var.trace_add('write', lambda *_: observer(self.safe_get()))
        else:
            self.var.trace('w', lambda *_: observer(self.safe_get()))

    def safe_get(self):
        try:
            return self.source_property.dtype(self.var.get())
        except tk.TclError:
            return self.source_property.dtype()

    def notify_to_model(self, val):
        if self.to_model:
            self.source_property.bindings.remove(self)
            self.source_property.fset(self.source, val)
            self.source_property.bindings.append(self)

    def notify_to_view(self, val, source):
        if self.to_view and self.source is source:
            self.var.set(val)

    @staticmethod
    def is_binding_expr(s):
        return isinstance(s, str) and (s.startswith('[') and s.endswith(']') or s.startswith('(') and s.endswith(')'))

