from flask import Flask, render_template, request, redirect
import requests
from flask.helpers import url_for
import json
from jinja2 import pass_eval_context
from markupsafe import Markup, escape
from datetime import datetime
import re

from controllers import informacoes as inf

# python app.py --flask -run
# base: https://www.fbi.gov/wanted/api
app = Flask(__name__, static_folder='./assets')

@app.route('/', methods=["GET", "POST"])
def Index():
    return render_template('Principal.html')


@app.route('/casos', methods=["GET", "POST"])
def casos():
    if request.args.get('estado'):
        estado = request.args.get('estado')
        requisicao = inf.informacoesCaso(filtros = {
                'field_offices': estado
            
        })
    else:
        requisicao = inf.informacoesCaso(filtros = {
                'page': '2'
            
            })

    for x in requisicao["casos"]:
        if x['details']:
            x['details'] = re.sub('<[^<]+?>', '', x['details'])
    return render_template('casos.html', todosDados=requisicao)


@app.route('/detalhes/', methods=["GET", "POST"])
def detalhes():
    pega = None
    if request.args.get('sobre'):
        title = request.args.get('sobre')
        pega = inf.informacoesCaso(filtros = {
            'title': title
        })

    proibidinhos = ["images", "path", "race", "eyes"]

    campos = [{'mostrar': campo.replace('_', ' ').capitalize(), 'filtro': campo} for campo in pega['casos'][0] if pega['casos'][0][campo] and campo not in proibidinhos]
    if pega['casos'][0]['details']:
            pega['casos'][0]['details'] = re.sub('<[^<]+?>', '', pega['casos'][0]['details'])
    return render_template('detalhes.html', pessoa=pega, campos=campos, imagem=pega['casos'][0]['images'])


if __name__ == '__main__':
    app.run(debug=True)
