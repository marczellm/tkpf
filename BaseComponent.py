import copy
import os
import xml.etree.ElementTree as Xml

from typing import Union
import tkinter as tk
from tkinter import ttk
from warnings import warn

from .Binding import Binding
from .ViewModel import ViewModel
from .OptionMenu import OptionMenu
from .misc import path

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
    _widget_registry['OptionMenu'] = OptionMenu
    _component_registry = {}
    _windows = []

    _counter = 0  # Unique ID for inclusion in the Tkinter name

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
        self.root_widget = self.create(parent, **kwargs)

    def create(self, parent, **_):
        """
        Parse the template string and construct the view hierarchy based on it.
        You can override this in a component if the component creates its view hierarchy in custom logic.

        :return: the root widget of the newly created view hierarchy
        """
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
        if elem.text and elem.text.strip():
            elem.attrib['text'] = elem.text.strip()

        component, widget = self.add_child(parent, elem.tag, elem.attrib)

        for child in elem:
            (component if isinstance(component, BaseComponent) else self).construct(child, widget)

        if any(ch.winfo_manager() == 'grid' for ch in widget.children.values()):
            columns = widget.grid_size()
            for i in range(columns[0]):
                widget.grid_columnconfigure(i, weight=1)

        return component

    def add_child(self, parent, classname, attrib):
        if classname in self._component_registry:
            cls = self._component_registry[classname]
        else:
            cls = self._widget_registry[classname]

        widget_name = attrib.pop('name', None)
        viewmodel_name = attrib.pop('tkpf-model', None)
        viewmodel = getattr(self.model, viewmodel_name[1:-1]) if viewmodel_name else None
        component = cls(parent, name=widget_name, model=viewmodel)
        widget = component.root_widget if isinstance(component, BaseComponent) else component

        if widget_name:
            self.named_widgets[widget_name] = component

        self.process_attributes(component, widget, attrib)

        return component, widget

    def bind(self, target_property, binding_expr,
             widget=None, widget_name=None, widget_classname=None, widget_config_method=None) -> dict:
        """
        Create a binding

        :param target_property: the name of the property that we're binding to
        :param binding_expr: the binding expression
        :param widget: the Tkinter object
        :param widget_name: the name of the Tkinter object
        :param widget_classname: the classname of the Tkinter object
        :param widget_config_method: the method that should be invoked by the binding in the case of a
        non-variable target property
        :return: a dictionary that should be passed to the config method to finally create the binding
        """
        to_view = False
        to_model = False
        if widget:
            widget_name = str(widget)
            widget_classname = type(widget).__name__
            widget_config_method = widget.config

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
        binding_key = widget_name + '.' + binding.target_property
        if binding_key in self.bindings:
            previous = self.bindings.pop(binding_key)
            previous.source_property.bindings.remove(previous)

        # Subscribe new binding
        self.bindings[binding_key] = binding
        source_property.bindings.append(binding)

        if 'variable' in target_property:
            return {target_property: binding.var}
        elif (widget_classname, target_property) in _variable_counterparts:
            return {_variable_counterparts[(widget_classname, target_property)]: binding.var,
                    target_property: None}
        else:
            if to_view:
                binding.add_observer(lambda val: widget_config_method(**{target_property: val}))
            if to_model:
                warn('Property "{}" is not a variable: binding back to model not supported'.format(target_property))
            return {target_property: getattr(self.model, binding_expr)}

    def process_attributes(self, component, widget, attrib):
        for key, name in copy.copy(attrib).items():
            if 'command' in key:
                attrib[key] = getattr(self, name) if hasattr(self, name) else getattr(self.model, name)
            elif name.startswith('[') and name.endswith(']') or name.startswith('(') and name.endswith(')'):
                attrib.update(self.bind(key, name, widget))

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
        elif not isinstance(widget, tk.Menu):
            widget.pack(**pack_args)

        component.config(**custom_args)

    def config(self, **kwargs):
        pass
