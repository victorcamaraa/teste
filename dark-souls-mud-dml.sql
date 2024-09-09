-- Populando a tabela regiao
INSERT INTO regiao (nome) VALUES
('Lordran'),
('Anor Londo'),
('New Londo Ruins'),
('Catacumbas'),
('Blighttown');

-- Populando a tabela area
INSERT INTO area (nome, id_regiao) VALUES
('Firelink Shrine', (SELECT id_regiao FROM regiao WHERE nome = 'Lordran')),
('Undead Burg', (SELECT id_regiao FROM regiao WHERE nome = 'Lordran')),
('Undead Parish', (SELECT id_regiao FROM regiao WHERE nome = 'Lordran')),
('Anor Londo Cathedral', (SELECT id_regiao FROM regiao WHERE nome = 'Anor Londo')),
('Painted World of Ariamis', (SELECT id_regiao FROM regiao WHERE nome = 'Anor Londo')),
('New Londo Ruins Upper', (SELECT id_regiao FROM regiao WHERE nome = 'New Londo Ruins')),
('The Abyss', (SELECT id_regiao FROM regiao WHERE nome = 'New Londo Ruins')),
('Catacombs Upper Level', (SELECT id_regiao FROM regiao WHERE nome = 'Catacumbas')),
('Tomb of the Giants', (SELECT id_regiao FROM regiao WHERE nome = 'Catacumbas')),
('Blighttown Swamp', (SELECT id_regiao FROM regiao WHERE nome = 'Blighttown')),
('The Great Hollow', (SELECT id_regiao FROM regiao WHERE nome = 'Blighttown')),
('Quelaag''s Domain', (SELECT id_regiao FROM regiao WHERE nome = 'Blighttown')),
('Lower Undead Burg', (SELECT id_regiao FROM regiao WHERE nome = 'Lordran')),
('Depths', (SELECT id_regiao FROM regiao WHERE nome = 'Lordran'));

-- Populando a tabela personagem
INSERT INTO personagem (tipo) VALUES
('NPC'), ('NPC'), ('NPC'), ('NPC'), ('NPC'), -- 5 NPCs
('NPC'), ('NPC'), ('NPC'), ('NPC'), ('NPC'), ('NPC'), ('NPC'), ('NPC'), ('NPC'), ('NPC'), -- 15 NPCs/inimigos
('PC'); -- 1 jogador

-- Populando a tabela npc
INSERT INTO npc (id_npc, nome, vida, funcao, resistencia, tipo, status, fraqueza) VALUES
(1, 'Crestfallen Warrior', 100, 'Amigo', 50, true, 'vivo', 'Espada'),
(2, 'Solaire of Astora', 150, 'Amigo', 70, true, 'vivo', 'Magia'),
(3, 'Siegmeyer of Catarina', 200, 'Amigo', 80, true, 'vivo', 'Fogo'),
(4, 'Andre of Astora', 120, 'Amigo', 60, true, 'vivo', 'Espada'),
(5, 'Firekeeper', 80, 'Fire_Keeper', 40, true, 'vivo', 'Fogo'),
(6, 'Hollow Soldier', 50, 'Inimigo', 30, false, 'vivo', 'Fogo'),
(7, 'Undead Archer', 40, 'Inimigo', 20, false, 'vivo', 'Espada'),
(8, 'Balder Knight', 80, 'Inimigo', 50, false, 'vivo', 'Magia'),
(9, 'Capra Demon', 150, 'Boss', 70, false, 'vivo', 'Fogo'),
(10, 'Bell Gargoyle', 200, 'Boss', 80, false, 'vivo', 'Espada'),
(11, 'Skeleton', 30, 'Inimigo', 20, false, 'vivo', 'Magia'),
(12, 'Giant Rat', 40, 'Inimigo', 10, false, 'vivo', 'Fogo'),
(13, 'Blighttown Mosquito', 20, 'Inimigo', 5, false, 'vivo', 'Fogo'),
(14, 'Infested Barbarian', 100, 'Inimigo', 40, false, 'vivo', 'Espada'),
(15, 'Chaos Eater', 80, 'Inimigo', 60, false, 'vivo', 'Magia');

-- Populando a tabela inimigo
INSERT INTO inimigo (id_inimigo, ataque) VALUES
(6, 20), (7, 15), (8, 30), (11, 10), (12, 15),
(13, 5), (14, 40), (15, 35);

-- Populando a tabela boss
INSERT INTO boss (id_boss, ataque, drops) VALUES
(9, 70, 1000), (10, 80, 1500);

-- Populando a tabela amigo
INSERT INTO amigo (id_amigo) VALUES (1), (2), (3), (4);

-- Populando a tabela fire_keeper
INSERT INTO fire_keeper (id_firekeeper, disponivel) VALUES (5, true);

-- Populando a tabela instancia_npc
INSERT INTO instancia_npc (id_npc, id_area) VALUES
(1, (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
(2, (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
(3, (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
(4, (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
(5, (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
(6, (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
(7, (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
(8, (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
(9, (SELECT id_area FROM area WHERE nome = 'Lower Undead Burg')),
(10, (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
(11, (SELECT id_area FROM area WHERE nome = 'Catacombs Upper Level')),
(12, (SELECT id_area FROM area WHERE nome = 'Depths')),
(13, (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp')),
(14, (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp')),
(15, (SELECT id_area FROM area WHERE nome = 'The Great Hollow'));

-- Populando a tabela viagem_area
INSERT INTO viagem_area (id_origem, id_destino) VALUES
((SELECT id_area FROM area WHERE nome = 'Firelink Shrine'), (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
((SELECT id_area FROM area WHERE nome = 'Undead Burg'), (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
((SELECT id_area FROM area WHERE nome = 'Undead Burg'), (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
((SELECT id_area FROM area WHERE nome = 'Undead Parish'), (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
((SELECT id_area FROM area WHERE nome = 'Undead Parish'), (SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral')),
((SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral'), (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
((SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral'), (SELECT id_area FROM area WHERE nome = 'Painted World of Ariamis')),
((SELECT id_area FROM area WHERE nome = 'Painted World of Ariamis'), (SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral')),
((SELECT id_area FROM area WHERE nome = 'Firelink Shrine'), (SELECT id_area FROM area WHERE nome = 'New Londo Ruins Upper')),
((SELECT id_area FROM area WHERE nome = 'New Londo Ruins Upper'), (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
((SELECT id_area FROM area WHERE nome = 'New Londo Ruins Upper'), (SELECT id_area FROM area WHERE nome = 'The Abyss')),
((SELECT id_area FROM area WHERE nome = 'The Abyss'), (SELECT id_area FROM area WHERE nome = 'New Londo Ruins Upper')),
((SELECT id_area FROM area WHERE nome = 'Firelink Shrine'), (SELECT id_area FROM area WHERE nome = 'Catacombs Upper Level')),
((SELECT id_area FROM area WHERE nome = 'Catacombs Upper Level'), (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
((SELECT id_area FROM area WHERE nome = 'Catacombs Upper Level'), (SELECT id_area FROM area WHERE nome = 'Tomb of the Giants')),
((SELECT id_area FROM area WHERE nome = 'Tomb of the Giants'), (SELECT id_area FROM area WHERE nome = 'Catacombs Upper Level')),
((SELECT id_area FROM area WHERE nome = 'Firelink Shrine'), (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp')),
((SELECT id_area FROM area WHERE nome = 'Blighttown Swamp'), (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
((SELECT id_area FROM area WHERE nome = 'Blighttown Swamp'), (SELECT id_area FROM area WHERE nome = 'The Great Hollow')),
((SELECT id_area FROM area WHERE nome = 'The Great Hollow'), (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp')),
((SELECT id_area FROM area WHERE nome = 'Blighttown Swamp'), (SELECT id_area FROM area WHERE nome = 'Quelaag''s Domain')),
((SELECT id_area FROM area WHERE nome = 'Quelaag''s Domain'), (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp')),
((SELECT id_area FROM area WHERE nome = 'Firelink Shrine'), (SELECT id_area FROM area WHERE nome = 'Lower Undead Burg')),
((SELECT id_area FROM area WHERE nome = 'Lower Undead Burg'), (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
((SELECT id_area FROM area WHERE nome = 'Lower Undead Burg'), (SELECT id_area FROM area WHERE nome = 'Depths')),
((SELECT id_area FROM area WHERE nome = 'Depths'), (SELECT id_area FROM area WHERE nome = 'Lower Undead Burg'));

-- Populando a tabela nivel
INSERT INTO nivel (n_nivel, drops) VALUES
(1, 100), (2, 200), (3, 300), (4, 400), (5, 500),
(6, 600), (7, 700), (8, 800), (9, 900), (10, 1000);

-- Populando a tabela item
INSERT INTO item (nome, valor, nivel, tipo) VALUES
('Espada Longa', 200, 1, 'Equipamento'),
('Machado de Batalha', 250, 2, 'Equipamento'),
('Lança', 180, 1, 'Equipamento'),
('Espadão', 300, 3, 'Equipamento'),
('Arco Curto', 150, 1, 'Equipamento'),
('Adaga', 100, 1, 'Equipamento'),
('Martelo de Guerra', 280, 2, 'Equipamento'),
('Espada Bastarda', 350, 3, 'Equipamento'),
('Katana', 400, 4, 'Equipamento'),
('Tridente', 320, 3, 'Equipamento'),
('Armadura de Couro', 150, 1, 'Equipamento'),
('Armadura de Placas', 400, 4, 'Equipamento'),
('Armadura de Malha', 250, 2, 'Equipamento'),
('Armadura de Cavaleiro', 350, 3, 'Equipamento'),
('Armadura Leve', 100, 1, 'Equipamento'),
('Armadura Pesada', 450, 4, 'Equipamento'),
('Armadura de Elite', 500, 5, 'Equipamento'),
('Armadura de Escamas', 300, 3, 'Equipamento'),
('Armadura de Ossos', 200, 2, 'Equipamento'),
('Armadura de Ouro', 600, 5, 'Equipamento'),
('Frasco de Estus', 50, 1, 'Consumivel'),
('Humanidade', 100, 1, 'Consumivel'),
('Erva Verde', 30, 1, 'Consumivel'),
('Resina de Pinho', 40, 1, 'Consumivel'),
('Musgo Roxo', 60, 2, 'Consumivel');

-- Populando a tabela instancia_de_item
INSERT INTO instancia_de_item (id_item, id_area) VALUES
((SELECT id_item FROM item WHERE nome = 'Espada Longa'), (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
((SELECT id_item FROM item WHERE nome = 'Machado de Batalha'), (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
((SELECT id_item FROM item WHERE nome = 'Lança'), (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
((SELECT id_item FROM item WHERE nome = 'Espadão'), (SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral')),
((SELECT id_item FROM item WHERE nome = 'Arco Curto'), (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
((SELECT id_item FROM item WHERE nome = 'Adaga'), (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
((SELECT id_item FROM item WHERE nome = 'Martelo de Guerra'), (SELECT id_area FROM area WHERE nome = 'Catacombs Upper Level')),
((SELECT id_item FROM item WHERE nome = 'Espada Bastarda'), (SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral')),
((SELECT id_item FROM item WHERE nome = 'Katana'), (SELECT id_area FROM area WHERE nome = 'Painted World of Ariamis')),
((SELECT id_item FROM item WHERE nome = 'Tridente'), (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp')),
((SELECT id_item FROM item WHERE nome = 'Armadura de Couro'), (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
((SELECT id_item FROM item WHERE nome = 'Armadura de Placas'), (SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral')),
((SELECT id_item FROM item WHERE nome = 'Armadura de Malha'), (SELECT id_area FROM area WHERE nome = 'Undead Parish')),
((SELECT id_item FROM item WHERE nome = 'Armadura de Cavaleiro'), (SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral')),
((SELECT id_item FROM item WHERE nome = 'Armadura Leve'), (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
((SELECT id_item FROM item WHERE nome = 'Armadura Pesada'), (SELECT id_area FROM area WHERE nome = 'New Londo Ruins Upper')),
((SELECT id_item FROM item WHERE nome = 'Armadura de Elite'), (SELECT id_area FROM area WHERE nome = 'Painted World of Ariamis')),
((SELECT id_item FROM item WHERE nome = 'Armadura de Escamas'), (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp')),
((SELECT id_item FROM item WHERE nome = 'Armadura de Ossos'), (SELECT id_area FROM area WHERE nome = 'Catacombs Upper Level')),
((SELECT id_item FROM item WHERE nome = 'Armadura de Ouro'), (SELECT id_area FROM area WHERE nome = 'Anor Londo Cathedral')),
((SELECT id_item FROM item WHERE nome = 'Frasco de Estus'), (SELECT id_area FROM area WHERE nome = 'Firelink Shrine')),
((SELECT id_item FROM item WHERE nome = 'Humanidade'), (SELECT id_area FROM area WHERE nome = 'Undead Burg')),
((SELECT id_item FROM item WHERE nome = 'Erva Verde'), (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp')),
((SELECT id_item FROM item WHERE nome = 'Resina de Pinho'), (SELECT id_area FROM area WHERE nome = 'The Great Hollow')),
((SELECT id_item FROM item WHERE nome = 'Musgo Roxo'), (SELECT id_area FROM area WHERE nome = 'Blighttown Swamp'));

-- Populando a tabela magia
INSERT INTO magia (nome, dano, tipo, custo_mana, descricao) VALUES
('Bola de Fogo', 50, 1, 30, 'Conjura uma bola de fogo que causa dano ao alvo'),
('Raio', 40, 2, 25, 'Lança um raio que atinge o inimigo'),
('Cura', 0, 3, 40, 'Restaura uma quantidade de pontos de vida'),
('Escudo Mágico', 0, 4, 35, 'Cria um escudo mágico que absorve danos'),
('Flecha de Gelo', 45, 5, 30, 'Dispara uma flecha de gelo que causa dano e diminui a velocidade do alvo');

-- Populando a tabela armadura
INSERT INTO armadura (id_armadura, requisitos, durabilidade, peso, descricao, resistencia) VALUES
((SELECT id_item FROM item WHERE nome = 'Armadura de Couro'), ARRAY[5,0,0,0], 100, 5, 'Uma armadura leve feita de couro resistente', 10),
((SELECT id_item FROM item WHERE nome = 'Armadura de Placas'), ARRAY[15,0,0,0], 200, 20, 'Uma armadura pesada feita de placas de metal', 30),
((SELECT id_item FROM item WHERE nome = 'Armadura de Malha'), ARRAY[10,0,0,0], 150, 10, 'Uma armadura média feita de anéis de metal entrelaçados', 20),
((SELECT id_item FROM item WHERE nome = 'Armadura de Cavaleiro'), ARRAY[12,0,0,0], 180, 15, 'Uma armadura robusta usada por cavaleiros', 25),
((SELECT id_item FROM item WHERE nome = 'Armadura Leve'), ARRAY[3,0,0,0], 80, 3, 'Uma armadura muito leve e flexível', 5),
((SELECT id_item FROM item WHERE nome = 'Armadura Pesada'), ARRAY[20,0,0,0], 250, 25, 'Uma armadura extremamente pesada e resistente', 40),
((SELECT id_item FROM item WHERE nome = 'Armadura de Elite'), ARRAY[18,0,0,0], 220, 18, 'Uma armadura de alta qualidade usada por guerreiros de elite', 35),
((SELECT id_item FROM item WHERE nome = 'Armadura de Escamas'), ARRAY[14,0,0,0], 190, 16, 'Uma armadura feita de escamas de dragão', 28),
((SELECT id_item FROM item WHERE nome = 'Armadura de Ossos'), ARRAY[8,0,0,0], 120, 8, 'Uma armadura sinistra feita de ossos', 15),
((SELECT id_item FROM item WHERE nome = 'Armadura de Ouro'), ARRAY[16,0,0,0], 210, 22, 'Uma armadura luxuosa feita de ouro', 32);

-- Populando a tabela arma
INSERT INTO arma (id_arma, requisitos, durabilidade, peso, descricao, dano, elemento) VALUES
((SELECT id_item FROM item WHERE nome = 'Espada Longa'), ARRAY[10,10,0,0], 100, 5, 'Uma espada longa bem equilibrada', 50, 0),
((SELECT id_item FROM item WHERE nome = 'Machado de Batalha'), ARRAY[15,8,0,0], 120, 8, 'Um machado pesado para combate', 65, 0),
((SELECT id_item FROM item WHERE nome = 'Lança'), ARRAY[12,12,0,0], 90, 4, 'Uma lança longa e afiada', 45, 0),
((SELECT id_item FROM item WHERE nome = 'Espadão'), ARRAY[20,10,0,0], 150, 10, 'Uma espada enorme e poderosa', 80, 0),
((SELECT id_item FROM item WHERE nome = 'Arco Curto'), ARRAY[7,14,0,0], 80, 3, 'Um arco leve e fácil de usar', 30, 0),
((SELECT id_item FROM item WHERE nome = 'Adaga'), ARRAY[6,14,0,0], 70, 1, 'Uma adaga pequena e ágil', 25, 0),
((SELECT id_item FROM item WHERE nome = 'Martelo de Guerra'), ARRAY[18,8,0,0], 130, 9, 'Um martelo pesado capaz de esmagar armaduras', 70, 0),
((SELECT id_item FROM item WHERE nome = 'Espada Bastarda'), ARRAY[16,10,0,0], 110, 7, 'Uma espada versátil de uma mão e meia', 60, 0),
((SELECT id_item FROM item WHERE nome = 'Katana'), ARRAY[12,18,0,0], 90, 4, 'Uma lâmina oriental afiada e elegante', 55, 0),
((SELECT id_item FROM item WHERE nome = 'Tridente'), ARRAY[14,12,0,0], 100, 6, 'Uma arma de longo alcance com três pontas', 50, 0);

-- Populando a tabela pocao
INSERT INTO pocao (id_pocao, efeito) VALUES
((SELECT id_item FROM item WHERE nome = 'Frasco de Estus'), 50),
((SELECT id_item FROM item WHERE nome = 'Humanidade'), 100);

-- Populando a tabela impulso
INSERT INTO impulso (id_impulso, efeito) VALUES
((SELECT id_item FROM item WHERE nome = 'Erva Verde'), 20),
((SELECT id_item FROM item WHERE nome = 'Resina de Pinho'), 30),
((SELECT id_item FROM item WHERE nome = 'Musgo Roxo'), 40);

-- Populando a tabela fala
INSERT INTO fala (fala, chance) VALUES
('Bem-vindo a Lordran, viajante. Que o sol brilhe em sua jornada.', 0.5),
('Os sinos do despertar... Você os ouvirá eventualmente.', 0.3),
('Cuidado com as armadilhas, elas estão por toda parte.', 0.4),
('A maldição dos mortos-vivos é um fardo pesado... Não perca sua humanidade.', 0.2),
('Procure por fogueiras, elas serão seu refúgio neste mundo hostil.', 0.6);

-- Populando a tabela npcfala
INSERT INTO npcfala (id_fala, id_npc) VALUES
(1, 1), -- Crestfallen Warrior
(2, 1),
(3, 2), -- Solaire of Astora
(4, 2),
(5, 3); -- Siegmeyer of Catarina

-- Populando a tabela magia_personagem (exemplo para alguns NPCs)
INSERT INTO magia_personagem (id_personagem, id_magia) VALUES
(2, 1), -- Solaire of Astora conhece Bola de Fogo
(3, 3), -- Siegmeyer of Catarina conhece Cura
(5, 4); -- Firekeeper conhece Escudo Mágico

-- Populando a tabela pc (jogador exemplo)
INSERT INTO pc (id_player, nome, vida, id_nivel, id_area, vigor, vitalidade, destreza, forca, stamina, resistencia, nivel, nivel_atual, status) VALUES
(16, 'Chosen Undead', 100, 1, (SELECT id_area FROM area WHERE nome = 'Firelink Shrine'), 10, 10, 10, 10, 10, 10, 1, 1, 'vivo');

-- Populando a tabela inventario (itens iniciais para o jogador exemplo)
INSERT INTO inventario (id_player, id_item, quantidade) VALUES
(16, (SELECT id_item FROM item WHERE nome = 'Espada Longa'), 1),
(16, (SELECT id_item FROM item WHERE nome = 'Armadura de Couro'), 1),
(16, (SELECT id_item FROM item WHERE nome = 'Frasco de Estus'), 3);