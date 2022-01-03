"""Class for managing all DataBase operations."""

from typing import List

import sqlite3
import json
from hashlib import sha3_256, md5
import time


class DataBase:
    """Managing all DataBase operations."""

    db_file = 'db.sqlite3'

    @staticmethod
    def create_database(db_file=db_file) -> None:
        """Create sqlite file, and add universities_data table."""
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS universities_data
                    (id TEXT UNIQUE NOT NULL,
                    code_name TEXT NOT NULL,
                    en_name TEXT NOT NULL,
                    ar_name TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    semester INTEGER NOT NULL,
                    majors_data_json TEXT NOT NULL,
                    create_time REAL NOT NULL);''')

        con.close()

    @staticmethod
    def connect(db_file=db_file) -> tuple:
        """Return a connection and cursur object for the DataBase."""
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        return con, cur

    @staticmethod
    def new_universities_table(con, cur) -> None:
        """
        Get university info from user and create new table for it.

        (University info are inserted to universities_data table.)
        """
        # Get data.
        code_name = input('University code name: ')
        en_name = input('English university name: ')
        ar_name = input('Arabic university name: ')
        year = int(input('Admission year: '))
        semester = int(input('Admission semester (1, 2, 3):'))

        # Input function for the total combination
        def get_total() -> List:
            CGP = float(input('CGP percentage: ').removesuffix('%')) or None
            GAT = float(input('GAT percentage: ').removesuffix('%')) or None
            Achievement = float(
                input('Achievement percentage: ').removesuffix('%')) or None
            STEP = float(input('STEP percentage: ').removesuffix('%')) or None
            print('\n\n')

            combination = [CGP, GAT, Achievement, STEP]

            return [None if not x
                    else (x / 100 if 1 < x <= 100 else x) for x in combination]

        # Get majors and return a json str
        def get_majors() -> str:
            # Unified total?
            if unified_total:
                print('\nWhat is the unified total combination? '
                      + '(0.4 as same as 40 and 40%), (Use 0 for None)')
                CGP, GAT, Achievement, STEP = get_total()

            majors_data_json = []
            for i in range(majors_count):
                major_code = input(f'Major {i} code (CS, SWE ...): ')
                major_en_name = input(f'Major {i} English name: ')
                major_ar_name = input(f'Major {i} Arabic name: ')
                major_sex = int(
                    input(f'Major {i} sex (0=Both, 1=Boys, 2=Girls): '))

                if not unified_total:
                    print(f'\n{major_en_name} total combination? '
                          + '(0.4 as same as 40 and 40%), '
                          + '(Keep it blank for None)')
                    CGP, GAT, Achievement, STEP = get_total()

                majors_data_json.append({'id': i,
                                         'code': major_code,
                                         'en_name': major_en_name,
                                         'ar_name': major_ar_name,
                                         'sex': major_sex,
                                         'CGP': CGP,
                                         'GAT': GAT,
                                         'Achievement': Achievement,
                                         'STEP': STEP})

            return json.dumps(majors_data_json)

        # Get majors ether from a file or cli
        choice = input(
            'Do you want to import a json file for majors data? '.lower())

        if choice in ['y', 'yes', 1]:
            use_majors_file = True
        else:
            use_majors_file = False

        del choice

        if use_majors_file:
            file_path = input('A valid file path (Don\'t use quotes): ')
            with open(file_path, 'r') as file:
                majors_data_json = json.dumps(json.loads(file.read()))
        else:
            choice = input(
                '\nDo you want to use unified total combination? ').lower()

            if choice in ['y', 'yes', 1, '']:
                unified_total = True
            else:
                unified_total = False

            del choice

            majors_count = int(input('\nUniversity majors count: '))

            majors_data_json = get_majors()

        # Create an id for the university
        id = 'u' + md5((en_name
                        + str(year)
                        + str(semester)
                        ).encode()).hexdigest()

        # Insert university data to db
        cur.execute('''INSERT INTO universities_data VALUES
                    (:id,
                     :code_name,
                     :en_name,
                     :ar_name,
                     :year,
                     :semester,
                     :majors_data_json,
                     :create_time);''',

                    {'id': id,
                     'code_name': code_name,
                     'en_name': en_name,
                     'ar_name': ar_name,
                     'year': year,
                     'semester': semester,
                     'majors_data_json': majors_data_json,
                     'create_time': time.time()})

        # Create new table for the university
        cur.execute(f'''CREATE TABLE IF NOT EXISTS {id}
                    (student_id TEXT UNIQUE NOT NULL,
                    sex INTEGER NOT NULL,
                    major TEXT NOT NULL,
                    batch INTEGER NOT NULL,
                    CGP REAL,
                    GAT INTEGER,
                    Achievement INTEGER,
                    STEP INTEGER,
                    region TEXT,
                    add_time REAL NOT NULL,
                    last_update REAL);''')

        # IF we get an error while creating the table
        # then no data will be inserted to universities_data
        con.commit()

    @ staticmethod
    def get_university_data(con, cur, id: str):
        """Return data from universities_data table using the university id."""
        cur.execute('''SELECT * FROM universities_data WHERE id = :id''',
                    {'id': id})
        return cur.fetchone()

    @ staticmethod
    def drop_table(con, cur):
        """Remove university table by en_name, year and semester."""
        # Get data
        en_name = input('English university name: ')
        year = int(input('Admission year: '))
        semester = int(input('Admission semester (1, 2, 3):'))

        # Create the university table id
        id = 'u' + md5((en_name
                        + str(year)
                        + str(semester)
                        ).encode()).hexdigest()

        confirmation = input('Are you sure that you want to delete '
                             + f'{en_name}-{year}-{semester} '
                             + 'and all it\'s data?').lower()

        if confirmation in ['y', 'yes', 1]:
            cur.execute('''DELETE FROM universities_data
                        WHERE id = :id;''')
            cur.execute('DROP TABLE IF EXISTS :id;', {'id', id})
            print("Done!")
        else:
            print("Ok, it will not be deleted.")

    @ staticmethod
    def insert_student_data(con, cur, id: str, student_id: str, sex: int,
                            major: str, batch: int, CGP: float = None,
                            GAT: int = None, Achievement: int = None,
                            STEP: int = None, region: str = None) -> None:
        """Insert a student data to the associated university table."""
        student_id = sha3_256(student_id.encode()).hexdigest()

        cur.execute(f'''INSERT INTO {id} VALUES
                    (:student_id,
                     :sex,
                     :major,
                     :batch,
                     :CGP,
                     :GAT,
                     :Achievement,
                     :STEP,
                     :region,
                     :add_time,
                     :last_update
                    )''',
                    {'student_id': student_id,
                     'sex': sex,
                     'major': major,
                     'batch': batch,
                     'CGP': CGP,
                     'GAT': GAT,
                     'Achievement': Achievement,
                     'STEP': STEP,
                     'region': region,
                     'add_time': time.time(),
                     'last_update': None})

        con.commit()

    # @ staticmethod
    # def get_student_data(con, cur, id: str, student_id: str) -> tuple:

    #     cur.execute('''SELECT * FROM :id
    #                 WHERE student_id = :student_id''')

    #     return cur.fetchone()

    # @ staticmethod
    # def update_student_data(con,
    #                         cur,
    #                         id: str,
    #                         student_id: str,
    #                         major: str,
    #                         batch: int,
    #                         CGP: float = None,
    #                         GAT: int = None,
    #                         Achievement: int = None,
    #                         STEP: int = None) -> None:

    #     cur.execute('''UPDATE :id SET
    #                 major = :major,
    #                 batch = :batch,
    #                 CGP =:CGP,
    #                 GAT = :GAT
    #                 Achievement = :Achievement,
    #                 STEP = :STEP,
    #                 lastupdate = :lastupdate,
    #                 WHERE student_id = :student_id''',
    #                 {'id': id,
    #                  'student_id': student_id,
    #                  'major': major,
    #                  'batch': batch,
    #                  'CGP': CGP,
    #                  'GAT': GAT,
    #                  'Achievement': Achievement,
    #                  'STEP': STEP,
    #                  'lastupdate': time.time()})

    #     con.commit()

    # @ staticmethod
    # def student_withdrawal(con, cur, id: str, student_id: str) -> None:
    #     cur.execute('DELETE FROM :id WHERE student_id = ":student_id"',
    #                 {'id': id, 'student_id': student_id})

    @ staticmethod
    def get_statistics(con, cur) -> set:
        """Return statistics numbers based on the associated data."""
        # TODO Get statistics from database
        pass
