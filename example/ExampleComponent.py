import sys
from tkpf import Component, Directive


class ExampleComponent(Component):
    template = '<Label name="thelabel">Example component text</Label>'

    def config(self, **kwargs):
        self.thelabel.config(text=kwargs['custom-text'])


if sys.version_info < (3,6):
    Directive.Registry.register(ExampleComponent)
