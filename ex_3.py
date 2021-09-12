from config import connection


def find_owners(pokemon_name):
    """
    receives the name of a pokemon,
    and returns the names of all the trainers that own it,
    or an empty array if no one owns it
    :param pokemon_name: name of pokemon
    """
    with connection.cursor() as cursor:
        query = "SELECT trainer FROM owned_by JOIN pokemon WHERE owned_by.pokemon = pokemon.id and pokemon.name = %s"
        cursor.execute(query, pokemon_name)
        result = cursor.fetchall()
        return [trainer["trainer"] for trainer in result]


if __name__ == '__main__':
    print(find_owners("esty"))
