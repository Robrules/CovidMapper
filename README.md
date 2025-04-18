

## COVID Mapper

### Note

Install virtualenv with `pip install virtualenv`. Create a new virtualenv using `python -m venv .\covid_mapper\venv`.

Use the command `./venv/bin/activate` or `./venv/Scripts/activate` to activate the virtualenv, and use `deactivate` to deactivate the virtualenv.

Use the command `pip install -r requirements.txt` to install the project dependencies.

If there is any update in the dependencies, run the command `pip freeze > requirements.txt`.

After making changes to the models in the system app, run `python manage.py makemigrations system`, then run `python manage.py migrate`.

Install bootstrap-vue with the command `npm install vue bootstrap bootstrap-vue` for frontend dependencies

Testing:
`coverage run manage.py test` to test with coverage
`coverage report` to see the coverage report
