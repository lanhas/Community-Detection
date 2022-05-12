from .models import register
import networkx as nx
from networkx.algorithms import community


class LPA:
    def __init__(self):
        pass

    def run(self, g=None, k=None):
        """
        LPA标签传播算法进行社区发现,并以列表list的形式返回分类结果
        """
        communities = list(community.label_propagation_communities(g))
        return communities


@register('lpa')
def lpa():
    return LPA()
