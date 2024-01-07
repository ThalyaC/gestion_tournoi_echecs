#from tournament import Tournament
import json
from registration_players_tourmanent import open_list_tournaments, create_file_folder_name, seek_player_ffe
import random


class Round:
    "création d'un round"
    def __init__(self, name_tournament, number_of_rounds, number_round, start_date_round, end_date_round,start_hour, end_hour, list_players_round, list_matches, number_tables):
        self.name_tournament=name_tournament
        self.number_of_rounds=number_of_rounds
        self.number_round = number_round
        self.start_date_round = start_date_round
        self.end_date_round = end_date_round
        self.start_hour = start_hour #automatique (import datatime p267)
        self.end_hour = end_hour
        self.list_players_round = list_players_round
        self.list_matches= list_matches
        self.number_tables = number_tables

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
        print("1. nombre de joueurs inscrits au tounoi :", len(list_chessplayers_tournament))
        print("2.",list_chessplayers_tournament)
    
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
    list_matches, number_tables = create_matches(number_round, number_of_rounds, number_players, list_players_round)
        
    """création d'une round"""
    round = Round(name_tournament=name_tournament, number_of_rounds=number_of_rounds, number_round=number_round, start_date_round=start_date_round, start_hour=start_hour, end_date_round=end_date_round, end_hour=end_hour, list_players_round=list_players_round, list_matches=list_matches, number_tables=number_tables)

    info_round={"Nom du tournoi" : round.name_tournament, "Nombre de rounds" : round.number_of_rounds, "Round": round.number_round, "Date de lancement":round.start_date_round, "Heure de lancement":round.start_hour, "Round finie le":round.end_date_round, "Heure de fin":round.end_hour, "Nombre de tables en cours de jeu":round.number_tables, "Liste des appariements":round.list_matches, "Liste des joueurs":round.list_players_round}

    """Enregistrement des infos de la round dans le fichier round du tournoi"""
    #list_rounds=[]
    #list_rounds.append(info_round)

    tourmanent_rounds_file = 'rounds_'+tournament_register1
    tourmanent_register_case = tournament_register1+'/'

    try :
        with open('chess_data/'+tourmanent_register_case+ tourmanent_rounds_file+'.json', 'r') as lp:
            list_rounds = json.load(lp)
       
    except:
        list_rounds=[]

    list_rounds.append(info_round)

    with open('chess_data/'+tourmanent_register_case+ tourmanent_rounds_file+'.json', 'a', encoding='utf-8') as lp:
        """Attention, pour le moment, ne vérifie pas si la round est djà existante!!!"""
        if lp.tell() > 0:
            lp.write(',')
        json.dump(list_rounds, lp, indent=4)
        
    return number_round, tournament_register1

"""
def create_pair(list_ffe_round, list_players_round, number_tables):
    n = 1
    list_pairing=[]
    for i in range(0, len(list_ffe_round),2):
        if i + 1 < len(list_ffe_round):
            new_table = "table"+str(n)
            list_pairing.append(("Blanc :"+str(list_ffe_round[i]), "Noir :"+str(list_ffe_round[i+1]),new_table))
        else:
            list_pairing.append(("Blanc :"+str(list_ffe_round[i]), "Noir : exempt","table"+str(n), "score :0.5-_"))
            player1 = list_ffe_round[i]
            print("player1",player1)
            score_player1_3 = 0.5
            key_score = "score"
            for player_round in list_players_round:
                if key_score in player_round:
                    player_exempt = player_round
                    score_player1_2 = float(player_round["score"])
                    player_round["score"] = score_player1_2 + score_player1_3
                    break
            print("joueur exempt:",player_exempt)
        n += 1
        if n > number_tables:
            break
    return list_pairing
        #return list_pairing, round_int
"""

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
    print(list_players_round)
    n = 1
    
    if round_int==1:
        """Creation des appariements de la premiere round de manière aléatoire"""        
        random.shuffle(list_ffe_round)
        #create_pair(list_ffe_round, list_players_round, number_tables)
        
        for i in range(0, len(list_ffe_round),2):
            if i + 1 < len(list_ffe_round):
                list_pairing.append(("Blanc :"+list_ffe_round[i], "Noir :"+list_ffe_round[i+1],"table"+str(n)))
            else:
                list_pairing.append(("Blanc :"+list_ffe_round[i], "Noir : exempt","table"+str(n), "score :0.5-_"))
                player1_ffe = list_ffe_round[i]
                print("player1",player1_ffe)
                score_player1_3 = 0.5
                #key_score = "score"
                key_ffe = "Numero FFE"
                for player_round in list_players_round:
                    if key_ffe in player_round and player_round[key_ffe] == player1_ffe:
                        player_exempt = player_round
                        score_player1_2 = float(player_round["score"])
                        player_round["score"] = score_player1_2 + score_player1_3
                        break
                print("joueur exempt:",player_exempt)
            n += 1
            if n > number_tables:
                break
        return list_pairing, number_tables
    
    elif 1 < round_int <= number_of_rounds_int:
        """ création des autres rounds en fonction des résultats des joueurs"""
        #key_score = "score"
        #list_sorted_by_score = sorted(list_players_round, key=lambda x: x["score"])
        #create_pair(list_sorted_by_score, list_players_round, number_tables)
        #return list_pairing, number_tables
        pass


    else :
        print("Cette round n'existe pas")
        return None

def score_recording():
    """Enregistrer les scores pour les appariements puis pour les joueurs individuellement"""
    tournament_register1, _, _ = which_tournament()
    number_round_score1 = input ("Dans quelle round souhaitez-vous enregistrer un score?")
    table_score2 = input ("Quelle table? (tapez juste un numéro)")
    table_score1 = "table" + table_score2
    table_score = str(table_score1)
    print("1.",table_score)
    
    with open('chess_data/'+tournament_register1+'/rounds_'+tournament_register1+'.json', 'r') as lp:
        list_info_current_tournament = json.load(lp)
      
    
    for number_round_score in list_info_current_tournament:
        """Pour accéder à la round demandée"""
        
        """Nombre de tables à enregistrer"""
        remaining_tables1 = number_round_score["Nombre de tables en cours de jeu"]
        print(f"Il reste {remaining_tables1} table(s) à enregistrer")
        
        if number_round_score.get("Round")==number_round_score1:

            """inscription des scores dans la liste d'appariement"""
            list_pairing = number_round_score['Liste des appariements']
            print("2;",list_pairing, len(list_pairing))
            info_pairing = list_pairing[int(table_score2)-1]
            print(info_pairing)
            add_score1 = input("Entrez le score (1-0,0-1 ou 0.5-0.5)")
            add_score = "Score :"+add_score1
            info_pairing.append(add_score)
            requested_table=info_pairing
            print("12.",requested_table)
            
            """Mise à jour du nombre de tables"""
            number_round_score["Nombre de tables en cours de jeu"] = remaining_tables1-1

            """Création automatique de la date et heure de fin de la round"""
            remaining_tables = number_round_score["Nombre de tables en cours de jeu"]
            if remaining_tables==0 :
                pass




            

            """inscription et modification des scores dans la liste des joueurs"""
            individual_score = add_score1.split("-")
            print(individual_score)
            score_player1_2 = float(individual_score[0])
            score_player2_2 = float(individual_score[1])
            print(f"joueur 1: {score_player1_2}, joueur 2: {score_player2_2}")
            
            player_1_2 = requested_table[0]
            player_2_2 = requested_table[1]
            player_1_1 = player_1_2[-7:]
            player_2_1 = player_2_2[-7:]

            list_individual = number_round_score['Liste des joueurs']
            #print(list_individual)
            player_1 = seek_player_ffe(list_individual, player_1_1)
            player_2 = seek_player_ffe(list_individual, player_2_1)
            print(player_1, player_2)
            
            score_player1_1 = float(player_1["score"])
            score_player1 = score_player1_1 + score_player1_2
            player_1["score"] = score_player1
            #print(score_player1)
            score_player2_1 = float(player_2["score"])
            score_player2 = score_player2_1 + score_player2_2
            player_2["score"] = score_player2
    
    with open('chess_data/'+tournament_register1+'/rounds_'+tournament_register1+'.json', 'w') as lp:
        json.dump(list_info_current_tournament, lp, indent=4)
        
        
        """for info_pairing in list_pairing:
                print("3.",info_pairing)
                if table_score in info_pairing:
                    #requested_table1 = tables
                    #requested_table = list_pairing[requested_table1]
                    add_score1 = input("Entrez le score (1-0,0-1 ou X-X)")
                    add_score = "Score :"+add_score1
                    #requested_table.append(add_score)
                    info_pairing.append(add_score)
                    requested_table=info_pairing
                    print(requested_table)
                    break
                else:
                    print("Cette table n'existe pas")
                    return None
            #print(requested_table)
            
    
            #individual_score1 = add_score.split("-")
            #print(individual_score1)
    
    with open('chess_data/'+tournament_register1+'/rounds_'+tournament_register1+'.json', 'w') as lp:
        json.dump(list_info_current_tournament, lp, indent=4)



            


    
def score_recording():
    Enregistrer les scores
    tournament_register1, name_tournament1, number_of_rounds = which_tournament()
    number_round_score = input ("Dans quelle round souhaitez-vous enregistrer un score?")
    previous_round2 = int(number_round_score)-1
    previous_round1 = str(previous_round2)
    table_score = input ("Quelle table? (tapez juste un numéro)")
    
    with open('chess_data/'+tournament_register1+'/rounds_'+tournament_register1+'.json', 'r') as lp:
        list_info_current_tournament = json.load(lp)
    
    for previous_round in list_info_current_tournament:
        if previous_round.get("Round")==previous_round1:
            print(previous_round)"""

#create_matches()


#new_round()

#x = 24//2+24%2
#print(x)
#score_recording()