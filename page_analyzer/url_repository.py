from datetime import date

from psycopg2.extras import DictCursor


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

    def save(self, name):
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO urls (name, created_at) 
                VALUES (%s, %s) RETURNING id""",
                (name, date.today(), )
            )
            id = cur.fetchone()[0]
        self.conn.commit()
        return id
