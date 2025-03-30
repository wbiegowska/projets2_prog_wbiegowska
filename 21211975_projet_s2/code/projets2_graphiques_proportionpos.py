#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 01:19:48 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.8: graphiques: La proportion de verbe, d’adjectif, de nom commun etc. qui ont été annotés comme des Entités nommées.
"""

'''importe des libraairies necessaires'''

import json
import matplotlib.pyplot as plt
import glob
import os

#1: Fonction pour ouvrir le fichier JSON

def ouvrir_json(chemin_fichier):# # paramètres : chemin vers le fichier JSON  
        with open(chemin_fichier, 'r', encoding='utf-8') as data: #ouvre et charge en mode de lecture un fichier JSON as "data" en encodage UTF-8
            return json.load(data) #:returne les données JSON analysées sous forme de dictionnaire Python
        
        
'''Répresenttaion graphique'''

path_pos = "../resultats/*/*/pos_tagging/*.json" #chemin vers le fichier json avec les annotations POS
dossier_sortie = "../graphiques/proportion_pos" #chemin vers le dossier pour sauvgarder les graphiques 
if not os.path.exists(dossier_sortie):# vérifie si le dossier existe
    os.makedirs(dossier_sortie) #crée le dossier si nécessaire

for chemin in glob.glob(path_pos): #boucle qui parcouri tous les fichiers correspondant à chemin donné
    nom_fichier = chemin.split("/")[-1].replace(".json", "")  # extraction du nom de fichier sans extension
    data = ouvrir_json(chemin) #charge le fichier json
    
    pos_tags = {} # initialise un dictionnaire pour compter les occurrences de chaque étiquette POS
    
   
    for word, info in data.items():  # itére sur le JSON pour compter les étiquettes POS
        pos = info.get('POS')  # obtenir l'étiquette POS
        
        if pos:  # compte les occurrences de chaque étiquette POS
            if pos not in pos_tags: #si l'étiquette n;est pas encore dans le dictionnaire
                pos_tags[pos] = 0 #on l'initialise dans le dictionnaire
            pos_tags[pos] += 1 #sinon on augment son effectif par 1 
    
    if len(pos_tags) == 0: #vérification s'il y a des données valides avant de générer le graphique
        print("Aucune donnée valide trouvée pour les étiquettes POS.")
    else: # préparation des labels et valeurs pour le graphique
        labels = list(pos_tags.keys()) 
        values = list(pos_tags.values())
    
        # Création du diagramme en camembert
        plt.figure(figsize=(10, 12))
        wedges, texts, autotexts = plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
        plt.legend(wedges, labels, title="Étiquettes POS", loc="center left", bbox_to_anchor=(1, 0.5)) # ajout d'une légende
        plt.title(f"Proportion des étiquettes POS dans le {nom_fichier}") #ajout d'un titre
        plt.axis('equal')  # assure que le graphique est un cercle parfait
        plt.savefig(f"{dossier_sortie}/proportionpos_{nom_fichier}",bbox_inches='tight') # sauvegarde du graphique sous forme d'image
        plt.show()