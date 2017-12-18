import pytest

from .. import companies_house_graph as chg


def test_graph_creation():
    """Ensure we initialise an empty graph"""
    test_graph = chg.CHGraph()
    assert test_graph
    assert len(test_graph.get_nodes()) == 0
    assert len(test_graph._graph.edges) == 0


@pytest.mark.parametrize('nodes', [
    (['Company1', 'Company2']),
    (['Company1', 'Company2', 'Company3']),
    ([]),
])
def test_get_nodes(nodes):
    """Ensure we correctly retrieve the node list."""
    test_graph = chg.CHGraph()
    test_graph._graph.add_nodes_from(nodes)
    assert len(test_graph.get_nodes()) == len(nodes)
    assert sorted(test_graph.get_nodes()) == sorted(nodes)


@pytest.mark.parametrize('node', [
    (chg.COMPANY('Company1', '1', '30')),
    (chg.COMPANY('Company45', '737', '0')),
])
def test_get_node_id(node):
    """Ensure we correctly retrieve a node's id."""
    test_graph = chg.CHGraph()
    test_graph._graph.add_node(
        node.name,
        type='company',
        id=node.id,
        direct_credit_score=node.direct_credit_score
    )
    assert test_graph.get_node_id(node.name) == node.id


@pytest.mark.parametrize('node, node_type', [
    (chg.COMPANY('Company1', '1', '30'), 'company'),
    (chg.PERSON('Director1', '2'), 'person'),
])
def test_get_node_type(node, node_type):
    """Ensure we correctly retrieve a node's type."""
    test_graph = chg.CHGraph()
    test_graph._graph.add_node(
        node.name,
        type=node_type,
        id=node.id,
    )
    assert test_graph.get_node_type(node.name) == node_type


@pytest.mark.parametrize('company_info, director_info', [
    (chg.COMPANY('Company1', '1', '30'), [chg.PERSON('Director1', '1'), chg.PERSON('Director2', '2')]),
    (chg.COMPANY('Company1', '1', '30'), []),
])
def test_update_graph(company_info, director_info):
    """Ensure we correctly update a graph to
    contain the correct nodes and edges.
    """
    test_graph = chg.CHGraph()
    test_graph.update_graph(company_info, director_info)
    assert len(test_graph.get_nodes()) == len([company_info]) + len(director_info)
    for person in director_info:
        assert person.name in test_graph.get_nodes()
        assert test_graph._graph.has_edge(person.name, company_info.name)
    for company in [company_info]:
        assert company.name in test_graph.get_nodes()


@pytest.mark.parametrize('company_info, director_info', [
    (chg.COMPANY('Company1', '1', '30'), [chg.PERSON('Director1', '1'), chg.PERSON('Director2', '2')]),
    (chg.COMPANY('Company1', '1', '30'), []),
])
def test_company_total_credit_score(company_info, director_info):
    """Ensure we correctly calculate the credit
    score based on other companies located 1 connection away.
    I.e company -> person -> company.
    """
    test_graph = chg.CHGraph()
    company1 = chg.COMPANY('Company1', '1', 30)
    company2 = chg.COMPANY('Company2', '2', 13)
    person1 = chg.PERSON('Director1', '1')
    person2 = chg.PERSON('Director2', '2')
    test_graph.update_graph(company1, [person1, person2])
    test_graph.update_graph(company2, [person1])
    assert test_graph.get_company_total_credit_score(company1.name) == 43
