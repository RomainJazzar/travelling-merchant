# FICHE DE RÉVISION ULTIME — Le marchand ambulant

> **À relire 10 minutes avant l'oral.** Tout ce qu'il faut, rien de plus.

---

## 1 · LES CHIFFRES À CONNAÎTRE PAR CŒUR

| Grandeur | Valeur |
|---|---:|
| Villes | **20** |
| Arêtes du graphe complet | **190** = 20 × 19 / 2 |
| Tournées possibles | **19!** ≈ 1,22 × 10¹⁷ |
| Rayon terrestre | 6 371,0088 km |
| **CHRISTOFIDES** | **3 445,60 km** |
| → poids du MST | 2 665,05 km |
| → poids du couplage | 1 142,03 km |
| → sommets de degré impair | **12** (donc 6 arêtes de couplage) |
| → circuit eulérien avant raccourcis | 3 807,08 km |
| → gain des raccourcis | 361,48 km |
| → temps observé | ≈ 1,5 ms *(dépend de la machine)* |
| **GÉNÉTIQUE** | **3 157,13 km** |
| → écart vs Christofides | **− 288,48 km = − 8,37 %** |
| → temps observé | ≈ 1,2 s / exécution *(dépend de la machine)* |
| → meilleur atteint à la génération | **67** sur 520 |
| **ENCADREMENT DE L'OPTIMUM** | **2 665,05 ≤ OPT ≤ 3 157,13** (fenêtre 492,07 km) |

### Configuration GA retenue — « équilibrée »

| Population | Générations | Tournoi k | Croisement | Mutation | Élite | Seeds |
|---:|---:|---:|---:|---:|---:|---|
| **160** | **520** | **5** | **95 %** | **22 %** | **6** | 11, 22, 33 |

### Benchmark (3 configs × 3 seeds)

| Config | Best | Moyenne | **σ** | Pire |
|---|---:|---:|---:|---:|
| rapide | 3 157,13 | 3 216,15 | 83,48 | 3 334,21 |
| **équilibrée** | 3 157,13 | **3 157,13** | **0,00** | 3 157,13 |
| exploratoire | 3 157,13 | 3 216,15 | 83,48 | 3 334,21 |

> **Les trois ont le même *best*.** C'est la **moyenne** et l'**écart-type** qui
> départagent. Rapide et exploratoire tombent sur les **deux mêmes attracteurs**
> (3 157,13 et 3 334,21) mais sur des seeds différents — d'où des stats identiques.

---

## 2 · LES FORMULES

**Haversine**
```
h = sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2)
d = 2 R · arcsin(√h)              R = 6 371,0088 km
```

**Nombre d'arêtes** `C(n,2) = n(n−1)/2` → 190
**Nombre de tournées** `(n−1)!` → 19! ; **et 19!/2** si on compte le sens
**Arbre** : n sommets → **n−1 arêtes**, aucun cycle
**Lemme des poignées de main** : `Σ deg(v) = 2|E|` → **nb de sommets impairs toujours PAIR**
**Inégalité triangulaire** : `d(A,C) ≤ d(A,B) + d(B,C)`
**Garantie Christofides** : `MST ≤ OPT` et `couplage ≤ OPT/2` ⟹ **≤ 1,5 × OPT**

---

## 3 · VOCABULAIRE ESSENTIEL

| Terme | En une ligne |
|---|---|
| **TSP** | cycle le plus court passant une fois par chaque ville, retour au départ |
| **NP-difficile** | aucun algorithme exact en temps polynomial connu (≠ impossible) |
| **Graphe complet** | toutes les paires reliées |
| **Métrique** | non-négativité + identité + symétrie + **inégalité triangulaire** |
| **TSP métrique** | TSP dont les distances sont une métrique → Christofides s'applique |
| **Degré** | nombre d'arêtes d'un sommet |
| **MST** | arbre couvrant de poids minimal — **pas une tournée** |
| **Couplage parfait** | arêtes sans sommet commun, couvrant TOUS les sommets |
| **Multigraphe** | autorise les arêtes parallèles |
| **Circuit EULÉRIEN** | chaque **ARÊTE** une fois — existe ssi tous degrés pairs |
| **Cycle HAMILTONIEN** | chaque **SOMMET** une fois — c'est le TSP |
| **Approximation** | heuristique **avec garantie** (Christofides oui, GA non) |
| **Métaheuristique** | schéma général de recherche (GA, recuit, fourmis) |
| **Stochastique** | dépend du hasard → dépend du seed |
| **Optimum local** | meilleur de son voisinage, pas de l'espace entier |
| **Fitness** | qualité d'un individu — ici la distance, **à minimiser** |
| **Élitisme** | les meilleurs passent tels quels à la génération suivante |
| **Seed** | graine du générateur pseudo-aléatoire → reproductibilité |
| **Borne inférieure** | valeur sous laquelle OPT ne descend pas (notre MST) |
| **Borne supérieure** | valeur au-dessus de laquelle OPT ne monte pas (notre meilleure tournée) |

---

## 4 · LA CHAÎNE CHRISTOFIDES

```
Graphe complet (20 sommets, 190 arêtes)
   ↓  PRIM
MST — 2 665,05 km, 19 arêtes            ← borne inférieure de OPT
   ↓  calcul des degrés
12 sommets de degré IMPAIR               ← toujours en nombre pair (poignées de main)
   ↓  COUPLAGE parfait de poids minimal
6 arêtes — 1 142,03 km                   ← minimal ⟹ ≤ OPT/2
   ↓  UNION (multigraphe)
25 arêtes, TOUS les degrés pairs          ← impair + 1 = pair
   ↓  HIERHOLZER
circuit eulérien — 3 807,08 km            ← villes répétées !
   ↓  SHORTCUTTING (inégalité triangulaire)
cycle hamiltonien — 3 445,60 km           ← gain 361,48 km
```

**Pourquoi chaque étape ?**
- MST → structure connexe la moins chère + borne inférieure
- degrés impairs → ils bloquent tout parcours eulérien
- couplage **parfait** → chaque impair doit être corrigé
- couplage **minimal** → (a) moins cher (b) preuve du `≤ OPT/2`
- union → tous degrés pairs ⟹ circuit eulérien existe
- Hierholzer → le construit en O(E)
- shortcut → Euler (arêtes) devient Hamilton (sommets), gratuitement

---

## 5 · LA CHAÎNE GÉNÉTIQUE

```
160 permutations aléatoires (Paris fixé, 19 gènes)
   ↓  ÉVALUATION : distance du cycle fermé [0]+ind+[0]   → à MINIMISER
   ↓  SÉLECTION : tournoi k=5, on garde le meilleur des 5
   ↓  CROISEMENT : Ordered Crossover, 95 %
        segment du parent 1 + villes manquantes dans l'ordre du parent 2
        ⟹ permutation TOUJOURS valide, aucune réparation
   ↓  MUTATION : 22 %, swap OU inversion (50/50)
        inversion = 2 arêtes modifiées = mouvement 2-opt
   ↓  ÉLITISME : 6 meilleurs conservés intacts
   ↓  × 520 générations                         → 83 200 évaluations
meilleure tournée = 3 157,13 km
```

---

## 6 · DIFFÉRENCES CLÉS

| | Christofides | Génétique |
|---|---|---|
| Nature | approximation **constructive** | métaheuristique **exploratoire** |
| Hasard | **aucun** | oui (seed) |
| Garantie | **≤ 1,5 × OPT** (métrique) | **aucune** |
| Distance | 3 445,60 km | **3 157,13 km** |
| Temps | **≈ 1,5 ms** | ≈ 1,2 s (≈ 1 000×) |
| Réglages | ~aucun | **6 hyperparamètres** |
| Robustesse | parfaite (déterministe) | σ = 0 km sur nos 3 seeds *(mais 3 seeds seulement)* |
| Plus de temps ? | ne change rien | peut améliorer |
| Nouvelles contraintes ? | ne s'adapte pas | **s'adapte** (on change la fitness) |

| | Euler | Hamilton |
|---|---|---|
| Compte | **arêtes** | **sommets** |
| Existe ssi | tous degrés pairs | **pas de critère simple** (NP-complet) |
| Algorithme | Hierholzer, O(E) | aucun efficace connu |

| | Prim | Kruskal | Dijkstra |
|---|---|---|---|
| But | MST | MST | plus courts chemins **depuis une source** |
| Structure | tas | union-find | tas |
| Chez nous | ✔ (graphe dense) | même poids | **autre problème** |

---

## 7 · LES 20 QUESTIONS LES PLUS PROBABLES

1. **Pourquoi pas tout tester ?** → 19! ≈ 1,2 × 10¹⁷ ≈ 4 ans à 10⁹/s.
2. **Pourquoi (n−1)! ?** → dans un cycle le départ n'importe pas ; n écritures du même cycle.
3. **Pourquoi 190 arêtes ?** → 20×19/2 ; on divise par 2 car non orienté (paires, pas couples).
4. **Pourquoi Haversine ?** → coordonnées sphériques ; 1° de longitude ≠ 1° de latitude.
5. **Pourquoi l'inégalité triangulaire ?** → elle rend le raccourci gratuit ⟹ garantie 1,5. *(vérifiée : 0 violation sur 6 840 triplets)*
6. **Pourquoi MST ≤ OPT ?** → retirer une arête à la tournée optimale donne un arbre couvrant.
7. **Pourquoi les sommets impairs sont-ils en nombre pair ?** → Σdeg = 2|E| est pair.
8. **Pourquoi un couplage *minimal* ?** → (a) coûte moins (b) c'est ce qui prouve ≤ OPT/2.
9. **Euler vs Hamilton ?** → arêtes vs sommets.
10. **D'où vient 1,5 ?** → MST ≤ OPT, couplage ≤ OPT/2, raccourci gratuit.
11. **Prim ou Kruskal ?** → même poids ; Prim car graphe dense + cité par le sujet.
12. **Prim ou Dijkstra ?** → problèmes différents : connexion totale vs distance à une source.
13. **Pourquoi OX ?** → garantit une permutation valide sans réparation + transmet l'ordre.
14. **Pourquoi la mutation ?** → sans elle, le croisement ne fait que recombiner → blocage.
15. **Pourquoi l'élitisme ?** → ne jamais perdre la meilleure solution trouvée.
16. **Pourquoi Paris fixé ?** → supprime les 20 écritures redondantes du même cycle.
17. **Pourquoi plusieurs seeds ?** → 1 exécution d'un algo stochastique ne dit rien. *(rapide : 3 334 au seed 11 !)*
18. **Comment choisissez-vous la config ?** → le **code** la choisit : moyenne, puis σ, puis best.
19. **C'est l'optimum ?** → **NON**. C'est la meilleure **observée**. OPT ∈ [2 665 ; 3 157].
20. **Votre plus grosse faiblesse ?** → benchmark à 3 seeds ; et 3 configs qui varient plusieurs paramètres à la fois.

---

## 8 · ⚠️ PIÈGES — NE JAMAIS DIRE

| ❌ | ✅ |
|---|---|
| « 3 157 km est l'optimum » | « la meilleure tournée **observée** » |
| « Christofides donne 1,5 × OPT » | « **au plus** 1,5 × OPT, en TSP **métrique** » |
| « le MST est une tournée » | « une structure de connexion ; son poids est une **borne inférieure** » |
| « le GA est meilleur que Christofides » | « **sur cette instance et avec nos réglages** » |
| « ça a convergé donc c'est l'optimum » | « ça ne progresse plus ; peut être un optimum **local** » |
| « 22 % est le taux optimal » | « valeur **empirique** de notre config la plus stable » |
| « l'algo met 0,68 s » | « ≈ 1 s **sur notre machine** — mesure expérimentale » |
| « 20! tournées » | « **(n−1)! = 19!** ; 19!/2 avec le sens » |
| « 380 arêtes » | « **190** — graphe non orienté » |
| « on a prouvé qu'il n'y a pas d'algo rapide » | « **P = NP est ouvert** » |
| « on a fait Christofides avec NetworkX » | « NetworkX **seulement pour le couplage** » |
| « σ = 0 prouve que c'est déterministe » | « nos 3 seeds ont convergé au même endroit » |
| « Haversine = distance réelle » | « **à vol d'oiseau** ; +15 à 30 % par la route » |
| « Dijkstra pour le MST » | « **Prim** ; Dijkstra = plus courts chemins » |

### Les 3 réflexes de langage
1. **« observée »**, jamais « optimale ».
2. **« au plus »**, jamais « égal à ».
3. **« sur cette instance »**, jamais « en général ».

### Si vous ne savez pas
> « Je ne suis pas certain, mais voici comment je raisonnerais : … Ce que je peux
> affirmer, c'est que … »

---

## 9 · LES 5 ARGUMENTS QUI FONT MOUCHE

1. **Zéro violation de l'inégalité triangulaire** sur les 6 840 triplets — vérifié, pas
   supposé. Notre instance est donc bien un TSP métrique.
2. **La garantie de Christofides donne OPT ≥ 2 297 km, moins bon que le MST (2 665 km)** —
   donc elle ne nous apprend rien de plus ici. Logique : elle vise le pire cas.
3. **On peut majorer l'écart à l'optimum sans le connaître** : GA ≤ 18,5 % au-dessus,
   Christofides ≤ 29,3 % — bien mieux que les 50 % garantis.
4. **Le meilleur est atteint dès la génération 67 sur 520** : 453 générations gaspillées.
   Un critère d'arrêt diviserait le temps par 3.
5. **Les 288 km se jouent dans le sud-est** : Christofides monte à Nice puis redescend sur
   Marseille (arêtes croisées) ; le GA fait Nîmes → Marseille → Toulon → Nice → Grenoble.

---

## 10 · LA CONCLUSION, MOT POUR MOT

> « Pour tracer sa route, nous recommandons **l'algorithme génétique** : 3 157,13 km, avec
> une configuration stable sur nos 3 seeds — 288 km économisés à chaque tournée.
>
> Mais nous gardons **Christofides comme filet de sécurité** : une très bonne tournée en
> 1,5 ms, sans réglage et sans hasard. C'est lui qu'on choisit si le temps devient
> critique ou si l'instance grandit.
>
> Et ce que nous savons vraiment : le MST, 2 665 km, est une borne inférieure **prouvée**.
> Notre meilleure tournée, 3 157 km, est une borne supérieure. L'optimum est entre les
> deux, dans une fenêtre de 492 km.
>
> **Nous ne livrons pas la tournée optimale. Nous livrons la meilleure tournée que nous
> sachions construire — et nous savons dire exactement ce qui nous en sépare.** »

---

## 11 · CHECK-LIST DES 5 DERNIÈRES MINUTES

- [ ] Le PPTX s'ouvre, les notes sont visibles en mode présentateur
- [ ] Le PDF est sur une clé USB, en secours
- [ ] Le dépôt GitHub est **public** et à jour
- [ ] `algogenetiques.py` (brouillon de cours cassé) est **supprimé** de la racine
- [ ] `results/route_christofides.html` et `route_genetique.html` s'ouvrent
- [ ] `python main.py` a été lancé une fois ce matin (≈ 35 s)
- [ ] Chacun sait qui parle sur quelle slide, et qui clique
- [ ] Les 3 réflexes de langage sont en tête : **observée · au plus · sur cette instance**

---

*Tous les chiffres viennent de `results/summary.json`, reproductible par `python main.py`.*
