from flask import Flask, render_template, request, redirect
import requests
from flask.helpers import url_for
import json
from jinja2 import pass_eval_context
from markupsafe import Markup, escape
from datetime import datetime
import re

# python app.py --flask -run
# base: https://www.fbi.gov/wanted/api
app = Flask(__name__, static_folder='./assets')

""" @app.route('/detalhes/')
def hello_world():  # put application's code here
    cp = request.args.get('cap')
    livro = loadDados()[cp]
    # print(livro)
    return render_template('app.html', texto=livro)
"""


@app.route('/', methods=["GET", "POST"])
def Index():
    return render_template('Principal.html')


@app.route('/casos', methods=["GET", "POST"])
def casos():
    requisicao = requests.request('GET', 'https://api.fbi.gov/wanted/v1/list', params = {
            'page': '2'
        })
    requisicao = json.loads(requisicao.content)
    # print(requisicao)
    for x in requisicao['items']:
        if x['details']:
            x['details'] = re.sub('<[^<]+?>', '', x['details'])
    return render_template('casos.html', todosDados=requisicao, procurados=requisicao['items'])


@app.route('/detalhes/', methods=["GET", "POST"])
def detalhes():
    pega = None
    if request.args.get('sobre'):
        title = request.args.get('sobre')
        pega = requests.get('https://api.fbi.gov/wanted/v1/list', params = {
            'title': title
        }).json()

    


    proibidinhos = ['images', '@id', 'path', 'title', 'files', 'uid']
    campos = [{'mostrar': campo.replace('_', ' ').capitalize(), 'filtro': campo} for campo in pega['items'][0] if pega['items'][0][campo] and campo not in proibidinhos]
    if pega['items'][0]['details']:
            pega['items'][0]['details'] = re.sub('<[^<]+?>', '', pega['items'][0]['details'])
    return render_template('detalhes.html', pessoa=pega, campos=campos, imagem=pega['items'][0]['images'])


if __name__ == '__main__':
    app.run(debug=True)
