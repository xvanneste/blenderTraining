# Atelier guidé — Débogage et performance

Depuis le dossier des scripts, lancez `python mesurer.py` avec Python 3. Gardez le même interpréteur pour toutes vos mesures. Retrouvez le fichier et la ligne indiqués dans le traceback avant de modifier le code.

## 1. Reproduire

Exécutez mesurer.py, puis introduisez dans une copie une demande de plan absent. Relevez la dernière ligne du traceback et l’appel correspondant.

**Pourquoi** Le type d’exception précise le mécanisme. La pile montre comment l’exécution y est arrivée.

**Contrôle** Vous identifiez l’accès qui échoue et un jeu de données reproductible.

## 2. Corriger

Décidez comment traiter un plan absent. Filtrez les demandes invalides en les journalisant ou remontez une erreur avec le nom demandé.

**Pourquoi** Une règle d’absence explicite évite un résultat incomplet difficile à voir.

**Contrôle** Le message contient le plan absent et le chemin nominal est toujours correct.

## 3. Mesurer

Revenez au jeu complet. Vérifiez l’égalité des listes, puis comparez les temps du parcours répété et de la table d’index.

**Pourquoi** La création du dictionnaire fait partie de la mesure. Les temps servent à comparer ce jeu de données.

**Contrôle** Le compte rendu donne taille, machine, version, temps et égalité du résultat.

## Vérification sur une variante

Mesurez 25, 250 et 5 000 lignes en incluant le coût de construction et trois répétitions par taille. Consignez interpréteur, machine et conditions. Refaites la comparaison en demandant un plan absent.
