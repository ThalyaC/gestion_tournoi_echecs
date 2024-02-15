import random
from datetime import datetime
import os

from models_chess import Round, Match
from toolbox import (
    open_list,
    write_list,
    not_in_list
)

from vues.registration_chessplayers_tourmanent import which_tournament

def tournament_number_round(list_tournaments, name_tournament1):
    """
    Indique le nombre de round d'un tournoi"""
    
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


def new_round():
    """Crée une nouvelle ronde en vérifiant les saisies de l'utilisateur"""
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
        list_chessplayers_tournament, number_players, players_file_tournament = create_list_players_tournament(tournament_register1)
        number_round = input("Quelle ronde souhaitez-vous lancer?")
        number_max_rounds = number_possible_round_players(number_players)
        if int(number_of_rounds)>=number_max_rounds:
            print(f"Attention, le nombre de joueurs ne permet que {number_max_rounds} rondes")
    
    try :
        result_list = open_list(path_tourmanent_rounds_file) 
    
        list_number_round = [element["Round"] for element in result_list]

        try :
            0 < int(number_round) <= int(number_of_rounds)

            if number_round in list_number_round:
                print("\nCette ronde existe déjà")
                print(f"\nActuellement, {list_number_round[0]} ronde(s) lancée(s)")
                #return None
            elif not check_round_previous(number_round, result_list):
                print ("\n Cette ronde ne peut pas être lancée. Les scores de la ronde précédente n'ont pas tous été encore enregistrés.")
            
            elif int(number_round)>number_max_rounds:
                print("Il n'y a pas assez de joueurs pour lancer cette ronde.")
            
            else :
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


def number_possible_round_players(number_players):
    """Vérifie le nombre de rondes possibles en fonction du nombre de joueurs enregistrés"""
    number_test = int(number_players)%2
    if number_test !=0:
        number_max_round = int(number_players)
        return number_max_round
    else:
        number_max_round = int(number_players)-1
        return number_max_round


def create_round(tournament_register1, name_tournament, number_round, number_of_rounds, path_tourmanent_rounds_file):
    """Génére les informations générales d'une ronde"""
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
    """1ère round - enregistre une seule fois les informations générales du tournoi, puis de la 1ère round"""
    
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
        list_sorted_by_score = check_round_previous1(
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

        


def check_round_previous(number_round, result_list):
    """Vérifie que tous les scores de la ronde précédente ont été enregistrés"""
    round_int_previous = int(number_round) - 1
    list_provisional = []
    
    for one_round in result_list:
        list_provisional.append(one_round)
    
    for round_previous in list_provisional:
        if round_previous["Round"] == str(round_int_previous):
            if round_previous["Etat"] == "Clos":
                return True
        

def check_round_previous1(number_round, path_tourmanent_rounds_file, list_players_round):
    """Vérifie que tous les scores de la ronde précédente ont été enregistrés"""
    round_int_previous = int(number_round) - 1
    list_provisional1 = []

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

                if j >= len(list_ffe_round_next):
                            print("\ncette ronde ne peut avoir lieu, pas assez de joueurs")
                            return False
                
                else:
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


def not_former_adversary(players_file_tournament, player1, player2):
    """Vérifie que les deux joueurs d'un match n'ont jamais joué auparavant ensemble"""
    list_players_tournament = open_list(players_file_tournament)
    key_former_adversary = "Anciens adversaires"
    for player in list_players_tournament:
        if key_former_adversary in player and player[key_former_adversary] == player1:
            list_former_adversary = player[key_former_adversary]
            not_in_list(list_former_adversary, player2)


