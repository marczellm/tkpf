from copy import copy
from typing import Union
import xml.etree.ElementTree as Xml
import tkinter as tk
from tkinter import ttk

from .Binding import Binding
from .NumericEntry import NumericEntry
from .OptionMenu import OptionMenu


_variable_counterparts = {
    ('Button', 'text'): 'textvariable',
    ('Checkbutton', 'text'): 'textvariable',
    ('Menubutton', 'text'): 'textvariable',
    ('RadioButton', 'text'): 'textvariable',
    ('Label', 'text'): 'textvariable',
    ('Message', 'text'): 'textvariable',
    ('Progressbar', 'value'): 'variable'
}


class Registry:
    widgets = copy(tk.__dict__)
    widgets.update(ttk.__dict__)
    widgets.update({'NumericEntry': NumericEntry, 'OptionMenu': OptionMenu})
    directives = {}

    @classmethod
    def register(cls, typ: type):
        name = typ.__name__
        if issubclass(typ, Directive):
            cls.directives[name] = typ
        elif issubclass(cls, tk.Widget):
            cls.widgets[name] = typ


class Directive:
    pass


class Structural(Directive):
    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        Registry.register(cls)

    def __init__(self, parent, model=None):
        self.parent = parent
        self.model = model
        self.bindings = {}
        self.named_widgets = {}
        self.root_widget = self.create(parent)

    def __getattr__(self, item):
        if item in self.named_widgets:
            return self.named_widgets[item]
        else:
            raise AttributeError

    def create(self, parent):
        """ Create the view hierarchy.

        :return: the root widget of the newly created view hierarchy
        """

    def construct(self, elem: Xml.Element, parent: Union[tk.Widget, tk.Wm]):
        """
        Given an XML tree and a parent widget, construct the view hierarchy described in the XML,
        with the given widget as its parent

        :param elem: the XML element
        :param parent: the parent widget
        :return: the newly constructed view hierarchy, in the form of its root widget or directive
        """

        if elem.text and elem.text.strip():
            elem.attrib['text'] = elem.text.strip()

        directive, widget = self.add_child(parent, elem.tag, elem.attrib)

        for child in elem:
            (directive or self).construct(child, widget)

        return directive or widget

    def add_child(self, parent, classname, attrib) -> tuple:
        """ This method gets called when, during XML tree traversal, this directive contains a child element.
        This method should decide what to do with that child, and return (if applicable)
        the root directive and root widget resulting from that decision

        :param parent:
        :param classname:
        :param attrib:
        :return:
        """

    def inflate(self, parent, classname, widget_name=None, viewmodel_expr=None):
        """ Find and instantiate one widget or directive class, attaching it to the given widget as parent """

        if classname in Registry.directives:
            if viewmodel_expr:
                viewmodel = getattr(self.model, viewmodel_expr[1:-1])
            else:
                viewmodel = self.model

            cls = Registry.directives[classname]
            component = cls(parent, model=viewmodel)
            widget = component.root_widget
        else:
            cls = Registry.widgets[classname]
            widget = cls(parent, name=widget_name)
            component = None

        if widget_name:
            self.named_widgets[widget_name] = component or widget

        return component, widget

    def process_attributes(self, widget, attrib):
        for key, name in copy(attrib).items():
            if 'command' in key:
                attrib[key] = getattr(self, name) if hasattr(self, name) else getattr(self.model, name)
            elif name.startswith('[') and name.endswith(']') or name.startswith('(') and name.endswith(')'):
                attrib.update(self.bind(key, name, widget))

        config_args = {k: v for k, v in attrib.items() if '-' not in k}
        pack_args = {k[5:]: v for k, v in attrib.items() if k.startswith('pack-')}
        grid_args = {k[5:]: v for k, v in attrib.items() if k.startswith('grid-')}
        place_args = {k[6:]: v for k, v in attrib.items() if k.startswith('place-')}

        widget.config(**config_args)

        if grid_args:
            widget.grid(**grid_args)
        elif place_args:
            widget.place(**place_args)
        elif not isinstance(widget, tk.Menu):
            widget.pack(**pack_args)

    def bind(self, target_property, binding_expr,
             widget=None, widget_name=None,
             widget_classname=None, widget_config_method=None) -> dict:
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
            widget_classname = type(widget).__name__
            if not widget_name:
                widget_name = str(widget)

        if binding_expr.startswith('[') and binding_expr.endswith(']'):
            binding_expr = binding_expr[1:-1]
            to_view = True
        if binding_expr.startswith('(') and binding_expr.endswith(')'):
            binding_expr = binding_expr[1:-1]
            to_model = True
        source_property = getattr(type(self.model), binding_expr)
        original_target = None
        if (widget_classname, target_property) in _variable_counterparts:
            original_target = target_property
            target_property = _variable_counterparts[widget_classname, target_property]
        binding = Binding(source=self.model, source_prop=source_property,
                          target=widget, target_prop=target_property,
                          to_model=to_model, to_view=to_view,
                          config_method=widget_config_method)

        # Unsubscribe previous binding
        binding_key = widget_name + '.' + binding.target_property
        if binding_key in self.bindings:
            previous = self.bindings.pop(binding_key)
            previous.source_property.bindings.remove(previous)

        # Subscribe new binding
        self.bindings[binding_key] = binding
        source_property.bindings.append(binding)

        if 'variable' in target_property:
            ret = {target_property: binding.var}
            if original_target:
                ret[original_target] = None
            return ret
        else:
            return {target_property: getattr(self.model, binding_expr)}

    def config(self, **kwargs):
        pass
