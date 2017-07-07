
class BindableProperty(property):
    def __init__(self, default_value=None, datatype=None, name=None):
        self.dtype = datatype
        self.name = name
        self.default_value = default_value
        self.bindings = []

        if default_value is not None:
            self.dtype = type(default_value)
        else:
            self.dtype = datatype or str

        def getter(this):
            return getattr(this, self.private_membername)

        def setter(this, val):
            setattr(this, self.private_membername, val)
            for binding in self.bindings:
                if binding.to_view and binding.source is this:
                    binding.var.set(val)

        super().__init__(getter, setter)

    @property
    def private_membername(self):
        return '__' + self.name
