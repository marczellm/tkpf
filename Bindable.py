import typing


class Bindable(property):
    def __init__(self, *args):
        if len(args) == 1:
            wrapped_prop = args[0]
            super().__init__(wrapped_prop.fget, self.wrap_setter(wrapped_prop.fset), wrapped_prop.fdel)
            self.wrapped_property = wrapped_prop
            self.bindings = []
            self.dtype = typing.get_type_hints(wrapped_prop.fget)['return']
        else:
            super().__init__(*args)

    def notify_bindings(self, val, this):
        for binding in self.bindings:
            if binding.to_view and binding.source is this:
                binding.var.set(val)

    def wrap_setter(self, fset):
        def wrapped_setter(this, val):
            fset(this, val)
            self.notify_bindings(val, this)
        return wrapped_setter

    def setter(self, fset):
        ret = super().setter(self.wrap_setter(fset))
        ret.wrapped_property = self.wrapped_property
        ret.bindings = self.bindings
        ret.dtype = self.dtype
        return ret
