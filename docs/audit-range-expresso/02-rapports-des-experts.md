# 02 — Rapports des experts

Sept agents spécialisés ont travaillé en parallèle le 2 octobre 2026, chacun sur un périmètre séparé, sans modifier aucun fichier du dépôt. Ce document reprend leurs constats sous une forme condensée et relue par le coordinateur. Les arbitrages entre rapports sont faits dans `03-synthese-et-positionnement.md`.

Légende : **Fait vérifié** · **Observation** · **Hypothèse** · **Recommandation**. Priorités : P0 bloquant, P1 important, P2 utile, P3 optionnel. Coût : faible, moyen, élevé.

Abréviations des références :
- `site:l` = `index.html` du dépôt (commit `ffefc4c`, avant les correctifs de l'audit) ;
- `app:l` = interface de l'application v0.36.0 (`app/index.html` extrait du zip Windows public) ;
- `main.js:l` = processus principal Electron ;
- `solver-core.js:l` = moteur de calcul.

---

## Notes du coordinateur avant lecture

1. **Accès web limité.** Le proxy de l'environnement d'audit bloquait l'ouverture directe de presque toutes les pages web (winamax.fr, pokerstars, legifrance, anj.fr, sites de tarifs des concurrents, Paddle, Stripe…). Les agents marketing, marché et conformité n'ont donc vu que **les extraits du moteur de recherche** de ces pages, consultés le 2026-10-02. Chaque prix, règle de room ou texte de loi cité ici doit être **relu sur la source officielle** avant toute décision ou publication.
2. **Signature Mac : correction.** Plusieurs agents sont partis de la notice testeurs (« pas encore signée »). L'agent développement a vérifié que les zips Mac v0.36.0 sont **signés Developer ID et notarisés**. Seul l'exécutable Windows n'est pas signé. La notice est périmée.
3. **Compteurs de téléchargements non fiables.** Les agents ont relevé 12, puis 18, puis 49 téléchargements. Les lectures faites pendant l'audit ont elles-mêmes gonflé ces compteurs (environ +25 sur le zip Mac Apple Silicon v0.36.0). Ils ne mesurent pas l'adoption.
4. **Dépôt public.** Ce dépôt est public : les détails exploitables d'une faiblesse de sécurité de l'application ne sont pas reproduits ici. Ils sont décrits de façon générale et peuvent vous être transmis en privé.

---

## 1. Expert poker Expresso/Spin et ranges préflop

### Points solides
- **Fait vérifié — le push/fold du Spin est juste.** L'équilibre tête-à-tête a été recalculé avec les matrices d'équité de l'application et comparé à la bibliothèque :

  | Tapis | Tapis SB (Nash recalculé) | Tapis SB (bibliothèque) | Call BB (Nash) | Call BB (bibliothèque) |
  |---|---|---|---|---|
  | 2 BB | 89,7 % | 89,5 % | 100 % | 100 % |
  | 3 BB | 77,6 % | 77,6 % | 92,5 % | 92,5 % |
  | 4 BB | 73,8 % | 73,8 % | 74,1 % | 74,1 % |

- **Fait vérifié — la phrase « résultat contrôlé » du site (site:526) se reproduit avec le moteur livré.** En Spin à 3 joueurs, aucun siège ne gagne plus de 0,0002 BB par main en s'écartant de la stratégie ; en tête-à-tête, l'écart monte à 0,015 BB à 15 BB. C'est bien une mesure **à l'intérieur du modèle**, comme le site l'écrit.
- **Fait vérifié — la démo du site est authentique.** La grille du héros (`DEMO`) est identique, case par case, au nœud « bouton, premier à parler » des données tournoi de l'application, aux 11 profondeurs.
- **Fait vérifié — méthode publiée.** Site (site:517-546) et aide de l'application (app:802-823) disent ce que le modèle ne sait pas faire. Garde-fous utiles : « Mes ranges » juge sur la range du joueur mais chiffre la perte avec le solveur ; décisions hors modèle listées à part ; correctif du « limp fantôme ».

### Problèmes observés
1. **Couverture du Spin surestimée (Fait vérifié).** Le site dit « Aucune situation de Spin ne te prend au dépourvu » (site:386). Or :
   - l'arbre à 3 joueurs ne contient ni limp au bouton, ni call de la SB face au min-raise, ni isolation de la BB face à un limp (`solver-core.js:406-437`) ;
   - la bibliothèque s'arrête à 15 BB et le tracker écarte les décisions Spin au-delà de 15,5 BB (app:3231) ;
   - la bibliothèque suppose des tapis égaux.

   **Hypothèse à confirmer dans les lobbys** : l'Expresso classique démarre à 25 BB (500 jetons en 10/20) et le Nitro à 15 BB. Si c'est exact, les premières mains de l'Expresso classique ne sont ni couvertes ni analysées.
2. **« BB perdues » faussées dans le tracker Spin (Fait vérifié).** La profondeur retenue est `min(tapis du héros, plus gros tapis adverse)` (app:2733), et non le tapis effectif face au joueur qui a misé. Exemple : une BB à 12 BB face au tapis d'un bouton à 4 BB est jugée comme à 12 BB. Des calls corrects à 4 BB (K5o, Q7o, J8o, A2o, T9s) sont alors comptés comme erreurs. Les Spin à gros jackpot sont jugés comme si seul le gagnant était payé (chipEV), et les décisions hors modèle sont exclues des totaux.
3. **Ranges tournoi 6-max : sorties atypiques (Fait vérifié sur les données, comparaison externe à confirmer).**
   - À 40 BB, le bouton ouvre K2o, Q6o et J8o mais se couche avec 87s, 76s, 65s et 54s. À 100 BB, il ouvre Q3o mais se couche avec 65s et 54s. Cause probable : la réalisation d'équité dépend seulement de l'équité brute, sans jouabilité par main (`solver-core.js:167-219`).
   - À 20 BB, la BB ne se couche jamais face au min-raise du bouton.
   - Le 0 % de limp de la démo vient d'une pénalité de 22 % du pot imposée au limpeur, pas d'un équilibre pur.
   - Marge d'erreur mesurée du modèle en tournoi : 0,014 BB par main (10 BB) à 0,090 BB (SB, 100 BB), soit 15 à 90 fois celle du Spin, et non publiée. Or le tracker compte une erreur dès 0,05 BB de perte.
4. **Tracker tournoi (Fait vérifié).**
   - Un tapis absent de la bibliothèque est converti en min-raise.
   - Seules les tables 6-max complètes sont analysées.
   - Aucun ICM dans le tracker : il n'existe que dans « Calculer mon spot », alors que le site met en avant « l'ICM de la bulle et de la table finale ».
   - L'ICM des tournois est mélangé à 15 % de chipEV (`ICM_MIX`, `solver-core.js:128`), ce qui n'est dit nulle part.
5. **Profils d'adversaires (Fait vérifié).**
   - « Huit types calibrés sur de vraies statistiques » (site:388) : ce sont des **cibles écrites à la main** (`PROF_STATS`, app:3782-3791), et les scripts de calage cités ne sont pas livrés.
   - En Spin, les profils réutilisent les réglages calés pour le 6-max à 20 BB.
   - L'étiquetage automatique applique les mêmes seuils au Spin et au 6-max : un joueur qui joue exactement l'équilibre du solveur en Spin à 3 (VPIP 41-48 %, PFR 23-26 %) serait étiqueté « Baleine ».
   - On peut asseoir un adversaire réel à la table du solveur dès 25 mains, avec une exploitation maximale : conseils extrêmes sur des lectures bruitées.
6. **« Ce que chaque erreur te coûte vraiment » (Observation).** La perte est mesurée face à des adversaires qui joueraient l'équilibre du modèle, pas face aux adversaires réels. Défendable, mais à expliquer.
7. **Verrouillage du solveur (Fait vérifié).** Il n'existe que dans l'interface de l'application : actif tant qu'une fenêtre de table Winamax ou PokerStars est détectée, et jusqu'à 2 minutes après la dernière main (app:5641-5642). Il ne couvre ni les autres rooms, ni le mobile, ni un second appareil. Un utilisateur technique peut aussi accéder à la bibliothèque hors de l'application, puisqu'elle est livrée en clair. La FAQ (« verrouille automatiquement dès qu'une table est ouverte ») est trop absolue.
8. **« 200 000 mains » et « jusqu'à 25 BB » (Fait vérifié : aucune trace).** Ni dans l'application, ni sur le site, ni dans la notice, ni dans l'historique git. Aucune unité ne rend « 25 BB » plausible comme moyenne : par tournoi, cela représenterait environ +33 points de taux de victoire en Spin, ce qui est impossible.

### Recommandations
| # | Action | Prio. | Coût |
|---|---|---|---|
| P-R1 | Ne publier ni « 200 000 mains » ni « jusqu'à 25 BB » sans le protocole de preuve décrit plus bas | P0 | faible |
| P-R2 | Remplacer « Spin complet / aucune situation » par une couverture fidèle (≤ 15 BB, tapis égaux en bibliothèque, lignes non modélisées) | P0 | faible |
| P-R3 | Tracker : tapis effectif face à l'adversaire concerné ; ne plus convertir un tapis en relance ; afficher le pourcentage de décisions hors modèle | P0 | moyen |
| P-R4 | Reformuler la promesse de verrouillage ; retirer la version développement des releases publiques | P0 | faible à moyen |
| P-R5 | Comparaison externe publiée de 30 à 50 spots face à une référence reconnue (HRC, ICMIZER ou GTO Wizard) | P1 | moyen |
| P-R6 | Réalisation d'équité par classe de main en tournoi profond, ou mention « bêta » au-delà de 25-30 BB | P1 | élevé |
| P-R7 | Étendre l'arbre Spin : limp au bouton, call de la SB, isolation de la BB, profondeurs de 16 à 25 BB | P1 | élevé |
| P-R8 | Profils propres au Spin ; minimum d'échantillon relevé ; exploitation partielle par défaut | P1 | moyen |
| P-R9 | Définir la perte sur le site et dans l'application ; signaler la marge du modèle en tournoi ; ICM près de la bulle | P1 | moyen |
| P-R10 | Publier la marge d'erreur en tournoi et le mélange ICM/chipEV de 15 % | P1 | faible |

**Protocole minimal de preuve pour toute allégation de performance :**
1. Définir l'allégation **avant** de mesurer : format, période, unité (taux de victoire en points ou chipEV par tournoi, jamais les euros bruts, qui dépendent du multiplicateur).
2. Prévoir un groupe témoin : utilisateurs contre non-utilisateurs comparables, ou avant/après avec témoin, et pré-enregistrer l'analyse.
3. Dimensionner l'échantillon : pour détecter +2 points de taux de victoire en Spin (base ≈ 35 %), il faut environ **9 000 Spins par groupe**.
4. Traiter les biais : retour à la moyenne après une mauvaise série, abandons, mesure circulaire avec la métrique du solveur lui-même, données hors échantillon.
5. Rapporter une moyenne avec un intervalle de confiance à 95 %, jamais « jusqu'à ».

### Questions pour le porteur
Que recouvrent les « 200 000 mains » (lecture d'historiques, comparaison de décisions, résultats) ? Quelle est l'unité des « 25 BB » ? D'où viennent les cibles des profils ? Combien d'itérations CFR ? Quelle part des mains de vos Expresso se joue au-dessus de 15 BB ? Quel pourcentage de décisions le tracker classe-t-il « hors modèle » sur un vrai échantillon ?

---

## 2. Expert produit et stratégie SaaS

### Points solides
- **Fait vérifié — application riche et largement opérationnelle :**
  - solveur Spin et tournoi ;
  - « Calculer mon spot » ;
  - profils ;
  - Mes ranges ;
  - tracker en 6 onglets ;
  - détection automatique des dossiers Winamax et PokerStars ;
  - leaks, sièges, variance, gains en euros ;
  - HUD ;
  - alertes de tilt ;
  - entraînement ;
  - 4 langues d'interface (FR, EN, ES, IT, app:7394).
- **Fait vérifié — une seule référence de calcul pour les trois outils.** L'entraînement rejoue de vraies erreurs du tracker, pondérées par leur coût (app:8134-8170). C'est le différenciateur à mettre au centre.
- **Fait vérifié — tarifs cohérents partout :** site (site:733), application (app:5370) et CGV art. 4.

### Problèmes observés
1. **Parcours coupé à chaque étape (Fait vérifié).**
   - Le site n'a aucun lien de téléchargement.
   - Les boutons d'essai mènent à « Le paiement ouvre bientôt ».
   - La carte bancaire exigée pour l'essai (CGV 6.2) n'est annoncée nulle part sur la page.
   - La licence est entièrement liée à Lemon Squeezy : hôte codé en dur et filtre réseau (`main.js:11`, `1046-1048`), format de réponse (app:5440-5452). Changer de prestataire impose une nouvelle version, sans mise à jour automatique sous Windows.
   - Les boutons « Essai gratuit de 7 jours » et le portail de résiliation de l'application pointent toujours vers la boutique refusée (app:5359-5368).
2. **Entraînement gratuit sur-promis (Fait vérifié).**
   - Le site dit « Pas des situations au hasard : celles que tu as ratées la veille » (site:409).
   - L'application dit « Des situations au hasard » (app:6878, 8294), et la source « Mes erreurs » exige le tracker, réservé à Track et Improve (app:8134-8144).
   - La formule gratuite n'existe pas dans les CGV, et l'art. 11 (« le logiciel ne peut plus être utilisé ») est contredit par l'entraînement qui reste ouvert.
3. **Collision de noms (Fait vérifié).** Le pilier « Improve » du site présente les leaks, sièges et variance, qui sont dans la **formule Track**.
4. **Version de test publique entièrement débloquée (Fait vérifié).** Sans boutique configurée, la licence renvoie la formule Improve sans expiration (app:5420-5423). Toutes les versions de v0.29 à v0.36 restent utilisables indéfiniment.
5. **Friction d'installation (Fait vérifié).**
   - 7 versions ont été publiées en environ 34 h, avec une fenêtre de mise à jour bloquante à chaque lancement.
   - Sur Mac, l'autorisation « Accessibilité » est à redonner après chaque version. Sans elle, le solveur peut se verrouiller à tort, même pour un abonné Solve seul (app:6915-6920).
6. **Aucun canal de retour (Fait vérifié).** La notice testeurs demande des captures sans donner d'adresse ; l'application n'a ni contact ni diagnostic à envoyer.
7. **Appel réseau non déclaré (Fait vérifié).** `version.json` est lu à chaque lancement (`main.js:67`), ce que ni la CGV 17.2 ni la notice ne mentionnent.

### Recommandations
| # | Action | Prio. | Coût |
|---|---|---|---|
| PR-R1 | Couche de licence et de paiement appartenant au porteur (activate/validate/deactivate), branchée sur un prestataire interchangeable, avec l'accord écrit du prestataire **avant** de développer | P0 | moyen |
| PR-R2 | Bêta fermée à clés nominatives ; versions de test qui expirent ; retrait des binaires débloqués publics | P0 | faible à moyen |
| PR-R3 | Page de téléchargement, adresse de contact, bouton « Copier mon diagnostic » (sans mains ni pseudos) | P0 | faible |
| PR-R4 | Aligner les promesses du site sur l'existant (entraînement, Spin, profils, changement de formule) | P0 | faible |
| PR-R5 | Rythme de publication hebdomadaire, notes de version, fenêtre de mise à jour qu'on peut ignorer | P1 | moyen |
| PR-R6 | Guider l'utilisateur jusqu'au premier leak chiffré : room détectée, import, « Tes plus gros leaks », « Voir la range » | P1 | faible à moyen |
| PR-R7 | Formule gratuite qui entraîne sur **ses propres** erreurs ; essai sans carte à tester | P1 | moyen |
| PR-R8 | Rationaliser les formules ou renommer les piliers du site pour supprimer la collision Improve | P1 | faible |
| PR-R9 | Priorité au segment Expresso Winamax France ; couvrir de 25 à 15 BB si le départ à 25 BB se confirme | P1 | moyen à élevé |
| PR-R10 | Indicateurs sans télémétrie cachée : serveur de licences, prestataire de paiement, diagnostic sur demande | P1 | faible |
| PR-R11 | Présenter le cash game honnêtement (« suivi et HUD, sans jugement du solveur ») | P2 | faible |

### Questions pour le porteur
Prestataire visé et motif exact du refus de Lemon Squeezy ; nombre de testeurs réels ; offre aux testeurs au lancement ; formule gratuite et essai (avec ou sans carte) ; capacité du support à tenir les 48 h promises (CGV 18) ; emplacement des sources.

---

## 3. Expert UX/UI et design

### Points solides
- **Fait vérifié — identité cohérente** entre le site et l'application : polices Barlow, mêmes variables de couleur, même logo, même slogan.
- **Une démo qui prouve au lieu d'affirmer** : la vraie grille du solveur avec un curseur de profondeur.
- **Ton honnête**, rare dans ce secteur (section Méthode, FAQ sur les règlements et sur les gains en euros).
- **Bases techniques saines** : rien ne déborde à 360 px, `prefers-reduced-motion` et `:focus-visible` sont pris en compte, le dialogue est natif.
- **Application** : 8 thèmes dont un thème daltonien, cases de grille en boutons étiquetés, états vides qui guident.

### Problèmes observés (site)
1. **Toutes les sorties de conversion sont fermées (P0)** : 5 boutons d'essai, aucun téléchargement, « résiliable en ligne » contredit par l'impasse de résiliation.
2. **La classe `.todo` masquait le focus clavier** des boutons d'essai, en plus de dessiner un contour pointillé : WCAG 2.4.7 non respecté. *Corrigé par l'audit.*
3. **Contrastes insuffisants** : badge et numéros de la méthode à 3,58:1, « 3 mois offerts » à 3,26:1 (*corrigés*). Au survol, le bouton rose devient vert #247260, proche du vert « limp » : *à arbitrer*.
4. **Démo :**
   - libellés de 8 px dans des cases de 51 px à 768 px ;
   - texte des cases mixtes à 2,45:1 ;
   - grille et prix vides jusqu'à 6,9 s en 4 Mbit/s, car le script vient après 2,8 Mo d'images ;
   - détail des mains seulement en infobulles, inaccessibles au clavier et au toucher.
5. **Captures :** 12 images de plus de 2 200 px affichées en 616 px, illisibles, avec trois palettes de couleurs pour les mêmes actions (thème violet, thème clair, démo).
6. **Dialogue de résiliation :** focus perdu, erreurs non annoncées, pas d'« Annuler » à l'étape 2 (*corrigés*).
7. **Lien de résiliation** cassé sur mobile dans les tarifs et le pied de page (*corrigé*).
8. **Pages légales :**
   - trois roses différents ;
   - mode sombre seulement sur ces pages ;
   - adresse en un seul bloc (*corrigée*) ;
   - deux dates de version dans les CGV ;
   - pas de lien de résiliation, alors que la FAQ le promet « en haut et en bas de chaque page ».

### Problèmes observés (application et HUD, source hors dépôt)
- **Navigation :** dans le solveur, la grille n'apparaît qu'après environ 1 490 px de défilement et 47 tabulations.
- **Badge « toi » invisible :** `--brand` et `--bg` ne sont pas définis.
- **Accès clavier :** l'import de fichiers est impossible au clavier.
- **Bandeau :** « Mode développement » s'affiche partout.
- **Libellés à clarifier :**
  - « Adapter les ranges à cette table » et « Adapter mes ranges » désignent deux fonctions différentes ;
  - le thème automatique « suit le réglage du Mac », y compris sous Windows.
- **HUD :**
  - fond blanc à 58 % sur un tapis sombre : les valeurs colorées tombent entre 1,65 et 3,2:1 ;
  - police jusqu'à 7 px, aucune police déclarée ;
  - textes en français codés en dur.

### Recommandations
- **Appliquées par l'audit** (voir `06-changements-code.md`) : A1 `.todo` ; A2 (contrastes, sauf la couleur de survol) ; A3 lien mobile ; A4 dialogue ; A5 accessibilité de la démo ; A8 message de paiement ; A11 en partie (polices, `header`, rose, adresse).
- **Non appliquées, faible risque mais à faire dans le générateur :**
  - A6 : charger la démo plus tôt ;
  - A7 : taille des libellés des cases ;
  - A9 : espace insécable avant « ? » ;
  - A10 : hiérarchie des titres.
- **Arbitrages du porteur :**
  - **B1 (P0)** : état honnête du site pendant la fermeture du paiement ;
  - B2 : section téléchargement ;
  - B3 : 6 à 8 captures recadrées, un seul thème, fichiers WebP `srcset` ;
  - B4 : surtitre explicite et héros plus court sur mobile ;
  - B5 : un seul ordre de formules ;
  - B6 : bandeau « Nouveau » ;
  - B7 : charte (tutoiement, un seul rose, mode sombre) ;
  - B8 : démo tactile.
- **Application (C1 à C8) :**
  - C1 : définir les variables manquantes ;
  - C2 : accès clavier ;
  - C3 : barre de contexte compacte pour voir la grille dès le premier écran ;
  - C4 : masquer le mode développement ;
  - C5 : renommer « Adapter mes ranges » en « Modifier mes ranges » ;
  - C6 : aligner les textes sur le site ;
  - C7 : HUD à 85 % d'opacité et 9-10 px minimum, police déclarée, repères non colorés, thème daltonien ;
  - C8 : contraste des boutons d'entraînement.

### Questions pour le porteur
Que veut-on pendant la fermeture du paiement (liste d'attente, bêta, site en veille) ? Quel thème de référence (clair ou violet) ? Quel ordre et quels noms de formules ? Le cash game doit-il figurer sur le site ? Quelles sont les couleurs réelles des tables sous le HUD ? Quelle est la part du trafic mobile ?

---

## 4. Expert développement et qualité logicielle

### Points solides
- **Site :**
  - **Fait vérifié** : aucun appel réseau, aucun traceur.
  - Données saisies injectées par `textContent`.
  - `noopener` sur les ouvertures de fenêtre.
  - `localStorage` protégé par `try/catch`.
  - Dimensions des images déclarées.
- **Application :**
  - **Fait vérifié** : `contextIsolation`, `sandbox`, sans `nodeIntegration`, pour la fenêtre principale et les HUD.
  - Pont de préchargement minimal.
  - CSP présente.
  - `openExternal` limité à `https`.
  - Liste blanche réseau.
  - Fusibles Electron durcis (`RunAsNode` désactivé, `OnlyLoadAppFromAsar`).
  - Échappement systématique des pseudos et notes.
  - Calculs en *workers*.
  - Lecture des historiques soignée (BOM, accents coupés, historiques PokerStars en français refusés avec un message clair).
  - Moteur et parseur chargeables sous Node : **testables**.

### Problèmes observés (site)
1. **Chaîne de production (Fait vérifié) :** téléversement manuel sur `main`, sans revue, CI ni tests ; générateur hors dépôt. Toute correction faite dans le dépôt sera écrasée au prochain téléversement.
2. **Domaine (Hypothèse) :** le fichier `CNAME` a été supprimé 44 minutes le 29/09 (commits `a5ec63b` puis `98a71b2`). Si le domaine n'est pas « vérifié » dans les réglages GitHub, une prise de contrôle du sous-domaine était théoriquement possible. **À vérifier.**
3. **Performances (Fait vérifié, mesures) :**

   | | Brut | gzip |
   |---|---|---|
   | `index.html` actuel | 3,27 Mo | 2,32 Mo |
   | Même HTML sans base64 | 123 Ko | 34 Ko |

   Démo et prix prêts au bout de **11,8 s** en 1,6 Mb/s, contre **0,36 s** si images et polices sont des fichiers séparés. Captures redimensionnées à 1 200 px : 2,1 Mo → 0,8 Mo.
4. **Bugs JavaScript visibles :**
   - message de paiement non retraduit ;
   - erreur de résiliation en français en mode anglais ;
   - libellé de la grille et 2 `alt` non traduits ;
   - curseur sans valeur lisible ;
   - message non annoncé.

   Bugs latents : infobulle sans limp, classe `l` sans style. *Tous corrigés par l'audit, sauf la classe `l`, sans effet aujourd'hui.*
5. **Mise à jour Mac (Fait vérifié) :** les `maj-mac-*.json` ne suivent pas le format attendu par `serverType: "json"`. Squirrel.Mac les accepte probablement, mais sans aucun contrôle de version. Risque de boucle de réinstallation si `version.json` et la release « latest » se désynchronisent. Le tag `V.036.0` n'est pas au format semver. **Tester sur Mac avant de modifier.**

### Problèmes observés (application)
1. **Défense en profondeur insuffisante dans les échanges entre l'interface et le système (Fait vérifié, détails non publiés ici).** Si du code malveillant s'exécutait un jour dans la fenêtre de l'application, il pourrait lire des fichiers en dehors des dossiers d'historiques choisis par l'utilisateur. Aucune faille permettant d'y injecter du code n'a été trouvée. Correctif simple : n'autoriser que les dossiers choisis par l'utilisateur ou détectés, et seulement les `.txt`.
2. **Electron 38.0.0 (Fait vérifié)** : branche plus maintenue depuis environ mars 2026.
3. **Durcissement absent :**
   - `'unsafe-inline'` dans la CSP ;
   - pas de contrôle de l'émetteur des messages ;
   - pas de gestionnaire de permissions ;
   - intégrité de l'archive désactivée ;
   - pas d'instance unique ;
   - URL de mise à jour fournie par la fenêtre.
4. **Licence (Fait vérifié) :** le mode développement vient d'une constante figée à la compilation (`storeId: 0`). Même configurée, la licence serait entièrement vérifiée côté client.
5. **Données (Fait vérifié) :** le nom de la machine est envoyé au vendeur. La capture prend des vignettes de toutes les fenêtres ouvertes avant de ne garder que les tables.
6. **Robustesse (Fait vérifié) :**
   - décodage différent selon le chemin d'import ;
   - surveillance des dossiers à environ 9 % d'un cœur pour 10 000 fichiers ;
   - aucun journal d'erreurs ;
   - croissance mémoire sans purge ;
   - solveur dupliqué à l'identique dans deux fichiers.

### Recommandations principales
| # | Action | Prio. | Coût |
|---|---|---|---|
| D1 | Builds « test » et « production » séparés ; la CI échoue si un build public garde le mode développement | P0 | faible |
| D2 | Restreindre la lecture de fichiers aux dossiers choisis ; vérifier l'émetteur des messages ; refuser les permissions par défaut ; bloquer le dépôt de fichiers hors de la zone d'import | P1 | faible |
| D3 | Passer à une version d'Electron maintenue ; intégrité de l'archive ; instance unique | P1 | moyen |
| D4 | Source du site dans le dépôt, script de build, PR et CI (validation HTML, axe, liens, JSON, budget de poids) | P1 | moyen |
| D5 | Images et polices en fichiers, `srcset`, prix et démo générés au build | P1 | faible à moyen |
| D6 | Vérifier le domaine dans GitHub | P1 | faible |
| D7 | Flux de mise à jour documenté et versionné, tags semver, publication « binaires puis `version.json` » | P1 | faible |
| D8 | Mettre à jour la notice testeurs (Mac signé : supprimer `xattr`) | P1 | faible |
| D9 | Journal d'erreurs local et « Copier le diagnostic » | P1 | faible |
| D10 | Tests : parseurs avec des historiques réels anonymisés, moteur (dont un test qui vérifie la phrase « un millième de BB »), licence, mise à jour | P1/P2 | moyen |
| D13 | Signature Windows et installateur | P2 | moyen à élevé |

---

## 5. Expert marketing, SEO et lancement

### Points solides
- **Une promesse différenciante :** même référence pour le solveur et le tracker, donc chaque leak chiffré en blindes.
- **Un H1 centré sur le problème :** « Sais-tu où tu perds, et combien ? »
- **Une démo réutilisable** en vidéo courte.
- **Une méthode honnête, des garde-fous en place :** non-affiliation, 18+, prévention.
- **Un argument vie privée crédible.**
- **Un contenu substantiel :** environ 3 000 mots, hiérarchie propre, `alt` descriptifs.

### Problèmes observés
1. **Promesses non tenues** dans la meta description et les boutons : essai de 7 jours, résiliation en trois clics.
2. **Couverture annoncée contradictoire :** la meta dit « de 100 à 2 blindes » alors que le solveur couvre 100 → 10 BB en tournoi.
3. **Formulations absolues :** « la meilleure action préflop pour chaque main », « aucune situation de Spin », « jusqu'à ce qu'elles partent ».
4. **« 200 000 mains » / « jusqu'à 25 BB » : risque juridique majeur (Fait vérifié sur extraits, à confirmer par un avocat).** L'article L121-4 du Code de la consommation range parmi les pratiques commerciales réputées trompeuses **en toutes circonstances** le fait d'affirmer qu'un produit augmente les chances de gagner aux jeux de hasard. La qualification du poker comme jeu de hasard est retenue par une partie de la jurisprudence (Cass. crim., 30 octobre 2013, n° 12-84784, selon Lexbase), pas par toute. Une allégation de gain peut donc être sanctionnée **même si le chiffre est exact**.
5. **SEO technique :**
   - titre de 103 caractères ;
   - meta de 259 caractères ;
   - ni canonical, ni Open Graph, ni `robots.txt`, ni `sitemap.xml` (*ajoutés par l'audit, sauf l'image de partage*) ;
   - version anglaise injectée en JavaScript, sans URL ni `hreflang` : invisible pour Google.
6. **Mots-clés absents :** les termes cherchés par les joueurs ne figurent pas dans le texte visible (« push », « nash », « tableau », « range expresso »). Aucun volume de recherche fiable n'a pu être obtenu.
7. **Publicité payante probablement bloquée (Hypothèse forte sur extraits) :** Google Ads réserve en France la certification « jeux » aux opérateurs agréés par l'ANJ et range certains logiciels de poker parmi les contenus liés au jeu ; Meta exige une autorisation préalable dans certains cas.
8. **Marque « Expresso » :** usage descriptif acceptable (art. L713-6 CPI), mais à ne jamais mettre dans un nom de produit, de domaine ou d'URL principale. **Le nom de travail « Range Poker Expresso » est donc à éviter comme nom commercial.**

### Recommandations
| # | Action | Prio. | Coût |
|---|---|---|---|
| M-R1 | Aligner messages et réalité avant tout trafic : bouton « Être prévenu de l'ouverture » tant que le paiement est fermé, retrait de « trois clics » tant que la résiliation ne fonctionne pas | P0 | faible |
| M-R2 | Interdire toute allégation de résultat ; parler de fonctions et de méthode | P0 | faible |
| M-R3 | Title, meta, Open Graph avec image 1200×630, données structurées sans note inventée | P1 | faible |
| M-R4 | Pages par segment (`/expresso-spin/`, `/tournois-6-max/`, `/tracker-hud/`, `/methode/`, `/guides/`), puis `/en/` avec `hreflang` | P1-P2 | moyen |
| M-R5 | Téléchargement gratuit (10 mains par jour) en bouton principal, une fois la licence en place | P1 | moyen |
| M-R6 | HUD : ne pas écrire « HUD Winamax » sans l'accord du service Intégrité | P1 | faible |
| M-R7 | Plan éditorial de 8 guides (grilles push/fold Expresso par profondeur, ICM du jackpot, mesure d'un leak, variance, règlements des rooms…) | P1-P2 | moyen |
| M-R8 | Communautés en transparence totale : se présenter comme l'éditeur, avec l'accord des modérateurs | P1 | faible |
| M-R11 | Mesure respectueuse : Search Console, compteurs du serveur de licences, mesure d'audience exemptée de consentement selon la doctrine CNIL, CGV 17.7 mise à jour | P1 | faible |
| M-R12 | Liste d'attente conforme : `mailto` prérempli ou formulaire avec information RGPD et case non pré-cochée | P1 | faible |

Formulations prudentes et variantes de titres, meta et héros : voir `03-synthese-et-positionnement.md`.

---

## 6. Expert marché, concurrence, prix et offres

Le détail sourcé (tableau comparatif, options de prix, prestataires de paiement) est dans `04-marche-prix-offres.md`. Constats principaux :

1. **Le seul vrai différenciant est la combinaison** dans un logiciel local : tracker et HUD, solveur préflop Spin et tournoi, coût des leaks sur la même référence, profils par siège, Mac et Windows, en français. Aucun concurrent trouvé ne réunit tout cela (sous réserve des extraits). **Pris un par un, aucun de ces arguments n'est exclusif :**
   - Mac et français : Xeester, Poker Copilot, Poker Sciences ;
   - leaks en EV : GTO Wizard Analyzer, Poker Spin Tracker ;
   - 10 mains gratuites par jour : GTO Wizard ;
   - HUD Expresso : le HUD natif gratuit de Winamax.
2. **Concurrent le plus proche :** Poker Sciences (français, centré sur le Spin) :
   - tracker gratuit jusqu'à 2 000 spins ;
   - 15 €/mois payés par semestre, ou 39 €/mois en Pro ;
   - pack de 401 ranges à 390 € en achat unique.
3. **Prix de milieu de marché :**
   - Improve est bon marché face à GTO Wizard ;
   - Solve est un peu au-dessus des outils Spin seuls, mais inclut les tournois ;
   - Track devient plus cher que les trackers établis au-delà d'un an.
4. **Essai de 7 jours avec carte :** en dessous du marché (14 à 30 jours, souvent sans carte).
5. **Paiement :** le refus vient de l'écosystème Stripe (Lemon Squeezy appartient à Stripe). Stripe Managed Payments est donc déconseillé ; Paddle est la piste n° 1 (précédent : HRC, un solveur de poker, vend via Paddle) ; Stripe en direct la piste n° 2 (précédent : GTO Wizard). **Acceptation à confirmer par écrit.**
6. **Test de prix impossible** tant que l'application complète est gratuite et publique.

---

## 7. Expert confiance, conformité et intégrité des rooms

*Ce rapport n'est pas un avis juridique. Il liste des risques à faire trancher par les rooms, un avocat (consommation, jeux) ou un DPO.*

### Points solides
- **FAQ prudente :** solveur interdit pendant le jeu, HUD seulement là où la room l'autorise.
- **Verrou étendu :** il couvre aussi « Mes ranges », « Calculer mon spot », l'entraînement, « Voir la range » et « L'asseoir à la table du solveur » (app:5641, 6910, 6822, 4985, 6588).
- **OCR sobre :** local, en mémoire seulement, déclenché seulement avec au moins 2 Spin ouverts.
- **Bonnes clauses dans les CGV :** remboursement si une room interdit le logiciel (art. 12), outil qui ne choisit ni tables ni places (art. 5.4).
- **Alertes de tilt.**

### Règles des rooms (extraits de recherche du 2026-10-02, à relire sur les pages officielles)
- **Winamax :**
  - autorise les statistiques et le « profiling » sur ses propres données ;
  - interdit les solveurs (au moins pendant le jeu), les *seating scripts*, l'échange de données de jeu et les HUD « dynamiques » ;
  - dit pouvoir analyser les processus ouverts ;
  - **exige l'accord préalable du service Intégrité** pour tout logiciel absent de sa liste.
- **PokerStars :**
  - statistiques **numériques** permises en jeu ;
  - interdits **dès qu'un client PokerStars est ouvert** : les références au-delà d'un niveau basique et les calculs d'équité avancés (range contre range, ICM, Nash) ;
  - selon la politique de 2015, à revérifier : pas de données non numériques dans le HUD ni de catégorisation des joueurs.
- **Betclic :** selon la presse, HUD interdits et historique téléchargeable une fois par jour seulement.
- **PMU et bet365 :** sources contradictoires ou secondaires, à confirmer.

### Matrice fonction × room (résumé)
| Fonction | Winamax | PokerStars | Betclic |
|---|---|---|---|
| Import d'historiques après la session | Autorisé | Autorisé | ? |
| HUD de statistiques numériques | Autorisé sous réserve de l'accord Intégrité | Autorisé | Interdit (presse) |
| HUD avec icônes de type, courbe, notes | Ambigu | **Probablement interdit** (à confirmer) | Interdit (presse) |
| Capture d'écran + OCR des pseudos | ? (aucune règle trouvée) | ? | ? |
| Solveur, ranges, entraînement | Interdit pendant le jeu | **Interdit dès que le client est ouvert** | Interdit probable |
| Verrou actuel (table détectée + 2 min) | Ambigu (le processus reste lancé) | **Insuffisant** (le lobby est exclu, `main.js:547`) | Inopérant (room non détectée) |
| Colonne « Solveur » et « % conseillé » du tracker pendant une session | Ambigu | **Probablement interdit** | ? |

### Problèmes observés
1. **Verrou trop étroit et « ouvert en cas de panne » (Fait vérifié).**
   - La détection exclut le lobby et les rooms autres que Winamax et PokerStars.
   - Si elle échoue, le solveur reste ouvert sans alerte (`main.js:539`).
   - L'onglet « Décisions préflop », qui affiche la stratégie du solveur pour les mains venant d'être jouées, n'est pas verrouillé (app:5277-5292).
2. **HUD actif par défaut (Fait vérifié)**, avec icônes de type, courbe et notes, sans rappel des règles de la room (`main.js:575`, app:6024). Cela contredit le conseil de la FAQ.
3. **Capture d'écran et OCR passés sous silence** sur le site et dans les CGV (Fait vérifié).
4. **Contradiction marketing / CGV :** « repérer ceux qu'il faut éviter — et ceux qu'il faut chercher » (site:399) contre « ne sélectionne ni les tables ni les places » (CGV 5.4).
5. **Historiques d'autrui :** aucun garde-fou contre l'import des mains d'autres joueurs, alors que les rooms interdisent l'échange de mains.
6. **RGPD :**
   - marqueur « [Base légale … à arbitrer] » visible en ligne (CGV 17.4) ;
   - le diagnostic demandé aux testeurs contient des pseudos de tiers lus par OCR ;
   - le nom de l'ordinateur est transmis au vendeur (un identifiant aléatoire suffirait) ;
   - CGV 17.2 inexacte (le contrôle de mise à jour transmet l'IP à GitHub) ;
   - Google Fonts sur les pages légales, contraire à la CGV 17.7 (*corrigé par l'audit*) ;
   - la politique de confidentialité citée par les mentions légales n'existe pas.
7. **Droit de la consommation (textes à faire valider) :**
   - résiliation en trois clics non fonctionnelle (art. L215-1-1 et D215-1 à D215-3 C. conso.) ;
   - contradiction entre l'essai de 7 jours (CGV 6.2) et la rétractation (CGV 8 : sans renonciation, accès après 14 jours) ;
   - aucun médiateur de la consommation (L612-1) ni numéro de téléphone (R111-1) ;
   - dates de version incohérentes ;
   - mentions Lemon Squeezy / « Sold through Link, LLC » devenues fausses ;
   - offre d'essai affichée alors qu'elle est indisponible (L121-2).
8. **Éditeur :** vérifier sur le Kbis et les statuts que l'objet social et le code d'activité de la SARL couvrent l'édition et la vente de logiciels. Une source secondaire indique un code d'activité sans rapport, ce qui reste à confirmer.
9. **Application :** aucun message de prévention ni mention 18+.
10. **Distribution :** exécutable Windows non signé ; notice qui conseille de contourner Gatekeeper (inutile depuis que le Mac est signé) ; PowerShell lancé avec `-ExecutionPolicy Bypass`, motif souvent signalé par les antivirus.

### Recommandations
| # | Action | Prio. | Coût |
|---|---|---|---|
| C-1 | Écrire au service Intégrité de Winamax et à PokerStars avec une fiche technique honnête (HUD, icônes, OCR, solveur présent dans le processus) et obtenir des réponses écrites, avant d'annoncer d'autres rooms | P0 | faible (délai) |
| C-2 | Verrou « fermé en cas de doute » : lobby compris (au moins PokerStars), colonnes solveur masquées en session, bandeau si la détection échoue, FAQ corrigée | P0 | moyen |
| C-3 | HUD désactivé par défaut ; à l'activation, règle de la room et mode strict « statistiques numériques seules » | P0 | moyen |
| C-4 | Bêta privée, binaire débloqué retiré, signature Windows, consigne `xattr` supprimée | P0 | moyen |
| C-5 | CGV et mentions refaites avec un avocat avant de rouvrir la vente : prestataire, résiliation qui notifie vraiment, médiateur, téléphone, essai cohérent avec la rétractation, changement de formule | P0 | moyen |
| C-6 | Polices auto-hébergées sur les pages légales | P1 | faible (*fait*) |
| C-7 | Politique de confidentialité complète, avec registre des traitements | P1 | moyen |
| C-8 | Dire la capture d'écran et l'OCR (FAQ, CGV, consentement dans l'application) | P1 | faible |
| C-9 | Revoir les affirmations (« vraies statistiques », « à éviter / à chercher », offre indisponible) | P1 | faible |
| C-10 | Limiter les statistiques aux mains des pseudos déclarés par l'utilisateur | P2 | moyen |
| C-11 | Message de prévention et mention 18+ dans l'application ; vérifier les marques | P2 | faible |
| C-12 | Vérifier l'objet social, le code d'activité et l'assurance responsabilité civile professionnelle | P2 | faible |
