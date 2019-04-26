from flask import render_template, request
from werkzeug.utils import redirect

from degrading_pastebin import app
from hashlib import sha256

from degrading_pastebin.words import adjectives, waste_categories, waste_synonyms

pastes = {}


@app.route('/<adj1>/<adj2>/<adj3>/<category>/<synonym>')
def paste(adj1: str, adj2: str, adj3: str, category: str, synonym: str):
    key = '{}/{}/{}/{}/{}'.format(adj1, adj2, adj3, category, synonym)
    if key in pastes:
        content = pastes[key]
        pastes[get_next_iteration(key)] = content
        del pastes[key]

        return render_template('paste.html', content=content)
    else:
        next_iteration = get_next_iteration(key)
        return render_template('not_found.html', url='/{}'.format(next_iteration)), 404


@app.route('/waste', methods=['POST'])
def new_waste():
    content = request.form.get('content', default='')
    url = get_next_iteration(content)
    pastes[url] = content
    return redirect(url, code=302)


def get_next_iteration(url):
    digest = sha256(bytes(url, 'utf-8')).hexdigest()
    result = ''
    for i in range(3):
        index = int(digest[i * 2: i * 2 + 2], 16)
        result += '{}/'.format(adjectives[index])

    index = int(digest[6: 7], 16)
    result += '{}/'.format(waste_categories[index])

    index = int(digest[7: 8], 16)
    result += waste_synonyms[index]

    return result


@app.route('/')
def input_form():
    return render_template('input_form.html')
