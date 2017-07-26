import xml.etree.ElementTree as Xml


class XmlWrapper:
    def __init__(self, node):
        self.node = node

    @property
    def name(self):
        return self.node.tag

    @property
    def text(self):
        return self.node.text

    @property
    def children(self):
        return (XmlWrapper(x) for x in self.node)

    @property
    def attrib(self):
        return self.node.attrib


class DictWrapper:
    def __init__(self, name, dic):
        self.dic = dic or {}
        self.name = name
        self.text = None
        if 'children' not in self.dic:
            self.dic['children'] = []

    @property
    def children(self):
        return (wrap(x) for x in self.dic['children'])

    @property
    def attrib(self):
        return {k: v for k, v in self.dic.items() if k != 'children'}


def wrap(obj):
    if isinstance(obj, Xml.ElementTree):
        obj = obj.getroot()
    if isinstance(obj, Xml.Element):
        return XmlWrapper(obj)
    elif isinstance(obj, dict):
        if len(obj) != 1:
            raise Exception('Dict with keys {} does not specify a directive or widget'.format(list(obj.keys())))
        k, v = next(iter(obj.items()))
        return DictWrapper(k, v)
    else:
        raise Exception('Object of type {} does not specify a directive or widget'.format(type(obj)))
