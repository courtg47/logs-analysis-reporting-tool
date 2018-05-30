#!/usr/bin/env python3

"""

Logs Analysis Reporting Tool: this program will query the PSQL database
called News using Python DB-API and retrieve information from the DB
pertaining to three questions:

1) What are the three most popular articles of all time?
2) Who are the most popular article authors of all time?
3) On which days did more than 1% of requests lead to errors?

"""

import psycopg2

""" PSQL query which finds top 3 most popular articles in the DB. """
popular_articles = """SELECT articles.title, COUNT(*) AS num
                    FROM articles JOIN log
                    ON log.path = '/article/' || articles.slug
                    GROUP BY path, title
                    ORDER BY num DESC
                    LIMIT 3"""


""" PSQL query which finds the most popular authors. """
popular_authors = """SELECT authors.name, COUNT(*) AS num
                    FROM authors JOIN articles
                    ON authors.id = articles.author
                    JOIN log
                    ON log.path = '/article/' || articles.slug
                    GROUP BY name
                    ORDER BY num DESC"""


""" PSQL query which displays the days
where there were more than 1% 404 errors. """
request_errors = """SELECT to_char(date, 'FMMonth DD, YYYY'),
                    ROUND(
                        (CAST(errors as float) /
                        CAST(views as float) * 100)::numeric,
                        1
                    )
                    FROM daily_errors
                    WHERE cast(errors as float) /
                    CAST(views as float) * 100 > 1.0
                    GROUP BY date, errors, views"""


def database_connection(command):
    """Connect to PostgreSQL database using Python DB-API.

    Parameters:
    command -- a string which contains a SQL query.

    Returns:
    Passes results of the SQL query to the print_results function.
    """
    try:
        db = psycopg2.connect("dbname=news")
        c = db.cursor()
        c.execute(command)
        results = c.fetchall()
        print_results(command, results)
        db.close()

    except psycopg2.DatabaseError as error:
        print(error)


def print_results(command, results):
    """Print results from the DB to the console.

    Parameters:
    command --  a string which contains a SQL query.
    results -- a string result returned from the DB based on the command.

    Returns:
    Results of the query to the console in the desired format as a string.
    """
    if command == popular_articles:
        print("What are the three most popular articles of all time? \n")
        for title, views in results:
            print('"{}" -- {} views'.format(title, views))
    elif command == popular_authors:
        print("Who are the most popular article authors of all time? \n")
        for title, views in results:
            print("{} -- {} views".format(title, views))
    elif command == request_errors:
        print("On which days did more than 1% of requests lead to errors? \n")
        for title, views in results:
            print("{} -- {}% errors".format(title, views))
    print("\n")


if __name__ == '__main__':
    database_connection(popular_articles)
    database_connection(popular_authors)
    database_connection(request_errors)
