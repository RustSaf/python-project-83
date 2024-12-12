import psycopg2


def conn(db_name):
    return psycopg2.connect(db_name)
