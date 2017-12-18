import chwrapper

API_ACCESS_KEY = 'PbFSzk27f_4hiW8v3TXmfpVt4xhdcIwVql_eI_xJ'


def get_search_client():
    """Return a search client object for accessing the
    Companies House API.
    """
    return chwrapper.Search(access_token=API_ACCESS_KEY)


def get_company_directors_shareholders(company_id):
    """Retrieve all the directors and shareholders info for
    a given company.
    """
    search_client = get_search_client()
    try:
        response = search_client.officers(company_id)
    # GJ MAKE MORE SPECIFIC ERROR CATCHING?
    except Exception as e:
        print(u"Error retrieving officers for company {}: {}".format(company_id, e))
        return []
    officers = response.json()
    return [officer for officer in officers['items']
            if officer['officer_role'].upper() in ('INVESTOR', 'DIRECTOR')]


def get_director_appointments(director_id):
    """For a given director, return their appointments,
    aka the companies they are involved with.
    """
    search_client = get_search_client()
    response = search_client.appointments(director_id)
    return response.json()['items']


def get_company_info(company_id):
    """Get the basic company information for a
    given company id.
    """
    search_client = get_search_client()
    try:
        response = search_client.profile(company_id)
    except Exception as e:
        print(u"Error retrieving data for company {}: {}".format(company_id, e))
        return {}
    return response.json()
