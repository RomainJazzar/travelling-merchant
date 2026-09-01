# Suivi du projet — Le marchand ambulant

Ce fichier est fait pour être ouvert directement dans VS Code pendant le suivi.

---

## Mardi 1er septembre 2026 — quoi dire

### Version courte (30–45 secondes)

> J'ai commencé par récupérer le CSV des 20 villes et vérifier les coordonnées. J'ai modélisé le problème sous forme de graphe complet pondéré, avec les distances calculées par Haversine. J'ai ensuite séparé le projet en deux méthodes : Christofides et l'algorithme génétique. La partie Christofides est structurée autour de Prim, des sommets de degré impair, du matching puis du parcours eulérien. Pour le génétique, j'ai défini la représentation des individus, la sélection par tournoi, le crossover OX, la mutation et l'élitisme. Là, je suis surtout dans la phase de tests et de comparaison des paramètres, puis je finalise les cartes, l'analyse comparative et les slides.

### Si on te demande ce qui est déjà concret

> Le chargement des données et Haversine fonctionnent. Le graphe contient bien les 20 villes. J'ai une première implémentation des deux approches et je garde les résultats dans des fichiers pour pouvoir comparer les distances et les temps d'exécution sans faire ça à la main.

### Si on te demande pourquoi Christofides

> Parce que les distances de Haversine forment un TSP métrique. Christofides est intéressant ici car il est déterministe, rapide, et il a une garantie théorique : sa tournée ne dépasse pas 1,5 fois l'optimum dans le cas métrique.

### Si on te demande ce que tu vas faire avant jeudi

> Je vais terminer le benchmark du génétique avec plusieurs configurations et plusieurs seeds, retenir la configuration la plus stable, générer les deux cartes d'itinéraire, puis faire le tableau de comparaison distance, temps, robustesse et facilité d'implémentation. Ensuite je finalise le README et la présentation.

---

## Jeudi 3 septembre 2026 — quoi dire

### Version courte (45–60 secondes)

> J'ai finalisé les deux méthodes et le benchmark. Christofides donne une tournée de **3445.6 km**. L'algorithme génétique descend à **3157.1 km**, donc environ **8.4% plus court** sur cette instance. J'ai testé trois configurations génétiques sur plusieurs seeds : la configuration équilibrée, avec une population de 160 individus, 520 générations et 22% de mutation, est la plus stable. J'ai aussi généré les cartes des deux itinéraires et la courbe de convergence. Ma conclusion est que Christofides est meilleur pour la rapidité et la garantie théorique, mais ici le génétique est le meilleur choix si l'objectif principal est la distance.

### Résultats à connaître par cœur

- Christofides : **3445.60 km**
- Algorithme génétique : **3157.13 km**
- Gain du génétique : **288.48 km**, soit **8.37%**
- MST : **2665.05 km**
- Configuration GA retenue : population **160**, générations **520**, tournoi **5**, crossover **95%**, mutation **22%**, élite **6**

### Questions probables du formateur

**Pourquoi ne pas tester les (n-1)! chemins ?**  
Avec 20 villes, cela représente 19! tournées possibles si on fixe le point de départ, donc une recherche exhaustive devient irréaliste.

**Pourquoi Haversine et pas la distance euclidienne ?**  
Parce que les données sont des latitudes et longitudes sur la Terre. Haversine estime la distance de grand cercle entre deux coordonnées géographiques.

**Pourquoi fixer Paris dans le chromosome du GA ?**  
Une tournée cyclique reste la même si on la décale. Fixer une ville comme point d'ancrage supprime des représentations redondantes sans changer les solutions possibles.

**Le GA a trouvé l'optimum ?**  
Je ne l'affirme pas. Il a trouvé la meilleure solution observée parmi mes tests, mais contrairement à une résolution exacte, il n'y a pas de preuve que ce soit l'optimum global.

**Pourquoi le génétique peut battre Christofides ?**  
La garantie de Christofides est une borne maximale, pas l'assurance qu'il donne la meilleure tournée. Un GA peut explorer d'autres permutations et trouver une tournée plus courte sur une instance particulière.

**Quelle méthode recommander ?**  
Pour une réponse immédiate et reproductible : Christofides. Pour chercher une meilleure distance sur cette petite instance : le génétique, surtout avec plusieurs exécutions.

---

## Démo rapide pendant le suivi

Dans le terminal VS Code :

```bash
pip install -r requirements.txt
python main.py
```

Puis ouvrir :

- `results/route_christofides.html`
- `results/route_genetique.html`
- `results/convergence_genetique.png`
- `results/benchmark_ga.csv`

Le résumé chiffré complet est dans `results/summary.json`.
