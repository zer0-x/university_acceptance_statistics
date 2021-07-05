#!/usr/bin/env python

from os import environ
from dotenv import load_dotenv
import telegram
import sqlite3
import json
from hashlib import sha3_256

load_dotenv('.env')

API_KEY = environ.get('API_KEY')


class DataBase:
	def connect(db_file = 'db.sqlite3') -> None:
		global con, cur

		con = sqlite3.connect(db_file)
		cur = con.cursor()

		try:
			cur.execute('''CEATE TABLE universitys_info
			(en_name, ar_name, year, )''')
		except sqlite3.OperationalError:
			pass

	def new_universitys_table() -> None:
		pass
	
	def insert_student_data(id, CGP=None, GAT=None, Achievement=None, STEP=None) -> None:
		pass

	def update_student_data(id, CGP=None, GAT=None, Achievement=None, STEP=None) -> None:
		pass

class BotCommands:
	def start():
		pass

	def update():
		pass


def cli() -> None:
	pass

def main() -> None:
	cli()
	pass



if __name__ == '__main__':
	main()