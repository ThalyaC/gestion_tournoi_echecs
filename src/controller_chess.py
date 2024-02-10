from vues.chessplayers import register_player, display_on_screen_players_club
from vues.registration_tournament import register_tournament
from vues.registration_chessplayers_tourmanent import register_players_tournament, display_on_screen_players_tournament
from vues.pairing import new_round, score_recording, display_on_screen_round
import sys
#from vues import chessplayers, registration_tournament, registration_chessplayers_tourmanent, pairing



def start_chess():
    print("\nQue souhaitez-vous faire? \nPour cela tapez le numéro corespondant à l'action")
    print("1.  Enregistrer un joueur dans la base de données du club.")
    print("2.  Afficher à l'écran la base de données des joueurs.")
    print("3.  Enregistrer un nouveau tournoi.")
    print("4.  Afficher à l'écran la liste des tournois.")
    print("5.  Afficher à l'écran les informations générales d'un tournoi.")
    print("6.  Enregistrer un joueur dans un tournoi.")
    print("7.  Afficher à l'écran la liste des joueurs d'un tournoi (par ordre alphabétique ou score)")
    print("8.  Lancer une ronde d'un tournoi.")
    print("9.  Enregistrer les scores des joueurs.")
    print("10. Afficher à l'écran une ronde d'un tournoi.")
    print("11. Afficher les informations générales d'une ronde.")
    print("Ou  toutes autres touches du clavier, si vous souhaiter quitter le programme.")
    choose_action = input("\nVotre choix : ")


    match choose_action:
        case "1":
            print("\nVous avez choisi d'enregistrer un joueur dans la base de données du club.\n")
            choice_action(register_player)
            
        case "2":
            print("\nVous avez choisi d'afficher à l'écran la base de données des joueurs.\n")
            choice_action(display_on_screen_players_club)
        case "3":
            print("\nVous avez choisi d\n")
            choice_action(register_tournament)
        case "4":
            #print("\nVous avez choisi d\n")
            pass
        case "5":
            #print("\nVous avez choisi d\n")
            pass
        case "6":
            print("\nVous avez choisi d\n")
            choice_action(register_players_tournament)
        case "7":
            print("\nVous avez choisi d\n")
            choice_action(display_on_screen_players_tournament)
        case "8":
            print("\nVous avez choisi d\n")
            choice_action(new_round)
        case "9":
            print("\nVous avez choisi d\n")
            choice_action(score_recording)
        case "10":
            print("\nVous avez choisi d\n")
            choice_action(display_on_screen_round)
        case "11":
            #print("\nVous avez choisi d\n")
            pass
        case _:
            print("\nMerci d'avoir utilisé ce programme. Keep on Chessing!\n")
            sys.exit(0)


def choice_action(action):
    action()
    return other_choice(action)

def other_choice(action):
    print("\nQue souhaitez-vous faire? Pour cela, tapez le numéro corespondant à l'action")
    print("1. Refaire la même action?")
    print("2. Revenir au menu")
    print("Ou  toutes autres touches du clavier, si vous souhaiter quitter le programme.")
    response = input("\nVotre choix : ")

    while response == "1" or "2":
        if response == "1":
            action()
            return other_choice(action)
        elif response == "2":
            return start_chess()
        else :
            print("Merci d'avoir utilisé ce programme. Keep on Chessing!")
            sys.exit(0)
    




start_chess()
#other_choice(chessplayers.register_player)

#/root/gestion_tournoi_echecs/src/models_chess.py
#display_on_screen_round()

#
#/root/gestion_tournoi_echecs/src/vues

"""
if choose_action =="1":
    register_player()

elif choose_action == "2":
    display_on_screen_players_club()


elif choose_action == "3":
    

elif choose_action == elif choose_action == elif choose_action == elif choose_action == elif choose_action == """