from models_chess import Tournament
from toolbox import open_list, write_list, generic_check, is_integer, no_special_char_word, EVENTS


def register_tournament():
    """saisie et enregistrement dans un fichier json list_tournament des tournois"""
    new_name_tournament = no_special_char_word(input("Nom du nouveau tournoi (suivi de l'année si annuel, du numero, si régulier): "))
    place = no_special_char_word(input("Adresse : "))
    start_date = input("Date de debut: ")
    end_date = input("Date de fin: ")
    number_of_rounds = generic_check("Nombre de rounds (par defaut : 4): ", is_integer, "Ce n'est pas un nombre entier, veuillez recommencer")
    director_comment = no_special_char_word(input("Commentaire du directeur: "))

    """création d'un tournoi"""
    tournament = Tournament(name_tournament=new_name_tournament, place=place, start_date=start_date, end_date=end_date, number_of_rounds=number_of_rounds, director_comment=director_comment)

    info_tournament={"Nom" : tournament.name, "Adresse" : tournament.place, "Date de debut": tournament.start_date, "Date de fin":tournament.end_date, "Nombre de rounds":tournament.number_of_rounds, "Commentaire du directeur":tournament.director_comment}

    try :
        list_tournaments = open_list(EVENTS)
       
    except:
        list_tournaments=[]

    list_tournaments.append(info_tournament)

    write_list(EVENTS, list_tournaments)

def display_on_screen_tournament_info():
    """Afficher à l'écran, par ordre alphabétique, la base des joueurs du club"""
    list_tournaments_screen = open_list(EVENTS)

    screen_tournaments1 = []
    for tournament_screen in list_tournaments_screen:
        tournament_screen1 = (
            tournament_screen["Nom"],
            tournament_screen["Adresse"],
            tournament_screen["Date de debut"],
            tournament_screen["Date de fin"],
            tournament_screen["Nombre de rounds"],
            tournament_screen["Commentaire du directeur"]
        )
        screen_tournaments1.append(tournament_screen1)
    screen_tournaments = []
    for tournament_screen in screen_tournaments1:
        screen_tournament = (
            tournament_screen[0],
            "\nLieu : ",
            tournament_screen[1],
            "\ndu ", tournament_screen[2],
            "au ", tournament_screen[3],
            "Nombre de rondes ", tournament_screen[4],
            "\nCommentaire du directeur ",tournament_screen[5],"\n"
        )
        screen_tournaments.append(screen_tournament)    

    print("Nombre de tournois enregistrés : ", len(screen_tournaments), "\n")

    for screen_tournament in screen_tournaments:
        print(*screen_tournament)