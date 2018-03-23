#!/usr/bin/python3

import psycopg2

"""

Logs Analysis Reporting Tool: this program will query the PSQL database
called News using Python DB-API and retrieve information from the DB
pertaining to three questions:

1) What are the three most popular articles of all time?
2) Who are the most popular article authors of all time?
3) On which days did more than 1% of requests lead to errors?

"""

""" PSQL query which finds top 3 most popular articles in the DB """
popular_articles = """SELECT articles.title, COUNT(*) AS num
                    FROM articles JOIN log
                    ON log.path = '/article/' || articles.slug
                    GROUP BY path, title
                    ORDER BY num DESC LIMIT 3"""


""" PSQL query which finds the most popular authors """
popular_authors = """SELECT authors.name, COUNT(*) AS num
                    FROM authors JOIN articles
                    ON authors.id = articles.author
                    JOIN log
                    ON log.path = '/article/' || articles.slug
                    GROUP BY name
                    ORDER BY num DESC"""


""" PSQL query which displays the days
where there were more than 1% 404 errors """
request_errors = """SELECT date,
                    TRUNC(
                        (CAST(errors as float) /
                        CAST(views as float) * 100)::numeric,
                        1
                    )
                    FROM daily_errors
                    WHERE cast(errors as float) /
                    CAST(views as float) * 100 > 1.0
                    GROUP BY date, errors, views"""


def database_connection(command):
    """Connects to PostgreSQL database using DB-API
    and queries the DB with the above SQL.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(command)
    results = c.fetchall()
    print_results(command, results)
    db.close()


def print_results(command, results):
    """This function takes the information fetched
    from the DB and prints to the console in the
    desired format, depending on the information queried.
    """
    if command == popular_articles:
        print "What are the three most popular articles of all time? \n"
        for row in results:
            print "\"" + row[0] + "\"" + " -- " + str(row[1]) + " views"
    elif command == popular_authors:
        print "Who are the most popular article authors of all time? \n"
        for row in results:
            print row[0] + " -- " + str(row[1]) + " views"
    elif command == request_errors:
        print "On which days did more than 1% of requests lead to errors? \n"
        for row in results:
            print row[0] + " -- " + str(row[1]) + "% errors"
    print "\n"


database_connection(popular_articles)
database_connection(popular_authors)
database_connection(request_errors)
