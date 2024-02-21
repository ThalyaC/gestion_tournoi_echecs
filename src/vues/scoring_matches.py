from datetime import datetime

from toolbox import (
    seek_player_ffe,
    open_list,
    write_list,
    generic_check,
    is_integer
)
from vues.registration_chessplayers_tourmanent import which_tournament


def score_recording():
    """Enregistrer les scores pour les appariements, mise à jour du nombre de matches restants,
    puis pour les joueurs individuellement"""

    _, tournament_register1, _ = which_tournament()
    number_round_score2 = generic_check(
        "Dans quelle ronde souhaitez-vous enregistrer un score?",
        is_integer, "Erreur de saisie. Veuillez choisir un nombre entier.")
    number_round_score1 = int(number_round_score2)

    path_tourmanent_rounds_file = (tournament_register1 + "/rounds_" + tournament_register1)
    list_info_current_tournament = open_list(path_tourmanent_rounds_file)

    if 0 <= number_round_score1 < len(list_info_current_tournament):
        round_info_total = list_info_current_tournament[number_round_score1]
        table_score1 = generic_check("Quelle table? (tapez juste un numéro)",
                                     is_integer, "Erreur de saisie, veuillez recommencer.")
        list_pairing = round_info_total['Liste des appariements']
        list_pairing_tables = [element["Table"] for element in list_pairing]
        if int(table_score1) in list_pairing_tables:
            if check_score_empty(table_score1, list_pairing) is None:
                print("Le score de cette table a déjà été enregistré")
                return None
            else:
                register_table_score(round_info_total, list_pairing, table_score1,
                                     tournament_register1, path_tourmanent_rounds_file, list_info_current_tournament)

        else:
            print(
                "Cette table n'existe pas ou vous avez fait une erreur de saisie"
            )

            return None
    else:
        print(
            "Cette ronde n'a pas été encore créée ou vous avez fait une erreur de saisie"
        )

        return None


def check_score_empty(table_score1: str, list_pairing: list):
    """Vérifie que le score n'a pas encore été enregistré"""

    info_pairing = list_pairing[int(table_score1) - 1]
    result_check_empty = info_pairing["score"]
    empty = " "
    if result_check_empty == empty:
        return True


def register_table_score(
    round_info_total: list, list_pairing: list, table_score1: str,
    tournament_register1: str, path_tourmanent_rounds_file: str,
    list_info_current_tournament: list
):
    """Enregistre dans le fichier round du tournoi les scores"""

    remaining_tables1 = round_info_total["Nombre de tables en cours de jeu"]
    info_pairing = list_pairing[int(table_score1) - 1]
    add_score = generic_check("Entrez le score (1-0,0-1 ou 0.5-0.5)",
                              check_points_entered, "Saisie erronée. Veuillez recommencer")
    info_pairing["score"] = add_score

    round_info_total["Nombre de tables en cours de jeu"] = remaining_tables1 - 1

    remaining_tables = round_info_total["Nombre de tables en cours de jeu"]
    if remaining_tables == 0:
        end_round = datetime.now()
        date_end = end_round.strftime("%d.%m.%y")
        hour_end = end_round.strftime("%H.%M")
        round_info_total["Heure de fin"] = hour_end
        round_info_total["Round finie le"] = date_end
        round_info_total["Etat"] = "Clos"

    register_individual_score(add_score, info_pairing, tournament_register1)
    write_list(path_tourmanent_rounds_file, list_info_current_tournament)


def check_points_entered(points: str):
    """Valide la saisie des scores"""

    list_points = ["0-1", "1-0", "0.5-0.5"]
    result = points in list_points
    return result


def register_individual_score(add_score: str, info_pairing: list, tournament_register1: str):
    """inscription et modification des scores dans la liste des joueurs du tournoi"""

    individual_score = add_score.split("-")
    score_player1_2 = float(individual_score[0])
    score_player2_2 = float(individual_score[1])

    # Le numéro FFE des joueurs
    player_1_1 = info_pairing["Blanc"]
    player_2_1 = info_pairing["Noir"]

    path_tourmanent_players_file = (
        tournament_register1 + "/players_" + tournament_register1
    )
    list_individual = open_list(path_tourmanent_players_file)

    player_1 = seek_player_ffe(list_individual, player_1_1)
    player_2 = seek_player_ffe(list_individual, player_2_1)
    player_1["Anciens adversaires"].append(player_2_1)
    player_2["Anciens adversaires"].append(player_1_1)
    score_player1_1 = float(player_1["score"])
    score_player1 = score_player1_1 + score_player1_2
    player_1["score"] = score_player1
    score_player2_1 = float(player_2["score"])
    score_player2 = score_player2_1 + score_player2_2
    player_2["score"] = score_player2

    write_list(path_tourmanent_players_file, list_individual)
