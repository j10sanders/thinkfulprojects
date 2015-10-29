__author__ = 'Jonathan'
import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets'")
logging.debug("Database connection established.")

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
        try:
            command = "insert into snippets values (%s, %s)"
            cursor.execute(command, (name, snippet))
        except psycopg2.IntegrityError as e:
            connection.rollback()
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name."""
    logging.info("Retrieving snippet {!r}".format(name))
    cursor = connection.cursor()
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    logging.debug("Snippet retrieved successfully.")
    if not row:
        logging.debug("That keyword doesn't exist")
        return "That keyword doesn't exist"
    else:
        return row[0]
        
def catalog():
    """Retrieve list of all the available keywords"""
    logging.info("Retrieving all the keywords: {!r}")
    cursor = connection.cursor()
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets")
        table = cursor.fetchall()
    logging.debug("Snippet retrieved successfully.")
    return [row[0] for row in table]
    
def like(snippet):
    """Retrieve list of all the similar snippets"""
    logging.info("Retrieving all similar snippets: {!r}")
    cursor = connection.cursor()
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets where message like %s", ("%" + snippet + "%",))
        table = cursor.fetchall()
    logging.debug("Snippets retrieved successfully.")
    return [row[0] for row in table]

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text (or let you know what's stored)")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")

     # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Get a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Return the keywords")
    
    logging.debug("Constructing like subparser")
    like_parser = subparsers.add_parser("like", help="Find similar snippets")
    like_parser.add_argument("snippet", help="The snippet text")

    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        name = catalog(**arguments)
        print("The options are: {!r}".format(name))
    elif command == "like":
        snippet = like(**arguments)
        print("Retrieved similar snippet(s): {!r}".format(snippet))
        logging.info('%s', type(snippet))


if __name__ == "__main__":
    main()