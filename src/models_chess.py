from toolbox import open_list


class ChessPlayer:
    """un joueur d'échecs"""

    def __init__(self, name, first_name, date_of_birth, ffe_number):
        """
        Identité du joueur (ffe, nom, prénom, date de naissance).
        ffe_number :
        numéro de licence de la Fédération Française des Echecs
        """
        self.ffe_number = ffe_number
        self.name = name
        self.first_name = first_name
        self.date_of_birth = date_of_birth


class Tournament:
    "Tournoi"

    def __init__(
        self,
        name_tournament,
        place,
        start_date,
        end_date,
        director_comment,
        number_of_rounds=4,
    ):
        self.name = name_tournament
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.director_comment = director_comment
        self.rounds = []


class PlayerTournament:
    def __init__(self, player_ffe, score, former_adversaries):
        self.player_ffe = player_ffe
        self.score = score
        self.former_adversaries = former_adversaries

    def info_playertournament(self):
        return {
            "Numero FFE": self.player_ffe,
            "score": self.score,
            "Anciens adversaires": self.former_adversaries,
        }

    def register_former_adversaries(self, adversary):
        self.former_adversaries.append(adversary)


class Round:
    "création d'un round"

    def __init__(
        self,
        name_tournament,
        number_round,
        current_round,
        start_date_round,
        end_date_round,
        start_hour,
        end_hour,
        list_matches,
        number_tables,
        status,
    ):
        self.name_tournament = name_tournament
        self.number_round = number_round
        self.current_round = current_round  # format "a/b"
        self.start_date_round = start_date_round
        self.end_date_round = end_date_round
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.list_matches = list_matches
        self.number_tables = number_tables
        self.status = status

    def round_info(self):
        return {
            "Round": self.number_round,
            "Etat": self.status,
            "Date de lancement": self.start_date_round,
            "Heure de lancement": self.start_hour,
            "Round finie le": self.end_date_round,
            "Heure de fin": self.end_hour,
            "Nombre de tables en cours de jeu": self.number_tables,
            "Liste des appariements": self.list_matches,
        }

    @classmethod
    def read_info_round(cls, path_tourmanent_rounds_file):
        list_data_round = open_list(path_tourmanent_rounds_file)
        list_data_round.pop(0)

        if isinstance(list_data_round, list):
            rounds = []
            for round_data in list_data_round:
                round = cls(
                    name_tournament=round_data.get("Nom du tournoi", None),
                    current_round=round_data.get("Round", None),
                    number_round=round_data.get("Round"),
                    status=round_data.get("Etat"),
                    start_date_round=round_data.get("Date de lancement"),
                    start_hour=round_data.get("Heure de lancement"),
                    end_date_round=round_data.get("Round finie le"),
                    end_hour=round_data.get("Heure de fin"),
                    number_tables=round_data.get("Nombre de tables en cours de jeu"),
                    list_matches=round_data.get("Liste des appariements"),
                )
                rounds.append(round)
            return rounds
        else:
            return cls(
                name_tournament=round_data.get("Nom du tournoi", None),
                current_round=round_data.get("Round", None),
                number_round=round_data.get("Round"),
                status=round_data.get("Etat"),
                start_date_round=round_data.get("Date de lancement"),
                start_hour=round_data.get("Heure de lancement"),
                end_date_round=round_data.get("Round finie le"),
                end_hour=round_data.get("Heure de fin"),
                number_tables=round_data.get("Nombre de tables en cours de jeu"),
                list_matches=round_data.get("Liste des appariements"),
            )


class Match(Round):
    def __init__(self, table, white, black, score_players):
        self.white = white
        self.black = black
        self.score_player1_2 = score_players
        self.table = table

    def info_match(self):
        return {
            "Table": self.table,
            "Blanc": self.white,
            "Noir": self.black,
            "score": self.score_player1_2,
        }
