#from tournament import Tournament
import json
from registration_players_tourmanent import open_list_tournaments, create_file_folder_name
import random


class Round:
    "création d'un round"
    def __init__(self, name_tournament, number_of_rounds, number_round, start_date_round, end_date_round,start_hour, end_hour, list_players_round, list_matches):
        self.name_tournament=name_tournament
        self.number_of_rounds=number_of_rounds
        self.number_round = number_round
        self.start_date_round = start_date_round
        self.end_date_round = end_date_round
        self.start_hour = start_hour #automatique (import datatime p267)
        self.end_hour = end_hour
        self.list_players_round = list_players_round
        self.list_matches= list_matches

    def add_match(self, match):
        """Ajoute un match au round en cours de création"""
        self.list_matches.append(match)
    

class Match:
    def __init__(self, player1, score_player1, player2, score_player2, table):
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.table = table
    


def which_tournament():
    """
    1. Demande à l'utilisateur de choisir un tournoi, 
    2. récupère les éléments nécessaires à la création d'une round"""
    list_tournaments = open_list_tournaments()
    list_tournaments_name = [element["Nom"] for element in list_tournaments]
    name_tournament1, tournament_register1 = create_file_folder_name(list_tournaments_name)
    
    """nom du tournoi"""
    #name_tournament1 = tournament_register1.replace("_"," ")

    for tournament in list_tournaments:
        """Donne le nombre de rounds contenus dans le tournoi demandé"""
        if "Nom" in tournament and tournament["Nom"]==name_tournament1:
            number_of_rounds = tournament.get("Nombre de rounds")

    return tournament_register1, name_tournament1, number_of_rounds

def create_list_players_tournament(tournament_register1):
    
    """Crée une liste de joueurs à partir 
    du fichier players du tournoi choisi par l'utilisateur
    Attention : ne peut fonctionner seule"""
    tournament_register_players = 'players_'+tournament_register1
    tournament_register_case = tournament_register1+'/'
    
    with open('chess_data/'+tournament_register_case+tournament_register_players+'.json', 'r') as lp:
        list_chessplayers_tournament = json.load(lp)
        number_players = len(list_chessplayers_tournament)
        print("nombre de joueurs inscrits au tounoi :", len(list_chessplayers_tournament))
        print(list_chessplayers_tournament)
    
    return list_chessplayers_tournament, number_players


def new_round():
        
    """1. Création d'une round,
    2. Enregistrement de cette round dans un fichier contenant toutes les rounds"""
    tournament_register1, name_tournament1, number_of_rounds = which_tournament()
    number_of_rounds = number_of_rounds
    name_tournament = name_tournament1
    print(f"Ce tournoi contient {number_of_rounds} rounds.")
    number_round = input ("Quelle round souhaitez-vous lancer?")
    start_date_round = input("Veuillez entrer la date du début de la round :")
    start_hour = input("Veuillez entrer l'heure exacte du début de la round :")
    end_date_round = ("")
    end_hour = ("")
    list_chessplayers_tournament, number_players = create_list_players_tournament(tournament_register1)
    print(f"La round {number_round} contient {number_players} joueurs.")
    list_players_round=list_chessplayers_tournament
    list_matches = create_matches(number_round, number_of_rounds, number_players, list_players_round)    
    """création d'une round"""
    round = Round(name_tournament=name_tournament, number_of_rounds=number_of_rounds, number_round=number_round, start_date_round=start_date_round, start_hour=start_hour, end_date_round=end_date_round, end_hour=end_hour, list_players_round=list_players_round, list_matches=list_matches)

    info_round={"Nom du tournoi" : round.name_tournament, "Nombre de rounds" : round.number_of_rounds, "Round": round.number_round, "Date de lancement":round.start_date_round, "Heure de lancement":round.start_hour, "Date de fin":round.end_date_round, "Fin de la round":round.end_hour, "Liste des appariements":round.list_matches, "Liste des joueurs":round.list_players_round}

    """Enregistrement des infos de la round dans le fichier round du tournoi"""
    list_rounds=[]
    list_rounds.append(info_round)

    tourmanent_rounds_file = 'rounds_'+tournament_register1
    tourmanent_register_case = tournament_register1+'/'

    with open('chess_data/'+tourmanent_register_case+ tourmanent_rounds_file+'.json', 'w', encoding='utf-8') as lp:
        if lp.tell() > 0:
            lp.write(',')
        json.dump(list_rounds, lp, indent=4)
        
    return number_round, tournament_register1



def create_matches(number_round, number_of_rounds, number_players, list_players_round):
    #round = round.number_round
    #print("Nom de la round :",round)
    #list_chessplayers_tournament, _ = create_list_players_tournament()
    round_int = int(number_round)
    number_of_rounds_int = int(number_of_rounds)
    number_players_int = int(number_players)
    number_tables = number_players_int//2+number_players%2
    list_ffe_round =[]
    list_pairing = [] 
    list_ffe_round = [element["Numero FFE"] for element in list_players_round]
    n = 1
    
    if round_int==1:
        """Creation des appariements de la premiere round de manière aléatoire"""        
        random.shuffle(list_ffe_round)
        for i in range(0, len(list_ffe_round),2):
            list_pairing.append((list_ffe_round[i], list_ffe_round[i+1],"table"+str(n)))
            n += 1 and n <= number_tables
        return list_pairing
    
    elif 1< round_int <= number_of_rounds_int:
        """ création des autres rounds en fonction des résultats des joueurs"""
        pass

    else :
        print("Cette round n'existe pas")
        return None



#create_matches()

new_round()

#x = 24//2+24%2
#print(x)