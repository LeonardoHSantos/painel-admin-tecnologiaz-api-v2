import requests

from base_process.data_aux.var_aux import URL_HTTP
from base_process.process.prepare_data.prepareData import PrepareData


def auth_broker(identifier, password):
    data = {
        "identifier": identifier,
        "password": password
    }
    auth = PrepareData.convert_data_to_json(requests.post(url=URL_HTTP, data=data).content)
    return auth