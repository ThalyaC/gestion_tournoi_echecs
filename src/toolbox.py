import json
import sys

PLAYERS = "list_players1"
EVENTS = "list_tournaments"
def seek_player_ffe(list_chessplayers,ffe_number_register):
    """Trouver un joueur à partir de son numéro FFE"""
    for player in list_chessplayers:
        if player.get("Numero FFE")==ffe_number_register:
            return player
    return None


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


def what_else(result):
    "Vérifie que l'opération est possible"
    if result == None:
        print("Fin")
        sys.exit(0)
    else :
        pass


def does_list_exist(result):
    "Vérifie que la liste existe ou en crée une vide"
    if result == None:
        wanted_list =[]
    else :
        wanted_list = result
    return wanted_list


def not_in_list(ma_liste,black):
    "vérifie qu'un élément n'est pas dans la liste"
    x = 0
    
    while x < len(ma_liste):
        if  any(ffe==black for ffe in ma_liste):
            #print(f"Le joueur {black} a déjà joué avec ce joueur")
            return None
        
        elif not any(ffe==black for ffe in ma_liste):
            black_player=black
            #print("Le joueur noir est:", black_player)
            return black_player
        
        else :
            x += 1


