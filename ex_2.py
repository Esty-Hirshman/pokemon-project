from config import connection

def find_by_type(type):
    """
    returns all of the pokemon names with given type
    """
    with connection.cursor() as cursor:
        query = "SELECT name FROM pokemon WHERE type = %s"
        cursor.execute(query,type)
        result = cursor.fetchall()
        return [pokemon["name"] for pokemon in result]


if __name__ == '__main__':
    print(find_by_type("grass"))