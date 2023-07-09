
# About The Project
A small web application with a connected database.

# Build With
* Flask
* Bootstrap
* SQLite


# Getting Started

## Installation
1. Clone the repo

2. Install environement
```
conda env create -f environment. yml
pre-commit install
```
3. Set Flask environement variables
```
export FLASK_APP=project
export FLASK_DEBUG=1
```
4. Init the database
```
python init_db.py
```

# Usage
```
flask run
```

# Acknowledgments
https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
