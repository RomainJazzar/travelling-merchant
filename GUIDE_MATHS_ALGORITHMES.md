# Guide complet — comprendre les maths et les algorithmes du projet « Le marchand ambulant »

Ce document part de **zéro**. L'objectif n'est pas seulement de savoir réciter « Christofides, MST, algorithme génétique », mais de comprendre **ce que chaque mot signifie, pourquoi il existe, comment les éléments s'enchaînent et pourquoi on compare ces deux méthodes dans le projet**.

---

# 1. Le problème général : le voyageur de commerce (TSP)

## 1.1 L'idée intuitive

On a plusieurs villes. On veut :

1. partir d'une ville ;
2. visiter **chaque ville une seule fois** ;
3. revenir à la ville de départ ;
4. minimiser la distance totale.

C'est le **Travelling Salesman Problem**, abrégé **TSP**, en français **problème du voyageur de commerce**.

Dans notre projet, il y a **20 villes françaises**.

Une solution est donc un ordre comme :

```text
Paris → Lille → Reims → Strasbourg → ... → Marseille → ... → Paris
```

Le but est de trouver l'ordre dont la somme des distances est la plus petite possible.

---

## 1.2 Pourquoi ce problème devient difficile ?

Avec seulement quelques villes, on pourrait tester toutes les possibilités.

Mais le nombre d'ordres possibles explose très vite.

Pour `n` villes, si on fixe la ville de départ, il reste approximativement `(n-1)!` permutations à tester.

Pour 20 villes :

```text
19! = 121 645 100 408 832 000
```

Donc plus de **121 millions de milliards** de permutations avant même de tenir compte des symétries.

Même un ordinateur très rapide ne veut pas tester naïvement toutes ces tournées.

C'est pour cela qu'on cherche des **algorithmes intelligents**.

---

# 2. Les grandes familles de solutions

Avant Christofides et l'algorithme génétique, il faut comprendre qu'il existe plusieurs catégories de méthodes.

## 2.1 Algorithme exact

Un algorithme exact garantit de trouver **l'optimum global**, c'est-à-dire la meilleure tournée possible.

Exemples :

- brute force ;
- programmation dynamique Held-Karp ;
- branch and bound ;
- méthodes de programmation linéaire entière.

Avantage : résultat optimal garanti.

Inconvénient : le coût de calcul devient énorme quand `n` augmente.

---

## 2.2 Algorithme d'approximation

Un algorithme d'approximation ne promet pas forcément l'optimum, mais donne une **garantie mathématique sur la qualité** de la solution.

Christofides est dans cette catégorie.

Pour un **TSP métrique**, Christofides garantit :

```text
solution_christofides ≤ 1,5 × solution_optimale
```

Donc même dans le pire cas théorique, sa tournée ne dépasse pas 150 % de l'optimum.

---

## 2.3 Heuristique

Une heuristique cherche une bonne solution rapidement, sans garantie mathématique forte.

Exemples :

- nearest neighbor ;
- 2-opt ;
- 3-opt.

Elle peut être excellente en pratique mais mauvaise sur certains cas.

---

## 2.4 Métaheuristique

Une métaheuristique est une stratégie générale d'exploration d'un très grand espace de solutions.

Exemples :

- algorithme génétique ;
- recuit simulé ;
- colonie de fourmis ;
- recherche tabou ;
- particle swarm optimization.

L'**algorithme génétique** de notre projet est donc une **métaheuristique stochastique**.

Il ne donne aucune garantie absolue de trouver l'optimum, mais il peut trouver de très bonnes tournées.

---

# 3. Le vocabulaire des graphes

Le projet transforme les villes en un **graphe**.

C'est le langage mathématique utilisé pour représenter le problème.

---

## 3.1 Graphe

Un graphe est constitué de :

- **sommets** (vertices / nodes) ;
- **arêtes** (edges).

Dans notre projet :

```text
sommet = ville
arête = liaison possible entre deux villes
poids de l'arête = distance entre les deux villes
```

On note souvent un graphe :

```text
G = (V, E)
```

avec :

- `V` = ensemble des sommets ;
- `E` = ensemble des arêtes.

---

## 3.2 Graphe non orienté

Dans un graphe **non orienté**, une arête Paris–Lyon est identique à Lyon–Paris.

C'est notre cas :

```text
distance(Paris, Lyon) = distance(Lyon, Paris)
```

On ne représente donc pas des flèches.

---

## 3.3 Graphe orienté

Dans un graphe orienté, les connexions ont un sens :

```text
A → B
```

n'est pas nécessairement identique à :

```text
B → A
```

Exemple réel : rues à sens unique.

Ce n'est pas le modèle utilisé dans notre projet.

---

## 3.4 Graphe pondéré

Un graphe pondéré associe une valeur à chaque arête.

Dans notre projet :

```text
poids = distance en kilomètres
```

Par exemple :

```text
Paris --465 km-- Lyon
```

---

## 3.5 Graphe complet

Un graphe est **complet** si chaque sommet est relié à tous les autres.

Avec 20 villes, chaque ville peut théoriquement aller directement vers chacune des 19 autres.

Le nombre d'arêtes d'un graphe complet non orienté est :

```text
n(n-1)/2
```

Pour 20 villes :

```text
20 × 19 / 2 = 190 arêtes
```

Notre programme construit précisément ce graphe complet pondéré.

---

## 3.6 Graphe connexe

Un graphe est **connexe** s'il existe un chemin permettant de rejoindre n'importe quel sommet depuis n'importe quel autre.

Un graphe complet est forcément connexe.

---

## 3.7 Degré d'un sommet

Le **degré** d'un sommet est le nombre d'arêtes qui lui sont incidentes.

Exemple :

```text
    B
    |
A---C---D
```

Le sommet `C` a un degré 3.

Dans Christofides, on s'intéresse énormément aux sommets de **degré impair**.

---

# 4. Distance géographique : Haversine

Les villes sont fournies par latitude et longitude.

On ne peut pas simplement utiliser une distance euclidienne `sqrt(dx² + dy²)` comme si la Terre était une feuille plate.

On utilise donc la **formule de Haversine**.

Elle calcule approximativement la distance du plus court arc sur une sphère entre deux points géographiques.

La formule utilisée dans le code est :

```text
h = sin²(Δφ/2)
    + cos(φ1) cos(φ2) sin²(Δλ/2)

d = 2R asin(√h)
```

avec :

- `φ` = latitude en radians ;
- `λ` = longitude en radians ;
- `R ≈ 6371 km` = rayon moyen de la Terre ;
- `d` = distance finale.

Le projet utilise `R = 6371.0088 km`.

---

# 5. Qu'est-ce qu'une métrique ?

C'est fondamental pour comprendre **pourquoi Christofides peut être utilisé**.

Une distance est une métrique si elle respecte notamment :

```text
d(A,B) ≥ 0

d(A,B) = d(B,A)

d(A,A) = 0

d(A,C) ≤ d(A,B) + d(B,C)
```

La dernière propriété s'appelle **l'inégalité triangulaire**.

---

## 5.1 Inégalité triangulaire

Elle dit que le chemin direct ne peut pas être plus long que faire un détour intermédiaire :

```text
A -------- C
 \        /
  \      /
   \ B  /
```

Mathématiquement :

```text
d(A,C) ≤ d(A,B) + d(B,C)
```

Cette propriété permet à Christofides de supprimer des répétitions dans une tournée eulérienne sans rendre la tournée plus longue.

C'est ce qu'on appelle le **shortcutting**.

---

# 6. Chemin, cycle, circuit

## 6.1 Chemin

Une suite de sommets reliés :

```text
A → B → C → D
```

---

## 6.2 Cycle

Un chemin qui revient au point de départ :

```text
A → B → C → D → A
```

Le TSP cherche un cycle particulier : un **cycle hamiltonien**.

---

# 7. Hamiltonien vs eulérien — différence à connaître absolument

C'est probablement l'une des distinctions les plus importantes de tout le projet.

## 7.1 Hamiltonien

Un chemin ou cycle **hamiltonien** s'intéresse aux **sommets**.

Un cycle hamiltonien visite :

```text
chaque SOMMET exactement une fois
```

puis revient au départ.

Le TSP cherche donc le **cycle hamiltonien de poids minimal**.

---

## 7.2 Eulérien

Un chemin ou circuit **eulérien** s'intéresse aux **arêtes**.

Un circuit eulérien parcourt :

```text
chaque ARÊTE exactement une fois
```

et revient au départ.

---

## 7.3 La phrase à retenir

```text
Hamilton = sommets
Euler = arêtes
```

Christofides construit d'abord un graphe eulérien, trouve un circuit eulérien, puis le transforme en cycle hamiltonien.

---

# 8. Les arbres

## 8.1 Arbre en théorie des graphes

Un **arbre** est un graphe :

- connexe ;
- sans cycle.

Exemple :

```text
    B
    |
A---C---D
    |
    E
```

Il relie tous ses sommets mais il n'existe aucune boucle.

---

## 8.2 Propriété importante

Un arbre comportant `n` sommets possède exactement :

```text
n - 1 arêtes
```

Donc avec 20 villes, tout arbre couvrant possède exactement :

```text
19 arêtes
```

---

# 9. Différents types d'arbres

Tous les arbres dont on parle en informatique ne servent pas au projet.

## 9.1 Arbre enraciné (rooted tree)

On désigne un sommet comme racine.

On parle alors de :

- parent ;
- enfant ;
- profondeur ;
- feuille.

Très utilisé en structures de données.

---

## 9.2 Arbre binaire

Chaque nœud possède au maximum deux enfants.

Utilisé dans les arbres binaires de recherche, heaps, etc.

**Ce n'est pas le MST du projet.**

---

## 9.3 Arbre couvrant (spanning tree)

Un arbre couvrant est un sous-graphe qui :

- contient **tous les sommets** du graphe original ;
- est connexe ;
- ne contient aucun cycle.

Exemple : à partir d'un graphe avec énormément d'arêtes, on conserve juste assez de liaisons pour relier toutes les villes sans boucle.

---

# 10. MST : Minimum Spanning Tree

MST signifie :

```text
Minimum Spanning Tree
```

En français :

```text
arbre couvrant de poids minimal
```

Il faut distinguer :

```text
Spanning Tree = n'importe quel arbre couvrant
MST = l'arbre couvrant dont la somme des poids est minimale
```

---

## 10.1 Exemple simple

Imaginons :

```text
A--1--B
|    / |
4   2  5
| /    |
C--3--D
```

On cherche les arêtes qui relient tous les sommets, sans cycle, avec la somme minimale.

Si on choisit :

```text
A-B = 1
B-C = 2
C-D = 3
```

poids total :

```text
1 + 2 + 3 = 6
```

Si aucun autre arbre couvrant ne coûte moins, c'est le MST.

---

# 11. Pourquoi le MST est utile au TSP ?

C'est une idée mathématique magnifique et très importante.

Une tournée TSP optimale est un cycle :

```text
A → B → C → D → A
```

Si on retire **une seule arête** de ce cycle, on obtient un arbre couvrant.

Or le MST est, par définition, le meilleur arbre couvrant possible.

Donc :

```text
poids(MST) ≤ poids(TSP optimal)
```

Le MST donne donc une **borne inférieure** de l'optimum du TSP.

Dans notre projet :

```text
MST ≈ 2665,05 km
```

alors que :

```text
Christofides ≈ 3445,60 km
GA ≈ 3157,13 km
```

Le MST n'est pas lui-même une tournée TSP parce qu'il ne revient pas forcément au départ et les degrés des sommets ne sont pas nécessairement 2.

---

# 12. Prim : comment trouver un MST

Notre projet utilise **l'algorithme de Prim**.

Principe :

1. partir d'un sommet ;
2. regarder les arêtes qui relient l'arbre actuel à un sommet encore non visité ;
3. prendre la moins chère ;
4. ajouter le nouveau sommet ;
5. recommencer jusqu'à avoir tous les sommets.

Image mentale :

```text
on fait pousser un arbre, branche après branche,
en prenant toujours la connexion disponible la moins chère.
```

---

# 13. Prim vs Kruskal

Les deux servent à calculer un MST.

## Prim

Il fait grandir **un seul arbre connecté** depuis un sommet initial.

Très intuitif pour un graphe dense comme notre graphe complet.

## Kruskal

Il trie toutes les arêtes par poids puis les ajoute de la moins chère à la plus chère, tant qu'elles ne créent pas de cycle.

Au début, il peut y avoir plusieurs petits arbres séparés qui finissent par fusionner.

## Résultat

Les deux cherchent un MST.

Ils peuvent produire des arbres différents si plusieurs MST ont exactement le même poids, mais leur poids minimal est identique.

---

# 14. Attention : MST ≠ plus court chemin

C'est une confusion classique.

**Prim / Kruskal** :

```text
objectif = connecter tous les sommets avec un coût total minimal
```

**Dijkstra** :

```text
objectif = trouver le plus court chemin depuis une source vers les autres sommets
```

Ce sont deux problèmes complètement différents.

Un arbre des plus courts chemins n'est pas forcément un MST.

---

# 15. Pourquoi les degrés impairs posent problème ?

Un théorème d'Euler dit qu'un graphe connexe possède un **circuit eulérien** si tous ses sommets ont un degré **pair**.

Dans un MST, certains sommets ont souvent un degré impair.

Exemple :

```text
A---B---C
    |
    D
```

`B` a degré 3 : impair.

Donc on ne peut pas forcément parcourir toutes les arêtes exactement une fois et revenir au départ.

Christofides doit réparer ce problème.

---

# 16. Pourquoi le nombre de sommets impairs est toujours pair ?

C'est le **lemme de la poignée de main**.

Dans n'importe quel graphe non orienté :

```text
somme des degrés = 2 × nombre d'arêtes
```

Donc la somme des degrés est toujours paire.

Cela implique que le nombre de sommets de degré impair est forcément pair.

C'est pratique : on peut donc les mettre par paires.

Dans notre MST, il y en a **12**.

---

# 17. Matching

Un **matching** est un ensemble d'arêtes qui ne partagent pas de sommet.

Exemple :

```text
A---B    C---D
```

On a apparié A avec B et C avec D.

---

# 18. Perfect matching

Un **perfect matching** ou **couplage parfait** apparie **tous** les sommets concernés exactement une fois.

Si les sommets impairs sont :

```text
A, B, C, D
```

un perfect matching pourrait être :

```text
A-B
C-D
```

ou :

```text
A-C
B-D
```

etc.

---

# 19. Minimum-weight perfect matching

Christofides ne choisit pas n'importe quel couplage parfait.

Il cherche celui dont la somme des distances est la plus faible.

Donc :

```text
minimum-weight perfect matching
= couplage parfait de poids minimal
```

Dans notre projet, le matching des sommets impairs pèse environ :

```text
1142,03 km
```

---

# 20. Pourquoi ajouter le matching au MST ?

Chaque sommet impair du MST reçoit exactement **une nouvelle arête** du matching.

Un degré impair + 1 devient pair.

Exemples :

```text
1 → 2
3 → 4
5 → 6
```

Tous les sommets impairs deviennent pairs.

Les sommets déjà pairs restent pairs.

On obtient ainsi un graphe :

- connexe ;
- dont tous les degrés sont pairs.

Donc il possède un **circuit eulérien**.

---

# 21. Multigraphe

Quand on combine le MST et le matching, il est possible que certaines liaisons apparaissent plusieurs fois.

Un graphe qui autorise plusieurs arêtes entre la même paire de sommets est un **multigraphe**.

Christofides travaille donc temporairement sur un multigraphe eulérien.

---

# 22. Algorithme de Hierholzer

Une fois le multigraphe eulérien construit, il faut trouver un circuit qui traverse chaque arête exactement une fois.

Notre projet utilise **Hierholzer**.

Principe intuitif :

1. partir d'un sommet ;
2. suivre des arêtes non utilisées jusqu'à revenir ;
3. s'il reste des arêtes non utilisées sur le circuit, créer un nouveau sous-circuit ;
4. fusionner les circuits.

Le résultat est un **circuit eulérien**.

---

# 23. Mais le TSP veut un cycle hamiltonien !

Exactement.

Le circuit eulérien peut répéter plusieurs fois la même ville parce qu'il doit parcourir toutes les arêtes du multigraphe.

Exemple :

```text
Paris → Lyon → Paris → Marseille → Nice → Lyon → ...
```

Le TSP interdit ces répétitions.

On effectue donc un **shortcut**.

---

# 24. Shortcutting

On parcourt le circuit eulérien et on ignore les villes déjà visitées.

Exemple :

```text
A → B → C → B → D → A
```

`B` apparaît deux fois.

On peut transformer en :

```text
A → B → C → D → A
```

Pourquoi cela ne rallonge-t-il pas la tournée ?

Grâce à l'inégalité triangulaire :

```text
d(C,D) ≤ d(C,B) + d(B,D)
```

Donc sauter une répétition ne peut pas augmenter le coût.

C'est précisément pour cela que Christofides exige un **TSP métrique**.

---

# 25. Christofides complet, étape par étape

L'algorithme utilisé dans notre projet fait exactement ceci :

```text
1. Construire le graphe complet pondéré
2. Calculer un MST avec Prim
3. Repérer les sommets de degré impair dans le MST
4. Calculer un minimum-weight perfect matching entre ces sommets
5. Fusionner MST + matching
6. Tous les degrés sont maintenant pairs
7. Trouver un circuit eulérien avec Hierholzer
8. Supprimer les répétitions grâce au shortcutting
9. Fermer le cycle
10. Calculer la distance finale
```

C'est le cœur mathématique de Christofides.

---

# 26. Pourquoi Christofides a une garantie de 1,5 ?

On note `OPT` la distance de la meilleure tournée TSP possible.

## Partie 1 : MST

On sait :

```text
MST ≤ OPT
```

## Partie 2 : matching

On peut montrer que le meilleur matching des sommets impairs ne coûte pas plus de la moitié de l'optimum :

```text
matching ≤ 0,5 × OPT
```

## Partie 3 : addition

Donc :

```text
MST + matching ≤ 1,5 × OPT
```

Le circuit eulérien utilise exactement ces arêtes.

Et grâce à l'inégalité triangulaire, le shortcutting n'augmente pas la distance.

Donc :

```text
Christofides ≤ 1,5 × OPT
```

C'est cette preuve qui rend Christofides beaucoup plus qu'une simple heuristique.

---

# 27. Pourquoi choisir Christofides dans le projet ?

Parce qu'il donne un excellent **point de référence théorique**.

Il est :

- déterministe dans notre utilisation ;
- rapide sur 20 villes ;
- mathématiquement justifiable ;
- fondé sur plusieurs concepts classiques de théorie des graphes ;
- garanti à 1,5 fois l'optimum au maximum pour un TSP métrique.

Il fournit donc une solution « sérieuse » avec garantie théorique à laquelle on peut comparer une méthode d'intelligence artificielle / optimisation stochastique.

---

# 28. Déterministe vs stochastique

## Déterministe

Même entrée + mêmes règles → même résultat.

Christofides est essentiellement déterministe dans notre projet.

## Stochastique

Un algorithme utilise du hasard.

Deux exécutions peuvent produire des résultats différents.

L'algorithme génétique est stochastique.

C'est pour cela qu'on le teste avec plusieurs **seeds**.

---

# 29. Algorithme génétique : idée générale

Un algorithme génétique s'inspire de l'évolution biologique.

On ne construit pas directement une seule tournée.

On crée une **population de nombreuses tournées candidates**.

Puis on répète :

```text
évaluer → sélectionner → croiser → muter → conserver les meilleurs
```

Après de nombreuses générations, la population tend à contenir de meilleures solutions.

---

# 30. Individu, chromosome et gène

Dans notre TSP :

```text
individu = une tournée candidate
chromosome = permutation des villes
un gène = une ville
```

Le projet fixe Paris (index 0) comme ancre de départ et d'arrivée.

Par exemple :

```text
chromosome = [Lyon, Lille, Marseille, Bordeaux]
```

correspond à :

```text
Paris → Lyon → Lille → Marseille → Bordeaux → Paris
```

---

# 31. Pourquoi une permutation ?

Parce qu'on doit visiter chaque ville exactement une fois.

Une permutation garantit que chaque identifiant de ville apparaît une fois dans le chromosome.

Il faut donc utiliser des opérations génétiques qui conservent cette propriété.

Un crossover classique utilisé pour des nombres binaires pourrait créer :

```text
A, B, B, D
```

avec une ville dupliquée et une autre absente.

Ce serait invalide pour le TSP.

---

# 32. Population

La population est l'ensemble des solutions candidates à une génération donnée.

Dans notre configuration équilibrée :

```text
population_size = 160
```

Donc l'algorithme entretient 160 tournées candidates à la fois.

Population plus grande :

- plus de diversité ;
- plus d'exploration ;
- plus de calcul.

Population trop petite :

- rapide ;
- risque de perdre rapidement de la diversité ;
- risque de convergence prématurée.

---

# 33. Génération

Une génération correspond à une itération complète de l'évolution.

Dans notre configuration équilibrée :

```text
generations = 520
```

Cela signifie que l'on renouvelle la population 520 fois.

---

# 34. Fonction objectif / fitness

Il faut mesurer la qualité d'un individu.

Dans notre projet, on calcule simplement la distance totale de la tournée.

Objectif :

```text
minimiser distance(route)
```

Une tournée plus courte est meilleure.

Dans certains algorithmes génétiques, on transforme la distance en fitness :

```text
fitness = 1 / distance
```

Mais notre implémentation compare directement les distances.

---

# 35. Sélection par tournoi

Pour créer les futurs enfants, il faut choisir des parents.

Notre projet utilise la **tournament selection**.

Avec :

```text
tournament_size = 5
```

on :

1. tire 5 individus au hasard ;
2. compare leurs distances ;
3. choisit le meilleur des 5 comme parent.

Cela crée une **pression de sélection**.

Les bons individus ont plus de chances de se reproduire, mais les autres ne sont pas totalement exclus.

---

# 36. Pression de sélection

Si la pression est trop faible :

- l'évolution est lente ;
- trop de mauvaises solutions se reproduisent.

Si elle est trop forte :

- les meilleurs dominent immédiatement ;
- la diversité disparaît ;
- la population risque de converger vers un optimum local.

Le `tournament_size` contrôle en partie cette pression.

---

# 37. Crossover / croisement

Le crossover combine deux parents pour produire des enfants.

Notre projet utilise **Ordered Crossover (OX)**.

C'est spécialement adapté aux permutations.

---

# 38. Ordered Crossover (OX)

Exemple :

```text
Parent 1 : A B C D E F G H
Parent 2 : D F B H A C E G
```

On choisit une zone dans Parent 1, par exemple :

```text
C D E
```

On conserve cette zone dans l'enfant puis on remplit les cases restantes dans l'ordre fourni par Parent 2, en ignorant les éléments déjà présents.

Ainsi :

- aucune ville n'est perdue ;
- aucune ville n'est dupliquée ;
- une partie de l'ordre des parents est conservée.

Dans notre configuration :

```text
crossover_rate = 0.95
```

Donc environ 95 % des couples de parents subissent un crossover.

---

# 39. Mutation

Le crossover recombine l'information existante.

La mutation crée de nouvelles variations.

Sans mutation, une population peut devenir trop homogène et rester bloquée.

Notre projet mélange deux mutations :

## Swap mutation

On échange deux villes.

```text
A B C D E
↓
A D C B E
```

## Inversion mutation

On inverse une portion.

```text
A B C D E F
```

si on inverse `B C D E` :

```text
A E D C B F
```

L'inversion est particulièrement intéressante pour le TSP car elle peut supprimer des croisements inutiles dans une tournée.

---

# 40. Mutation rate

Dans notre configuration :

```text
mutation_rate = 0.22
```

Cela signifie qu'un enfant a 22 % de chances de subir une mutation.

Trop faible : manque de diversité.

Trop élevée : l'évolution ressemble presque à une recherche aléatoire et détruit les bonnes structures.

---

# 41. Élitisme

L'élitisme consiste à copier directement les meilleurs individus dans la génération suivante.

Dans notre configuration :

```text
elite_size = 6
```

Donc les 6 meilleures tournées survivent sans modification.

Avantage : on ne perd jamais accidentellement les meilleures solutions trouvées.

Inconvénient potentiel : trop d'élitisme réduit la diversité.

---

# 42. Exploration vs exploitation

C'est une notion générale très importante en optimisation.

## Exploration

Tester de nouvelles régions de l'espace de recherche.

Favorisée par :

- population grande ;
- mutation ;
- hasard ;
- diversité.

## Exploitation

Améliorer les bonnes solutions déjà trouvées.

Favorisée par :

- sélection ;
- élitisme ;
- crossover entre bons individus.

Un bon algorithme génétique doit équilibrer les deux.

---

# 43. Optimum global vs optimum local

## Optimum global

La meilleure solution de **tout l'espace de recherche**.

## Optimum local

Une solution meilleure que les solutions voisines, mais pas forcément meilleure que tout ce qui existe ailleurs.

Image mentale :

```text
      global
        /\
       /  \
  /\  /    \
 /  \/      \
local
```

Un algorithme génétique peut se bloquer autour d'un optimum local si la population perd trop de diversité.

---

# 44. Convergence

On dit que l'algorithme converge lorsque les meilleures distances cessent de s'améliorer significativement.

Notre programme enregistre la meilleure distance à chaque génération dans `history`.

Cela produit le graphique :

```text
results/convergence_genetique.png
```

Une courbe qui descend puis se stabilise signifie que l'algorithme a progressivement amélioré la solution avant d'atteindre un plateau.

---

# 45. Seed / graine aléatoire

Un ordinateur ne produit généralement pas du hasard véritable pour ce type de programme : il utilise un générateur pseudo-aléatoire.

Une **seed** initialise ce générateur.

Avec la même seed, on peut reproduire la même séquence pseudo-aléatoire.

Notre benchmark utilise :

```text
11
22
33
```

Pourquoi plusieurs seeds ?

Parce qu'un algorithme génétique ne doit pas être jugé sur un seul coup de chance.

---

# 46. Benchmark

Un benchmark consiste à comparer plusieurs configurations de manière contrôlée.

Notre projet teste :

```text
rapide
équilibrée
exploratoire
```

avec plusieurs seeds.

Pour chaque configuration, on regarde :

- meilleur résultat ;
- moyenne ;
- écart-type ;
- pire résultat.

---

# 47. Moyenne

La moyenne est :

```text
(x1 + x2 + ... + xn) / n
```

Elle mesure la performance moyenne d'une configuration.

Si trois runs donnent :

```text
3150, 3200, 3250 km
```

la moyenne vaut :

```text
3200 km
```

---

# 48. Écart-type

L'écart-type mesure la dispersion des résultats.

Petit écart-type : résultats réguliers et stables.

Grand écart-type : résultats très variables selon le hasard.

Dans nos résultats, la configuration équilibrée a obtenu la même meilleure distance sur les trois seeds du benchmark, donc :

```text
std = 0
```

sur ces trois exécutions précises.

Attention : cela ne prouve pas qu'elle donnera toujours exactement le même résultat pour toutes les seeds possibles.

---

# 49. Les trois configurations de notre projet

## Rapide

```text
population = 80
générations = 220
tournoi = 4
mutation = 18 %
élite = 4
```

But : réduire le temps de calcul.

## Équilibrée

```text
population = 160
générations = 520
tournoi = 5
crossover = 95 %
mutation = 22 %
élite = 6
```

But : compromis entre coût de calcul, exploration et stabilité.

## Exploratoire

```text
population = 240
générations = 800
tournoi = 6
mutation = 30 %
élite = 8
```

But : explorer davantage, au prix d'un temps de calcul plus élevé.

Dans le benchmark actuel, le programme choisit la configuration **équilibrée** selon :

```text
1. meilleure moyenne
2. puis plus faible écart-type
3. puis meilleur minimum
```

---

# 50. Pourquoi l'algorithme génétique dans ce projet ?

Parce qu'il représente une approche très différente de Christofides.

Christofides dit en substance :

```text
« Je vais exploiter des théorèmes de graphes et construire méthodiquement une tournée avec une garantie. »
```

L'algorithme génétique dit :

```text
« Je vais faire évoluer une grande population de tournées et chercher empiriquement une excellente solution. »
```

L'un est surtout **théorique et constructif**.

L'autre est **stochastique, expérimental et adaptatif**.

Comparer les deux est donc pédagogiquement intéressant.

---

# 51. Résultats actuels du projet

Le résultat généré actuellement est :

```text
Christofides : 3445,60 km
Algorithme génétique : 3157,13 km
Différence : -288,48 km
Amélioration du GA par rapport à Christofides : environ 8,37 %
```

Le MST pèse :

```text
2665,05 km
```

Le matching pèse :

```text
1142,03 km
```

et le MST possède :

```text
12 sommets de degré impair
```

---

# 52. Important : 3157,13 km n'est pas forcément l'optimum global

Le fait que l'algorithme génétique trouve une tournée meilleure que Christofides ne signifie pas :

```text
GA = optimum exact
```

Cela signifie seulement :

```text
meilleure solution observée par notre expérience = 3157,13 km
```

Pour prouver que c'est l'optimum global, il faudrait utiliser une méthode exacte ou disposer d'une preuve mathématique correspondante.

---

# 53. Pourquoi Christofides peut être moins bon ici alors qu'il a une garantie ?

Une garantie de 1,5 n'affirme pas que Christofides trouvera l'optimum.

Elle affirme seulement qu'il ne fera pas arbitrairement mauvais :

```text
C ≤ 1,5 OPT
```

Si l'optimum était, par exemple, 3150 km, Christofides aurait le droit théorique d'aller jusqu'à :

```text
4725 km
```

et resterait dans sa garantie.

Notre 3445,60 km est donc parfaitement compatible avec la théorie.

---

# 54. Pourquoi le GA peut battre Christofides ?

Christofides suit une construction spécifique :

```text
MST → matching → Euler → shortcut
```

Il ne cherche pas ensuite toutes les modifications possibles du cycle final.

Le GA, lui, explore directement de nombreuses permutations de villes.

Il peut donc découvrir un ordre plus court pour cette instance particulière.

En revanche, il n'offre pas la même garantie dans le pire cas.

---

# 55. Tableau mental : Christofides vs génétique

| Élément | Christofides | Algorithme génétique |
|---|---|---|
| Type | approximation | métaheuristique |
| Hasard | non / très peu selon implémentation | oui |
| Garantie théorique | oui, ≤ 1,5 OPT pour TSP métrique | non |
| Répétabilité | forte | dépend de la seed |
| Vitesse | très rapide ici | plus coûteux |
| Paramètres | peu | beaucoup |
| Base mathématique | graphes, MST, matching, Euler | évolution, probabilités, optimisation |
| Solution actuelle | 3445,60 km | 3157,13 km |
| Peut prouver l'optimum ? | non | non |

---

# 56. Complexité — notion de base

La complexité décrit comment le temps ou la mémoire d'un algorithme évolue lorsque la taille `n` du problème augmente.

On utilise la notation **Big O**.

Exemples :

```text
O(n)        linéaire
O(n log n)  quasi linéaire
O(n²)       quadratique
O(2^n)      exponentielle
O(n!)       factorielle
```

Le brute force du TSP est de nature factorielle, ce qui explique son explosion.

---

# 57. Complexité intuitive du GA

Si on note :

```text
P = taille de population
G = nombre de générations
n = nombre de villes
```

il faut évaluer approximativement `P` tournées à chaque génération, chaque tournée coûtant environ `O(n)` à mesurer.

Donc une intuition simple du coût est :

```text
O(G × P × n)
```

sans compter les coûts supplémentaires de tri, sélection et crossover.

Le GA est donc contrôlable : on décide combien de ressources on veut investir via ses paramètres.

---

# 58. Matrice de distances

Notre programme pré-calcule toutes les distances dans une **matrice de distances**.

Pour quatre villes :

```text
       A    B    C    D
A      0   10   20   30
B     10    0   15   22
C     20   15    0   12
D     30   22   12    0
```

Comme la distance est symétrique :

```text
matrix[i][j] = matrix[j][i]
```

et la diagonale vaut zéro :

```text
matrix[i][i] = 0
```

Cela évite de recalculer Haversine des milliers ou millions de fois pendant le GA.

---

# 59. Route fermée

Une tournée TSP doit finir là où elle commence.

Dans le code du GA :

```text
route = [0] + individual + [0]
```

Donc Paris est ajouté au début et à la fin.

Une liste de 20 villes distinctes devient ainsi une route comportant 21 positions parce que la ville initiale apparaît également comme destination finale.

---

# 60. Pourquoi fixer Paris ?

Un cycle :

```text
Paris → Lyon → Nice → Paris
```

est le même cycle que :

```text
Lyon → Nice → Paris → Lyon
```

Fixer une ville de départ supprime une partie des représentations redondantes.

Cela simplifie le chromosome sans changer le problème réel.

---

# 61. Symétrie d'une tournée

Dans un TSP symétrique :

```text
A → B → C → D → A
```

et :

```text
A → D → C → B → A
```

ont la même distance.

Ce sont la même tournée parcourue dans les deux sens.

---

# 62. Sous-graphe

Un sous-graphe est obtenu en prenant seulement une partie des sommets et/ou des arêtes d'un graphe.

Le MST est un **sous-graphe** du graphe complet.

Le graphe des sommets impairs utilisé pour le matching est également un sous-graphe construit spécifiquement.

---

# 63. Borne inférieure et borne supérieure

## Borne inférieure

Une valeur dont on sait que l'optimum ne peut pas être inférieur.

Le MST fournit une borne inférieure simple :

```text
MST ≤ OPT
```

## Borne supérieure

La distance de n'importe quelle tournée valide donne une borne supérieure :

```text
OPT ≤ distance_tournée_connue
```

Donc avec nos résultats :

```text
2665,05 ≤ OPT ≤ 3157,13
```

puisque 3157,13 km est une tournée valide trouvée par le GA.

Cela ne signifie pas que l'optimum est proche de 2665 : le MST est simplement une borne inférieure.

---

# 64. Notion de solution faisable

Une solution est **faisable** si elle respecte toutes les contraintes.

Pour notre TSP :

- chaque ville est visitée une fois ;
- on revient au départ ;
- seules des liaisons valides sont utilisées.

Une permutation contenant deux fois Marseille et zéro fois Lyon serait **invalide**.

---

# 65. Fonction coût

La fonction coût est la valeur que l'on veut minimiser.

Ici :

```text
coût(route) = somme des distances entre villes consécutives
```

Si :

```text
A → B → C → A
```

alors :

```text
coût = d(A,B) + d(B,C) + d(C,A)
```

---

# 66. Pourquoi pas simplement aller toujours vers la ville la plus proche ?

Cette méthode s'appelle souvent **nearest neighbor**.

Elle semble logique localement :

```text
« à chaque étape, je choisis la ville restante la plus proche »
```

Mais un bon choix local peut provoquer une très mauvaise fin de tournée.

C'est la différence entre :

```text
optimum local / décision gloutonne
```

et :

```text
optimum global
```

Le TSP est justement difficile parce que les décisions interagissent à l'échelle de toute la tournée.

---

# 67. Algorithme glouton

Un algorithme glouton choisit à chaque étape ce qui semble immédiatement le meilleur.

Prim possède une stratégie gloutonne qui fonctionne parfaitement pour le problème du MST grâce aux propriétés mathématiques du MST.

Mais appliquer un comportement glouton naïf au TSP ne garantit pas l'optimum.

Important :

```text
« glouton » ne signifie pas automatiquement « mauvais ».
```

Cela dépend du problème et de la preuve mathématique disponible.

---

# 68. Ce qu'il faut être capable d'expliquer à l'oral

Si le formateur demande « qu'est-ce que vous avez fait ? », une réponse solide serait :

> On a modélisé les 20 villes sous forme d'un graphe complet non orienté et pondéré. Chaque ville est un sommet et chaque arête porte une distance calculée avec Haversine. On compare ensuite deux stratégies pour résoudre approximativement le TSP. Christofides utilise un MST calculé par Prim, corrige les degrés impairs par un matching parfait minimum, construit un multigraphe eulérien, utilise Hierholzer puis shortcut les répétitions pour obtenir un cycle hamiltonien. En parallèle, l'algorithme génétique représente une tournée par une permutation, fait évoluer une population avec sélection par tournoi, Ordered Crossover, mutation et élitisme. On compare enfin les distances, temps et stabilité sur plusieurs seeds.

---

# 69. Questions pièges et réponses

## « Le MST est-il la solution du TSP ? »

Non. Le MST connecte toutes les villes sans cycle et avec 19 arêtes. Le TSP exige un cycle qui revient au départ.

## « Pourquoi ne pas garder simplement MST + matching ? »

Parce que cela donne un multigraphe eulérien, pas encore un cycle hamiltonien. Il faut parcourir son circuit eulérien puis supprimer les répétitions.

## « Pourquoi les sommets impairs ? »

Parce qu'un circuit eulérien nécessite que tous les sommets aient un degré pair.

## « Pourquoi un matching parfait ? »

Pour ajouter exactement une arête à chaque sommet impair et ainsi rendre tous leurs degrés pairs.

## « Pourquoi le matching doit-il être minimum ? »

Parce qu'on veut rendre le graphe eulérien en ajoutant le moins de distance possible et conserver la garantie théorique de Christofides.

## « Pourquoi Haversine ? »

Parce que les données sont géographiques et qu'on veut mesurer une distance sur la surface terrestre plutôt qu'une distance cartésienne naïve latitude/longitude.

## « Pourquoi le GA n'est-il pas exact ? »

Parce qu'il n'explore pas toutes les permutations et n'apporte aucune preuve que la meilleure tournée découverte est l'optimum global.

## « Pourquoi plusieurs seeds ? »

Parce que le GA est stochastique. Une seule exécution peut être exceptionnellement bonne ou mauvaise.

## « Pourquoi l'écart-type ? »

Pour mesurer la stabilité des résultats entre plusieurs runs.

## « Pourquoi le GA bat Christofides ? »

Parce que la garantie de Christofides n'est pas une garantie d'optimalité. Le GA a exploré des permutations qui donnent une meilleure tournée sur cette instance.

## « Est-ce que le GA à 3157,13 km a trouvé l'optimum ? »

On ne peut pas l'affirmer. C'est seulement la meilleure solution observée actuellement.

---

# 70. Schéma global à mémoriser

```text
CSV latitude / longitude
        │
        ▼
Haversine
        │
        ▼
Matrice de distances
        │
        ▼
Graphe complet pondéré
        │
        ├───────────────────────────────┐
        │                               │
        ▼                               ▼
CHRISTOFIDES                     ALGORITHME GÉNÉTIQUE
        │                               │
        ▼                               ▼
MST avec Prim                   Population aléatoire
        │                               │
        ▼                               ▼
Sommets impairs                 Évaluation distance
        │                               │
        ▼                               ▼
Matching parfait min.           Sélection tournoi
        │                               │
        ▼                               ▼
MST + matching                  Crossover OX
        │                               │
        ▼                               ▼
Multigraphe eulérien            Mutation
        │                               │
        ▼                               ▼
Hierholzer                      Élitisme
        │                               │
        ▼                               ▼
Circuit eulérien                Génération suivante
        │                               │
        ▼                               │
Shortcut                        répété 520 fois
        │                               │
        ▼                               ▼
Cycle hamiltonien               Meilleure tournée
        │                               │
        └──────────────┬────────────────┘
                       ▼
              Comparaison finale
```

---

# 71. Les 20 mots à connaître absolument

| Terme | Définition ultra-courte |
|---|---|
| TSP | visiter toutes les villes une fois et revenir en minimisant la distance |
| Graphe | sommets + arêtes |
| Sommet | ici, une ville |
| Arête | liaison entre deux villes |
| Poids | ici, distance en km |
| Graphe complet | chaque ville reliée à toutes les autres |
| Métrique | distance respectant notamment l'inégalité triangulaire |
| Cycle hamiltonien | passe une fois par chaque sommet |
| Circuit eulérien | passe une fois par chaque arête |
| Arbre | graphe connexe sans cycle |
| Spanning tree | arbre contenant tous les sommets |
| MST | spanning tree de poids minimal |
| Prim | algorithme pour calculer un MST |
| Degré | nombre d'arêtes incidentes à un sommet |
| Matching | ensemble d'arêtes sans sommets partagés |
| Perfect matching | matching couvrant tous les sommets concernés |
| Hierholzer | trouve un circuit eulérien |
| Chromosome | représentation d'une solution dans le GA |
| Crossover | combinaison de deux parents |
| Mutation | modification aléatoire d'une solution |

---

# 72. Version ultra-courte à retenir avant un suivi

```text
On résout un TSP sur 20 villes.
Les villes deviennent les sommets d'un graphe complet pondéré.
Les poids sont des distances Haversine.

Christofides :
MST avec Prim
→ sommets impairs
→ matching parfait minimum
→ graphe eulérien
→ Hierholzer
→ shortcut
→ tournée TSP.

Génétique :
population de permutations
→ sélection tournoi
→ crossover OX
→ mutations swap/inversion
→ élitisme
→ plusieurs générations et plusieurs seeds.

Résultat :
Christofides ≈ 3445,60 km
GA ≈ 3157,13 km
GA meilleur d'environ 288,48 km / 8,37 %.
Mais GA ne prouve pas l'optimum.
```

---

# 73. La vraie logique du projet en une phrase

**Christofides utilise des garanties mathématiques de théorie des graphes pour construire rapidement une bonne tournée, tandis que l'algorithme génétique utilise une exploration stochastique de nombreuses permutations pour tenter de trouver une tournée encore meilleure ; le projet compare donc une méthode d'approximation théorique à une métaheuristique expérimentale.**
