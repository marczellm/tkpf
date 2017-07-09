from .BaseComponent import BaseComponent
from .BaseWindow import BaseWindow
from .AutoProperty import AutoProperty
from tkpf.Bindable import Bindable
from .Binding import Binding
from .ViewModel import ViewModel
from .NumericEntry import NumericEntry
from .misc import path
from .Menu import Menu as _Menu

BaseComponent.register(NumericEntry)
