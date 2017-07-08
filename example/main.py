from tkpf.example.ExampleModel import ExampleModel
from tkpf.example.ExampleWindow import ExampleWindow
from tkpf.example.ExampleComponent import ExampleComponent  # because it is registered on import

ExampleWindow(ExampleModel()).show()
