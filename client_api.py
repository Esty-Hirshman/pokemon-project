import requests
from config import poke_base_url


def get_pokemon(pokemon):
    """
    get pokemon by name from pokeApi
    :param pokemon: pokemon name
    """
    response = requests.get(f'{poke_base_url}/{pokemon}', verify=False)
    res_json = response.json()
    return res_json


def get_api_data(url):
    """
    get some data from pokeApi by url
    """
    response = requests.get(url, verify=False)
    return response.json()
