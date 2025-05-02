
import Data_frame as dat
import pandas as pd
import numpy as np

data_tmdb = dat.TMDB_clean()
data_netflix = dat.Netflix_clean()
"""
*********************************************************************************

Ce module forunis les fonctions de filtres, de suggestions et de recommandation.
Ce sont les premières versions des fonctions, où l'on utilise des input pour
l'interaction avec l'utilisateur. 
Vous pourrez retrouver ces fonctions adaptés pour l'utilisation de l'interface
dans le module 'Fonctions.py'


*********************************************************************************
"""


""" 
Fonctions du point 1 

""" 

#Filtre par genre
def df_filtre_genre():
    genres_ent = input("Entrez vos genres favoris séparés par des virgules")
    genres_liste = [genre for genre in genres_ent.split(",") if genre] #On utilise les listes en compréhension pour créer une liste
    #à partir des genres entrés par l'utilisateur. 
    
    #Pour éviter le problème des espaces dans la saisie de l'utilisateur (par exemple après les virgules)
    #On fait une boucle pour parcourir les élements de la liste et on applique la méthode strip() pour éliminer les espaces 
    genres_liste = [genre.strip() for genre in genres_liste]
    
    if genres_liste: #Si la liste des genres n'est pas vide
        df = data_tmdb.copy() 
        for genre in genres_liste:
            df = df[df["genres"].str.contains(genre, case=False)] 
            #On parcours la liste des genres puis on filtre la dataframe pour ne garder que les films qui ont pour genre le genre entré par l'utilisateur
        
        df = df.sort_values(by=["vote_average", "popularity"], ascending=False) #On trie la dataframe d'abord par la note
        # puis par la popularité si même note, par ordre décroissant
        return df["title"]
    else: #dans le cas où l'utilisateur n'entre pas de genre 
        df = data_tmdb.sort_values(by=["vote_average", "popularity"], ascending=False)
        return df




#Filtre par annee
def df_filtre_annee(): 
    global data_tmdb
    year_ent = input("Entrez l'année de sortie du film que vous souhaitez :") #Entrée de l'utilisateur
    
    if year_ent is not None: #si l'utilisateur a bien entré une valeur
        df=data_tmdb.copy() 
        df = df[df["release_date"].str.contains(year_ent)]  #On regarde la colonne release date et on ne garde les films que de l'année entré par l'utilisateur
        return df
    else : 
        return df 




""" 
Le but de la fonction est de retourner une DataFrame contenant les 5 films les plus susceptibles d'être appréciés par l'utilisateur,
selon les infos qu'il renseigne. 
La fonction prend 5 arguments : 
    genre_ent : le/les genres entrés par l'utilisateur
    annee_ent : le/les années entrés par l'utilisateur
    pays_ent : le/les pays entrés par l'utilisateur
    adult_ent : Une variable indicatrice pour savoir si l'utilisateur veut inclure ou non les films pour adulte
    runtime_ent : La durée de film souhaitée par l'utilisateur

    
""" 
def infos_perso():
    global data_tmdb  
    df = data_tmdb.copy()  

    genres_ent = input("Entrez vos genres favoris : ").lower()
    annee_ent = input("Entrez l'année que vous souhaitez : ").lower()
    pays_ent = input("Entrez les pays de production que vous souhaitez : ").lower()
    adult_ent = input("Voulez-vous inclure les films pour adulte ? (répondez par oui ou non) : ").lower()
    runtime_ent = input("Entrez la durée du film que vous souhaitez (en minutes) : ")
    
    #On met les entrées de l'utilisateur en minuscule afin d'éviter la sensibilité à la casse.
    #En d'autres termes l'utilisateur pourra entrer les valeurs avec ou sans majuscule le résultat sera le même
    
    #On utilise les listes en compréhension pour créer des listes à partir des genres et pays entrés par l'utilisateur
    genres_liste = [genre for genre in genres_ent.split(",")]  
    pays_liste = [pays for pays in pays_ent.split(",")] 
    
    
    #Comme dans les fonctions de la première partie on élimine les espaces grâce à la méthode strip()
    for genre in genres_liste:
        genre = genre.strip()
    
    for pays in pays_liste : 
        pays = pays.strip()
    

    #On crée deux fonctions qui nous permettront de compter le nombre de genres/pays en commun entre les entrées de l'utilisateur
    #et les films du dataframe (cela nous permettra de faire un classement ensuite)
    def compteur_genres(film_genres):
        compteur = 0 #on initialise le compteur à 0 
        for genre in genres_liste: #On parcourt la liste des genres 
            if genre in str(film_genres).lower(): #Si le genre en question est contenue dans les genre du film de la ligne du DF
            #On utilise la méthode lower() comme nous l'avions fait sur l'entrée de l'utilisateur
                compteur += 1 #le compteur augmente de 1
        return compteur
    
    #Même chose pour le pays
    def compteur_pays(film_pays):
        compteur = 0
        for pays in pays_liste:
            if pays in str(film_pays).lower():
                compteur += 1
        return compteur
    
    if genres_liste: #Si l'utilisateur a entré des genres (cf si la liste n'est pas vide)
        df["memes_genres"] = df["genres"].apply(compteur_genres) #on crée une nouvelle colonne "même genres"
        #on applique la fonction crée ci dessus à chaque ligne de la colonne genres et on stocke le résultat dans la colonne crée
    else:
        df = df #Si l'utilisateur n'a pas entré de genres on ne fait rien

    
    if pays_liste: #Si l'utilisateur a entré des pays
        df["memes_pays"] = df["production_countries"].apply(compteur_pays)
        #On applique la fonction à la colonne "production_countries"
    else : 
        df = df 
  
    
    if annee_ent is not None: #Si l'utilisateur a entré une année
        df = df[df["release_date"] == annee_ent] #on filtre la DF pour ne garder que les films de l'année demandée par l'utilisateur
    else : 
        df = df
    
    
    #Variable binaire adult
    if adult_ent == "non":
        df = df[df["adult"] == 0] #Si l'utilisateur ne souhaite pas les films pour adulte
        # On filtre la DF pour ne garder que les films qui ont 0 dans la colonne adult. 
    elif adult_ent == "oui":
        df = df
        #Si l'utilisateur veut inclure les films adulte : pas nécéssaire de filtrer.
        #On retourne la DF complète
    
    if runtime_ent.isdigit():
        runtime_ent = int(runtime_ent)
    else: 
        runtime_ent = None
   
    if runtime_ent is not None:
        df = df[(df["runtime"] >= runtime_ent - 30) & (df["runtime"] <= runtime_ent + 30)]
    #Si l'utilisateur a bien entré une valeur pour la durée du film, on a choisi de filtrer la DF
    #afin de garder les films dans un intervalle de 30min
    
    #Trie du dataframe
    df_sorted = df.sort_values(
        by=["memes_genres", "memes_pays", "release_date", "vote_average", "popularity"],
        ascending=[False, False, False, False, False]
    )
    
    #On crée la dataframe contenant les 5 meilleurs recommandations
    df_top_5 = df_sorted.head(5)["title"]
    
    return df_top_5


#Commentaires plus détaillés dans le module Fonctions.py

#Recommandation par mots_clefs
def reco_titre():
    
    """
    ------
    Fonction qui permet de donner des recommandations similaires, basés sur les mots_clefs, à un utilisateur 
    à partir de titres de films entrés dans un input 'titres'.
    
    (Voir justification dans le rapport)
    
    
    ##INPUT : 
        --global TMDB_net par la fonction dat() du module Data_frame
        --Titres de films (5 maximums) en input dans la console python ou sur dans le terminal
    
    ##OUTPUTS : 
        -- Affichage dans la console python ou le terminal
    ------
    """
    
    #Appel du dataframe TMDB_clean et Netflix_clean puis copie
    global data_tmdb
    global data_netflix
    df = data_tmdb.copy()
    df_netflix = data_netflix.copy()
    
    titres_bruts = input("Veuilez saisir vos titres : ").lower()
    
    titres_bruts = [titre for titre in titres_bruts.split(", ")]  
    """
    ---
    1.TRAITEMENT DES MINISCULES ET MAJUSCULES
    ---
    """
    #Pour permettre des inputs majuscules et minnuscules 
    titres_bruts_minus = [titres_bruts[i].lower() for i in range(len(titres_bruts))]
    
    #On créer une nouvelle colonne pour les titres en minuscules
    df["title_minus"] = df["title"].str.lower()  
    
    #Dataframe des titres recherchés
    df_titres = df[df["title_minus"].isin(titres_bruts_minus)]
    
    #Conversion en liste des titres recherchés dans leur bonne écriture Majuscule/Minuscule
    titres_bruts = df_titres["title"].tolist()

    
    #Si pas de films associés df_titres est vide; On retourne un message à propos dans le terminal
    if df_titres.empty : 
        df_titres = "Il n'y a pas de films associés à ce/ces titre(s)"
        return df_titres
    
    
    ############################################################
    """
    ---
    2.TRAITEMENT DES DOUBLONS
    ---
    """
    #Liste vide que l'on remplira avec les id des films choisit si doublons par l'utilisateurs (si input)
    id_liste = []
    #Initialisation du datafame qui contiendra les bons titres choisis par leurs id
    df_titres_bon = pd.DataFrame(columns=list(df_titres.columns))
    #Si un film n'a pas de doublons, son id sera mis automatiquement dans cette liste
    id_bon = []
    
        
    #Initialisation de la liste des doublons
    elem = []
    """
    Si le nombre de titres associés dans le dataframe de base est supérieur aux titres recherchés :
    On vérifie si pour chaque titre recherché, le nombre de titres associés dans le dataframe
    est supérieur à 1.
    Si c'est le cas, c'est au moins un doublon, et on ajoute le titre en problématique dans elem et les id 
    des doublons associés dans id_liste.
    Sinon, on ajoute les id des films non problématiques dans id_bon.
    On obtient ainsi le dataframe avec les bon id choisis en utilisant id récupéré.
    """
    if len(df_titres) > len(set(titres_bruts)):
    
        
        for element in set(titres_bruts): 
            doublon = df_titres[df_titres["title"] == element]
            if doublon.shape[0] > 1 :
                elem.append(element)
                print(f"Vous avez {element} en doublon.")
                print(doublon[["id","title","overview"]])
                id_elem = int(input("Choisissez l'id voulu : "))
                id_liste.append(id_elem)
            else :
                id_autre = df[df["title"]==element]["id"]
                id_liste.append(int(id_autre))
                id_bon.append(int(id_autre))
                
    
       
        
    
        for i in range(len(id_liste)):
                bt = id_liste[i]
                df_titres_bon = pd.concat([df[df["id"]==bt],df_titres_bon])
      
                
    #Si aucuns doublons, on ne fait rien
    else : 
        df_titres_bon = df_titres
        print("Vous n'avez aucun doublon ! ")
    ##############################################################
        
   
    #On récupère chaques mot_clefs des films recherchés et traité des doublons 
    keywords = df_titres_bon["keywords"].str.split(", ")
    #On met en liste ces mot_clefs pour pouvoir utiliser isin() dans la suite
    keywords = list(keywords.explode().unique())
    
    #On récupère la note minimale des films recherchés et traité des doublons
    note = float(df_titres_bon["vote_average"].min())
    
    
    """
    ---
    3.QUALITE DES RECOMMANDATIONS
    Si quali_reco > 0, alors beaucoup de valeurs manquantes sont présentes dans les keywords.
    Comme le Dataframe va par la suite en être vidé pour pouvoir permettre la comparaison, on dira que 
    si quali_reco > 0, les recommandations sont d'une qualitée moyenne.
    Sinon, on dira qu'elle sont d'une qualité bonne.
    ---
    """
    #Variable indicatrice de la qualité des recommandations par keywords
    quali_reco = 0
    
    #Gestion des nan pour les keywords
    df_test_na = data_tmdb.copy()
    #On enleve les doublons sur un dataframe de test
    df_test_na = df_test_na.dropna(subset=["keywords"])
    #On selectionne les films recherchés qui sont dans ce dataframe avec aucunes valeurs manquantes en mot-clefs
    titres_test_na = list(df_test_na[df_test_na["title"].isin(titres_bruts)]["title"].unique())
    #Grace à la différence symétrique (conversion en set des listes obligée), on récupère les titres 
    #recherchés qui n'ont pas de mot-clefs (valeurs manquantes)
    test = set(titres_bruts)^set(titres_test_na)
        
    
    
    #Puis on traite la liste des mot-clefs des valeurs manquantes
    #Si au moins une valeurs manquantes, on incrémente de 1 la variable de recommandation
    for key in keywords :
        if type(key) == float:
            keywords.remove(key)
            quali_reco += 1 
        else :
            quali_reco = quali_reco
    if not keywords:
        print("pas de mots clefs")
        
    #On deleste enfin le dataframe de base des keywords en valeurs manquantes pour pouvoir effectuer des comparaisons avec ceux des titres en inputs
    df = df.dropna(subset=["keywords"])
    
    #On selectionne les titres recherchés exploitables (sans keywords manquants)
    titres = list(df[df["title"].isin(titres_bruts)]["title"].unique())
    
    """
    4.RECOMMANDATIONS PAR MOT-CLEFS 
    """
    #Dictionnaire qui à chaque titre lui attribue un dictionnaire contenant ses keywords en liste
    titres_dico = {f"{titres[i]}" : list(df[df["title"] == f"{titres[i]}"]["keywords"].str.split(", ").explode().unique()) for i in range(len(titres))}
    
    #Compteur des mot_clefs communs avec chaque titres du dataframe de base
    count = 0
    #Liste des indices des pour les films ayant en communs plus de 3 mot_clefs avec la liste globale des mot-clefs
    indices = []
    #Liste du nombre de mot-clefs en communs pour chaque films du dataframe de base
    count_val =[]
    #L'ensemble des mots-clefs du dataframe de base
    key = df["keywords"].str.split(", ")

    for i in range(key.shape[0]):
        for j in range(len(keywords)):
             if keywords[j] in list(key.iloc[i]):
                 count += 1
             else:
                 pass
        #Si il y a au moins 3 mots_clefs en communs en ajoute l'indice du film en question
        #On ajoute aussi le nombre exact de mots-clefs en communs
        if count >= 3 :
            indices.append(i)
            count_val.append(count)
            count = 0
        else : 
            count = 0
    
    #Le dataframe de recommandation
    df_reco = df.iloc[indices]
    
    
    
    #Affichage dans le terminal de la qualité des recommandations
    if not df_reco.empty and df_reco.shape[0] >= 1:
        df_reco = df_reco[df_reco["vote_average"] >= note ]
    if quali_reco == 0 :
        print("La qualité de la recommandation est bonne selon les mots clefs : tous mot-clefs sont disponibles pour vos titres")
    else :
        print(f"La qualité de la recommandation est moyenne selon les mots clefs : les mots clefs pour {str(test)} sont non disponibles")
    
    #On enlève les titres recherchés par l'utilisaters du dataframe de recommandation
    df_reco = df_reco[~df_reco["title"].isin(titres)]
    
    #On prend les mots_clefs des films du dataframe de recommandation
    key_net = df_reco["keywords"].str.split(", ")
    
    """
    Etape de l'affichage des similitudes : On introduit un tableau de comparaison vide (que des 0)
    En ligne : les films recherchés traités
    En colonne : les films recommandés
    Le but : Obtenir le nombre de mots_clefs en communs entre chaque films recommandés
    et chaque films recherchés traités
    """
    tableau_comparaison = np.zeros((len(titres),df_reco.shape[0]))
    
    #Initialisation d'un compteur et d'un score (nombre de mots-clefs en commun)
    count_titres = 0
    score_count = []
    
    """
    Pour chaque titres recherchés traités du dictionnaire titres_dico, on regarde combien de mots-clefs sont 
    en commun avec chaque titres recommandés.
    On ajoute alors ce nombre dans le tableau de comparaison
    """
    for i in range(df_reco.shape[0]):
         for j in range(len(titres)):
            for k in range(len(titres_dico[titres[j]])):
                if titres_dico[titres[j]][k] in df_reco["keywords"].iloc[i]:
                    count_titres += 1 
            tableau_comparaison[j,i] = count_titres
            count_titres = 0
    #Conversion tu tableau de comparaison en dataframe pandas 
    tableau_comparaison = pd.DataFrame(tableau_comparaison, columns=[df_reco["title"].iloc[i] for i in range(df_reco.shape[0])])
    #Initialisation du dictionnaire de comparaison 
    dico_comparaison = {f"{titres[i]}" : [] for i in range(len(titres))}
    
    
    """
    Pour chaque colonnes (films recommandés) du tableau de comparaison, on regarde l'indice de ligne 
    (film recherché traité) qui possède le plus grand nombre de mots-clefs en communs.
    L'indice qui l'emporte sera le films recherché traité associé comme similaire au film recommandé.
    On ajoute alors par cet indice, le film recommandé similaire au film recherché traité dans le dictionnaire 
    de comparaison.
    """
    for col in list(tableau_comparaison.columns):
        best_indices = tableau_comparaison[col].idxmax()
        if type(best_indices) == int:
            dico_comparaison[titres[best_indices]].append(col)
        else :
            pass 
    
    
    """
    Dans le cas où 3 mots-clefs ne suffisent pas, on reprend la même idée que précédement 
    mais cette fois-ci pour des mots_clefs en communs au moins supérieur à 1
    """
    count2 = 0
    indices2 = []
    count_val2 =[]
    for k in dico_comparaison.keys():
          if dico_comparaison[k] == []:
              for i in range(key.shape[0]):
                  for j in range(len(titres_dico[k])):
                       if titres_dico[k][j] in list(key.iloc[i]):
                           count2 += 1
                       else:
                           pass
                  if count2 >0 :
                      indices2.append(i)
                      count_val2.append(count)
                      count2 = 0
                  else : 
                      count2 = 0
              
          #Création du dataframe de moindres recommandation
          reco_moindre = df.iloc[indices]
          #On enlève les indices de films déja présent dans le dataframe de recommandation principal df_reco
          reco_moindre = reco_moindre[~reco_moindre["id"].isin(df_reco["id"].tolist())]
          #De même pour les titres
          reco_moindre = reco_moindre[~reco_moindre["title"].isin(titres_bruts)]
          #Concatenation des deux dataframe df_reco et df_moindre
          df_reco = pd.concat([df_reco,reco_moindre])
          #On ajoute les films similaires aux titres qui n'avait pas au moins 3 mots_clefs en communs 
          for i in range(len(reco_moindre["title"].tolist())):
               dico_comparaison[k].append(reco_moindre["title"].tolist()[i])
          
    

    #Affichage dans le terminal des similitudes de recommandations
    print("")
    for i in range(len(titres)):
        print(f"Similaire à {titres[i]} : ", dico_comparaison[titres[i]])
        print("")
        print("")
    
    
    #############################################
    """
    5.DISPONIBILITEES SUR NETFLIX
    """
    #On prends les titres des films recommandés que l'on convertit en liste
    comparaison_title = df_reco["title"].tolist()
    #On ajoute d'abord nos titres recherchés
    for i in range(len(titres_bruts)):
        comparaison_title.append(titres_bruts[i])
    #On compare enfin avec la base de donnée netflix 
    df_dispo_netflix = df_netflix[df_netflix["title"].isin(comparaison_title)]
    
    
   
    
    #############################################
        
    



















