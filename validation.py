from typing import List, Tuple, Dict, Any, Optional

class FormDataValidation:
	def __init__(self, majors_data: List[Any], REGIONS: List[Tuple[str, str]], gettext) -> None:
		self.majors_count = len(majors_data)
		self.majors_data = [{'id': d['id'], 'CGP': d['CGP'], 'GAT': d['GAT'], 'Achievement': d['Achievement'], 'STEP': d['STEP']} for d in majors_data]
		#HACK remove int() after fixing the database
		self.majors_sex = [(major['id'], int(major['sex'])) for major in majors_data]
		self.REGIONS_codes = [code for code, _ in REGIONS]

		self.gettext = gettext

	def major(self, sex: int, major: int) -> Tuple[bool, Optional[str]]:
		print(f'sex: {sex} major:{major}')
		print(self.majors_sex)
		if sex not in [1, 2]:
			pass
		#FIXME when major for bot sexes (sex = 0)
		elif (major, sex) in self.majors_sex:
			return True, None
		return False, self.gettext('Major incompatible with sex value.')

	def CGP(self, CGP: float) -> Tuple[bool, Optional[str]]:
		if 0<=CGP<=100:
			return True, None
		return False, self.gettext('CGP value error.')

	def GAT(self, GAT: int) -> Tuple[bool, Optional[str]]:
		if 0<=GAT<=100:
			return True, None
		return False, self.gettext('GAT value error.')

	def Achievement(self, Achievement: int) -> Tuple[bool, Optional[str]]:
		if 0<=Achievement<=100:
			return True, None
		return False, self.gettext('Achievement value error.')

	def STEP(self, STEP: int) -> Tuple[bool, Optional[str]]:
		if 0<=STEP<=100:
			return True, None
		return False, self.gettext('STEP value error.')

	def region(self, region: str) -> Tuple[bool, Optional[str]]:
		if region in self.REGIONS_codes:
			return True, None
		return False, self.gettext('Region value error.')


	#Forms functions
	def home_page_form(self, args) -> Tuple[bool, list[str]]:
		valid: Dict[int, bool] = dict()
		flashes: list[str] = []

		#TODO use the flash as True or False

		valid[0], flash = self.major(args[0], args[1])
		if flash: flashes.append(flash)
		valid[1], flash = self.CGP(args[2])
		if flash: flashes.append(flash)
		valid[2], flash = self.GAT(args[3])
		if flash: flashes.append(flash)
		valid[3], flash = self.Achievement(args[4])
		if flash: flashes.append(flash)
		valid[4], flash = self.STEP(args[4])
		if flash: flashes.append(flash)
		valid[5], flash = self.region(args[4])

		return all(valid.values()), flashes

	def __call__(self, *args, form_name: str = '') -> Tuple[bool, list[str]]:

		if form_name == 'home_page_form':
			valid, flashes = self.home_page_form(args)

		return valid, flashes