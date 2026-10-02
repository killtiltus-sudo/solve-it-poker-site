# 01 — État des lieux (phase 1 : cartographie de l'existant)

Audit réalisé le 2 octobre 2026 sur la branche `claude/range-poker-expresso-audit-2ofzgo` (identique à `main`, commit `ffefc4c` du 1er octobre 2026).

Légende utilisée dans tous les livrables :
- **Fait vérifié** : constaté directement (fichier, commande, page officielle) ; la preuve est citée.
- **Observation** : constat qualitatif tiré des faits.
- **Hypothèse** : plausible mais non démontré ; à confirmer.
- **Recommandation** : action proposée.

---

## 1. Ce qu'est réellement le dépôt

**Fait vérifié.** Le projet que vous appelez « Range Poker Expresso » s'appelle partout **Solve It Poker** (« Track. Solve. Improve. »). Le nom « Range Poker Expresso » n'apparaît dans aucun fichier du dépôt ni dans l'application.

**Fait vérifié.** Le dépôt `killtiltus-sudo/solve-it-poker-site` est **uniquement le site vitrine statique**, publié par GitHub Pages sur `www.solve-it-poker.com` (fichier `CNAME`). Il ne contient :
- ni le code source de l'application ;
- ni `package.json`, ni outil de build, ni test, ni lint, ni CI (pas de dossier `.github/`) ;
- ni documentation, maquette ou fichier de stratégie.

| Fichier | Taille | Rôle |
|---|---|---|
| `index.html` | 3,27 Mo, 906 lignes | Page d'accueil complète (CSS + 2 scripts inline). Contient 12 captures WebP en base64 (≈ 2,1 Mo binaires) et 5 polices Barlow woff2 en base64 (≈ 0,26 Mo). Le HTML/CSS/JS « utile » ne pèse que ≈ 130 Ko. Taille compressée gzip : 2,3 Mo. |
| `cgv.html` | 327 lignes | Conditions générales de vente et d'utilisation (20 articles). |
| `mentions-legales.html` | 118 lignes | Mentions légales (SARL La Petite Orange, Montpellier). |
| `version.json` | — | Version publiée de l'application (0.36.0 du 2026-10-01) et liens de téléchargement. |
| `maj-mac-arm.json`, `maj-mac-intel.json` | — | Flux de mise à jour automatique macOS (format Squirrel.Mac). Pas de flux Windows. |
| `CNAME` | — | `www.solve-it-poker.com` |

**Fait vérifié.** L'historique compte 18 commits du 28 septembre au 1er octobre 2026, tous faits depuis l'interface web de GitHub (« Add files via upload », « Update version.json », « Delete … ») : les fichiers sont produits ailleurs puis téléversés. Le script de `index.html` cite des fichiers sources absents du dépôt (`scripts_v5.js`, `scripts_v5.bak-lemonsqueezy`, l. 242 et 764).

**Observation importante.** Toute correction faite directement dans ce dépôt sera **écrasée au prochain téléversement** si elle n'est pas reportée dans la source réelle du site. Les changements faits pendant cet audit sont donc documentés sous forme de correctifs à reporter (voir `06-changements-code.md`).

### Technologies
- Site : HTML/CSS/JavaScript natifs, sans framework ni dépendance externe sur l'accueil ; traduction anglaise par dictionnaire JavaScript (`I18N`, l. 866) appliqué au DOM ; mise en page CSS Grid/Flex ; polices Barlow intégrées.
- Application (hors dépôt, voir § 2) : Electron 38 + electron-builder, interface en un seul fichier HTML de 13,5 Mo, moteur de calcul JavaScript en *worker*, OCR tesseract.js, scripts PowerShell (Windows) et AppleScript/JXA (macOS) pour repérer les fenêtres de tables.

---

## 2. L'application de bureau (hors dépôt)

**Fait vérifié.** Les binaires sont publiés en **releases GitHub publiques** du même dépôt : V.036.0, v0.35.0, v0.33.0, v0.32.0, v0.31.0, v0.30.0, v0.29.0 (du 30 septembre au 1er octobre 2026, sans notes de version). Le tag `V.036.0` ne suit pas la convention des autres (`v0.35.0`).

Pour pouvoir auditer l'application, j'ai téléchargé le zip Windows public (127 Mo) et extrait son paquet Electron **en lecture seule, hors du dépôt**. Rien n'a été exécuté ni modifié.

**Faits vérifiés dans le paquet extrait :**
- `LISEZ-MOI-TESTEURS.txt` : « version de test », « complète et entièrement débloquée », « aucun abonnement n'est demandé », « la mention “Mode développement” dans “Mon abonnement” est normale ».
- `package.json` : `author` et `copyright` valent « À compléter » ; cible macOS `dmg universal` alors que les releases distribuent des zip par architecture.
- `main.js` l. 3 et 11 : seul réseau prévu = API de licences Lemon Squeezy (`https://api.lemonsqueezy.com/`) ; l. 67 : lecture de `https://www.solve-it-poker.com/version.json` pour la mise à jour ; l. 20 : fenêtre principale avec `contextIsolation`, `sandbox`, sans `nodeIntegration`.
- `app/index.html` l. 658 : bandeau « Mode développement : boutique Lemon Squeezy non configurée, toutes les fonctions sont ouvertes ».
- `main.js` l. 737-1022 : capture des fenêtres de tables (`desktopCapturer`) et **lecture des pseudos par OCR** (tesseract.js) pour associer chaque HUD à sa table.
- Binaires **non signés** : la notice demande de contourner Gatekeeper (dont `xattr -dr com.apple.quarantine`) et SmartScreen.

---

## 3. Inventaire fonctionnel : existant, incomplet, prévu, hypothétique

« Présent dans le code » signifie que l'interface et la logique existent dans le paquet 0.36.0 ; je n'ai **pas** exécuté l'application, donc le bon fonctionnement réel reste **à confirmer** par un test manuel sur Mac et Windows.

| Élément | Statut | Preuve |
|---|---|---|
| Solveur préflop Spin/Expresso, 3 joueurs et tête-à-tête, gagnant unique ou gros jackpot (buy-in 2 à 500 €, multiplicateurs x100 à x100 000) | Présent dans le code | `app-index` l. 661, 703-725 ; données `DATA`/`DATAJ` |
| Solveur préflop tournois 6-max (100 → 10 BB, ante, actions successives) | Présent dans le code | `data-game="mtt"` l. 662 ; `DATAM` (12 Mo) |
| Bibliothèque / Mes ranges / Calculer mon spot (tapis inégaux, 10 à 30 s) | Présent dans le code | l. 687-689, 725-735 |
| Profils d'adversaires par siège (adaptation par *node-locking* + meilleure réponse) | Présent dans le code | l. ~1951 |
| Tracker (import de fichiers/dossier, suivi en direct), Winamax et PokerStars | Présent dans le code | l. 782-800 ; `main.js` `hh:*` |
| HUD superposé aux tables, réglable | Présent dans le code | `hud.html`, `main.js` l. 590-660 (fenêtres HUD l. 600 et 643) |
| Gains en euros (récapitulatifs de tournoi), variance/EV, sièges, mains coûteuses, leaks chiffrés | Présent dans le code, montré par les captures du site | `index.html` § Aperçu |
| Entraînement (10 mains/jour gratuites annoncées) | Présent dans le code (zone `trainzone`) ; la limite de 10 mains est **à confirmer** | l. 8293 |
| **Cash game** (tables 2 à 9 joueurs) | Présent dans l'application, **absent du site** | `data-game="cash"` l. 663, l. 674-683 ; notes de `maj-mac-*.json` |
| Verrouillage du solveur pendant le jeu | Annoncé (FAQ, CGV art. 15) ; implémentation analysée par les agents poker et conformité | `index.html` FAQ |
| Interface en 4 langues (FR, EN, ES, IT) | Annoncé pour l'application ; le site n'existe qu'en FR + EN | `index.html` l. 412 |
| Paiement / essai gratuit 7 jours | **Non fonctionnel** : Lemon Squeezy a refusé la boutique le 01/10/2026, liens vides | `index.html` l. 763-772 |
| Résiliation en ligne « en trois clics » | **Non fonctionnelle** : ni service ni portail configuré ; affiche « Le service de résiliation n'est pas encore configuré » | `index.html` l. 789-825 ; test navigateur |
| Licence et activation | Codée pour l'API Lemon Squeezy, donc **inutilisable** en l'état ; l'application tombe en « Mode développement » tout ouvert | `main.js` l. 51-60 ; `app-index` l. 658 |
| Mise à jour automatique macOS | Flux publiés ; fonctionnement avec une application non signée **à confirmer** (Squirrel.Mac exige normalement une signature) | `maj-mac-*.json` ; `main.js` l. 113-150 |
| Mise à jour Windows | Pas de flux automatique ; l'application propose de télécharger la nouvelle version | `version.json` ; `app-index` l. 637-644 |
| PMU Poker, Betclic, bet365 | **Prévus** (FAQ), aucun signe d'implémentation relevé à ce stade | `index.html` FAQ |
| Jugement des décisions après le flop | **Non disponible** (« ne juge pas encore ») | `index.html` FAQ |
| « Modèle testé sur plus de 200 000 mains réelles », « jusqu'à 25 BB d'amélioration en Spin » | **Hypothétique** : affirmations du porteur, aucune trace dans le dépôt ni dans l'application | recherche `grep` sans résultat |

---

## 4. Vérifications exécutées

Aucune vérification n'est prévue par le projet (pas de tests, lint ni build). J'ai donc lancé des contrôles génériques, depuis un dossier de travail hors dépôt.

| Commande / contrôle | Résultat |
|---|---|
| `python3 -m json.tool` sur les 3 fichiers JSON | Valides |
| Extraction des 2 scripts inline + `node --check` | Aucune erreur de syntaxe |
| Contrôle des ancres internes (`href="#…"`) des 3 pages | Toutes résolues |
| `npx html-validate` (règles recommandées) sur les 3 pages | Erreurs mineures : `aria-labelledby`/`aria-label` sur des `div` sans rôle (l. 350, 367), `<label>` associé à deux contrôles (l. 354), `<input>` sans `type` (l. 706, 708), titre de plus de 70 caractères (l. 6), styles inline, `<!doctype>` en minuscules. Aucune erreur bloquante. |
| Rendu Chromium (Playwright) à 1280 px et 360 px | Aucune erreur JavaScript ; aucun débordement horizontal |
| axe-core (accessibilité) | Accueil : 1 contraste insuffisant (`.badge` « Le plus complet », #120B2B sur #B34279 = 3,58:1, minimum 4,5:1). CGV et mentions : contenu hors repères (`region`). |
| Parcours tarifs | Prix affichés : 19,90 / 29,90 / 14,90 € par mois ; 179 / 269 / 134 € par an (« soit 14,92 / 22,42 / 11,17 € par mois »). Le clic sur « Démarrer l'essai gratuit » affiche « Le paiement ouvre bientôt. Écris-nous pour être prévenu. » |
| Parcours résiliation | Étape 2 → « Le service de résiliation n'est pas encore configuré. » |
| Démo de la grille (11 profondeurs, 10 → 100 BB) | Fréquences cohérentes (somme 100 % par main) ; **le limp vaut 0 % à toutes les profondeurs** de la démo |
| Passage en anglais | Titre, H1 et textes traduits ; restent en français les messages dynamiques créés avant le changement de langue |
| Réseau | `index.html` : aucun appel externe. `cgv.html` et `mentions-legales.html` : appel à `fonts.googleapis.com` |

### Problèmes rencontrés
- **Le site en ligne n'est pas accessible** depuis l'environnement d'audit (proxy : 403). L'analyse repose sur le dépôt local, supposé identique à la version publiée (**à confirmer** : comparer `https://www.solve-it-poker.com/` avec `index.html` du commit `ffefc4c`).
- Le code source de l'application n'étant pas fourni, l'audit de l'application porte sur le paquet compilé (code JavaScript lisible, mais sans historique, commentaires de build ni tests).

---

## 5. Points à confirmer

1. La version en ligne du site correspond-elle au commit `ffefc4c` ? (comparer les deux)
2. Où se trouvent les sources du site (`scripts_v5.js`…) et de l'application ? Peut-on les verser dans un dépôt (privé) pour que les corrections ne soient pas perdues ?
3. Combien de personnes ont téléchargé la version de test ? (statistiques de téléchargement des releases GitHub)
4. Le fonctionnement réel de l'application sur Mac (Apple Silicon/Intel) et Windows : à vérifier par une session de test manuelle (import d'historiques Winamax, HUD, verrouillage du solveur).
5. Quel prestataire de paiement et de licence remplacera Lemon Squeezy ?
