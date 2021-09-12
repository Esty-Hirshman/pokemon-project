from config import connection
import json


def insert_data():
    """
    insert all data to tables
    """
    with open('pokemon_data.json', 'r') as file:
        data = json.load(file)
    with connection.cursor() as cursor:
        for pokemon in data:
            query_insert_pokemon = "INSERT INTO pokemon VALUES(%s, %s, %s, %s);"
            val = (pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
            cursor.execute(query_insert_pokemon, val)
            query_insert_pokemon_type = "INSERT INTO pokemon_type VALUES(%s,%s)"
            cursor.execute(query_insert_pokemon_type,(pokemon["id"],pokemon["type"]))
            for trainer in pokemon["ownedBy"]:
                query_insert_trainer = "INSERT INTO trainer VALUES(%s, %s);"
                try:
                    cursor.execute(query_insert_trainer, (trainer['name'], trainer['town']))
                except:
                    pass
                query_inset_owned_by = "INSERT INTO owned_by VALUES(%s, %s);"
                cursor.execute(query_inset_owned_by, (pokemon['id'], trainer['name']))
            connection.commit()


if __name__ == '__main__':
    insert_data()
