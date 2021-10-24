import csv
import os

import matplotlib.pyplot as plt
import networkx as nx

from file_processor import (
    check_crawler_file, get_mean_values_from_file,
    process_file,
)


def create_graph(filename: str):
    in_file_name = f"{filename}.csv"
    check_crawler_file(in_file_name)

    node_file_name = f"{filename}_nodes.csv"
    edge_file_name = f"{filename}_edges.csv"
    _check_other_files(node_file_name, edge_file_name)

    # create graph here
    graph = nx.DiGraph()
    _add_nodes_from_csv(graph, filename=node_file_name)
    _get_edges_from_csv(graph, filename=edge_file_name)

    return graph


def get_stats_messages(graph, filename: str) -> list[str]:
    node_file_name = f"{filename}_nodes.csv"
    avg_int, avg_ext, avg_size = get_mean_values_from_file(node_file_name)

    # extra usage possible
    # In-degree for all nodes:  dict(graph.in_degree())
    # Out degree for all nodes:  dict(graph.out_degree)
    # all short paths: nx.all_pairs_shortest_path(graph)
    # all nodes we can go to in a single step from node graph_node:
    #       list(graph.successors(graph_node))
    #
    #  all nodes from which we can go to graph node in a single step:
    #       list(graph.predecessors(graph_node))

    return [
        "Directed Graphs hold directed edges.\n"
        "A Directed Graph stores nodes and edges with optional data, "
        "or attributes.",
        f"Total number of nodes: {graph.number_of_nodes()}",
        f"Total number of edges:  {graph.number_of_edges()}",
        f"Average number of external links (not unique domain): {avg_int:.0f}",
        f"Average number of internal links (not unique): {avg_ext:.0f}",
        f"Average size of the page: {avg_size:.0f}",
    ]


def _check_other_files(*filenames):
    for filename in filenames:
        if not os.path.exists(filename):
            process_file(filename=filename)


def _get_edges_from_csv(graph: nx.DiGraph, filename: str):
    with open(filename, 'r') as in_file:
        reader = csv.DictReader(in_file)
        urls = set()
        for line in reader:
            if (
                    line['next_url'].strip('/') in graph.nodes()
                    and line['url'].strip('/') != line['next_url'].strip('/')
            ):
                urls.add((line['url'].strip('/'), line['next_url'].strip('/')))

        graph.add_edges_from(urls)


def _add_nodes_from_csv(graph: nx.DiGraph, filename: str):
    with open(filename, 'r') as in_file:
        reader = csv.DictReader(in_file)
        urls = (line['url'].strip('/') for line in reader)
        graph.add_nodes_from(urls)


def get_shortest_path(graph, from_node: str, to_node: str):
    try:
        path = nx.shortest_path(graph, from_node, to_node)
    except nx.NodeNotFound:
        return []
    return path


def plot_from_graph(graph, plot_name: str):
    plt.figure(figsize=(50, 50))
    nx.draw_networkx(
        graph,
        alpha=0.7,
        # with_labels=True,
        edge_color='.4',
        cmap=plt.cm.Blues
    )

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'{plot_name}.png')
