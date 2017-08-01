from copy import copy
from abc import ABCMeta as Abstract, abstractmethod

from tkpf.Directive import Directive
from tkpf.Registry import Registry

class WidgetWrapper(Directive, metaclass=Abstract):
    def __init__(self, parent_widget, parent_directive,
                 model=None):
        super().__init__(parent_widget, parent_directive, model)
        self.root_widget = self.create(parent_widget)

    @abstractmethod
    def create(self, parent):
        pass

    def add_child(self, parent, classname, attrib, text=None):
        if text:
            attrib['text'] = text

        attr_dirs = {k: v for k, v in attrib.items() if k in Registry.attributes}
        attrib =  {k: v for k, v in attrib.items() if k not in Registry.attributes}
        directive, widget = self.inflate(parent, classname,
                                         widget_name=attrib.pop('name', None),
                                         attr_dirs)
        self.process_attributes(widget, self.resolve_bindings(widget, attrib))
        return directive, widget
