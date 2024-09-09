-- Enums

CREATE TYPE funcao_personagem AS ENUM ('Inimigo', 'Amigo', 'Boss', 'Fire_Keeper');

CREATE TYPE tipo_fraqueza AS ENUM ('Fogo', 'Espada', 'Magia');

CREATE TYPE tipo_personagem AS ENUM ('PC', 'NPC');

CREATE TYPE tipo_equipamento AS ENUM ('Arma', 'Armadura');

CREATE TYPE tipo_consumivel AS ENUM ('Impulso', 'Pocao');

CREATE TYPE tipo_item AS ENUM ('Consumivel', 'Equipamento');

CREATE TYPE status_npc AS ENUM ('vivo', 'morto');



-- Tabela de personagem

CREATE TABLE IF NOT EXISTS personagem (

    id_personagem SERIAL PRIMARY KEY,

    tipo tipo_personagem NOT NULL

);



-- Tabela regiao

CREATE TABLE IF NOT EXISTS regiao (

    id_regiao SERIAL PRIMARY KEY,

    nome VARCHAR(30) UNIQUE NOT NULL

);



-- Tabela area

CREATE TABLE IF NOT EXISTS area (

    id_area SERIAL PRIMARY KEY,

    nome VARCHAR(30) UNIQUE NOT NULL,

    id_regiao INTEGER REFERENCES regiao(id_regiao)

);



-- Tabela NPC

CREATE TABLE IF NOT EXISTS npc (

    id_npc INTEGER PRIMARY KEY REFERENCES personagem(id_personagem),

    nome VARCHAR(30) NOT NULL,

    vida INTEGER NOT NULL,

    funcao funcao_personagem NOT NULL,

    resistencia INTEGER NOT NULL,

    tipo BOOLEAN NOT NULL,

    status status_npc,

    fraqueza tipo_fraqueza,

    CONSTRAINT chk_vida CHECK (vida >= 1),

    CONSTRAINT chk_resistencia CHECK (resistencia >= 0)

);



-- Tabela inimigo

CREATE TABLE IF NOT EXISTS inimigo (

    id_inimigo INTEGER PRIMARY KEY REFERENCES npc(id_npc),

    ataque INTEGER NOT NULL,

    CONSTRAINT check_ataque CHECK (ataque >= 1)

);



-- Tabela boss

CREATE TABLE IF NOT EXISTS boss (

    id_boss INTEGER PRIMARY KEY REFERENCES npc(id_npc),

    ataque INTEGER NOT NULL,

    drops INTEGER NOT NULL,

    CONSTRAINT check_ataque CHECK (ataque >= 1),

    CONSTRAINT check_drops CHECK (drops >= 0)

);



-- Tabela amigo

CREATE TABLE IF NOT EXISTS amigo (

    id_amigo INTEGER PRIMARY KEY REFERENCES npc(id_npc)

);



-- Tabela fire_keeper

CREATE TABLE IF NOT EXISTS fire_keeper (

    id_firekeeper INTEGER PRIMARY KEY REFERENCES npc(id_npc),

    disponivel BOOLEAN NOT NULL

);



-- Tabela Instancia_de_npc

CREATE TABLE IF NOT EXISTS instancia_npc (

    id_instancia SERIAL PRIMARY KEY,

    id_npc INTEGER NOT NULL,

    id_area INTEGER NOT NULL,

    CONSTRAINT fk_npc FOREIGN KEY(id_npc) REFERENCES npc(id_npc),

    CONSTRAINT fk_area FOREIGN KEY(id_area) REFERENCES area(id_area)

);



-- Tabela viagem_area

CREATE TABLE IF NOT EXISTS viagem_area (

    id_origem INTEGER REFERENCES area(id_area),

    id_destino INTEGER REFERENCES area(id_area),

    PRIMARY KEY (id_origem, id_destino)

);



-- Tabela nivel

CREATE TABLE IF NOT EXISTS nivel (

    id_nivel SERIAL PRIMARY KEY,

    n_nivel INTEGER NOT NULL,

    drops INTEGER NOT NULL,

    CONSTRAINT check_n_nivel CHECK (n_nivel >= 0),

    CONSTRAINT check_drops CHECK (drops >= 0)

);



-- Tabela pc (jogador)

CREATE TABLE IF NOT EXISTS pc (

    id_player INTEGER PRIMARY KEY REFERENCES personagem(id_personagem),

    nome VARCHAR(25) NOT NULL,

    vida INTEGER NOT NULL,

    id_nivel INTEGER REFERENCES nivel(id_nivel),

    id_area INTEGER REFERENCES area(id_area),

    vigor INTEGER NOT NULL,

    vitalidade INTEGER NOT NULL,

    destreza INTEGER NOT NULL,

    forca INTEGER NOT NULL,

    stamina INTEGER NOT NULL,

    resistencia INTEGER NOT NULL,

    nivel INTEGER NOT NULL,

    nivel_atual INTEGER NOT NULL,

    status status_npc,

    CONSTRAINT check_vida CHECK (vida >= 1),

    CONSTRAINT check_nivel CHECK (nivel >= 1),

    CONSTRAINT check_vigor CHECK (vigor >= 1),

    CONSTRAINT check_vitalidade CHECK (vitalidade >= 1),

    CONSTRAINT check_resistencia CHECK (resistencia >= 1),

    CONSTRAINT check_destreza CHECK (destreza >= 1),

    CONSTRAINT check_forca CHECK (forca >= 1),

    CONSTRAINT check_stamina CHECK (stamina >= 1),

    CONSTRAINT check_nivel_atual CHECK (nivel_atual >= 1)

);



-- Tabela item

CREATE TABLE IF NOT EXISTS item (

    id_item SERIAL PRIMARY KEY,

    nome VARCHAR(50) NOT NULL,

    valor INTEGER,

    nivel INTEGER NOT NULL,

    tipo tipo_item,

    CONSTRAINT check_valor CHECK (valor >= 0),

    CONSTRAINT check_nivel CHECK (nivel >= 1)

);



-- Tabela instancia_de_item

CREATE TABLE IF NOT EXISTS instancia_de_item (

    id_instancia_item SERIAL PRIMARY KEY,

    id_item INTEGER REFERENCES item(id_item),

    id_area INTEGER REFERENCES area(id_area)

);



-- Tabela inventario

CREATE TABLE IF NOT EXISTS inventario (

    id_inventario SERIAL PRIMARY KEY,

    id_player INTEGER REFERENCES pc(id_player),

    id_item INTEGER REFERENCES item(id_item),

    quantidade INTEGER NOT NULL,

    CONSTRAINT check_quantidade CHECK (quantidade > 0)

);



-- Tabela magia

CREATE TABLE IF NOT EXISTS magia (

    id_magia SERIAL PRIMARY KEY,

    nome VARCHAR(30) UNIQUE NOT NULL,

    dano INTEGER NOT NULL,

    tipo INTEGER NOT NULL,

    custo_mana INTEGER NOT NULL,

    descricao VARCHAR(200) NOT NULL,

    CONSTRAINT check_dano CHECK (dano >= 0),

    CONSTRAINT check_custo_mana CHECK (custo_mana >= 0)

);



-- Tabela armadura

CREATE TABLE IF NOT EXISTS armadura (

    id_armadura INTEGER PRIMARY KEY REFERENCES item(id_item),

    requisitos INTEGER[],

    durabilidade INTEGER NOT NULL,

    peso INTEGER NOT NULL,

    descricao VARCHAR(200) NOT NULL,

    resistencia INTEGER NOT NULL,

    CONSTRAINT check_peso CHECK (peso >= 0),

    CONSTRAINT check_requisitos CHECK (array_length(requisitos, 1) = 4),

    CONSTRAINT check_resistencia CHECK (resistencia >= 0),

    CONSTRAINT check_durabilidade CHECK (durabilidade >= 1)

);



-- Tabela arma

CREATE TABLE IF NOT EXISTS arma (

    id_arma INTEGER PRIMARY KEY REFERENCES item(id_item),

    requisitos INTEGER[],

    durabilidade INTEGER NOT NULL,

    peso INTEGER NOT NULL,

    descricao VARCHAR(200) NOT NULL,

    dano INTEGER NOT NULL,

    elemento INTEGER NOT NULL,

    CONSTRAINT check_peso CHECK (peso >= 0),

    CONSTRAINT check_requisitos CHECK (array_length(requisitos, 1) = 4),

    CONSTRAINT check_durabilidade CHECK (durabilidade >= 1),

    CONSTRAINT check_dano CHECK (dano >= 0),

    CONSTRAINT check_elemento CHECK (elemento >= 0)

);



-- Tabela pocao

CREATE TABLE IF NOT EXISTS pocao (

    id_pocao INTEGER PRIMARY KEY REFERENCES item(id_item),

    efeito INTEGER NOT NULL,

    CONSTRAINT check_efeito CHECK (efeito > 0)

);



-- Tabela impulso

CREATE TABLE IF NOT EXISTS impulso (

    id_impulso INTEGER PRIMARY KEY REFERENCES item(id_item),

    efeito INTEGER NOT NULL,

    CONSTRAINT check_efeito CHECK (efeito > 0)

);



-- Tabela Fala

CREATE TABLE IF NOT EXISTS fala (

    id_fala SERIAL PRIMARY KEY,

    fala VARCHAR(300) NOT NULL,

    chance DECIMAL(5, 2) NOT NULL,

    CONSTRAINT check_chance CHECK (chance >= 0 AND chance <= 1)

);



-- Tabela npcfala

CREATE TABLE IF NOT EXISTS npcfala (

    id_npcfala SERIAL PRIMARY KEY,

    id_fala INTEGER REFERENCES fala(id_fala),

    id_npc INTEGER REFERENCES npc(id_npc)

);



-- Tabela magia_personagem (para rastrear magias aprendidas pelos personagens)

CREATE TABLE IF NOT EXISTS magia_personagem (

    id_personagem INTEGER REFERENCES personagem(id_personagem),

    id_magia INTEGER REFERENCES magia(id_magia),

    PRIMARY KEY (id_personagem, id_magia)

);
