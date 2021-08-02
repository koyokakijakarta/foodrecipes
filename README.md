# Food Recipes Apps

A food recipes application that serves to display various food recipes.

## Module used

[![Flask](https://img.shields.io/badge/Flask-gray)](https://flask.palletsprojects.com/en/2.0.x/)
[![Celery](https://img.shields.io/badge/Celery-red)](https://docs.celeryproject.org/en/stable/)
[![PyMySQL](https://img.shields.io/badge/PyMySQL-orange)](https://pymysql.readthedocs.io/en/latest/)
[![PyJWT](https://img.shields.io/badge/PyJWT-red)](https://pyjwt.readthedocs.io/en/stable/)
[![Faker](https://img.shields.io/badge/Faker-blue)](https://faker.readthedocs.io/en/master/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-purple)](http://cloudinary.com/documentation/django_integration)
[![Flask-Celery](https://img.shields.io/badge/Flask-Celery-red)](https://flask.palletsprojects.com/en/2.0.x/patterns/celery/)
[![Flask SQLAlchemy](https://img.shields.io/badge/Flask-SQLAlchemy-yellow)](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
[![Flask Migrate](https://img.shields.io/badge/Flask-Migrate-blue)](https://flask-migrate.readthedocs.io/en/latest/)
[![Flask Marshmallow](https://img.shields.io/badge/Flask-Marshmallow-inactive)](https://flask-marshmallow.readthedocs.io/en/latest/)
[![Flask Mail](https://img.shields.io/badge/Flask-Mail-white)](https://flask-mail.readthedocs.io/en/latest/)

## Requirements

- Python
- Redis
- MySQL

## Installation

Clone the project repository via github:
```
$ git clone git@github.com/koyokakijakarta/foodrecipes.git
```
Another altertive is download the zip tarball and extract it somewhere in your box.

Run ```py -m venv env```
```
$ py -m venv env
```

Once you’ve created a virtual environment, you may activate it.

On Windows, run:
```
> env\Scripts\activate.bat
```

On Unix or MacOS, run:
```
$ source env/bin/activate
```

Run ```pip install -r requirements.txt``` to install requirements module.
```
(env) $ pip install -r requirements.txt
```

## Environment Variables

Environment variables are located in ```.env```

### UPLOAD_TO

The value is **CLOUDINARY** or **IMGBB** or **else (local)**

### UPLOAD_FOLDER

If ```UPLOAD_TO``` environment variable is local, it is used.

### CLOUDINARY_NAME

Your Cloudinary Name, if is used.

### CLOUDINARY_API_KEY

Your Cloudinary Api Key, if is used.

### CLOUDINARY_API_SECRET

Your Cloudinary Api Secret, if is used.

### IMGBB_API_KEY

You can get the api key in this link : [api.imgbb.com](https://api.imgbb.com/)

### SQLALCHEMY_DATABASE_URI
Change from:
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://@127.0.0.1:3306/foodrecipes
```
to:
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<username>:<password>@<hostname>:<port>/<tablename>
```
or:
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<username>@<hostname>:<port>/<tablename>
```

### JWT_SECRET

Your [JWT](https://jwt.io/) Secret Key for token authentication.

## Usage and Examples

To create table and update data from dummy data run ```flask db upgrade```:
```
(env) $ flask db upgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> d1c2b0c1d4c5, user and recipe table
```

Run server:
```
(env) $ flask run
 * Serving Flask app 'main.py' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-456-789
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

And for remove table, you can run ```flask db downgrade```
```
(env) $ flask db downgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade d1c2b0c1d4c5 -> , user and recipe table
```

You can deactivate a virtual environment by typing “deactivate” in your shell. The exact mechanism is platform-specific and is an internal implementation detail (typically a script or shell function will be used).
```
(env) $ deactivate
$ 
```

## Entity Relationship Diagram Database

<table>
  <thead>
    <tr>
      <th colspan="2">Source</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="center"><img src="https://cdn.holistics.io/logo-dbdiagram-notext.ico" width="50"/></td>
      <td valign="center">dbdiagram.io</td>
      <td valign="center">
        <a href="https://dbdiagram.io/d/60e37a6b0b1d8a6d3967ec42">https://dbdiagram.io/d/60e37a6b0b1d8a6d3967ec42</a>
      </td>
    </tr>
  </tbody>
</table>

## API Documentation

<table>
  <thead>
    <tr>
      <th colspan="2">Source</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td valign="center"><img src="https://www.postman.com/favicon-32x32.png" width="50"/></td>
      <td valign="center">Postman</td>
      <td valign="center">
        <a href="https://god.postman.co/run-collection/58c3653958a1ae6967ef?action=collection%2Fimport#?env%5BFood%20Recipes%20Apps%5D=W3sia2V5IjoiaG9zdG5hbWUiLCJ2YWx1ZSI6ImxvY2FsaG9zdCIsImVuYWJsZWQiOnRydWV9LHsia2V5IjoicG9ydCIsInZhbHVlIjoiNTAwMCIsImVuYWJsZWQiOnRydWV9LHsia2V5IjoidG9rZW4iLCJ2YWx1ZSI6ImV5SjBlWEFpT2lKS1YxUWlMQ0poYkdjaU9pSklVekkxTmlKOS5leUoxYzJWeWJtRnRaU0k2SW1Ga2JXbHVJaXdpY0dGemMzZHZjbVFpT2lKaFpHMXBiaUlzSW1WNGNDSTZNVFl5T0RZME9Ea3lNMzAuTVBURFBOMmFzOGdLUlQxUlRwd0RxVDlIY1VWODhEWVNyUEVDbkhiZHp0SSIsImVuYWJsZWQiOnRydWV9XQ==">
          <img src="https://run.pstmn.io/button.svg"/>
        </a>
      </td>
    </tr>
  </tbody>
</table>
