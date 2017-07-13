class AutoProperty(property):
    def __init__(self, arg=str, name=None):
        self.name = name

        if isinstance(arg, type):
            self.dtype = arg
            self.default_value = None
        else:
            self.default_value = arg
            self.dtype = type(arg)

        def getter(this) -> self.dtype:
            return getattr(this, self.private_membername)

        def setter(this, val):
            setattr(this, self.private_membername, val)

        super().__init__(getter, setter)

    @property
    def private_membername(self):
        return '__' + self.name
