from tkpf import ViewModel, BindableProperty


class ExampleModel(ViewModel):
    choice = BindableProperty(int)
    available_suboptions = BindableProperty()
    selected_suboption = BindableProperty()
    numeric_value = BindableProperty(5)

    def __init__(self):
        super().__init__()
        self.available_suboptions = ('suboption1', 'suboption2')
