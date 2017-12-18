import argparse
import sys

import companies_house_data as chd


def get_parser():
    """Set up the parser with the required arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--company_id",
        help="The id of the company you wish to query.",
        action="store",
    )

    parser.add_argument(
        "--director_id",
        help="The id of the director you wish to query.",
        action="store",
    )

    parser.add_argument(
        "--depth",
        help="The depth of the query you are making. Defaults to 2.",
        action="store",
        type=int,
        default=2
    )

    return parser


def get_director_data(director_id, depth):
    """Calculate the relevant director data and visualise
    as a graph.
    """
    company_info = chd.get_one_company(director_id)
    if not company_info:
        print("\nSorry, we are unable to provide data for the director id {}".format(director_id))
        return
    graph = chd.create_company_graph(company_info, depth=depth)
    graph.visualise_graph_to_file()
    print("\nPlease see output file for director graph.")


def get_company_data(company_id, depth):
    """Calculate the relevant company data and visualise
    as a graph.
    """
    company_info = chd.get_company_info(company_id)
    if not company_info:
        print("\nSorry, we are unable to provide data for the company id {}".format(company_id))
        return
    graph = chd.create_company_graph(company_info, depth=depth)
    graph.visualise_graph_to_file()
    print("\nPlease see output file for company graph.")
    credit_score = graph.get_company_total_credit_score(company_info['company_name'])
    print("\nTotal credit score is {}. The closer to 0 the better.".format(credit_score))


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    # Display help if no args.
    if len(sys.argv) == 1 or not any((args.company_id, args.director_id)):
        parser.print_help()
        print("You must include one of company_id or director_id.")
        sys.exit(1)

    if args.company_id:
        get_company_data(args.company_id, args.depth)

    if args.director_id:
        get_director_data(args.director_id, args.depth)
