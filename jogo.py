import psycopg2
from psycopg2 import sql
import os

# Configuração da conexão com o banco de dados
conn = psycopg2.connect(
    dbname="dark_souls_mud",
    user="postgres",
    password="123",
    host="localhost"
)
cur = conn.cursor()


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def criar_personagem():
    print("Bem-vindo à criação de personagem!")
    nome = input("Digite o nome do seu personagem: ")

    pontos_restantes = 10
    atributos = {
        'vigor': 10, 'vitalidade': 10, 'resistencia': 10, 'forca': 10,
        'destreza': 10, 'inteligencia': 10, 'fe': 10
    }

    while pontos_restantes > 0:
        print(f"\nPontos restantes: {pontos_restantes}")
        for attr, valor in atributos.items():
            print(f"{attr.capitalize()}: {valor}")

        attr = input("Escolha um atributo para aumentar: ").lower()
        if attr in atributos:
            atributos[attr] += 1
            pontos_restantes -= 1
        else:
            print("Atributo inválido.")

    cur.execute(
        """
        CALL create_character(%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nome, atributos['vigor'], atributos['vitalidade'], atributos['resistencia'],
         atributos['forca'], atributos['destreza'], atributos['inteligencia'], atributos['fe'])
    )
    conn.commit()

    print("Personagem criado com sucesso!")
    return obter_id_jogador(nome)


def obter_id_jogador(nome):
    cur.execute("SELECT id_player FROM pc WHERE nome = %s", (nome,))
    return cur.fetchone()[0]


def obter_info_jogador(id_jogador):
    cur.execute(
        """
        SELECT nome, vida, id_area, vigor, vitalidade, resistencia, forca, destreza, inteligencia, fe, souls
        FROM pc WHERE id_player = %s
        """,
        (id_jogador,)
    )
    return cur.fetchone()


def obter_nome_area(id_area):
    cur.execute("SELECT nome FROM area WHERE id_area = %s", (id_area,))
    return cur.fetchone()[0]


def obter_areas_disponiveis(id_area_atual):
    cur.execute("SELECT * FROM get_available_areas(%s)", (id_area_atual,))
    return cur.fetchall()


def mover_jogador(id_jogador, id_destino):
    cur.execute("SELECT move_player(%s, %s)", (id_jogador, id_destino))
    return cur.fetchone()[0]


def obter_inimigos_na_area(id_area):
    cur.execute("SELECT * FROM get_enemies_in_area(%s)", (id_area,))
    return cur.fetchall()


def atacar_inimigo(id_jogador, id_inimigo):
    cur.execute("SELECT * FROM attack_enemy(%s, %s)", (id_jogador, id_inimigo))
    return cur.fetchone()


def jogo_principal():
    limpar_tela()
    print("Bem-vindo ao Dark Souls MUD!")
    nome = input("Digite o nome do seu personagem (ou deixe em branco para criar um novo): ")

    if nome:
        id_jogador = obter_id_jogador(nome)
        if not id_jogador:
            print("Personagem não encontrado. Criando um novo...")
            id_jogador = criar_personagem()
    else:
        id_jogador = criar_personagem()

    while True:
        limpar_tela()
        info_jogador = obter_info_jogador(id_jogador)
        nome, vida, id_area, vigor, vitalidade, resistencia, forca, destreza, inteligencia, fe, souls = info_jogador
        nome_area = obter_nome_area(id_area)

        print(f"Nome: {nome} | Vida: {vida} | Souls: {souls}")
        print(f"Vigor: {vigor} | Vitalidade: {vitalidade} | Resistência: {resistencia}")
        print(f"Força: {forca} | Destreza: {destreza} | Inteligência: {inteligencia} | Fé: {fe}")
        print(f"Localização atual: {nome_area}")

        print("\nAções disponíveis:")
        print("1. Mover")
        print("2. Atacar")
        print("3. Sair do jogo")

        escolha = input("Escolha uma ação: ")

        if escolha == '1':
            areas_disponiveis = obter_areas_disponiveis(id_area)
            print("\nÁreas disponíveis:")
            for id_destino, nome_destino in areas_disponiveis:
                print(f"{id_destino}: {nome_destino.strip()}")

            id_destino = int(input("Escolha o ID da área para onde deseja ir: "))
            if mover_jogador(id_jogador, id_destino):
                print("Você se moveu com sucesso!")
            else:
                print("Movimento inválido.")

        elif escolha == '2':
            inimigos = obter_inimigos_na_area(id_area)
            if not inimigos:
                print("Não há inimigos nesta área.")
            else:
                print("\nInimigos na área:")
                for id_inimigo, nome, vida, ataque in inimigos:
                    print(f"{id_inimigo}: {nome.strip()} (Vida: {vida}, Ataque: {ataque})")

                id_inimigo = int(input("Escolha o ID do inimigo que deseja atacar: "))
                resultado = atacar_inimigo(id_jogador, id_inimigo)
                if resultado:
                    dano_jogador, dano_inimigo, vida_inimigo, vida_jogador = resultado
                    print(f"Você causou {dano_jogador} de dano ao inimigo.")
                    print(f"O inimigo causou {dano_inimigo} de dano a você.")
                    print(f"Vida restante do inimigo: {vida_inimigo}")
                    print(f"Sua vida restante: {vida_jogador}")

                    if vida_jogador <= 0:
                        print("Você morreu. Fim de jogo.")
                        return
                else:
                    print("Ataque inválido.")

        elif escolha == '3':
            print("Obrigado por jogar!")
            break

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    jogo_principal()
    cur.close()
    conn.close()