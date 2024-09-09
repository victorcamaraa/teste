-- Create a new table for character creation
CREATE TABLE character_creation (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    vigor INTEGER NOT NULL DEFAULT 10,
    vitality INTEGER NOT NULL DEFAULT 10,
    endurance INTEGER NOT NULL DEFAULT 10,
    strength INTEGER NOT NULL DEFAULT 10,
    dexterity INTEGER NOT NULL DEFAULT 10,
    intelligence INTEGER NOT NULL DEFAULT 10,
    faith INTEGER NOT NULL DEFAULT 10,
    humanity INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT check_attribute_sum CHECK (
        vigor + vitality + endurance + strength + dexterity + intelligence + faith = 70
    )
);

-- Modify the PC table to include more relevant fields
ALTER TABLE pc
ADD COLUMN endurance INTEGER NOT NULL DEFAULT 10,
ADD COLUMN intelligence INTEGER NOT NULL DEFAULT 10,
ADD COLUMN faith INTEGER NOT NULL DEFAULT 10,
ADD COLUMN humanity INTEGER NOT NULL DEFAULT 0,
ADD COLUMN souls INTEGER NOT NULL DEFAULT 0,
ADD COLUMN equipped_weapon INTEGER REFERENCES arma(id_arma),
ADD COLUMN equipped_armor INTEGER REFERENCES armadura(id_armadura);

-- Create a stored procedure for character creation
CREATE OR REPLACE PROCEDURE create_character(
    p_name VARCHAR(30),
    p_vigor INTEGER,
    p_vitality INTEGER,
    p_endurance INTEGER,
    p_strength INTEGER,
    p_dexterity INTEGER,
    p_intelligence INTEGER,
    p_faith INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_character_id INTEGER;
    starting_weapon_id INTEGER;
    starting_armor_id INTEGER;
BEGIN
    -- Insert into character_creation table
    INSERT INTO character_creation (name, vigor, vitality, endurance, strength, dexterity, intelligence, faith)
    VALUES (p_name, p_vigor, p_vitality, p_endurance, p_strength, p_dexterity, p_intelligence, p_faith)
    RETURNING id INTO new_character_id;

    -- Get starting equipment
    SELECT id_arma INTO starting_weapon_id FROM arma WHERE nome = 'Espada Longa' LIMIT 1;
    SELECT id_armadura INTO starting_armor_id FROM armadura WHERE nome = 'Armadura de Couro' LIMIT 1;

    -- Insert into pc table
    INSERT INTO pc (id_player, nome, vida, id_nivel, id_area, vigor, vitalidade, destreza, forca, stamina, resistencia, nivel, nivel_atual, status, endurance, intelligence, faith, equipped_weapon, equipped_armor)
    VALUES (new_character_id, p_name, p_vigor * 10, 1, 1, p_vigor, p_vitality, p_dexterity, p_strength, p_endurance * 10, p_vitality, 1, 1, 'vivo', p_endurance, p_intelligence, p_faith, starting_weapon_id, starting_armor_id);

    -- Add starting equipment to inventory
    INSERT INTO inventario (id_player, id_item, quantidade)
    VALUES (new_character_id, starting_weapon_id, 1), (new_character_id, starting_armor_id, 1);
END;
$$;

-- Create a function to get available areas
CREATE OR REPLACE FUNCTION get_available_areas(p_current_area INTEGER)
RETURNS TABLE (id_destino INTEGER, nome_destino CHAR(30))
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT va.id_destino, a.nome
    FROM viagem_area va
    JOIN area a ON va.id_destino = a.id_area
    WHERE va.id_origem = p_current_area;
END;
$$;

-- Create a function to move the player
CREATE OR REPLACE FUNCTION move_player(p_player_id INTEGER, p_destination_id INTEGER)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    current_area INTEGER;
BEGIN
    -- Get the player's current area
    SELECT id_area INTO current_area FROM pc WHERE id_player = p_player_id;

    -- Check if the move is valid
    IF EXISTS (
        SELECT 1
        FROM viagem_area
        WHERE id_origem = current_area AND id_destino = p_destination_id
    ) THEN
        -- Update the player's location
        UPDATE pc SET id_area = p_destination_id WHERE id_player = p_player_id;
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$;

-- Create a function to get enemies in the current area
CREATE OR REPLACE FUNCTION get_enemies_in_area(p_area_id INTEGER)
RETURNS TABLE (id_inimigo INTEGER, nome CHAR(30), vida INTEGER, ataque INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT i.id_inimigo, i.nome, i.vida, i.ataque
    FROM instancia_de_inimigo ii
    JOIN inimigo i ON ii.id_npc = i.id_inimigo
    WHERE ii.id_area = p_area_id;
END;
$$;

-- Create a function to attack an enemy
CREATE OR REPLACE FUNCTION attack_enemy(p_player_id INTEGER, p_enemy_id INTEGER)
RETURNS TABLE (player_damage INTEGER, enemy_damage INTEGER, enemy_remaining_hp INTEGER, player_remaining_hp INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    player_attack INTEGER;
    player_defense INTEGER;
    enemy_attack INTEGER;
    enemy_defense INTEGER;
    player_damage INTEGER;
    enemy_damage INTEGER;
    player_hp INTEGER;
    enemy_hp INTEGER;
BEGIN
    -- Get player's attack and defense
    SELECT (pc.forca + COALESCE(a.dano, 0)) * 2, (pc.resistencia + COALESCE(arm.resistencia, 0))
    INTO player_attack, player_defense
    FROM pc
    LEFT JOIN arma a ON pc.equipped_weapon = a.id_arma
    LEFT JOIN armadura arm ON pc.equipped_armor = arm.id_armadura
    WHERE pc.id_player = p_player_id;

    -- Get enemy's attack and defense
    SELECT i.ataque, i.resistencia, i.vida
    INTO enemy_attack, enemy_defense, enemy_hp
    FROM inimigo i
    WHERE i.id_inimigo = p_enemy_id;

    -- Calculate damage
    player_damage := GREATEST(player_attack - enemy_defense, 1);
    enemy_damage := GREATEST(enemy_attack - player_defense, 1);

    -- Update enemy HP
    enemy_hp := GREATEST(enemy_hp - player_damage, 0);
    UPDATE inimigo SET vida = enemy_hp WHERE id_inimigo = p_enemy_id;

    -- Update player HP
    SELECT vida INTO player_hp FROM pc WHERE id_player = p_player_id;
    player_hp := GREATEST(player_hp - enemy_damage, 0);
    UPDATE pc SET vida = player_hp WHERE id_player = p_player_id;

    -- Check if player died
    IF player_hp = 0 THEN
        UPDATE pc SET status = 'morto' WHERE id_player = p_player_id;
    END IF;

    -- Check if enemy died
    IF enemy_hp = 0 THEN
        DELETE FROM instancia_de_inimigo WHERE id_npc = p_enemy_id;
        -- Give souls to the player
        UPDATE pc SET souls = souls + (SELECT drops FROM boss WHERE id_boss = p_enemy_id)
        WHERE id_player = p_player_id;
    END IF;

    RETURN QUERY SELECT player_damage, enemy_damage, enemy_hp, player_hp;
END;
$$;

-- Create a trigger to respawn enemies when a player enters an area
CREATE OR REPLACE FUNCTION respawn_enemies()
RETURNS TRIGGER AS $$
BEGIN
    -- Delete all existing enemy instances in the area
    DELETE FROM instancia_de_inimigo WHERE id_area = NEW.id_area;

    -- Respawn enemies
    INSERT INTO instancia_de_inimigo (id_npc, id_area)
    SELECT id_inimigo, NEW.id_area
    FROM inimigo
    WHERE id_inimigo NOT IN (SELECT id_boss FROM boss)
    ORDER BY RANDOM()
    LIMIT 5;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER respawn_enemies_trigger
AFTER UPDATE OF id_area ON pc
FOR EACH ROW
EXECUTE FUNCTION respawn_enemies();
