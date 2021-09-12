import pymysql
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Eh322367475@",
    db="db_pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

port = 3000

poke_base_url = 'https://pokeapi.co/api/v2/pokemon'

local_url = 'http://localhost:'+str(port)+'/pokemon'