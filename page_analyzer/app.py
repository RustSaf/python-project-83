import os

from flask import (
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

import requests

from bs4 import BeautifulSoup

from page_analyzer.url_repository import UrlRepository

from page_analyzer.check_repository import CheckRepository

try:
    from dotenv import load_dotenv

    load_dotenv()

except ModuleNotFoundError:
    pass


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
#app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
repo_url = UrlRepository(conn)
repo_check = CheckRepository(conn)


@app.get('/')
def url_new():
    return render_template('index.html', url='', messages='')


@app.route('/urls')
def urls_get_all():
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
            return redirect(url_for('urls_get', id=id)), 302
        else:
            id = url_repo['id']
            flash('Страница уже существует', 'exists')
            return redirect(url_for('urls_get', id=id)), 302
    else:
        flash('Некорректный URL', 'error')
        return redirect(url_for('url_new')), 303


@app.route('/urls/<int:id>')
def urls_get(id):
    url = repo_url.find_id(id)
    checks = repo_check.find_id(id)
    return render_template(
        'show.html',
        url=url,
        checks=checks
    )


@app.route('/urls/<int:id>/checks', methods=['POST'])
def urls_check(id):
    url = repo_url.find_id(id)['name']
    try:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            url_code = r.status_code
            bs = BeautifulSoup(r.text, "lxml")
            h1 = bs.find('h1').string if bs.find('h1') else ''
            title = bs.find('title').string if bs.find('title') else ''
            meta = bs.find('meta', {"name": "description"})
            description = meta.attrs.get('content', '') if meta else ''
            repo_check.save(id, url_code, h1, title, description)
            flash('Страница успешно проверена', 'success')
            return redirect(url_for('urls_get', id=id)), 302
        else:
            flash('Произошла ошибка при проверке', 'error')
            return redirect(url_for('urls_get', id=id)), 303
    except requests.exceptions.ConnectionError:
        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('urls_get', id=id)), 303
