#MODULE 'Fonctions' DEDIE A L'INTERACTION AVEC L'INTERFACE GRAPHIQUE

"""
*********************************************************************************

Ce module reprend les fonctions créees pour la partie n°2 de l'exercice.
Au lieu cette fois d'y intégrer des inputs pour l'interraction homme/machine,
on y integre une adaptation pour interragir facilement avec l'interface graphique Tkinter.'

*********************************************************************************
"""


import Data_frame as dat
import pandas as pd
import numpy as np

"""

"""
#Appel de TMDB_net du module Data_frame
data_tmdb = dat.TMDB_clean()
data_netflix = dat.Netflix_clean()

"""
                              #######
          Fonctions utilisée pour l'onglet 'recherches par filtres simples'
                              #######
                              
        **df_filtre_genre : filtre le dataframe TMDB_clean selon les genres donnés
        et selon les meilleures notes reçus ---> renvoie un dataframe
        
        **df_filtre_année : filtre le dataframe df_filtre_genre selon date
        ---> renvoie un dataframe
        
        **df
"""


"""
df_filtre_genre
df_filtre_annee

Le but de ces fonctions est de filtrer la Dataframe afin de ne garder que les films les plus pertinents
d'après les genres/années entrés par l'utilisateur. 

"""

#Filtre par genre
def df_filtre_genre(genres=None): #On crée la fonction avec comme argument les genres entrés par l'utilisateur.
#On met comme valeur par défaut : None. Ce qui laisse la possibilité à l'utilisateur de ne rien entrer.
    global data_tmdb
    
    if genres is not None: #Si l'utilisateur a bien entré des genres
        df = data_tmdb.copy() #On appelle df la DataFrame pour plus de facilité dans la fonciton
        for genre in genres: 
            df = df[df["genres"].str.contains(genre, case=False)]
        #On crée une boucle pour parcourir les genres entrés par l'utilisateur
        #Pour chaque genre entré on cherche dans la Dataframe les films qui contiennent ce genre grâce à la fonction contains. 
        #La fonction contains nous retourne un Booléen True ou False selon si la chaine de caractère contient le genre entré ou non.
        #case = False permet de rendre la recherche insensible à la casse càd qu'elle ignore les maj et min. 
        
        #On obtient à la fin de la boucle une DataFrame contenant seulement les films ayant des genres entrés par l'utilisateur. 
        
        
        #La dernière étape est le tri de la DataFrame. 
        #Grâce à la méthode sort_values on trie d'abord par la note puis par la popularité du film
        df = df.sort_values(by=["vote_average","popularity"],ascending = False ) #ascending = False permet de trier dans le sens décroissant
        return df
    else:
        data = data_tmdb.sort_values(by=["vote_average","popularity"],ascending = False )
        return data
    #Si l'utilisateur n'a pas entré de genres on renvoie simplement la DataFrame en triant par la note et la popularité.


#Filtre par année 
#La fonction prend comme argument la DataFrame et l'année qu'on initialise à None pour permettre à l'utilisateur de ne rien entrer
def df_filtre_annee(data, year=None):
    if year is not None:   #Dans le cas ou l'utilisateur a bien entré une valeur
        df=data.copy() 
        df = df[df["release_date"].isin(year)] #On cherche grâce à la méthode isin qui retourne des booléens pour chaque film selon si la valeur 
        #entré par l'utilisateur se trouve dans la colonne release_date
        return df
    else : 
        return data #Dans le cas où l'utilisateur n'a pas entré de valeur on retourne simplement la DataFrame

"""
infos_perso est la fonction qui renvoie à la partie deux de la conception du moteur de recherche

Le but de la fonction est de retourner une DataFrame contenant les 5 films les plus susceptibles d'être appréciés par l'utilisateur,
selon les infos qu'il renseigne. 
La fonction prend 5 arguments : 
    genre_ent : le/les genres entrés par l'utilisateur
    annee_ent : le/les années entrés par l'utilisateur
    pays_ent : le/les pays entrés par l'utilisateur
    adult_ent : Une variable indicatrice pour savoir si l'utilisateur veut inclure ou non les films pour adulte
    runtime_ent : La durée de film souhaitée par l'utilisateur
    
"""

#Filtre pour suggestions personnelles
def infos_perso(genre_ent=None,annee_ent=None,pays_ent=None,adult_ent=None,runtime_ent=None): 
    global data_tmdb  
    df = data_tmdb.copy()

    if runtime_ent is not None: 
        runtime_ent = runtime_ent
    
    #On crée une fonction qui va compter le nombre de genres en commun (voir utilisateur plus loin)
    def compteur_genres(film_genres): 
        compteur = 0   #On initialise la variable compteur à 0
        for genre in genre_ent: #Pour chaque genre dans la liste des genres entrés par l'utilisateur
            if genre in str(film_genres): #Si le genre en question est compris dans les genres du film de la ligne du dataframe,
                compteur += 1 #On ajoute 1 à compteur. 
        return compteur
    
    #On fait la même chose pour compter le nombre de pays en commun
    def compteur_pays(film_pays):
        compteur = 0 #On initialise le compteur à 0.
        for pays in pays_ent: #Pour chaque pays dans la liste des pays entrés
            if pays in str(film_pays): #Si le pays est contenu dans les pays de production du film de la ligne du dataframe, 
                compteur += 1 #Le compteur augmente de 1
        return compteur
    
    
    if genre_ent: #Si la liste des genres entrés n'est pas vide (cf l'utilisateur a entré des genres)
        df["memes_genres"] = df["genres"].apply(compteur_genres) #On crée une colonne "memes_genres" dans la dataframe.
        #Cette nouvelle colonne contiendra un nombre qui sera le nb de genres en commun avec les genres entrés par l'utilisateur.
        #On applique à la colonne "genres " de la DF la fonction créee ci-dessus
    else : 
        df = df #Dans le cas où l'utilisateur n'entre pas de genres. 

    
    if pays_ent: #Si la liste des pays entrés par l'utilisateur n'est pas vide (cf L'utilisatateur a bien entré des valeurs pour les pays)
        df["memes_pays"] = df["production_countries"].apply(compteur_pays)
        #Tout comme pour les genres on crée une colonne "memes pays" dans laquelle on retrouvera le nb de pays en commun avec les pays entrés par l'utilisateur
        #On applique pour cela à la colonne "production_countries" la fonction crée ci-dessus. 
    else : 
        df = df 
  
    
    if annee_ent: #Si l'utilisateur a bien entré des valeurs pour les années
        df = df[df["release_date"].isin(annee_ent)] #On filtre la dataframe (comme dans la fonction précédente) pour ne garder que les films
        #étant produit l'année entré par l'utilisateur
    else : 
        df = df
    
    
    #La variable binaire adult
    if adult_ent == "non": #Si l'utilisateur entre la chaine de caractère "non"
        df = df[df["adult"] == 0] #On filtre la dataframe en ne gardant que les films pour lesquels adult=0
    elif adult_ent == "oui": #Si l'utilisateur entre "oui"
        df=df #Dans ce cas l'utilisateur n'impose pas de restriction.
        #On lui retourne la dataframe avec à la fois les films pour adulte et les autres films.  
   
    #La question de la durée du film. 
    if runtime_ent:
        df = df[(df["runtime"] >= runtime_ent - 30) & (df["runtime"] <= runtime_ent + 30)]
        #Si l'utilisateur entre bien une valeur pour le runtime. Nous avons décidé d'afficher les films dans un intervalle de 30 min
    else : 
        df = df 
    
    
    df_sorted = df.sort_values(
        by=["memes_genres", "memes_pays", "release_date", "vote_average", "popularity"],
        ascending=[False, False, False, False, False]
    )
    #On trie les valeurs d'abord selon la correspondance des genres, puis la correspondance des pays, la date de réalisation, la note et enfin la popularité. 
    
    df_top_5 = df_sorted.head(5) #On crée df_top_5 qui correspond simplement aux 5 premières lignes de la DataFrame df_sorted.
    
    return df_top_5 #On retourne la DataFrame avec les 5 meilleurs recommendations







#Recommandation par mots_clefs
def reco_titre(titres_bruts,ID=[]):
    
    """
    ------
    Fonction qui permet de donner des recommandations similaires, basés sur les mots_clefs, à un utilisateur 
    à partir de titres de films entrés dans un input 'titres', ici conçus pour s'intégrer
    à l'interface Tkinter
    
    (Voir justification dans le rapport)
    
    
    ##INPUT : 
        --global TMDB_net par la fonction dat() du module Data_frame
        --Titres de films (5 maximums)
        -- Une liste ID, par défaut vide, servant à l'interraction homme/machine pour saisir les id des films 
        souhaités dans le cas des doublons
    
    ##OUTPUTS : 
        --Un dictionnaire 'dico_comparaison' permettant de lié les films rercherchés et recommandés à partir de leurs similitudes en termes de mots clefs 
    
        --Un dataframe 'df_reco' comprenant les recommandations liées aux films recherchés 
        
        --Un dataframe 'df_titres' comprenant simplement les films recherchés
        
        --Un dataframe 'df_dispo_netflix' comprenant les films recherchés et recommandés
        disponibles sur la plateforme netflix
        
        --Une liste des films avec doublons,s'il en existe nommé 'elem'
    ------
    """
    
    #Appel du dataframe TMDB_clean et Netflix_clean puis copie
    global data_tmdb
    global data_netflix
    df = data_tmdb.copy()
    df_netflix = data_netflix.copy()
    

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
    Sinon, on ajoute les id des films non problématiques dans id_bon
    """
    if len(df_titres) > len(set(titres_bruts)):
    
        
        for element in set(titres_bruts): 
            doublon = df_titres[df_titres["title"] == element]
            if doublon.shape[0] > 1 :
                elem.append(element)
                for i in range(len(doublon["id"].tolist())):
                    id_liste.append(doublon["id"].tolist()[i])
            else :
                id_autre = df[df["title"]==element]["id"]
                id_liste.append(int(id_autre))
                id_bon.append(int(id_autre))
                
                
    
       
        """
    Pour chaque id, si la liste ID est vide, c'est que rien n'a été entré par l'utilisateur dans Tkinter.
    Dans ce cas, on selectionne chaque id récupéré dans id_liste, et on prend les films 
    du dataframe associées à l'ensemble de ces id.
        """
    
        for i in range(len(id_liste)):
            if ID == []:
                bt = id_liste[i]
                df_titres_bon = pd.concat([df[df["id"]==bt],df_titres_bon])
        """
        Si ID n'est pas vide, c'est qu'au moins un id à été saisis par l'utilisateur dans Tkinter.
        Dans ce cas, on rajoute en plus des id saisis, les id des films non problématiques.
        On finis alors par ajouter les titres des bons films dans le dataframe des bon titres
        """
        if ID != []:
            for i in range(len(id_bon)):
                ID.append(id_bon[i])
            for i in range(len(ID)):
                bt = ID[i]
                df_titres_bon = pd.concat([df[df["id"]==int(bt)],df_titres_bon])
                
    #Si aucuns doublons, on ne fait rien
    else : 
        df_titres_bon = df_titres
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
        
    return dico_comparaison,df_reco,df_titres,df_dispo_netflix,elem





