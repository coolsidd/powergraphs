#!/usr/bin/env python3

from sage.all import *
import networkx as nx
from collections import Counter
from pprint import pprint
import math
from importlib import reload
import matplotlib.pyplot as plt
from tqdm import tqdm, trange


def get_epg(g: groups, group_type=PermutationGroup) -> nx.Graph:
    ele = [k for k in g]
    G = nx.Graph()
    G.add_nodes_from(ele)
    for i in range(len(ele)):
        for j in trange(i + 1, len(ele)):
            temp = g.subgroup([ele[i], ele[j]])
            if temp.is_cyclic():
                G.add_edge(ele[i], ele[j])
    return G


def isPower(element1, element2, identity) -> bool:
    e1 = element1
    e2 = element2
    if e1 == e2:
        return True
    while e1 != identity:
        e1 = e1 * element1
        if e1 == element2:
            return True
    while e2 != identity:
        e2 = e2 * element2
        if e2 == element1:
            return True
    return False


def get_pg(g: groups, group_type=PermutationGroup) -> nx.Graph:
    ele = [k for k in g]
    G = nx.DiGraph()
    G.add_nodes_from(ele)
    for i in range(len(ele)):
        temp = ele[i]
        while temp != ele[0]:
            temp = temp * ele[i]
            G.add_edge(ele[i], temp)
        # for j in trange(i + 1, len(ele)):
        #     if isPower(ele[i], ele[j], ele[0]):
        #         G.add_edge(ele[i], ele[j])
    return G


def get_components(graph: nx.Graph) -> list:
    pass


def is_clique(graph: nx.Graph) -> bool:
    num_nodes = len(graph.nodes)
    return len(graph.edges) == num_nodes * (num_nodes - 1) / 2


def plot_monoid(index, period, draw=True):

    eles = list(range(1, index + period))
    G = nx.Graph()
    G.add_nodes_from(eles)
    for i in range(len(eles) - 1):
        G.add_edge(eles[i], eles[i + 1])
    G.add_edge(eles[index + period - 2], eles[index - 1])
    if draw:
        plt.figure()
        nx.draw_kamada_kawai(G, with_labels=True)
    return G


def PG_monoid_details(
    index, period, ignore_one=True, draw_clique=False, draw_all_cliques=False
) -> nx.Graph:
    eles = list(range(1, index + period))
    G = nx.Graph()
    G.add_nodes_from(eles)
    order_dict = dict()
    layout = nx.kamada_kawai_layout(plot_monoid(index, period, draw=False))
    for element in eles:
        if element == eles[0] and ignore_one:
            continue
        adj_nodes = set()
        next_node = element
        while next_node not in adj_nodes:
            adj_nodes.add(next_node)
            if next_node != element:
                G.add_edge(element, next_node)
            next_node += element
            if next_node > index:
                next_node = index + (next_node - index) % period
        print(element, ": ", adj_nodes)
        if element >= index:
            order_dict[len(adj_nodes)] = order_dict.get(len(adj_nodes), set()).union(
                {element}
            )
    print(order_dict)
    plt.figure()
    nx.draw(G, layout, with_labels=True, node_size=200)
    plt.show()


def PG_group_details(g: groups, *args, **kwargs):
    PG = get_pg(g)
    nx.draw(PG, with_labels=True, **kwargs)
    plt.show()


def main():
    G_1 = KleinFourGroup()
    EPG_1 = get_epg(G_1)
    G_2 = CyclicPermutationGroup(5)
    EPG_2 = get_epg(G_2)
    # nx.draw(EPG_1, with_labels=True, node_size=500)
    # plt.savefig("Graph.png", format="PNG", dpi=300)
    nx.draw(EPG_2, with_labels=True, node_size=500)
    plt.savefig("Graph2.png", format="PNG", dpi=300)
    # for n in range(4, 5):
    #     # n = 2 ** n
    #     G = sg.SymmetricGroup(n)
    #     PG = get_pg(G)
    #     # EPG = get_epg(G)
    #     eles = [x for x in G]
    #     nx.draw(PG.to_undirected(), with_labels=True, node_size=500)
    #     plt.savefig("Graph.png", format="PNG", dpi=300)
    #     # PG.remove_node(eles[0])
    #     # EPG.remove_node(eles[0])
    #     # components_EPG = list(nx.connected_components(EPG))
    #     # components_PG = list(nx.connected_components(PG.to_undirected()))
    #     # nx.write_gpickle(PG, "./S_{}_EPG_Directed.gpickle".format(n))
    #     # pprint(Counter([len(x) for x in components]))
    #     # print("|Components| {}| ".format(Counter([len(x) for x in components_EPG])))
    #     # try:
    #     #     print("|Diameter|  {} |".format(nx.diameter(PG.to_undirected())))
    #     # except:
    #     #     print("Not Connected")
    #     # print("| {} | {}|".format(nx.diameter(PG), nx.diameter(EPG)))


if __name__ == "__main__":
    main()
