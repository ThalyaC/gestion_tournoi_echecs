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
    

def generic_check(data_requested, condition, error_message):
    while True:
        user_response = input(data_requested)
        if condition(user_response):
            return user_response
        else:
            print(error_message)


def is_integer(user_response):
    try:
        int(user_response)
        return True
    except ValueError:
        return False


# Les 2 fonctions ont été récupérées sur Foxxpy - Mathématiques et algorithmie, ai rajouté oe + @
def no_special_char(char):
    """Retire l'accent d'un caractère"""
    table_correspondance = {
                            192 : 65,
                            193 : 65,
                            194 : 65,
                            195 : 65,
                            196 : 65,
                            197 : 65,
                            198 : 65,
                            199 : 67,
                            200 : 69,
                            201 : 69,
                            202 : 69,
                            203 : 69,
                            204 : 73,
                            205 : 73,
                            206 : 73,
                            207 : 73,
                            208 : 68,
                            209 : 78,
                            210 : 79,
                            211 : 79,
                            212 : 79,
                            213 : 79,
                            214 : 79,
                            216 : 79,
                            217 : 85,
                            218 : 85,
                            219 : 85,
                            220 : 85,
                            221 : 89,
                            224 : 97,
                            225 : 97,
                            226 : 97,
                            227 : 97,
                            228 : 97,
                            229 : 97,
                            230 : 97,
                            231 : 99,
                            232 : 101,
                            233 : 101,
                            234 : 101,
                            235 : 101,
                            236 : 105,
                            237 : 105,
                            238 : 105,
                            239 : 105,
                            240 : 111,
                            241 : 110,
                            242 : 111,
                            243 : 111,
                            244 : 111,
                            245 : 111,
                            246 : 111,
                            248 : 111,
                            249 : 117,
                            250 : 117,
                            251 : 117,
                            252 : 117,
                            253 : 121  
    }

    if 339 == ord(char) :
        oe = chr(111) + chr(101)
        return oe
    elif 338 == ord(char):
        oe_maj = chr(79) + chr(101)
        return oe_maj
    elif 64 == ord(char) :
        at = "(at)"
        return at
    elif 192 <= ord(char) <= 214 or 216 <= ord(char) <= 253:
        return chr(table_correspondance[ord(char)])
    else:
        return char


def no_special_char_word(string):
    """Retire tous les accents d'un mot"""
    new_string = ""
    for char in string:
        new_string += no_special_char(char)

    return new_string

#print(no_special_char_word("L'Étourneau a chanté d'août à Noël @ Voix ambiguë d’un cœur qui, au zéphyr, préfÈre les jattes de kiwis"))
#test = no_special_char_word(input("test"))
#print (test)
