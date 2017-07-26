from tkinter import filedialog
from tkpf import Window


class ExampleWindow(Window):
    template_path = 'example/ExampleWindow.yaml'

    def file_open(self):
        filedialog.askopenfilename()

    def do_stuff(self):
        print('Stuff')
