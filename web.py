from typing import List, Optional, Any

import logging
from os import environ
__import__('dotenv').load_dotenv()

from flask import Flask, render_template, url_for, request, session, redirect
from flask_babel import Babel, gettext, ngettext
from captcha.image import ImageCaptcha


app = Flask(__name__)
babel = Babel(app)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

app.config['LANGUAGES'] = {
	'ar': 'Arabic',
	'en': 'English'
}
RTL_LANGUAGES = [
	'ar'
]
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

#CONT

@babel.localeselector
def get_locale():
	try:
		return session['language']
	except KeyError:
		return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/', methods=['GET', 'POST'])
def home():
	#CONT
	return render_template('home.html',
							CURRENT_LANGUAGE = session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys())),
							RTL_LANGUAGES = RTL_LANGUAGES)


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