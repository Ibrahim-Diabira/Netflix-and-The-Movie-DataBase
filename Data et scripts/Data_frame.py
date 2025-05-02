#MODULE PREPARATION DES DATA FRAME 'Prepare_data' 

"""
                                               ---------------------------------------
    Module de préparation des données pour leurs bonne intégration dans les systemes de filtres/suggestions et de recommandations
                                               ---------------------------------------
"""

import pandas as pd



TMDB = pd.read_csv("Data/TMDB_movie_dataset_v11.csv")
Netflix = pd.read_csv("Data/netflix_titles.csv",encoding='unicode_escape')

def TMDB_clean():
    """
    -----
    Fonctions qui prépare les données TMDB en vue d'une utilisation de filtrage et de recommandation
    
    **INPUT** : Le data frame TMDB brut
    
    **OUTPUT** : Un data frame TMDB utilisable pour une recherche par filtre
    
    ##Voir le rapport situé dans le fichier ... pour plus de justification du code
    
    -----
    """
    global TMDB
    df_clean = TMDB.copy()
    
    
    #On eneleve les valeurs manquantes pour les variables d'intérêts pour les recherches par filtres/suggestions
    df_clean = df_clean.dropna(subset =["title","release_date","id","genres"])
    
    #On décide de prendre uniquement les films d'une durée supérieur à 30 minutes et inférireur à 300 minutes
    #On prend également uniquement les films qui ont recus plus de 10 votes pour avoir un minimum de cohérence 
    df_clean = df_clean[(df_clean["runtime"]>=30) & (df_clean["runtime"]<=300) & (df_clean["vote_count"]>= 20)] 
    
    #On convertit les dates dans le format année pour simplifier les recherches, et pouvoir comparer avec Netflix
    df_clean["release_date"] = pd.to_datetime(df_clean["release_date"])
    df_clean["release_date"] = df_clean["release_date"].dt.strftime("%Y")
    
    return df_clean
    
TMDB_clean().shape

def Netflix_clean():
    """
    -----
    Fonction qui traite simplement le dataframe netflix en lui enlevant les colonnes inutiles
    
    **INPUT** : Le data frame Netflix 
    
    **OUTPUT** : Le data frame Netflix utilisable 
    -----
    
    """
    global Netflix
    df = Netflix.copy()
    
    #On ne garde que les 12 premières colonnes
    colonnes = df.columns
    colonnes = list(colonnes)
    df_clean = df[colonnes[:12]]
    
    return df_clean
    



def prod_countries(data):
    """
    ------
    Fonction qui nous renvoie la liste des pays de production depuis le dataframe TMDB
    Elle sera integrer à l'interface pour creer un filtre "Pays de production"'
    
    ***INPUT*** : Le dataframe utilisable
    
    ***OUTPUT*** : Renvoie une liste des pays de productions contenu dans le dataframe utilisable
    ------
    """
    df = data.copy()
    #Suppresion des valeurs manquantes pour éviter les erreurs futurs
    df = df.dropna(subset=["production_countries"])
    
    #Récupération des Pays de production de manière séparé
    df["production_countries"] = df["production_countries"].str.split(", ")
    df = df.explode("production_countries")
    
    
    return list(df["production_countries"].unique())



















