#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 13:28:50 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.1: L'annotation des  entités nommées, leur label BIO et leur label de catégorie sémantique (PER, LOC, ORG, MISC)


"""

'''importe des libraairies necessaires'''

import spacy  # Bibliothèque de traitement du langage naturel
import json   # pour la gestion des fichiers JSON
import glob   # pour récupérer plusieurs fichiers correspondant à un motif
import re     # pour la manipulation des expressions régulières
import os     # pour gérer les fichiers et dossiers
import csv    # pour l'écriture et la lecture de fichiers CSV

'''Définitions des fonctions'''

#1: fonction  permettant d’ouvrir un fichier .txt et de lire son contenu
def lire_fichier(chemin):  #parametre: chemin vers le fichier 
 with open(chemin, encoding = "utf-8") as f: #ouvre le fichier en lecture avec encodage UTF-8
     chaine = f.read() #lit le contenu du fichier
 return chaine #retourne le texte 

#2:supprime la ponctuation tout en conservant les espaces
def nettoyer_texte(texte): #Paramètre: texte (chaine de caracteres)

    return re.sub(r'["“”«»„’‘\'.,!?;:]', '', texte)  # remplace les signes de ponctuation par une chaîne vide '' et garde les espaces
    
#3:Annoter le texte avec spaCy en format IOB
def annoter_texte(texte):  
    nlp = spacy.load("fr_core_news_sm")  # Charge le modèle de langue
    doc = nlp(texte) #analyse le texte avec spaCy
    annotations = {}  # initialise un dictionnaire pour stocker des annotations

    for token in doc:  # Boucle qui itère à travers tous les tokens
        if token.ent_iob_ == "O": #si le mot n'appartient à aucune entité nommée
            bio_tag = "O" #on le donne l'étiquette vide "0"
        else:
            bio_tag = f"{token.ent_iob_}-{token.ent_type_}" # formate l'étiquette IOB avec le type d'entité
        
        annotations[token.text] = {
            "type": bio_tag #stockage des annotations sous forme de dictionnaire
        }
    
    return annotations # retourne les annotations sous forme de dictionnaire

# 4: Fonction pour sauvegarder les annotations dans un fichier JSON

def json_ecrire(nom, dic): # paramètres : nom du fichier, dictionnaire d'annotations
    with open (nom, "w") as w: #ouvrre le fichier en mode écriture
        w.write (json.dumps(dic, indent= 2)) #convertit le dictionnaire en JSON 
        return w
    
# 5: Fonction pour sauvegarder les annotations dans un fichier CSV

def sauvegarder_csv(annotations, fichier_sortie):
    with open(fichier_sortie, "w", newline="", encoding="utf-8") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Écriture de l'en-tête
        writer.writerow(["Texte", "Type d'entité"])
        
        # Écriture des annotations
        for mot, info in annotations.items():  # Corrected: Iterate over key-value pairs
            writer.writerow([mot, info["type"]])  # Corrected: Write word + entity type


''' Application de focntions'''

chemin_fichiers = "../DATA-ELTeC/*/*/*.txt" # définition du chemin vers les fichiers texte à traiter


for chemin in glob.glob(chemin_fichiers): #boucle à travers tous les fichiers correspondants
    #print (chemin)
    nom_fichier = chemin.split("/")[-1].replace(".txt", "")  # extraction du nom de fichier sans extension ".txt"
    auteur = chemin.split("/")[2] #extraction du nom de l'auteur 
    ocr = nom_fichier.split("_")[-1] #détermine le type de traitement OCR
    # lecture et nettoyage du texte
    texte = lire_fichier(chemin) #lit le fichier avec "lire_fichier"
    texte = nettoyer_texte(texte) #nettoye le texte avec "nettoyer_texte"
    # Annotation du texte avec spaCy
    annotations = annoter_texte(texte)
    
    # Définition du chemin où enregistrer les annotations
    dossier_annotations = f"../resultats/{auteur}/{ocr}/annotations_bio" 
    if not os.path.exists(dossier_annotations): # vérifie si le dossier existe
        os.makedirs(dossier_annotations) #crée le dossier si nécessaire

     # Sauvegarde des annotations en JSON
    fichier_json= f"../resultats/{auteur}/{ocr}/annotations_bio/{nom_fichier}_bioannot.json"
    #print(fichier_json)
    json_ecrire (fichier_json, annotations)
    
    # Sauvegarde en CSV
    fichier_csv = f"../resultats/{auteur}/{ocr}/annotations_bio/{nom_fichier}_annot.csv"
    sauvegarder_csv(annotations, fichier_csv) #sauvgarde les annotations dans un fichier CSV
    


        
        
        