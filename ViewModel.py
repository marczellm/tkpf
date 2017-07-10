from .AutoProperty import AutoProperty
from .Bindable import Bindable


class ViewModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        for name, member in namespace.items():
            if isinstance(member, AutoProperty):
                member.name = name
            elif isinstance(member, Bindable) and isinstance(member.wrapped_property, AutoProperty):
                member.wrapped_property.name = name
        return super().__new__(mcs, name, bases, namespace)


class ViewModel(metaclass=ViewModelMeta):
    def __init__(self):
        super().__init__()

        for name, member in type(self).__dict__.items():
            if isinstance(member, AutoProperty):
                member.fset(self, member.default_value or member.dtype())
            elif isinstance(member, Bindable) and isinstance(member.wrapped_property, AutoProperty):
                member.fset(self, member.wrapped_property.default_value or member.dtype())
