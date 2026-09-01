# Présentation orale — script conseillé

## Slide 1 — Contexte

> Le problème consiste à aider Théobald à visiter 20 villes françaises une seule fois puis revenir au point de départ, en minimisant la distance totale. C'est un TSP, un problème NP-difficile : une recherche exhaustive devient vite impossible.

## Slide 2 — Modélisation

> J'ai utilisé les coordonnées GPS du CSV. Chaque ville devient un sommet, chaque paire de villes une arête, et le poids est la distance de Haversine. Le graphe est complet et les distances sont métriques.

## Slide 3 — Christofides

> Christofides commence par un arbre couvrant minimal. J'ai implémenté Prim pour cette étape. Je récupère ensuite les sommets de degré impair, je fais un matching parfait de poids minimal, puis j'obtiens un multigraphe eulérien. Après un parcours de Hierholzer, je supprime les répétitions de villes. La tournée obtenue mesure 3445.6 km.

## Slide 4 — Génétique

> Pour le GA, chaque individu est une permutation des villes. La fitness est la distance totale, donc plus elle est faible, meilleur est l'individu. J'utilise une sélection par tournoi, un crossover OX, une mutation swap ou inversion et de l'élitisme.

## Slide 5 — Paramétrage

> J'ai testé trois niveaux de paramétrage et plusieurs seeds. La configuration équilibrée est la plus robuste : 160 individus, 520 générations et 22% de mutation. Elle converge vers 3157.1 km sur les runs de benchmark.

## Slide 6 — Comparaison

> Le GA gagne environ 288.5 km, soit 8.4%. Christofides reste beaucoup plus simple à reproduire et a une garantie théorique. Le GA est plus sensible aux paramètres mais donne ici une meilleure distance.

## Slide 7 — Organisation

> J'ai organisé le travail par blocs : données et modélisation, Christofides, génétique, benchmark et visualisation, puis documentation et slides. Le Trello permet de visualiser ce qui est terminé et ce qui reste à vérifier avant le rendu.

## Slide 8 — Conclusion

> Pour cette instance, je recommande le génétique si la priorité est la distance. Si Théobald avait besoin d'une solution immédiatement reproductible avec une garantie théorique, Christofides serait le choix le plus sûr. Je précise que le GA donne la meilleure solution observée, pas une preuve d'optimalité.
