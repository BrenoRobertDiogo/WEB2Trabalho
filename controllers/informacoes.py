from json import loads, dumps
from requests import get

urlApi = "https://api.fbi.gov/wanted/v1/list"

def buscaDados(filtros={}):
    try:
        dados = get(urlApi, params=filtros)
        if dados.status_code == 200:
            return dados
        else:
            raise Exception("Houve algum erro desconhecido, tente novamente mais tarde")
    except Exception as statusError:
        return None

def tratamentoDados(dados):
    infos = ["title", "details", "reward_text", "subjects", "description", "race", "images", "hair", "caution", "field_offices", "scars_and_marks", "aliases", "race_raw", "suspects", "legat_names", "eyes", "possible_countries", "additional_information", "remarks", "path", "sex", "eyes_raw", "possible_states", "race", "warning_message"]

    retorno = []
    for x in dados:
        caso = {}
        for y in range(len(infos)):
            caso[infos[y]] = x[infos[y]]
        retorno.append(caso)
    return retorno

def informacoesCaso(filtros={}):
    dados = tratamentoDados(buscaDados(filtros).json()["items"])
    return dados
