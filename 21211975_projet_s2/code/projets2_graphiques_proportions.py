#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 23:37:37 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.8: graphiques:  Les proportions de VP, FP, VN, FN dans la REN sur des donn ́ees OCR pour chaque textes selon les versions et globalement.

"""

'''importe des libraairies necessaires'''
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import seaborn as sns

# Dossier contenant les fichiers CSV
dossier_csv = "../scores_comparaison/"

dossier_graphiques = "../graphiques/precision" #chemin vers le dossier pour sauvgarder les graphiques 
if not os.path.exists(dossier_graphiques): # vérifie si le dossier existe
    os.makedirs(dossier_graphiques) #crée le dossier si nécessaire


fichiers = glob.glob(os.path.join(dossier_csv, "*.csv")) # charger tous les fichiers CSV avec glob
data = pd.concat([pd.read_csv(f, delimiter=';') for f in fichiers], ignore_index=True) #lire et concaténer tous les fichiers CSV en un seul DataFrame pandas


data["VN"] = (data["VP"] + data["FP"] + data["FN"]) * 2  # Calcule le VN

# Graphique 1 : Proportions de VP, FP, FN, VN
plt.figure(figsize=(12, 10)) # définition de la taille du graphique
data_melted = data.melt(id_vars=["Auteur", "Fichier", "OCR"], value_vars=["VP", "FP", "FN", "VN"], var_name="Type", value_name="Nombre") #transformation des données pour un affichage adapté au diagramme en barres 


# Création du diagramme en barres empilées


sns.barplot(x="OCR", y="Nombre", hue="Type", data=data_melted, ci=None)

# Ajout du titre et des étiquettes des axes
plt.title("Proportions de VP, FP, FN et VN par OCR")
plt.xlabel("Système OCR")
plt.ylabel("Nombre d'annotations")
plt.legend(title="Type d'entité")
plt.xticks(rotation=45) # rotation des noms des systèmes OCR 
plt.savefig(f"{dossier_graphiques}/proportions_globales",bbox_inches='tight') # sauvegarde du graphique
plt.show() #affichage du grpahique


# Graphique 2 : Comparaison des scores par OCR et Auteur
plt.figure(figsize=(12, 6)) #définition de la taille du graphique
for metric in ["Précision", "Rappel", "F-score"]: # Création d'un graphique en ligne pour chaque métrique (Précision, Rappel, F-score)
    sns.lineplot(x="Auteur", y=metric, hue="OCR", data=data, marker="o")
    # ajout du titre et des étiquettes des axes
    plt.title(f"Comparaison de {metric} par OCR et Auteur")
    plt.xlabel("Auteur")
    plt.ylabel(metric)
    plt.legend(title="OCR")
    plt.xticks(rotation=45)
    plt.savefig(f"{dossier_graphiques}/Comparaison_{metric}_OCRetAuteur",bbox_inches='tight') #saugarde 
    plt.show() #affichage
