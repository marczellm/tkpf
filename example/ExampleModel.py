from tkpf import ViewModel, AutoProperty, Bindable


class ExampleComponentModel(ViewModel):
    custom_text = Bindable(AutoProperty('Custom model text'))


class ExampleModel(ViewModel):
    choice = Bindable(AutoProperty(int))
    dropdown_options = Bindable(AutoProperty())
    combobox_selected = Bindable(AutoProperty())
    optionmenu_selected = Bindable(AutoProperty())
    component_model = ExampleComponentModel()

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
        self.dropdown_options = ('suboption1', 'suboption2', 'suboption3')


