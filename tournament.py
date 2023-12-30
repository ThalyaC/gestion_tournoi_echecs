import json

class Tournament:
    "Tournoi"
    def __init__(self, name_tournament, place, start_date, end_date, director_comment, number_of_rounds=4):
        self.name = name_tournament
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.director_comment = director_comment
        self.rounds=[]
    
def register_tournament():
    "saisie et enregistrement dans un fichier json list_tournament des tournois"
    print("Veuillez ne pas noter les accents")
    new_name_tournament = input("Nom du nouveau tournoi (suivi de l'année si annuel, du numero, si régulier):")
    place = input("Adresse :")
    start_date = input("Date de debut:")
    end_date = input("Date de fin:")
    number_of_rounds = input("Nombre de rounds (par defaut : 4):")
    director_comment = input("Commentaire du directeur (si vide, noter RAS):")

    """création d'un tournoi"""
    tournament = Tournament(name_tournament=new_name_tournament, place=place, start_date=start_date, end_date=end_date, number_of_rounds=number_of_rounds, director_comment=director_comment)

    info_tournament={"Nom" : tournament.name, "Adresse" : tournament.place, "Date de debut": tournament.start_date, "Date de fin":tournament.end_date, "Nombre de rounds":tournament.number_of_rounds, "Commentaire du directeur":tournament.director_comment}

    try :
        with open('chess_data/list_tournaments.json', 'r') as lp:
            list_tournaments = json.load(lp)
       
    except:
        list_tournaments=[]

    list_tournaments.append(info_tournament)

    with open('chess_data/list_tournament.json', 'w', encoding='utf-8') as lp:
        if lp.tell() > 0:
            lp.write(',')
        json.dump(list_tournaments, lp, indent=4) 

#register_tournament()