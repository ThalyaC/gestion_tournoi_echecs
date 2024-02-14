import sys
import random
from datetime import datetime
import sys
import os

from models_chess import Round, Match
from toolbox import (
    seek_player_ffe,
    open_list,
    write_list,
    what_else,
    #does_list_exist,
    not_in_list,
    PLAYERS
)

from vues.registration_chessplayers_tourmanent import which_tournament

def tournament_number_round(list_tournaments, name_tournament1):  #
    """
    indique le nombre de round d'un tournoi"""
    
    for tournament in list_tournaments:
        """Donne le nombre de rounds contenus dans le tournoi demandé"""
        if "Nom" in tournament and tournament["Nom"] == name_tournament1:
            number_of_rounds = tournament.get("Nombre de rounds")

    return number_of_rounds


    
def create_list_players_tournament(tournament_register1):
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
    


"""
def check_round(number_round, name_file):
    
    1. Vérifie que la round n'a pas déjà été créée
    2. Crée une liste des rounds précédentes si le fichier existe
    
    
    list_info = open_list(name_file)
    try : 
        if list_info:
            list_number_round = [element["Round"] for element in list_info]

        if number_round in list_number_round:
            print("Cette ronde existe déjà")
            print(f"Actuellement, {list_number_round[0]} ronde(s) lancée(s)")
            return None
    
        else:
            return list_info
    except FileNotFoundError:
        list_info = []
        return list_info
"""
    









def new_round():
    name_tournament, tournament_register1, list_tournaments  = which_tournament()
    
    folder = "chess_data/"+tournament_register1
    if not os.path.isdir(folder):
        print("Ce tournoi ne peut être lancé sans joueur")
        return None
    else :
        number_of_rounds = tournament_number_round(list_tournaments, name_tournament)
        print(f"\nCe tournoi contient {number_of_rounds} rondes.")
        path_tourmanent_rounds_file = (
        tournament_register1 + "/" + "rounds_" + tournament_register1)
    
        number_round = input("Quelle ronde souhaitez-vous lancer?")
        #new_round1(tournament_register1, name_tournament, number_of_rounds)
    
    try :
        result_list = open_list(path_tourmanent_rounds_file) 
    
        list_number_round = [element["Round"] for element in result_list]

        try :
            0 < int(number_round) <= int(number_of_rounds)

            if number_round in list_number_round:
                print("\nCette ronde existe déjà")
                print(f"\nActuellement, {list_number_round[0]} ronde(s) lancée(s)")
                #return None
            
            

            else:
                info_round_common, info_round, current_round = create_round(tournament_register1, name_tournament, number_round, number_of_rounds, path_tourmanent_rounds_file)
                round_other(result_list, path_tourmanent_rounds_file, current_round, info_round)
                print(f"\nParfait, la ronde {number_round} du tournoi {name_tournament} vient d'être créée")

        except ValueError:
            print("\nSaisie erronée. Vous devez saisir un nombre entier inférieur ou égal en chiffres au nombre total de ce tournoi")
    
    except FileNotFoundError:
        result_list = []
        info_round_common, info_round, _ = create_round(tournament_register1, name_tournament, number_round, number_of_rounds, path_tourmanent_rounds_file)
        round_one(result_list, path_tourmanent_rounds_file, info_round_common, info_round)
        print(f"\nParfait, la ronde {number_round} du tournoi {name_tournament} vient d'être créée")
        

def create_round(tournament_register1, name_tournament, number_round, number_of_rounds, path_tourmanent_rounds_file):
    list_players_round, number_players, players_file_tournament = (
        create_list_players_tournament(tournament_register1)
    )
    current_round = number_round + "/" + number_of_rounds
    start_round = datetime.now()
    start_date_round = start_round.strftime("%d.%m.%y")
    start_hour = start_round.strftime("%H.%M")
    end_date_round = ""
    end_hour = ""

    #print(f"\nLa ronde {current_round} contient {number_players} joueurs.")

    result = create_matches(
        number_round,
        number_of_rounds,
        number_players,
        list_players_round,
        players_file_tournament,
        path_tourmanent_rounds_file,
    )
    #what_else(result)
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
    return info_round_common, info_round, current_round



def round_one(result_list, path_tourmanent_rounds_file, info_round_common, info_round):
    
    # update_current_round = current_round
    result_list.append(info_round_common)
    result_list.append(info_round)
    write_list(path_tourmanent_rounds_file, result_list)
    

def round_other(result_list, path_tourmanent_rounds_file, current_round, info_round):
    result_list[0]["Round"] = current_round
    result_list.append(info_round)

    write_list(path_tourmanent_rounds_file, result_list)
    


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
        print("\n Les scores de la ronde précédente n'ont pas tous été encore enregistrés")
        #return None


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
                    print("\ncette ronde ne peut avoir lieu, pas assez de joueurs")
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





"""def what_else(result):
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
"""

def not_former_adversary(players_file_tournament, player1, player2):
    "Vérifie que les deux joueurs d'un match n'ont jamais joué auparavant ensemble"
    list_players_tournament = open_list(players_file_tournament)
    key_former_adversary = "Anciens adversaires"
    for player in list_players_tournament:
        if key_former_adversary in player and player[key_former_adversary] == player1:
            list_former_adversary = player[key_former_adversary]
            not_in_list(list_former_adversary, player2)


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
        f"""Actuellement la dernière ronde est la ronde {number_of_rounds}.
        \nQuelle ronde souhaitez-vous afficher?"""
    )

    try:
        display_round = int(display_round1)
        print("\n", name_tournament, "\n", "Round", display_round)
        display_round_3(
            list_round, display_round, list_players_round, list_chess_players
        )
    except:
        print(
            "Cette ronde n'a pas été encore créée ou vous avez fait une erreur de saisie"
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



