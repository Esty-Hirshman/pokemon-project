from config import connection


def finds_most_owned():
    """
    finds the most owned pokemon,
    meaning the pokemon that has the highest number of owners.
    If many have the same count, return them all
    """
    with connection.cursor() as cursor:
        query = "SELECT pokemon.name " \
                "FROM pokemon JOIN owned_by " \
                "WHERE owned_by.pokemon = pokemon.id " \
                "GROUP BY owned_by.pokemon " \
                "HAVING COUNT(*) = (" \
                "SELECT MAX(tr) FROM (SELECT pokemon, COUNT(*) as tr FROM owned_by GROUP BY pokemon) as max);"
        cursor.execute(query)
        result = cursor.fetchall()
        return [pokemon["name"] for pokemon in result]


if __name__ == '__main__':
    print(finds_most_owned())
