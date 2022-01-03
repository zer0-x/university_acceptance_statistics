"""Main code to run the web server."""

from typing import Optional
# import logging
import json
from random import randint
from secrets import token_hex
from base64 import b64encode
from urllib.parse import quote

from flask import (Flask, render_template, url_for, request, session, redirect,
                   flash, g)
from flask_babel import Babel, gettext
from captcha.image import ImageCaptcha

from database import DataBase
from validation import FormDataValidation

env = __import__('dotenv').dotenv_values()


app = Flask(__name__)
babel = Babel(app)

app.config['SECRET_KEY'] = env['SECRET_KEY']

# Localization things
app.config['LANGUAGES'] = {
    'ar': 'العَرَبيَّة',
    'en': 'English'
}
RTL_LANGUAGES = [
    'ar'
]
REGIONS = [
    ('MC', 'Mecca Region'),
    ('RD', 'Riyadh Region'),
    ('ES', 'Eastern Region '),
    ('AS', 'Asir Region'),
    ('JZ', 'Jizan Region'),
    ('MD', 'Medina Region'),
    ('QS', 'Al-Qassim Region'),
    ('TB', 'Tabuk Region'),
    ('HL', 'Ha\'il Region'),
    ('NJ', 'Najran Region'),
    ('JF', 'Al-Jawf Region'),
    ('BH', 'Al-Bahah Region'),
    ('NB', 'Northern Borders Region')
]
app.config['BABEL_DEFAULT_LOCALE'] = 'en'


@babel.localeselector
def get_locale() -> Optional[str]:
    """Get the user language code."""
    try:
        return session['language']
    except KeyError:
        return request.accept_languages.best_match(
            app.config['LANGUAGES'].keys())


# DataBase connection
def get_database() -> tuple:
    """Return database connection object and cursor.

    1- Check if there was no current connection and cursor.
    2- If there was not, create new.
    3- Return the connection and the cursor.
    """
    # TODO use try & except (Duck Type)
    if ('database_con' not in g) and ('database_cur' not in g):
        g.database_con, g.database_cur = DataBase.connect()
        print('DataBase connected!')

    return g.database_con, g.database_cur


def get_university_data() -> tuple:
    """Get the data from the database in a tuple."""
    con, cur = DataBase.connect()
    # id, en_name, ar_name, year, semester, majors_data_json, create_time
    university_data = DataBase.get_university_data(
        con, cur, env['DATABASE_UNIVERSITY_TABLE_ID'])

    con.close()

    return university_data


# Close DataBase
@app.teardown_appcontext
def close_database(error):
    """Close the database connection after the request ends."""
    con = g.pop('database_con', None)
    cur = g.pop('database_cur', None)
    del cur

    if con is not None:
        con.close()
        print('DataBase closed!')


# Generate Captcha
def get_captcha() -> tuple:
    """Create a captcha image then encode the image using base64."""
    image = ImageCaptcha(width=187, height=60)
    captcha_text = str(randint(99999, 999999))
    captcha_image = b64encode(image.generate(
        captcha_text, 'jpeg').getvalue()).decode()
    return captcha_image, captcha_text


# Get university and majors data
university_data = list(get_university_data())
majors_data = json.loads(university_data[6])
# Make a validation object
validate = FormDataValidation(majors_data, REGIONS, gettext)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Display a form.

    After submitting displays some thanking words and share buttons.
    """
    if 'student_id' in session:
        # Social media message for Whatsapp and Telegram
        social_media_message = gettext(f'''
New students are kindly requested to participate in this form.
Just enter your grades for the purpose of knowing the admission grades.

Year: {university_data[4]}
Semester: {university_data[5]}
{university_data[2]}

🔴This form is unofficial and completely managed by other students,
{university_data[1]} university has no hand in it🔴
''')

        return render_template('done.html',
                               CURRENT_LANGUAGE=session.get(
                                'language',
                                request.accept_languages.best_match(
                                    app.config['LANGUAGES'])),
                               # For user display
                               CURRENT_LOCAL=app.config['LANGUAGES'][
                                   session.get('language',
                                               request.accept_languages
                                               .best_match(
                                                   app.config['LANGUAGES']))],
                               RTL_LANGUAGES=RTL_LANGUAGES,
                               WEBSITE_URL=quote(request.base_url),
                               SOCIAL_MEDIA_MESSAGE=quote(
                                    social_media_message),
                               student_id=session['student_id'])

    elif request.method == 'POST':

        # Verify CAPTCHA
        if not request.form.get('CAPTCHA') == session['CAPTCHA_TEXT']:
            flash(gettext(u'Invalid CAPTCHA.'), 'error')
            return redirect(url_for('home'))

        # Form data to Vars
        sex = request.form.get('sex')
        major = request.form.get('major')
        batch = request.form.get('batch')
        CGP = request.form.get('CGP')
        GAT = request.form.get('GAT')
        Achievement = request.form.get('Achievement')
        STEP = request.form.get('STEP')
        region = request.form.get('region')
        try:
            sex = int(sex)
            major = int(major)
            batch = int(batch)
            CGP = float(CGP)
            GAT = int(GAT)
            Achievement = int(Achievement)
            STEP = int(STEP)
        except ValueError:
            flash(gettext(u'Form value error, '), 'error')
            return redirect(url_for('home'))

        # Validate form data
        flashes = validate(sex, major, batch, CGP, GAT, Achievement,
                           STEP, region, form_name='participate_form')

        if flashes:
            for flash_message in flashes:
                flash(flash_message, 'error')

            return redirect(url_for('home'))

        student_id = token_hex(16)
        session['student_id'] = student_id

        # Insert student data to database
        con, cur = get_database()
        try:
            DataBase.insert_student_data(
                                         con,
                                         cur,
                                         env['DATABASE_UNIVERSITY_TABLE_ID'],
                                         student_id,
                                         sex,
                                         major,
                                         batch,
                                         CGP,
                                         GAT,
                                         Achievement,
                                         STEP,
                                         region)
        except Exception as e:
            print(e)
            flash(gettext('Your data could not be inserted to the database,\
please try again later. (Server Error)'),
                  'error')
        else:
            flash(gettext('You data has been inserted \
to the database sucessfully.'),
                  'success')

        return redirect(url_for('home'))

    # Get regions names
    # TODO remove & uncomment after localize
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
                           CURRENT_LANGUAGE=session.get(
                            'language', request.accept_languages.best_match(
                                app.config['LANGUAGES'])),
                           CURRENT_LOCAL=app.config['LANGUAGES'][session.get(
                            'language', request.accept_languages.best_match(
                                app.config['LANGUAGES']))],  # For user display
                           RTL_LANGUAGES=RTL_LANGUAGES,
                           CODE_NAME=university_data[1],
                           EN_NAME=university_data[2],
                           AR_NAME=university_data[3],
                           YEAR=university_data[4],
                           SEMESTER=university_data[5],
                           MAJORS_DATA=majors_data,
                           REGIONS=REGIONS_localized,
                           CAPTCHA_IMAGE=captcha_image,
                           PAGE_TITLE=gettext('%s Acceptance') %
                            university_data[1])


@app.route('/statics')
def statistics():
    """Show some statics and numbers  according to the collected data."""
    # TODO Statistics page
    return render_template('statics.html')


@app.route('/about')
def about():
    """Credits, license, disclaimers and etc..."""
    # TODO About page
    return render_template('about.html')


@app.route('/locale', methods=['POST', 'GET'])
def set_locale():
    """Form to choose between the available languages."""
    if request.method == 'POST':
        language = request.form.get('language')

        if language in app.config['LANGUAGES'].keys():
            session['language'] = language

        return redirect(url_for('home'))

    else:
        return render_template('locale.html',
                               CURRENT_LANGUAGE=session.get(
                                 'language',
                                 request.accept_languages.best_match(
                                     app.config['LANGUAGES'])),
                               # For user display
                               CURRENT_LOCAL=app.config['LANGUAGES'][
                                   session.get(
                                     'language',
                                     request.accept_languages.best_match(
                                         app.config['LANGUAGES']))],
                               AVAILABLE_LOCALS=app.config['LANGUAGES']
                               .items(),
                               RTL_LANGUAGES=RTL_LANGUAGES)
