import json
from os import mkdir

"""Pour le moment, seuls les joueurs enregistrés dans la base de données du club peuvent être inscrits, à élargir plus tard """

def seek_player_ffe(list_chessplayers,ffe_number_register):
    """Trouver un joueur à partir de son numéro FFE"""
    for player in list_chessplayers:
        if player.get("Numero FFE")==ffe_number_register:
            return player
    return None

def list_of_numbered_tournaments(liste_tournaments):
    """Donner un numéro à un tournoi pour éviter par la suite à l'utilisateur de le saisir"""
    for i, nom_tournoi in enumerate(liste_tournaments, start=1):
        print(f"{i}. {nom_tournoi}")

def choose_tournament():
    """Proposer à l'utilisateur de choisir un tournoi dans une liste donnée à partir d'un numéro attribué à chaque tournoi"""
    try :
        choice = int(input("Choisissez le numéro qui correspond au tournoi souhaité :"))
        return choice
    
    except ValueError:
        print("Ce n'est un numéro valide.")
        return None

def create_file_folder_name(list_tournaments):
    """Créer le nom du dossier ou d'une partie du fichier 
    lié au tournoi à partir d'un numéro"""
    list_of_numbered_tournaments(list_tournaments)
    choice_user=choose_tournament()

    if choice_user is not None and 1<= choice_user <= len(list_tournaments):
        name_tournament=list_tournaments[choice_user - 1]
        print("Vous avez choisi le tournoi :", name_tournament)
        name_tournament_file_folder = name_tournament.replace(" ","_")
        return name_tournament, name_tournament_file_folder

    else :
        return print("erreur de saisie")


def open_list_chessplayers():
    with open('chess_data/list_players1.json', 'r') as lp:
        list_chessplayers = json.load(lp)
    return list_chessplayers

def open_list_tournaments():
    'Transforme le fichier chess_data/list_tournaments.json en liste'
    with open('chess_data/list_tournaments.json', 'r') as lp:
        list_tournaments = json.load(lp)
    return list_tournaments

def register_players_tournament():
    """Objectif : inscrire un joueur à un tournoi.
    vérifie si à partir du numéro FFE, le joueur est inscrit sur la liste générale du club;
    Demande à l'utilisateur de sélectionner par le biai d'un numéro le tournoi souhaité;
    créer si nécessaire le dossier du tournoi et le fichier recevant les joueurs inscrits 
    pour ce tournoi;
    enregistre le joueur dans le fichier.
    Ajoute un score =0
    !!! pas de vérification pour le moment si l'inscription du joueur dans le fichier existe déjà
    """
    
    list_chessplayers = open_list_chessplayers()
    list_tournaments = open_list_tournaments()
    
    list_tournaments_nom = [element["Nom"] for element in list_tournaments]

    ffe_number_register = input("Numéro de licence (du type AB12345) :")

    seek_player = seek_player_ffe(list_chessplayers,ffe_number_register)

    if seek_player:
        print("personne à inscrire :", seek_player)
        #print(liste_tournaments)
        _, tourmanent_register1 = create_file_folder_name(list_tournaments_nom)
        tourmanent_register = 'players_'+tourmanent_register1
        tourmanent_register_case = tourmanent_register1+'/'
        try :
         with open('chess_data/'+tourmanent_register_case+tourmanent_register+'.json', 'r') as lp:
            list_players_tournament = json.load(lp)
       
        except:
            list_players_tournament=[]
       
            try:
                mkdir('chess_data/'+tourmanent_register_case)
            except OSError :
                pass
            finally :
                pass
        
        """Pour ajouter au profil du joueur un score initial = 0"""
        score = 'score'
        seek_player[score] = 0

        list_players_tournament.append(seek_player)

        with open('chess_data/'+tourmanent_register_case+tourmanent_register+'.json','w', encoding='utf-8') as lp:
            if lp.tell() > 0:
                lp.write(',')
            json.dump(list_players_tournament, lp, indent=4)

    else:
        print("Personne ne correspond à ce numéro FFE")

#register_players_tournament()