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
    requisicao = requests.request('GET', 'https://api.fbi.gov/wanted/v1/list')
    requisicao = json.loads(requisicao.content)
    # print(requisicao)
    return render_template('Principal.html', todosDados=requisicao, procurados=requisicao['items'])

if __name__ == '__main__':
    app.run(debug=True)
