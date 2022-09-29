"""
Program to visualise partial order relations.

@author yisiox
@version September 2022
"""

import networkx as nx
import matplotlib.pyplot as plt

def test():
    """
    Function to test packages and GUI functionality.
    Proof of concept.
    """
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(1, 5))
    G.add_edges_from([(1, 2), (1, 3), (4, 4), (2, 4), (3, 4)])

    G.nodes[1]["subset"] = 1
    G.nodes[2]["subset"] = 2
    G.nodes[3]["subset"] = 2
    G.nodes[4]["subset"] = 3

    nx.draw(G, pos = nx.multipartite_layout(G, align = "horizontal"), with_labels = True)
    plt.show()


def display_graph(graph):
    """
    Displays the graph using matplotlib.pyplot.
    
    @param graph The graph to be displayed.
    """
    print("<<< Displaying hasse diagram >>>")
    nx.draw_spectral(graph, with_labels = True)
    plt.show()


def display_hasse_diagram(graph):
    """
    Displays the graph using matplotlib.pyplot as a multipartite graph.

    @param graph The graph to be displayed.
    """
    nx.draw(graph, pos = nx.multipartite_layout(graph, align = "horizontal"), with_labels = True, arrowstyle = '-')
    plt.show()


def check_partial_order(graph):
    """
    Checks if the graph representing a relation is a partial order 
    using the definition of a partial order.
    
    1. The relation must be reflexive. 
    2. The relation must be antisymmetric.
    3. The relation must be transitive.

    @param graph The graph to be checked.
    @return A boolean value representing if the input is a partial order.
    """
    print("Checking if partial order...")
    #for all x in G
    for node in graph:
        # check reflexivity: xRx
        if not graph.has_edge(node, node):
            print("Relation is not reflexive.")
            print("Counterexample: ", node)
            return False

        # for all y in G 
        for first_degree_neighbour in graph.neighbors(node):
            # check antisymmetry: xRy implies not yRx
            if graph.has_edge(first_degree_neighbour, node) and not node is node:
                print("Relation is not antisymmetric.")
                print("Counterexample: ", node, first_degree_neighbour)
                return False

            # check transitivity: xRy and yRz implies xRz
            for second_degree_neighbour in graph.neighbors(first_degree_neighbour):
                if not graph.has_edge(node, second_degree_neighbour):
                    print("Relation is not transitive.")
                    print("Counterexample: ", node, first_degree_neighbour, second_degree_neighbour)
                    return False
    
    print("Confirmed!")
    return True


def generate_graph(domain, fn):
    """
    Generates the nodes and edges based on the input function.

    @param domain The domain of discourse.
    @param fn The relation.
    @return A graph.
    """
    G = nx.MultiDiGraph()
    G.add_nodes_from(domain)
    for x in G:
        for y in G:
            if fn(x, y):
                G.add_edge(x, y)
    return G


def generate_hasse_diagram(graph):
    """
    Generates a graph that when displayed is a hasse diagram. Direction of edges is kept.
    The display function will omit the direction.

    @param graph The graph to be converted, must be a partial order relation.
    @return A graph representing the hasse diagram.
    """
    for node in graph:
        # remove self loops
        graph.remove_edge(node, node)
    # get the transitive reduction
    graph = nx.transitive_reduction(graph)
    # enumerate the depth of each node
    minimal_elements = list(filter(lambda x: x[1] == 0, graph.in_degree()))
    shortest_paths = dict(nx.all_pairs_shortest_path_length(graph))
    for node in graph:
        graph.nodes[node]["subset"] = 1
        for ele, _ in minimal_elements:
            if node in shortest_paths[ele]:
                graph.nodes[node]["subset"] = max(graph.nodes[node]["subset"], shortest_paths[ele][node] + 1)

    return graph


def get_minimal(graph):
    """
    Finds the minimal elements.

    @param graph The graph, must be DAG.
    @return A list of minimal elements
    """
    return list(map(lambda x: x[0], filter(lambda x: x[1] == 0, graph.in_degree())))

def get_maximal(graph):
    """
    Finds the maximal elements.
    
    @param graph The graph, must be DAG.
    @return A list of maximal elements.
    """
    return list(map(lambda x: x[0], filter(lambda x: x[1] == 0, graph.out_degree())))

def get_smallest(graph):
    """
    Finds the smallest element.

    @param graph The graph, must be DAG.
    @return The smallest element or None.
    """
    temp = get_minimal(graph)
    if not nx.is_weakly_connected(graph) or len(temp) != 1:
        return None

    return temp[0]

def get_largest(graph):
    """
    Finds the largest element.

    @param graph The graph, must be DAG.
    @return The largest element or None.
    """
    temp = get_maximal(graph)
    if not nx.is_weakly_connected(graph) or len(temp) != 1:
        return None

    return temp[0] 

def print_info(graph):
    print("Maximal elements: ", get_maximal(graph))
    print("Minimal elements: ", get_minimal(graph))
    print("Largest element: ", get_largest(graph))
    print("Smallest element: ", get_smallest(graph))


def main():
    pass 

if __name__ == "__main__":
    main()
