from enum import Enum
from tkinter import ttk


class Action(Enum):
    DELETE = 0
    INSERT = 1


class NumericEntry(ttk.Entry):
    def __init__(self, *args, datatype: type=int, **kwargs):
        self.datatype = datatype
        super().__init__(*args, **kwargs)
        self.config(validate='key',
                    validatecommand=(self.register(self.on_validate), '%d', '%P'))

    def on_validate(self, action, text):
        if int(action) == Action.INSERT.value:
            try:
                self.datatype(text)
                return True
            except ValueError:
                return False
        else:
            return True
