from collections import namedtuple

import networkx as nx
import matplotlib.pyplot as plt

# Input types to the CHGraph.
COMPANY = namedtuple('COMPANY', ['name', 'id', 'direct_credit_score'])
PERSON = namedtuple('PERSON', ['name', 'id'])


class CHGraph(object):
    """Class representing a Companies House
    graph, with methods to build and query
    the graph data.
    """
    def __init__(self):
        self._graph = self.initialise_graph()

    def initialise_graph(self):
        """Initialise the graph ready for creating
        a companies house graph.
        """
        return nx.Graph()

    def get_nodes(self):
        return self._graph.nodes

    def get_node_id(self, name):
        return self._graph.node[name]['id']

    def get_node_type(self, name):
        return self._graph.node[name]['type']

    def update_graph(self, company_info, director_info):
        """Update the graph to add nodes / edges between
        the company and employees. Note the employees may or
        may not already exist in the graph.
        """

        # Add the company node.
        self._graph.add_node(
            company_info.name,
            type='company',
            id=company_info.id,
            direct_credit_score=company_info.direct_credit_score
        )

        # Add the nodes and edges for each director.
        for director in director_info:
            self._graph.add_node(director.name, type='person', id=director.id)
            self._graph.add_edge(company_info.name, director.name)

    def _get_nodes_by_type(self, type='company'):
        return [node for node in self._graph.nodes if self._graph.node[node]['type'] == type]

    def get_company_total_credit_score(self, company_name):
        company_neighbours = []
        node_person_neighbours = list(self._graph.neighbors(company_name))
        for person_node in node_person_neighbours:
            neighbours = list(self._graph.neighbors(person_node))
            company_neighbours.extend(neighbours)

        total_score = sum([self._graph.node[company_node]['direct_credit_score']
                           for company_node in set(company_neighbours)])

        return total_score

    def visualise_graph_to_file(self, file_name='company_graph.png'):
        """Create an image file visualising the graph."""
        pos = nx.spring_layout(self._graph)
        company_nodes = self._get_nodes_by_type()
        person_nodes = self._get_nodes_by_type('person')
        nx.draw_networkx_nodes(self._graph, pos, cmap=plt.get_cmap('jet'), node_size=25, nodelist=person_nodes)
        nx.draw_networkx_nodes(self._graph, pos, cmap=plt.get_cmap('jet'), node_color='0.7', node_size=50, nodelist=company_nodes)
        nx.draw_networkx_labels(self._graph, pos, font_size=1)
        nx.draw_networkx_edges(self._graph, pos, edgelist=self._graph.edges, edge_color='b')
        plt.axis('off')
        plt.savefig(file_name, dpi=500)
