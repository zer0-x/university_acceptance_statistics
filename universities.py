#!/usr/bin/env python
from typing import Optional

import json

from database import DataBase

class CLI:
	@staticmethod
	def get_university_id(con, cur) -> Optional[str]:
		universities_data = list(cur.execute('''SELECT id, en_name, year, semester FROM universities_data'''))

		print('-'*10)
		i = 0
		for i in range(len(universities_data)):
			university = universities_data[i]
			print(f'{i}) {university[1]}-{university[2]}-{university[3]}')
		else:
			print(f'{i+1}) *NEW UNIVERSITY*')
			print(f'{i+2}) *DELETE UNIVERSITY*')
		print('-'*10)

		choice = int(input('Choose an option: '))

		if choice == i+1:
			DataBase.new_universities_table(con, cur)
			return None

		elif choice == i+2:
			DataBase.drop_table(con, cur)
			return None

		else:
			return universities_data[choice][0]

def main() -> bool:
	con, cur = DataBase.connect()
	

	id = CLI.get_university_id(con, cur)

	if not id:
		con.close()
		return True

	print('ID: '+ id)

	con.close()
	return False

if __name__ == '__main__':
	while True:
		if not main():
			break