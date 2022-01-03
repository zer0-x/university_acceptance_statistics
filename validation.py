"""Functions to validate form data before inserting them to the DataBase."""
from typing import List, Tuple, Any, Optional


class FormDataValidation:
    """Validation for web app form data."""

    def __init__(self, majors_data: List[Any], REGIONS: List[Tuple[str, str]],
                 gettext) -> None:
        """Add some important data to the object for validation purposes."""
        self.majors_count = len(majors_data)
        self.majors_data = [{'id': d['id'],
                             'CGP': d['CGP'],
                             'GAT': d['GAT'],
                             'Achievement': d['Achievement'],
                             'STEP': d['STEP']} for d in majors_data]
        self.majors_sex = [{major['id']:
                            major['sex']} for major in majors_data]
        self.REGIONS_codes = [code for code, _ in REGIONS]

        self.gettext = gettext

    def major(self, sex: int, major: int) -> Optional[str]:
        """Validate major and sex."""
        try:
            major_sex = self.majors_sex[major]
        except KeyError:
            return self.gettext('Major doesn\'t exist.')
        else:
            if (sex == major_sex) or (0 == major_sex):
                return None
            else:
                return self.gettext('Major incompatible with sex value.')

    def CGP(self, CGP: float) -> Optional[str]:
        """Validate CGP grade."""
        if 0 <= CGP <= 100:
            return None
        return self.gettext('CGP value error.')

    def GAT(self, GAT: int) -> Optional[str]:
        """Validate GAT grade."""
        if 0 <= GAT <= 100:
            return None
        return self.gettext('GAT value error.')

    def Achievement(self, Achievement: int) -> Optional[str]:
        """Validate Achievement grade."""
        if 0 <= Achievement <= 100:
            return None
        return self.gettext('Achievement value error.')

    def STEP(self, STEP: int) -> Optional[str]:
        """Validate STEP grade."""
        if 0 <= STEP <= 100:
            return None
        return self.gettext('STEP value error.')

    def region(self, region: str) -> Optional[str]:
        """Validate region."""
        if region in self.REGIONS_codes:
            return None
        return self.gettext('Region value error.')

    # Forms functions

    def participate_form(self, args) -> list[str]:
        """Validate data sent by the participate form."""
        flashes: list[str] = []

        flash = self.major(args[0], args[1])
        if flash:
            flashes.append(flash)
        flash = self.CGP(args[2])
        if flash:
            flashes.append(flash)
        flash = self.GAT(args[3])
        if flash:
            flashes.append(flash)
        flash = self.Achievement(args[4])
        if flash:
            flashes.append(flash)
        flash = self.STEP(args[4])
        if flash:
            flashes.append(flash)
        flash = self.region(args[4])

        return flashes

    def __call__(self, *args, form_name: str = '') -> list[str]:
        """If the return value contains a message, there is an error."""
        if form_name == 'participate_form':
            flashes = self.participate_form(args)

        return flashes
