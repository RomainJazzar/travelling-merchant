# Questions probables du formateur — Le marchand ambulant

> Cette liste n'est **pas fournie par le sujet**. C'est une préparation à l'oral construite à partir des notions que le sujet demande explicitement de modéliser, expliquer et comparer, et de notre implémentation réelle.

Le guide détaillé est dans [`GUIDE_MATHS_ALGORITHMES.md`](GUIDE_MATHS_ALGORITHMES.md).

---

# Niveau 1 — indispensables

## 1. Quel est le problème que vous résolvez ?

Le TSP : trouver le cycle de distance minimale qui visite toutes les villes exactement une fois et revient au départ.

## 2. Pourquoi ne pas tester toutes les tournées ?

Avec 20 villes et un départ fixé, le sujet donne `(n-1)! = 19!`, soit environ `1,216 × 10^17` ordres possibles. La recherche brute devient irréaliste.

## 3. Comment avez-vous représenté le problème ?

Sous forme d'un graphe complet pondéré non orienté : une ville est un sommet, une liaison est une arête et son poids est la distance Haversine.

## 4. Pourquoi complet ?

Parce qu'on peut calculer Haversine entre chaque paire de villes.

## 5. Pourquoi non orienté ?

Parce que Haversine est symétrique : `d(A,B) = d(B,A)`.

## 6. Pourquoi Haversine ?

Le sujet l'impose et les données sont des coordonnées latitude/longitude.

## 7. Est-ce une vraie distance routière ?

Non. C'est une distance géographique de grand cercle, pas un réseau de routes.

## 8. C'est quoi un cycle hamiltonien ?

Un cycle qui visite chaque sommet exactement une fois puis revient au départ. Le TSP cherche le cycle hamiltonien de poids minimal.

## 9. C'est quoi un circuit eulérien ?

Un circuit qui traverse chaque arête exactement une fois et revient au départ.

## 10. Euler vs Hamilton ?

Euler = arêtes. Hamilton = sommets.

---

# Niveau 2 — MST / Prim

## 11. C'est quoi un arbre ?

Un graphe connexe sans cycle.

## 12. C'est quoi un spanning tree ?

Un arbre qui couvre tous les sommets du graphe.

## 13. C'est quoi un MST ?

Le Minimum Spanning Tree : l'arbre couvrant dont la somme des poids est minimale.

## 14. Pourquoi le MST est-il utile dans Christofides ?

Il relie toutes les villes avec une faible somme de distances et fournit une borne inférieure de l'optimum TSP.

## 15. Pourquoi est-il une borne inférieure ?

Si on retire une arête d'une tournée TSP optimale, on obtient un arbre couvrant. Le MST ne peut pas coûter davantage que cet arbre.

## 16. Pourquoi le MST n'est-il pas directement une tournée TSP ?

Parce qu'un arbre n'a pas de cycle et les degrés des sommets ne sont pas forcément 2.

## 17. Combien d'arêtes possède le MST avec 20 villes ?

`20 - 1 = 19`.

## 18. Pourquoi Prim ?

Prim calcule un MST, et le sujet cite explicitement Prim dans sa base de connaissances.

## 19. Prim vs Kruskal ?

Les deux calculent un MST. Prim fait grandir un arbre depuis un sommet ; Kruskal ajoute globalement les arêtes les moins chères sans créer de cycle.

## 20. Prim vs Dijkstra ?

Prim minimise le poids total d'un arbre couvrant ; Dijkstra minimise les distances de chemin depuis une source.

---

# Niveau 3 — Christofides

## 21. Donnez les étapes de Christofides.

`MST → sommets impairs → matching parfait minimum → multigraphe eulérien → Hierholzer → shortcut → tournée hamiltonienne`.

## 22. Pourquoi les sommets impairs ?

Parce qu'un graphe connexe possède un circuit eulérien lorsque tous ses degrés sont pairs.

## 23. Pourquoi le nombre de sommets impairs est-il pair ?

Le lemme de la poignée de main dit que la somme des degrés vaut `2|E|`, donc elle est paire ; le nombre de degrés impairs doit donc être pair.

## 24. C'est quoi un matching ?

Un ensemble d'arêtes ne partageant pas de sommet.

## 25. C'est quoi un perfect matching ?

Un matching qui apparie tous les sommets concernés exactement une fois.

## 26. Pourquoi minimum-weight ?

Parce qu'on veut rendre les degrés pairs en ajoutant le moins de distance possible.

## 27. Pourquoi les degrés deviennent-ils pairs ?

Chaque sommet impair reçoit exactement une nouvelle arête : `impair + 1 = pair`.

## 28. Pourquoi un multigraphe ?

Le matching peut ajouter une arête entre deux sommets déjà reliés dans le MST ; il faut conserver les deux occurrences.

## 29. Pourquoi le graphe est-il eulérien après MST + matching ?

Il reste connexe et tous les degrés sont pairs.

## 30. Que fait Hierholzer ?

Il construit un circuit eulérien en utilisant chaque arête exactement une fois.

## 31. Pourquoi faut-il ensuite un shortcut ?

Le circuit eulérien peut revisiter des villes alors que le TSP exige une seule visite par ville.

## 32. Pourquoi le shortcut n'augmente-t-il pas le coût ?

Grâce à l'inégalité triangulaire de la métrique.

## 33. Que garantit Christofides ?

Pour le TSP métrique : `C ≤ 1,5 × OPT`.

## 34. D'où vient le facteur 1,5 ?

`MST ≤ OPT` et `matching ≤ OPT/2`, donc `MST + matching ≤ 1,5 OPT`, puis le shortcut n'augmente pas la distance.

## 35. Est-ce une garantie d'optimalité ?

Non. C'est une garantie d'approximation.

---

# Niveau 4 — algorithme génétique

## 36. C'est quoi un individu ?

Une tournée candidate, représentée par une permutation des villes.

## 37. Pourquoi Paris n'est-il pas dans le chromosome ?

Paris est fixé comme ancre de départ/retour. Un cycle peut toujours être réécrit en commençant par Paris, donc on élimine une redondance sans perdre de solutions.

## 38. C'est quoi la population ?

L'ensemble des tournées candidates présentes dans une génération.

## 39. Votre fitness est quoi ?

Nous utilisons directement la distance totale comme coût à minimiser.

## 40. Comment sélectionnez-vous les parents ?

Par tournoi : plusieurs individus sont tirés au hasard et le plus court gagne.

## 41. Pourquoi tournoi ?

Simple, efficace et facile à régler avec la taille du tournoi.

## 42. C'est quoi la pression de sélection ?

L'intensité avec laquelle les meilleurs individus sont favorisés. Un tournoi plus grand augmente généralement cette pression.

## 43. Quel crossover utilisez-vous ?

Ordered Crossover (OX).

## 44. Pourquoi OX ?

Parce qu'un chromosome TSP doit rester une permutation valide sans ville dupliquée ou absente.

## 45. Quelles mutations utilisez-vous ?

Swap et inversion.

## 46. Pourquoi ces mutations ?

Elles modifient l'ordre tout en préservant une permutation valide.

## 47. Pourquoi la mutation est-elle nécessaire ?

Pour maintenir de la diversité et réduire le risque de rester bloqué dans un optimum local.

## 48. Pourquoi pas 100 % de mutation ?

Cela détruirait trop souvent les bonnes structures. Il faut équilibrer exploration et exploitation.

## 49. C'est quoi l'élitisme ?

La conservation automatique d'un certain nombre de meilleurs individus dans la génération suivante.

## 50. Pourquoi 6 élites ?

C'est le paramètre de la configuration équilibrée testée et retenue ; ce n'est pas une constante universelle.

## 51. Pourquoi 160 individus et 520 générations ?

Nous avons testé trois profils. La configuration équilibrée a obtenu la meilleure moyenne et la meilleure stabilité sur nos seeds.

## 52. Pourquoi plusieurs seeds ?

Parce que le GA est stochastique. Elles permettent de vérifier la robustesse et la reproductibilité.

## 53. Les seeds 11, 22 et 33 ont-elles une propriété spéciale ?

Non. Ce sont simplement trois graines distinctes et reproductibles.

## 54. C'est quoi la convergence ?

La stabilisation progressive de la meilleure solution au fil des générations.

## 55. C'est quoi un optimum local ?

Une solution meilleure que les solutions voisines mais pas forcément meilleure que toutes les solutions possibles.

---

# Niveau 5 — analyse des résultats

## 56. Résultat Christofides ?

`3445,60 km`.

## 57. Résultat GA ?

`3157,13 km`.

## 58. Différence ?

Environ `288,48 km`, soit `8,37 %` en faveur du génétique.

## 59. MST ?

`2665,05 km`.

## 60. Le GA est-il optimal ?

Pas prouvé. C'est la meilleure solution observée.

## 61. Pourquoi la meilleure solution observée peut-elle être supérieure à l'optimum ?

Parce qu'une métaheuristique n'explore pas nécessairement toutes les permutations.

## 62. Encadrement possible de l'optimum ?

Avec nos informations :

```text
2665,05 ≤ OPT ≤ 3157,13 km
```

Le MST donne la borne inférieure, et notre meilleure tournée valide donne une borne supérieure.

## 63. Pourquoi le génétique peut-il battre Christofides ?

La garantie de Christofides est une borne de pire cas, pas une promesse d'être meilleur que toutes les autres heuristiques sur chaque instance.

## 64. Quelle méthode est la plus rapide ?

Christofides dans notre implémentation.

## 65. Quelle méthode est la plus robuste ?

Christofides est naturellement plus reproductible car déterministe. Pour le GA, la robustesse est empirique et doit être mesurée sur plusieurs seeds.

## 66. Quelle méthode recommandez-vous ?

GA si la priorité est la distance observée ; Christofides si la priorité est rapidité, stabilité et garantie théorique.

---

# Niveau 6 — questions qui montrent si vous avez vraiment compris le code

## 67. Avez-vous utilisé la fonction Christofides toute faite de NetworkX ?

Non. La logique est implémentée dans `src/christofides.py`. NetworkX sert notamment à la structure du graphe et au matching minimum.

## 68. Pourquoi utiliser `heapq` dans Prim ?

Pour récupérer efficacement l'arête candidate de plus petit poids.

## 69. Pourquoi un `edge_id` dans Hierholzer ?

Parce qu'un multigraphe peut avoir plusieurs arêtes entre les mêmes sommets. Il faut distinguer chaque occurrence.

## 70. Pourquoi `seen` après Hierholzer ?

Pour supprimer les revisites et construire la tournée hamiltonienne finale.

## 71. Pourquoi `hamiltonian.append(hamiltonian[0])` ?

Pour fermer le cycle en revenant à la ville de départ.

## 72. Pourquoi la matrice est-elle symétrique ?

Parce que Haversine est symétrique : la distance A→B vaut B→A.

## 73. Pourquoi stocker les distances ?

Pour éviter de recalculer Haversine pendant chaque évaluation du GA et simplifier le code.

## 74. Pourquoi garder `history` dans le GA ?

Pour visualiser la convergence de la meilleure solution au fil des générations.

## 75. Comment choisissez-vous la meilleure configuration ?

Dans `main.py` : meilleure moyenne, puis plus faible écart-type, puis meilleur minimum.

---

# Niveau 7 — critique du projet

## 76. Première amélioration réaliste ?

Utiliser de vraies distances routières via OpenStreetMap / moteur de routage au lieu de Haversine si l'on voulait modéliser un vrai déplacement.

## 77. Amélioration algorithmique du GA ?

Ajouter 2-opt ou 3-opt après crossover/mutation ou sur les meilleurs individus.

## 78. Amélioration du benchmark ?

Utiliser davantage de seeds et des intervalles de confiance.

## 79. Comment certifier l'optimum pour 20 villes ?

Tester une méthode exacte comme Held-Karp ou un solveur TSP/ILP et comparer sa valeur à 3157,13 km.

## 80. Pourquoi ne l'avez-vous pas fait ?

Parce que le sujet demande principalement Christofides et l'algorithme génétique. Une méthode exacte serait une extension intéressante pour valider expérimentalement les résultats.

---

# Réponse finale de 60 secondes à apprendre

> Nous avons modélisé les 20 villes comme un graphe complet pondéré avec les distances de Haversine demandées par le sujet. Nous avons ensuite implémenté Christofides. Il part d'un MST calculé avec Prim, corrige les sommets impairs avec un matching parfait minimum, construit un multigraphe eulérien, applique Hierholzer puis un shortcut pour obtenir un cycle hamiltonien. Son intérêt est qu'il est rapide, déterministe et possède une garantie de 1,5 fois l'optimum dans le cas métrique. En parallèle, nous avons développé un algorithme génétique où chaque individu est une permutation des villes. Nous utilisons sélection par tournoi, crossover OX, mutation swap/inversion et élitisme. Plusieurs configurations et seeds permettent d'évaluer la robustesse. Christofides donne 3445,60 km et le génétique 3157,13 km, soit 8,37 % de moins. Nous recommandons donc le génétique si la priorité est la distance observée, mais Christofides reste la meilleure référence pour rapidité et garantie théorique. Et nous précisons que 3157,13 km est notre meilleure solution observée, pas une preuve de l'optimum global.
