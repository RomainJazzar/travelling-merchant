# Le marchand ambulant — TSP

Projet d'algorithmique autour du **problème du voyageur de commerce (TSP)** sur 20 villes françaises.

## Objectif

Construire un graphe complet pondéré à partir des coordonnées GPS des 20 villes, calculer les distances avec la formule de **Haversine**, puis comparer deux approches :

1. **Christofides** : approximation déterministe adaptée au TSP métrique.
2. **Algorithme génétique** : recherche stochastique basée sur une population de tournées.

Le programme génère automatiquement les itinéraires, les distances, les cartes HTML, les graphiques PNG et un benchmark de plusieurs configurations génétiques.

## Données

Le fichier `data/villes_france_lat_long.csv` contient 20 villes françaises avec latitude et longitude.

La distance entre deux villes est calculée par la formule de Haversine :

`d = 2R × asin(sqrt(sin²(Δφ/2) + cos(φ1)cos(φ2)sin²(Δλ/2)))`

avec `R = 6371.0088 km`.

## Structure du projet

```text
travelling-merchant/
├── data/
│   └── villes_france_lat_long.csv
├── src/
│   ├── core.py
│   ├── christofides.py
│   ├── genetic.py
│   └── visualization.py
├── results/
│   ├── summary.json
│   ├── benchmark_ga.csv
│   ├── route_christofides.html
│   ├── route_genetique.html
│   ├── route_christofides.png
│   ├── route_genetique.png
│   └── convergence_genetique.png
├── main.py
├── requirements.txt
├── SUIVI_PROJET.md
├── PRESENTATION_ORALE.md
└── README.md
```

## Installation et exécution

```bash
python -m venv .venv
```

Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Linux/macOS :

```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Pour afficher le résumé complet :

```bash
python main.py --json
```

## 1. Modélisation

Chaque ville est un sommet. Le graphe est **complet** : chaque paire de villes possède une arête dont le poids est la distance de Haversine. Comme cette distance est métrique, elle respecte notamment l'inégalité triangulaire, ce qui rend Christofides pertinent.

## 2. Algorithme de Christofides

Implémentation dans `src/christofides.py` :

1. Construction d'un arbre couvrant minimal avec **Prim**.
2. Identification des sommets de degré impair.
3. Appariement parfait de poids minimal entre ces sommets.
4. Union de l'arbre et de l'appariement pour obtenir un multigraphe eulérien.
5. Parcours eulérien avec **Hierholzer**.
6. Suppression des sommets déjà visités pour obtenir un cycle hamiltonien.

### Résultat Christofides

- Distance totale : **3445.60 km**
- Poids de l'arbre couvrant minimal : **2665.05 km**
- Poids de l'appariement : **1142.03 km**
- Sommets impairs dans le MST : **12**
- Temps d'exécution observé : **2.26 ms**

Itinéraire :

> Paris → Le Havre → Rennes → Nantes → Angers → Bordeaux → Toulouse → Montpellier → Nîmes → Nice → Toulon → Marseille → Saint-Étienne → Clermont-Ferrand → Lyon → Grenoble → Dijon → Strasbourg → Reims → Lille → Paris

Carte interactive : `results/route_christofides.html`.

## 3. Algorithme génétique

Un individu représente une permutation des villes. Paris est fixé comme point d'ancrage afin d'éviter des représentations équivalentes du même cycle.

### Opérateurs

- **Sélection** : tournoi.
- **Reproduction** : Ordered Crossover (OX).
- **Mutation** : échange de deux villes ou inversion d'un segment.
- **Élitisme** : les meilleurs individus sont conservés d'une génération à la suivante.
- **Fitness** : minimisation de la distance totale de la tournée.

### Configuration retenue

- Population : **160**
- Générations : **520**
- Taille du tournoi : **5**
- Taux de croisement : **95%**
- Taux de mutation : **22%**
- Élite : **6**

Cette configuration a été retenue parce qu'elle obtient la meilleure moyenne et la meilleure stabilité parmi les configurations testées.

### Résultat génétique

- Distance totale : **3157.13 km**
- Meilleur temps d'une exécution observée : **0.861 s**
- Configuration : **equilibree**

Itinéraire :

> Paris → Le Havre → Rennes → Angers → Nantes → Bordeaux → Toulouse → Montpellier → Nîmes → Marseille → Toulon → Nice → Grenoble → Lyon → Saint-Étienne → Clermont-Ferrand → Dijon → Strasbourg → Reims → Lille → Paris

Carte interactive : `results/route_genetique.html`.

## 4. Tests de configurations génétiques

| Configuration | Runs | Meilleure (km) | Moyenne (km) | Écart-type (km) | Pire (km) |
|---|---:|---:|---:|---:|---:|
| rapide | 3 | 3157.13 | 3216.15 | 83.48 | 3334.21 |
| equilibree | 3 | 3157.13 | 3157.13 | 0.00 | 3157.13 |
| exploratoire | 3 | 3157.13 | 3216.15 | 83.48 | 3334.21 |

## 5. Analyse comparative

| Critère | Christofides | Algorithme génétique |
|---|---|---|
| Distance obtenue | **3445.60 km** | **3157.13 km** |
| Écart | — | **288.48 km de moins** |
| Gain relatif du GA | — | **8.37%** |
| Nature | Déterministe | Stochastique |
| Garantie théorique | Oui, au plus 1,5× l'optimum pour un TSP métrique | Aucune garantie d'optimalité |
| Répétabilité | Très forte | Dépend du seed, mais améliorable par répétitions |
| Paramétrage | Faible | Important |
| Temps observé | Très faible | Plus élevé |
| Facilité d'explication | Très bonne | Bonne, mais plus de paramètres |

### Interprétation

Sur ce jeu de données, l'algorithme génétique trouve une tournée **8.37% plus courte** que Christofides. Christofides reste extrêmement rapide, stable et théoriquement encadré. Le génétique obtient ici la meilleure distance, mais demande un choix de paramètres et plusieurs exécutions pour vérifier la robustesse.

## 6. Recommandation

Pour Théobald, je recommande :

- **Christofides** lorsqu'il faut obtenir immédiatement une bonne tournée, déterministe et explicable.
- **L'algorithme génétique** lorsque la priorité est d'améliorer la distance et qu'un temps de calcul un peu supérieur est acceptable.

Dans cette instance de 20 villes, la recommandation finale est **l'algorithme génétique**, car il produit la meilleure tournée observée avec une configuration équilibrée qui s'est montrée stable sur les seeds testés.

## Limites

Le projet compare deux solutions approchées. Il ne calcule pas l'optimum exact du TSP, donc on ne peut pas affirmer que **3157.13 km** est la distance optimale absolue. Les distances sont géodésiques à vol d'oiseau et ne représentent pas la longueur réelle des routes routières.

## Reproductibilité

Le seed du GA est contrôlé. Tous les fichiers de sortie sont régénérés par `python main.py`. Les résultats détaillés sont stockés dans `results/summary.json` et `results/benchmark_ga.csv`.

## Tests automatiques

```bash
python -m unittest discover -s tests -v
```

Les tests vérifient notamment que chaque algorithme renvoie un cycle valide qui visite exactement les 20 villes puis revient au point de départ.
