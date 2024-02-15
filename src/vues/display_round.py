from models_chess import Round
from toolbox import (
    seek_player_ffe,
    open_list
)

from vues.registration_chessplayers_tourmanent import which_tournament


def display_on_screen_round():
    """Affiche la round souhaitée"""

    name_tournament, tournament_register1, _ = which_tournament()
    list_chess_players = open_list("list_players1")
    path_tourmanent_rounds_file = (
        tournament_register1 + "/rounds_" + tournament_register1
    )
    path_tourmanent_players_file = (
        tournament_register1 + "/players_" + tournament_register1
    )
    list_round = Round.read_info_round(path_tourmanent_rounds_file)
    list_players_round = open_list(path_tourmanent_players_file)

    number_of_rounds = len(list_round)
    display_round1 = input(
        f"""Actuellement la dernière ronde est la ronde {number_of_rounds}.
        \nQuelle ronde souhaitez-vous afficher? """
    )

    try:
        display_round = int(display_round1)
        print("\n", name_tournament, "\n", "Round", display_round)
        round_choose = list_round[display_round - 1]
        content_round = round_choose.round_info()
        display_round_2(content_round)
        display_round_3(
            content_round, list_players_round, list_chess_players
        )
    except:
        print(
            "Cette ronde n'a pas été encore créée ou vous avez fait une erreur de saisie"
        )


def display_round_3(content_round, list_players_round, list_chess_players):
    """Affiche les matches. Lie les matches aux noms des joueurs et à leur score actuel"""

    list_pairing1 = content_round["Liste des appariements"]

    for table in list_pairing1:
        number_table_screen = table["Table"]
        player_white2 = seek_player_ffe(list_players_round, table["Blanc"])
        player_white1 = seek_player_ffe(list_chess_players, table["Blanc"])
        player_white = (
            player_white2["score"],
            player_white1["Nom"],
            player_white1["Prenom"],
        )
        espace_number_white = 25 - (
            (len(player_white1["Nom"]) + len(player_white1["Prenom"]))
            + len(table["score"])
        )
        espace = " "
        espaces_w = espace_number_white * espace

        player_black3 = table["Noir"]
        if player_black3 == "exempt":
            player_black = "exempt"

            espace_number_black = 25 - (len("exempt") + len(table["score"]))
            espace = " "
            espaces_b = espace_number_black * espace

        else:
            player_black2 = seek_player_ffe(list_players_round, player_black3)
            player_black1 = seek_player_ffe(list_chess_players, player_black3)
            player_black = (
                player_black1["Nom"],
                player_black1["Prenom"],
                player_black2["score"],
            )
            espace_number_black = 25 - (
                (len(player_black1["Nom"]) + len(player_black1["Prenom"]))
                + len(table["score"])
            )

            espace = " "
            espaces_b = espace_number_black * espace
        
        print(
            "\nTable",
            number_table_screen,
            "\n",
            *player_white,
            espaces_w,
            "|",
            *table["score"],
            "|",
            espaces_b,
            *player_black,
            "\n",
        )

def display_round_2(content_round):
    """Indique les infos générales de la ronde"""

    etat = content_round["Etat"]
    date_start = content_round["Date de lancement"]
    hour_start = content_round["Heure de lancement"]
    date_end = content_round["Round finie le"]
    hour_end = content_round["Heure de fin"]
    number_tables_playing = content_round["Nombre de tables en cours de jeu"]
    return print(f"Etat : {etat}\nCommencé le : {date_start} à {hour_start} \nFini le : {date_end} à {hour_end} \nNombre de tables en cours de jeu {number_tables_playing}")

