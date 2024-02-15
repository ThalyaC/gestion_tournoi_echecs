from models_chess import ChessPlayer
from toolbox import write_list, open_list, no_special_char_word, PLAYERS


def validate_format_ffe_number(ffe_number) -> str | None:
    """Vérifie le format du numéro de licence type : AB12345"""

    if (
        len(ffe_number) == 7
        and ffe_number[:2].isalpha()
        and ffe_number.isupper()
        and ffe_number[2 - 7 :].isdigit()
    ):
        print("Le numéro de licence est conforme.")
        return ffe_number

    else:
        print(
            "Le format du numéro de licence est invalide.\n Il doit être du type : AB12345"
        )
        return None


def check_old_number_ffe(list_chessplayers: list, ffe_number: str, txt):
    """Vérifie si le numéro FFE existe déjà dans la liste des joueurs"""
    try:
        liste_ffe_number = [element["Numero FFE"] for element in list_chessplayers]
        ffe_number1 = str(ffe_number)

        if ffe_number1 in liste_ffe_number:
            print("\nCe numéro a déjà été enregistré dans ", txt)
            return None

        else:
            print("Le numéro de licence va être enregistré.\n")
            return ffe_number1

    # Si le fichier n'existe pas encore
    except FileNotFoundError:
        print("Le numéro de licence va être enregistré.\n")
        return ffe_number1


def ffe_check(ffe_number, list_chessplayers: list, txt):
    """Valide le numéro FFE"""
    if validate_format_ffe_number(ffe_number):
        if check_old_number_ffe(list_chessplayers, ffe_number, txt):
            return ffe_number
        else:
            new_ffe_number = input(
                "\nNouveau numéro FFE (ou appuyer sur Entrée pour terminer) : "
            )
            if not new_ffe_number:
                print("")
            else:
                return ffe_check(new_ffe_number, list_chessplayers, txt)
    else:
        new_ffe_number = input(
            "\nNouveau numéro FFE (ou appuyer sur Entrée pour terminer) : "
        )
        if not new_ffe_number:
            print("")
        else:
            return ffe_check(new_ffe_number, list_chessplayers, txt)


def register_player():
    """Création d'un joueur d'échecs en vérifiant le numéro FFE"""
    list_chessplayers = open_list(PLAYERS)
    ffe_number1 = input("\nNuméro de licence (du type AB12345) : ")
    ffe_number = ffe_check(
        ffe_number1, list_chessplayers, txt="la base de données du club."
    )

    if ffe_number is None:
        return print("fin d'enregistrement.\n")

    else:
        new_name = no_special_char_word(input("Nom : "))
        new_first_name = no_special_char_word(input("Prénom : "))
        new_date_of_birth = input("Date de naissance : ")

        if 0<len(new_name) and 0<len(new_first_name) and 0<len(new_date_of_birth):
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
                "Parfait, {} {} vient d'être enregistré(e) dans la base de données du club.\n".format(
                    prenom, nom
                )
            )
        else :
            print("Au moins un des 3 champs est vide, ce joueur ne peut être enregitré")


def display_on_screen_players_club():
    """Afficher à l'écran, par ordre alphabétique, la base des joueurs du club"""
    try:
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

        print("Nombre de joueurs enregistrés : ", len(screen_players_alpha), "\n")

        for screen_player in screen_players_alpha:
            print(*screen_player)

    except FileNotFoundError:
        print("La liste des joueurs du club n'a pas été encore créée")
