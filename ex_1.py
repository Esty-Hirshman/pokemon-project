from config import connection


def heaviest_pokemon():
    """
    SQL query
    :return: returns the heaviest pokemon (the one with the biggest weight property)
    """
    with connection.cursor() as cursor:
        query = "SELECT name FROM pokemon WHERE weight in (SELECT MAX(weight) FROM pokemon)"
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == '__main__':
    print(heaviest_pokemon())
