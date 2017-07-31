from tkpf.Directive import Directive
from tkpf.Registry import Registry


class Attribute(Directive):
    name = None

    @classmethod
    def __init_subclass__(cls):
        Registry.attributes[cls.name] = cls

    def __init__(self, value,
                 parent_widget=None, parent_directive=None):
        self.value = value
        self.hosting_widget = None
        self.hosting_directive = None
        self.parent_widget = parent_widget
        self.parent_directive = parent_directive

    def get(self):
        return self.hosting_directive, self.hosting_widget

    def kwargs(self):
        return {}
    

    
class TkpfModel(Attribute):
    name = 'tkpf-model'

    def kwargs(self):
        return {'model': getattr(self.parent_directive.model, self.value[1:-1])}

        
