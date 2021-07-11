import os
import sqlite3

from typing import List, Tuple

import config
import asyncio


class DataBase:

    def __init__(self, db_filename):
        self.db_filename = os.path.join(config.BASEDIR, 'db', db_filename)

    async def _create_connection(self):
        self._connection = sqlite3.connect(self.db_filename)
        self._cursor = self._connection.cursor()

    async def _close_connection(self):
        self._connection.close()

    async def create_tables(self):
        await self._create_connection()
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS course (
                id INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                description VARCHAR,
                price REAL,
                subject_id INTEGER,
                PRIMARY KEY (id),
                FOREIGN KEY (subject_id) REFERENCES subject(id)
            )''')
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS subject (
                id INTEGER NOT NULL,
                name VARCHAR,
                PRIMARY KEY (id)
            )
        ''')
        await self._close_connection()

    # Course methods
    async def get_course(self, course_id) -> Tuple[int, str, str, float]:
        await self._create_connection()
        self._cursor.execute('''SELECT id, name, description, price FROM course WHERE id = ?''',
                             (course_id,))
        course = self._cursor.fetchone()
        await self._close_connection()
        return course

    async def get_list_courses(self, subject_id) -> List[Tuple[int, str]]:
        await self._create_connection()

        self._cursor.execute('''
            SELECT id, name 
            FROM course 
            WHERE subject_id = ?
        ''', (subject_id,))

        courses = self._cursor.fetchall()
        await self._close_connection()

        return courses

    async def get_all_courses(self):
        await self._create_connection()

        self._cursor.execute('''
            SELECT course.id, course.name, course.subject_id, s.name
            FROM course
            INNER JOIN subject s on course.subject_id = s.id
        ''')

        courses = self._cursor.fetchall()
        await self._close_connection()

        return courses

    async def add_course(self, name, description, price, subject_id):
        subjects = map(lambda x: x[0], await self.get_list_subjects())

        if int(subject_id) not in subjects:
            raise ValueError('Предмета с таким id нет в базе данных')

        else:
            await self._create_connection()
            self._cursor.execute('''
                INSERT INTO course(name, description, price, subject_id)
                VALUES (?, ?, ?, ?)
            ''', (name, description, price, subject_id))
            self._connection.commit()

            await self._close_connection()

    async def change_course(self, data: dict):
        keys = []
        values = []

        for k, v in data.items():
            if k != 'id':

                if k == 'price' and not v.isnumeric():
                    raise ValueError('Значение цены должно быть числовым')

                if k == 'subject_id':
                    if not v.isnumeric():
                        raise ValueError('Значение id предмета должно быть числовым')
                    subjects = map(lambda x: x[0], await self.get_list_subjects())
                    if int(v) not in subjects:
                        raise ValueError('Предмета с таким id нет в базе данных')

                keys.append(k)
                values.append(v)
            else:
                if k == 'id' and not v.isnumeric():
                    raise ValueError('Значение id должно быть числовым')

        if keys:
            await self._create_connection()

            query = f'''
                UPDATE course
                SET ({', '.join(keys)}) = ({"?, " * (len(keys) - 1) + "?"})
                WHERE id = {data['id']}
            '''

            self._cursor.execute(query, values)
            self._connection.commit()

            await self._close_connection()

    async def delete_course(self, data: dict):
        course_id = data['id']

        if not course_id.isnumeric():
            raise ValueError('Значение id должно быть числовым')

        await self._create_connection()

        self._cursor.execute('''
            DELETE FROM course
            WHERE id = ?
        ''', (course_id, ))
        self._connection.commit()

        await self._close_connection()

    # Subject methods
    async def get_list_subjects(self) -> List[Tuple[int, str]]:
        await self._create_connection()
        self._cursor.execute('''SELECT id, name from subject''')
        subjects = self._cursor.fetchall()
        await self._close_connection()
        return subjects

    async def get_all_subjects(self):
        await self._create_connection()

        self._cursor.execute('''
                    SELECT id, name
                    FROM subject
                ''')

        subjects = self._cursor.fetchall()
        await self._close_connection()

        return subjects

    async def add_subject(self, name):
        await self._create_connection()

        self._cursor.execute('''
            INSERT INTO subject(name)
            VALUES (?)
        ''', (name, ))
        self._connection.commit()

        await self._close_connection()

    async def change_subject(self, data: dict):
        subject_id = data.get('id')
        name = data.get('name')

        if not subject_id.isnumeric():
            raise ValueError('Значение id должно быть числовым')

        if name:
            await self._create_connection()

            query = f'''
                            UPDATE subject
                            SET name = ?
                            WHERE id = ?
                        '''

            self._cursor.execute(query, (name, subject_id))
            self._connection.commit()

            await self._close_connection()

    async def delete_subject(self, data:dict):
        subject_id = data['id']

        if not subject_id.isnumeric():
            raise ValueError('Значение id должно быть числовым')

        await self._create_connection()

        self._cursor.execute('''
            DELETE FROM course
            WHERE subject_id = ?
        ''', (subject_id, ))

        self._cursor.execute('''
                    DELETE FROM subject
                    WHERE id = ?
                ''', (subject_id,))

        self._connection.commit()

        await self._close_connection()


if __name__ == '__main__':
    db = DataBase(config.DATABASE_PATH)
    asyncio.run(db.get_all_courses())
