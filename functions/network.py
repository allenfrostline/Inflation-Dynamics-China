import networkx as nx
import numpy as np
from .draw_networkx_edges_with_arrows import draw_networkx_edges_with_arrows


def network(plt, net, year, plot=True, save=False, ret=False):
    u = net.source
    v = net.target
    w = net.flow

    G = nx.DiGraph()
    for ui, vi, wi in zip(u, v, w): G.add_edges_from([(ui, vi)], weight=wi)
    if plot:
        pos = nx.circular_layout(G)
        edge_labels = dict([((u, v,), d['weight']) for u, v, d in G.edges(data=True)])
        weights = [G[u][v]['weight'] for u, v in G.edges()]
        weights = np.array(list(map(lambda x: (x - min(weights)) / (max(weights) - min(weights)), weights)))  # normalize
        weights = weights * 10
    
        fig = plt.figure(figsize=(10, 10))
        plt.axis('off')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                     font_family='serif', font_size=4,
                                     font_color='grey', bbox={'alpha': .0, 'lw': 0})
        nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_color='r',
                               node_size=100)
    
        draw_networkx_edges_with_arrows(G, pos, weights, '#5cce40', plt)
    
        nx.draw_networkx_labels(G, pos, font_color='white', font_family='serif',
                                font_size=6)
    
        fig.set_facecolor('#262626')
    
        plt.title(r'Railway Transport ($10^3$ ton), {}'.format(year), color='white')
        plt.tight_layout()
    
        if save:
            plt.savefig('./plots/net{}.pdf'.format(year),
                        facecolor=fig.get_facecolor())
    
        plt.show()
    if ret: return G
