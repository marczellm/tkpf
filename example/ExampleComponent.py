from tkpf import BaseComponent


class ExampleComponent(BaseComponent):
    template = '<Label name="thelabel">Example component text</Label>'

    def config(self, **kwargs):
        self.thelabel.config(text=kwargs['custom-text'])
