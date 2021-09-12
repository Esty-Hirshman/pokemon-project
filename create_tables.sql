USE db_pokemon;


CREATE TABLE pokemon(
    id INTEGER,
    name VARCHAR (20),
    height INTEGER,
    weight INTEGER,
    PRIMARY KEY(id)
);

CREATE TABLE pokemon_type(
    pokemon INTEGER ,
    type VARCHAR (20),
    PRIMARY KEY (pokemon,type),
    FOREIGN KEY (pokemon) REFERENCES pokemon(id)
    

);
CREATE TABLE trainer(
    name VARCHAR (20) PRIMARY KEY,
    town VARCHAR(20)
);

CREATE TABLE owned_by(
    pokemon INTEGER,
    trainer VARCHAR(20),
    PRIMARY KEY(pokemon, trainer),
    FOREIGN KEY (pokemon) REFERENCES pokemon(id),
    FOREIGN KEY (trainer) REFERENCES trainer(name)
); 



