"""
graph.py.

ADT definitions for directed and undirected graphs.

Project UID bd3b06d8a60861e18088226c3a1f0595e4426dcf
"""

import csv
import doctest
# add whatever imports you need here


class GraphError(Exception):
    """This class is used for raising exceptions in the graph ADTs.

    >>> e = GraphError()
    >>> str(e)
    ''
    >>> f = GraphError('some message')
    >>> str(f)
    'some message'
    >>> repr(e)
    "GraphError('')"
    >>> f # interpreter does the same thing as print(repr(f))
    GraphError('some message')
    """

    def __init__(self, message=''):
        """Initialize this exception with the given message.

        The message defaults to an empty string.
        """
        super().__init__(message)
        self.message = message
        # add your code here

    def __str__(self):
        """Return the message used to create this exception."""
        return self.message

    def __repr__(self):
        """Return the canonical string representation of this graph."""
        return f'GraphError({repr(str(self))})'


class Node:
    r"""Represents a node in a graph.

    >>> n = Node('node1', weight=80, age=90)
    >>> n.identifier()
    'node1'
    >>> d = n.attributes()
    >>> d['age']
    90
    >>> d['weight']
    80
    >>> str(n)
    'Node [node1]\n    age : 90\n    weight : 80\n'
    """

    def __init__(self, identifier, **attributes):
        """Initialize this node with the given ID.

        The keyword arguments are optional node attributes.
        """
        self.dict = attributes
        self.string = identifier

    def identifier(self):
        """Return the identifier of this node."""
        return self.string

    def attributes(self):
        """Return a copy of this node's attribute dictionary."""
        return self.dict

    def __str__(self):
        """Return a string representation of this node.

        Produces a representation of this node and its attributes in
        sorted, increasing, lexicographic order.
        """
        temp = ""
        temp += ("Node [" + str(self.string)+"]\n")
        for key in sorted(self.dict):
            temp += "    "+key+" : "+str(self.dict[key])+'\n'
        return temp


class Edge:
    r"""Represents a directed edge in a graph.

    >>> n1, n2 = Node('node1'), Node('node2')
    >>> e = Edge(n1, n2, size=3, cost=5)
    >>> d = e.attributes()
    >>> d['cost']
    5
    >>> d['size']
    3
    >>> e.nodes() == (n1, n2)
    True
    >>> str(e)
    'Edge from node [node1] to node [node2]\n    cost : 5\n    size : 3\n'
    """

    def __init__(self, node1, node2, **attributes):
        """Initialize this edge with the Nodes node1 and node2.

        The keyword arguments are optional edge attributes.
        """
        self.node1 = node1
        self.node2 = node2
        self.dict = attributes

    def attributes(self):
        """Return a copy of this edge's attribute dictionary."""
        return self.dict

    def nodes(self):
        """Return a tuple of the Nodes corresponding to this edge.

        The nodes are in the same order as passed to the constructor.
        """
        # print((self.node1.identifier(), self.node2.identifier()))
        return ((self.node1, self.node2))

    def __str__(self):
        """Return a string representation of this edge.

        Produces a representation of this edge and its attributes in
        sorted, increasing, lexicographic order.
        """
        temp = "Edge from node [" + str(self.node1.identifier())+"] to node ["
        temp += str(self.node2.identifier())+"]\n"
        for key in sorted(self.dict):
            temp += "    " + str(key) + " : " + str(self.dict[key])+"\n"
        return temp


class BaseGraph:
    r"""A graph where the nodes and edges have optional attributes.

    This class should not be instantiated directly by a user.

    >>> g = BaseGraph()
    >>> len(g)
    0
    >>> g.add_node(1, a=1, b=2)
    >>> g.add_node(3, f=6, e=5)
    >>> g.add_node(2, c=3)
    >>> g.add_edge(1, 2, g=7)
    >>> g.add_edge(3, 2, h=8)
    >>> len(g)
    3
    >>> str(g.node(2))
    'Node [2]\n    c : 3\n'
    >>> g.node(4)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> str(g.edge(1, 2))
    'Edge from node [1] to node [2]\n    g : 7\n'
    >>> g.edge(1, 3)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> len(g.nodes())
    3
    >>> g.nodes()[0].identifier()
    1
    >>> len(g.edges())
    2
    >>> str(g.edges()[1])
    'Edge from node [3] to node [2]\n    h : 8\n'
    >>> 1 in g, 4 in g
    (True, False)
    >>> (1, 2) in g, (2, 3) in g
    (True, False)
    >>> g[1].identifier()
    1
    >>> g[(1, 2)].nodes()[0].identifier()
    1
    >>> print(g)
    BaseGraph:
    Node [1]
        a : 1
        b : 2
    Node [2]
        c : 3
    Node [3]
        e : 5
        f : 6
    Edge from node [1] to node [2]
        g : 7
    Edge from node [3] to node [2]
        h : 8
    <BLANKLINE>
    """

    def __init__(self):
        """Initialize this graph object."""
        self.len = 0
        self.graph = {}
        self.edgesl = {}

    def __len__(self):
        """Return the number of nodes in the graph."""
        return self.len

    def add_node(self, node_id, **attributes):
        """Add a node to this graph.

        Requires that node_id, the unique identifier for the node, is
        hashable and comparable to all identifiers for nodes currently
        in the graph. The keyword arguments are optional node
        attributes. Raises a GraphError if a node already exists with
        the given ID.
        """
        if node_id in self.graph:
            raise GraphError("add_node")
        self.len += 1
        self.graph[node_id] = Node(node_id, **attributes)

    def node(self, node_id):
        """Return the Node object for the node whose ID is node_id.

        Raises a GraphError if the node ID is not in the graph.
        """
        if node_id not in self.graph:
            raise GraphError("node")
        return self.graph[node_id]

    def nodes(self):
        """Return a list of all the Nodes in this graph.

        The nodes are sorted by increasing node ID.
        """
        temp_list = []
        for key in sorted(self.graph):
            temp_list.append(self.graph[key])
        return temp_list
        # add your code here

    def add_edge(self, node1_id, node2_id, **attributes):
        """Add an edge between the nodes with the given IDs.

        The keyword arguments are optional edge attributes. Raises a
        GraphError if either node is not found, or if the graph
        already contains an edge between the two nodes.
        """
        if (node1_id not in self.graph or node2_id not in self.graph):
            raise GraphError("add_edge")
        if node1_id == node2_id:
            raise GraphError("add_edge")
        temp = Edge(self.graph[node1_id], self.graph[node2_id], **attributes)
        self.edgesl[(node1_id, node2_id)] = temp
        # add your code here

    def edge(self, node1_id, node2_id):
        """Return the Edge object for the edge between the given nodes.

        Raises a GraphError if the edge is not in the graph.
        """
        if (node1_id, node2_id) not in self.edgesl:
            raise GraphError("edge")
        return self.edgesl[(node1_id, node2_id)]
        # add your code here

    def edges(self):
        """Return a list of all the edges in this graph.

        The edges are sorted in increasing, lexicographic order of the
        IDs of the two nodes in each edge.
        """
        temp_list = []
        for edge in sorted(self.edgesl.items()):
            temp_list.append(edge[1])
        return temp_list

    def __getitem__(self, key):
        """Return the Node or Edge corresponding to the given key.

        If key is a node ID, returns the Node object whose ID is key.
        If key is a pair of node IDs, returns the Edge object
        corresponding to the edge between the two nodes. Raises a
        GraphError if the node IDs or edge are not in the graph.
        """
        if key in self.graph:
            return self.graph[key]
        if key in self.edgesl:
            return self.edgesl[key]
        raise GraphError("getitem")

    def __contains__(self, item):
        """Return whether the given node or edge is in the graph.

        If item is a node ID, returns True if there is a node in this
        graph with ID item. If item is a pair of node IDs, returns
        True if there is an edge corresponding to the two nodes.
        Otherwise, returns False.
        """
        return (item in self.graph or item in self.edgesl)

    def __str__(self):
        """Return a string representation of the graph.

        The string representation contains the nodes in sorted,
        increasing order, followed by the edges in order.
        """
        result = f'{type(self).__name__}:\n'
        for node in self.nodes():
            result += str(node)
        for edge in self.edges():
            result += str(edge)
        return result


class UndirectedGraph(BaseGraph):
    """An undirected graph where nodes/edges have optional attributes.

    >>> g = UndirectedGraph()
    >>> g.add_node(1, a=1)
    >>> g.add_node(2, b=2)
    >>> g.add_edge(1, 2, c=3)
    >>> len(g)
    2
    >>> g.degree(1)
    1
    >>> g.degree(2)
    1
    >>> g.edge(1, 2).nodes() == (g.node(1), g.node(2))
    True
    >>> g.edge(2, 1).nodes() == (g.node(2), g.node(1))
    True
    >>> 1 in g, 4 in g
    (True, False)
    >>> (1, 2) in g, (2, 1) in g
    (True, True)
    >>> (2, 3) in g
    False
    >>> g[1].identifier()
    1
    >>> g[(1, 2)].nodes()[0].identifier()
    1
    >>> g.add_edge(1, 1, d=4)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> print(g)
    UndirectedGraph:
    Node [1]
        a : 1
    Node [2]
        b : 2
    Edge from node [1] to node [2]
        c : 3
    Edge from node [2] to node [1]
        c : 3
    <BLANKLINE>
    """

    def __init__(self):
        """Initialize this graph object."""
        super().__init__()
        self.degrees = {}

    def add_node(self, node_id, **attributes):
        """Add a node to this graph.

        Requires that node_id, the unique identifier for the node, is
        hashable and comparable to all identifiers for nodes currently
        in the graph. The keyword arguments are optional node
        attributes. Raises a GraphError if a node already exists with
        the given ID.
        """
        if node_id in self.graph:
            raise GraphError("add_node")
        self.len += 1
        self.graph[node_id] = Node(node_id, **attributes)
        self.degrees[node_id] = 0

    def degree(self, node_id):
        """Return the degree of the node with the given ID.

        Raises a GraphError if the node ID is not found.
        """
        num = 0
        # print(self.edgesl)
        for edhe in self.edgesl:
            if node_id in edhe:
                num += 1
        return num // 2
        # add your code here

    def __contains__(self, item):
        """Return whether the given node or edge is in the graph.

        If item is a node ID, returns True if there is a node in this
        graph with ID item. If item is a pair of node IDs, returns
        True if there is an edge corresponding to the two nodes.
        Otherwise, returns False.
        """
        if isinstance(item, int):
            return item in self.graph
        if (isinstance(item, str) and len(item) == 1):
            return item in self.graph
        temp_pair = (item[1], item[0])
        return (item in self.edgesl or temp_pair in self.edgesl)
    # Add whatever overridden or new methods you need here

    def add_edge(self, node1_id, node2_id, **attributes):
        """Add an edge between the nodes with the given IDs.

        The keyword arguments are optional edge attributes. Raises a
        GraphError if either node is not found, or if the graph
        already contains an edge between the two nodes.
        """
        if (node1_id not in self.graph or node2_id not in self.graph):
            raise GraphError("add_edge")
        if node1_id == node2_id:
            raise GraphError("add_edge")
        edge1 = Edge(self.graph[node1_id], self.graph[node2_id], **attributes)
        edge2 = Edge(self.graph[node2_id], self.graph[node1_id], **attributes)
        self.edgesl[(node1_id, node2_id)] = edge1
        self.edgesl[(node2_id, node1_id)] = edge2
        self.degrees[node1_id] += 1
        self.degrees[node2_id] += 1

    def edge(self, node1_id, node2_id):
        """Return the Edge object for the edge between the given nodes.

        Raises a GraphError if the edge is not in the graph.
        """
        if (node1_id, node2_id) in self.edgesl:
            # print(self.edgesl[(node1_id, node2_id)])
            return self.edgesl[(node1_id, node2_id)]
        if (node2_id, node1_id) in self.edgesl:
            # print("Second")
            # print(self.edgesl[(node2_id, node1_id)])
            return self.edgesl[(node2_id, node1_id)]
        raise GraphError("edge")


class DirectedGraph(BaseGraph):
    """A directed graph where nodes/edges have optional attributes.

    >>> g = DirectedGraph()
    >>> g.add_node(1, a=1)
    >>> g.add_node(2, b=2)
    >>> g.add_edge(1, 2, c=3)
    >>> len(g)
    2
    >>> g.in_degree(1), g.out_degree(1)
    (0, 1)
    >>> g.in_degree(2), g.out_degree(2)
    (1, 0)
    >>> g.edge(1, 2).nodes() == (g.node(1), g.node(2))
    True
    >>> g.edge(2, 1)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> 1 in g, 4 in g
    (True, False)
    >>> (1, 2) in g, (2, 1) in g
    (True, False)
    >>> g[1].identifier()
    1
    >>> g[(1, 2)].nodes()[0].identifier()
    1
    >>> g.add_edge(1, 1, d=4)
    >>> g.in_degree(1), g.out_degree(1)
    (1, 2)
    >>> g.in_degree(-1)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> g.out_degree(-1)
    Traceback (most recent call last):
        ...
    GraphError: ...
    >>> print(g)
    DirectedGraph:
    Node [1]
        a : 1
    Node [2]
        b : 2
    Edge from node [1] to node [1]
        d : 4
    Edge from node [1] to node [2]
        c : 3
    <BLANKLINE>
    """

    def __init__(self):
        """Initialize this DirectedGraph object."""
        super().__init__()
        self.out_degrees = {}
        self.in_degrees = {}

    def add_node(self, node_id, **attributes):
        """Add a node to this graph.

        Requires that node_id, the unique identifier for the node, is
        hashable and comparable to all identifiers for nodes currently
        in the graph. The keyword arguments are optional node
        attributes. Raises a GraphError if a node already exists with
        the given ID.
        """
        if node_id in self.graph:
            raise GraphError("add_node")
        self.len += 1
        self.graph[node_id] = Node(node_id, **attributes)
        self.out_degrees[node_id] = 0
        self.in_degrees[node_id] = 0

    def add_edge(self, node1_id, node2_id, **attributes):
        """Add an edge between the nodes with the given IDs.

        The keyword arguments are optional edge attributes. Raises a
        GraphError if either node is not found, or if the graph
        already contains an edge between the two nodes.
        """
        if (node1_id not in self.graph or node2_id not in self.graph):
            raise GraphError("add_edge")
        temp = Edge(self.graph[node1_id], self.graph[node2_id], **attributes)
        self.edgesl[(node1_id, node2_id)] = temp
        self.out_degrees[node1_id] += 1
        self.in_degrees[node2_id] += 1

    def in_degree(self, node_id):
        """Return the in-degree of the node with the given ID.

        Raises a GraphError if the node is not found.
        """
        if node_id not in self.graph:
            raise GraphError("in_degree")
        return self.in_degrees[node_id]

    def out_degree(self, node_id):
        """Return the out-degree of the node with the given ID.

        Raises a GraphError if the node is not found.
        """
        if node_id not in self.out_degrees:
            raise GraphError("out_degree")
        return self.out_degrees[node_id]
        # add your code here

    def edges(self):
        """Return a list of all the edges in this graph.

        The edges are sorted in increasing, lexicographic order of the
        IDs of the two nodes in each edge.
        """
        temp_list = []
        for edge in sorted(self.edgesl):
            temp_list.append(self.edgesl[edge])
        return temp_list
    # Add whatever overridden or new methods you need here


def read_graph_from_csv(node_file, edge_file, directed=False):
    """Read a graph from CSV node and edge files.

    Refer to the project specification for the file formats.
    """
    result = DirectedGraph() if directed else UndirectedGraph()
    for i, filename in enumerate((node_file, edge_file)):
        attr_start = i + 1
        with open(filename, 'r', encoding="utf8") as csv_data:
            reader = csv.reader(csv_data)
            header = next(reader)
            attr_names = header[attr_start:]

            for line in reader:
                identifier, attr_values = (line[:attr_start],
                                           line[attr_start:])
                attributes = {attr_names[i]: attr_values[i]
                              for i in range(len(attr_names))}
                if i == 0:
                    result.add_node(*identifier, **attributes)
                else:
                    result.add_edge(*identifier, **attributes)
    return result


def _test():
    """Run this module's doctests."""
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)


if __name__ == '__main__':
    # Run the doctests
    _test()
