from vues.chessplayers import register_player, display_on_screen_players_club
from vues.registration_tournament import register_tournament, display_on_screen_tournament_info
from vues.registration_chessplayers_tourmanent import register_players_tournament, display_on_screen_players_tournament
from vues.pairing import new_round
from vues.display_round import display_on_screen_round
from vues.scoring_matches import score_recording
import sys


def start_chess():
    print("\nQue souhaitez-vous faire? \nPour cela, tapez le numéro correspondant à l'action")
    print("1.  Enregistrer un joueur dans la base de données du club.")
    print("2.  Afficher à l'écran la base de données des joueurs.")
    print("3.  Enregistrer un nouveau tournoi.")
    print("4.  Afficher à l'écran la liste des tournois avec leurs informations générales.")
    print("5.  Enregistrer un joueur dans un tournoi.")
    print("6.  Afficher à l'écran la liste des joueurs d'un tournoi (par ordre alphabétique ou score)")
    print("7.  Lancer une ronde d'un tournoi.")
    print("8.  Enregistrer les scores des joueurs.")
    print("9.  Afficher à l'écran une ronde d'un tournoi.")
    print("Ou  toute autre touche du clavier, si vous souhaitez quitter le programme.")
    choose_action = input("\nVotre choix : ")

    match choose_action:
        case "1":
            print(
                "\nVous avez choisi d'enregistrer un joueur dans la base de données du club.\n")
            choice_action(register_player)

        case "2":
            print(
                "\nVous avez choisi d'afficher à l'écran la base de données des joueurs.\n")
            choice_action(display_on_screen_players_club)
        case "3":
            print("\nVous avez choisi d'enregistrer un nouveau tournoi.\n")
            choice_action(register_tournament)
        case "4":
            print("\nVous avez choisi d'afficher à l'écran la liste des tournois avec leurs informations générales.\n")
            choice_action(display_on_screen_tournament_info)
        case "5":
            print("\nVous avez choisi d'enregistrer un joueur dans un tournoi\n")
            choice_action(register_players_tournament)
        case "6":
            print("""\nVous avez choisi d'afficher à l'écran la liste des joueurs
                  d'un tournoi (par ordre alphabétique ou score)\n""")
            choice_action(display_on_screen_players_tournament)
        case "7":
            print("\nVous avez choisi de lancer une ronde d'un tournoi\n")
            choice_action(new_round)
        case "8":
            print("\nVous avez choisi d'enregistrer les scores des joueurs.\n")
            choice_action(score_recording)
        case "9":
            print("\nVous avez choisi d'afficher à l'écran une ronde d'un tournoi.\n")
            choice_action(display_on_screen_round)
        case _:
            print("\nMerci d'avoir utilisé ce programme. Keep on Chessing!\n")
            sys.exit(0)


def choice_action(action):
    action()
    return other_choice(action)


def other_choice(action):
    print("\nQue souhaitez-vous faire? Pour cela, tapez le numéro corespondant à l'action")
    print("1. Refaire la même action")
    print("2. Revenir au menu")
    print("Ou  toute autre touche du clavier, si vous souhaitez quitter le programme.")
    response = input("\nVotre choix : ")

    while response == "1" or "2":
        if response == "1":
            action()
            return other_choice(action)
        elif response == "2":
            return start_chess()
        else:
            print("Merci d'avoir utilisé ce programme. Keep on Chessing!\n")
            sys.exit(0)
