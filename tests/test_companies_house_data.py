import pytest

from .. import companies_house_data as chd


@pytest.mark.parametrize('appointment_url, expected_id', [
    ('/officers/sriCiU2EVpT0_c3AtFiXbGnLySk/appointments', 'sriCiU2EVpT0_c3AtFiXbGnLySk'),
    ("/officers/bPwsuK6ZoKXgz_MHZK6p-DQhJgw/appointments", 'bPwsuK6ZoKXgz_MHZK6p-DQhJgw'),
])
def test_get_director_id(appointment_url, expected_id):
    """Ensure we correctly extract the id from an appointment url."""
    test_id = chd.get_director_id(appointment_url)
    assert test_id == expected_id


@pytest.mark.parametrize('company_info, expected_score', [
    ({'has_been_liquidated': True}, 10),
    ({'has_been_liquidated': False}, 0),
    ({'has_insolvency_history': True}, 5),
    ({'undeliverable_registered_office_address': True}, 5),
    ({'registered_office_is_in_dispute': True}, 2),
    ({'has_been_liquidated': True, 'has_insolvency_history': True, 'registered_office_is_in_dispute': True}, 17),

])
def test_calculate_company_credit_score(company_info, expected_score):
    """Ensure we correctly calculate the credit_score from company info."""
    test_score = chd.calculate_company_credit_score(company_info)
    assert test_score == expected_score
