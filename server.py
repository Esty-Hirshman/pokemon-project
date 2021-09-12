from flask import Flask, Response, request
from ex_4 import find_roster
from ex_3 import find_owners
from config import connection, port
from client_api import get_pokemon, get_api_data
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)


@app.route('/sanity')
def sanity():
    """
    Get the sever up
    :return: Response the server up
    """
    return Response("Server up and running", 200)


@app.route('/pokemon/update/<pokemon_name>', methods=['PUT'])
def update_pokemon_type(pokemon_name):
    """
    URL: http://localhost:3000/pokemon/update?pokemon_name=pokemon_name
    update a pokemon's types, access the external pokeAPI to get the types and then update the DB.
    :param pokemon_name: Pokemon to update is types
    :return: Response success or failed with the status
    """
    try:
        pokemon = get_pokemon(pokemon_name)
    except:
        return Response("failed to get pokemon", 401)
    with connection.cursor() as cursor:
        try:
            for pokemon_type in pokemon["types"]:
                query = 'INSERT INTO pokemon_type VALUES(%s,%s)'
                pokemon_type = pokemon_type["type"]
                try:
                    cursor.execute(query, (pokemon["id"], pokemon_type["name"]))
                except:
                    continue
            connection.commit()
        except:
            return Response("pokemon not in data base", 502)
        return Response("pokemon types update successfully", 201)


@app.route('/pokemon/trainersPokemon/<trainer>', methods=['GET'])
def get_pokemon_by_trainer(trainer):
    """
    URL: http://localhost:3000/pokemon/trainersPokemon?trainer=trainer
    Get all the pokemons of a given owner
    :param trainer: trainer to get there pokemon
    :return: Response with all the pokemon
    """
    try:
        res = find_roster(trainer)
        return Response(json.dumps(res), 201)
    except:
        return Response("trainer not in data base", 501)


@app.route('/pokemon/getTrainers/<pokemon>', methods=['GET'])
def get_trainers_of_pokemon(pokemon):
    """
    URL: http://localhost:3000/pokemon/getTrainers?pokemon=pokemon
    Get all the trainers of a given pokemon
    :param pokemon: pokemon to get there trainers
    :return: Response with all the trainers
    """
    try:
        return Response(json.dumps(find_owners(pokemon)), 201)
    except:
        return Response("pokemon not in data base", 501)


@app.route('/pokemon/add', methods=['POST'])
def add_new_pokemon():
    """
    URL: http://localhost:3000/pokemon/add
    Adding a new pokemon with the
    body required: json{"id": pokemon_id,
                    "name": pokemon_name,
                    "height": pokemon_height,
                    "weight": pokemon_weight,
                    "types": array_of_pokemon_types}
    :return: Response of success or failed
    """
    data = request.get_json()
    res = add_pokemon(data)
    return Response(res["text"], res["status"])


@app.route('/pokemon/type/<type>', methods=['GET'])
def get_pokemon_by_type(type):
    """
    URL: http://localhost:3000/pokemon/type?type=type
    Get all pokemons with the specific type
    :param type: to get it's pokemons
    :return: Response json of all the pokemons or fail texst on failed
    """
    with connection.cursor() as cursor:
        try:
            query = "SELECT pokemon.name FROM pokemon JOIN pokemon_type WHERE  pokemon_type.pokemon = pokemon.id and " \
                    "pokemon_type.type = %s "
            cursor.execute(query, type)
            result = cursor.fetchall()
            return Response(json.dumps([pokemon["name"] for pokemon in result]), 201)
        except:
            return Response("type is not in data base", 501)


@app.route('/pokemon/delete/<pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    """
    URL: http://localhost:3000/pokemon/delete?pokemon_id=pokemon_id
    Delete pokemon
    :param pokemon_id:pokemon to delete
    :return:Response of success or failed and the status
    """
    with connection.cursor() as cursor:
        try:
            query1 = 'DELETE FROM pokemon_type WHERE pokemon = %s'
            query2 = 'DELETE FROM owned_by WHERE pokemon = %s'
            query3 = 'DELETED FROM pokemon WHERE id = %s'
            cursor.execute(query1, pokemon_id)
            cursor.execute(query2, pokemon_id)
            cursor.execute(query3, pokemon_id)
            connection.commit()
            return Response("pokemon deleted", 201)
        except:
            return Response("pokemon to delete not in data base", 501)


@app.route('/pokemon/deleteAll/<trainer>', methods=['DELETE'])
def delete_trainers_pokemon(trainer):
    """
    URL: http://localhost:3000/pokemon/deleteAll?trainer=trainer
    Delete the pokemon of the trainer
    :param trainer: trainer to delete its pokemons
    :return: Response success massage or failed massage with the status
    """
    with connection.cursor() as cursor:
        try:
            query = 'DELETE FROM owned_by WHERE trainer = %s'
            cursor.execute(query, trainer)
            connection.commit()
        except:
            return Response("error", 401)
        return Response("trainers pokemons deleted", 201)


@app.route('/pokemon/evolve', methods=['GET'])
def get_pokemon_evolve():

    """
    URL: http://localhost:3000/pokemon/evolve?trainer=trainer_name&pokemonpokemon_name
    Get the the evolve of specific pokemon of a specific trainer
    required params: {trainer: "trainer_name", pokemon: "pokemon_name"}
    :return: Response of success or failed with the status
    """
    params = request.args
    # if given trainer does not have given pokemon
    if not trainer_has_pokemon(params["trainer"], params["pokemon"]):
        return Response(f"{params['trainer']} does not have {params['pokemon']} pokemon", 500)
    pokemon = get_pokemon(params["pokemon"])
    species = get_api_data(pokemon["species"]["url"])
    evolution_chain_info = get_api_data(species["evolution_chain"]["url"])["chain"]
    chain_name = evolution_chain_info["species"]["name"]
    while chain_name != pokemon["name"]:
        evolution_chain_info = evolution_chain_info["evolves_to"][0]
        chain_name = evolution_chain_info["species"]["name"]
    try:
        evolution_chain_info = evolution_chain_info["evolves_to"][0]
    # if pokemon can not evolve
    except:
        return Response("pokemon can not evolve", 500)
    new_pokemon_evolve = evolution_chain_info["species"]["name"]
    with connection.cursor() as cursor:
        try:
            get_id = 'SELECT id FROM pokemon WHERE name = %s'
            cursor.execute(get_id, new_pokemon_evolve)
            new_pokemon_id = cursor.fetchall()[0]
        except:
            pokemon_to_add = get_pokemon(evolution_chain_info)
            add_pokemon(pokemon_to_add)
        try:
            query = 'UPDATE owned_by SET pokemon = %s WHERE trainer = %s and pokemon = ' \
                    '(SELECT id FROM pokemon WHERE name = %s)'
            values = (new_pokemon_id["id"], params["trainer"], pokemon["name"])
            cursor.execute(query, values)
        except:
            return Response(
                f"{params['pokemon']} evolved to {new_pokemon_evolve} , and {params['trainer']} already has this pokemon",
                201)
        connection.commit()
        return Response(f"pokemon {params['pokemon']} evolved to {new_pokemon_evolve}", 201)


def add_pokemon(pokemon):
    """
    Add a new pokemon with its types
    :param pokemon:
    :return:
    """
    with connection.cursor() as cursor:
        query = "INSERT INTO pokemon VALUES (%s, %s,%s,%s)"
        data = (pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
        try:
            cursor.execute(query, data)
        except ValueError:
            return {"text": "pokemon already exist", "status": 502}
        for type in pokemon["types"]:
            query = "INSERT INTO pokemon_type VALUES (%s,%s)"
            data = (pokemon["id"], type)
            try:
                cursor.execute(query, data)
            except ValueError:
                continue
        connection.commit()
        return {"text": "pokemon added successfully", "status": 201}


def trainer_has_pokemon(trainer, pokemon):
    with connection.cursor() as cursor:
        query = 'SELECT * FROM owned_by JOIN pokemon WHERE pokemon.id = owned_by.pokemon and pokemon.name = %s and ' \
                'owned_by.trainer = %s '
        cursor.execute(query, (pokemon, trainer))
        res = cursor.fetchall()
        return True if res else False


if __name__ == '__main__':
    app.run(port=port)
