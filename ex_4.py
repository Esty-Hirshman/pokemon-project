from config import connection


def find_roster(trainer_name):
    """
    receives the name of a trainer,
     and returns the names of all the pokemon he or she owns
    :param trainer_name: name of trainer
    """
    with connection.cursor() as cursor:
        query = "SELECT pokemon.name FROM owned_by JOIN pokemon WHERE owned_by.pokemon = pokemon.id and " \
                "owned_by.trainer = %s "
        cursor.execute(query, trainer_name)
        result = cursor.fetchall()
        return [pokemon["name"] for pokemon in result]


if __name__ == '__main__':
    print(find_roster("Loga"))
