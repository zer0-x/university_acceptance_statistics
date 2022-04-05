# University Acceptance Statistics

A simple and light Flask web app to create a simple form to collect data from new students in universities that don't publish acceptance info.


The project isn't completed. It lacks the `Statistics` page. However, you still can delete it from the flask and html code and use the project as a form only, then extract the data manually from the database as `csv` and create some statistics in something like `LibreOffice Calc`.

It seams that there is a bug in the sex valadation. Maybe at sometime I will solve it or someone will create a pullrequest or something.

# Development

## Create a virtual environment
You need to have `pipenv` installed in your system.

Create the environment with:
```
$ pipenv install
```
Then activate the environment:
```
$ pipenv shell
```

## Create a new database and a university

Before that, create a copy from `majors-example.json` and use it as a template for the university's majors list.
```
0 = both
1 = male
2 = female
```

Then, run this to get a simple cli wizard:
```
python3 universities.py
```
Don't enter the majors data manually, use the file you created before.

When you finish, you will get the university id, so copy it. You can also get it at any time by running the wizard again, also you can delete the university using the wizard.

## Create `.env` file
Copy the existing env file:
```
$ cp env .env
```

Create any secret key and add it in the `.env` file.

You can do it with python:
```
>>> import secrets
>>> secrets.token_hex()
```

Paste your university id to be the value of the `DATABASE_UNIVERSITY_TABLE_ID` key.


## Running the server
Use this command to run a local development server:
```
$ flask run
```
And if you wanted to use it on the local network you can use:
```
$ flask run --host=0.0.0.0
```
And you will need to open a port in your system's firewall.
