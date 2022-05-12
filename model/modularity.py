from .models import register
import networkx as nx
from networkx.algorithms import community


class Modularity:
    def __init__(self):
        pass

    def calculate(self, g=None, com=None):
        """
        计算模块度并返回
        """
        result = community.modularity(g, com)
        return result


@register('modularity')
def modularity():
    return Modularity()
