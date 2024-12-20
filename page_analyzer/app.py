import os
from urllib.parse import urlparse

import requests
import validators
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.check_repository import CheckRepository
from page_analyzer.db import get_connection
from page_analyzer.url_repository import UrlRepository

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


def analyzer(url):
    try:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            url_code = r.status_code
            bs = BeautifulSoup(r.text, "lxml")
            h1 = bs.find('h1').string if bs.find('h1') else ''
            title = bs.find('title').string if bs.find('title') else ''
            meta = bs.find('meta', {"name": "description"})
            description = meta.attrs.get('content', '') if meta else ''
            return url_code, h1, title, description
        return None
    except requests.exceptions.ConnectionError:
        return None
    

def get_normalyze_url(input_url): 
    parsed_url = urlparse(input_url)
    norm_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return norm_url


@app.get('/')
def url_new():
    return render_template('index.html', url=''), 200


@app.route('/urls')
def urls_get_all():
    repo_url = UrlRepository(get_connection(app.config['DATABASE_URL']))
    url_check_repo_all = repo_url.get_content_with_last_date()
    return render_template(
        'view.html',
        urls=url_check_repo_all
    ), 200


@app.route('/urls', methods=['POST'])
def urls_post():
    input_url = request.form.get('url')
    if not validators.url(input_url):
        flash('Некорректный URL', 'error')
        return render_template('index.html', url=input_url), 422
    repo_url = UrlRepository(get_connection(app.config['DATABASE_URL']))
    norm_url = get_normalyze_url(input_url)
    url_repo = repo_url.find_name(norm_url)
    if url_repo is None:
        id = repo_url.save(norm_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('urls_get', id=id), 302)
    else:
        id = url_repo['id']
        flash('Страница уже существует', 'exists')
        return redirect(url_for('urls_get', id=id), 302)

        
@app.route('/urls/<int:id>')
def urls_get(id):
    repo_url = UrlRepository(get_connection(app.config['DATABASE_URL']))
    repo_check = CheckRepository(get_connection(app.config['DATABASE_URL']))
    url = repo_url.find_id(id)
    checks = repo_check.find_id(id)
    return render_template(
        'show.html',
        url=url,
        checks=checks
    ), 200


@app.route('/urls/<int:id>/checks', methods=['POST'])
def urls_check(id):
    repo_url = UrlRepository(get_connection(app.config['DATABASE_URL']))
    url = repo_url.find_id(id)['name']
    if analyzer(url) is not None:
        url_code, h1, title, description = analyzer(url) 
        repo_check = CheckRepository(get_connection(app.config['DATABASE_URL']))
        repo_check.save(id, url_code, h1, title, description)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('urls_get', id=id), 302)
    flash('Произошла ошибка при проверке', 'error')
    return redirect(url_for('urls_get', id=id), 302)
