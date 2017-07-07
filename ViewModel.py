from .BindableProperty import BindableProperty


class ViewModelMeta(type):
    def __new__(cls, name, bases, namespace):
        for name, member in namespace.items():
            if isinstance(member, BindableProperty):
                member.name = name
        return super().__new__(cls, name, bases, namespace)


class ViewModel(metaclass=ViewModelMeta):
    def __init__(self):
        super().__init__()

        for name, member in type(self).__dict__.items():
            if isinstance(member, BindableProperty):
                setattr(self, member.private_membername, member.default_value or member.dtype())
