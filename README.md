# Netflix and The Movie Database Recommender – Python Project

## Overview

The ever-growing availability of digital content makes it increasingly important to develop intelligent systems for navigating large media catalogs. This project aims to design a **simple recommendation system** based on data from **Netflix** and **The Movie Database (TMDb)**. It was developed as part of the "Programming Language 1" course at Université Paris 1 Panthéon-Sorbonne.

Our approach relies on **explicit user preferences** and filters based on key attributes such as genre, rating, language, or release year. It is built entirely in Python, with a graphical interface created using Tkinter to ensure a smooth user experience.

➡️ **Grade received: 16/20**

## Project Description

The project is divided into three core components:

### 1. **Descriptive Analysis and Visualization**
Using Jupyter Notebooks, we explored the two datasets to highlight trends and patterns:
- Average movie rating by genre
- Distribution of release years across platforms
- Key factors influencing rating and popularity

### 2. **Recommendation System**
We implemented several recommendation logics:
- **User-based filters**: Genre, country, duration, language, rating, year, etc.
- **Top-N suggestions** based on rating and popularity
- **Similarity-based suggestions**: Movies similar to those the user already enjoyed

### 3. **Graphical User Interface**
A user-friendly interface was developed using **Tkinter**:
- Allows users to input preferences via dropdowns, checkboxes and entry fields
- Displays filtered movie recommendations with key details (title, genre, synopsis, rating, etc.)


## Project setup

Create a single folder and place the entire project inside it.

## How to launch the project

1. Download the two datasets:

- [Netflix dataset](https://www.kaggle.com/datasets/rahulvyasm/netflix-movies-and-tv-shows)
- [TMDb dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)

2. Place them in the `Data/` folder at the root of the project.

3. Run the scripts in this order:

```bash
python "Data et scripts/Data_frame.py"
python "Data et scripts/Fonctions.py"
python "Data et scripts/Interface.py"
```
To test the functions without the graphical interface, run:

```bash
python "Data et scripts/Fonctions_input.py"
```

Data exploration
To view the data exploration from part 1, open the notebook:

```bash
Data et scripts/Version_final_ p1.ipynb
```
- __Contributors__ :
  
Ibrahim DIABIRA,
Tigran GYURJYAN,
Marwan HAMZAOUI,
Guillaume Roustan

Hope you enjoy exploring 🎬
