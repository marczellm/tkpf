from tkinter import filedialog
from tkpf import Window


class ExampleWindow(Window):
    template_path = 'tkpf/example/ExampleWindow.xml'

    def file_open(self):
        filedialog.askopenfile()