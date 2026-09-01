# Le marchand ambulant — Présentation

## 1. Contexte

**Objectif :** aider Théobald à visiter 20 villes françaises, une seule fois chacune, puis revenir au point de départ en minimisant la distance totale.

Le problème correspond au **Travelling Salesman Problem (TSP)**, un problème NP-difficile. Avec 20 villes et un point de départ fixé, une recherche exhaustive devrait explorer jusqu'à `19!` tournées.

---

## 2. Modélisation

- 20 villes issues du CSV fourni.
- Une ville = un sommet du graphe.
- Une liaison entre chaque paire de villes = graphe complet.
- Poids des arêtes = distance géodésique calculée avec **Haversine**.
- Rayon terrestre utilisé : `6371.0088 km`.

La distance de Haversine est métrique, ce qui permet d'appliquer Christofides avec sa garantie théorique.

---

## 3. Christofides

Étapes implémentées :

1. Arbre couvrant minimal avec **Prim**.
2. Sommets de degré impair.
3. Matching parfait de poids minimal.
4. Multigraphe eulérien.
5. Parcours de **Hierholzer**.
6. Shortcut des sommets déjà visités pour obtenir un cycle hamiltonien.

**Résultat : 3445.60 km**

- MST : 2665.05 km
- Matching : 1142.03 km
- 12 sommets impairs
- Exécution observée : environ 2.26 ms

---

## 4. Algorithme génétique

Un individu est une permutation des villes, avec Paris fixé comme point d'ancrage.

- Sélection : tournoi
- Crossover : Ordered Crossover (OX)
- Mutation : swap ou inversion de segment
- Élitisme : conservation des meilleurs individus
- Fitness : distance totale de la tournée à minimiser

**Résultat retenu : 3157.13 km**

---

## 5. Paramètres testés

Trois configurations ont été comparées sur plusieurs seeds :

| Configuration | Population | Générations | Mutation | Résultat moyen |
|---|---:|---:|---:|---:|
| Rapide | 80 | 220 | 18% | 3216.15 km |
| **Équilibrée** | **160** | **520** | **22%** | **3157.13 km** |
| Exploratoire | 240 | 800 | 30% | 3216.15 km |

Configuration finale : tournoi 5, crossover 95%, mutation 22%, élite 6.

---

## 6. Comparaison des distances

- Christofides : **3445.60 km**
- Génétique : **3157.13 km**
- Différence : **288.48 km**
- Gain relatif du GA : **8.37%**

Sur cette instance, le génétique trouve donc la meilleure tournée observée.

---

## 7. Comparaison qualitative

| Critère | Christofides | Génétique |
|---|---|---|
| Distance observée | 3445.60 km | **3157.13 km** |
| Garantie théorique | **Oui : ≤ 1.5 × optimum** | Non |
| Vitesse | **Très rapide** | Plus lent |
| Déterminisme | **Oui** | Non, dépend du seed |
| Paramétrage | Faible | Important |
| Robustesse | Très forte | À tester sur plusieurs runs |

---

## 8. Itinéraires

Les cartes interactives sont disponibles dans :

- `results/route_christofides.html`
- `results/route_genetique.html`

Elles permettent de visualiser l'ordre des 20 villes et le retour à Paris.

---

## 9. Organisation du projet

Le travail a été organisé en blocs :

**Terminé :** données, Haversine, graphe complet, Prim/MST, Christofides, GA, benchmark, cartes, analyse comparative, README et présentation.

**Dernières vérifications :** dépôt GitHub public, répétition de l'oral et cohérence des slides.

Le détail du Kanban est disponible dans `TRELLO_ORGANISATION.md`.

---

## 10. Conclusion et recommandation

Pour cette instance de 20 villes, **l'algorithme génétique est recommandé si la priorité est la distance**, car la meilleure solution observée mesure 3157.13 km, soit 8.37% de moins que Christofides.

**Christofides reste préférable** lorsqu'on veut une solution très rapide, reproductible et accompagnée d'une garantie théorique.

Important : le résultat du GA est la meilleure solution observée pendant les essais ; il ne constitue pas une preuve d'optimalité globale.
