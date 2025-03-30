#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 13:57:17 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.5: Récupération des tokens dont le label est ”PROPN” (Proper Noun).
"""

'''importe des libraairies necessaires'''



import json   # pour la gestion des fichiers JSON
import glob   # pour récupérer plusieurs fichiers correspondant à un motif
import os     # pour gérer les fichiers et dossiers


'''définition des fonctions'''

#1: FOnction pour ouvrir le fichier JSON

def ouvrir_json(chemin_fichier):# # paramètres : chemin vers le fichier JSON  
        with open(chemin_fichier, 'r', encoding='utf-8') as data: #ouvre et charge en mode de lecture un fichier JSON as "data" en encodage UTF-8
            return json.load(data) #:returne les données JSON analysées sous forme de dictionnaire Python
        
# 2: Fonction pour sauvegarder les annotations dans un fichier JSON

def json_ecrire(nom, dic): # paramètres : nom du fichier, dictionnaire d'annotations
    with open (nom, "w") as w: #ouvrre le fichier en mode écriture
        w.write (json.dumps(dic, indent= 2)) #convertit le dictionnaire en JSON 
        return w

''' Application de focntions'''


path_json = "../resultats/*/*/pos_tagging/*.json" # définition du chemin vers les fichiers json à traiter: les fichiers avec POS-tagging
for chemin in  glob.glob(path_json): #cherche le chemin vers chaque fichier avec librarie glob
    dic_propn = {} #initialisation d'un dictionnaire pour stocker tous les tokens dont le label est ”PROPN”
    dic_pos = ouvrir_json(chemin) #appelle une fonction "ouvrir_json" pour charger le fichier json
    #print(chemin)
    for token, label_info in dic_pos.items():#boucle à travers tous les tokens (clés) et leurs étiquettes (valuers)
        if "POS" in label_info and label_info["POS"] == "PROPN":
            dic_propn[token] = label_info

    nom_fichier = chemin.split("/")[-1].replace(".json", "") # extraction du nom de fichier sans extension
    auteur = chemin.split("/")[2] #extraction du nom de l'auteur
    ocr = nom_fichier.split("_")[2] #détermine le type de traitement OCR
    
 # Créer un dossier pour sauvegarder les résultats
    dossier_propn = f"../resultats/{auteur}/{ocr}/pos_tagging/noms_propres"  #chemin vers le dossier pour sauvgarder les dictionnaires 
    if not os.path.exists(dossier_propn): # vérifie si le dossier existe
        os.makedirs(dossier_propn) #crée le dossier si nécessaire
 # Sauvegarde des dictionnaires avec les noms porpres en JSON
    json_ecrire(f"{dossier_propn}/{nom_fichier}_propn.json", dic_propn)
    
            