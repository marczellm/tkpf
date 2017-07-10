import xml.etree.ElementTree as Xml

from typing import Union
import tkinter as tk

from . import Directive


class Component(Directive.Structural):
    _windows = []
    _counter = 0  # Unique ID for inclusion in the Tkinter name

    template = None
    template_path = None

    def __init__(self, parent, model=None, **_):
        super().__init__(parent, model)
        self.bindings = {}

    def create(self, parent, **_):
        tree = self.parsed_template()
        if isinstance(tree, Xml.ElementTree):
            tree = tree.getroot()
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
            return Xml.fromstring(self.template)
        elif self.template_path:
            return Xml.parse(self.template_path)
        else:
            raise Exception('Component template not specified')

    def construct(self, elem: Xml.Element, parent: Union[tk.Widget, tk.Wm]):
        ret = super().construct(elem, parent)

        if isinstance(ret, tk.Widget):
            if any(ch.winfo_manager() == 'grid' for ch in ret.children.values()):
                columns = ret.grid_size()
                for i in range(columns[0]):
                    ret.grid_columnconfigure(i, weight=1)

        return ret

    def add_child(self, parent, classname, attrib):
        directive, widget = self.inflate(parent, classname,
                                         widget_name=attrib.pop('name', None),
                                         viewmodel_expr=attrib.pop('tkpf-model', None))
        self.process_attributes(widget, attrib)
        return directive, widget
