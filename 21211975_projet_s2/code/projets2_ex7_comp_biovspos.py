#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 16:44:55 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.7: Comparaison des sorties  obtenues avec le Part-of-speech tagging ”PROPN” evec celles obtenues avec l’outil de REN
"""

'''importe des libraairies necessaires'''



import json   # pour la gestion des fichiers JSON
import glob   # pour récupérer plusieurs fichiers correspondant à un motif
import os     # pour gérer les fichiers et dossiers

'''définition des fonctions'''

#1:     Compare les entités nommées en annotation BIO avec les noms propres en annotation POS

def comparer_annotations(fichier_bio, fichier_pos): # paramètres : fichier avec des annotations BIO et POS

    # Charger les annotations BIO
    with open(fichier_bio, 'r', encoding='utf-8') as f: #ouvre et charge en mode de lecture un fichier JSON as "data" en encodage UTF-8
        donnees_bio = json.load(f) # analyse les données JSON  sous forme de dictionnaire 
    
    # Charger les annotations POS
    with open(fichier_pos, 'r', encoding='utf-8') as f:#ouvre et charge en mode de lecture un fichier JSON as "data" en encodage UTF-8
        donnees_pos = json.load(f) # analyse les données JSON  sous forme de dictionnaire 
    
    # extraction des entités nommées BIO (uniquement les tokens marqués B- et I-)
    entites_bio = set( #création d'un ensemble contenant les entités nommées extraites
        token for token, info in donnees_bio.items() #parcourt chaque token et ses informations dans les annotations BIO
        if isinstance(info.get('type'), str) and #vérifie si la valeur associée à 'type' est une chaîne de caractères
           (info['type'].startswith('B-') or info['type'].startswith('I-')) #sélectionne uniquement les tokens marqués 'B-' ou 'I-'
    )
    
    # Extraire les noms propres à partir des annotations POS
    noms_propres_pos = set( #création d'un ensemble contenant les noms propres extraits
        token for token, info in donnees_pos.items() #parcourt chaque token et ses informations dans les annotations POS
        if info.get('POS') == 'PROPN' # prend uniquement les tokens dont la catégorie grammaticale (POS) est 'PROPN' (nom propre)
    )
    
    # Calculer les métriques de comparaison
    return {
        'entites_nommees_bio': len(entites_bio),  # nombre d'entités nommées en BIO
        'noms_propres_pos': len(noms_propres_pos),  # nombre de noms propres en POS
        'tokens_communs': len(entites_bio.intersection(noms_propres_pos)),  # nombre de tokens en commun
        'uniquement_dans_bio': list(entites_bio - noms_propres_pos),  # tokens uniquement présents en BIO
        'uniquement_dans_pos': list(noms_propres_pos - entites_bio)  # tokens uniquement présents en POS
    }

#2:Compare les annotations BIO et POS pour chaque auteur et type d'OCR.

def traiter_comparaisons(chemin_resultats): # paramètres:chemin vers les fichiers

    resultats = {}  # initialise un dictionnaire pour stocker les résultats des comparaisons
    
    for auteur in os.listdir(chemin_resultats): # parcours tous les auteurs et liste tous les éléments dans le répertoire des résultats
        chemin_auteur = os.path.join(chemin_resultats, auteur) #construire le chemin complet du dossier de l'auteur
        if not os.path.isdir(chemin_auteur):  # vérifier si c'est bien un dossier
            continue # passer à l'auteur suivant si ce n'est pas un dossier
        
        resultats_auteur = {} #initialise un dictionnaire pour stocker les résultats de l'auteur
        
        # Traiter chaque type d'OCR
        for type_ocr in ['Kraken-base', 'TesseractFra-PNG']:  # parcourir les deux types d'OCR à analyser
            # Trouver les fichiers BIO et POS
            fichiers_bio = glob.glob(os.path.join(chemin_auteur, type_ocr, 'annotations_bio', '*.json'))   # récupére les fichiers JSON des annotations BIO pour ce type d'OCR
            fichiers_pos = glob.glob(os.path.join(chemin_auteur, type_ocr, 'pos_tagging', 'noms_propres', '*.json')) #idem pour POS
            
            # Passer si aucun fichier correspondant n'est trouvé
            if not fichiers_bio or not fichiers_pos:# vérifier si au moins un fichier BIO et un fichier POS existent
                continue # si l'un des deux est manquant, passer à l'itération suivante
            
            # Comparer les  fichiers correspondants
            comparaison = comparer_annotations(fichiers_bio[0], fichiers_pos[0]) #appellle la fonction de comparaison
            resultats_auteur[type_ocr] = comparaison # stockage de résultat de la comparaison pour ce type d'OCR
        
        
        resultats[auteur] = resultats_auteur # ajoute les résultats de l'auteur au dictionnaire principal
    
    return resultats
''' Application de focntions'''


chemin_resultats = "../resultats/" # Chemin vers le dossier avec des fichiers BIO et POS

resultats_comparaison = traiter_comparaisons(chemin_resultats) #appelle une fontion pour comparer les fichiers 

# Affichage des résultats
for auteur, comparaisons_ocr in resultats_comparaison.items():
    print(f"\nAuteur : {auteur}")
    for type_ocr, comparaison in comparaisons_ocr.items():
        print(f"\nOCR : {type_ocr}")
        print(f"Entités nommées BIO : {comparaison['entites_nommees_bio']}")
        print(f"Noms propres POS : {comparaison['noms_propres_pos']}")
        print(f"Tokens communs : {comparaison['tokens_communs']}")
        print("Top 5 tokens uniquement en BIO :", comparaison['uniquement_dans_bio'][:5])
        print("Top 5 tokens uniquement en POS :", comparaison['uniquement_dans_pos'][:5])

# Créer un dossier pour sauvegarder les résultats

dossier_sauvegarde = "../comp_bio_pos" #chemin vers les dossier pour stocker des résultats

if not os.path.exists(dossier_sauvegarde): # vérifie si le dossier existe
    os.makedirs(dossier_sauvegarde) #crée le dossier si nécessaire

# Sauvegarde des résultats

with open(f'{dossier_sauvegarde}/comparison_biovspos_results.json', 'w', encoding='utf-8') as f:#ouvrre le fichier en mode écriture
    json.dump(resultats_comparaison, f, ensure_ascii=False, indent=4)  #convertit le dictionnaire en JSON  et le sauvgarde
