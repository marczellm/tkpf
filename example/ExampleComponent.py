from tkpf import Component


class ExampleComponent(Component):
    template = '<Label name="thelabel">Example component text</Label>'

    def config(self, **kwargs):
        self.thelabel.config(text=kwargs['custom-text'])
