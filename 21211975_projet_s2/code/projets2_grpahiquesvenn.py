#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 00:07:16 2025

@author: weronika
Projet S2: Programmation de Modèles Linguistiques (II)
Weronika BIEGOWSKA 21211975

Ex.8: graphiques:  les intersections entre les sorties de REN et les sorties de Part-of-speech tagging ”PROPN” avec des diagrammes de Venn.
"""

'''importe des libraairies necessaires'''
import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import os


# Charger les résultats de la comparaison depuis le fichier JSON
with open('../comp_bio_pos/comparison_biovspos_results.json', 'r', encoding='utf-8') as f:
    resultats_comparaison = json.load(f)
    
'''définition des fonctions'''

# Fonction pour créer un diagramme de Venn
def creer_diagramme_venn(entities_bio, noms_propres_pos, tokens_communs, chemin_sortie, type_ocr, auteur):
    """
    Créer et sauvegarder un diagramme de Venn pour l'intersection des entités BIO et des noms propres POS
    """
    # Créer le diagramme de Venn
    plt.figure(figsize=(6, 6))
    venn2(subsets=(entities_bio - tokens_communs, noms_propres_pos - tokens_communs, tokens_communs),
          set_labels=('Entités BIO', 'Noms Propres POS'))
    plt.title(f"Diagramme de Venn - {type_ocr} - {auteur}")
    
    # Sauvegarder le diagramme de Venn dans un fichier
    chemin_image_venn = f"{chemin_sortie}/venn_{type_ocr}_{auteur}.png"
    plt.savefig(chemin_image_venn)
    plt.show()


'''Répresenttaion graphique'''

# Chemin pour sauvegarder les diagrammes de Venn
chemin_sortie = "../graphiques/diagrammes_venn"
if not os.path.exists(chemin_sortie):
    os.makedirs(chemin_sortie) # créer le répertoire de sortie s'il n'existe pas


# Boucle à travers les résultats et créer les diagrammes de Venn
for auteur, comparaisons_ocr in resultats_comparaison.items():
    for type_ocr, comparaison in comparaisons_ocr.items():
        # Extraire les données pertinentes
        entities_bio = comparaison['entites_nommees_bio']
        noms_propres_pos = comparaison['noms_propres_pos']
        tokens_communs = comparaison['tokens_communs']
        
        # Créer et sauvegarder le diagramme de Venn
        creer_diagramme_venn(entities_bio, noms_propres_pos, tokens_communs, chemin_sortie, type_ocr, auteur)

