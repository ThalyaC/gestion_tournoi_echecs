PATH = "/root/gestion_tournoi_echecs/"

import sys

sys.path.append(PATH)
from src.models_chess import ChessPlayer

"""
import os
parent_path = os.path.abspath("../gestion_tournoi_echecs/models_chess.py")"""
# from ..models_chess import ChessPlayer
from src.toolbox import write_list, open_list, no_special_char_word, PLAYERS


def validate_format_ffe_number(ffe_number: str) -> str | None:
    """Vérifie le format du numéro de licence type : AB12345"""

    if (
        len(ffe_number) == 7
        and ffe_number[:2].isalpha()
        and ffe_number.isupper()
        and ffe_number[2 - 7 :].isdigit()
    ):
        print("Le numéro de licence est valide.")
        return ffe_number

    else:
        print("Le format du numéro de licence est invalide, veuillez réessayer.")
        new_ffe_number = input("\nNuméro de licence (du type AB12345) à nouveau: ")
        return validate_format_ffe_number(new_ffe_number) if new_ffe_number else None


def check_old_number_ffe(list_chessplayers: list, ffe_number: str):
    """Vérifie si le numéro FFE existe déjà dans la liste des joueurs"""
    try:
        liste_ffe_number = [element["Numero FFE"] for element in list_chessplayers]
        print(sorted(liste_ffe_number))
        ffe_number1 = str(ffe_number)
        print(ffe_number1)

        if ffe_number1 in liste_ffe_number:
            while True:
                new_ffe_number = input(
                    "\nCe numéro a déjà été enregistré dans la base de données du club." 
                    "\nNouveau numéro FFE (ou appuyer sur Entrée pour terminer): "
                )

                if not new_ffe_number:
                    return None

                elif new_ffe_number not in liste_ffe_number:
                    new_ffe_number_last = validate_format_ffe_number(new_ffe_number)
                    if new_ffe_number_last:
                        ffe_number1 = new_ffe_number_last
                        print("Le numéro de licence va être enregistré.\n")
                        return ffe_number1

        else:
            print("Le numéro de licence va être enregistré.\n")
            return ffe_number1

    # Si le fichier n'existe pas encore
    except FileNotFoundError:
        print("Le numéro de licence va être enregistré.\n")
        return ffe_number1


def ffe_check(list_chessplayers: list):
    """Valide le numéro FFE"""
    ffe_number = input("\nNuméro de licence (du type AB12345) : ")
    resultat = check_old_number_ffe(
        list_chessplayers, validate_format_ffe_number(ffe_number)
    )
    return resultat


def register_player():
    """Création d'un joueur d'échecs en vérifiant le numéro FFE"""
    list_chessplayers = open_list(PLAYERS)
    ffe_number = ffe_check(list_chessplayers)

    if ffe_number is None:
        print("fin d'enregistrement.\n")

    else:
        new_name = no_special_char_word(input("Nom : "))
        new_first_name = no_special_char_word(input("Prénom : "))
        new_date_of_birth = input("Date de naissance : ")

        """création d'un joueur d'échecs"""
        chess_player = ChessPlayer(
            name=new_name,
            first_name=new_first_name,
            date_of_birth=new_date_of_birth,
            ffe_number=ffe_number,
        )

        info_chess_player = {
            "Nom": chess_player.name,
            "Prenom": chess_player.first_name,
            "Date de naissance": chess_player.date_of_birth,
            "Numero FFE": chess_player.ffe_number,
        }

        list_chessplayers.append(info_chess_player)

        write_list(PLAYERS, list_chessplayers)
        nom = info_chess_player["Nom"]
        prenom = info_chess_player["Prenom"]
        print(
            "Parfait, {} {} vient d'être enregistré(e) dans la base de données du club.\n"
            .format(
                prenom, nom
            )
        )


def display_on_screen_players_club():
    """Afficher à l'écran, par ordre alphabétique, la base des joueurs du club"""
    list_chessplayers_screen = open_list(PLAYERS)

    screen_players = []
    for chess_player_screen in list_chessplayers_screen:
        chess_player_screen1 = (
            chess_player_screen["Numero FFE"],
            chess_player_screen["Nom"],
            chess_player_screen["Prenom"],
            chess_player_screen["Date de naissance"],
        )
        screen_players.append(chess_player_screen1)

    screen_players_alpha = sorted(screen_players, key=lambda x: x[1])

    print("Nombre de joueurs enregistrés : ", len(screen_players_alpha))

    for screen_player in screen_players_alpha:
        print(*screen_player)


#register_player()
# display_on_screen_players_club()
