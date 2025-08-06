# WoodKG

WoodKG est un projet de construction d’un graphe de connaissances reliant la taxonomie botanique et les caractéristiques anatomiques du bois définies par l’IAWA.  
Les données proviennent principalement des échantillons du CEPAM et de la base InsideWood.

## Table des matières

- [Installation](#installation)
- [Fonctionnalités](#fonctionnalités)
- [Usage](#usage)
- [Exemple d'utilisation](#exemple-dutilisation)
- [Technologies utilisées](#technologies-utilisées)

## Installation

Avant de commencer, vous devez télécharger deux ressources importantes :

### 1. XR2RML

Clonez ou téléchargez XR2RML et placez-le dans un dossier nommé `XR2RML/` :

git clone https://github.com/frmichel/morph-xr2rml XR2RML

### 2. WCVP - Taxonomie des plantes

Téléchargez les données taxonomiques du WCVP à l’adresse suivante :

https://sftp.kew.org/pub/data-repositories/WCVP/

Téléchargez le fichier `wccp_dwca.zip`, puis extrayez le fichier `wcvp_taxon.csv` au root du projet.

Découpez ce fichier en sous-fichiers de 100 000 lignes pour faciliter le traitement :

split -l 100000 -d --additional-suffix=.csv wcvp_taxon.csv input/powo/raw/wcvp_part_

## Fonctionnalités

### input

Ce dossier contient toutes les sources de données :
- powo/ : taxonomie WCVP,
- insidewood/ : observations InsideWood,
- cepam_observations/ : observations du CEPAM.

Chaque sous-dossier contient :
- raw/ : fichiers bruts,
- currated/ : versions transformées prêtes à être utilisées.

### output

Contient les graphes RDF générés :
- la taxonomie POWO (powo_taxonomy_*.ttl),
- les observations (InsideWood, CEPAM),
- le thésaurus IAWA.

Un fichier `wrong_taxonid.txt` indique les échantillons pour lesquels aucun identifiant taxonomique n’a été trouvé dans POWO.

### tools

Contient les scripts :
- de transformation des fichiers raw vers currated,
- de génération des fichiers RDF.

### xr2rml

Contient les fichiers de mapping et de configuration nécessaires pour utiliser XR2RML.

## Usage

Lancez le menu principal avec :

## Table des matières
**./menu.sh**

Le menu vous propose différentes options :

1. Generate IAWA thesaurus as JSON  
Transforme les fichiers du thésaurus IAWA de raw vers currated.

2. Generate IAWA thesaurus as RDF  
Génère thesaurus.ttl à partir des fichiers JSON.  
A exécuter après l'option 1.

3. Generate POWO taxonomy as JSON  
Transforme les fichiers taxonomiques WCVP de raw vers currated.

4. Generate POWO taxonomy as RDF  
Génère les fichiers RDF powo_taxonomy_*.ttl à partir des fichiers JSON.

5. Generate CEPAM observations as JSON  
Transforme les observations du CEPAM de raw vers currated.

6. Generate InsideWood observations as JSON  
Transforme les observations d’InsideWood de raw vers currated.

7. Generate observations as RDF  
Demande un fichier .json ou .csv (de type currated) et génère les observations au format RDF.

8. Quit  
Quitte le menu.

## Exemple d'utilisation

Voici un exemple d’exécution complète :

./menu.sh

Puis dans le menu :  
1 → pour générer le thésaurus IAWA JSON  
5 → pour transformer les observations CEPAM  
7 → et entrer ce chemin :

/home/lyam/Bureau/Stage2A/WoodKGL2/input/cepam_observations/currated/CEPAM_feature_net_taxa_and_numbers_homogene.json

## Technologies utilisées

- RDF, Turtle, JSON, CSV  
- SPARQL, ontologies SOSA/SSN  
- XR2RML  
- Bash  
- Python
