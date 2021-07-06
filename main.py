#!/usr/bin/env python

__author__ = 'zer0-x'

from os import environ
from typing import List
import telegram
import sqlite3
import json
from hashlib import sha3_256, md5
import time
##TODO translation
#import gettext
##TODO sync
#import asyncio


class DataBase:
	@staticmethod
	def connect(db_file = 'db.sqlite3') -> None:
		global con, cur

		con = sqlite3.connect(db_file)
		cur = con.cursor()


		cur.execute('''CEATE TABLE IF NOT EXISTS universitys_data
					(id TEXT UNIQUE NOT NULL,
					en_name TEXT NOT NULL,
					ar_name TEXT NOT NULL,
					year INTEGER NOT NULL,
					semester INTEGER NOT NULL,
					majors_data_json TEXT NOT NULL,
					create_time REAL NOT NULL);''')


	@staticmethod
	def new_universitys_table() -> None:
		##get university info
		en_name = input('English university name: ')
		ar_name = input('Arabic university name: ')
		year = int(input('Admission year: '))
		semester = int(input('Admission semester (1, 2, 3):'))
		
		majors_count = int(input('\nUniversity majors count: '))
		unified_total = bool(input('Do you want to use unified total combination? '))

		##Input function for the total combination
		def get_total() -> List:
			CGP = float(input('CGP percentage: ').removesuffix('%')) or None
			GAT = float(input('GAT percentage: ').removesuffix('%')) or None
			Achievement = float(input('Achievement percentage: ').removesuffix('%')) or None
			STEP = float(input('STEP percentage: ').removesuffix('%')) or None
			print('\n\n')

			combination = [CGP, GAT, Achievement, STEP]

			return [None if not x else (x/100 if 1<x<=100 else x) for x in combination]

		##Get majors and return a json str
		def get_mojors() -> str:
			##Unified total?
			if unified_total:
				print('\nWhat is the unified total combination? (0.4 as same as 40 and 40%), (Keep it blank for None)')
				CGP, GAT, Achievement, STEP = get_total()

			majors_data_json = []
			for i in range(majors_count):
				major_code = input(f'Major {i} code (CS, SWE ...): ')
				major_en_name = input(f'Major {i} English name: ')
				major_ar_name = input(f'Major {i} Arabic name: ')
				major_sex = input(f'Major {i} sex (0=Both, 1=Boys, 2=Girls): ')

				if not unified_total:
					print(f'\n{major_en_name} total combination? (0.4 as same as 40 and 40%), (Keep it blank for None)')
					CGP, GAT, Achievement, STEP = get_total()

					majors_data_json.append({'id': i,
											'code': major_code,
											'en_name': major_en_name,
											'ar_name': major_ar_name,
											'sex': major_sex,
											'CGP': CGP, 'GAT': GAT, 'Achievement': Achievement, 'STEP': STEP})


			return json.dumps(majors_data_json)

		##Get majors ether from a file or cli
		use_mjors_file = bool(input('Do you want to import a json file for majors data? '))

		if use_mjors_file:
			file_path = input('A valed file path (Don\'t use quotes): ')
			with open(file_path, 'r') as file:
				majors_data_json = file.read()
		else:
			majors_data_json = get_mojors()

		##Create an id for the university
		id = md5((en_name + str(year) + str(semester)).encode()).hexdigest()

		##Insert university data to db
		cur.execute('''INSERT INTO universitys_data VALUES
					(:id, :en_name, :ar_name, :year, :semester, :majors_data_json, :create_time);''',

					{'id': id,
					'en_name': en_name,
					'ar_name': ar_name,
					'year': year,
					'semester': semester,
					'majors_data_json': majors_data_json,
					'create_time': time.time()})

		##Create new table for the university
		cur.execute('''CREATE TABLE :id 
					(student_id TEXT UNIQUE NOT NULL,
					sex TEXT,
					major TEXT,
					CGP REAL,
					GAT INTEGER,
					Achievement INTEGER,
					STEP INTEGER,
					add_time REAL NOT NULL,
					last_update REAL,
					);''', {'id': id})

		con.commit()

	@staticmethod
	def drop_table():
		##Get data
		en_name = input('English university name: ')
		year = int(input('Admission year: '))
		semester = int(input('Admission semester (1, 2, 3):'))

		##Create the university table id
		id = md5((en_name + str(year) + str(semester)).encode()).hexdigest()

		confirmation = bool(input(f'Are you sure that you want to delete {en_name}-{year}-{semester} and all it\'s data?'))

		cur.execute('''DELETE FROM universitys_data
					WHERE id = :id;''')
		cur.execute('DROP TABLE IF EXISTS :id;', {'id', id})

	@staticmethod
	def insert_student_data(id, student_id, sex, major, CGP=None, GAT=None, Achievement=None, STEP=None) -> None:
		cur.execute('''INSERT INTO :id VALUES
					(:student_id, :sex, :major, :CGP, :GAT, :Achievement, :STEP, :add_time, :last_update
					)''',
					{'id': id,
					'student_id': student_id,
					'sex': sex,
					'major': major,
					'CGP': CGP,
					'GAT': GAT,
					'Achievement': Achievement,
					'STEP': STEP,
					'add_time': time.time(),
					'lastupdate': None})

	@staticmethod
	def update_student_data(id, student_id, major, CGP=None, GAT=None, Achievement=None, STEP=None) -> None:
		cur.execute('''UPDATE :id SET
					major = :major,
					CGP =:CGP,
					GAT = :GAT
					Achievement = :Achievement,
					STEP = :STEP''',
					{'id': id,
					'CGP': CGP,
					'GAT': GAT,
					'Achievement': Achievement,
					'STEP': STEP})

	@staticmethod
	def student_withdrawal(id, student_id):
		cur.execute('DELETE FROM :id WHERE student_id = :student_id',
					{'id': id, 'student_id': student_id})


class BotCommands:
	@staticmethod
	def start():
		pass

	@staticmethod
	def update():
		pass

	@staticmethod
	def withdrawal():
		pass


def cli() -> None:
	pass

def main() -> None:
	__import__('dotenv').load_dotenv()
	API_KEY = environ.get('API_KEY')

	cli()




if __name__ == '__main__':
	main()