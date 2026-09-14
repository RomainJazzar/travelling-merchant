"""Construit le PowerPoint de soutenance, slide par slide, notes comprises.

Lancer :  python tools/build_deck.py
Sortie :  FINAL_SOUTENANCE/Travelling_Merchant_Romain_Yannis_Lisa_FINAL.pptx
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

from tools.pptx_kit import (
    ASSETS, BG, CHRIST, CFG, CORAL, CYAN, GA, GAP, GAP_PCT, GOLD, GOLD_SOFT,
    GREEN, H, IMG_BOTTOM, IMG_LEFT, IMG_RIGHT, LINE, MATCH, MST, MUTED, ODD,
    OUT_PPTX, PANEL, PANEL_HI, S, TEXT, W,
    footer, fr, new_slide, notes, para, place_image, rect, slide_header,
    stat_card, textbox,
)

ROMAIN, YANNIS, LISA = "Romain", "Yannis", "Lisa"


# ===========================================================================
#  ROMAIN — poser le problème
# ===========================================================================
def s01(prs):
    slide = new_slide(prs)
    rect(slide, 0, 0, Inches(0.16), H, fill=GOLD, shape=MSO_SHAPE.RECTANGLE)
    place_image(slide, "01_carte_villes.png", Inches(7.35), Inches(0.25),
                Inches(13.20), Inches(7.25))
    rect(slide, Inches(6.75), 0, Inches(0.85), H, fill=BG,
         shape=MSO_SHAPE.RECTANGLE)

    tf = textbox(slide, Inches(0.95), Inches(1.42), Inches(6.0), Inches(0.4))
    para(tf, "PROJET D'ALGORITHMIQUE  ·  B3 IA", size=12.5, color=GOLD,
         bold=True, first=True)

    tf = textbox(slide, Inches(0.95), Inches(1.95), Inches(6.0), Inches(2.1))
    para(tf, "Le marchand", size=47, color=TEXT, bold=True, first=True,
         spacing=0.92)
    para(tf, "ambulant", size=47, color=TEXT, bold=True, spacing=0.92)

    rect(slide, Inches(0.95), Inches(4.05), Inches(1.5), Pt(2.4), fill=GOLD,
         shape=MSO_SHAPE.RECTANGLE)

    tf = textbox(slide, Inches(0.95), Inches(4.35), Inches(5.6), Inches(1.4))
    para(tf, "Problème du voyageur de commerce sur 20 villes françaises",
         size=15, color=MUTED, first=True, spacing=1.2)
    para(tf, "Christofides  vs  Algorithme génétique", size=19, color=CYAN,
         bold=True, space_before=10)

    tf = textbox(slide, Inches(0.95), Inches(6.10), Inches(5.6), Inches(0.9))
    para(tf, "Romain   ·   Yannis   ·   Lisa", size=16, color=TEXT, bold=True,
         first=True)
    para(tf, "github.com/RomainJazzar/travelling-merchant", size=11.5,
         color=MUTED, space_before=6)

    notes(slide, ROMAIN, "55 s",
          "Bonjour, nous sommes Romain, Yannis et Lisa. Notre projet, c'est le "
          "marchand ambulant, autrement dit le problème du voyageur de commerce. "
          "On nous demande d'aider Théobald à visiter vingt villes françaises, "
          "une seule fois chacune, puis à rentrer à son point de départ, en "
          "parcourant le moins de kilomètres possible. Nous avons implémenté les "
          "deux méthodes demandées : l'algorithme de Christofides et un "
          "algorithme génétique. À la fin, nous vous dirons laquelle nous "
          "recommandons, et surtout pourquoi. Je commence par le problème "
          "lui-même, Yannis prendra Christofides, et Lisa la partie génétique.",
          "J'enchaîne sur ce qui rend ce problème difficile.")


def s02(prs):
    slide = new_slide(prs)
    slide_header(slide, "Le problème",
                 "Pourquoi on ne peut pas simplement tout essayer",
                 "Visiter les 20 villes une seule fois, revenir au départ, "
                 "minimiser la distance totale.")
    place_image(slide, "07_explosion_combinatoire.png", Inches(0.55),
                Inches(1.78), Inches(8.55), IMG_BOTTOM)
    x, w = Inches(8.90), Inches(3.88)
    for i, (val, lab, col, vs) in enumerate([
            ("20", "villes à visiter, départ et retour à Paris", GOLD, 27),
            ("19 !", "ordres possibles une fois le départ fixé", CYAN, 27),
            ("NP-difficile", "aucun algorithme exact rapide connu", CORAL, 19)]):
        stat_card(slide, x, Inches(1.95) + Inches(1.30) * i, w, Inches(1.12),
                  val, lab, color=col, vsize=vs, lsize=11)
    tf = textbox(slide, x, Inches(6.00), w, Inches(1.0))
    para(tf, "Le sujet le formule ainsi : trouver le chemin le plus court parmi "
             "les (n−1)! possibles, « et ça bien sûr sans tous les évaluer ».",
         size=12, color=GOLD_SOFT, italic=True, first=True, spacing=1.25)
    footer(slide, 2, ROMAIN)

    notes(slide, ROMAIN, "1 min 10",
          "Le TSP consiste à trouver le cycle le plus court qui passe une fois "
          "par chaque ville et revient au point de départ. Le réflexe naturel, "
          "c'est de dire : essayons tous les ordres possibles et gardons le "
          "meilleur. Le problème, c'est que si on fixe la ville de départ, il "
          "reste dix-neuf factorielle ordres, c'est-à-dire environ cent vingt "
          "millions de milliards de tournées. Même en évaluant un milliard de "
          "tournées par seconde, il faudrait près de quatre ans de calcul pour "
          "une seule instance. Et attention à l'échelle du graphique : elle est "
          "logarithmique, donc chaque graduation vaut dix fois la précédente. "
          "C'est pour ça que le TSP est dit NP-difficile : on ne connaît aucun "
          "algorithme exact qui reste rapide quand le nombre de villes augmente. "
          "Notre objectif n'est donc pas de trouver la solution parfaite, mais "
          "une très bonne solution, en un temps raisonnable.",
          "Avant de chercher, il faut traduire ce problème en objet mathématique.")


def s03(prs):
    slide = new_slide(prs)
    slide_header(slide, "Modélisation", "Du territoire de Théobald à un graphe",
                 "Un sommet = une ville.  Une arête = une liaison.  "
                 "Un poids = une distance.")
    place_image(slide, "02_graphe_complet.png", Inches(0.55), Inches(1.78),
                Inches(6.55), IMG_BOTTOM)
    x, w = Inches(6.95), Inches(5.83)
    rows = [
        ("Complet", "Toutes les paires de villes sont reliées : on sait calculer "
         "la distance entre n'importe lesquelles.", CYAN),
        ("Pondéré", "Le poids d'une arête est la distance de Haversine entre les "
         "deux villes.", CYAN),
        ("Non orienté", "d(A,B) = d(B,A) : aller de Lyon à Nice coûte autant que "
         "l'inverse.", CYAN),
        ("190 arêtes", "C(20,2) = 20 × 19 / 2. On divise par deux car une arête "
         "relie une paire, pas un couple ordonné.", GOLD),
    ]
    for i, (title, body, col) in enumerate(rows):
        y = Inches(1.95) + Inches(1.26) * i
        rect(slide, x, y, w, Inches(1.08), fill=PANEL, line=LINE, lw=1.0)
        rect(slide, x, y, Inches(0.045), Inches(1.08), fill=col,
             shape=MSO_SHAPE.RECTANGLE)
        tf = textbox(slide, x + Inches(0.28), y + Inches(0.14), w - Inches(0.52),
                     Inches(0.82))
        para(tf, title, size=15, color=col, bold=True, first=True, spacing=0.95)
        para(tf, body, size=11.5, color=MUTED, space_before=4, spacing=1.14)
    footer(slide, 3, ROMAIN)

    notes(slide, ROMAIN, "1 min 05",
          "Pour résoudre le problème, on le traduit en théorie des graphes. "
          "Chaque ville devient un sommet, chaque liaison possible devient une "
          "arête, et le poids de l'arête est la distance entre les deux villes. "
          "Notre graphe a trois propriétés importantes. Il est complet, parce "
          "qu'on sait calculer une distance entre n'importe quelle paire de "
          "villes : Théobald n'est bloqué par aucune route manquante. Il est "
          "pondéré, puisque chaque arête porte une distance. Et il est non "
          "orienté, parce que la distance de Lyon à Nice est la même que de Nice "
          "à Lyon. Conséquence directe : avec vingt sommets, on a cent "
          "quatre-vingt-dix arêtes, soit vingt fois dix-neuf divisé par deux. On "
          "divise par deux parce qu'une arête relie une paire de villes, pas un "
          "couple ordonné : l'arête Paris-Lyon et l'arête Lyon-Paris, c'est la "
          "même.",
          "Reste à savoir comment on calcule concrètement ces 190 distances.")


def s04(prs):
    slide = new_slide(prs)
    slide_header(slide, "Distance", "Haversine, et pourquoi ce choix compte",
                 "Nos données sont des latitudes et des longitudes : ce ne sont "
                 "pas des coordonnées dans un plan.")
    place_image(slide, "08_haversine.png", IMG_LEFT, Inches(1.82),
                IMG_RIGHT, Inches(6.48))
    tf = textbox(slide, Inches(0.75), Inches(6.58), Inches(11.83), Inches(0.42))
    para(tf, "Pas d'euclidien : la Terre est courbe.      Pas d'API routière : "
             "les temps de trajet réels ne garantissent pas l'inégalité "
             "triangulaire. Or c'est elle qui fait de notre instance un "
             "TSP métrique — le seul cas où Christofides garantit ≤ 1,5 × OPT.",
         size=12, color=GOLD_SOFT, first=True, align=PP_ALIGN.CENTER,
         spacing=1.2)
    footer(slide, 4, ROMAIN)

    notes(slide, ROMAIN, "1 min 30",
          "Nos données sont des latitudes et des longitudes, donc des points sur "
          "une sphère. Si on appliquait Pythagore directement sur ces nombres, on "
          "additionnerait des degrés de latitude et des degrés de longitude, qui "
          "ne représentent pas la même distance selon l'endroit où on se trouve. "
          "La formule de Haversine, elle, calcule la longueur de l'arc de grand "
          "cercle entre deux points : la vraie distance à vol d'oiseau sur la "
          "surface de la Terre. On prend un rayon terrestre de six mille trois "
          "cent soixante et onze kilomètres. Le point vraiment important est à "
          "droite. Haversine est une métrique : elle est positive, nulle "
          "uniquement entre une ville et elle-même, symétrique, et surtout elle "
          "respecte l'inégalité triangulaire. Passer par une ville intermédiaire "
          "ne peut jamais raccourcir le trajet. Retenez bien cette dernière "
          "propriété : c'est exactement l'hypothèse dont Christofides a besoin "
          "pour que sa garantie tienne. Et c'est aussi pour ça que nous n'avons "
          "pas pris de distances routières réelles : elles ne respectent pas "
          "forcément cette propriété, et on perdrait la garantie. En contrepartie, "
          "nos distances sont à vol d'oiseau, donc plus courtes que la réalité — "
          "nous y reviendrons dans les limites.",
          "On a un graphe et des distances : il reste à choisir comment chercher.")


def s05(prs):
    slide = new_slide(prs)
    slide_header(slide, "Deux approches", "Construire, ou explorer",
                 "Le sujet impose les deux, puis demande de les comparer sur la "
                 "distance, le temps, la facilité d'implémentation et la robustesse.")
    place_image(slide, "20_deux_strategies.png", IMG_LEFT, Inches(1.82),
                IMG_RIGHT, IMG_BOTTOM)
    footer(slide, 5, ROMAIN)

    notes(slide, ROMAIN, "50 s",
          "Il existe deux grandes familles de réponses à ce type de problème. À "
          "gauche, l'approche constructive : Christofides. On construit la "
          "tournée étape par étape, avec des outils de théorie des graphes. C'est "
          "déterministe, donc une seule exécution suffit, et surtout on dispose "
          "d'une garantie mathématique prouvée. À droite, l'approche "
          "exploratoire : l'algorithme génétique. On ne construit rien du tout, "
          "on fait évoluer une population de tournées candidates. C'est "
          "stochastique, il faut donc plusieurs exécutions pour parler "
          "sérieusement d'un résultat, et il n'y a aucune garantie d'optimalité. "
          "Ce sont vraiment deux philosophies opposées, et c'est tout l'intérêt "
          "de les comparer sur exactement la même instance.",
          "Yannis va vous détailler la première : Christofides.")


# ===========================================================================
#  YANNIS — Christofides
# ===========================================================================
def s06(prs):
    slide = new_slide(prs)
    slide_header(slide, "Christofides", "Huit étapes, et pas une de trop",
                 "Chaque transformation répare un défaut de l'étape précédente.")
    place_image(slide, "09_pipeline_christofides.png", IMG_LEFT, Inches(1.82),
                IMG_RIGHT, IMG_BOTTOM)
    footer(slide, 6, YANNIS)

    notes(slide, YANNIS, "1 min 15",
          "Merci Romain. Voici la chaîne complète de Christofides. Je vous donne "
          "d'abord la vue d'ensemble, puis on reprend les étapes clés une par "
          "une. On part du graphe complet. On construit un arbre couvrant "
          "minimal, qui relie toutes les villes au coût le plus faible, mais qui "
          "n'est pas une tournée. Dans cet arbre, certains sommets ont un degré "
          "impair : on les apparie deux à deux au coût le plus bas possible. En "
          "ajoutant ces arêtes à l'arbre, on obtient un multigraphe où tous les "
          "degrés sont pairs, ce qui garantit l'existence d'un circuit eulérien. "
          "On le parcourt avec Hierholzer, puis on supprime les villes déjà "
          "visitées. On obtient enfin un vrai cycle hamiltonien : notre tournée. "
          "Ce qu'il faut retenir, c'est que chaque étape corrige un défaut précis "
          "de la précédente, et qu'au bout de la chaîne on a une garantie : la "
          "tournée ne dépasse jamais une fois et demie l'optimum.",
          "On commence par la première brique : l'arbre couvrant minimal.")


def s07(prs):
    slide = new_slide(prs)
    slide_header(slide, "Étape 1",
                 "L'arbre couvrant minimal, construit avec Prim",
                 "Relier les 20 villes au coût total le plus faible, sans jamais "
                 "créer de cycle.")
    place_image(slide, "03_mst_prim.png", Inches(0.55), Inches(1.78),
                Inches(6.35), IMG_BOTTOM)
    x, w = Inches(6.80), Inches(5.98)
    stat_card(slide, x, Inches(1.92), w, Inches(1.14), f"{fr(MST)} km",
              "Poids total du MST  ·  19 arêtes pour 20 sommets", color=CYAN,
              vsize=27, lsize=12)
    rows = [
        ("Pourquoi un arbre ?", "Un arbre connecte tout sans redondance : n "
         "sommets, n−1 arêtes, aucun cycle. C'est le squelette le moins cher."),
        ("Pourquoi Prim ?", "On part d'une ville et on ajoute à chaque tour "
         "l'arête la moins chère qui atteint une ville pas encore reliée. Un tas "
         "binaire garde cette arête à portée de main."),
        ("Pourquoi c'est une borne ?", "Retirez une arête à la tournée "
         "optimale : vous obtenez un arbre couvrant. Donc MST ≤ OPT. Nous tenons "
         "déjà une borne inférieure valable."),
    ]
    for i, (t, b) in enumerate(rows):
        y = Inches(3.22) + Inches(1.24) * i
        rect(slide, x, y, w, Inches(1.08), fill=PANEL, line=LINE, lw=1.0)
        tf = textbox(slide, x + Inches(0.28), y + Inches(0.13), w - Inches(0.52),
                     Inches(0.85))
        para(tf, t, size=13.5, color=GOLD, bold=True, first=True, spacing=0.95)
        para(tf, b, size=11.5, color=MUTED, space_before=3, spacing=1.1)
    footer(slide, 7, YANNIS)

    notes(slide, YANNIS, "1 min 30",
          "Un arbre couvrant, c'est un sous-graphe qui touche toutes les villes "
          "sans jamais former de boucle. Avec vingt sommets, il a exactement "
          "dix-neuf arêtes. Le minimal, c'est celui dont la somme des poids est "
          "la plus faible : chez nous, deux mille six cent soixante-cinq "
          "kilomètres. Je l'ai implémenté avec l'algorithme de Prim : on part "
          "d'une ville, et à chaque tour on ajoute l'arête la moins chère qui "
          "relie une ville pas encore atteinte. On utilise un tas binaire pour "
          "retrouver cette arête rapidement. Attention à ne pas confondre avec "
          "Dijkstra : Dijkstra minimise la distance depuis un point de départ, "
          "Prim minimise le coût total de connexion de tout le réseau. Kruskal "
          "aurait donné exactement le même poids, c'est simplement une autre "
          "façon de le construire. Petit détail que nous avons vérifié : le "
          "sommet de départ de Prim ne change pas le poids final, nous l'avons "
          "testé pour les vingt villes. Et surtout, ce poids est une borne "
          "inférieure de l'optimum du TSP : si on prend la tournée optimale et "
          "qu'on lui enlève une arête, on obtient un arbre couvrant, qui coûte "
          "donc au moins autant que le minimal. On y reviendra à la fin.",
          "Ce squelette n'est pas une tournée : voyons ce qui lui manque.")


def s08(prs):
    slide = new_slide(prs)
    slide_header(slide, "Étape 2",
                 "De l'arbre au cycle : réparer les degrés impairs",
                 "Pour emprunter chaque arête une seule fois, il faut pouvoir "
                 "entrer et ressortir de chaque sommet.")
    place_image(slide, "04_impairs_matching.png", Inches(0.55), Inches(1.78),
                Inches(6.35), IMG_BOTTOM)
    x, w = Inches(6.80), Inches(5.98)
    cw = (w - Inches(0.16)) / 2
    stat_card(slide, x, Inches(1.92), cw, Inches(1.10), str(ODD),
              "sommets de degré impair dans le MST", color=GOLD, vsize=27)
    stat_card(slide, x + cw + Inches(0.16), Inches(1.92), cw, Inches(1.10),
              f"{fr(MATCH)} km", "coût du couplage parfait minimal", color=CORAL,
              vsize=21)
    rows = [
        ("Ils sont toujours en nombre PAIR", "Lemme des poignées de main : la "
         "somme des degrés vaut 2 × le nombre d'arêtes, elle est donc paire. Il "
         "ne peut pas y avoir un nombre impair de termes impairs."),
        ("Couplage parfait de poids minimal", "On les apparie deux à deux, chacun "
         "dans exactement une paire, en minimisant la somme des distances. Ici : "
         "6 arêtes pour 12 sommets."),
        ("Pourquoi ça règle le problème", "Ajouter une arête à un sommet augmente "
         "son degré de 1 : impair + 1 = pair. Après l'union, TOUS les degrés sont "
         "pairs."),
    ]
    for i, (t, b) in enumerate(rows):
        y = Inches(3.18) + Inches(1.26) * i
        rect(slide, x, y, w, Inches(1.10), fill=PANEL, line=LINE, lw=1.0)
        tf = textbox(slide, x + Inches(0.28), y + Inches(0.12), w - Inches(0.52),
                     Inches(0.9))
        para(tf, t, size=13, color=GOLD, bold=True, first=True, spacing=0.95)
        para(tf, b, size=11, color=MUTED, space_before=3, spacing=1.1)
    footer(slide, 8, YANNIS)

    notes(slide, YANNIS, "1 min 25",
          "Le degré d'un sommet, c'est son nombre d'arêtes. Dans notre arbre, "
          "douze villes ont un degré impair, elles sont en doré sur la carte. "
          "Pourquoi est-ce un problème ? Parce que pour traverser une ville sans "
          "s'y arrêter, il faut y entrer par une arête et en ressortir par une "
          "autre : les arêtes vont par paires. Un sommet de degré impair bloque "
          "donc le parcours. Premier point mathématique : ces sommets sont "
          "forcément en nombre pair. C'est le lemme des poignées de main : si on "
          "additionne tous les degrés, on compte chaque arête deux fois, donc la "
          "somme est paire ; et une somme paire ne peut pas contenir un nombre "
          "impair de termes impairs. Comme ils sont en nombre pair, on peut les "
          "apparier deux à deux. On cherche le couplage parfait de poids "
          "minimal : chaque sommet impair dans exactement une paire, et la somme "
          "des distances la plus petite possible. Chez nous, six arêtes pour mille "
          "cent quarante-deux kilomètres, en rouge sur la carte. En les ajoutant à "
          "l'arbre, chaque sommet impair gagne exactement un degré, et devient "
          "donc pair.",
          "Un graphe connexe dont tous les degrés sont pairs a une propriété "
          "remarquable.")


def s09(prs):
    slide = new_slide(prs)
    slide_header(slide, "Étape 3", "Euler, Hamilton, et le raccourci",
                 "Le passage du circuit eulérien à la tournée finale — et d'où "
                 "vient exactement le facteur 1,5.")
    place_image(slide, "21_euler_hamilton_raccourci.png", IMG_LEFT, Inches(1.82),
                IMG_RIGHT, IMG_BOTTOM)
    footer(slide, 9, YANNIS)

    notes(slide, YANNIS, "1 min 20",
          "Un graphe connexe dont tous les degrés sont pairs possède toujours un "
          "circuit eulérien : un parcours qui emprunte chaque arête exactement "
          "une fois et revient au départ. C'est l'algorithme de Hierholzer qui le "
          "construit. Mais attention, ce n'est pas encore une tournée pour "
          "Théobald, parce qu'un circuit eulérien raisonne en arêtes, pas en "
          "sommets : certaines villes y apparaissent plusieurs fois. Le TSP, lui, "
          "cherche un cycle hamiltonien, qui passe une seule fois par chaque "
          "sommet. C'est la distinction essentielle : Euler compte les arêtes, "
          "Hamilton compte les sommets. On fait donc la conversion en parcourant "
          "le circuit et en sautant toute ville déjà visitée. Et c'est là que "
          "l'inégalité triangulaire dont parlait Romain revient : si on passait "
          "par A, puis B, puis C, et qu'on saute B, on remplace la distance A-B "
          "plus B-C par la distance A-C, qui est forcément inférieure ou égale. "
          "Le raccourci ne rallonge donc jamais la tournée. Si on met tout bout à "
          "bout : le MST coûte au plus l'optimum, le couplage coûte au plus la "
          "moitié de l'optimum, et les raccourcis n'ajoutent rien. D'où la "
          "garantie d'une fois et demie l'optimum — valable uniquement parce que "
          "nos distances sont métriques.",
          "Voyons ce que ça donne concrètement sur la carte de Théobald.")


def s10(prs):
    slide = new_slide(prs)
    slide_header(slide, "Résultat", "L'itinéraire proposé par Christofides",
                 "Tournée complète, départ et retour à Paris, chaque ville "
                 "visitée exactement une fois.")
    place_image(slide, "05_route_christofides.png", Inches(0.55), Inches(1.78),
                Inches(6.55), IMG_BOTTOM)
    x, w = Inches(6.95), Inches(5.83)
    stat_card(slide, x, Inches(1.92), w, Inches(1.28), f"{fr(CHRIST)} km",
              "Distance totale de la tournée Christofides", color=CYAN, vsize=33,
              lsize=12.5)
    cw = (w - Inches(0.16)) / 2
    stat_card(slide, x, Inches(3.34), cw, Inches(1.02), f"{fr(MST, 0)} km",
              "arbre couvrant minimal", color=MUTED, vsize=19)
    stat_card(slide, x + cw + Inches(0.16), Inches(3.34), cw, Inches(1.02),
              f"{fr(MATCH, 0)} km", "couplage minimal", color=CORAL, vsize=19)
    stat_card(slide, x, Inches(4.50), cw, Inches(1.02), str(ODD),
              "sommets de degré impair", color=GOLD, vsize=19)
    stat_card(slide, x + cw + Inches(0.16), Inches(4.50), cw, Inches(1.02),
              "≈ 1,5 ms", "temps mesuré sur notre machine", color=GREEN, vsize=19)
    tf = textbox(slide, x, Inches(5.76), w, Inches(1.1))
    para(tf, "Le temps d'exécution est une mesure expérimentale, pas une "
             "constante universelle : il dépend de la machine. Ce qui est "
             "structurel, c'est l'ordre de grandeur — quelques millisecondes.",
         size=11.5, color=GOLD_SOFT, italic=True, first=True, spacing=1.22)
    footer(slide, 10, YANNIS)

    notes(slide, YANNIS, "1 min 15",
          "Voici la tournée que Christofides propose à Théobald. Elle part de "
          "Paris, passe par Le Havre, Rennes, Nantes, descend la façade "
          "atlantique jusqu'à Toulouse, longe la Méditerranée, remonte par les "
          "Alpes et Lyon, puis revient par Dijon, Strasbourg, Reims et Lille. "
          "Trois mille quatre cent quarante-cinq virgule six kilomètres. Les "
          "numéros sur la carte donnent l'ordre de passage : vous pouvez vérifier "
          "qu'aucune ville n'apparaît deux fois et qu'on revient bien au départ. "
          "À droite, le détail du calcul : l'arbre couvrant pesait deux mille six "
          "cent soixante-cinq kilomètres, le couplage a ajouté mille cent "
          "quarante-deux kilomètres, ce qui ferait trois mille huit cent sept ; "
          "et les raccourcis ont fait redescendre le total à trois mille quatre "
          "cent quarante-cinq. Côté temps, on est autour d'une milliseconde et "
          "demie sur nos machines. Je précise que c'est une mesure "
          "expérimentale : sur une autre machine le chiffre changera, ce qui "
          "reste vrai c'est l'ordre de grandeur, quelques millisecondes.",
          "Lisa va maintenant vous montrer une approche radicalement différente.")


# ===========================================================================
#  LISA — l'algorithme génétique, la comparaison, la conclusion
# ===========================================================================
def s11(prs):
    slide = new_slide(prs)
    slide_header(slide, "Algorithme génétique",
                 "On ne construit pas la tournée : on la fait évoluer",
                 "Un individu = une tournée complète. Une population = 160 "
                 "Théobald d'univers parallèles.")
    place_image(slide, "12_pipeline_ga.png", Inches(0.55), Inches(1.82),
                Inches(8.35), IMG_BOTTOM)
    x, w = Inches(8.70), Inches(4.08)
    rows = [
        ("Individu / chromosome", "une permutation des 19 villes ; Paris est "
         "fixé comme point d'ancrage", CYAN),
        ("Gène", "une ville à une position donnée dans la tournée", CYAN),
        ("Fitness", "la distance totale du cycle, retour au départ compris — "
         "à MINIMISER", GOLD),
        ("Génération", "un tour complet du cycle : évaluer, sélectionner, "
         "croiser, muter", GREEN),
    ]
    for i, (t, b, col) in enumerate(rows):
        y = Inches(1.95) + Inches(1.22) * i
        rect(slide, x, y, w, Inches(1.06), fill=PANEL, line=LINE, lw=1.0)
        rect(slide, x, y, Inches(0.045), Inches(1.06), fill=col,
             shape=MSO_SHAPE.RECTANGLE)
        tf = textbox(slide, x + Inches(0.26), y + Inches(0.13), w - Inches(0.5),
                     Inches(0.82))
        para(tf, t, size=13, color=col, bold=True, first=True, spacing=0.95)
        para(tf, b, size=10.5, color=MUTED, space_before=3, spacing=1.12)
    tf = textbox(slide, Inches(0.55), Inches(6.52), Inches(8.0), Inches(0.42))
    para(tf, "Pourquoi fixer Paris ? Paris→Lyon→Nice→Paris et "
             "Lyon→Nice→Paris→Lyon sont le même cycle, simplement décalé. "
             "Fixer un point supprime ces doublons de représentation.",
         size=11, color=GOLD_SOFT, italic=True, first=True, spacing=1.18)
    footer(slide, 11, LISA)

    notes(slide, LISA, "1 min 20",
          "Merci Yannis. L'algorithme génétique ne construit rien : il part de "
          "solutions au hasard et les fait évoluer, exactement comme une "
          "population biologique. Le vocabulaire, c'est celui de la génétique. Un "
          "individu, c'est une tournée complète — le sujet parle joliment de "
          "Théobald d'univers parallèles. Son chromosome, c'est la permutation "
          "des villes ; un gène, c'est une ville à une position donnée. La "
          "fitness, c'est la distance totale du cycle, retour au départ compris, "
          "et ici on cherche à la minimiser : plus la distance est faible, "
          "meilleur est l'individu. Une génération, c'est un tour complet de la "
          "boucle que vous voyez à gauche : on évalue, on sélectionne, on croise, "
          "on mute, et on repart. Nous en faisons cinq cent vingt. Un détail "
          "d'implémentation important : nous avons fixé Paris comme point "
          "d'ancrage et le chromosome ne contient que les dix-neuf autres villes. "
          "La raison, c'est qu'une tournée cyclique reste la même si on la "
          "décale : Paris-Lyon-Nice-Paris et Lyon-Nice-Paris-Lyon, c'est le même "
          "cycle. Fixer un point supprime ces représentations redondantes sans "
          "supprimer aucune solution.",
          "Regardons maintenant en détail les opérateurs qui font cette évolution.")


def s12(prs):
    slide = new_slide(prs)
    slide_header(slide, "Les opérateurs",
                 "Quatre mécanismes, une contrainte commune",
                 "Chaque opérateur doit produire une permutation valide : aucune "
                 "ville perdue, aucune ville en double.")
    place_image(slide, "22_operateurs.png", IMG_LEFT, Inches(1.82),
                IMG_RIGHT, IMG_BOTTOM)
    footer(slide, 12, LISA)

    notes(slide, LISA, "1 min 40",
          "Voici nos quatre opérateurs. Je commence par le croisement, en haut à "
          "gauche, parce que c'est le plus subtil. Si on prenait un croisement "
          "naïf — la première moitié du parent un, la seconde moitié du parent "
          "deux — on obtiendrait une tournée invalide : certaines villes "
          "apparaîtraient deux fois, d'autres disparaîtraient. Le Ordered "
          "Crossover règle ça : on conserve un segment du parent un, en doré, "
          "puis on complète les cases vides en parcourant le parent deux dans "
          "l'ordre, en ignorant les villes déjà présentes. Le résultat est "
          "toujours une permutation valide. Ensuite la mutation, en bas à gauche. "
          "Nous en utilisons deux : l'échange, qui permute deux villes, et "
          "l'inversion, qui retourne un segment entier. Les deux préservent la "
          "permutation par construction. La mutation sert à explorer : sans elle, "
          "la population s'appauvrit et on reste coincé. Trop de mutation, à "
          "l'inverse, et la recherche devient du hasard pur. À droite, la "
          "sélection par tournoi : on tire cinq individus au hasard et on garde "
          "le meilleur comme parent. C'est plus simple et plus stable que la "
          "roulette, et le paramètre k règle la pression de sélection. Enfin "
          "l'élitisme : les six meilleures tournées passent telles quelles à la "
          "génération suivante, ce qui garantit que la meilleure solution connue "
          "n'est jamais perdue.",
          "Ces opérateurs ont des réglages : voyons comment nous les avons choisis.")


def s13(prs):
    slide = new_slide(prs)
    slide_header(slide, "Paramétrage",
                 "Trois configurations, trois seeds, un choix argumenté",
                 "Le sujet demande de tester différentes configurations : voici "
                 "ce que nous avons mesuré.")
    place_image(slide, "16_benchmark.png", Inches(0.55), Inches(1.82),
                Inches(8.15), IMG_BOTTOM)

    x, w = Inches(8.95), Inches(3.83)
    rect(slide, x, Inches(1.92), w, Inches(3.05), fill=PANEL_HI, line=GOLD,
         lw=1.6)
    tf = textbox(slide, x + Inches(0.28), Inches(2.06), w - Inches(0.56),
                 Inches(0.4))
    para(tf, "CONFIGURATION RETENUE", size=11, color=GOLD, bold=True, first=True)
    para(tf, "« équilibrée »", size=17, color=TEXT, bold=True, space_before=2)
    params = [("Population", CFG["population_size"]),
              ("Générations", CFG["generations"]),
              ("Tournoi (k)", CFG["tournament_size"]),
              ("Croisement", f"{int(CFG['crossover_rate'] * 100)} %"),
              ("Mutation", f"{int(CFG['mutation_rate'] * 100)} %"),
              ("Élite", CFG["elite_size"])]
    for i, (k, v) in enumerate(params):
        y = Inches(2.86) + Inches(0.335) * i
        tfk = textbox(slide, x + Inches(0.28), y, Inches(2.0), Inches(0.3))
        para(tfk, k, size=11.5, color=MUTED, first=True)
        tfv = textbox(slide, x + Inches(2.20), y, w - Inches(2.48), Inches(0.3))
        para(tfv, str(v), size=11.5, color=GOLD_SOFT, bold=True,
             align=PP_ALIGN.RIGHT, first=True)

    rect(slide, x, Inches(5.13), w, Inches(1.79), fill=PANEL, line=LINE, lw=1.0)
    tf = textbox(slide, x + Inches(0.28), Inches(5.27), w - Inches(0.56),
                 Inches(1.55))
    para(tf, "Pourquoi elle, et pas l'exploratoire ?", size=12.5, color=CYAN,
         bold=True, first=True, spacing=1.0)
    para(tf, "Elle obtient la même meilleure distance, mais avec un écart-type "
             "nul : les 3 seeds convergent au même endroit. Plus de calcul ne "
             "garantit pas un meilleur résultat — l'exploratoire échoue sur un "
             "seed malgré 800 générations.",
         size=10.5, color=MUTED, space_before=5, spacing=1.15)
    footer(slide, 13, LISA)

    notes(slide, LISA, "1 min 25",
          "Nous avons testé trois configurations — rapide, équilibrée et "
          "exploratoire — chacune sur trois seeds différents : onze, vingt-deux "
          "et trente-trois. Un seed, c'est la graine du générateur aléatoire : à "
          "seed identique, l'exécution est rigoureusement reproductible. Tester "
          "plusieurs seeds est indispensable, parce qu'avec un algorithme "
          "stochastique, une seule exécution ne dit rien sur la robustesse. "
          "Regardez le résultat : les trois configurations atteignent la même "
          "meilleure distance, trois mille cent cinquante-sept kilomètres. Mais "
          "la rapide et l'exploratoire ont chacune un seed qui échoue à trois "
          "mille trois cent trente-quatre, ce qui leur donne un écart-type de "
          "quatre-vingt-trois kilomètres. La configuration équilibrée, elle, a un "
          "écart-type nul : les trois seeds convergent exactement au même "
          "endroit. C'est pour ça que nous l'avons retenue, et le code la "
          "sélectionne automatiquement sur le critère moyenne, puis écart-type, "
          "puis meilleure. Et j'insiste sur un point contre-intuitif : "
          "l'exploratoire fait huit cents générations avec deux cent quarante "
          "individus, donc bien plus de calcul, et elle n'est pas meilleure. Plus "
          "de calcul ne garantit pas un meilleur résultat. Enfin, soyons "
          "honnêtes : trois seeds, c'est peu pour un vrai jugement statistique.",
          "Regardons maintenant comment se comporte cette configuration au fil "
          "des générations.")


def s14(prs):
    slide = new_slide(prs)
    slide_header(slide, "Convergence", "Ce que la courbe dit — et ne dit pas",
                 "La meilleure distance connue au fil des 520 générations, "
                 "configuration équilibrée, seed 11.")
    place_image(slide, "15_convergence.png", Inches(0.55), Inches(1.82),
                Inches(8.55), IMG_BOTTOM)
    x, w = Inches(8.90), Inches(3.88)
    rect(slide, x, Inches(1.95), w, Inches(1.92), fill=PANEL, line=CYAN, lw=1.4)
    tf = textbox(slide, x + Inches(0.28), Inches(2.12), w - Inches(0.56),
                 Inches(1.95))
    para(tf, "Ce que la courbe montre", size=13, color=CYAN, bold=True,
         first=True)
    para(tf, "L'essentiel du progrès se joue dans les 70 premières générations. "
             "La meilleure tournée est atteinte dès la génération 67, puis la "
             "courbe est plate jusqu'à la 520e.",
         size=11, color=MUTED, space_before=5, spacing=1.18)

    rect(slide, x, Inches(4.05), w, Inches(2.87), fill=PANEL_HI, line=CORAL,
         lw=1.6)
    tf = textbox(slide, x + Inches(0.28), Inches(4.24), w - Inches(0.56),
                 Inches(2.5))
    para(tf, "Ce qu'elle ne prouve PAS", size=13, color=CORAL, bold=True,
         first=True)
    para(tf, "Une courbe plate signifie que l'algorithme ne progresse plus, pas "
             "qu'il a trouvé l'optimum global. Il peut être bloqué dans un "
             "optimum local : le meilleur de son voisinage, pas le meilleur "
             "possible. Seul un calcul exact trancherait.",
         size=11, color=MUTED, space_before=5, spacing=1.18)
    footer(slide, 14, LISA)

    notes(slide, LISA, "1 min 10",
          "Cette courbe montre la meilleure distance connue au fil des "
          "générations. Elle part très haut, autour de six mille quatre cents "
          "kilomètres, parce que la population initiale est complètement "
          "aléatoire, et elle chute très vite. L'essentiel du progrès se joue "
          "dans les soixante-dix premières générations : la meilleure tournée est "
          "atteinte dès la génération soixante-sept. Ensuite, plus rien pendant "
          "quatre cent cinquante générations. La ligne bleue en pointillés, c'est "
          "le résultat de Christofides : on voit que le génétique le dépasse très "
          "tôt. Et voici le point le plus important de cette slide : une courbe "
          "plate ne prouve pas du tout que nous avons trouvé l'optimum global. "
          "Elle prouve seulement que l'algorithme ne progresse plus. Il peut être "
          "coincé dans un optimum local, c'est-à-dire la meilleure solution de "
          "son voisinage immédiat, sans être la meilleure possible. C'est "
          "exactement ce qui arrive aux seeds qui s'arrêtent à trois mille trois "
          "cent trente-quatre kilomètres.",
          "Voici la tournée que cette configuration propose à Théobald.")


def s15(prs):
    slide = new_slide(prs)
    slide_header(slide, "Résultat", "L'itinéraire proposé par l'algorithme génétique",
                 "Meilleure tournée observée sur l'ensemble de nos exécutions.")
    place_image(slide, "06_route_genetique.png", Inches(0.55), Inches(1.78),
                Inches(6.55), IMG_BOTTOM)
    x, w = Inches(6.95), Inches(5.83)
    stat_card(slide, x, Inches(1.92), w, Inches(1.28), f"{fr(GA)} km",
              "Meilleure distance observée — configuration équilibrée",
              color=GOLD, vsize=33, lsize=12.5)
    cw = (w - Inches(0.16)) / 2
    stat_card(slide, x, Inches(3.34), cw, Inches(1.02), f"− {fr(GAP)} km",
              "de moins que Christofides", color=GREEN, vsize=19)
    stat_card(slide, x + cw + Inches(0.16), Inches(3.34), cw, Inches(1.02),
              f"− {fr(GAP_PCT)} %", "d'amélioration relative", color=GREEN,
              vsize=19)
    stat_card(slide, x, Inches(4.50), cw, Inches(1.02), "0,0 km",
              "écart-type sur les 3 seeds", color=CYAN, vsize=19)
    stat_card(slide, x + cw + Inches(0.16), Inches(4.50), cw, Inches(1.02),
              "≈ 1,2 s", "par exécution, sur notre machine", color=MUTED,
              vsize=19)
    tf = textbox(slide, x, Inches(5.76), w, Inches(1.1))
    para(tf, "À dire précisément : c'est la meilleure tournée que nous ayons "
             "observée — pas l'optimum. Nous n'avons jamais calculé l'optimum "
             "exact de cette instance.",
         size=11.5, color=GOLD_SOFT, italic=True, first=True, spacing=1.22)
    footer(slide, 15, LISA)

    notes(slide, LISA, "1 min",
          "Voici la tournée du génétique. Trois mille cent cinquante-sept virgule "
          "treize kilomètres, soit deux cent quatre-vingt-huit kilomètres et "
          "demi de moins que Christofides, c'est-à-dire huit virgule trente-sept "
          "pour cent d'amélioration. Si vous comparez les deux cartes, la "
          "différence se voit surtout dans le sud-est : Christofides fait un "
          "aller-retour vers Nice avant de revenir sur Marseille, alors que le "
          "génétique enchaîne proprement Nîmes, Marseille, Toulon, Nice, puis "
          "remonte par Grenoble. C'est là que se jouent les deux cent quatre-"
          "vingt-huit kilomètres. Une formulation à laquelle je tiens : trois "
          "mille cent cinquante-sept kilomètres, c'est la meilleure tournée que "
          "nous ayons observée, pas l'optimum. Nous n'avons pas calculé l'optimum "
          "exact, donc nous ne pouvons pas l'affirmer.",
          "Yannis va maintenant mettre les deux méthodes face à face.")


def s16(prs):
    slide = new_slide(prs)
    slide_header(slide, "Analyse comparative", "Le tableau de décision",
                 "Distance, temps d'exécution, facilité d'implémentation, "
                 "robustesse — les quatre critères demandés par le sujet.")
    place_image(slide, "17_comparaison.png", Inches(0.55), Inches(1.82),
                Inches(6.35), Inches(4.60))
    tf = textbox(slide, Inches(0.55), Inches(4.78), Inches(6.35), Inches(2.1))
    para(tf, "Lire correctement cet écart", size=13, color=GOLD, bold=True,
         first=True)
    para(tf, "Sur CETTE instance et avec NOS réglages, le génétique gagne "
             "288,48 km. Cela ne signifie pas qu'un algorithme génétique bat "
             "toujours Christofides : la garantie de Christofides est un "
             "plafond (jamais plus de 1,5 × OPT), pas une promesse d'être le "
             "meilleur. Le génétique, lui, n'a aucun plafond — il peut aussi "
             "faire bien pire, comme le montrent nos seeds à 3 334 km.",
         size=11.5, color=MUTED, space_before=6, spacing=1.25)

    x, w = Inches(7.15), Inches(5.63)
    rows = [
        ("Critère", "Christofides", "Algorithme génétique", True),
        ("Distance obtenue", f"{fr(CHRIST, 0)} km", f"{fr(GA, 0)} km", False),
        ("Temps observé", "≈ 1,5 ms", "≈ 1,2 s par run", False),
        ("Déterminisme", "Total", "Dépend du seed", False),
        ("Garantie théorique", "≤ 1,5 × OPT", "Aucune", False),
        ("Paramétrage", "Quasi nul", "6 hyperparamètres", False),
        ("Robustesse mesurée", "Exacte à chaque run", "σ = 0 km (config retenue)",
         False),
        ("Implémentation", "Longue : 6 briques", "Courte, mais à régler", False),
        ("Reproductibilité", "Garantie", "Garantie à seed fixé", False),
    ]
    rh = Inches(0.545)
    for i, (c1, c2, c3, is_head) in enumerate(rows):
        y = Inches(1.92) + rh * i
        fill = PANEL_HI if is_head else (PANEL if i % 2 else BG)
        rect(slide, x, y, w, rh, fill=fill, line=LINE, lw=0.75,
             shape=MSO_SHAPE.RECTANGLE)
        for cx, cw_, txt, col, al in (
                (x + Inches(0.16), Inches(2.05), c1,
                 GOLD if is_head else MUTED, PP_ALIGN.LEFT),
                (x + Inches(2.25), Inches(1.55), c2,
                 GOLD if is_head else CYAN, PP_ALIGN.CENTER),
                (x + Inches(3.88), Inches(1.65), c3,
                 GOLD if is_head else GOLD_SOFT, PP_ALIGN.CENTER)):
            tfc = textbox(slide, cx, y, cw_, rh, anchor=MSO_ANCHOR.MIDDLE)
            para(tfc, txt, size=10.5 if not is_head else 11,
                 color=col, bold=is_head, align=al, first=True, spacing=1.0)
    footer(slide, 16, YANNIS)

    notes(slide, YANNIS, "1 min 30",
          "Merci Lisa. Voici le tableau de décision, sur les quatre critères "
          "demandés par le "
          "sujet. Distance : le génétique gagne, deux cent quatre-vingt-huit "
          "kilomètres de moins. Temps : Christofides écrase le génétique, une "
          "milliseconde et demie contre un peu plus d'une seconde par exécution — "
          "soit un facteur de l'ordre de mille. Déterminisme : Christofides donne "
          "toujours exactement le même résultat, le génétique dépend du seed. "
          "Garantie : Christofides ne dépasse jamais une fois et demie l'optimum, "
          "le génétique n'offre aucune borne. Paramétrage : Christofides n'a "
          "presque rien à régler, le génétique a six hyperparamètres. Facilité "
          "d'implémentation : c'est nuancé — Christofides demande six briques "
          "distinctes, c'est plus long à écrire, mais une fois écrit il n'y a "
          "rien à ajuster ; le génétique s'écrit vite, mais il faut ensuite "
          "passer du temps à le calibrer. Et un point que je veux souligner : le "
          "fait que le génétique gagne ici ne veut pas dire qu'il gagne toujours. "
          "La garantie de Christofides est un plafond, pas une promesse d'être le "
          "meilleur. Le génétique, lui, n'a aucun plafond : nos seeds "
          "malheureux finissent à trois mille trois cent trente-quatre "
          "kilomètres, donc moins bien que Christofides.",
          "Romain va maintenant présenter les limites de notre étude.")


# ===========================================================================
#  Clôture
# ===========================================================================
def s17(prs):
    slide = new_slide(prs)
    slide_header(slide, "Honnêteté scientifique", "Limites de notre étude, et suites possibles",
                 "Ce que nos chiffres ne disent pas, et ce que nous ferions avec "
                 "plus de temps.")
    lim = [
        ("Distances à vol d'oiseau", "Haversine ≠ distance routière réelle. La "
         "tournée de Théobald serait plus longue sur de vraies routes."),
        ("Aucun optimum exact calculé", "Nous encadrons l'optimum, nous ne le "
         "connaissons pas : meilleure observée n'est pas optimale."),
        ("Benchmark à 3 seeds seulement", "Suffisant pour départager nos trois "
         "configs, insuffisant pour une conclusion statistique solide."),
        ("Hyperparamètres empiriques", "Choisis par essais et benchmark, pas "
         "démontrés optimaux. Aucune théorie ne les justifie."),
        ("Une seule instance, 20 villes", "Nos conclusions valent pour ce jeu de "
         "données, pas pour le TSP en général."),
    ]
    amel = [
        ("2-opt / 3-opt après le GA", "Une recherche locale qui décroise les "
         "arêtes : gain quasi systématique, coût faible."),
        ("Christofides comme graine du GA", "Injecter la tournée Christofides "
         "dans la population initiale : on part déjà sous 3 446 km."),
        ("30 seeds au lieu de 3", "Permettrait de parler vraiment de moyenne, "
         "d'écart-type et de robustesse."),
        ("Réglage automatique (grid/random search)", "Explorer "
         "systématiquement l'espace des hyperparamètres au lieu de trois points."),
        ("Held-Karp sur une sous-instance", "Exact en O(n²·2ⁿ) : impossible à 20 "
         "villes, faisable à 15 pour calibrer notre écart réel à l'optimum."),
    ]
    for col_i, (titre, items, color) in enumerate(
            [("CE QUE NOS CHIFFRES NE DISENT PAS", lim, CORAL),
             ("CE QUE NOUS FERIONS ENSUITE", amel, GREEN)]):
        x = Inches(0.55) + Inches(6.28) * col_i
        w = Inches(5.95)
        tf = textbox(slide, x, Inches(1.82), w, Inches(0.3))
        para(tf, titre, size=12, color=color, bold=True, first=True)
        for i, (t, b) in enumerate(items):
            y = Inches(2.22) + Inches(0.93) * i
            rect(slide, x, y, w, Inches(0.80), fill=PANEL, line=LINE, lw=0.9)
            rect(slide, x, y, Inches(0.042), Inches(0.80), fill=color,
                 shape=MSO_SHAPE.RECTANGLE)
            tfi = textbox(slide, x + Inches(0.24), y + Inches(0.09),
                          w - Inches(0.46), Inches(0.64))
            para(tfi, t, size=11.5, color=TEXT, bold=True, first=True,
                 spacing=0.95)
            para(tfi, b, size=9.5, color=MUTED, space_before=2, spacing=1.08)
    footer(slide, 17, ROMAIN)

    notes(slide, ROMAIN, "1 min 30",
          "Je reprends la main pour les limites, parce qu'un projet honnête doit "
          "savoir dire ce qu'il ne prouve pas. Première limite, la plus "
          "concrète : nos distances sont à vol d'oiseau. Théobald ne volera pas, "
          "donc sa tournée réelle serait plus longue. Deuxième limite : nous "
          "n'avons jamais calculé l'optimum exact. Nous pouvons l'encadrer, mais "
          "pas le nommer. Troisième : trois seeds, c'est assez pour départager "
          "nos trois configurations, ce n'est pas assez pour une conclusion "
          "statistique solide. Quatrième : nos hyperparamètres sont empiriques, "
          "issus du benchmark, aucune théorie ne dit que cent soixante individus "
          "et vingt-deux pour cent de mutation sont les bons réglages. Et "
          "cinquièmement, tout cela vaut pour une instance de vingt villes, pas "
          "pour le TSP en général. À droite, ce que nous ferions ensuite. Le plus "
          "rentable serait d'ajouter une recherche locale deux-opt après le "
          "génétique : elle décroise les arêtes et améliore presque toujours le "
          "résultat pour un coût très faible. On pourrait aussi injecter la "
          "tournée de Christofides dans la population initiale du génétique, ce "
          "qui garantirait de partir déjà sous trois mille quatre cent "
          "quarante-cinq kilomètres. Et évidemment, passer à trente seeds.",
          "J'enchaîne sur la façon dont nous nous sommes organisés tous les trois.")


def s18(prs):
    slide = new_slide(prs)
    slide_header(slide, "Organisation", "Notre tableau Trello, et le dépôt GitHub",
                 "Une carte = un livrable vérifiable. Revue du tableau à chaque "
                 "séance.")
    place_image(slide, "19_kanban.png", Inches(0.55), Inches(1.82),
                Inches(9.05), IMG_BOTTOM)
    x, w = Inches(9.35), Inches(3.43)
    blocks = [
        ("Romain", "Données, Haversine, graphe complet, dépôt GitHub, README",
         GOLD),
        ("Yannis", "Christofides : Prim, degrés impairs, couplage, Hierholzer",
         CYAN),
        ("Lisa", "Algorithme génétique, opérateurs, benchmark, visualisations",
         GREEN),
        ("En commun", "Tests unitaires, analyse comparative, slides, répétitions",
         MUTED),
    ]
    for i, (who, what, col) in enumerate(blocks):
        y = Inches(1.95) + Inches(1.18) * i
        rect(slide, x, y, w, Inches(1.02), fill=PANEL, line=LINE, lw=1.0)
        rect(slide, x, y, Inches(0.045), Inches(1.02), fill=col,
             shape=MSO_SHAPE.RECTANGLE)
        tf = textbox(slide, x + Inches(0.26), y + Inches(0.13), w - Inches(0.5),
                     Inches(0.78))
        para(tf, who, size=13.5, color=col, bold=True, first=True, spacing=0.95)
        para(tf, what, size=10, color=MUTED, space_before=3, spacing=1.12)
    rect(slide, x, Inches(6.72), w, Inches(0.0), fill=LINE,
         shape=MSO_SHAPE.RECTANGLE)
    tf = textbox(slide, x, Inches(6.72), w, Inches(0.35))
    para(tf, "github.com/RomainJazzar/travelling-merchant", size=11,
         color=CYAN, bold=True, first=True)
    footer(slide, 18, ROMAIN)

    notes(slide, ROMAIN, "1 min 05",
          "Le sujet demande que notre organisation apparaisse dans la "
          "présentation, la voici. Nous avons travaillé sur un tableau Trello à "
          "trois colonnes, avec une règle simple : une carte égale un livrable "
          "vérifiable, pas une intention. Dans la colonne terminée, vous "
          "retrouvez toute la chaîne technique : le CSV des vingt villes, "
          "Haversine, le graphe complet, Prim, Christofides, le génétique, le "
          "benchmark, les cartes, et l'analyse comparative. Côté répartition : "
          "Romain s'est occupé des données, de Haversine, du graphe et du dépôt ; "
          "Yannis a pris toute la partie Christofides ; Lisa a fait l'algorithme "
          "génétique, le benchmark et les visualisations. Les tests unitaires, "
          "l'analyse comparative et les slides, nous les avons faits ensemble. "
          "Tout est public sur le dépôt GitHub travelling-merchant, avec un "
          "README qui reprend le contexte, les deux algorithmes et la conclusion.",
          "Lisa va conclure avec notre recommandation pour Théobald.")


def s19(prs):
    slide = new_slide(prs)
    slide_header(slide, "Conclusion", "Notre recommandation à Théobald",
                 "Et ce que nous savons — vraiment — de l'optimum.")
    place_image(slide, "18_bornes.png", Inches(0.55), Inches(1.80),
                Inches(12.78), Inches(3.72))

    y = Inches(3.95)
    cards = [
        ("POUR TRACER SA ROUTE", "L'algorithme génétique",
         f"{fr(GA)} km — la meilleure tournée que nous ayons obtenue, avec une "
         f"configuration stable sur nos 3 seeds. C'est ce que nous mettons entre "
         f"les mains de Théobald.", GOLD),
        ("COMME FILET DE SÉCURITÉ", "Christofides",
         f"{fr(CHRIST)} km en 1,5 ms, sans réglage et sans hasard. C'est la "
         f"référence qui valide le génétique et le remplace si le temps de calcul "
         f"devient critique.", CYAN),
    ]
    for i, (eyebrow, title, body, col) in enumerate(cards):
        x = Inches(0.55) + Inches(6.28) * i
        w = Inches(5.95)
        rect(slide, x, y, w, Inches(1.92), fill=PANEL, line=col, lw=1.6)
        rect(slide, x, y, Inches(0.05), Inches(1.92), fill=col,
             shape=MSO_SHAPE.RECTANGLE)
        tf = textbox(slide, x + Inches(0.30), y + Inches(0.18),
                     w - Inches(0.6), Inches(1.6))
        para(tf, eyebrow, size=10.5, color=col, bold=True, first=True)
        para(tf, title, size=19, color=TEXT, bold=True, space_before=3,
             spacing=0.98)
        para(tf, body, size=11, color=MUTED, space_before=6, spacing=1.2)

    rect(slide, Inches(0.55), Inches(6.12), Inches(12.23), Inches(0.74),
         fill=PANEL_HI, line=GOLD, lw=1.5)
    tf = textbox(slide, Inches(0.55), Inches(6.12), Inches(12.23), Inches(0.74),
                 anchor=MSO_ANCHOR.MIDDLE)
    para(tf, "Nous ne livrons pas la tournée optimale : nous livrons la "
             "meilleure tournée que nous sachions construire, et nous savons "
             "dire exactement ce qui nous sépare de l'optimum.",
         size=13.5, color=GOLD_SOFT, bold=True, align=PP_ALIGN.CENTER,
         first=True)
    footer(slide, 19, LISA)

    notes(slide, LISA, "1 min 30",
          "Notre recommandation pour Théobald tient en deux temps. Pour tracer sa "
          "route, nous recommandons l'algorithme génétique : trois mille cent "
          "cinquante-sept kilomètres, avec une configuration qui s'est montrée "
          "stable sur nos trois seeds. C'est concrètement deux cent quatre-vingt-"
          "huit kilomètres économisés à chaque tournée. Mais nous gardons "
          "Christofides comme filet de sécurité : il donne une très bonne tournée "
          "en une milliseconde et demie, sans aucun réglage et sans hasard, et il "
          "sert de référence pour valider le génétique. Si Théobald devait "
          "recalculer sa tournée en permanence, ou avec beaucoup plus de villes, "
          "c'est Christofides que nous choisirions. Et pour finir, la phrase à "
          "laquelle nous tenons le plus. Le schéma du haut montre ce que nous "
          "savons vraiment : l'arbre couvrant minimal, deux mille six cent "
          "soixante-cinq kilomètres, est une borne inférieure prouvée de "
          "l'optimum. Notre meilleure tournée, trois mille cent cinquante-sept, "
          "est une borne supérieure, puisque c'est une tournée valide. L'optimum "
          "est donc quelque part entre les deux, dans une fenêtre de quatre cent "
          "quatre-vingt-douze kilomètres. Nous ne livrons pas la tournée "
          "optimale : nous livrons la meilleure tournée que nous sachions "
          "construire, et nous savons dire exactement ce qui nous en sépare. "
          "Merci de votre attention, nous sommes prêts pour vos questions.",
          "— Fin de la présentation, place aux questions.")


SLIDES = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10,
          s11, s12, s13, s14, s15, s16, s17, s18, s19]


def main():
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    for builder in SLIDES:
        builder(prs)
    OUT_PPTX.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_PPTX))
    print(f"{len(SLIDES)} slides  ->  {OUT_PPTX}")


if __name__ == "__main__":
    main()
