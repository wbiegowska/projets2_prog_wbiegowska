#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 14:38:17 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.2-3: La comparaison des annotations BIO  de référence (PP) avec celles d'un OCR: les VP, les FP, le FN, la precision, le rappel et le f-score.

"""

'''importe des libraairies necessaires'''

import csv
import os
import glob


''' Formulation de définitions '''
#1: fonction pour lire  un fichier CSV d'annotations et les retourner dans une forme de liste 
def lire_annotations_csv(fichier_csv): #le seul paramètre d'une fonction est le chemin vers le fichier csv
    annotations = [] #initialisation d'une liste pour stocker des annotations
    with open(fichier_csv, newline="", encoding="utf-8") as f: #ouvre le fichier csv as "f", specifie l'encodage et saute de ligne
        reader = csv.DictReader(f, delimiter=';') #lire le fichier csv
        for row in reader: #boucle qui traverse toutes les lignes du fichier csv et les ajoute dans la liste "annotations"
            annotations.append(row)
    return annotations #retourne la liste des annotations

# 2: Compare les annotations de référence (PP) avec celles d'un OCR et calcule des Vrais Positifs (VP), Faux Positifs (FP) et Faux Négatifs (FN).

def comparer_annotations(ref_annotations, ocr_annotations):#paramètres d'une fonction sont la liste des annotations de référence(PP) et liste des annotations extraites à partir de l'OCR
    VP, FP, FN = 0, 0, 0  # initialise des variables: Vrai Positif, Faux Positif, Faux Négatif
    #création de dictionnaires pour un accès aux annotations
    ref_dict = {ann["Texte"]: ann["Type d'entité"] for ann in ref_annotations} #contient les annotations de référence sous forme {mot : type d'entité}
    ocr_dict = {ann["Texte"]: ann["Type d'entité"] for ann in ocr_annotations} #idem pour les annotations OCR

    # Comparaison des entités
    for token, ref_type in ref_dict.items():#boucle qui traverse tous les tokens du dictionnaire de référence et leur type d'entité
        ocr_type = ocr_dict.get(token, "O") #si le mot n'existe pas dans le dictionnaire 'OCR on considère "O" (aucune entité)
        if ref_type == ocr_type and ref_type != "O": #si le type d'entité de référence  est le meme que celui d'OCR et il n'est pas "O" (aucune entité) alors l'entité est correctement détectée et de même type
            VP += 1  # Vrai Positif: on l'augment par 1
        elif ref_type != "O" and ocr_type == "O":
            FN += 1  # # Faux Négatif : l'entité est absente des annotations OCR
        elif ref_type == "O" and ocr_type != "O":
            FP += 1  # # faux positif : un mot sans entité dans la réference a été annoté comme une entité par l'OCR

    return VP, FP, FN #retourne la tuple (VP, FP, FN)

#3:  calcule la précision, le rappel et le score F1 à partir des Vrais Positifs (VP),Faux Positifs (FP) et Faux Négatifs (FN

def calculer_scores(VP, FP, FN): #3 Paramètres:  Vrais Positifs (VP),Faux Positifs (FP) et Faux Négatifs (FN)
    precision = VP / (VP + FP) if (VP + FP) > 0 else 0 # callcul de  précision : proportion des entités détectées qui sont correctes
    rappel = VP / (VP + FN) if (VP + FN) > 0 else 0 #rappel : proportion des entités de référence qui ont été détectées
    fscore = 2 * (precision * rappel) / (precision + rappel) if (precision + rappel) > 0 else 0 #score F1 : moyenne harmonique entre précision et rappel
    return precision, rappel, fscore #Retourne une tuple (precision, rappel, fscore) :

        


''' Les chemins vers les dossiers/fichiers'''


dossier_principal = "../resultats/" # chemin vers le dossier  contenant les auteurs


dossier_scores = "../scores_comparaison/" # chemin vers un dossier pour sauvegarder les résultats
if not os.path.exists(dossier_scores): # si le dossier n'existe pas encore
    os.makedirs(dossier_scores) #creation du dossier 

''' Application de focntions'''

for auteur in os.listdir(dossier_principal): ## Boucle sur chaque auteur 
    chemin_auteur = os.path.join(dossier_principal, auteur) #extraction du chemin vers le dossier de l'auteur 
    
    if os.path.isdir(chemin_auteur):  # condition "if" vérifie si c'est bien un dossier
        dossier_ref = os.path.join(chemin_auteur, "PP", "annotations_bio") #crée une chemin vers le fichier avec des annotations BIO de référence
        if os.path.exists(dossier_ref):#vérifie que le dossier de référence (PP) existe
            for fichier_pp in glob.glob(os.path.join(dossier_ref, "*_PP_annot.csv")):
                nom_fichier = os.path.basename(fichier_pp).replace("_PP_annot.csv", "") #extraction du nom de fichier de référence
                annotations_ref = lire_annotations_csv(fichier_pp) # charge la version de référence avec "lire_annotations_csv"
                # Comparer avec chaque OCR (Kraken, Tesseract)
                for ocr_type in ["TesseractFra-PNG", "Kraken-base"]:
                    fichier_ocr = f"../resultats/{auteur}/{ocr_type}/annotations_bio/{nom_fichier}_{ocr_type}_annot.csv" # construit un chemin vers un fichier OCR correspondant

                    if os.path.exists(fichier_ocr): # # vérifie si le fichier OCR existe
                        annotations_ocr = lire_annotations_csv(fichier_ocr) #lire des annotations OCR
                        VP, FP, FN = comparer_annotations(annotations_ref, annotations_ocr) #comparaison des annotations entre la référence et l'OCR avec "comparer_annotations"
                        precision, rappel, fscore = calculer_scores(VP, FP, FN)#calcul des métriques de performance: Précision, Rappel, F-score
                        #print(auteur, nom_fichier, ocr_type,VP, FP, FN,precision, rappel, fscore) #affichage des résultats

'''Sauvegarde des résultats'''
                        fichier_sortie = os.path.join(dossier_scores, f"{auteur}_{nom_fichier}_{ocr_type}_scores.csv")
                        with open(fichier_sortie, "w", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f, delimiter=';')
                            writer.writerow(["Auteur", "Fichier", "OCR", "VP", "FP", "FN","Précision", "Rappel", "F-score"]) #écrit l'en-tête du fichier CSV
                            writer.writerow([auteur, nom_fichier, ocr_type, VP, FP, FN, precision, rappel, fscore]) #écrit des résultats