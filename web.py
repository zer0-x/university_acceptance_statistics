from typing import List, Optional, Any
import logging
import json
from os import environ
__import__('dotenv').load_dotenv()

from flask import Flask, render_template, url_for, request, session, redirect, g
from flask_babel import Babel, gettext, ngettext
from captcha.image import ImageCaptcha

from database import DataBase

app = Flask(__name__)
babel = Babel(app)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

#Localization things
app.config['LANGUAGES'] = {
	'ar': 'Arabic',
	'en': 'English'
}
RTL_LANGUAGES = [
	'ar'
]
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

@babel.localeselector
def get_locale():
	try:
		return session['language']
	except KeyError:
		return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


#DataBase connection
def get_database():
	if not hasattr(g, 'sqlite3'):
		g.database_con, g.database_cur = DataBase.connect()
	return g.database_con, g.database_cur

def get_university_data(con, cur):
	if not hasattr(g, 'university_data'):
		#id, en_name, ar_name, year, semester, majors_data_json, create_time
		g.university_data = DataBase.get_university_data(con, cur, environ.get('DATABASE_ID'))
	return g.university_data


#Close DataBase when idle
@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'database_con'):
		g.database_con.close()


@app.route('/', methods=['GET', 'POST'])
def home():
	con, cur = get_database()
	university_data = get_university_data(con, cur)

	if request.method == 'POST':
		session['student_id'] = ''
		return redirect(url_for('home'))
	#CONT

	return render_template('home.html',
							CURRENT_LANGUAGE = session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys())),
							RTL_LANGUAGES = RTL_LANGUAGES,
							CODE_NAME = university_data[1],
							EN_NAME = university_data[2],
							AR_NAME = university_data[3],
							YEAR = university_data[4],
							SEMESTER = university_data[5],
							MAJORS_DATA = json.loads(university_data[6]))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
	#CONT
	return render_template('edit.html')


@app.route('/statics')
def statics():
	#CONT
	return render_template('statics.html')


@app.route('/about')
def about():
	#CONT
	return render_template('about.html')



@app.route('/locale', methods = ['POST', 'GET'])
def set_locale():
	if request.method == 'POST':
		language = request.form.get('language')
		
		if language in app.config['LANGUAGES'].keys():
			session['language'] = language

		return redirect(url_for('home'))
	
	else:
		return render_template('locale.html',
							CURRENT_LANGUAGE = session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys())),
							RTL_LANGUAGES = RTL_LANGUAGES)

#CONT