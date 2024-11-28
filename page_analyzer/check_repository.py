import psycopg2
from psycopg2.extras import DictCursor
from datetime import date


class CheckRepository:
    def __init__(self, conn):
        self.conn = conn


    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM url_checks ORDER BY id DESC")
            rows = cur.fetchall()
            return rows if rows else None


    def find_id(self, url_id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC", (url_id, ))
#            row = cur.fetchone()
#            return dict(row) if row else None
            rows = cur.fetchall()
            return rows if rows else None


    def find_name(self, name):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM url_checks WHERE name = %s", (name, ))
            rows = cur.fetchall()
            return rows if rows else None


#    def find_last(self, url_id):
#        with self.conn.cursor(cursor_factory=DictCursor) as cur:
#            cur.execute("SELECT MAX(created_at) FROM url_checks WHERE url_id = %s", (url_id,))
#            row = cur.fetchone()
#            return dict(row) if row else None


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
    def save(self, url_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id) VALUES (%s) RETURNING id",
                (url_id, )
            )
            id = cur.fetchone()[0]
        self.conn.commit()
        return id
