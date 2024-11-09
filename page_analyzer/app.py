import os

from flask import (
    get_flashed_messages,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)

import psycopg2

from dotenv import load_dotenv

#from user_repository import UserRepository

#from validator import validate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
repo = UserRepository(conn)


@app.route('/users')
def users_index():
    term = request.args.get('query')
    if term:
        users = repo.get_by_term(search_term=term)
    else:
        users = repo.get_content()
    return render_template('users/index.html', search=term, users=users)


@app.route('/user/<int:id>')
def users_show(id):
    user = repo.find(id)
    if user is None:
        flash('User is not exist', 'error')
        render_template('users/show.html', user={})
    return render_template('users/show.html', user=user)


@app.route('/users/new')
def users_new():
    return render_template('users/new.html', user={}, errors={})


@app.route('/users', methods=['POST'])
def users_post():
    data = request.form.to_dict()
#    users = session.setdefault('users_list', [])
#    errors = validate(users, user)
    errors = validate(data)

    if not errors:
        user = {'name': data['name'], 'email': data['email']}
        repo.save(user)
        flash('User was added successfully', 'success')
        return redirect(url_for('users_index'))

    return render_template('users/new.html', user=data, errors=errors), 422
