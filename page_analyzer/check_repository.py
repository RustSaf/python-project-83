
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
            rows = cur.fetchall()
            return rows if rows else None


    def find_name(self, name):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM url_checks WHERE name = %s", (name, ))
            rows = cur.fetchall()
            return rows if rows else None


    def save(self, url_id, url_code, h1, title, description):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (url_id, url_code, h1, title, description, date.today(), )
            )
            id = cur.fetchone()[0]
        self.conn.commit()
        return id
