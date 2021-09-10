from database import DataBase
from base64 import b64encode
from random import randint
from captcha.image import ImageCaptcha
from flask_babel import Babel, gettext, ngettext
from flask import Flask, render_template, url_for, request, session, redirect, flash, g
from typing import List, Optional, Any
import logging
import json
env = __import__('dotenv').dotenv_values()


app = Flask(__name__)
babel = Babel(app)

app.config['SECRET_KEY'] = env['SECRET_KEY']

# Localization things
app.config['LANGUAGES'] = {
	'ar': 'Arabic',
	'en': 'English'
}
RTL_LANGUAGES = [
	'ar'
]
# REGIONS = [
# 	('MC', 'Mecca Region'),
# 	('RD', 'Riyadh Region'),
# 	('ES', 'Eastern Region '),
# 	('AS', 'Asir Region'),
# 	('JZ', 'Jizan Region'),
# 	('MD', 'Medina Region'),
# 	('QS', 'Al-Qassim Region'),
# 	('TB', 'Tabuk Region'),
# 	('HL', 'Ha\'il Region'),
# 	('NJ', 'Najran Region'),
# 	('JF', 'Al-Jawf Region'),
# 	('BH', 'Al-Bahah Region'),
# 	('NB', 'Northern Borders Region')
# ]
app.config['BABEL_DEFAULT_LOCALE'] = 'en'


@babel.localeselector
def get_locale() -> Optional[str]:
	try:
		return session['language']
	except KeyError:
		return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


# DataBase connection
def get_database() -> tuple:
	if ('database_con' not in g) and ('database_cur' not in g):
		g.database_con, g.database_cur = DataBase.connect()
		print('DataBase connected!')

	return g.database_con, g.database_cur


def get_university_data() -> str:
	if not hasattr(g, 'university_data'):
		con, cur = get_database()
		#id, en_name, ar_name, year, semester, majors_data_json, create_time
		g.university_data = DataBase.get_university_data(
			con, cur, env['DATABASE_ID'])
	return g.university_data


# Close DataBase when idle
@app.teardown_appcontext
def close_database(error):
	con = g.pop('database_con', None)
	cur = g.pop('database_cur', None)

	if con is not None:
		con.close()
		print('DataBase closed!')


# Generate Captcha
def get_captcha() -> tuple:
	image = ImageCaptcha(width=187, height=60)
	captcha_text = str(randint(99999, 999999))
	captcha_image = b64encode(image.generate(
		captcha_text, 'jpeg').getvalue()).decode()
	return captcha_image, captcha_text


@app.route('/', methods=['GET', 'POST'])
def home():
	university_data = get_university_data()

	if request.method == 'POST':
		session['student_id'] = ''
		return redirect(url_for('home'))
	# CONT

	# Get regions
	# REGIONS_localized = [(code, gettext(name)) for code, name in REGIONS]
	REGIONS_localized = [
		('MC', gettext('Mecca Region')),
		('RD', gettext('Riyadh Region')),
		('ES', gettext('Eastern Region ')),
		('AS', gettext('Asir Region')),
		('JZ', gettext('Jizan Region')),
		('MD', gettext('Medina Region')),
		('QS', gettext('Al-Qassim Region')),
		('TB', gettext('Tabuk Region')),
		('HL', gettext('Ha\'il Region')),
		('NJ', gettext('Najran Region')),
		('JF', gettext('Al-Jawf Region')),
		('BH', gettext('Al-Bahah Region')),
		('NB', gettext('Northern Borders Region'))
	]

	# Generate Captcha
	captcha_image, captcha_text = get_captcha()
	session["CAPTCHA_TEXT"] = captcha_text

	return render_template('home.html',
						CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys())),
						RTL_LANGUAGES=RTL_LANGUAGES,
						CODE_NAME=university_data[1],
						EN_NAME=university_data[2],
						AR_NAME=university_data[3],
						YEAR=university_data[4],
						SEMESTER=university_data[5],
						MAJORS_DATA=json.loads(university_data[6]),
						REGIONS=REGIONS_localized,
						CAPTCHA_IMAGE=captcha_image,
						#University code name
						PAGE_META_TITLE=gettext('Acceptance | Participate') ,
						PAGE_TITLE=gettext('%s Acceptance') % university_data[1])

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	# CONT
	return render_template('edit.html')


@app.route('/statics')
def statistics():
	# CONT
	return render_template('statics.html')


@app.route('/about')
def about():
	# CONT
	return render_template('about.html')


@app.route('/locale', methods=['POST', 'GET'])
def set_locale():
	if request.method == 'POST':
		language = request.form.get('language')

		if language in app.config['LANGUAGES'].keys():
			session['language'] = language

		return redirect(url_for('home'))

	else:
		return render_template('locale.html',
							   CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(
								   app.config['LANGUAGES'].keys())),
							   RTL_LANGUAGES=RTL_LANGUAGES)

# CONT
