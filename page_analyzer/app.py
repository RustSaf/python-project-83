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

import validators

from urllib.parse import urlparse

from page_analyzer.url_repository import UrlRepository

from page_analyzer.check_repository import CheckRepository

try:
    from dotenv import load_dotenv

    load_dotenv('.env.dev')
except ModuleNotFoundError:
    pass


app = Flask(__name__)
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#DATABASE_URL = os.getenv('DATABASE_URL')
#app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
#print(DATABASE_URL)
DATABASE_URL = os.environ.get('DATABASE_URL')
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


conn = psycopg2.connect(DATABASE_URL)
repo_url = UrlRepository(conn)
repo_check = CheckRepository(conn)

# @app.route('/')
# def urls_index():
#    term = request.args.get('query')
#    if term:
#        users = repo.get_by_term(search_term=term)
#    else:
#        users = repo.get_content()
#    return render_template('users/index.html', search=term, users=users)


@app.get('/')
def url_new():
    return render_template('index.html', url='', messages='')


@app.route('/urls')
def urls_get_all():
    # url_repo_all = repo_url.get_content()
    # check_repo_all = repo_check.get_content()
    url_check_repo_all = repo_url.get_content_with_last_date()
    return render_template(
        'view.html',
        urls=url_check_repo_all
    )


@app.route('/urls', methods=['POST'])
def urls_post():
    input_url = request.form.get('url')
    if validators.url(input_url):
        parsed_url = urlparse(input_url)
        norm_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        url_repo = repo_url.find_name(norm_url)
        if url_repo is None:
            id = repo_url.save(norm_url)
            flash('Страница успешно добавлена', 'success')
            return redirect(f'urls/{id}'), 302
        else:
            id = url_repo['id']
            flash('Страница уже существует', 'exists')
            return redirect(f'urls/{id}'), 302
    else:
        flash('Некорректный URL', 'error')
        return render_template('index.html', url=input_url), 422


@app.route('/urls/<int:id>')
def urls_get(id):
    url = repo_url.find_id(id)
    checks = repo_check.find_id(id)
#    url_repo_all = repo_url.get_content()
#    checks = repo_check.find_id(id)
#    messages = get_flashed_messages(with_categories='True')
#    print(messages)
    return render_template(
        'show.html',
        url=url,
        checks=checks
    )


@app.route('/urls/<int:id>/checks', methods=['POST'])
def urls_check(id):
    repo_check.save(id)
#    url = repo_url.find_id(id)
#    print(checks)
    flash('Страница успешно проверена', 'success')
    return redirect(f'/urls/{id}'), 302
#    return redirect(f'urls/{id}'), 302
#    return render_template(
#        'show.html',
#        url=url,
#        checks=checks,
#        messages=messages
#    ), 302
