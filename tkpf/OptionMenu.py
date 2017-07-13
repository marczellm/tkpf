from tkinter import ttk


class OptionMenu(ttk.OptionMenu):
    """ The role of this OptionMenu subclass is just to standardize the API so that it can be used
    uniformly from other code. """

    def __init__(self, parent, **kwargs):
        kw = {k: v for k, v in kwargs.items() if k not in {'name', 'model'}}
        super().__init__(parent, None, **kw)

    def config(self, values=list(), variable=None, **kwargs):
        if variable:
            self._variable = variable
            kwargs['textvariable'] = variable
        if values:
            self.set_menu(values[0], *values)
        super().config(**kwargs)
