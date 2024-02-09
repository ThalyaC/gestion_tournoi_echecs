from registration_players_tourmanent import (
    create_file_folder_name,
    seek_player_ffe,
    open_list,
    write_list,
)
import random
from datetime import datetime
import sys


class Round:
    "création d'un round"

    def __init__(
        self,
        name_tournament,
        number_round,
        current_round,
        start_date_round,
        end_date_round,
        start_hour,
        end_hour,
        list_matches,
        number_tables,
        status,
    ):
        self.name_tournament = name_tournament
        self.number_round = number_round
        self.current_round = current_round  # format "a/b"
        self.start_date_round = start_date_round
        self.end_date_round = end_date_round
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.list_matches = list_matches
        self.number_tables = number_tables
        self.status = status

    def round_info(self):
        return {
            "Round": self.number_round,
            "Etat": self.status,
            "Date de lancement": self.start_date_round,
            "Heure de lancement": self.start_hour,
            "Round finie le": self.end_date_round,
            "Heure de fin": self.end_hour,
            "Nombre de tables en cours de jeu": self.number_tables,
            "Liste des appariements": self.list_matches,
        }

    @classmethod
    def read_info_round(cls, path_tourmanent_rounds_file):
        list_data_round = open_list(path_tourmanent_rounds_file)
        list_data_round.pop(0)

        if isinstance(list_data_round, list):
            rounds = []
            for round_data in list_data_round:
                round = cls(
                    name_tournament=round_data.get("Nom du tournoi", None),
                    current_round=round_data.get("Round", None),
                    number_round=round_data.get("Round"),
                    status=round_data.get("Etat"),
                    start_date_round=round_data.get("Date de lancement"),
                    start_hour=round_data.get("Heure de lancement"),
                    end_date_round=round_data.get("Round finie le"),
                    end_hour=round_data.get("Heure de fin"),
                    number_tables=round_data.get("Nombre de tables en cours de jeu"),
                    list_matches=round_data.get("Liste des appariements"),
                )
                rounds.append(round)
            return rounds
        else:
            return cls(
                name_tournament=round_data.get("Nom du tournoi", None),
                current_round=round_data.get("Round", None),
                number_round=round_data.get("Round"),
                status=round_data.get("Etat"),
                start_date_round=round_data.get("Date de lancement"),
                start_hour=round_data.get("Heure de lancement"),
                end_date_round=round_data.get("Round finie le"),
                end_hour=round_data.get("Heure de fin"),
                number_tables=round_data.get("Nombre de tables en cours de jeu"),
                list_matches=round_data.get("Liste des appariements"),
            )


class Match(Round):
    def __init__(self, table, white, black, score_players):
        self.white = white
        self.black = black
        self.score_player1_2 = score_players
        self.table = table

    def info_match(self):
        return {
            "Table": self.table,
            "Blanc": self.white,
            "Noir": self.black,
            "score": self.score_player1_2,
        }


def which_tournament():  #
    """
    1. Demande à l'utilisateur de choisir un tournoi,
    2. récupère les éléments nécessaires à la création d'une round"""
    list_tournaments = open_list("list_tournaments")

    """nom du tournoi"""
    list_tournaments_name = [element["Nom"] for element in list_tournaments]
    name_tournament1, tournament_register1 = create_file_folder_name(
        list_tournaments_name
    )

    for tournament in list_tournaments:
        """Donne le nombre de rounds contenus dans le tournoi demandé"""
        if "Nom" in tournament and tournament["Nom"] == name_tournament1:
            number_of_rounds = tournament.get("Nombre de rounds")

    return tournament_register1, name_tournament1, number_of_rounds


def create_list_players_tournament(tournament_register1):  #
    """Crée :
    1. une liste de joueurs à partir du fichier players du tournoi choisi par l'utilisateur
    2. indique le nombre de joueurs
    3. une partie du chemin d'accès du fichier"""
    players_file_tournament = (
        tournament_register1 + "/" + "players_" + tournament_register1
    )
    list_chessplayers_tournament = open_list(players_file_tournament)
    number_players = len(list_chessplayers_tournament)
    print("Nombre de joueurs inscrits au tounoi :", len(list_chessplayers_tournament))

    return list_chessplayers_tournament, number_players, players_file_tournament


def check_round(number_round, name_file):
    """
    1. Vérifie que la round n'a pas déjà été créée
    2. Crée une liste des rounds précédentes si le fichier existe"""
    try:
        list_info = open_list(name_file)
    except:
        return None

    if list_info:
        list_number_round = [element["Round"] for element in list_info]

        if number_round in list_number_round:
            print("Cette round existe déjà")
            print(f"Actuellement, {list_number_round[0]} round(s) lancée(s)")
            sys.exit(0)
        else:
            return list_info


def new_round():
    """
    1. Création d'une round,
    2. Enregistrement de cette round dans un fichier contenant toutes les rounds du tournoi
    """
    tournament_register1, name_tournament, number_of_rounds = which_tournament()
    print(f"Ce tournoi contient {number_of_rounds} rounds.")

    path_tourmanent_rounds_file = (
        tournament_register1 + "/" + "rounds_" + tournament_register1
    )
    number_round = input("Quelle round souhaitez-vous lancer?")
    result_list1 = check_round(number_round, path_tourmanent_rounds_file)
    result_list = does_list_exist(result_list1)

    list_players_round, number_players, players_file_tournament = (
        create_list_players_tournament(tournament_register1)
    )
    current_round = number_round + "/" + number_of_rounds
    start_round = datetime.now()
    start_date_round = start_round.strftime("%d.%m.%y")
    start_hour = start_round.strftime("%H.%M")
    end_date_round = ""
    end_hour = ""

    print(f"La round {current_round} contient {number_players} joueurs.")

    result = create_matches(
        number_round,
        number_of_rounds,
        number_players,
        list_players_round,
        players_file_tournament,
        path_tourmanent_rounds_file,
    )
    what_else(result)
    list_matches, number_tables = result

    """création d'une round"""
    round = Round(
        name_tournament=name_tournament,
        number_round=number_round,
        current_round=current_round,
        start_date_round=start_date_round,
        start_hour=start_hour,
        end_date_round=end_date_round,
        end_hour=end_hour,
        list_matches=list_matches,
        number_tables=number_tables,
        status="En cours",
    )
    info_round_common = {
        "Nom du tournoi": round.name_tournament,
        "Round": round.current_round,
    }
    info_round = round.round_info()
    if result_list == []:

        # update_current_round = current_round
        result_list.append(info_round_common)
        result_list.append(info_round)

    else:
        result_list[0]["Round"] = current_round
        result_list.append(info_round)

    write_list(path_tourmanent_rounds_file, result_list)
    return number_round, tournament_register1


def create_matches(
    number_round: int,
    number_of_rounds,
    number_players,
    list_players_round,
    players_file_tournament,
    path_tourmanent_rounds_file,
):
    """Création des matches:
    1.  Création des appariements de la première round de manière aléatoire;
    2.  Vérifie, si nécessaire, que les scores de la round précédente ont 
        tous été enregistrés;
    3.  Création des autres rounds en fonction des résultats des joueurs et
        des adversaires précédents;
    4.  En cas de nombre impair des joueurs, génére un exempt et enregistre 
        automatiquement le score.
    """
    round_int = int(number_round)
    number_of_rounds_int = int(number_of_rounds)
    number_players_int = int(number_players)
    number_tables = number_players_int // 2 + number_players % 2
    list_ffe_round = []
    list_matches = []
    list_ffe_round = [element["Numero FFE"] for element in list_players_round]
    n = 1

    if round_int == 1:
        random.shuffle(list_ffe_round)
        for i in range(0, len(list_ffe_round), 2):

            if i + 1 < len(list_ffe_round):
                simple_match(list_ffe_round, i, n, list_matches)
            else:
                exempt_match(
                    list_ffe_round,
                    list_players_round,
                    list_matches,
                    players_file_tournament,
                    i,
                    n,
                )
                number_tables = number_tables - 1
            n += 1
            if n > number_tables:
                break
        return list_matches, number_tables

    elif 1 < round_int <= number_of_rounds_int:
        list_sorted_by_score = check_round_previous(
            round_int, path_tourmanent_rounds_file, list_players_round
        )
        list_ffe_round_next = [
            element["Numero FFE"] for element in list_sorted_by_score
        ]

        for i in range(0, len(list_ffe_round_next), 2):

            if i + 1 < len(list_ffe_round_next):
                simple_match1(
                    list_ffe_round_next, i, n, list_matches, players_file_tournament
                )
            else:
                exempt_match(
                    list_ffe_round_next,
                    list_players_round,
                    list_matches,
                    players_file_tournament,
                    i,
                    n,
                )
                number_tables = number_tables - 1
            n += 1
            if n > number_tables:
                break

        return list_matches, number_tables

    else:
        print("Cette round n'existe pas")
        return None


def check_round_previous(round_int, path_tourmanent_rounds_file, list_players_round):
    """Vérifie que tous les scores de la round précédente ont été enregistrés"""
    round_int_previous = round_int - 1
    list_provisional1 = []
    try:
        list_provisional2 = open_list(path_tourmanent_rounds_file)
        for one_round in list_provisional2:
            list_provisional1.append(one_round)
        list_provisional = list_provisional1

        for round_previous in list_provisional:
            if round_previous["Round"] == str(round_int_previous):
                if round_previous["Etat"] == "Clos":
                    list_sorted_by_score = sorted(
                        list_players_round, key=lambda x: x["score"], reverse=True
                    )
        return list_sorted_by_score
    except:
        print("Les scores de la round précédente n'ont pas tous été encore enregistrés")
        sys.exit(0)


def simple_match(list_ffe_round, i, n, list_matches):
    """Création des matches simples (sans exempt) pour la 1ère round"""
    white = list_ffe_round[i]
    black = list_ffe_round[i + 1]

    table = n
    match1 = Match(table=table, white=white, black=black, score_players=" ")
    info_match1 = match1.info_match()
    list_matches.append(info_match1)


def simple_match1(list_ffe_round_next, i, n, list_matches, players_file_tournament):
    """Création des matches simples (sans exempt) pour les rounds suivantes"""
    white = list_ffe_round_next[i]
    list_players_tournament = open_list(players_file_tournament)

    for player in list_players_tournament:

        if "Numero FFE" in player and player["Numero FFE"] == white:
            list_former_adversary = player.get("Anciens adversaires")
            result_adversary = not_in_list(
                list_former_adversary, list_ffe_round_next[i + 1]
            )

            if result_adversary != None:
                black = list_ffe_round_next[i + 1]
                table = n
                match1 = Match(table=table, white=white, black=black, score_players=" ")
                info_match1 = match1.info_match()
                list_matches.append(info_match1)

            else:
                j = i + 2

                try:
                    while j < len(list_ffe_round_next):
                        result_adversary = not_in_list(
                            list_former_adversary, list_ffe_round_next[j]
                        )
                        if result_adversary != None:
                            black1 = list_ffe_round_next[j]
                            black = str(black1)
                            list_ffe_round_next.pop(j)
                            list_ffe_round_next.insert(i + 1, black)

                        else:
                            j += 1

                    table = n
                    match1 = Match(
                        table=table, white=white, black=black, score_players=" "
                    )
                    info_match1 = match1.info_match()
                    list_matches.append(info_match1)

                except:
                    print("cette round ne peut avoir lieu, pas assez de joueurs")
                    break


def exempt_match(
    list_ffe_round, list_players_round, list_matches, players_file_tournament, i, n
):
    """Si le nombre de joueurs est impair, création d'une dernière table avec 
    un joueur exempté, enregistrement automatique du score 0.5-_"""
    white = list_ffe_round[i]
    black = "exempt"
    table = n
    match1 = Match(table=table, white=white, black=black, score_players="0.5-_")
    info_match1 = match1.info_match()
    list_matches.append(info_match1)
    player1_ffe = list_ffe_round[i]
    score_player1_3 = 0.5
    key_ffe = "Numero FFE"

    """Ajout automatique de 0.5 point au joueur exempté"""
    for player_round in list_players_round:
        if key_ffe in player_round and player_round[key_ffe] == player1_ffe:
            # player_exempt = player_round
            score_player1_2 = float(player_round["score"])
            player_round["score"] = score_player1_2 + score_player1_3
            player_round["Anciens adversaires"].append(black)
            write_list(players_file_tournament, list_players_round)
            break


def score_recording():
    """Enregistrer les scores pour les appariements,
    mise à jour du nombre de matches restants,
    puis pour les joueurs individuellement"""

    tournament_register1, _, _ = which_tournament()
    number_round_score2 = input(
        "Dans quelle round souhaitez-vous enregistrer un score?"
    )
    number_round_score1 = int(number_round_score2)

    path_tourmanent_rounds_file = (
        tournament_register1 + "/rounds_" + tournament_register1
    )
    list_info_current_tournament = open_list(path_tourmanent_rounds_file)

    try:
        round_info_total = list_info_current_tournament[number_round_score1]
    except:
        print(
            "Cette round n'a pas été encore créée ou vous avez fait une erreur de saisie"
        )
        sys.exit(0)

    table_score2 = input("Quelle table? (tapez juste un numéro)")

    remaining_tables1 = round_info_total["Nombre de tables en cours de jeu"]

    list_pairing = round_info_total["Liste des appariements"]
    info_pairing = list_pairing[int(table_score2) - 1]

    add_score = input("Entrez le score (1-0,0-1 ou 0.5-0.5)")
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


def register_individual_score(add_score, info_pairing, tournament_register1):
    """inscription et modification des scores dans la liste des joueurs"""
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


def what_else(result):
    "Vérifie que l'opération est possible"
    if result == None:
        print("Fin")
        sys.exit(0)
    else:
        pass


def does_list_exist(result):
    "Vérifie que la liste existe ou en crée une vide"
    if result == None:
        wanted_list = []
    else:
        wanted_list = result
    return wanted_list


def not_in_list(ma_liste, black):
    "vérifie qu'un élément n'est pas dans la liste"
    x = 0

    while x < len(ma_liste):
        if any(ffe == black for ffe in ma_liste):
            # print(f"Le joueur {black} a déjà joué avec ce joueur")
            return None

        elif not any(ffe == black for ffe in ma_liste):
            black_player = black
            # print("Le joueur noir est:", black_player)
            return black_player

        else:
            x += 1


def not_former_adversary(players_file_tournament, player1, player2):
    "Vérifie que les deux joueurs d'un match n'ont jamais joué auparavant ensemble"
    list_players_tournament = open_list(players_file_tournament)
    key_former_adversary = "Anciens adversaires"
    for player in list_players_tournament:
        if key_former_adversary in player and player[key_former_adversary] == player1:
            list_former_adversary = player[key_former_adversary]
            not_in_list(list_former_adversary, player2)


# score_recording()
# new_round()
# display_on_screen_players_round()
# STOP
# faire un fichier toolbox
# affichage des rounds _ display
# main


def display_on_screen_round():
    "Affiche la round souhaitée"

    tournament_register1, name_tournament, _ = which_tournament()
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
        f"""Actuellement la dernière round est la round {number_of_rounds}.
        \nQuelle round souhaitez-vous afficher?"""
    )

    try:
        display_round = int(display_round1)
        print("\n", name_tournament, "\n", "Round", display_round)
        display_round_3(
            list_round, display_round, list_players_round, list_chess_players
        )
    except:
        print(
            "Cette round n'a pas été encore créée ou vous avez fait une erreur de saisie"
        )
        sys.exit(0)


def display_round_3(list_round, display_round, list_players_round, list_chess_players):
    "Affiche les matches. Lie les matches aux noms des joueurs et à leurs scores précédents"
    round_choose = list_round[display_round - 1]
    content_round = round_choose.round_info()
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
        # test1=len(player_white1["Nom"])+len(player_white1["Prenom"])
        # print(test1)
        espace_number_white = 25 - (
            (len(player_white1["Nom"]) + len(player_white1["Prenom"]))
            + len(table["score"])
        )
        # print(espace_number_white)
        espace = " "
        espaces_w = espace_number_white * espace
        # print(len(table["score"]))

        player_black3 = table["Noir"]
        if player_black3 == "exempt":
            player_black = "exempt"
            # print(len(player_black))
            # print(len(table["score"]))
            espace_number_black = 25 - (len("exempt") + len(table["score"]))
            espace = " "
            espaces_b = espace_number_black * espace
            # print(espace_number_black)
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
            # print(espace_number_black)
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


display_on_screen_round()
