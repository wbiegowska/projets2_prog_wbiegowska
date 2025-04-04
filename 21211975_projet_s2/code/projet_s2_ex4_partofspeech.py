#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 15:28:59 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.4: L'annotation automatique des textes avec Part-of-speech tagging de spaCy

"""

'''importe des libraairies necessaires'''


import spacy  # Bibliothèque de traitement du langage naturel
import json   # pour la gestion des fichiers JSON
import glob   # pour récupérer plusieurs fichiers correspondant à un motif
import re     # pour la manipulation des expressions régulières
import os     # pour gérer les fichiers et dossiers

'''Définitions des fonctions'''

#1: fonction  permettant d’ouvrir un fichier .txt et de lire son contenu
def lire_fichier(chemin):  #parametre: chemin vers le fichier 
 with open(chemin, encoding = "utf-8") as f: #ouvre le fichier en lecture avec encodage UTF-8
     chaine = f.read() #lit le contenu du fichier
 return chaine #retourne le texte 

# 2: Fonction pour sauvegarder les annotations dans un fichier JSON

def json_ecrire(nom, dic): # paramètres : nom du fichier, dictionnaire d'annotations
    with open (nom, "w") as w: #ouvrre le fichier en mode écriture
        w.write (json.dumps(dic, indent= 2)) #convertit le dictionnaire en JSON 
        return w

#3:supprime la ponctuation tout en conservant les espaces
def nettoyer_texte(texte): #Paramètre: texte (chaine de caracteres)

    return re.sub(r'["“”«»„’‘\'.,!?;:]', '', texte)  # remplace les signes de ponctuation par une chaîne vide '' et garde les espaces


#4:Analyse du texte avec spaCy

def nlp_spacy(texte): # paramètres : texte (chaîne de caractères)
    nlp = spacy.load("fr_core_news_sm") #charge le modèle de langue français de spaCy
    doc = nlp(texte) #analyse le texte avec spaCy
    return doc # retourne l'objet spaCy (doc) contenant l'analyse linguistique 

#5: #Fonction pour étiquetter les tokens avec l'outil Part-of-speech tagging de spaCy
def pos_tagger(doc):  # paramètres : le doc (objet spaCy contenant l'analyse du texte)
    pos = {} #initiation du dictionnaire pour stocker les étiquettes
    for token in doc: #boucle qui itère à travers les tokens dans le texte 
        if not token.is_punct and not token.is_space: #condition: si le token est alphanumerique => ignore la ponctuation et les espaces
            pos[token.text] = {"POS": token.pos_} #on ajoute des étiquettes de la catégorie grammaticale pour chaque token 
    return pos #retourne le dictionnaire contenant les mots et leurs catégories grammaticales

'''Application des fontions'''


path = "../DATA-ELTeC/*/*/*.txt" # définition du chemin vers les fichiers texte à traiter
for chemin in  glob.glob(path): ##boucle qui itère à travers les chemins correspondants 
    nom_fichier = chemin.split("/")[-1].replace(".txt", "")  # extraction du nom de fichier sans extension
    auteur = chemin.split("/")[2] #extraction du nom de l'auteur 
    ocr = nom_fichier.split("_")[-1] #détermine le type de traitement OCR
    texte = lire_fichier(chemin) #appelle la fonction lire_fichier pour ouvrir les fichiers 
    texte = nettoyer_texte(texte) #appelle la fonction pour supprimer la ponctuation tout en conservant les espaces
    doc = nlp_spacy(texte) #appelle la fonction pour annoter le texte avec spaCy 
    #filename = os.path.basename(chemin) #extraire le nom de fichier 
    pos = pos_tagger(doc) # appelle la fonction pour donner les étiquettes de la catégorie grammaticale pour chaque token
    
 # Créer un dossier pour sauvegarder les résultats
    dossier_pos = f"../resultats/{auteur}/{ocr}/pos_tagging/"
    if not os.path.exists(dossier_pos): # vérifie si le dossier existe
        os.makedirs(dossier_pos) #crée le dossier si nécessaire
 # Sauvegarde des annotations en JSON
    json_ecrire(f"{dossier_pos}/{nom_fichier}_pos.json", pos) 
    