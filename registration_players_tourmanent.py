import json
from os import mkdir
from chess_player import register_player


class PlayerTournament(): ##
    def __init__(self, player_ffe, score, former_adversaries):
        self.player_ffe = player_ffe
        self.score = score
        self.former_adversaries = former_adversaries

    def info_playertournament(self):
        return {"Numero FFE": self.player_ffe, "score":self.score, "Anciens adversaires":self.former_adversaries}
    
    def register_former_adversaries(self, adversary):
        self.former_adversaries.append(adversary)


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

def open_list(name_file):
    'Transforme un fichier json en liste'
    with open('chess_data/'+name_file+'.json', 'r') as lp:
        list_what_you_want = json.load(lp)
    return list_what_you_want

def write_list(name_file, list_name):
    "enregistre la liste dans un fichier json"
    with open('chess_data/'+name_file+'.json','w', encoding='utf-8') as lp:
            if lp.tell() > 0:
                lp.write(',')
            json.dump(list_name, lp, indent=4)

def register_ffe():
    "1ère partie de register_players_tournament pour éviter de saisir 3 fois le numéro FFE si pas encore enregistré"
    ffe_number_register = input("Numéro de licence (du type AB12345) tournoi:")
    return ffe_number_register

def register_players_tournament1(ffe_number_register):
    "2ème partie de register_players_tournament"
    list_chessplayers = open_list_chessplayers()
    list_tournaments = open_list_tournaments()
    
    list_tournaments_nom = [element["Nom"] for element in list_tournaments]
    
    seek_player = seek_player_ffe(list_chessplayers,ffe_number_register)

    if seek_player:
        print("personne à inscrire :", seek_player)
        _, tournament_register1 = create_file_folder_name(list_tournaments_nom)
        file_tournament = tournament_register1+'/'+'players_'+tournament_register1
        try :
            list_players_tournament = open_list(file_tournament)            
            
            # Si un joueur est déjà inscrit à ce tournoi
            seek_player_old = seek_player_ffe(list_players_tournament, ffe_number_register)
            if seek_player_old :           
                print("Ce joueur est déjà enregistré dans ce tournoi")
                return None            
        except:
            list_players_tournament=[]
            try:
                mkdir('chess_data/'+tournament_register1+'/')
            except OSError :
                pass
            finally :
                pass

        player_tournament1 = PlayerTournament(player_ffe=seek_player['Numero FFE'], score=0, former_adversaries=[]) ##
        player_tournament = player_tournament1.info_playertournament()

        list_players_tournament.append(player_tournament)

        write_list(file_tournament, list_players_tournament)

    else:         
        print("Ce joueur n'est pas enregistré dans la base du club.")
        response = input("Souhaitez-vous l'enregistrer? (Y pour oui/N pour non)")
        if response == "Y":
            register_player()
            register_players_tournament1(ffe_number_register)
        else :
            return print("Fin")


def register_players_tournament():
    """Objectif : inscrire un joueur à un tournoi.
    
    - Vérifie si le joueur est déjà inscrit au tournoi - si oui fin de la procédure;
    - sinon à partir du numéro FFE, le joueur est recherché dans la liste générale du club;
        - si non enregistré : inscription du joueur dans le fichier général;
        - inscription dans le tournoi choisi :
            - Demande à l'utilisateur de sélectionner par le biais d'un numéro le tournoi souhaité;
            - crée si nécessaire le dossier du tournoi et le fichier recevant les joueurs inscrits 
            pour ce tournoi;
            - enregistre le numéro FFE du joueur dans le fichier.
            - Ajoute un score =0 et une liste des anciens joueurs pour éviter des appariements identiques
    """
    ffe_number_register = register_ffe()
    register_players_tournament1(ffe_number_register)


def display_on_screen_players_tournament():
    
    """Afficher à l'écran, par ordre alphabétique ou de classement, la liste de joueurs inscrits à un tournoi"""
    list_tournaments = open_list_tournaments()
    list_tournaments_nom = [element["Nom"] for element in list_tournaments]
    _, tournament_register1 = create_file_folder_name(list_tournaments_nom)
    tournament_register = tournament_register1+'/'+'players_'+tournament_register1
    list_players_tournament= open_list(tournament_register)
    screen_players = []
    list_players_tournament_ffe = [element['Numero FFE'] for element in list_players_tournament]
    list_chess_players = open_list_chessplayers()
    
    for player_tournament_ffe1 in list_players_tournament_ffe:
        player_tournament_ffe2 = seek_player_ffe(list_players_tournament, player_tournament_ffe1)
        player_tournament_ffe = seek_player_ffe(list_chess_players, player_tournament_ffe1)
        screen_player1 = (player_tournament_ffe["Numero FFE"], player_tournament_ffe["Nom"], player_tournament_ffe["Prenom"], player_tournament_ffe2['score'])
        screen_players.append(screen_player1)
    
    result = input('Souhaitez-vous afficher la liste par ordre alphabétique(1) ou de classement(2)?')
    if result == "1":
        screen_players_alpha = sorted(screen_players, key=lambda x: x[1])
    elif result == "2":
        screen_players_alpha = sorted(screen_players, key=lambda x: x[3], reverse=True)

    for screen_player in screen_players_alpha:
        print(*screen_player)
        

#display_on_screen_players_tournament()
#register_players_tournament()
