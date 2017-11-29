import numpy as np
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
from matplotlib.colors import colorConverter


def draw_networkx_edges_with_arrows(G, pos, width, edge_color, plt,
                                    alpha=0.5, ax=None):
    ec = colorConverter.to_rgba(edge_color, alpha)

    if ax is None:
        ax = plt.gca()

    edge_pos = np.asarray([(pos[e[0]], pos[e[1]]) for e in G.edges()])
    edge_collection = LineCollection(edge_pos, colors=ec, linewidths=width,
                                     antialiaseds=(1,), linestyle='solid',
                                     transOffset=ax.transData)

    edge_collection.set_zorder(1)
    ax.add_collection(edge_collection)
    edge_collection.set_alpha(alpha)

    p = .8  # length of edge apart from the arrow part

    for (src, dst), lwi in zip(edge_pos, width):
        x1, y1 = src
        x2, y2 = dst
        dx = x2 - x1  # x offset
        dy = y2 - y1  # y offset

        d = np.sqrt(float(dx ** 2 + dy ** 2))  # length of edge

        if d == 0:
            continue

        if dx == 0:  # vertical edge
            xa = x2
            ya = dy * p + y1
        if dy == 0:  # horizontal edge
            ya = y2
            xa = dx * p + x1
        else:
            theta = np.arctan2(dy, dx)
            xa = p * d * np.cos(theta) + x1
            ya = p * d * np.sin(theta) + y1
        dx, dy = x2 - xa, y2 - ya
        patch = mpatches.Arrow(xa, ya, dx, dy, width=lwi / 55,
                               alpha=lwi * alpha / 5, color=ec,
                               transform=ax.transData)
        ax.add_patch(patch)

    minx = np.amin(np.ravel(edge_pos[:, :, 0]))
    maxx = np.amax(np.ravel(edge_pos[:, :, 0]))
    miny = np.amin(np.ravel(edge_pos[:, :, 1]))
    maxy = np.amax(np.ravel(edge_pos[:, :, 1]))

    w = maxx - minx
    h = maxy - miny

    padx, pady = 0.05 * w, 0.05 * h
    corners = (minx - padx, miny - pady), (maxx + padx, maxy + pady)

    ax.update_datalim(corners)
    ax.autoscale_view()

    return edge_collection
