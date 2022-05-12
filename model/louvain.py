from .models import register
import networkx as nx
import community

class Louvain:
    def __init__(self):
        pass

    def run(self, g=None, k=None):
        partition = community.best_partition(g)
        communities = []
        size = float(len(set(partition.values())))
        for com in set(partition.values()):
            list_nodes = {nodes for nodes in partition.keys() if partition[nodes] == com}
            communities.append(list_nodes)
            # if len(communities) > 3:
            #     return communities
        return communities


@register('louvain')
def louvain():
    return Louvain()
