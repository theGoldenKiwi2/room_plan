"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, CePro & CMS, 2025"""

# Outil d’annotation de carte (ÉCOLE POLYTECHNIQUE FÉDÉRALE DE LAUSANNE)

© 2025 — **ÉCOLE POLYTECHNIQUE FÉDÉRALE DE LAUSANNE (EPFL)**  
**Développé par :** *Samuel Dubuis* et *Lucile Pinard*  
**CePro & CMS**

---

## Description

Ce script Python permet de **placer des points numérotés ou étiquetés sur une image** (par exemple un plan) à l’aide de la souris.  
Chaque clic enregistre les coordonnées et l’étiquette du point dans un fichier CSV, et génère une **image annotée** finale.

L’outil a été conçu pour faciliter la création de plans de salle à l'EPFL.

---

## Fonctionnalités principales

- Interface simple avec **sélection du mode de numérotation** :
  - `chiffres` → points numérotés 1, 2, 3…
  - `lettres` → points étiquetés A, B, C…
  - `manuel` → saisie manuelle du texte pour chaque point
  - `préfix` → points étiquetés avec un préfixe (ex. “A1”, “A2”, …)
- Sauvegarde automatique dans un **fichier CSV** (`coord.csv`)
- Export d’une **image annotée** (`export.jpg`)
- Possibilité d’**annuler le dernier point** (`u`)
- Fermeture propre avec `Échap (ESC)`
- Forme des points paramétrable (`circle` ou `square`)

---

## Fichiers et chemins

| Élément | Description | Par défaut |
|----------|--------------|-------------|
| `IMG_PATH` | Image de base sur laquelle placer les points | `map/AAC_006.jpg` |
| `CSV_PATH` | Fichier CSV où sont sauvegardées les coordonnées et étiquettes | `coord.csv` |
| `EXPORT_PATH` | Image finale exportée avec annotations | `export.jpg` |
| `FONT_PATH` | Police utilisée pour le texte (TrueType `.ttf`) | `NotoSans-Bold.ttf` |

---

## Format du fichier CSV

Chaque ligne du fichier `coord.csv` contient :  


`x, y, label`


Exemple :

`450, 230, A`
`620, 480, B`
`700, 300, C`

## Utilisation
Préparer le dossier

Place le script dans un dossier contenant :

- séléctionnner l'image dans le dossier "map"

- changer le nom de l'image à la ligne 11 (par ex. map/AAC_006.jpg)

- une police TrueType (.ttf) — par défaut : NotoSans-Bold.ttf

## Dépendances

Installe les dépendances nécessaires avec :

`pip install -r requirements.txt`

 Le module tkinter est inclus par défaut avec Python sur la plupart des systèmes (notamment Ubuntu et macOS).

## Lancer le script
`python3 main.py`

## Choisir le mode de numérotation

Une petite fenêtre s’ouvre :

- Sélectionne un mode (chiffres, lettres, manuel, ou préfix)

- Si tu choisis préfix, saisis le texte à utiliser (ex. “E” → E1, E2, …)

## Annoter l’image

Clique sur les zones où tu veux placer un point.
Appuie sur :

- u → pour annuler le dernier point,

- Échap → pour terminer.

## Résultats

Un fichier coord.csv est généré avec les coordonnées.
Une image annotée export.jpg est enregistrée.


## Crédits

Script développé par :

**Samuel Dubuis, CMS**

**Lucile Pinard, CePro**

(c) 2025 — ECOLE POLYTECHNIQUE FÉDÉRALE DE LAUSANNE (EPFL), CePro & CMS
Tous droits réservés.
