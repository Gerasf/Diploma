import psycopg2
from psycopg2.extras import RealDictCursor, Json

class DbHandler:
    def __init__(self, dsn="dbname=parking_finder user=postgres password=YOURPASS host=localhost"):
        self.conn = psycopg2.connect(dsn, cursor_factory=RealDictCursor)
        self.conn.autocommit = True
        self.create_tables()  # Добавляем создание таблиц при инициализации
        self.__parkingAreas = []
        self.__parkingPositions = []
        self.__initParkingAreas()
        self.__initParkingPositions()

    def _fetch(self, query, args=None):
        with self.conn.cursor() as cur:
            cur.execute(query, args or ())
            return cur.fetchall()

    def _exec(self, query, args=None):
        with self.conn.cursor() as cur:
            cur.execute(query, args or ())

    def create_tables(self):
        # Создаём таблицу parking_areas
        self._exec("""
            CREATE TABLE IF NOT EXISTS parking_areas (
                area_id SERIAL PRIMARY KEY,
                top JSON,
                "right" JSON,
                bottom JSON,
                "left" JSON
            )
        """)
        # Создаём таблицу parking_positions
        self._exec("""
            CREATE TABLE IF NOT EXISTS parking_positions (
                id SERIAL PRIMARY KEY,
                area_id INTEGER,
                left_up JSON,
                right_up JSON,
                right_down JSON,
                left_down JSON,
                FOREIGN KEY (area_id) REFERENCES parking_areas(area_id)
            )
        """)

    def __initParkingAreas(self):
        rows = self._fetch('SELECT area_id, top, "right", bottom, "left" FROM parking_areas')
        self.__parkingAreas = [
            [r["top"], r["right"], r["bottom"], r["left"]] for r in rows
        ]

    def __initParkingPositions(self):
        rows = self._fetch("""
            SELECT left_up, right_up, right_down, left_down
            FROM parking_positions
        """)
        self.__parkingPositions = [
            [r["left_up"], r["right_up"], r["right_down"], r["left_down"]] for r in rows
        ]

    def getParkingArea(self):
        return self.__parkingAreas

    def getParkingPositions(self):
        return self.__parkingPositions

    def addParkingArea(self, a, b, c, d):
        self._exec("""
            INSERT INTO parking_areas (top,"right", bottom, "left")
            VALUES (%s, %s, %s, %s)
        """, (Json(a), Json(b), Json(c), Json(d)))

    def addParkingPosition(self, a, b, c, d, area_id=1):
        self._exec("""
            INSERT INTO parking_positions (area_id, left_up, right_up, right_down, left_down)
            VALUES (%s, %s, %s, %s, %s)
        """, (area_id, Json(a), Json(b), Json(c), Json(d)))

    def deleteParkingArea(self, a, b, c, d):
        self._exec("""
            DELETE FROM parking_areas
            WHERE top = %s AND "right" = %s AND bottom = %s AND "left" = %s
        """, (Json(a), Json(b), Json(c), Json(d)))

    def deleteParkingPosition(self, a, b, c, d):
        self._exec("""
            DELETE FROM parking_positions
            WHERE left_up = %s AND right_up = %s AND right_down = %s AND left_down = %s
        """, (Json(a), Json(b), Json(c), Json(d)))

__all__ = ['DbHandler']