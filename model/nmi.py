from .models import register
from sklearn import metrics
import networkx as nx
from networkx.algorithms import community


class NMI:
    def __init__(self):
        pass

    def calculate(self):
        """
        计算标准化互信息并返回
        """
        pass


@register('nmi')
def nmi():
    return NMI()
