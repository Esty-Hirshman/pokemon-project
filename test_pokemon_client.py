import requests
from config import local_url
from client_api import get_pokemon
from insert_data import insert_data


def test_insert_data():
    # insert data from json
    insert_data()


def test_get_pokemon_by_type():
    # get all pokemon of type "normal" and assert "eevee" is in
    response = requests.get(url=f"{local_url}/type/normal")
    response = response.json()
    assert "eevee" in response

    # update pokemon "eevee" types
    res = requests.put(url=f"{local_url}/update/eevee", )
    assert res.status_code == 201


def test_add_pokemon():
    # add pokemon "yanma" to DB asset status code is 201 - succeed
    yanma_details = get_pokemon("yanma")
    types = yanma_details["types"]
    yanma_details["types"] = [type["type"]["name"] for type in types]
    res = requests.post(url=f"{local_url}/add", json=yanma_details)
    assert res.status_code == 201

    # check if can get "yanma" by 2 types: "bug" and "flying"
    res = requests.get(f"{local_url}/type/bug")
    assert "yanma" in res.json()
    res = requests.get(f"{local_url}/type/flying")
    assert "yanma" in res.json()

    # try to add "yanma" again and assert status code is 502
    res = requests.post(url=f"{local_url}/add", json=yanma_details)
    assert res.status_code == 500


def update_pokemon_types():
    # update pokemon "venusaur" types
    res = requests.get(url=f"{local_url}/update/update")
    assert res.status_code == 201

    # assert "grass" and "poison" are in "venusaur" types
    res = requests.get(url=f"{local_url}/type/grass")
    assert "venusaur" in res.json()
    res = requests.get(url=f"{local_url}/type/poison")
    assert "venusaur" in res.json()


def test_get_pokemons_by_owner():
    # get all of "Drasna"'s pokemons
    res = requests.get(url=f'{local_url}/trainersPokemon/Drasna')
    res = res.json()
    assert res == ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff", "persian", "growlithe",
                   "machamp", "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"]


def test_get_owners_of_pokemon():
    # get all owners of "charmander" pokemon
    res = requests.get(url=f"{local_url}/getTrainers/charmander")
    assert res.json() == ["Giovanni", "Jasmine", "Whitney"]


def test_evolve_1():
    # assert "pinsir" pokemon can not evolve
    res = requests.get(f"{local_url}/evolve", params={"trainer": "Whitney", "pokemon": "pinsir"})
    assert res.status_code == 500


def test_evolve_2():
    # assert "Archie" owner does not have a "spesarow" pokemon
    res = requests.get(f"{local_url}/evolve", params={"trainer": "Archie", "pokemon": "spearow"})
    assert res.status_code == 500


def test_evolve_3():
    # assert "oddish"  evolved to ""gloom
    res = requests.get(f"{local_url}/evolve", params={"trainer": "Whitney", "pokemon": "oddish"})
    assert res.status_code == 201
    assert res.text == "pokemon oddish evolved to gloom"

    # evolve again "oddish" and make shure "Whitney" does not have "oddish" pokemon because "oddish" evolved to "gloom"
    res = requests.get(f"{local_url}/evolve", params={"trainer": "Whitney", "pokemon": "oddish"})
    assert res.status_code == 500
    assert res.text == "Whitney does not have oddish pokemon"

    # aaser "gloom" in "Whitney" pokemon
    res = requests.get(url=f'{local_url}/trainersPokemon/Whitney')
    res = res.json()
    assert "gloom" in res


def test_evolve_4():
    # assert owner "Whitney" has pokemon: "pikachu" and "raichu"
    res = requests.get(url=f'{local_url}/trainersPokemon/Whitney')
    res = res.json()
    assert "pikachu" in res and "raichu" in res

    # evolve "pikachu" to "raichu" , assert server did nothing because "Whitney" already has that pokemon
    res = requests.get(f"{local_url}/evolve", params={"trainer": "Whitney", "pokemon": "pikachu"})
    assert res.status_code == 201
    assert res.text == "pikachu evolved to raichu , and Whitney already has this pokemon"


