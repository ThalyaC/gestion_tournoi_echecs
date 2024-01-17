import json
from os import mkdir
from chess_player import register_player


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
    
    - Vérifie si le joueur est déjà inscrit au tournoi - si oui fin de la procédure;
    - sinon à partir du numéro FFE, le joueur est recherché dans la liste générale du club;
        - si non enregistré : inscription du joueur dans le fichier général;
        - inscription dans le tournoi choisi :
            - Demande à l'utilisateur de sélectionner par le biai d'un numéro le tournoi souhaité;
            - crée si nécessaire le dossier du tournoi et le fichier recevant les joueurs inscrits 
            pour ce tournoi;
            - enregistre le numéro FFE du joueur dans le fichier.
            - Ajoute un score =0
    
    Problème : si le joueur n'a jamais été enregistré, l'utilisateur doit saisir 3 fois le n FFE
    """
    
    list_chessplayers = open_list_chessplayers()
    list_tournaments = open_list_tournaments()
    
    list_tournaments_nom = [element["Nom"] for element in list_tournaments]
    
    ffe_number_register = input("Numéro de licence (du type AB12345) tournoi:")
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
            
                # Si un joueur est déjà inscrit à ce tournoi
                seek_player_old = seek_player_ffe(list_players_tournament, ffe_number_register)
                if seek_player_old :           
                    print("Ce joueur est déjà enregistré dans ce tournoi")
                    return None
                
        except:
            list_players_tournament=[]
       
            try:
                mkdir('chess_data/'+tourmanent_register_case)
            except OSError :
                pass
            finally :
                pass
        
        #Pour ajouter au profil du joueur un score initial = 0
        player_tournament = {}
        player_tournament['Numero FFE'] = seek_player['Numero FFE']
        player_tournament ['score'] = 0

        list_players_tournament.append(player_tournament)

        with open('chess_data/'+tourmanent_register_case+tourmanent_register+'.json','w', encoding='utf-8') as lp:
            if lp.tell() > 0:
                lp.write(',')
            json.dump(list_players_tournament, lp, indent=4)

    else:         
        print("Ce joueur n'est pas enregistré dans la base du club.")
        response = input("Souhaitez-vous l'enregistrer? (Y pour oui/N pour non)")
        if response == "Y":
            register_player()
            register_players_tournament()
        else :
            return print("Fin")
           
def display_on_screen_players_tournament():
    
    """Afficher à l'écran, par ordre alphabétique, la liste de joueurs inscrits à un tournoi"""
    list_tournaments = open_list_tournaments()
    list_tournaments_nom = [element["Nom"] for element in list_tournaments]
    _, tourmanent_register1 = create_file_folder_name(list_tournaments_nom)
    tourmanent_register = 'players_'+tourmanent_register1
    tourmanent_register_case = tourmanent_register1+'/'
    with open('chess_data/'+tourmanent_register_case+tourmanent_register+'.json', 'r') as lp:
        list_players_tournament = json.load(lp)
    
    screen_players = []
    list_players_tournament_ffe = [element['Numero FFE'] for element in list_players_tournament]
    list_chess_players = open_list_chessplayers()
    for player_tournament_ffe1 in list_players_tournament_ffe:
        player_tournament_ffe = seek_player_ffe(list_chess_players, player_tournament_ffe1)
        for player_tournament_ffe1 in list_players_tournament:
            score1 = player_tournament_ffe1['score']
                
        screen_player1 = (player_tournament_ffe["Numero FFE"], player_tournament_ffe["Nom"], player_tournament_ffe["Prenom"], score1)
        screen_players.append(screen_player1)
    
    screen_players_alpha = sorted(screen_players, key=lambda x: x[1])

    for screen_player in screen_players_alpha:
        print(*screen_player)
        

#display_on_screen_players_tournament()
#register_players_tournament()