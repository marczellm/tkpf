import xml.etree.ElementTree as Xml
import yaml
from typing import Union
import tkinter as tk

from tkpf import Directive
from tkpf import parser

class Component(Directive.Structural):
    _counter = 0  # Unique ID for inclusion in the Tkinter name

    template = None
    template_path = None
    template_yaml = None

    def __init__(self, parent_widget, parent_directive, model=None, **_):
        super().__init__(parent_widget, parent_directive, model)
        self.bindings = {}

    def create(self, parent, **_):
        tree = self.parsed_template()
        if tree is not None:
            if isinstance(parent, tk.Wm):
                return self.construct(tree, parent)
            else:
                root_widget = tk.Frame(parent, name=type(self).__name__.lower() + str(self._counter))
                type(self)._counter += 1
                self.construct(tree, root_widget)
                return root_widget

    def parsed_template(self):
        if self.template:
            return parser.XmlWrapper(Xml.fromstring(self.template))
        elif self.template_yaml:            
            return parser.DictWrapper(yaml.load(self.template_yaml))
        elif self.template_path:
            if self.template_path.lower().endswith('.xml'):
                return parser.XmlWrapper(Xml.parse(self.template_path))
            elif self.template_path.lower().endswith('.yaml'):
                with open(self.template_path) as bf:
                    return yaml.load(bf)
        raise Exception('Component template not specified')

    def construct(self, elem, parent: Union[tk.Widget, tk.Wm]):
        ret = super().construct(elem, parent)

        if isinstance(ret, tk.Widget):
            if any(ch.winfo_manager() == 'grid' for ch in ret.children.values()):
                columns = ret.grid_size()
                for i in range(columns[0]):
                    ret.grid_columnconfigure(i, weight=1)

        return ret
