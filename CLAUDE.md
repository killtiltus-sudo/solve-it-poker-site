# Solve It Poker — consignes pour Claude Code

Ce fichier est chargé à chaque session : il reste court. Lis le reste seulement si la tâche l'exige.

## Le porteur
- Réponds en français. Ne devine jamais : pose une question dès qu'un point est flou.
- Produit : **Solve It Poker** (solveur préflop + tracker pour Expresso/Spin et tournois 6 joueurs). « Range Poker Expresso » est un nom de travail interne : ne jamais l'afficher (marque Expresso de Winamax).
- Aucune publication, aucun déploiement, aucun achat, aucun contact externe sans accord. Refonte, logique poker, modèle économique ou décision irréversible : proposition écrite d'abord.
- Les livrables internes (PDF, PPTX, maquettes) restent **hors de GitHub** : le dépôt est public.

## Ce dépôt
- Site statique (GitHub Pages, www.solve-it-poker.com) : `index.html`, `cgv.html`, `mentions-legales.html`, `fonts/`, flux de mise à jour (`version.json`, `maj-mac-*.json`). Le code de l'application de bureau (Electron) **n'est pas ici**.
- `index.html` était **généré hors du dépôt** (`scripts_v5.js` chez le porteur) puis déposé à la main. Depuis le 8 octobre 2026, la version de référence est celle du dépôt (images et polices sorties dans des fichiers) : un nouvel envoi depuis `scripts_v5.js` écraserait ces changements.

## Économiser les jetons (important)
- Les captures sont dans `images/*.webp` et les polices dans `fonts/` : `index.html` ne fait plus que 132 Ko. **Si un `index.html` réapparaît avec des images en base64 (`data:image/webp;base64`), c'est qu'il a été régénéré par l'ancien générateur** : le signaler au porteur avant toute autre chose.
- Ne pas lire `index.html` en entier : deux lignes restent très longues (ligne 844 `DEMO`, 12 000 caractères ; ligne 884 `I18N`, 43 000 caractères).
- Utiliser `python3 outils/vue-index.py` (numéros de ligne d'origine, lignes longues tronquées, base64 éventuel masqué) :
  - `python3 outils/vue-index.py 343 420` : une plage de lignes ;
  - `python3 outils/vue-index.py -g "tarif|PAIEMENT"` : lignes contenant un motif ;
  - `-f cgv.html` pour une autre page, `-l 2000` pour voir plus loin dans une ligne longue.
- Repères de `index.html` : CSS 16-255 · en-tête 259 · héros 344 · fonctions 383 · aperçu (captures) 423 · méthode 524 · tarif 557 · FAQ 604 · pied 629 · script `PAIEMENT` 775 · `DEMO` 844 · `I18N` 884 · `DYN` 886. Vérifier avec `-g` avant de s'y fier : les numéros bougent.
- Modifier `index.html` par remplacement exact avec un court script Python (lecture, `str.replace` avec contrôle du nombre d'occurrences, écriture), pas avec Edit sur les lignes géantes.
- Traduction : `I18N` est un dictionnaire indexé par le **texte français exact** ; changer un texte français oblige à changer sa clé dans `I18N`. Les éléments listés dans `DYN` ne sont pas traduits.
- Pour l'audit, lire d'abord la synthèse au lieu des 6 documents (≈ 120 Ko au total) : voir ci-dessous.
- Préférer Grep ciblé et lectures partielles (`offset`/`limit`) ; ne lancer des sous-agents que si le porteur le demande.

## Application de bureau (lecture seule)
- Son code source est chez le porteur, pas sur GitHub : les releases de ce dépôt ne contiennent que les binaires (zip Mac et Windows). Toute modification de l'app se fait dans les sources du porteur.
- Pour lire le code publié : `python3 outils/extraire-app.py -d <dossier hors dépôt>` (télécharge la dernière release Windows et extrait `app.asar` ; `-t v0.35.0` pour une autre version).
- Fichiers utiles : `asar/main.js` (licences, mises à jour, historiques, HUD, OCR) ; `asar/app/index.html` (interface, 13,5 Mo) ; moteur dans `app.asar.unpacked/native/engine/solver-core.js`.
- **Ne jamais lire `asar/app/index.html` en entier** : lignes 3605-3608 = données de ranges (`DATA`, `DATAJ`, `DATAM` 12 Mo, `ExpressoSolver.init`). Utiliser `python3 outils/vue-index.py -f <dossier>/asar/app/index.html -g "motif"` (≈ 670 Ko au lieu de 13,5 Mo).

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
