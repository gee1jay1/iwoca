import companies_house_graph as chgraph
import companies_house_api as chapi


def get_director_id(director_appointments_url):
    director_id = director_appointments_url.split('/')[2]
    return director_id


def get_companies_from_directors(directors, graph):
    """Given a list of directors, get all the associated
    company names.
    """
    companies = []
    for director_name in directors:
        director_id = graph.get_node_id(director_name)
        appointments = chapi.get_director_appointments(director_id)
        for item in appointments:
            company_name = item['appointed_to'].get('company_name') or ''
            company_id = item['appointed_to']['company_number']
            if company_name in graph.get_nodes() or any(company.id == company_id for company in companies):
                # Don't want to add companies we already know about.
                continue
            company_info = chapi.get_company_info(company_id)
            company_credit_score = calculate_company_credit_score(company_info)
            companies.append(chgraph.COMPANY(company_name, company_id, company_credit_score))

    return companies


def update_graph_one_depth(graph, companies):
    for company in companies:
        directors = chapi.get_company_directors_shareholders(company.id)
        director_info = [
            chgraph.PERSON(director['name'].upper(), get_director_id(director['links']['officer']['appointments']))
            for director in directors
        ]

        graph.update_graph(company, director_info)

    return graph


def calculate_company_credit_score(company_info):
    if not company_info:
        return 0
    company_score = 0
    field_to_score_map = {
        'has_been_liquidated': 10,
        'has_insolvency_history': 5,
        'undeliverable_registered_office_address': 5,
        'registered_office_is_in_dispute': 2

    }

    for field, score in field_to_score_map.items():
        if company_info.get(field, False):
            company_score += score

    return company_score


def get_company_info(company_id):
    company_info = chapi.get_company_info(company_id)
    return company_info


def get_one_company(director_id):
    """Get the info for an arbitrary company associated
    with the given director id.
    """
    appointments = chapi.get_director_appointments(director_id)
    if not appointments:
        return {}

    first_company = appointments[0]
    company_id = first_company['appointed_to']['company_number']
    company_info = chapi.get_company_info(company_id)
    return company_info


def create_company_graph(company_info, depth=2):
    """For a given company_id, create a visualised graph
    of the company and directors / shareholders up to the
    given depth.
    """
    graph = chgraph.CHGraph()
    company_id = company_info['company_number']
    company_name = company_info['company_name']
    company_credit_score = calculate_company_credit_score(company_info)
    companies = [chgraph.COMPANY(company_name, company_id, company_credit_score)]
    for ii in range(0, depth):
        graph = update_graph_one_depth(graph, companies)

        if ii < depth - 1:
            director_nodes = [node for node in graph.get_nodes()
                              if graph.get_node_type(node) == 'person']
            companies = get_companies_from_directors(director_nodes, graph)

    return graph
