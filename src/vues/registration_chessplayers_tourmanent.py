PATH = "/root/gestion_tournoi_echecs/"

from os import mkdir
import sys

sys.path.append(PATH)
from src.models_chess import PlayerTournament
from src.toolbox import (
    seek_player_ffe,
    generic_check,
    is_integer,
    open_list,
    write_list,
    PLAYERS,
    EVENTS,
)
from chessplayers import register_player, ffe_check


def list_of_numbered_tournaments(list_tournaments:list):
    """Donner un numéro à un tournoi pour éviter à l'utilisateur de saisir le nom."""
    for i, nom_tournoi in enumerate(list_tournaments, start=1):
        print(f"{i}. {nom_tournoi}")


def create_file_folder_name(list_tournaments:list):
    """Créer le nom du dossier ou d'une partie du fichier
    lié au tournoi à partir d'un numéro."""
    list_of_numbered_tournaments(list_tournaments)
    choice_user = int(
        generic_check(
            "\nChoisissez le numéro qui correspond au tournoi souhaité : ",
            is_integer,
            "\nErreur de saisie. Seul un nombre entier est accepté. Veuillez recommencer.\n",
        )
    )

    try:
        choice_user is not None and 1 <= choice_user <= len(list_tournaments)
        name_tournament = list_tournaments[choice_user - 1]
        print("\nVous avez choisi le tournoi : ", name_tournament)
        name_tournament_file_folder = name_tournament.replace(" ", "_")
        return name_tournament, name_tournament_file_folder

    except IndexError:
        print(
            "\nErreur de saisie. Ce choix ne fait pas partie de la liste. Veuillez recommencer.\n"
        )
        return create_file_folder_name(list_tournaments)


def print_seek_player(seek_player:dict): ##
    "Affiche à l'écran le joueur à inscrire"
    print("\nPersonne à inscrire : ")
    for key, value in seek_player.items():
        print(key + " : " + value)
    print("\n")

        
def which_tournament():
    """Demande à l'utilisateur de choisir un tournoi"""
    
    list_tournaments = open_list(EVENTS)

    list_tournaments_name = [element["Nom"] for element in list_tournaments]
    name_tournament1, tournament_register1 = create_file_folder_name(
        list_tournaments_name
    )
    return name_tournament1, tournament_register1, list_tournaments


def number_rounds(list_tournaments, name_tournament1): ## pairing
    """Récupère les éléments nécessaires à la création d'une round"""
    name_tournament1, _, list_tournaments = which_tournament()
    
    for tournament in list_tournaments:
        """Donne le nombre de rounds contenus dans le tournoi demandé"""
        if "Nom" in tournament and tournament["Nom"] == name_tournament1:
            number_of_rounds = tournament.get("Nombre de rounds")
    return number_of_rounds


def registration_data_chessplayer_tournament(seek_player, list_players_tournament, file_tournament):
    """Enregistre et affiche les données d'un joueur dans un tournoi"""
    print_seek_player(seek_player)
    player_tournament1 = PlayerTournament(player_ffe=seek_player["Numero FFE"], score=0, former_adversaries=[]) 
    player_tournament = player_tournament1.info_playertournament()

    list_players_tournament.append(player_tournament)
    nom = seek_player["Nom"]
    prenom = seek_player["Prenom"]

    write_list(file_tournament, list_players_tournament)
    print("Parfait, {} {} vient d'être enregistré(e).\n".format(prenom, nom))


def folder_tournament_players(file_tournament, tournament_register1):
    """Ouvre ou crée un dossier d'un tournoi et une liste des participants"""
    try:
        list_players_tournament = open_list(file_tournament)
        return list_players_tournament
    except FileNotFoundError:
        list_players_tournament = []
        try:
            mkdir("chess_data/" + tournament_register1 + "/")
        except OSError:
            pass
        finally:
            pass
        return list_players_tournament


def register_players_tournament():
    """Inscrit un joueur dans un tournoi"""
        
    _, tournament_register1, _ = which_tournament()
    file_tournament = tournament_register1 + "/" + "players_" + tournament_register1
    list_players_tournament = folder_tournament_players(file_tournament, tournament_register1)
    ffe_number1 = input("\nNuméro de licence (du type AB12345) : ")
    ffe_number_register = ffe_check(ffe_number1, list_players_tournament,txt="ce tournoi")


    list_chessplayers = open_list(PLAYERS)

    seek_player = seek_player_ffe(list_chessplayers, ffe_number_register)

    if seek_player:
        registration_data_chessplayer_tournament(seek_player, list_players_tournament, file_tournament)

    else:
        print("\nCe joueur n'est pas enregistré dans la base du club.")
        response = input(
            "Souhaitez-vous l'enregistrer? (1 pour oui/N'importe quelle autre touche pour non) "
        )
        if response == "1":
            register_player()
            list_chessplayers = open_list(PLAYERS)
            seek_player = seek_player_ffe(list_chessplayers, ffe_number_register)
            registration_data_chessplayer_tournament(seek_player, list_players_tournament, file_tournament)

        else:
            print("Fin")


def condition_display(result):
    try:
        resultat = int(result)
        1 <= resultat <= 2
        return True
    except ValueError:
        return False
    

def user_request_to_display(screen_players):    
    result = generic_check("\nSouhaitez-vous afficher la liste par ordre alphabétique(1) ou de classement(2)? ", condition_display, "Erreur de saisie.")
    if result == "1":
        screen_players_alpha = sorted(screen_players, key=lambda x: x[1])
        return screen_players_alpha
    elif result == "2":
        screen_players_alpha = sorted(screen_players, key=lambda x: x[3], reverse=True)
        return screen_players_alpha
    else :
        print("2 choix possibles : 1 ou 2 \n")
        return user_request_to_display(screen_players)


def display_on_screen_players_tournament():
    """Afficher à l'écran, par ordre alphabétique ou de classement, la liste de joueurs inscrits à un tournoi."""
    list_tournaments = open_list(EVENTS)
    list_tournaments_nom = [element["Nom"] for element in list_tournaments]
    _, tournament_register1 = create_file_folder_name(list_tournaments_nom)
    tournament_register = tournament_register1 + "/" + "players_" + tournament_register1
    list_players_tournament = open_list(tournament_register)
    screen_players = []
    list_players_tournament_ffe = [
        element["Numero FFE"] for element in list_players_tournament
    ]
    list_chess_players = open_list(PLAYERS)

    for player_tournament_ffe1 in list_players_tournament_ffe:
        player_tournament_ffe2 = seek_player_ffe(
            list_players_tournament, player_tournament_ffe1
        )
        player_tournament_ffe = seek_player_ffe(
            list_chess_players, player_tournament_ffe1
        )
        screen_player1 = (
            player_tournament_ffe["Numero FFE"],
            player_tournament_ffe["Nom"],
            player_tournament_ffe["Prenom"],
            player_tournament_ffe2["score"],
        )
        screen_players.append(screen_player1)
    screen_players_alpha = user_request_to_display(screen_players)
    for screen_player in screen_players_alpha:
            print(*screen_player)
    

#display_on_screen_players_tournament()
#register_players_tournament()
