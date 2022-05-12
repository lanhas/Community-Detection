from .datasets import register


@register('karata')
class Karata:
    def __init__(self, root_path=None):
        self.data_txt = open('materials/karate/karate.txt')
        self.data_gml = open('materials/karate/karate.gml')

    def get_txt(self):
        return self.data_txt.read()

    def get_gml(self):
        return self.data_gml.read()

    def len(self):
        return len(self.data)

    def get_item(self, index):
        return self.data[index]

    def close(self):
        self.data_txt.close()
        self.data_gml.close()