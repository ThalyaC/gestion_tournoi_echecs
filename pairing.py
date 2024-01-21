#from tournament import Tournament
import json
from registration_players_tourmanent import open_list_tournaments, create_file_folder_name, seek_player_ffe
import random
from datetime import datetime
import sys


class Round:
    "création d'un round"
    def __init__(self, name_tournament, number_round, current_round, start_date_round, end_date_round,start_hour, end_hour, list_matches, number_tables, status):
        self.name_tournament=name_tournament
        #self.number_of_rounds=number_of_rounds
        self.number_round = number_round
        self.current_round = current_round # format "a/b"
        self.start_date_round = start_date_round
        self.end_date_round = end_date_round
        self.start_hour = start_hour
        self.end_hour = end_hour
        #self.list_players_round = list_players_round
        self.list_matches= list_matches
        self.number_tables = number_tables
        self.status = status

    #def add_match(self, info_match):
        #"""Ajoute un match au round en cours de création"""
        #self.list_matches.append(info_match)
    

class Match:
    def __init__(self, table, white, black, score_players):
        self.white = white
        self.black = black
        self.score_player1_2 = score_players
        self.table = table
    


def which_tournament(): #
    """
    1. Demande à l'utilisateur de choisir un tournoi, 
    2. récupère les éléments nécessaires à la création d'une round"""
    list_tournaments = open_list_tournaments()
    
    """nom du tournoi"""
    list_tournaments_name = [element["Nom"] for element in list_tournaments]
    name_tournament1, tournament_register1 = create_file_folder_name(list_tournaments_name)
    
    for tournament in list_tournaments:
        """Donne le nombre de rounds contenus dans le tournoi demandé"""
        if "Nom" in tournament and tournament["Nom"]==name_tournament1:
            number_of_rounds = tournament.get("Nombre de rounds")

    return tournament_register1, name_tournament1, number_of_rounds

def create_list_players_tournament(tournament_register1): #
    
    """Crée une liste de joueurs à partir 
    du fichier players du tournoi choisi par l'utilisateur et indique le nombre de joueurs"""
    tournament_register_players = 'players_'+tournament_register1
    tournament_register_case = tournament_register1+'/'
    players_file_tournament = 'chess_data/'+tournament_register_case+tournament_register_players+'.json'
    with open(players_file_tournament, 'r') as lp:
        list_chessplayers_tournament = json.load(lp)
        number_players = len(list_chessplayers_tournament)
        print("1. nombre de joueurs inscrits au tounoi :", len(list_chessplayers_tournament))
        print("2.",list_chessplayers_tournament)
    
    return list_chessplayers_tournament, number_players, players_file_tournament


def new_round():
        
    """1. Création d'une round,
    2. Enregistrement de cette round dans un fichier contenant toutes les rounds"""
    tournament_register1, name_tournament1, number_of_rounds = which_tournament()
    number_of_rounds = number_of_rounds
    name_tournament = name_tournament1
    print(f"Ce tournoi contient {number_of_rounds} rounds.")
    
    number_round = input ("Quelle round souhaitez-vous lancer?")
    current_round = number_round+"/"+number_of_rounds
    start_round = datetime.now()
    start_date_round = start_round.strftime("%d.%m.%y")
    start_hour = start_round.strftime("%H.%M")
    end_date_round = ("") # Cela sera affecté à la fin de la round dans score_recording
    end_hour = ("") # idem
    list_chessplayers_tournament, number_players, players_file_tournament = create_list_players_tournament(tournament_register1)
    print(f"La round {current_round} contient {number_players} joueurs.")

    tourmanent_rounds_file = 'rounds_'+tournament_register1
    tourmanent_register_case = tournament_register1+'/'
    path_tourmanent_rounds_file = 'chess_data/'+tourmanent_register_case+ tourmanent_rounds_file+'.json'
    list_rounds1=[] # résout le pb d'effacement yes!

    list_players_round = list_chessplayers_tournament
    result = create_matches(number_round, number_of_rounds, number_players, list_players_round, players_file_tournament, path_tourmanent_rounds_file)
    what_else(result)
    list_matches, number_tables = result    
    """création d'une round"""
    round = Round(name_tournament=name_tournament, number_round = number_round, current_round=current_round, start_date_round=start_date_round, start_hour=start_hour, end_date_round=end_date_round, end_hour=end_hour, list_matches=list_matches, number_tables=number_tables, status="En cours")
    info_round_common = {"Nom du tournoi" : round.name_tournament, "Round" : round.current_round}
    info_round={"Round" : round.number_round, "Etat":round.status, "Date de lancement":round.start_date_round, "Heure de lancement":round.start_hour, "Round finie le":round.end_date_round, "Heure de fin":round.end_hour, "Nombre de tables en cours de jeu":round.number_tables, "Liste des appariements":round.list_matches}
    
    """
    1ere modif
    if number_round==1: ##
        round = Round(name_tournament=name_tournament, number_round = number_round, current_round=current_round, start_date_round=start_date_round, start_hour=start_hour, end_date_round=end_date_round, end_hour=end_hour, list_matches=list_matches, number_tables=number_tables)
        info_round_common = {"Nom du tournoi" : round.name_tournament, "Round" : round.current_round}
        info_round1 = {"Round":round.number_round,"Date de lancement":round.start_date_round, "Heure de lancement":round.start_hour, "Round finie le":round.end_date_round, "Heure de fin":round.end_hour, "Nombre de tables en cours de jeu":round.number_tables, "Liste des appariements":round.list_matches}
        info_round = info_round_common, info_round1

    else:
        round = Round(name_tournament=name_tournament, current_round=current_round, start_date_round=start_date_round, start_hour=start_hour, end_date_round=end_date_round, end_hour=end_hour, list_matches=list_matches, number_tables=number_tables)
        info_round={"Nom du tournoi" : round.name_tournament, "Round" : round.current_round, "Date de lancement":round.start_date_round, "Heure de lancement":round.start_hour, "Round finie le":round.end_date_round, "Heure de fin":round.end_hour, "Nombre de tables en cours de jeu":round.number_tables, "Liste des appariements":round.list_matches}
    
   
    avant modif :
    round = Round(name_tournament=name_tournament, current_round=current_round, start_date_round=start_date_round, start_hour=start_hour, end_date_round=end_date_round, end_hour=end_hour, list_matches=list_matches, number_tables=number_tables)
    info_round={"Nom du tournoi" : round.name_tournament, "Round" : round.current_round, "Date de lancement":round.start_date_round, "Heure de lancement":round.start_hour, "Round finie le":round.end_date_round, "Heure de fin":round.end_hour, "Nombre de tables en cours de jeu":round.number_tables, "Liste des appariements":round.list_matches}
    """
    
    
    """Enregistrement des infos de la round dans le fichier round du tournoi
    tourmanent_rounds_file = 'rounds_'+tournament_register1
    tourmanent_register_case = tournament_register1+'/'
    list_rounds1=[] # résout le pb d'effacement yes!"""

    try :
        with open(path_tourmanent_rounds_file, 'r') as lp:
            list_rounds2 = json.load(lp)
            (print(list_rounds2))
            for one_round in list_rounds2:
                list_rounds1.append(one_round)
                list_rounds=list_rounds1
       
    except:
        list_rounds=[]

    if list_rounds==[]:
        list_rounds.append(info_round_common)
        list_rounds.append(info_round)

    else:
        update_current_round = current_round
        list_rounds[0]["Round"] = update_current_round
        list_rounds.append(info_round)
    

    with open(path_tourmanent_rounds_file, 'w', encoding='utf-8') as lp:
        """Attention, pour le moment, ne vérifie pas si la round est djà existante!!!"""
        if lp.tell() > 0:
            lp.write(',')
        json.dump(list_rounds, lp, indent=4)
        
    return number_round, tournament_register1

def update_score_players_tournament(players_file_tournament, list_players_tournament):
    "Permettre aux autres fonctions de mettre à jour les données dans le fichier des joueurs du tournoi"
    with open(players_file_tournament,'w', encoding='utf-8') as lp:
            if lp.tell() > 0:
                lp.write(',')
            json.dump(list_players_tournament, lp, indent=4)


def create_matches(number_round, number_of_rounds, number_players, list_players_round, players_file_tournament, path_tourmanent_rounds_file):
    
    """Création des matches"""
    round_int = int(number_round)
    number_of_rounds_int = int(number_of_rounds)
    number_players_int = int(number_players)
    number_tables = number_players_int//2+number_players%2
    list_ffe_round =[]
    list_matches = [] 
    list_ffe_round = [element["Numero FFE"] for element in list_players_round]
    print(list_players_round)
    n = 1
    
    if round_int==1:
        
        """Creation des appariements de la premiere round de manière aléatoire"""        
        random.shuffle(list_ffe_round)
        """
        result = create_match(list_ffe_round, list_matches, list_players_round, players_file_tournament, number_tables)
        
        if result is not None:
            list_matches, number_tables = result

        else :
            pass        
        """
        for i in range(0, len(list_ffe_round),2):
            
            """Création d'un match simple"""
            if i + 1 < len(list_ffe_round):
                white = list_ffe_round[i] #
                black = list_ffe_round[i+1] #
                table = n # 
                match = Match(table=table, white=white, black=black, score_players=" ")
                info_match={"Table" : match.table, "Blanc": match.white, "Noir":match.black, "score": match.score_player1_2}
                #Round.add_match(info_match)
                list_matches.append(info_match)
                #list_pairing.append(("Blanc :"+list_ffe_round[i], "Noir :"+list_ffe_round[i+1],"table"+str(n)))
            
            else:
                """Si le nombre de joueurs est impair, création d'une dernière table avec un joueur exempté, 
                enregistrement automatique du score 0.5-_"""
                #list_pairing.append(("Blanc :"+list_ffe_round[i], "Noir : exempt","table"+str(n), "score :0.5-_"))
                white = list_ffe_round[i] #
                black = "exempt" #
                table = n # 
                match = Match(table=table, white=white, black=black, score_players="0.5-_")
                info_match={"Table" : match.table, "Blanc": match.white, "Noir":match.black, "score": match.score_player1_2}
                #Round.add_match(info_match)
                list_matches.append(info_match)
                player1_ffe = list_ffe_round[i]
                print("Blanc :",player1_ffe)
                score_player1_3 = 0.5
                key_ffe = "Numero FFE"

                #Soustraction automatique de ce match au nombre de tables en jeu
                number_tables = number_tables-1
                
                "Ajout automatique de 0.5 point au joueur exempté"
                for player_round in list_players_round:
                    if key_ffe in player_round and player_round[key_ffe] == player1_ffe:
                        player_exempt = player_round
                        score_player1_2 = float(player_round["score"])
                        player_round["score"] = score_player1_2 + score_player1_3
                        update_score_players_tournament(players_file_tournament, list_players_round)
                        break
                print("joueur exempt:",player_exempt)
            n += 1
            if n > number_tables:
                break
        return list_matches, number_tables
    
    elif 1 < round_int <= number_of_rounds_int:

        """ création des autres rounds en fonction des résultats des joueurs"""

        """Vérifier que tous les scores de la round précédente ont été enregistrés"""
        round_int_previous = round_int-1
        list_provisional1 = []
        
        with open(path_tourmanent_rounds_file, 'r') as lp:
            list_provisional2 = json.load(lp)
            for one_round in list_provisional2:
                list_provisional1.append(one_round)
                list_provisional=list_provisional1
        

        for round_previous in list_provisional:
            if round_previous["Round"] == round_int_previous:
                status_previous = round_previous["Etat"]
                if status_previous == "Clos":
                    list_sorted_by_score = sorted(list_players_round, key=lambda x: x["score"], reverse=True)
                    print(list_sorted_by_score)

                    for i in range(0, len(list_ffe_round),2):
                        
                        """Création d'un match simple"""
                        if i + 1 < len(list_ffe_round):
                            white = list_ffe_round[i] #
                            black = list_ffe_round[i+1] #

                            table = n # 
                            match = Match(table=table, white=white, black=black, score_players=" ")
                            info_match={"Table" : match.table, "Blanc": match.white, "Noir":match.black, "score": match.score_player1_2}
                            #Round.add_match(info_match)
                            list_matches.append(info_match)
                            #list_pairing.append(("Blanc :"+list_ffe_round[i], "Noir :"+list_ffe_round[i+1],"table"+str(n)))
                        
                        else:
                            """Si le nombre de joueurs est impair, création d'une dernière table avec un joueur exempté, 
                            enregistrement automatique du score 0.5-_"""
                            #list_pairing.append(("Blanc :"+list_ffe_round[i], "Noir : exempt","table"+str(n), "score :0.5-_"))
                            white = list_ffe_round[i] #
                            black = "exempt" #
                            table = n # 
                            match = Match(table=table, white=white, black=black, score_players="0.5-_")
                            info_match={"Table" : match.table, "Blanc": match.white, "Noir":match.black, "score": match.score_player1_2}
                            #Round.add_match(info_match)
                            list_matches.append(info_match)
                            player1_ffe = list_ffe_round[i]
                            print("Blanc :",player1_ffe)
                            score_player1_3 = 0.5
                            key_ffe = "Numero FFE"

                            #Soustraction automatique de ce match au nombre de tables en jeu
                            number_tables = number_tables-1
                            
                            "Ajout automatique de 0.5 point au joueur exempté"
                            for player_round in list_players_round:
                                if key_ffe in player_round and player_round[key_ffe] == player1_ffe:
                                    player_exempt = player_round
                                    score_player1_2 = float(player_round["score"])
                                    player_round["score"] = score_player1_2 + score_player1_3
                                    update_score_players_tournament(players_file_tournament, list_players_round)
                                    break
                            print("joueur exempt:",player_exempt)
                        n += 1
                        if n > number_tables:
                            break
                    return list_matches, number_tables
            else :
                print("Les scores de la round précédente n'ont pas tous été enregistrés")
                return None
    else :
        print("Cette round n'existe pas")
        return None
    
# STOP ICI à faire : modifier fonction create matches pour éviter répétition des tables, 
# mise à jour de score_recording puis affichage des rounds

def score_recording():
    
    """Enregistrer les scores pour les appariements, 
    mise à jour du nombre de matches restants,
    puis pour les joueurs individuellement"""
    tournament_register1, _, _ = which_tournament()
    number_round_score2 = input ("Dans quelle round souhaitez-vous enregistrer un score?")
    number_round_score1 = int(number_round_score2)
    
    
    """Pour accéder à la round demandée"""
    with open('chess_data/'+tournament_register1+'/rounds_'+tournament_register1+'.json', 'r') as lp:
        list_info_current_tournament = json.load(lp)

    try:  
        round_info_total = list_info_current_tournament[number_round_score1]
    except:
        print("Cette round n'a pas été encore créée ou vous avez fait une erreur de saisie")
        sys.exit(0)

    table_score2 = input ("Quelle table? (tapez juste un numéro)")
    #table_score1 = "table" + table_score2
    table_score1 = int(table_score2)
    table_score = str(table_score2)
    
    print("1.",table_score)
    print (len(round_info_total))
    print (round_info_total)
    remaining_tables1 = round_info_total["Nombre de tables en cours de jeu"]
    print (remaining_tables1)
    print(f"Il reste {remaining_tables1} table(s) à enregistrer")

    """

    for number_round_score in round_info_total:
        print(number_round_score["Nombre de tables en cours de jeu"])

    


    for number_round_score in round_info_total:   
        #Nombre de tables à enregistrer
        number_round_common = number_round_score[0]
        number_round_common[7]
        print(remaining_tables1)
        print(f"Il reste {remaining_tables1} table(s) à enregistrer")
    """
    #STOP ICI
        


    """inscription des scores dans la liste d'appariement"""
    list_pairing = round_info_total['Liste des appariements']
    print("2;",list_pairing, len(list_pairing))
    info_pairing = list_pairing[int(table_score2)-1]
    print(info_pairing)
    add_score = input("Entrez le score (1-0,0-1 ou 0.5-0.5)")
    info_pairing["score"] = add_score
    print("12.",info_pairing)
    
    """Mise à jour du nombre de tables"""
    round_info_total["Nombre de tables en cours de jeu"] = remaining_tables1-1

    """Création automatique de la date et heure de fin de la round"""
    remaining_tables = round_info_total["Nombre de tables en cours de jeu"]
    if remaining_tables==0 :
        end_round = datetime.now()
        date_end = end_round.strftime("%d.%m.%y")
        hour_end = end_round.strftime("%H.%M")
        round_info_total["Heure de fin"] = hour_end
        round_info_total["Round finie le"] = date_end


    """inscription et modification des scores dans la liste des joueurs"""
    individual_score = add_score.split("-")
    print(individual_score)
    score_player1_2 = float(individual_score[0])
    score_player2_2 = float(individual_score[1])
    print(f"joueur 1: {score_player1_2}, joueur 2: {score_player2_2}")
    
    # Le numéro FFE des joueurs
    player_1_1 = info_pairing["Blanc"]
    player_2_1 = info_pairing["Noir"]
    #player_1_1 = player_1_2[-7:]
    #player_2_1 = player_2_2[-7:]

    #list_individual = number_round_score['Liste des joueurs']
    #print(list_individual)
    with open('chess_data/'+tournament_register1+'/players_'+tournament_register1+'.json', 'r') as lp:
        list_individual = json.load(lp)
    
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

    with open('chess_data/'+tournament_register1+'/players_'+tournament_register1+'.json','w', encoding='utf-8') as lp:
        json.dump(list_individual, lp, indent=4)

     


def what_else(result):
    "Vérifie que l'opération est possible"
    if result == None:
        print("Fin")
        sys.exit(0)
    else :
        pass

#create_matches()




score_recording()
#new_round()
"""
ne marche pas
def create_match(list_ffe_round, list_matches, list_players_round, players_file_tournament, number_tables):
    n = 1
    for i in range(0, len(list_ffe_round),2):
            
        
        if i + 1 < len(list_ffe_round):
            white = list_ffe_round[i] #
            black = list_ffe_round[i+1] #
            table = n # 
            match = Match(table=table, white=white, black=black, score_players=" ")
            info_match={"Table" : match.table, "Blanc": match.white, "Noir":match.black, "score": match.score_player1_2}
            #Round.add_match(info_match)
            list_matches.append(info_match)
            #list_pairing.append(("Blanc :"+list_ffe_round[i], "Noir :"+list_ffe_round[i+1],"table"+str(n)))    
            
        else:
            
            #list_pairing.append(("Blanc :"+list_ffe_round[i], "Noir : exempt","table"+str(n), "score :0.5-_"))
            white = list_ffe_round[i] #
            black = "exempt" #
            table = n # 
            match = Match(table=table, white=white, black=black, score_players="0.5-_")
            info_match={"Table" : match.table, "Blanc": match.white, "Noir":match.black, "score": match.score_player1_2}
            #Round.add_match(info_match)
            list_matches.append(info_match)
            player1_ffe = list_ffe_round[i]
            print("Blanc :",player1_ffe)
            score_player1_3 = 0.5
            key_ffe = "Numero FFE"

           
            number_tables = number_tables-1
            
            "Ajout automatique de 0.5 point au joueur exempté"
            for player_round in list_players_round:
                if key_ffe in player_round and player_round[key_ffe] == player1_ffe:
                    player_exempt = player_round
                    score_player1_2 = float(player_round["score"])
                    player_round["score"] = score_player1_2 + score_player1_3
                    update_score_players_tournament(players_file_tournament, list_players_round)
                    break
            print("joueur exempt:",player_exempt)
        n += 1
        if n > number_tables:
            break
    
"""
