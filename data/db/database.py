import os
import sqlite3

from typing import List, Tuple

import config


class DataBase:

    def __init__(self, db_filename):
        self.db_filename = os.path.join(config.BASEDIR, 'db', db_filename)

    async def _create_connection(self):
        self.connection = sqlite3.connect(self.db_filename)
        self.cursor = self.connection.cursor()

    async def _close_connection(self):
        self.connection.close()

    async def create_tables(self):
        await self._create_connection()
        self.cursor.execute('''
            CREATE TABLE course (
                id INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                description VARCHAR,
                price REAL,
                subject_id INTEGER,
                PRIMARY KEY (id),
                FOREIGN KEY (subject_id) REFERENCES subject(id)
            )''')
        self.cursor.execute('''
            CREATE TABLE subject (
                id INTEGER NOT NULL,
                name VARCHAR,
                PRIMARY KEY (id)
            )
        ''')
        await self._close_connection()

    async def get_list_subjects(self) -> List[Tuple[int, str]]:
        await self._create_connection()
        self.cursor.execute('''SELECT id, name from subject''')
        subjects = self.cursor.fetchall()
        await self._close_connection()
        return subjects

    async def get_list_courses(self, subject_id) -> List[Tuple[int, str]]:
        await self._create_connection()
        self.cursor.execute('''SELECT id, name FROM course WHERE subject_id = ?''', (subject_id, ))
        courses = self.cursor.fetchall()
        await self._close_connection()
        return courses

    async def get_course(self, course_id) -> Tuple[int, str, str, float]:
        await self._create_connection()
        self.cursor.execute('''SELECT id, name, description, price FROM course WHERE id = ?''', (course_id,))
        course = self.cursor.fetchone()
        await self._close_connection()
        return course


if __name__ == '__main__':
    db = DataBase(config.DATABASE_PATH)
    # asyncio.run(db.get_subjects())

