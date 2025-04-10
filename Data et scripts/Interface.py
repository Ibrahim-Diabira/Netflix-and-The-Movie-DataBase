#PARTIE 2 projet python

from tkinter import *
from tkinter import ttk
import Data_frame as dat
import Fonctions as fun
import datetime

date_ajd = str(datetime.date.today())


#Import des dataframes
data_tmdb = dat.TMDB_clean()
data_netflix = dat.Netflix_clean()
df_avenir = dat.TMDB[dat.TMDB["release_date"] > date_ajd]

#Listes des selections pour listboxs
genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 
 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 
 'Mystery', 'Romance', 'Science fiction', 'Tv movie', 'Thriller', 
 'War', 'Western']
dates  = list(data_tmdb["release_date"].unique())
pays_prod = dat.prod_countries(data_tmdb)
duree = sorted(list(data_tmdb["runtime"].unique()))




#Trie les dates dans l'ordre décroissant
dates = sorted(dates,reverse=True)

#Listes pour sauvegarder les selections multiples
"""
#save_filtre : genres | dates
#save_perso : pays de production
"""
save_filtre = []
save_perso = []

#Variables pour sauvegarder les selections uniques
entree_age = None
duree = None



"""
                    ----------------------------------------
                              ******************
                    ****************************************
   FONCTIONS D'INTEGRATION DE L'INTERFACE AUX FONCTIONS DE RECOMMANDATIONS DU MODULE
  'Fonctions' / GESTION DES SAUVEGARDES DES INPUTS UTILISATEURS / GESTION DES AFFICHAGES ET DES INTERRACTIONS 
   UTILISATEUR :
                    ****************************************
                              ******************
                    ----------------------------------------
"""
#SAUVEGARDES DES SELECTIONS
def select_genre1():
    """
    Sauvegarde la selection genre pour la recherche par filtre simple
    """
    selection = filtre1.curselection()
    save_filtre.append(selection)
    return selection

def select_date1():
    """
    Sauvegarde la selection date pour la recherche par filtre simple
    """
    selection = filtre2.curselection()
    save_filtre.append(selection)
    
def select_genre2():
    """
    Sauvegarde la selection genre pour les suggestions 
    """
    selection = filtre_genre2.curselection()
    save_filtre.append(selection)
    
def select_date2():
    """
    Sauvegarde la selection date pour les suggestions 
    """
    selection = filtre_date2.curselection()
    save_filtre.append(selection)
    
def select_age():
    """
    Sauvegarde la selection date pour les suggestions 
    """
    global entree_age
    entree_age = filtre_age.get()
    
def select_prod():
    """
    Sauvegarde la selection pays de production pour les suggestions 
    """
    selection = filtre_prod.curselection()
    save_perso.append(selection)
    
def select_duree():
    """
    Sauvegarde la selection durée pour les suggestions 
    """
    global duree
    duree = filtre_duree.get()


    

    

def get_infos_filtre():
    
    """
    -----
    Fonction qui a partir des selections de filtres sauvegardées pour le genre et la date, 
    va retourner les informations principales des films filtrés par ordre croissant de note
    (et par plus grand nombre de votes si même note) : titre, synopsys, note, 
    année, langue originale, genre.
    -----
    """
    global save_filtre
    #si pas de selection pour genres, le resultat est vide
    if not save_filtre[0]:
        resu1 = None
    #sinon, on récupère les sauvegardes de genres (l'indice) et récupère les valeurs selectionnées
    else :
        save_filtre[0] = list(save_filtre[0])
        resu1 = [filtre1.get(save_filtre[0][i]) for i in range(len(save_filtre[0]))]
    #On réitère l'opération pour les dates
    if not save_filtre[1]:
        resu2 = None
    else : 
        save_filtre[1] = list(save_filtre[1])
        resu2 = [filtre2.get(save_filtre[1][i]) for i in range(len(save_filtre[1]))]
    
    #Appel des fonctions de filtres pour le genre et la date de manière séparée depuis le module 'Fonctions'
    tgenres = fun.df_filtre_genre(resu1)
    tgenres = fun.df_filtre_annee(tgenres,resu2)
    
    #nombre de suggestion 
    nb_suggest = tgenres.shape[0]
    print(resu1)
    print(resu2)
    #Affichage de chaque variable d'intérêts dans l'afficheur de texte
    resul =f"Nombres de résultats : {nb_suggest}\n"
    for i in range(tgenres.shape[0]): 
        titre = tgenres.iloc[i,1]
        annee = tgenres.iloc[i,5]
        syno = tgenres.iloc[i,15]
        langue = tgenres.iloc[i,13]
        note = tgenres.iloc[i,2]
        genre = tgenres.iloc[i,19]
        if str(syno) =="nan":
            syno = "Non disponible"
        resul+=f"Suggestion n°{i+1}\n"
        resul+=f"Titre : {titre} | Année : {annee}  |  Langue originale : {langue}  |  Genre : {genre}\n"
        resul+=f"Synopsis : {syno}\n"
        resul+=f"Note : {note}\n"
        resul +="\n\n"
    
    
    #Actualise la fenetre d'affichage texte
    resu.config(state="normal")
    resu.delete(1.0,END)
    resu.insert(END,resul)
    resu.config(state="disabled")
    
    #Vide la liste de sauvegarde GENRE/DATES pour une nouvelle recherche
    save_filtre = []


def suggestion_perso():
    """
    -------
    Fonction qui actualise l'affichage de l'onglet 'Suggestions personnalisées', en récupérant les inputs 
    utilisateurs depuis les sauvegardes. 
    
    ##Appel de fonctions tiers : 'infos_perso' | module 'Fontions''
    ##Appel de data frame : 'TMDB_net' | module 'Data_frame'
    ##Affiche : genre, synopsys, date, duree, note
    -------
    """
    #appel des souvegardes 
    global save_perso
    global save_filtre
    global entree_age
    global duree
    
    #######################################
    """
    Récupère les sauvegardes des inputs entré par l'utilisateur 
    """
    if not save_filtre[0]:
        resu_genre = None
    else :
        save_filtre[0] = save_filtre[0]
        resu_genre = [filtre_genre2.get(save_filtre[0][i]) for i in range(len(save_filtre[0]))]
    if not save_filtre[1]:
        resu_date = None
    else : 
        save_filtre[1] = save_filtre[1]
        resu_date = [filtre_date2.get(save_filtre[1][i]) for i in range(len(save_filtre[1]))]
    if not save_perso[0]:
        resu_pays = None
    else :
        save_perso[0] = save_perso[0]
        resu_pays = [filtre_prod.get(save_perso[0][i]) for i in range(len(save_perso[0]))]
    if duree is not None:
        resu_run = int(duree)
    else :
        resu_run = None
    if entree_age is not None:
        entree_age = str(entree_age).lower()
    else : 
        entree_age = None
    ########################################
    
    #Appel du la fonction de suggestion personalisée depuis le module 'Fonction'
    df = fun.infos_perso(resu_genre, resu_date, resu_pays, entree_age, resu_run)
    nb_suggest = df.shape[0]
    
    
    #Affichage de chaque variable d'intérêts dans l'afficheur de texte
    resul =f"Nombres de résultats : {nb_suggest}\n"
    for i in range(df.shape[0]): 
        duree = df.iloc[i,7]
        titre = df.iloc[i,1]
        annee = df.iloc[i,5]
        syno = df.iloc[i,15]
        langue = df.iloc[i,13]
        genre_commun = df.iloc[i,24]
        pays_commun = df.iloc[i,25]
        note = df.iloc[i,2]
        genre = df.iloc[i,19]
        if str(syno) =="nan":
            syno = "Non disponible"
        resul+=f"Suggestion n°{i+1}\n"
        resul+=f"Titre : {titre} | Année : {annee}  |  Langue originale : {langue}  |  Genre : {genre}  |  Durée : {duree}  minutes |\n"
        resul+=f"Synopsis : {syno}  |\n"
        resul+=f"Note : {note}\n"
        resul += f"Nombre de genres en commun : {genre_commun}  |  Nombre de pays commun : {pays_commun}\n"
        resul +="\n\n"
        
    
    #On actualise la fenetre d'affichage texte
    resu_perso.config(state="normal")
    resu_perso.delete(1.0,END)
    resu_perso.insert(END,resul)
    resu_perso.config(state="disabled")
    
    
    #Vide les sauvegardes GENRES/DATES PAYS DUREE AGE  pour une nouvelle recherche 
    save_perso=[]
    save_filtre=[]
    entree_age = None
    

#Liste des id saisis par l'utilisateur, qui sert dans la fonction reco_titres du module 'Fonction'
ID = []


def id_recup():
    """
    Fonction qui récupère les id saisis par l'utilisateur si doublons.
    Ajoute chaque id dans la liste ID
    **INPUT : liste ID global
    """
    global ID
    selection = id_choisi.get().split(", ")
    for s in selection:
        ID.append(s)
    #Affiche les id saisis dans le terminal
    print(ID)
    

def id_choix():
    """
    Fonction d'affichage des doublons et de leurs informations, notamment de leurs
    id pour que l'utilisateur puisse les récupérer manuellement pour une saisis 
    """
    #Récupère les titres saisis 
    selection = titre_search.get()
    selection = selection.split(", ")
    
    #Appel de la fonction reco_titre du module 'Fonctions'
    #On récupère la liste elem des doublons
    elem = fun.reco_titre(selection)[-1]
    
    #Appel du dataframe des doublons depuis la fonction reco_titre 
    df = fun.reco_titre(elem)
    #Dataframe des titres recherchés pour l'affichage et la récupération manuelle des id choisis par l'utilisateur
    df_titres = df[2]
    #Affichage des doublons dans le terminal
    print(elem)
    resul1 = "Verification des doublons... \n "
    #Si la liste des doublons n'est pas vide, on affiche les informations sur les doublons pour guider les choix
    if elem != [] : 
        resul1 += f"Vous avez ce(s) film(s) en doublon : {elem}  \n"
        for i in range(df_titres.shape[0]):
            
           
      
            iD = df_titres.iloc[i,0]
            duree1 = df_titres.iloc[i,7]
            titre1 = df_titres.iloc[i,1]
            annee1 = df_titres.iloc[i,5]
            syno1 = df_titres.iloc[i,15]
            langue1 = df_titres.iloc[i,13]
            note1 = df_titres.iloc[i,2]
            genre1 = df_titres.iloc[i,19]
            if str(syno1) =="nan":
                syno1 = "Non disponible"
            resul1+=f"Suggestion n°{i+1} \n"
            resul1+=f"ID : {iD} \n"
            resul1+=f"Titre : {titre1} | Année : {annee1}  |  Langue originale : {langue1}  |  Genre : {genre1}  |  Durée : {duree1}  minutes | \n"
            resul1+=f"Synopsis : {syno1}  | \n"
            resul1+=f"Note : {note1} \n"
            resul1 +="\n\n"
        resul1 += "Choisissez les ID que vous souhaitez dans la barre de recherche associée comme ceci : xxxxx, xxx, xx, puis valide à l'aide du bouton 'Valider ID'."
        #On actualise la fenetre d'affichage texte
        resu_titre1.config(state="normal")
        resu_titre1.delete(1.0,END)
        resu_titre1.insert(END,resul1)
        resu_titre1.config(state="disabled")
                
        
    #Si la liste des doublons est vide, on informe l'utilisateur qu'aucuns doublons n'est présent dans la saisis
    else : 
        resul1 = "Vous n'avez aucun doublons ! Vous pouvez afficher vos recommandations"
        resu_titre1.config(state="normal")
        resu_titre1.delete(1.0,END)
        resu_titre1.insert(END,resul1)
        resu_titre1.config(state="disabled")
        
                



def recherche_titre():
    """
    Fonction qui affiche les recommandations depuis les titres saisis, incluant une gestion des doublons 
    
    **INPUT : la liste ID des id choisis par l'utilisateur
    """
    global ID
    #On récupère la selection des titres saisis 
    selection = titre_search.get()
    selection = selection.split(", ")
    
    #On appel reco_titre en lui donnant les titres saisis, et les id correspondant aux titres choisis par l'utilisateurs dans le cas de présence des doublons
    df = fun.reco_titre(selection,ID)
    #Dataframe des titres recherchés pour l'affichage dans la partie 'Résultats'
    df_titres = df[2]
    
    """
    ------
    Affichage des titres selectionnés
    ------
    """
    
    ####################################################
    nb_suggest1 = len(selection)
    
            
  
    resul1 =f"Nombres de résultats : {nb_suggest1} \n"
    for i in range(df_titres.shape[0]): 
        iD = df_titres.iloc[i,0]
        duree1 = df_titres.iloc[i,7]
        titre1 = df_titres.iloc[i,1]
        annee1 = df_titres.iloc[i,5]
        syno1 = df_titres.iloc[i,15]
        langue1 = df_titres.iloc[i,13]
        note1 = df_titres.iloc[i,2]
        genre1 = df_titres.iloc[i,19]
        if str(syno1) =="nan":
            syno1 = "Non disponible"
        resul1+=f"Suggestion n°{i+1} \n"
        resul1+=f"ID : {iD} \n"
        resul1+=f"Titre : {titre1} | Année : {annee1}  |  Langue originale : {langue1}  |  Genre : {genre1}  |  Durée : {duree1}  minutes | \n"
        resul1+=f"Synopsis : {syno1}  | \n"
        resul1+=f"Note : {note1} \n"
        resul1 +="\n\n"
    
    #On actualise la fenetre d'affichage texte 'Résultats'
    resu_titre1.config(state="normal")
    resu_titre1.delete(1.0,END)
    resu_titre1.insert(END,resul1)
    resu_titre1.config(state="disabled")
    ######################################################
    
    #Selection du dataframe de recommandation correspondant
    df_reco = df[1]
    #Selection du dictionnaire de comparaison pour afficher les similitudes
    dico_comparaison = df[0]
    
    nb_suggest2 = df_reco.shape[0]
    
    resul2 =f"Nombres de résultats : {nb_suggest2} \n"
    for i in range(df_reco.shape[0]): 
        
        #récupération des similitudes
        titre2 = df_reco.iloc[i,1]
        for key in dico_comparaison:
            if titre2 in dico_comparaison[key]:
                 simili = key
        
        
        duree2 = df_reco.iloc[i,7]
        annee2 = df_reco.iloc[i,5]
        syno2 = df_reco.iloc[i,15]
        langue2 = df_reco.iloc[i,13]
        note2 = df_reco.iloc[i,2]
        genre2 = df_reco.iloc[i,19]
        if str(syno2) =="nan":
            syno2 = "Non disponible"
        resul2+=f"SIMILAIRE A {simili} : \n\n"
        resul2+=f"Suggestion n°{i+1} \n"
        resul2+=f"Titre : {titre2} | Année : {annee2}  |  Langue originale : {langue2}  |  Genre : {genre2}  |  Durée : {duree2}  minutes | \n"
        resul2+=f"Synopsis : {syno2}  |\n"
        resul2+=f"Note : {note2}\n"
        resul2 +="\n\n"
    
    #On actualise la fenetre d'affichage texte 'Recommandations'
    resu_titre2.config(state="normal")
    resu_titre2.delete(1.0,END)
    resu_titre2.insert(END,resul2)
    resu_titre2.config(state="disabled")
    
    
    ######################################################
    
    #Selection du dataframe netflix pour les disponibilités
    df_netflix = df[3]
    
    nb_suggest3 = df_netflix.shape[0]
    
    resul3 =f"Nombres de résultats : {nb_suggest3} \n"
    for i in range(df_netflix.shape[0]): 
        
        titre3 = df_netflix.iloc[i,2]
        
        
        duree3 = df_netflix.iloc[i,9]
        annee3 = df_netflix.iloc[i,7]
        syno3 = df_netflix.iloc[i,11]
        pays3 = df_netflix.iloc[i,5]
        note3 = df_netflix.iloc[i,8]
        genre3 = df_netflix.iloc[i,10]
        if str(syno3) =="nan":
            syno3 = "Non disponible"
        resul3+=f"Suggestion n°{i+1} \n"
        resul3+=f"Titre : {titre3} | Année : {annee3}  |  Pays de production : {pays3}  |  Genre : {genre3}  |  Durée : {duree3}  minutes | \n"
        resul3+=f"Synopsis : {syno3}  | \n"
        resul3+=f"Catégorie d'âge' : {note3} \n"
        resul3 +="\n\n"
    
    #On actualise la fenetre d'affichage texte 'Disponibles sur Netflix'
    resu_titre3.config(state="normal")
    resu_titre3.delete(1.0,END)
    resu_titre3.insert(END,resul3)
    resu_titre3.config(state="disabled")
    ID = []
    


def avenir_search():
    global df_avenir
    df_titres = df_avenir.copy()
    
    resul = "Films a venir prochainement : \n"
    for i in range(df_titres.shape[0]): 
        iD = df_titres.iloc[i,0]
     
        titre = df_titres.iloc[i,1]
        annee = df_titres.iloc[i,5]
        syno = df_titres.iloc[i,15]
        langue = df_titres.iloc[i,13]
        genre = df_titres.iloc[i,19]
        if str(syno) =="nan":
            syno = "Non disponible"
        resul+=f"Suggestion n°{i+1} \n"
        resul+=f"ID : {iD} \n"
        resul+=f"Titre : {titre} | Date de sortie : {annee}  |  Langue originale : {langue}  |  Genre : {genre}  | \n"
        resul+=f"Synopsis : {syno}  | \n"
        resul +="\n\n"
    
    #On actualise la fenetre d'affichage texte 'Résultats'
    resu_fvenir.config(state="normal")
    resu_fvenir.delete(1.0,END)
    resu_fvenir.insert(END,resul)
    resu_fvenir.config(state="disabled")
    





"""            **************************************
                          ***************
                 --------------------------------
                       INTERFACE Searchfilms
                 --------------------------------
                          ***************
              ****************************************
"""

#Initialisation de l'interface et de sa taille 
Searchfilms = Tk()
Searchfilms.geometry("1220x1080")

#Tab de controle pour les onglets
tab = ttk.Notebook(Searchfilms)

#Ajouter les onglets 
accueil = ttk.Frame(tab)
r_perso = ttk.Frame(tab)
r_filtre = ttk.Frame(tab)
r_saisie = ttk.Frame(tab)
avenir = ttk.Frame(tab)


#On nomme les onglets
tab.add(accueil,text="Accueil")
tab.add(r_perso,text="Suggestions personalisées")
tab.add(r_filtre,text="Recherche par filtres simples")
tab.add(r_saisie,text="Recommandations par titres ")
tab.add(avenir,text="Films à venir")
tab.pack(expand=1,fill="both")


"""
ONGLET D'ACCEUIL
"""

accueil_title = ttk.Label(accueil, text="Bienvenue sur le moteur de recherche Searchfilms",font=("Arial",14))
accueil_title.pack(pady=10)
accueil_label1 = ttk.Label(accueil,text="Vous pourrez ici obtenir toutes les informations nécéssaires sur un grand ensemble de films.",font=("Arial",14))
accueil_label1.pack()
accueil_label2 = ttk.Label(accueil,text="Vous pourrez effectuer des recherches par filtre : genres, popularité, langues originales, pays, et plus..",font=("Arial",14))
accueil_label2.pack()
accueil_label3=ttk.Label(accueil,text="Pour plus d'informations, veuillez consulter l'annexe du rapport fournis.",font=("Arial",14))
accueil_label3.pack()


"""
ONGLET DE SUGGESTIONS PERSONNALISEES
"""

#listbox genre
label_genre2 = Label(r_perso,text="Genres")
label_genre2.grid(row=0,column=0)

filtre_genre2 = Listbox(r_perso,selectmode = MULTIPLE)
for i in range(len(genres)):
    filtre_genre2.insert(END,genres[i])
filtre_genre2.grid(row=1,column=0,sticky="nsew",padx=10,pady=10)

button_genre2 = Button(r_perso,text="Valider genre(s)",command=select_genre2)
button_genre2.grid(row=2,column=0,sticky="nsew")




#listbox prod

label_prod = Label(r_perso,text="Pays de production")
label_prod.grid(row=0,column=1)

filtre_prod = Listbox(r_perso,selectmode=MULTIPLE)
for i in range(len(pays_prod)):
    filtre_prod.insert(END,pays_prod[i])
filtre_prod.grid(row=1,column=1,sticky="nsew",padx=10,pady=10)

button_prod = Button(r_perso,text="Valider pays",command=select_prod)
button_prod.grid(row=2,column=1,sticky="nsew")

#listbox date
label_date2 = Label(r_perso,text="Date(s) (année(s))")
label_date2.grid(row=0,column=2)

filtre_date2 = Listbox(r_perso,selectmode=MULTIPLE)
for i in range(len(dates)):
    filtre_date2.insert(END,dates[i])
filtre_date2.grid(row=1,column=2,padx=10,pady=10)

button_date2 = Button(r_perso,text="Valider date(s)",command=select_date2)
button_date2.grid(row=2,column=2,sticky="nsew")

#listbox duree
label_duree = Label(r_perso,text="Durées (minutes)")
label_duree.grid(row=0,column=3)


filtre_duree = Entry(r_perso)

filtre_duree.grid(row=1,column=3,padx=10,pady=10)

button_duree = Button(r_perso,text="Valider durée",command=select_duree)
button_duree.grid(row=2,column=3,sticky="nsew")


#input age
label_age = Label(r_perso,text="Voulez-vous inclure les catégories adultes (oui/non)")
label_age.grid(row=0,column=4)

filtre_age = Entry(r_perso)
filtre_age.grid(row=1,column=4,padx=3,pady=3)

button_age = Button(r_perso,text="Valider",command=select_age)
button_age.grid(row=2,column=4,sticky="nsew")

#validation avec appel de la fonction suggestion_perso
button_valid = Button(r_perso,text="Afficher",command=suggestion_perso)
button_valid.grid(row=2,column=5,padx=10,pady=10,sticky="nsew")

#Affichage

resu_perso = Text(r_perso, height=20, width=60, state="disabled",wrap="word")
resu_perso.grid(row=7, column=0, columnspan=2, padx=50, pady=50,sticky="nw")




"""
RECHERCHE PAR FILTRES SIMPLES
"""

filtre_title1 = Label(r_filtre,text="Genres")
filtre_title1.grid(row=0,column=0)
filtre_title2 = Label(r_filtre,text="Dates (Années)")
filtre_title2.grid(row=0,column=1)

#MULTIPLE permet de selectionner plusieurs items à la fois
#Listbox genres
filtre1 = Listbox(r_filtre,selectmode=MULTIPLE)  
for i in range(len(genres)):
    filtre1.insert(END,genres[i])
filtre1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

#Bouton de sauvegarde genres et appel de la fonction select_genre1 pour la sauvegarde
bf1 = Button(r_filtre,text="Valider genres",command=select_genre1)  
bf1.grid(row=5,column=0)

#Listbox dates
filtre2 = Listbox(r_filtre,selectmode=MULTIPLE)
for i in range(len(dates)):
    filtre2.insert(END,dates[i])
filtre2.grid(row=1,column=1,padx=10,pady=10,sticky="nsew")

#Bouton de sauvegarde dates et appel de la fonction select_date1 pour la sauvegarde
bf2 = Button(r_filtre,text="Valider date",command=select_date1)
bf2.grid(row=5,column=1)

#Bouton d'affichage et appel de la fonction get_infos_filtre
button = Button(r_filtre,text="Afficher",command=get_infos_filtre)  #Boutton pour valider les entrer et obtenir l'affichage
button.grid(row=1,column=10,sticky="nsew")

#Affichage
resu = Text(r_filtre, height=20, width=60, state="disabled",wrap="word")  #Affichage : wrap="word" permet de passer à la ligne à la fin d'un mot
resu.grid(row=7, column=0, columnspan=2, padx=50, pady=50,sticky="sw")



"""
RECHERCHE PAR TITRE ET RECOMMANDATION
"""
 


titre_label = Label(r_saisie,text="Veuillez saisir des noms de films (10 maximum)")
titre_label.grid(row=0,column = 0,padx=10,pady=10,sticky="nsew")

#Saisis des titres 
titre_search = Entry(r_saisie)
titre_search.grid(row=1,column=0,padx=1,pady=1,sticky="nsew")

#Buton de vérification de l'id et appeld de la fonction id_choix pour remplir l'affichage des doublons dans 'Résultats'
button_verifid = Button(r_saisie, text="Vérifiez doublon(s)",command=id_choix)
button_verifid.grid(row=2,column = 2)

#Buton pour afficher les résultats dans les 3 cellules d'affichages et appel de la fonction recherche_titre
button_titre = Button(r_saisie,text="Valider la saisie et afficher",command=recherche_titre)
button_titre.grid(row=2,column=0,padx=10,pady=10,sticky="nsew")


id_titre = Label(r_saisie,text="Entrez le(s) ID d'un des films doublons")
id_titre.grid(row=0,column=10)
#Saisis des id si doublons
id_choisi=Entry(r_saisie)
id_choisi.grid(row=1,column=10)

#Buton de validation des id saisis qui les enregistre avec l'appel de la fonction id_recup
button_id = Button(r_saisie,text="Valider ID",command = id_recup)
button_id.grid(row=2,column=10)

#Affichage 'Résultats'
resu_label1 = Label(r_saisie,text="Resultats")
resu_label1.grid(row=3,column=0)
resu_titre1 = Text(r_saisie, height=20, width=40, state="disabled",wrap="word")
resu_titre1.grid(row=4,column=0,sticky="nsew")

#Affichage 'Films similaires'
resu_label1 = Label(r_saisie,text="Films similaires")
resu_label1.grid(row=3,column=5)
resu_titre2 = Text(r_saisie, height=20, width=40, state="disabled",wrap="word")
resu_titre2.grid(row=4,column=5,sticky="se")

#Affichage 'Disponibles sur Netflix'
resu_label1 = Label(r_saisie,text="Disponibles sur Netflix")
resu_label1.grid(row=3,column=10)
resu_titre3 = Text(r_saisie, height=20, width=40, state="disabled",wrap="word")
resu_titre3.grid(row=4,column=10,sticky="se")

"""
FILMS A VENIR
"""

fvenir = Label(avenir, text="Retrouvez ici tous vos films à venir")
fvenir.grid(row=0,column=0,sticky="nsew")

resu_fvenir = Text(avenir,height=50, width=50, state="disabled",wrap="word")
resu_fvenir.grid(row=4,column=0,sticky="nsew")

buton_avenir = Button(avenir, text="Afficher",command=avenir_search)
buton_avenir.grid(row=4,column =4)


Searchfilms.mainloop()



