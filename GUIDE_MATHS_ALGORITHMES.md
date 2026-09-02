# Guide TOTAL — comprendre, expliquer et défendre le projet « Le marchand ambulant »

> Objectif de ce document : être capable de **comprendre le projet depuis zéro**, d'expliquer **pourquoi chaque choix a été fait**, de distinguer les notions qui se ressemblent, de lire le code sans être perdu, et de répondre aux questions probables du formateur.
>
> Ce guide distingue trois choses :
> - **Ce que le sujet demande explicitement** ;
> - **Ce que notre implémentation fait réellement** ;
> - **Les explications / questions probables du formateur**, qui sont une préparation pédagogique et non des exigences écrites du sujet.

---

# 0. La carte mentale du projet en 30 secondes

Le projet entier peut se résumer comme ceci :

```text
20 villes + latitude/longitude
        ↓
Distances de Haversine entre toutes les paires
        ↓
Graphe complet pondéré
        ↓
Problème TSP : trouver un cycle court visitant toutes les villes
        ↓
Deux stratégies obligatoires dans le sujet
        ↓
┌──────────────────────────────┬──────────────────────────────┐
│ CHRISTOFIDES                 │ ALGORITHME GÉNÉTIQUE        │
│ méthode d'approximation      │ métaheuristique             │
│ déterministe                 │ stochastique                │
│ garantie théorique ≤ 1,5 OPT│ pas de garantie d'optimalité│
│                              │                              │
│ MST avec Prim                │ population de tournées      │
│ ↓                            │ ↓                            │
│ sommets impairs              │ sélection                   │
│ ↓                            │ ↓                            │
│ matching minimum             │ crossover OX                │
│ ↓                            │ ↓                            │
│ graphe eulérien              │ mutation                    │
│ ↓                            │ ↓                            │
│ Hierholzer                   │ élitisme                    │
│ ↓                            │ ↓                            │
│ shortcut                     │ générations                 │
└──────────────────────────────┴──────────────────────────────┘
        ↓
Comparaison : distance / temps / facilité / robustesse
        ↓
Recommandation
```

Si cette carte mentale est claire, tout le reste est une explication détaillée de chaque boîte.

---

# 1. Ce que le sujet demande réellement

Le sujet définit le **TSP** comme la recherche du chemin le plus court permettant de visiter toutes les villes une seule fois puis de revenir au point de départ. Il rappelle aussi qu'il s'agit d'un problème difficile à résoudre exactement à grande échelle.

Le sujet demande explicitement :

1. **20 villes françaises** ;
2. une représentation sous forme de **graphe** ;
3. la **distance de Haversine** ;
4. une résolution par **Christofides** ;
5. une résolution par **algorithme génétique** ;
6. plusieurs configurations du génétique ;
7. une comparaison sur :
   - distance totale ;
   - temps d'exécution ;
   - facilité d'implémentation ;
   - robustesse ;
8. une recommandation finale ;
9. une présentation ;
10. un dépôt GitHub public.

Le sujet cite également **Prim** dans sa base de connaissances, ce qui rend naturel son usage pour construire l'arbre couvrant minimum de Christofides.

**Important :** nous n'avons donc pas choisi Christofides et le génétique au hasard : **le sujet impose les deux**. Notre travail consiste surtout à les implémenter correctement, à comprendre pourquoi ils fonctionnent et à les comparer intelligemment.

---

# 2. Le problème mathématique : TSP

## 2.1 Définition intuitive

On possède `n` villes.

On cherche une tournée qui :

1. part d'une ville ;
2. visite toutes les autres villes ;
3. visite chaque ville une seule fois ;
4. revient au point de départ ;
5. minimise la distance totale.

Exemple :

```text
Paris → Lille → Reims → Strasbourg → ... → Marseille → ... → Paris
```

Ce n'est pas seulement « aller de Paris à Marseille au plus court ». Il faut choisir **l'ordre global de toutes les villes**.

---

## 2.2 Différence entre shortest path et TSP

C'est une confusion très probable à l'oral.

### Plus court chemin classique

On veut aller de `A` à `B` au moindre coût.

Exemple :

```text
Paris → Marseille
```

Dijkstra peut répondre à ce genre de problème.

### TSP

On veut visiter **toutes les villes**, puis revenir au départ.

```text
Paris → Lille → Strasbourg → Lyon → Marseille → ... → Paris
```

Dijkstra ne résout donc **pas** le TSP.

### Phrase à dire au formateur

> Dijkstra optimise un chemin entre une source et une destination, alors que le TSP optimise l'ordre global d'une tournée qui visite tous les sommets.

---

# 3. Pourquoi le TSP est difficile

## 3.1 Explosion combinatoire

Si on fixe la ville de départ, il reste `(n - 1)!` ordres possibles dans la formulation simplifiée du sujet.

Avec 20 villes :

```text
19! = 121 645 100 408 832 000
```

C'est gigantesque.

On pourrait encore remarquer que, pour un TSP symétrique, une tournée et la même tournée parcourue à l'envers ont la même longueur, donc le nombre de cycles distincts peut être réduit par symétrie. Mais même avec cette réduction, le nombre reste astronomique.

### Pourquoi c'est important ?

Parce que cela justifie toute la stratégie du projet :

```text
On ne veut PAS énumérer toutes les permutations.
On veut trouver une très bonne tournée intelligemment.
```

---

## 3.2 NP-difficile : ce que cela signifie ici

Le sujet dit que le TSP est **NP-difficile**.

Version utile à connaître :

> On ne connaît pas d'algorithme polynomial général capable de résoudre exactement toutes les grandes instances du TSP de manière efficace.

Attention à ne pas dire :

> « NP-difficile veut dire impossible. »

C'est faux.

On peut :

- résoudre exactement de petites instances ;
- résoudre certaines grandes instances grâce à des solveurs très avancés ;
- utiliser des approximations ou heuristiques pour obtenir rapidement d'excellentes solutions.

---

# 4. Quatre familles de stratégies à distinguer

## 4.1 Algorithme exact

Il garantit l'optimum global.

Exemples :

- brute force ;
- Held-Karp ;
- branch and bound ;
- programmation linéaire entière.

Avantage : optimum garanti.

Inconvénient : coût potentiellement énorme.

---

## 4.2 Algorithme d'approximation

Il produit une solution proche de l'optimum avec parfois une **garantie mathématique**.

Christofides appartient à cette famille.

Pour un TSP métrique :

```text
C_Christofides ≤ 1,5 × OPT
```

---

## 4.3 Heuristique

Méthode pratique sans garantie générale forte.

Exemples :

- nearest neighbor ;
- 2-opt ;
- 3-opt.

---

## 4.4 Métaheuristique

Cadre général d'exploration d'un espace de solutions.

Exemples :

- algorithme génétique ;
- recuit simulé ;
- recherche tabou ;
- colonies de fourmis.

Notre algorithme génétique est une **métaheuristique stochastique**.

---

# 5. Modéliser les villes avec un graphe

## 5.1 Graphe

Un graphe s'écrit souvent :

```text
G = (V, E)
```

- `V` = sommets ;
- `E` = arêtes.

Dans notre projet :

```text
sommet = ville
arête = possibilité de passer d'une ville à une autre
poids = distance en kilomètres
```

---

## 5.2 Pourquoi un graphe ?

Parce que le TSP est naturellement un problème de théorie des graphes.

Il faut choisir un cycle parmi des connexions pondérées.

Le graphe donne donc le langage mathématique nécessaire pour parler de :

- sommets ;
- cycles ;
- poids ;
- arbres ;
- degrés ;
- matching ;
- circuits eulériens.

---

# 6. Quel type de graphe utilisons-nous ?

Notre code construit un graphe :

```text
complet
pondéré
non orienté
connexe
simple au départ
```

Puis Christofides construit temporairement un **multigraphe**.

Il faut comprendre chaque mot.

---

## 6.1 Pondéré

Chaque arête possède un poids :

```text
poids = distance Haversine
```

---

## 6.2 Non orienté

Une arête n'a pas de sens imposé.

```text
Paris — Lyon
```

équivaut à :

```text
Lyon — Paris
```

Cela est cohérent avec Haversine :

```text
d(A,B) = d(B,A)
```

---

## 6.3 Complet

Toutes les paires de villes sont reliées.

Pour `n = 20` :

```text
nombre d'arêtes = n(n-1)/2
                  = 20×19/2
                  = 190
```

### Pourquoi avons-nous choisi un graphe complet ?

Parce qu'avec Haversine nous savons calculer une distance directe entre **n'importe quelle paire de villes**. Cela donne exactement le cadre classique du TSP métrique complet utilisé par Christofides.

Le code `build_complete_graph()` ajoute effectivement une arête pour chaque paire `i < j`.

---

## 6.4 Connexe

Un graphe est connexe si tous les sommets sont atteignables les uns depuis les autres.

Un graphe complet est automatiquement connexe.

C'est indispensable notamment pour construire un arbre couvrant.

---

## 6.5 Graphe simple vs multigraphe

### Graphe simple

Au maximum une arête entre deux sommets.

### Multigraphe

Plusieurs arêtes peuvent relier la même paire de sommets.

Christofides doit autoriser cette possibilité après :

```text
MST + matching
```

Une arête du matching peut correspondre à une paire déjà reliée dans le MST. On doit donc conserver les deux occurrences : d'où le multigraphe.

---

# 7. Haversine : pourquoi cette distance ?

## 7.1 Première raison : le sujet l'impose

Le sujet dit explicitement de considérer la **distance de Haversine**.

Donc il ne faut surtout pas répondre :

> « J'ai choisi Haversine parce que Google Maps était compliqué. »

La première réponse est :

> Le sujet demande Haversine.

---

## 7.2 Deuxième raison : latitude / longitude

Les villes sont données par coordonnées géographiques.

Une distance euclidienne naïve :

```text
sqrt((lat2-lat1)² + (lon2-lon1)²)
```

traite les degrés de latitude/longitude comme des coordonnées cartésiennes plates, ce qui n'est pas le bon modèle géographique.

Haversine calcule une distance de grand cercle sur une sphère.

Notre code utilise :

```text
R = 6371.0088 km
```

et :

```text
h = sin²(Δφ/2)
  + cos(φ1)cos(φ2)sin²(Δλ/2)

d = 2R asin(sqrt(h))
```

---

## 7.3 Est-ce une vraie distance routière ?

Non.

C'est une limitation importante.

Haversine mesure une distance géographique « à vol d'oiseau » sur la Terre, pas :

- les routes réelles ;
- les autoroutes ;
- les montagnes ;
- les sens interdits ;
- les temps de trajet.

### Bonne réponse au prof

> Pour ce projet, on optimise une distance géographique abstraite conforme au sujet. Pour un vrai marchand, il faudrait remplacer Haversine par un graphe routier réel ou des temps de trajet.

---

# 8. Pourquoi Haversine rend Christofides pertinent : la métrique

Christofides a sa garantie classique pour le **TSP métrique**.

Une métrique respecte notamment :

1. non-négativité ;
2. identité ;
3. symétrie ;
4. inégalité triangulaire.

L'inégalité triangulaire dit :

```text
d(A,C) ≤ d(A,B) + d(B,C)
```

### Exemple intuitif

Aller directement de Paris à Lyon ne doit pas être plus long que :

```text
Paris → Dijon → Lyon
```

Cette propriété sera cruciale au moment du **shortcut** de Christofides.

---

# 9. La matrice de distances

Notre fonction `distance_matrix()` pré-calcul toutes les distances entre les villes.

Avec 20 villes, on obtient conceptuellement :

```text
            Paris   Marseille   Lyon   ...
Paris        0        dPM        dPL
Marseille   dPM       0          dML
Lyon        dPL      dML          0
...
```

### Pourquoi une matrice ?

Parce que les algorithmes demandent la distance entre énormément de paires.

Au lieu de recalculer Haversine à chaque comparaison, on peut lire directement :

```python
matrix[i][j]
```

Cela simplifie et accélère les évaluations de tournées.

---

# 10. Chemin, cycle, tournée

## Chemin

```text
A → B → C
```

## Cycle

```text
A → B → C → A
```

Le TSP cherche un cycle particulier : un **cycle hamiltonien de poids minimal**.

---

# 11. Hamiltonien vs eulérien : distinction fondamentale

## 11.1 Hamiltonien

S'intéresse aux **sommets**.

Un cycle hamiltonien visite chaque sommet exactement une fois puis revient au départ.

Le TSP est un problème hamiltonien.

---

## 11.2 Eulérien

S'intéresse aux **arêtes**.

Un circuit eulérien traverse chaque arête exactement une fois et revient au départ.

---

## 11.3 Pourquoi Christofides parle d'Euler alors que le TSP parle d'Hamilton ?

Parce qu'il est plus facile de construire un circuit eulérien lorsque tous les degrés sont pairs.

Christofides fait donc :

```text
problème hamiltonien difficile
        ↓
construction temporaire eulérienne facile à parcourir
        ↓
shortcut
        ↓
cycle hamiltonien final
```

C'est une des idées centrales de l'algorithme.

---

# 12. Les arbres : tout ce qu'il faut distinguer

## 12.1 Arbre en théorie des graphes

Un arbre est :

- connexe ;
- sans cycle.

Un arbre de `n` sommets possède exactement :

```text
n - 1 arêtes
```

Donc pour 20 villes :

```text
19 arêtes
```

---

## 12.2 Arbre enraciné

Un arbre auquel on donne une racine.

Les notions parent/enfant/profondeur appartiennent souvent à ce contexte.

Ce n'est pas ce qui définit notre MST.

---

## 12.3 Arbre binaire

Chaque nœud a au maximum deux enfants.

Très utilisé en structures de données.

**Rien à voir avec le MST du projet.**

---

## 12.4 Arbre couvrant / spanning tree

Sous-graphe qui :

- contient tous les sommets ;
- est connexe ;
- ne possède aucun cycle.

---

## 12.5 MST

**Minimum Spanning Tree** = arbre couvrant de poids minimal.

Il minimise :

```text
somme des poids des arêtes
```

parmi tous les arbres couvrants.

---

# 13. Pourquoi le MST intervient dans le TSP

Cette justification est très importante à savoir expliquer.

Supposons que `OPT` soit la tournée TSP optimale.

Une tournée optimale est un cycle :

```text
A → B → C → D → A
```

Si on enlève une arête :

```text
A → B → C → D
```

on obtient un arbre couvrant.

Le MST est, par définition, l'arbre couvrant le moins cher.

Donc :

```text
poids(MST) ≤ OPT
```

Le MST fournit une **borne inférieure** de l'optimum.

Dans notre résultat :

```text
MST = 2665,05 km
```

Donc on sait au minimum :

```text
OPT ≥ 2665,05 km
```

Attention : cela ne veut PAS dire que l'optimum vaut 2665,05 km, car un MST n'est pas une tournée TSP.

---

# 14. Pourquoi le MST seul n'est pas une solution TSP

Dans une tournée TSP valide, chaque ville possède exactement deux connexions dans le cycle final : une arrivée et un départ.

Dans un arbre, un sommet peut avoir :

```text
degré 1
2
3
4
...
```

et il n'y a aucun cycle.

Donc le MST :

- relie toutes les villes ;
- coûte peu ;
- mais ne revient pas nécessairement au départ ;
- n'est pas un cycle hamiltonien.

Il est seulement une excellente structure de départ pour Christofides.

---

# 15. Prim : notre méthode pour construire le MST

Notre fonction `prim_mst()` commence avec un sommet visité puis maintient un tas (`heapq`) contenant les arêtes candidates.

L'idée :

```text
1. commencer par Paris (index 0)
2. regarder les arêtes qui sortent de l'arbre actuel
3. choisir la moins chère vers un sommet non visité
4. ajouter ce sommet
5. recommencer
```

---

## 15.1 Pourquoi Prim ?

Deux réponses :

### Réponse projet

Le sujet cite Prim dans la base de connaissances.

### Réponse algorithmique

Prim calcule exactement ce qu'il nous faut : un MST sur un graphe pondéré connexe.

Notre graphe est complet donc très dense, et Prim est parfaitement adapté.

---

# 16. Prim vs Kruskal vs Dijkstra

## Prim

Objectif :

```text
MST
```

Il agrandit un arbre connecté.

## Kruskal

Objectif :

```text
MST
```

Il trie globalement les arêtes et ajoute les moins chères sans créer de cycle.

## Dijkstra

Objectif :

```text
plus courts chemins depuis une source
```

### Question probable

**« Pourquoi pas Dijkstra pour le MST ? »**

Réponse :

> Parce que Dijkstra optimise des distances de chemin depuis une source. Prim optimise le poids total d'un arbre couvrant. Les objectifs mathématiques sont différents.

---

# 17. Christofides : pourquoi cet algorithme ?

Il y a trois raisons.

## Raison 1 — le sujet l'impose

C'est la raison principale dans le cadre du projet.

## Raison 2 — nos distances sont métriques

Haversine fournit le cadre nécessaire à sa garantie classique.

## Raison 3 — compromis intéressant

Christofides :

- est déterministe pour une implémentation déterministe ;
- est rapide sur 20 villes ;
- fournit une solution valide ;
- possède une garantie théorique `≤ 1,5 × OPT`.

Il constitue donc une excellente référence contre laquelle comparer le génétique.

---

# 18. Christofides : les 6 étapes

Notre code suit :

```text
1. MST avec Prim
2. sommets de degré impair
3. matching parfait minimum
4. MST + matching = multigraphe eulérien
5. circuit eulérien avec Hierholzer
6. shortcut → cycle hamiltonien
```

Il faut comprendre **pourquoi chaque étape existe**.

---

# 19. Étape 1 — MST

On commence avec une structure qui :

- relie toutes les villes ;
- est très peu coûteuse ;
- donne une borne inférieure de l'optimum.

Dans notre instance :

```text
MST ≈ 2665,05 km
```

Mais il n'est pas encore eulérien ni hamiltonien.

---

# 20. Étape 2 — degrés pairs et impairs

Le degré d'un sommet est le nombre d'arêtes qui le touchent.

Exemple :

```text
    A
    |
B---C---D
```

`deg(C) = 3`.

Dans notre MST, **12 sommets sont de degré impair**.

---

## 20.1 Pourquoi s'intéresser aux sommets impairs ?

Parce qu'un graphe connexe possède un **circuit eulérien** si tous ses sommets ont un degré pair.

Donc le problème devient :

```text
Comment rendre pairs tous les sommets impairs
sans ajouter trop de distance ?
```

Réponse : le matching minimum.

---

## 20.2 Pourquoi y a-t-il toujours un nombre pair de sommets impairs ?

Grâce au **lemme de la poignée de main** :

```text
somme des degrés = 2 × nombre d'arêtes
```

La somme des degrés est donc paire.

Pour que la somme soit paire, le nombre de termes impairs doit lui-même être pair.

C'est utile car on peut alors former des paires entre les sommets impairs.

---

# 21. Étape 3 — matching parfait de poids minimal

## 21.1 Matching

Un matching est un ensemble d'arêtes qui ne partagent pas de sommet.

## 21.2 Perfect matching

Tous les sommets concernés sont appariés exactement une fois.

## 21.3 Minimum-weight perfect matching

Parmi tous les appariements parfaits possibles, on choisit celui dont la somme des distances est minimale.

Dans notre projet :

```text
matching ≈ 1142,03 km
```

---

## 21.4 Pourquoi cela rend les degrés pairs ?

Chaque sommet impair reçoit exactement **une** nouvelle arête.

Donc :

```text
1 → 2
3 → 4
5 → 6
...
```

Chaque degré impair devient pair.

Les sommets déjà pairs ne sont pas touchés par ce matching.

---

# 22. Étape 4 — MST + matching = multigraphe eulérien

Après l'union :

- le graphe reste connexe ;
- tous les degrés sont pairs.

Il est donc eulérien.

Pourquoi un **multigraphe** ?

Parce qu'une arête ajoutée par le matching peut dupliquer une liaison existante du MST.

---

# 23. Étape 5 — Hierholzer

Hierholzer construit un **circuit eulérien**.

Notre fonction `_hierholzer_multigraph()` utilise :

- une pile ;
- un identifiant unique pour chaque arête ;
- un ensemble `used_edges`.

Cela est particulièrement important dans un multigraphe : deux arêtes entre les mêmes sommets doivent être considérées comme deux arêtes distinctes.

À la fin, on obtient une tournée qui traverse chaque arête du multigraphe exactement une fois.

---

# 24. Étape 6 — shortcut

Le circuit eulérien peut revisiter des villes.

Exemple :

```text
A → B → C → B → D → A
```

Mais le TSP veut chaque ville une seule fois.

On supprime donc les répétitions :

```text
A → B → C → D → A
```

### Pourquoi la distance n'augmente pas ?

Grâce à l'inégalité triangulaire :

```text
d(C,D) ≤ d(C,B) + d(B,D)
```

Le raccourci direct est au plus aussi long que le détour.

C'est précisément pour cela que la propriété métrique est centrale.

---

# 25. La garantie 1,5 de Christofides — raisonnement intuitif

C'est un excellent niveau de réponse si le prof demande :

**« D'où vient le facteur 1,5 ? »**

On note `OPT` la longueur de la tournée optimale.

## Étape A

Le MST est moins cher que l'optimum :

```text
MST ≤ OPT
```

## Étape B

On peut montrer que le matching minimum sur les sommets impairs coûte au plus :

```text
Matching ≤ OPT / 2
```

Intuition : une tournée optimale permet de connecter ces sommets impairs ; en prenant un appariement approprié et grâce à la métrique, le matching minimum ne peut pas être plus mauvais que cette borne.

## Étape C

Donc :

```text
MST + Matching ≤ OPT + OPT/2
                 ≤ 1,5 OPT
```

## Étape D

Le circuit eulérien parcourt exactement toutes ces arêtes.

## Étape E

Le shortcut n'augmente pas la distance.

Donc :

```text
Christofides ≤ 1,5 × OPT
```

---

# 26. Ce que la garantie NE signifie PAS

Elle ne signifie pas :

```text
Christofides sera toujours exactement 50 % plus long.
```

Elle signifie :

```text
C ≤ 1,5 OPT
```

Il peut être :

- optimal ;
- 2 % au-dessus ;
- 10 % au-dessus ;
- etc.

Le facteur 1,5 est une **borne de pire cas**.

---

# 27. Déterministe : que veut dire ce mot ?

Un algorithme déterministe, avec :

- mêmes données ;
- même implémentation ;
- même gestion des égalités ;

produit le même résultat.

Notre Christofides ne s'appuie pas sur du hasard.

Le génétique, au contraire, en utilise.

---

# 28. Algorithme génétique : pourquoi utiliser cette seconde méthode ?

Première raison : le sujet l'impose.

Mais c'est aussi une comparaison intéressante car la philosophie est totalement différente.

Christofides :

```text
construction mathématique structurée
```

Génétique :

```text
exploration stochastique de nombreuses tournées
```

Le génétique peut parfois trouver une tournée plus courte que Christofides, sans pour autant pouvoir prouver qu'elle est optimale.

---

# 29. L'idée biologique du génétique

On imite grossièrement :

```text
population
↓
sélection des meilleurs
↓
reproduction
↓
mutation
↓
nouvelle génération
↓
répéter
```

Le mot « meilleur » signifie ici : **tournée plus courte**.

---

# 30. Représentation d'un individu dans notre code

Paris est l'index `0`.

Notre chromosome contient uniquement :

```text
1, 2, ..., 19
```

c'est-à-dire les 19 autres villes dans un certain ordre.

Exemple simplifié :

```text
chromosome = [3, 2, 5, 1, 4]
```

La tournée évaluée devient :

```text
Paris → 3 → 2 → 5 → 1 → 4 → Paris
```

---

# 31. Pourquoi fixer Paris au départ ?

Dans un cycle, le point de départ est arbitraire.

Ces tournées décrivent le même cycle :

```text
Paris → Lyon → Lille → Paris
Lyon → Lille → Paris → Lyon
Lille → Paris → Lyon → Lille
```

Fixer Paris comme ancre élimine cette redondance de rotation et simplifie les chromosomes.

Cela ne force pas le marchand à une mauvaise solution : n'importe quel cycle peut être réécrit en commençant par Paris.

---

# 32. Permutation : pourquoi c'est important

Un chromosome doit contenir chaque ville exactement une fois.

Il s'agit donc d'une **permutation**.

Valide :

```text
[1, 4, 3, 2]
```

Invalide :

```text
[1, 4, 4, 2]
```

car une ville est dupliquée et une autre manque.

Cela explique pourquoi on ne peut pas utiliser n'importe quel crossover génétique classique.

---

# 33. Population initiale

Notre code crée plusieurs permutations aléatoires :

```python
rng.shuffle(chromosome)
```

Pourquoi aléatoires ?

Parce qu'on veut commencer avec une diversité de tournées, pas avec 160 copies de la même solution.

---

# 34. Fitness vs coût

Dans de nombreux cours, une fitness « élevée » est meilleure.

Notre code travaille directement avec un **coût à minimiser** : la distance.

```text
3157 km est meilleur que 3400 km
```

Donc le classement prend le minimum.

### Question piège

**« Où est votre fonction fitness ? »**

Réponse :

> Dans notre implémentation, nous n'inversons pas la distance pour créer une fitness maximisée. Nous utilisons directement la distance totale comme fonction objectif à minimiser.

---

# 35. Sélection par tournoi

Notre code sélectionne `k` individus au hasard puis choisit le meilleur d'entre eux.

Pour la configuration retenue :

```text
tournament_size = 5
```

Exemple :

```text
A = 3400 km
B = 3180 km
C = 3500 km
D = 3250 km
E = 3330 km
```

Le parent choisi est `B`.

---

# 36. Pourquoi la sélection par tournoi ?

Elle est :

- simple ;
- efficace ;
- compatible avec une fonction objectif de minimisation ;
- facile à contrôler par `tournament_size`.

### Pression de sélection

Plus le tournoi est grand, plus les très bons individus ont tendance à gagner.

Trop forte pression : risque de perdre la diversité.

Trop faible pression : progression plus lente.

---

# 37. Crossover : pourquoi reproduire deux parents ?

L'idée est de combiner des structures intéressantes de deux tournées.

Mais sur un TSP, il faut préserver la contrainte de permutation.

C'est pourquoi notre code utilise **Ordered Crossover (OX)**.

---

# 38. Ordered Crossover (OX) — exemple détaillé

Parents :

```text
P1 = A B C D E F G H
P2 = C F E H A D B G
```

On choisit une zone dans P1, par exemple :

```text
C D E
```

L'enfant conserve ce segment puis remplit les positions restantes avec l'ordre de P2 en ignorant les éléments déjà présents.

L'objectif est d'obtenir :

- toutes les villes une fois ;
- aucune duplication ;
- une partie de l'ordre des parents préservée.

Notre taux :

```text
crossover_rate = 0.95
```

Donc dans 95 % des reproductions, on tente un crossover ; sinon les parents sont copiés.

---

# 39. Pourquoi 95 % de crossover ?

Il faut être précis à l'oral :

> Ce n'est pas une constante mathématiquement optimale. C'est un hyperparamètre de notre configuration expérimentale.

Un taux élevé encourage la recombinaison des tournées.

Mais il est équilibré par :

- l'élitisme ;
- la mutation ;
- la sélection.

---

# 40. Mutation

Notre mutation fait aléatoirement :

1. **swap** ; ou
2. **inversion**.

---

## 40.1 Swap

```text
A B C D E
```

peut devenir :

```text
A D C B E
```

Deux villes échangent de position.

---

## 40.2 Inversion

```text
A B C D E F
```

on inverse `[B C D E]` :

```text
A E D C B F
```

L'inversion est particulièrement naturelle pour le TSP car elle peut modifier un segment entier de tournée tout en gardant une permutation valide.

---

# 41. Pourquoi muter ?

Sans mutation, la population risque de devenir très homogène.

Elle peut alors rester bloquée dans un **optimum local**.

La mutation réintroduit :

```text
diversité
exploration
```

---

# 42. Pourquoi pas 100 % de mutation ?

Trop de mutation détruit continuellement les bonnes structures apprises.

On veut un équilibre entre :

```text
exploitation = améliorer les bonnes solutions connues
exploration  = chercher ailleurs
```

La configuration retenue utilise :

```text
mutation_rate = 0.22
```

soit 22 % de probabilité de mutation par enfant dans notre code.

---

# 43. Élitisme

La configuration retenue conserve directement les :

```text
6 meilleurs individus
```

Pourquoi ?

Sans élitisme, une excellente tournée pourrait disparaître par hasard à la génération suivante.

L'élitisme garantit que la meilleure qualité déjà atteinte n'est pas perdue.

Cela explique aussi pourquoi notre courbe du **best-so-far** ne remonte pas.

---

# 44. Générations

Une génération = une itération complète :

```text
évaluation
↓
sélection
↓
crossover
↓
mutation
↓
nouvelle population
```

Notre configuration retenue utilise :

```text
520 générations
```

---

# 45. Population : pourquoi 160 ?

Notre benchmark compare trois configurations :

```text
rapide       : 80 individus / 220 générations
équilibrée   : 160 individus / 520 générations
exploratoire : 240 individus / 800 générations
```

Le code choisit ensuite la configuration selon :

```text
1. meilleure distance moyenne
2. puis plus faible écart-type
3. puis meilleur minimum
```

Sur nos trois seeds, la configuration **équilibrée** a été la plus stable et a obtenu la meilleure moyenne.

Donc `160` n'est pas présenté comme une vérité universelle :

> c'est le meilleur compromis parmi les configurations testées dans notre expérience.

---

# 46. Seed : pourquoi 11, 22, 33 ?

Le génétique utilise du hasard.

Une `seed` initialise le générateur pseudo-aléatoire.

Avec la même seed et les mêmes paramètres, on peut reproduire la même séquence pseudo-aléatoire.

Nous testons :

```text
11
22
33
```

pour observer si une configuration fonctionne bien seulement grâce à un coup de chance ou si elle reste stable.

Les nombres eux-mêmes n'ont rien de magique : ils sont simplement trois seeds distinctes et reproductibles.

---

# 47. Robustesse

Le sujet demande de comparer la **robustesse**.

Ici, cela veut dire notamment :

> Une méthode donne-t-elle des résultats cohérents quand on la relance ou quand les conditions aléatoires changent ?

Christofides : très stable car pas de hasard dans notre implémentation.

Génétique : dépend de la seed et des paramètres.

---

# 48. Moyenne, meilleur, pire, écart-type

Pour chaque configuration GA, nous calculons :

- `best_km` ;
- `mean_km` ;
- `std_km` ;
- `worst_km`.

## Moyenne

Qualité moyenne sur plusieurs runs.

## Écart-type

Mesure la dispersion.

Petit écart-type : résultats proches les uns des autres.

Grand écart-type : comportement plus variable.

Dans notre benchmark :

```text
équilibrée : std = 0 sur les trois seeds testées
```

### Attention à la formulation

Ne dites pas :

> « L'algorithme équilibré a une variance zéro en général. »

Dites :

> « Sur nos trois seeds testées, les trois runs ont convergé vers la même distance, donc l'écart-type observé est zéro. »

Trois runs restent un échantillon limité.

---

# 49. Pourquoi la configuration « exploratoire » n'est-elle pas forcément meilleure ?

Question très plausible.

Plus de :

- population ;
- générations ;
- mutation ;

ne garantit pas automatiquement une meilleure solution.

Raisons possibles :

1. le processus est stochastique ;
2. une mutation plus forte peut détruire de bonnes structures ;
3. plus d'exploration ne signifie pas forcément meilleure exploitation ;
4. le nombre de seeds testées est limité.

Il faut parler des **résultats observés**, pas inventer une loi générale.

---

# 50. Optimum local vs optimum global

## Optimum global

La meilleure tournée parmi absolument toutes les tournées.

## Optimum local

Une solution très bonne dans sa région de l'espace de recherche, mais pas forcément la meilleure globalement.

Le génétique essaie d'éviter les optima locaux grâce à :

- population multiple ;
- crossover ;
- mutation.

Mais il n'y a aucune garantie absolue.

---

# 51. Convergence

La convergence signifie que l'algorithme cesse progressivement d'améliorer sa meilleure solution.

Notre `history` enregistre la meilleure distance connue après chaque génération.

Une courbe typique :

```text
distance
  |
  |\
  | \
  |  \____
  |       \_____
  |______________ génération
```

Au début : améliorations rapides.

Ensuite : améliorations plus rares.

Puis plateau.

---

# 52. Nos résultats actuels

Les résultats générés par le projet sont :

```text
MST                         2665,05 km
Christofides                3445,60 km
Algorithme génétique        3157,13 km
```

Différence :

```text
3445,60 - 3157,13 = 288,48 km
```

Le génétique est donc :

```text
≈ 8,37 % plus court que Christofides
```

sur **cette instance et ces expérimentations**.

---

# 53. Que nous apprend le MST sur nos résultats ?

Comme :

```text
MST ≤ OPT ≤ meilleure tournée connue
```

nous avons ici :

```text
2665,05 ≤ OPT ≤ 3157,13 km
```

La tournée génétique est environ :

```text
492,07 km
```

au-dessus de cette borne inférieure MST, soit environ `18,46 %` au-dessus du MST.

Attention : cela **ne prouve pas** qu'elle est 18,46 % au-dessus de l'optimum.

L'optimum peut être n'importe où entre la borne inférieure et la meilleure solution connue.

---

# 54. Pourquoi le génétique peut battre Christofides sans contradiction

Christofides ne promet pas de battre toutes les heuristiques.

Il promet :

```text
≤ 1,5 OPT
```

Un algorithme génétique peut très bien découvrir une meilleure tournée sur une instance particulière.

La différence est :

```text
Christofides : garantie théorique
GA           : qualité empirique observée
```

---

# 55. Peut-on dire que le GA a trouvé l'optimum ?

Non.

On peut dire :

> 3157,13 km est la meilleure solution observée dans nos runs.

On ne peut pas dire :

> 3157,13 km est l'optimum mathématique.

Pour le prouver, il faudrait une méthode exacte ou une borne inférieure qui atteigne exactement cette valeur.

---

# 56. Temps d'exécution : comment l'interpréter

Dans un run généré récemment :

- Christofides s'exécute en quelques millisecondes ;
- un run du GA équilibré est de l'ordre de la seconde ;
- plusieurs runs et le benchmark prennent davantage de temps.

Mais les temps dépendent :

- de la machine ;
- de Python ;
- de la charge système ;
- des versions de bibliothèques.

La conclusion importante n'est pas un nombre universel :

> Christofides est beaucoup moins coûteux ici que notre benchmark génétique.

---

# 57. Complexité — niveau utile pour l'oral

## 57.1 Construire toutes les distances

Il y a environ :

```text
n(n-1)/2
```

paires.

Donc :

```text
O(n²)
```

---

## 57.2 Prim

Sur un graphe avec `V` sommets et `E` arêtes, une implémentation avec tas est typiquement exprimée autour de :

```text
O(E log V)
```

Pour un graphe complet :

```text
E = O(n²)
```

---

## 57.3 Matching

Le matching parfait minimum est une étape plus sophistiquée, généralement polynomiale mais plus coûteuse que les opérations simples du MST.

Notre code délègue cette étape à NetworkX.

---

## 57.4 Algorithme génétique

Il évalue environ :

```text
population × générations
```

individus, chaque distance de tournée parcourant `n` villes.

Approximation pédagogique :

```text
O(P × G × n)
```

sans détailler tous les coûts du tri, de la sélection et du crossover.

Avec :

```text
P = 160
G = 520
```

cela représente déjà des dizaines de milliers d'évaluations de tournées pour un run.

---

# 58. Pourquoi NetworkX ?

Le sujet le cite dans sa base de connaissances.

Dans notre code, NetworkX sert notamment à :

- représenter les graphes ;
- calculer le minimum-weight matching.

Mais nous avons implémenté nous-mêmes :

- Prim ;
- Hierholzer ;
- la logique de Christofides ;
- la logique génétique.

### Question probable

**« Vous avez juste appelé une fonction Christofides de NetworkX ? »**

Réponse :

> Non. La logique de Christofides est explicitement implémentée dans `src/christofides.py`. NetworkX est utilisé pour la structure du graphe et le matching minimum.

---

# 59. Lecture du code — `src/core.py`

## `City`

Stocke :

```text
nom
latitude
longitude
```

## `load_cities()`

- ouvre le CSV ;
- vérifie les colonnes ;
- convertit latitude/longitude en `float` ;
- exige au moins 3 villes.

## `haversine_km()`

Calcule la distance géographique.

## `distance_matrix()`

Pré-calcule toutes les distances.

## `build_complete_graph()`

Ajoute tous les sommets et toutes les arêtes pondérées.

## `route_distance()`

Somme :

```text
matrix[route[i]][route[i+1]]
```

## `route_names()`

Convertit les indices numériques en noms de villes lisibles.

---

# 60. Lecture du code — `src/christofides.py`

## `prim_mst()`

Construit le MST.

## calcul des degrés

```python
degree[u] += 1
degree[v] += 1
```

## sommets impairs

```python
odd_vertices = [v for v, deg in enumerate(degree) if deg % 2 == 1]
```

## graphe des sommets impairs

On crée un sous-graphe complet uniquement sur ces sommets.

## `min_weight_matching()`

Trouve le matching minimum.

## union MST + matching

On construit l'adjacence du multigraphe.

## `_hierholzer_multigraph()`

Circuit eulérien.

## `seen`

Supprime les répétitions du circuit eulérien.

## fermeture du cycle

```python
hamiltonian.append(hamiltonian[0])
```

On revient à Paris.

---

# 61. Lecture du code — `src/genetic.py`

## `GAConfig`

Stocke tous les hyperparamètres.

## `_closed_distance()`

Transforme le chromosome en :

```text
Paris + chromosome + Paris
```

## `_tournament()`

Choisit le meilleur de `k` individus tirés au hasard.

## `_ordered_crossover()`

Produit deux enfants permutations valides.

## `_mutate()`

Swap ou inversion.

## `genetic_tsp()`

Boucle principale des générations.

## élites

```python
ranked[: config.elite_size]
```

## `history`

Stocke le meilleur coût atteint.

## `benchmark_configs()`

Relance chaque configuration sur plusieurs seeds et calcule :

- minimum ;
- moyenne ;
- écart-type ;
- maximum.

---

# 62. Lecture du code — `main.py`

`run_all()` orchestre tout :

```text
charger villes
↓
Christofides
↓
benchmark GA
↓
choisir configuration
↓
faire 3 runs GA
↓
prendre meilleur run
↓
générer cartes
↓
générer PNG
↓
générer CSV benchmark
↓
générer summary.json
```

---

# 63. Pourquoi choisir la configuration par moyenne puis écart-type ?

Le meilleur résultat isolé peut être un coup de chance.

Nous préférons d'abord :

```text
bonne qualité moyenne
```

puis :

```text
stabilité
```

puis seulement :

```text
meilleur résultat unique
```

C'est cohérent avec la demande du sujet de discuter de **robustesse**.

---

# 64. Pourquoi trois seeds seulement ?

C'est suffisant pour démontrer le principe dans un projet pédagogique et garder un temps de calcul faible.

Mais scientifiquement, trois runs sont peu.

### Très bonne réponse au prof

> Trois seeds donnent un premier indicateur de robustesse, mais une étude plus solide utiliserait davantage de runs, par exemple 20, 30 ou plus, avec intervalles de confiance et tests statistiques.

---

# 65. Pourquoi ne pas initialiser le GA avec Christofides ?

Nous aurions pu injecter la tournée de Christofides dans la population initiale.

Cela aurait donné au GA une bonne solution de départ.

Mais notre implémentation démarre avec des permutations aléatoires afin de comparer plus proprement deux approches séparées.

C'est une **amélioration possible**, pas quelque chose que le sujet impose.

---

# 66. Pourquoi ne pas utiliser 2-opt après le génétique ?

2-opt améliore localement une tournée en supprimant deux arêtes et en reconnectant les segments différemment.

Un hybride :

```text
GA + 2-opt
```

pourrait probablement améliorer la qualité ou accélérer la convergence.

Mais ce serait une extension au-delà du cœur demandé.

---

# 67. Limites de notre projet

Il faut les connaître : un bon oral ne prétend jamais que tout est parfait.

## 67.1 Haversine n'est pas la route réelle

Déjà expliqué.

## 67.2 Le GA ne prouve pas l'optimum

3157,13 km est une meilleure solution observée.

## 67.3 Benchmark limité

3 configurations × 3 seeds.

## 67.4 Hyperparamètres non exhaustifs

Nous n'avons pas exploré toutes les populations, mutations, croisements possibles.

## 67.5 20 villes seulement

Les conclusions de performance ne se généralisent pas automatiquement à 1000 villes.

---

# 68. Comparaison conceptuelle finale

| Critère | Christofides | Algorithme génétique |
|---|---|---|
| Famille | Approximation | Métaheuristique |
| Hasard | Non | Oui |
| Garantie | ≤ 1,5 OPT si TSP métrique | Aucune |
| Solution observée | 3445,60 km | 3157,13 km |
| Temps sur notre projet | Très faible | Plus élevé |
| Paramètres | Peu | Beaucoup |
| Robustesse | Très élevée | À mesurer selon seeds |
| Explication mathématique | Forte | Plus expérimentale |
| Amélioration possible par plus de calcul | Limitée dans l'algo standard | Oui |

---

# 69. Notre recommandation

Si Théobald veut avant tout :

## une garantie théorique + rapidité + simplicité d'exécution

```text
Christofides
```

## la plus courte tournée observée dans notre expérience

```text
algorithme génétique
```

Notre recommandation finale dans le projet est donc :

> Sur cette instance de 20 villes, retenir le génétique si la priorité principale est la distance, tout en gardant Christofides comme référence rapide, stable et théoriquement encadrée.

---

# 70. Questions TRÈS probables du formateur

Cette partie est une **prévision pédagogique**, pas une liste fournie par le sujet.

---

## Q1. C'est quoi le TSP ?

> Trouver le cycle de coût minimal qui visite chaque ville exactement une fois et revient au départ.

---

## Q2. Pourquoi ne pas tester toutes les possibilités ?

> Parce que le nombre de permutations croît factoriellement. Avec 20 villes et un départ fixé, le sujet parle de `19!`, soit environ `1,216 × 10^17` possibilités.

---

## Q3. Pourquoi utiliser un graphe ?

> Parce que les villes deviennent des sommets, les connexions des arêtes et les distances des poids. Le TSP est naturellement formulé comme la recherche d'un cycle hamiltonien minimum dans un graphe pondéré.

---

## Q4. Pourquoi le graphe est-il complet ?

> Nous pouvons calculer Haversine entre toutes les paires de villes, donc chaque ville est reliée à toutes les autres. C'est le cadre du TSP métrique complet utilisé par Christofides.

---

## Q5. Combien d'arêtes pour 20 villes ?

```text
20×19/2 = 190
```

---

## Q6. Pourquoi Haversine ?

> Le sujet le demande et les données sont des latitudes/longitudes. Haversine calcule une distance géographique cohérente sur une sphère.

---

## Q7. Haversine donne-t-elle la vraie route ?

> Non, elle donne une distance géographique de grand cercle, pas un itinéraire routier.

---

## Q8. Qu'est-ce que l'inégalité triangulaire ?

```text
d(A,C) ≤ d(A,B) + d(B,C)
```

> Elle garantit qu'un raccourci direct ne coûte pas plus qu'un détour. Elle est essentielle au shortcut de Christofides.

---

## Q9. C'est quoi un MST ?

> L'arbre couvrant de poids minimal : il relie tous les sommets sans cycle avec une somme d'arêtes minimale.

---

## Q10. Pourquoi un MST a 19 arêtes ici ?

> Tout arbre à `n` sommets a `n-1` arêtes. Donc 20 villes → 19 arêtes.

---

## Q11. Pourquoi le MST est une borne inférieure du TSP ?

> Si on retire une arête d'une tournée TSP optimale, on obtient un arbre couvrant. Le MST étant le meilleur arbre couvrant, il ne peut pas coûter plus que la tournée optimale.

---

## Q12. Pourquoi le MST n'est-il pas directement la tournée ?

> Parce qu'il ne contient aucun cycle et que les degrés ne sont pas forcément 2. Il ne satisfait donc pas la contrainte de tournée TSP.

---

## Q13. Pourquoi Prim ?

> Prim calcule un MST, et le sujet le cite dans la base de connaissances. Il est adapté à notre graphe pondéré connexe et dense.

---

## Q14. Prim et Dijkstra, différence ?

> Prim minimise le poids total d'un arbre couvrant. Dijkstra calcule les plus courts chemins depuis une source.

---

## Q15. Prim et Kruskal, différence ?

> Les deux calculent un MST. Prim fait grandir un arbre depuis une racine ; Kruskal trie les arêtes et fusionne progressivement des composantes sans créer de cycle.

---

## Q16. Pourquoi regarder les degrés impairs dans Christofides ?

> Parce qu'un circuit eulérien nécessite que tous les degrés soient pairs. Le matching va corriger exactement les sommets impairs.

---

## Q17. Pourquoi le nombre de sommets impairs est-il pair ?

> Parce que la somme des degrés vaut deux fois le nombre d'arêtes et est donc paire. Le nombre de degrés impairs doit être pair.

---

## Q18. C'est quoi un matching parfait ?

> Un ensemble d'arêtes qui apparie tous les sommets concernés exactement une fois.

---

## Q19. Pourquoi minimum ?

> Parce qu'on veut rendre les degrés pairs en ajoutant le moins de distance possible.

---

## Q20. Pourquoi MST + matching devient eulérien ?

> Le MST reste connecté et chaque sommet impair reçoit une nouvelle arête, donc tous les degrés deviennent pairs.

---

## Q21. C'est quoi un multigraphe ?

> Un graphe qui autorise plusieurs arêtes entre la même paire de sommets. Il est utile ici parce que le matching peut ajouter une arête déjà présente dans le MST.

---

## Q22. C'est quoi Hierholzer ?

> Un algorithme pour construire un circuit eulérien en parcourant chaque arête exactement une fois.

---

## Q23. Euler vs Hamilton ?

> Euler = chaque arête une fois. Hamilton = chaque sommet une fois. Le TSP cherche un cycle hamiltonien ; Christofides passe temporairement par un circuit eulérien.

---

## Q24. Pourquoi le shortcut est valide ?

> Parce que l'inégalité triangulaire garantit que sauter une ville déjà visitée n'augmente pas la distance.

---

## Q25. Que garantit Christofides ?

> Pour un TSP métrique, une solution de coût au plus `1,5 × OPT`.

---

## Q26. Est-ce que 3445,60 km est 1,5 fois l'optimum ?

> Pas nécessairement. 1,5 est une borne maximale théorique, pas la valeur attendue.

---

## Q27. Pourquoi un algorithme génétique ?

> Le sujet le demande et il permet d'explorer un grand espace de permutations sans recherche exhaustive, avec une stratégie stochastique différente de Christofides.

---

## Q28. C'est quoi un individu ?

> Une tournée candidate, représentée par une permutation des 19 villes autres que Paris.

---

## Q29. Pourquoi seulement 19 villes dans le chromosome ?

> Paris est fixé comme ancre de départ et de retour. Cela retire une redondance de rotation sans changer l'ensemble des cycles possibles.

---

## Q30. C'est quoi la fitness ?

> Dans notre code, nous utilisons directement la distance totale comme coût à minimiser.

---

## Q31. Comment sélectionnez-vous les parents ?

> Par tournoi : on tire quelques individus au hasard et on prend celui dont la distance est la plus petite.

---

## Q32. Pourquoi OX ?

> Parce qu'un chromosome TSP est une permutation. OX produit des enfants sans dupliquer ou oublier de ville.

---

## Q33. Pourquoi mutation swap/inversion ?

> Ces deux opérations modifient l'ordre des villes tout en préservant une permutation valide.

---

## Q34. Pourquoi l'élitisme ?

> Pour conserver les meilleures solutions déjà trouvées et éviter qu'elles soient perdues par hasard.

---

## Q35. Pourquoi mutation 22 % ?

> C'est l'hyperparamètre de la configuration équilibrée retenue parmi celles testées. Ce n'est pas une constante théorique universelle.

---

## Q36. Pourquoi 160 individus ?

> Même logique : c'est la configuration qui a fourni la meilleure moyenne et stabilité parmi nos trois configurations testées.

---

## Q37. Pourquoi plusieurs seeds ?

> Parce que le génétique est aléatoire. Plusieurs seeds permettent d'évaluer la stabilité et de réduire le risque de conclure à partir d'un run chanceux.

---

## Q38. Pourquoi seed 11, 22, 33 ?

> Ce sont simplement trois valeurs distinctes reproductibles. Elles n'ont pas de propriété mathématique spéciale.

---

## Q39. Pourquoi l'écart-type est important ?

> Il mesure la dispersion des résultats et donc une partie de la robustesse empirique.

---

## Q40. Pourquoi la config exploratoire n'est pas meilleure malgré plus de calcul ?

> Plus de population/générations/mutation ne garantit pas une meilleure convergence. Le processus est stochastique et une mutation trop forte peut également perturber de bonnes structures.

---

## Q41. Le GA a-t-il trouvé l'optimum ?

> Nous ne pouvons pas le prouver. 3157,13 km est la meilleure solution observée.

---

## Q42. Alors comment savez-vous que la solution est bonne ?

> Elle bat Christofides sur cette instance et reste comparée à une borne inférieure MST de 2665,05 km. Mais seule une méthode exacte ou une borne plus serrée pourrait certifier l'optimalité.

---

## Q43. Pourquoi le GA est-il plus lent ?

> Parce qu'il évalue des populations entières pendant des centaines de générations et nous le relançons plusieurs fois pour mesurer sa robustesse.

---

## Q44. Pourquoi ne pas choisir directement le GA puisqu'il donne moins de kilomètres ?

> Parce que le sujet demande une analyse multicritère. Christofides offre rapidité, déterminisme et garantie théorique, tandis que le GA donne ici la meilleure distance mais avec plus de calcul et sans garantie.

---

## Q45. Quelle méthode recommandez-vous ?

> Pour cette instance, le GA si la priorité est la distance. Christofides si la priorité est une réponse très rapide, stable et théoriquement encadrée.

---

# 71. Questions « pièges » un peu plus avancées

## « Pourquoi Christofides nécessite-t-il une distance métrique ? »

> Principalement pour que le shortcut ne rallonge pas le circuit et pour la preuve de la borne 3/2.

## « Si les distances routières ne respectaient pas l'inégalité triangulaire, que se passe-t-il ? »

> La garantie standard de Christofides ne s'appliquerait plus directement. Il faudrait vérifier ou prendre la fermeture métrique du graphe.

## « Pourquoi pouvez-vous partir de Paris sans perdre l'optimum ? »

> Un cycle n'a pas de véritable début. Toute tournée optimale peut être tournée dans son écriture pour commencer par Paris.

## « Pourquoi ne divisez-vous pas exactement par 2 le nombre `(n-1)!` ? »

> Le sujet présente `(n-1)!` comme ordre de grandeur avec le départ fixé. Pour un TSP symétrique, on peut encore identifier une tournée avec son inverse, ce qui réduit les cycles uniques, mais cela ne change pas la conclusion : l'espace reste gigantesque.

## « Un MST est-il unique ? »

> Pas forcément. Si plusieurs arêtes ont les mêmes poids, plusieurs MST différents peuvent avoir le même poids minimal.

## « Prim dépend-il du sommet de départ ? »

> Le poids du MST reste minimal. Si plusieurs MST existent, le choix de départ ou les égalités peuvent conduire à un MST différent mais de même coût minimal.

## « Pourquoi le matching est uniquement sur les sommets impairs ? »

> Parce que seuls eux empêchent l'existence d'un circuit eulérien. Ajouter des arêtes aux sommets pairs serait inutile et augmenterait le coût.

## « Pourquoi un simple matching, pas n'importe quelles arêtes ? »

> Chaque sommet impair doit recevoir exactement une nouvelle incidence pour devenir pair avec le minimum de coût. Le perfect matching formalise précisément cela.

## « Pourquoi pas nearest neighbor ? »

> Ce serait une heuristique possible, mais le sujet impose Christofides et le génétique. Nearest neighbor n'offre pas la même garantie que Christofides.

## « Pourquoi pas brute force avec seulement 20 villes ? »

> `19!` reste beaucoup trop grand pour une recherche naïve en Python.

## « Pourquoi pas Held-Karp ? »

> Ce serait une excellente extension pour 20 villes car sa complexité `O(n²2^n)` est radicalement meilleure que `n!`, mais le sujet demande précisément Christofides et GA. On pourrait l'utiliser comme référence exacte si les ressources le permettent.

## « Votre GA peut-il produire une ville deux fois ? »

> Non si les opérateurs fonctionnent correctement : population initiale, OX, swap et inversion préservent tous la permutation.

## « Pourquoi le best-so-far ne se dégrade pas ? »

> Grâce à l'élitisme et au fait que nous conservons explicitement la meilleure distance historique.

---

# 72. Ce qu'il faut dire si le prof attaque les limites

Ne cherchez pas à défendre l'indéfendable. Une bonne réponse montre que vous comprenez vos hypothèses.

### « Vos routes traversent peut-être la mer ou les montagnes. »

> Oui. Haversine ne représente pas un réseau routier. C'est une abstraction conforme au sujet. Une version réelle utiliserait OpenStreetMap ou une API de routage.

### « Trois seeds, c'est peu. »

> Oui. C'est suffisant pour notre benchmark pédagogique, mais insuffisant pour une validation statistique forte. Une étude approfondie augmenterait le nombre de runs.

### « Vous n'avez pas prouvé l'optimum. »

> Exact. Nous parlons de meilleure solution observée. Le projet demande des solutions presque optimales et une comparaison, pas une preuve d'optimalité exacte.

### « Pourquoi ces hyperparamètres précisément ? »

> Nous avons défini trois profils et retenu celui qui avait la meilleure moyenne puis la meilleure stabilité dans nos runs. Nous ne prétendons pas avoir effectué une recherche exhaustive d'hyperparamètres.

---

# 73. Le raisonnement complet du projet — version que vous devez savoir raconter

Voici la meilleure réponse à une question du type :

**« Expliquez-moi votre projet de A à Z et justifiez vos choix. »**

> Le sujet nous donne 20 villes avec leurs coordonnées et nous demande de résoudre un TSP avec deux méthodes. Nous commençons donc par charger les coordonnées et calculer une distance de Haversine entre chaque paire, comme demandé. Comme toute paire possède une distance, nous modélisons un graphe complet, pondéré et non orienté. Haversine nous donne en plus un cadre métrique, ce qui rend Christofides pertinent.
>
> Pour Christofides, nous construisons d'abord un MST avec Prim. Le MST est intéressant parce qu'il relie toutes les villes à coût minimal et constitue une borne inférieure de la tournée optimale. Mais ce n'est pas encore un cycle. Nous identifions alors les sommets de degré impair, car un circuit eulérien exige des degrés pairs. Nous calculons un matching parfait minimum sur ces sommets afin de les rendre pairs en ajoutant le moins de distance possible. L'union du MST et du matching donne un multigraphe eulérien. Nous utilisons Hierholzer pour en extraire un circuit eulérien, puis nous supprimons les répétitions de villes. Le shortcut ne rallonge pas la tournée grâce à l'inégalité triangulaire. Cela donne une tournée hamiltonienne avec la garantie classique de Christofides : au plus 1,5 fois l'optimum dans le cas métrique.
>
> Pour la seconde approche, nous représentons chaque tournée par une permutation des 19 villes autres que Paris, Paris étant fixé comme ancre. Nous générons une population de permutations, puis nous faisons évoluer cette population avec sélection par tournoi, crossover OX, mutations swap ou inversion et élitisme. OX et les mutations sont choisis parce qu'ils préservent la validité des permutations. Comme le processus est stochastique, nous testons trois configurations sur plusieurs seeds et comparons moyenne, écart-type, meilleur et pire résultat. La configuration équilibrée est retenue car elle obtient la meilleure moyenne et la meilleure stabilité dans nos runs.
>
> Sur nos résultats, Christofides produit 3445,60 km et le génétique 3157,13 km, soit environ 288,48 km ou 8,37 % de moins pour le génétique. Le MST vaut 2665,05 km et sert de borne inférieure. Nous ne prétendons pas que 3157,13 km est l'optimum exact. Notre conclusion est donc que le génétique est meilleur ici si la priorité est la distance, tandis que Christofides est préférable si l'on privilégie rapidité, déterminisme et garantie théorique.

Si vous savez réellement expliquer ce paragraphe, vous maîtrisez le cœur du projet.

---

# 74. Glossaire ultra-compact

| Terme | Signification |
|---|---|
| TSP | tournée minimale visitant toutes les villes |
| sommet | ville |
| arête | liaison entre deux villes |
| poids | distance |
| graphe complet | toutes les paires sont reliées |
| graphe pondéré | les arêtes possèdent un coût |
| non orienté | A→B et B→A équivalents |
| métrique | distance respectant notamment l'inégalité triangulaire |
| cycle hamiltonien | visite chaque sommet une fois |
| circuit eulérien | traverse chaque arête une fois |
| degré | nombre d'arêtes incidentes |
| arbre | graphe connexe sans cycle |
| spanning tree | arbre couvrant tous les sommets |
| MST | spanning tree de poids minimum |
| Prim | algorithme de MST |
| matching | ensemble de paires sans sommet partagé |
| perfect matching | tous les sommets concernés sont appariés |
| multigraphe | plusieurs arêtes possibles entre deux sommets |
| Hierholzer | circuit eulérien |
| shortcut | suppression des revisites grâce à la métrique |
| approximation | méthode avec borne de qualité possible |
| heuristique | bonne solution sans garantie forte |
| métaheuristique | stratégie générale d'exploration |
| stochastique | utilise du hasard |
| chromosome | permutation représentant une tournée |
| population | ensemble de tournées candidates |
| sélection | choix de parents |
| tournoi | sélection du meilleur parmi un échantillon |
| crossover OX | croisement préservant une permutation |
| mutation swap | échange de deux positions |
| mutation inversion | renversement d'un segment |
| élitisme | conservation des meilleurs individus |
| seed | graine pseudo-aléatoire reproductible |
| convergence | stabilisation de la meilleure solution |
| optimum local | meilleur dans une région |
| optimum global | meilleur de tout l'espace |
| robustesse | stabilité des résultats |
| écart-type | dispersion des résultats |

---

# 75. Plan de révision conseillé

## Première passe — 20 minutes

Apprendre :

```text
TSP
Graphe
Haversine
Métrique
Hamilton vs Euler
Arbre
MST
Prim
```

## Deuxième passe — 20 minutes

Apprendre Christofides :

```text
MST
→ impairs
→ matching
→ eulérien
→ Hierholzer
→ shortcut
```

## Troisième passe — 20 minutes

Apprendre GA :

```text
individu
population
fitness/coût
sélection tournoi
OX
mutation
élitisme
seed
convergence
```

## Quatrième passe — 15 minutes

Résultats à connaître :

```text
MST          2665,05 km
Christofides 3445,60 km
GA           3157,13 km
Gain         288,48 km
Gain %       8,37 %
GA config    160 / 520 / tournoi 5 / crossover 95% / mutation 22% / élite 6
```

## Cinquième passe

Faire les questions de ce guide sans regarder les réponses.

---

# 76. Les 10 phrases que vous devez pouvoir dire sans hésiter

1. **Le TSP cherche un cycle hamiltonien de poids minimal.**
2. **Notre graphe est complet, pondéré et non orienté.**
3. **Haversine est imposé par le sujet et fournit une distance géographique métrique.**
4. **Le MST est une borne inférieure de l'optimum TSP.**
5. **Prim sert à construire le MST, pas à résoudre directement le TSP.**
6. **Christofides rend les degrés pairs grâce à un matching minimum.**
7. **Hierholzer trouve un circuit eulérien, puis le shortcut le transforme en cycle hamiltonien.**
8. **Christofides garantit au plus 1,5 fois l'optimum pour le TSP métrique.**
9. **Le GA explore des permutations par sélection, crossover, mutation et élitisme.**
10. **3157,13 km est notre meilleure solution observée, pas une preuve d'optimalité.**

---

# 77. Conclusion pédagogique

Le projet n'est pas une collection de termes indépendants.

Il raconte une seule histoire logique :

```text
Le TSP est trop grand pour la brute force.
        ↓
On modélise les villes en graphe métrique.
        ↓
Christofides exploite la structure mathématique du graphe.
        ↓
Le génétique explore l'espace des permutations expérimentalement.
        ↓
On compare une méthode garantie et déterministe
à une méthode stochastique capable de trouver mieux en pratique.
```

C'est cette logique qu'il faut comprendre plutôt que mémoriser des définitions isolées.
