# Gestion de tournoi d'échecs
Application exécutable hors ligne permettant de générer des tournois d'échecs, de sauvegarder les données et de les afficher.

Résultat attendu : L'application gère de A à Z la mise en place d'un tournoi d'échecs (liste des joueurs du club, inscription des joueurs à un tournoi, création des tournois, des rounds et des matches, enregistrement des scores, affichage en temps réél des demandes)

** Ce programme est une version béta. Il ne fonctionne pour le moment que dans un terminal.**

## Installation
### Prérequis
+ Python3
+ Pour les dépendances : consulter src/requirements.txt
+ Terminal
### Installation étape par étape
+	Sur GitHub :
1.	Aller sur https://github.com/ThalyaC/gestion_tournoi_echecs
2.	Cliquer sur le bouton « code » puis copier l’url du dépôt.

+	Ouvrir votre terminal :
1.	Aller vers le dossier où sera stocké le projet (commande « cd ») 
2.	Cloner le dépôt, pour cela :
commande `git clone` + url copiée  
Exemple : `git clone https://github.com/ThalyaC/gestion_tournoi_echecs.git`
3.	Accéder au dossier du programme (commande « cd ») 
4.	Mettre en place un environnement virtuel :  
    a. Pour installer votre environnement :
    Taper : `python3 -m venv env`  
    b. Pour l’activer : `source env/bin/activate`   
(pour le désactiver à la fin du processus, taper simplement : `deactivate`)
7.	Installer les dépendances listées dans le fichier requirements.txt  
`pip install -r requirements.txt`
## UTILISATION 
### POUR EXÉCUTER LE PROGRAMME
Saisir  `python3 src/lancement.py`
### RÉSULTAT ATTENDU
1.  Enregistrer un joueur dans la base de données du club.
2.  Afficher à l'écran la base de données des joueurs.
3.  Enregistrer un nouveau tournoi.
4.  Afficher à l'écran la liste des tournois avec leurs informations générales.
5.  Enregistrer un joueur dans un tournoi.
6.  Afficher à l'écran la liste des joueurs d'un tournoi (par ordre alphabétique ou score)
7.  Lancer une ronde d'un tournoi.
8.  Enregistrer les scores des joueurs.
9.  Afficher à l'écran une ronde d'un tournoi.  

Avec possibilité à chaque fois de:
+ Refaire la même action
+ Revenir au menu
+ Ou  toute autre touche du clavier, pour quitter le programme.
### POUR GÉNÉRER UN RAPPORT FLAKE 8
Dans le terminal, saisir `flake8 --format=html --htmldir=flake-report`
