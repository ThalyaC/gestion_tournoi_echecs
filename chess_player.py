import json


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

        #ChessPlayer._player_data[self.player_id] = {"Nom" : self.name, "Prenom" : self.first_name, "Date de naissance": self.date_of_birth, "Numero FFE":self.ffe_number} #
        

# print(ChessPlayer.players_created)
  
def validate_format_ffe_number(ffe_number):
    """1. vérifie le format du numéro de licence type : AB12345"""
    
    if len(ffe_number) == 7 and ffe_number[:2].isalpha() and ffe_number.isupper() and ffe_number[2-7:].isdigit():
        print("Le numéro de licence est valide")
        return ffe_number
                    
    else :
        print("Le format du numéro de licence est invalide, veuillez réessayer")
        new_ffe_number = input("Numéro de licence (du type AB12345) à nouveau:")
        return validate_format_ffe_number(new_ffe_number) if new_ffe_number else None


def check_old_number_ffe(list_chessplayers, ffe_number):
    """2. vérifie si le numéro existe déjà dans la liste des joueurs"""
    try:
        liste_ffe_number=[element["Numero FFE"] for element in list_chessplayers]
        print(liste_ffe_number)
        ffe_number1= str(ffe_number)
        print(ffe_number1)
        
        if ffe_number1 in liste_ffe_number:
            while True:
                new_ffe_number = input("Ce numéro a déjà été enregistré. Nouveau numéro FFE (ou appuyer sur Entrée pour terminer):")
                        
                if not new_ffe_number:
                    print("Fin d'enregistrement")
                    return None
  
                else:
                    new_ffe_number_last=validate_format_ffe_number(new_ffe_number)
                    if new_ffe_number_last:
                        ffe_number1= new_ffe_number_last
                        #check_old_number_ffe(list_chessplayers, new_ffe_number)
                        break
            
        else:     
            print("Le numéro de licence va être enregistré")
        return ffe_number1
         
    except FileNotFoundError:
        print("1 Le numéro de licence va être enregistré")
        return ffe_number1
    

            
def ffe_check (list_chessplayers):
    ffe_number = input("Numéro de licence (du type AB12345) :")
    resultat=check_old_number_ffe(list_chessplayers, validate_format_ffe_number(ffe_number))
    #breakpoint()
    return resultat
    
def register_player():
    """Création d'un joueur d'échecs en vérifiant le numéro FFE"""         
    with open('chess_data/list_players1.json', 'r') as lp:
        list_chessplayers = json.load(lp)

    ffe_number= ffe_check(list_chessplayers)

    if ffe_number is None:
        print("fin d'enregistrement")
    
    else :
        new_name = input("Nom :")
        new_first_name = input("Prénom :")
        new_date_of_birth = input("Date de naissance :")

        """création d'un joueur d'échecs"""
        chess_player = ChessPlayer(name=new_name, first_name=new_first_name, date_of_birth=new_date_of_birth, ffe_number=ffe_number)

        info_chess_player={"Nom" : chess_player.name, "Prenom" : chess_player.first_name, "Date de naissance": chess_player.date_of_birth, "Numero FFE":chess_player.ffe_number}

        list_chessplayers.append(info_chess_player)

        with open('chess_data/list_players1.json', 'w', encoding='utf-8') as lp:
            if lp.tell() > 0:
                 lp.write(',')
            json.dump(list_chessplayers, lp, indent=4) 


register_player()