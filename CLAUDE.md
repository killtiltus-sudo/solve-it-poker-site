# Solve It Poker — consignes pour Claude Code

Ce fichier est chargé à chaque session : il reste court. Lis le reste seulement si la tâche l'exige.

## Le porteur
- Réponds en français. Ne devine jamais : pose une question dès qu'un point est flou.
- Produit : **Solve It Poker** (solveur préflop + tracker pour Expresso/Spin et tournois 6 joueurs). « Range Poker Expresso » est un nom de travail interne : ne jamais l'afficher (marque Expresso de Winamax).
- Aucune publication, aucun déploiement, aucun achat, aucun contact externe sans accord. Refonte, logique poker, modèle économique ou décision irréversible : proposition écrite d'abord.
- Les livrables internes (PDF, PPTX, maquettes) restent **hors de GitHub** : le dépôt est public.

## Ce dépôt
- Site statique (GitHub Pages, www.solve-it-poker.com) : `index.html`, `cgv.html`, `mentions-legales.html`, `fonts/`, flux de mise à jour (`version.json`, `maj-mac-*.json`). Le code de l'application de bureau (Electron) **n'est pas ici**.
- `index.html` est **généré hors du dépôt** (`scripts_v5.js` chez le porteur) puis déposé à la main : une modification faite ici est écrasée au prochain dépôt si elle n'est pas reportée dans le générateur. Le signaler à chaque changement.

## Économiser les jetons (important)
- **Ne jamais lire `index.html` en entier** avec Read ni `cat` : 3,2 Mo dont 2,8 Mo d'images et de polices en base64 sur des lignes géantes (lignes 17-21, 437-519 : jusqu'à 386 000 caractères ; ligne 844 `DEMO` ; ligne 884 `I18N`, 43 000 caractères).
- Utiliser `python3 outils/vue-index.py` (≈ 75 Ko, numéros de ligne d'origine) :
  - `python3 outils/vue-index.py 343 420` : une plage de lignes ;
  - `python3 outils/vue-index.py -g "tarif|PAIEMENT"` : lignes contenant un motif ;
  - `-f cgv.html` pour une autre page, `-l 2000` pour voir plus loin dans une ligne longue.
- Repères de `index.html` : CSS 16-255 · en-tête 259 · héros 344 · fonctions 383 · aperçu (captures) 423 · méthode 524 · tarif 557 · FAQ 604 · pied 629 · script `PAIEMENT` 775 · `DEMO` 844 · `I18N` 884 · `DYN` 886. Vérifier avec `-g` avant de s'y fier : les numéros bougent.
- Modifier `index.html` par remplacement exact avec un court script Python (lecture, `str.replace` avec contrôle du nombre d'occurrences, écriture), pas avec Edit sur les lignes géantes.
- Traduction : `I18N` est un dictionnaire indexé par le **texte français exact** ; changer un texte français oblige à changer sa clé dans `I18N`. Les éléments listés dans `DYN` ne sont pas traduits.
- Pour l'audit, lire d'abord la synthèse au lieu des 6 documents (≈ 120 Ko au total) : voir ci-dessous.
- Préférer Grep ciblé et lectures partielles (`offset`/`limit`) ; ne lancer des sous-agents que si le porteur le demande.

## Audit d'octobre 2026 (`docs/audit-range-expresso/`)
| Fichier | Taille | Contenu | Sections (ligne) |
|---|---|---|---|
| `03-synthese-et-positionnement.md` | 24 Ko | **À lire en premier** : diagnostic, valeur, UX, prix, conformité | 1 diag. 9 · 4 UX 108 · 6 prix 159 · 8 conformité 234 · 9 plan 269 |
| `05-plan-daction.md` | 11 Ko | Phases 0 à 4, chemin critique | phase 0 20 · phase 1 32 · chemin critique 88 |
| `06-changements-code.md` | 14 Ko | Corrections faites et propositions en attente d'accord | faits 21 · en attente 75 |
| `01-etat-des-lieux.md` | 12 Ko | Inventaire du dépôt et de l'app | app 41 · inventaire 57 · à confirmer 109 |
| `04-marche-prix-offres.md` | 18 Ko | Concurrents sourcés, prix, paiement | tableau 18 · prix 118 · paiement 191 |
| `02-rapports-des-experts.md` | 39 Ko | Rapports bruts des 7 experts : ne lire que la section utile | poker 24 · produit 92 · UX 149 · dev 221 · SEO 299 · marché 341 · conformité 364 |

## Vérifications
- Rendu et accessibilité : Playwright est installé (`/opt/node22/lib/node_modules/playwright`, Chromium dans `/opt/pw-browsers`) ; lancer `python3 -m http.server` puis tester la page.
- Après une modification de `index.html` : `python3 outils/vue-index.py -g "<motif>"` pour relire seulement la zone changée.

## Git
- Ne jamais pousser sur `main` sans accord ; pas de pull request sans demande.
