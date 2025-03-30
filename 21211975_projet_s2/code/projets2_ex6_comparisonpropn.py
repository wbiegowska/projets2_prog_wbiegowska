#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 14:32:14 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.6: Comparaison des sorties du Part-of-speech tagging ”PROPN” de la référence avec les sorties pour les OCR.
"""

'''importe des libraairies necessaires'''



import json   # pour la gestion des fichiers JSON
import glob   # pour récupérer plusieurs fichiers correspondant à un motif
import os     # pour gérer les fichiers et dossiers


'''définition des fonctions'''

#1: Fonction pour ouvrir le fichier JSON

def ouvrir_json(chemin_fichier):# # paramètres : chemin vers le fichier JSON  
        with open(chemin_fichier, 'r', encoding='utf-8') as data: #ouvre et charge en mode de lecture un fichier JSON as "data" en encodage UTF-8
            return json.load(data) #:returne les données JSON analysées sous forme de dictionnaire Python
        

#2:Compare les annotations des noms propres entre le fichier de référence et le fichier OCR.

def comparer_annotations_propn(fichier_reference, fichier_ocr): #paramètres: Chemins vers le fichier JSON des noms propres de référence et OCR
    
    # Charger les dictionnaires
    propn_reference = ouvrir_json(fichier_reference) #dic de référence
    propn_ocr = ouvrir_json(fichier_ocr) #dic OCR
    
    # Extraire les tokens de noms propres
    tokens_reference = set(token for token, info in propn_reference.items() if info.get('POS') == 'PROPN') #dic de référence
    tokens_ocr = set(token for token, info in propn_ocr.items() if info.get('POS') == 'PROPN')  #dic OCR
    
    # Calculer les métriques de comparaison
    intersection = tokens_reference.intersection(tokens_ocr) # trouve les tokens communs 
    union = tokens_reference.union(tokens_ocr)  # combine tous les tokens des deux ensembles sans doublons
    difference_reference = tokens_reference - tokens_ocr #extrait les tokens présents dans tokens_reference mais pas dans tokens_ocr
    difference_ocr = tokens_ocr - tokens_reference #les tokens présents dans tokens_ocr mais pas dans tokens_reference
    
    return { #retourne un dictionnaire avec les métriques de comparaison
        'total_ref_propn': len(tokens_reference),
        'total_ocr_propn': len(tokens_ocr),
        'intersection_count': len(intersection),
        'union_count': len(union),
        'difference_ref_count': len(difference_reference),
        'difference_ocr_count': len(difference_ocr),
        'intersection': list(intersection),
        'difference_ref': list(difference_reference),
        'difference_ocr': list(difference_ocr)
    }

#3: Traite les comparaisons pour tous les auteurs dans le répertoire des résultats.

def traiter_comparaisons_auteurs(chemin_resultats): #paramètres:chemin vers le répertoire des résultats contenant les dossiers des auteurs
   
    resultats = {} #initialisation d'un dictionnaire pour stocker les résultats
    
    
    auteurs = [d for d in os.listdir(chemin_resultats) # liste des auteurs (noms des dossiers dans le répertoire des résultats)
               if os.path.isdir(os.path.join(chemin_resultats, d))] #récupère les dossiers d'auteurs
    
    for auteur in auteurs: #boucle qui parcours  chaque auteur
        chemin_auteur = os.path.join(chemin_resultats, auteur) #définit le chemin complet vers le dossier de l'auteur
        resultats_auteur = {}  # initialise un dictionnaire pour stocker les résultats de l'auteur
        
        types_ocr = ['Kraken-base', 'TesseractFra-PNG']  # liste avec les types OCR (Kraken-base et TesseractFra-PNG)

        
        for type_ocr in types_ocr: #parcours des types OCR
            # trouver les chemins vers les fichiers de référence (PP) et OCR des noms propres:
            chemin_pp = os.path.join(chemin_auteur, 'PP', 'pos_tagging', 'noms_propres', '*.json') 
            chemin_ocr = os.path.join(chemin_auteur, type_ocr, 'pos_tagging', 'noms_propres', '*.json') 
            # obtenir tous les fichiers correspondants
            fichiers_pp = sorted(glob.glob(chemin_pp)) #récupère les fichiers de référence (PP)
            fichiers_ocr = sorted(glob.glob(chemin_ocr))#idem pourles fichiers OCR
            comparaison = comparer_annotations_propn(fichiers_pp[0], fichiers_ocr[0])  # Compare les fichiers de référence et OCR
            resultats_auteur[type_ocr] = comparaison #enregistre les résultats de la comparaison pour ce type OCR
        
        # Stocker les résultats pour cet auteur
        resultats[auteur] = resultats_auteur
    
    return resultats #retourne dles résultats détaillés des comparaisons pour tous les auteurs

#4: Afficher les résultats détaillés de la comparaison

def afficher_resultats_detailles(resultats): #paramètres: le diictionnaire des résultats de la comparaison

    for auteur, comparaisons_ocr in resultats.items(): #parcours  les auteurs et leur comparaisons dans le dictionnaire vaec des résultats 
        print(f"\n{'='*20} Auteur: {auteur} {'='*20}") #affichage du nom de l'auteyr
        for type_ocr, comparaison in comparaisons_ocr.items(): #boucle à  travers les types ocr dans le dictionnaire des résultats
            print(f"\n--- Comparaison {type_ocr} ---") #afffichage du type de OCR
            print(f"Total des noms propres de référence : {comparaison['total_ref_propn']}")
            print(f"Total des noms propres OCR : {comparaison['total_ocr_propn']}")
            print(f"Nombre d'intersections : {comparaison['intersection_count']}")
            # Affichage les 10 premières différences si nécessaire
            print("\nTop 10 des tokens uniquement dans la référence :")
            print(comparaison['difference_ref'][:10])
            print("\nTop 10 des tokens uniquement dans l'OCR :")
            print(comparaison['difference_ocr'][:10])
            
            
#5:  Sauvegarde les résultats de comparaison dans un fichier JSON       
def enregistrer_resultats_dans_fichier(resultats, chemin_sortie):#paramètres:dictionnaire des résultats de la comparaison et le chemin pour enregistrer le fichier des résultats
    with open(chemin_sortie, 'w', encoding='utf-8') as f: #ouvrre le fichier en mode écriture
        json.dump(resultats, f, ensure_ascii=False, indent=4) #convertit le dictionnaire en JSON 

''' Application de focntions'''

# Chemin vers le dossier avec des noms propres de référence et OCR
chemin = "../resultats/"
resultats = traiter_comparaisons_auteurs(chemin) #Comparaison des sorties avec "traiter_comparaisons_auteurs"

 # Créer un dossier pour sauvegarder les résultats
dossier_comppropn = "../comparison_pos_npropres"
if not os.path.exists(dossier_comppropn):# vérifie si le dossier existe
    os.makedirs(dossier_comppropn) #crée le dossier si nécessaire

# Sauvegarde les résultats dans un fichier
enregistrer_resultats_dans_fichier(resultats, f"{dossier_comppropn}/'pospropn_comparison_results.json'")

# Affichage dess résultats détaillés
afficher_resultats_detailles(resultats)


