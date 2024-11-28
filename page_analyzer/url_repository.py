import psycopg2
from psycopg2.extras import DictCursor
from datetime import date


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn


    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY id DESC")
            rows = cur.fetchall()
            return rows if rows else None


    def get_content_with_last_date(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """SELECT DISTINCT ON (urls.id)
                urls.id AS id,
                url_checks.created_at AS created_at,
                urls.name AS name,
                url_checks.status_code AS status_code
                FROM urls
                LEFT JOIN url_checks ON urls.id=url_checks.url_id
                ORDER BY id DESC, created_at DESC""")
            rows = cur.fetchall()
            return rows if rows else None
    

    def find_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id, ))
            row = cur.fetchone()
            return row if row else None


    def find_name(self, name):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (name, ))
            row = cur.fetchone()
            return row if row else None


#    def get_by_term(self, search_term=''):
#        with self.conn.cursor(cursor_factory=DictCursor) as cur:
#            cur.execute(cur.execute("""
#                    SELECT * FROM users
#                    WHERE name ILIKE %s OR email ILIKE %s
#                """, (f'%{search_term}%', f'%{search_term}%')))
#            return cur.fetchall()

#    def save(self, urls):
#        if 'id' in urls and urls['id']:
#            self._update(urls)
#        else:
#            self._create(urls)

#    def _update(self, urls):
#        with self.conn.cursor() as cur:
#            cur.execute(
#                "UPDATE urls SET name = %s, created_at = %s WHERE id = %s",
#                (urls['name'], urls['created_at'], urls['id'])
#            )
#        self.conn.commit()
    def save(self, name):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (name, date.today(), )
            )
            id = cur.fetchone()[0]
        self.conn.commit()
        return id
