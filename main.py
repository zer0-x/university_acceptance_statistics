#!/usr/bin/env python

__author__ = 'zer0-x'


from typing import List, Optional, Any

import json


from database import DataBase
import web


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
			return university[choice][0]

def main() -> bool:
	con, cur = DataBase.connect()
	

	id = CLI.get_university_id(con, cur)

	if not id:
		con.close()
		return True

	id, en_name, ar_name, year, semester, majors_data_json, create_time  = next(cur.execute(
												'''SELECT * FROM universities_data WHERE id = ":id"''',
												{'id': id}))

	majors_data = json.loads(majors_data_json)
	del majors_data_json



	##CONT




	con.close()
	return False

if __name__ == '__main__':
	while True:
		if not main():
			break