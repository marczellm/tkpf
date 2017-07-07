from tkpf import BaseWindow


class ExampleWindow(BaseWindow):
    template_path = 'tkpf/example/ExampleWindow.xml'

    def do_stuff(self):
        self.combobox.config(state='disabled')
