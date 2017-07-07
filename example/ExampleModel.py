from tkpf import ViewModel, AutoProperty, Bindable


class ExampleModel(ViewModel):
    choice = Bindable(AutoProperty(int))
    available_suboptions = Bindable(AutoProperty())
    selected_suboption = Bindable(AutoProperty())

    @Bindable
    @property
    def numeric_value(self) -> int:
        return self.__num

    @numeric_value.setter
    def numeric_value(self, val):
        self.__num = val

    def __init__(self):
        super().__init__()
        self.__num = 5
        self.available_suboptions = ('suboption1', 'suboption2')
