#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 16:19:38 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.8: graphiques:  La proportion d’entit ́es pour chaque label s ́emantique (PER, ORG, LOC, MISC) selon les diff ́erentes versions des textes.
"""

'''importe des libraairies necessaires'''

import json
import glob
import matplotlib.pyplot as plt
import os

'''définition des fonctions'''


#1: Fonction pour ouvrir le fichier JSON

def ouvrir_json(chemin_fichier):# paramètres : chemin vers le fichier JSON  
        with open(chemin_fichier, 'r', encoding='utf-8') as data: #ouvre et charge en mode de lecture un fichier JSON as "data" en encodage UTF-8
            return json.load(data) #:returne les données JSON analysées sous forme de dictionnaire Python

#2: Fonction pour extraire les proportions des entités

def obtenir_proportions_entites(chemin_fichier):# paramètres :chemin vers le fichier
    nom_version = chemin_fichier.split('/')[-1].replace(".json", "")  # Nom du fichier comme identifiant de version
    data = ouvrir_json(chemin_fichier) # Ouvrir le fichier JSON et récupérer les données
    bio_tags = [] #iitialise une liste des tags 
    
    # Boucle pour récupérer les labels des mots qui ne sont pas 'O' 
    for token, info in data.items():
        if info['type'] != 'O':  # Si l'entité n'est pas 'O' ('0' signifie absence d'entité))
            bio_tags.append(info['type'])  # ajouter le label de l'entité à la liste
    
    etiquettes_entites = {}  # initialisation d'un dictionnaire pour les effectifs des entités par catégorie

    for tag in bio_tags: # Boucle pour compter les entités par étiquette
        if '-' in tag: # vérifie si l'étiquette contient un préfixe (par exemple B-PER etc)
            etiquette = tag.split('-')[1] # extraction du label principal (PER, ORG, LOC, etc)
            etiquettes_entites[etiquette] = etiquettes_entites.get(etiquette, 0) + 1 # Mise à jour du compteur
    return nom_version, etiquettes_entites  # retourner le nom de la version et les comptages des entités

#3: Fonction pour tracer les proportions des entités par fichier

def tracer_proportions_par_fichier(comptage_entites):
   
    for entry in comptage_entites:  # une boucle à travers chaque tuple: nom du fichier, comptages des entités
        nom_fichier, comptages = entry  # decomposer le tuple en nom de fichier et comptages des entités
        
        plt.figure(figsize=(12, 6))  # créer un nouveau graphique pour chaque fichier

        
        # trace les proportions pour chaque type d'entité dans le fichier avec des couleurs fixes
        bars = plt.bar(comptages.keys(), comptages.values(), color=['blue', 'orange', 'green', 'red'])  
        
        # aujoute des étiquettes à chaque barre depuis les comptages
        for bar in bars:
            yval = bar.get_height()  # la hauteur  de chaque barre
            # Placer l'étiquette directement au-dessus de la barre en utilisant le nombre des comptages
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 10, str(int(yval)), 
                     ha='center', va='bottom', fontsize=12)
        
        # Ajouter des étiquettes et un titre
        plt.xlabel("Entité")
        plt.ylabel("Nombre")
        plt.title(f"Proportions des entités dans le fichier {nom_fichier}")
        plt.savefig(f"../graphiques/types_bio/proportions_{nom_fichier}")
        plt.show() #affichage

#4: Fonction pour tracer les proportions des entités par auteur et OCR

def tracer_parauteur(comptage_entites_tous):
    couleurs = ['blue', 'orange', 'green', 'red']  # Couleurs des barres
    
    for auteur, ocr_data in comptage_entites_tous.items():
        types_ocr = list(ocr_data.keys())  # Types d'OCR
        types_entites = list(next(iter(ocr_data.values())).keys())  # Types d'entités
        
        # Tracer le graphique
        fig, ax = plt.subplots(figsize=(10, 6))
        largeur = 0.2
        x = range(len(types_ocr))

        for i, type_entite in enumerate(types_entites):
            ax.bar([pos + (i - len(types_entites) / 2) * largeur for pos in x],
                   [ocr_data[ocr].get(type_entite, 0) for ocr in types_ocr],
                   largeur, label=type_entite, color=couleurs[i])

        ax.set_xlabel('Type d\'OCR')
        ax.set_ylabel('Nombre d\'Entités')
        ax.set_title(f'Comptage des entités par OCR pour {auteur}')
        ax.set_xticks(x)
        ax.set_xticklabels(types_ocr)
        ax.legend(title='Types d\'Entités')
        
        plt.savefig(f"../graphiques/types_bio/proportions_{auteur}") # Sauvegarde du graphique
        plt.show()



'''Répresenttaion graphique'''

path_jsonbio = "../resultats/*/*/annotations_bio/*.json"  #chemin vers les fichiers avec des annotations bio
comptage_entites_tous = {} 

chemin_sortie = "../graphiques/types_bio"

if not os.path.exists(chemin_sortie): #Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(chemin_sortie)
    
for chemin in glob.glob(path_jsonbio):
    comptage_entites = []
    #print(chemin)
    #print(comptage_entites)
    version, entites = obtenir_proportions_entites(chemin)  # analyse le fichier JSON
    comptage_entites.append((version, entites))  
    tracer_proportions_par_fichier(comptage_entites) # Génère le graphique
    nom_fichier = chemin.split("/")[-1].replace(".txt", "")  # Extraction du nom de fichier sans extension
    auteur = chemin.split("/")[2]
    ocr = nom_fichier.split("_")[-2]
    
    if auteur not in comptage_entites_tous: # stockage des résultats dans un dictionnaire
        comptage_entites_tous[auteur] = {}

    if ocr not in comptage_entites_tous[auteur]:
        comptage_entites_tous[auteur][ocr] = {}
    comptage_entites_tous[auteur][ocr] = entites #ajout des données


tracer_parauteur(comptage_entites_tous) # Appeler la fonction avec les données


    
