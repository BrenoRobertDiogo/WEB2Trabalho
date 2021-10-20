from flask import Flask, render_template, request, redirect
import requests
from flask.helpers import url_for
import json

# python app.py --flask -run
# base: https://www.fbi.gov/wanted/api
app = Flask(__name__)

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
    return render_template('casos.html', todosDados=requisicao, procurados=requisicao['items'])


@app.route('/detalhes/', methods=["GET", "POST"])
def detalhes():
    pega = None
    if request.args.get('sobre'):
        title = request.args.get('sobre')
        pega = requests.get('https://api.fbi.gov/wanted/v1/list', params = {
            'title': title
        }).json()
    proibidinhos = []
    campos = [{'mostrar': campo.replace('_', ' '), 'filtro': campo} for campo in pega['items'][0] if pega['items'][0][campo] and campo not in proibidinhos]
    return render_template('detalhes.html', pessoa=pega, campos=campos)


if __name__ == '__main__':
    app.run(debug=True)
