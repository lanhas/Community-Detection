import itertools
import networkx as nx
from networkx.algorithms import community

from .models import register


class GN:
    def __init__(self):
        pass

    def run(self, g=None, k=None):
        communities = list(community.girvan_newman(g))
        for communities in itertools.islice(communities, k):
            pass
        return list(communities)


@register('gn')
def gn():
    return GN()
