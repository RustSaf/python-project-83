import psycopg2


def get_connection(db_name):
    return psycopg2.connect(db_name)