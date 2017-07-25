import xml.etree.ElementTree as Xml


class XmlWrapper:
    def __init__(self, node):
        if isinstance(node, Xml.ElementTree):
            node = node.getroot()
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
        self.dic = dic
        self.name = name
        self.text = None

    @property
    def name(self):
        return self.name

    @property
    def children(self):
        print(self.dic['children'])
        return (DictWrapper(x) for x in self.dic['children'])

    @property
    def attrib(self):
        return {k: v for k, v in self.dic.items() if k != 'children'}
