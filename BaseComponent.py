import copy
import os
import xml.etree.ElementTree as Xml

from typing import Union
import tkinter as tk
from tkinter import ttk
from warnings import warn

from .Binding import Binding
from .misc import path
from .ViewModel import ViewModel

_variable_counterparts = {
    ('Button', 'text'): 'textvariable',
    ('Checkbutton', 'text'): 'textvariable',
    ('Menubutton', 'text'): 'textvariable',
    ('RadioButton', 'text'): 'textvariable',
    ('Label', 'text'): 'textvariable',
    ('Message', 'text'): 'textvariable',
    ('Progressbar', 'value'): 'variable'
}


class BaseComponent:
    _widget_registry = copy.copy(tk.__dict__)
    _widget_registry.update(ttk.__dict__)
    _component_registry = {}
    _windows = []
    template = ''
    template_path = ''

    @classmethod
    def register(cls, component_class: type):
        name = component_class.__name__
        if issubclass(component_class, BaseComponent):
            if not cls.template and not cls.template_path:
                template_path = os.path.join(path, name + '.xml')
                if os.path.isfile(template_path):
                    cls.template_path = template_path
            cls._component_registry[name] = component_class
        elif issubclass(component_class, tk.Widget):
            cls._widget_registry[name] = component_class

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.register(cls)

    def __init__(self, parent, model: ViewModel=None, **kwargs):
        self.model = model  # type: ViewModel
        self.parent = parent
        self.named_widgets = {}
        self.root_widget = None
        self.bindings = {}
        tree = self.parsed_template()
        if isinstance(tree, Xml.ElementTree):
            tree = tree.getroot()
        if tree is not None:
            if isinstance(parent, tk.Wm):
                self.root_widget = self.construct(tree, parent)
            else:
                self.root_widget = tk.Frame(parent)
                self.construct(tree, self.root_widget)

    def __getattr__(self, item):
        if item in self.named_widgets:
            return self.named_widgets[item]
        else:
            raise AttributeError

    def parsed_template(self):
        if self.template:
            return Xml.fromstring(self.template)
        elif self.template_path:
            return Xml.parse(self.template_path)

    def construct(self, elem: Xml.Element, parent: Union[tk.Widget, tk.Wm]):
        if elem.tag in self._widget_registry:
            cls = self._widget_registry[elem.tag]
        else:
            cls = self._component_registry[elem.tag]

        widget_name = elem.attrib.pop('name', None)
        viewmodel_name = elem.attrib.pop('tkpf-model', None)
        viewmodel = getattr(self.model, viewmodel_name[1:-1]) if viewmodel_name else None
        component = cls(parent, name=widget_name, model=viewmodel)
        widget = component.root_widget if isinstance(component, BaseComponent) else component

        if 'tkpf-model' in elem.attrib:
            component.model = elem.attrib['tkpf-model'][1:-1]

        for child in elem:
            self.construct(child, widget)

        if widget_name:
            self.named_widgets[widget_name] = component

        if elem.text and elem.text.strip():
            elem.attrib['text'] = elem.text.strip()

        self.process_attributes(component, widget, elem.attrib)

        if any(ch.winfo_manager() == 'grid' for ch in widget.children.values()):
            columns = widget.grid_size()
            for i in range(columns[0]):
                widget.grid_columnconfigure(i, weight=1)

        return component

    def bind(self, widget, target_property, binding_expr) -> dict:
        to_view = False
        to_model = False
        if binding_expr.startswith('[') and binding_expr.endswith(']'):
            binding_expr = binding_expr[1:-1]
            to_view = True
        if binding_expr.startswith('(') and binding_expr.endswith(')'):
            binding_expr = binding_expr[1:-1]
            to_model = True
        source_property = getattr(type(self.model), binding_expr)
        binding = Binding(source=self.model, source_prop=source_property,
                          target=widget, target_prop=target_property,
                          to_model=to_model, to_view=to_view)

        # Unsubscribe previous binding
        binding_key = str(widget) + '.' + binding.target_property
        if binding_key in self.bindings:
            previous = self.bindings.pop(binding_key)
            previous.source_property.bindings.remove(previous)

        # Subscribe new binding
        self.bindings[binding_key] = binding
        source_property.bindings.append(binding)

        if 'variable' in target_property:
            return {target_property: binding.var}
        elif (type(widget).__name__, target_property) in _variable_counterparts:
            return {_variable_counterparts[(type(widget).__name__, target_property)]: binding.var,
                    target_property: None}
        else:
            if to_view:
                binding.add_observer(lambda val: widget.config(**{target_property: val}))
            if to_model:
                warn('Property "{}" is not a variable: binding back to model not supported'.format(target_property))
            return {target_property: getattr(self.model, binding_expr)}

    def process_attributes(self, component, widget, attrib: dict):
        for key, name in copy.copy(attrib).items():
            if 'command' in key:
                attrib[key] = getattr(self, name) if hasattr(self, name) else getattr(self.model, name)
            elif name.startswith('[') and name.endswith(']') or name.startswith('(') and name.endswith(')'):
                attrib.update(self.bind(widget, key, name))

        config_args = {k: v for k, v in attrib.items() if '-' not in k}
        pack_args = {k[5:]: v for k, v in attrib.items() if k.startswith('pack-')}
        grid_args = {k[5:]: v for k, v in attrib.items() if k.startswith('grid-')}
        place_args = {k[6:]: v for k, v in attrib.items() if k.startswith('place-')}
        custom_args = {k: v for k, v in attrib.items()
                       if '-' in k and not any(k.startswith(p) for p in ['tkpf-', 'grid-', 'pack-', 'place-'])}

        widget.config(**config_args)

        if grid_args:
            widget.grid(**grid_args)
        elif place_args:
            widget.place(**place_args)
        else:
            widget.pack(**pack_args)

        component.config(**custom_args)

    def config(self, **kwargs):
        pass
