# 03 — Synthèse et positionnement

Synthèse du coordinateur, rédigée à partir de l'état des lieux (`01`) et des sept rapports d'experts (`02`). Elle tranche les contradictions entre rapports au lieu de les juxtaposer.

Légende : **Fait vérifié** · **Observation** · **Hypothèse** · **Recommandation**.

---

## 1. Diagnostic général

### Où en est réellement le projet

**Fait vérifié.**
- Solve It Poker est un **logiciel de bureau avancé techniquement** : version 0.36.0, Electron, Mac et Windows.
- Il réunit un solveur préflop Spin et tournoi 6-max, un tracker avec HUD, un chiffrage des leaks et un entraînement.
- Son site vitrine est soigné et honnête sur sa méthode.

Mais **il n'est pas commercialisable aujourd'hui**, pour quatre raisons :

1. **Pas de paiement.** Lemon Squeezy a refusé la boutique le 1er octobre 2026 : aucun essai, aucun abonnement, aucune résiliation fonctionnelle.
2. **Pas de licence.** Le module de licence de l'application est codé pour Lemon Squeezy. Sans boutique, l'application publique v0.36.0 bascule en « Mode développement » : **produit complet, gratuit, sans limite de durée**, téléchargeable par tous depuis un dépôt public.
3. **Conformité aux rooms non établie.** Le HUD est actif par défaut, avec icônes de type et notes ; l'application capture les fenêtres de tables pour lire les pseudos par OCR ; le verrou du solveur ne couvre ni le lobby ni les autres rooms. Aucune réponse écrite de Winamax ni de PokerStars n'est connue.
4. **Documents légaux à refaire.** Les CGV se déclarent elles-mêmes « non applicables tant qu'elles n'ont pas été relues par un conseil ». Elles citent un vendeur qui n'existe plus et contredisent la FAQ.

### Principaux atouts
- **Une idée différenciante et réellement livrée** (Fait vérifié) : la même référence de calcul pour le solveur, le tracker et l'entraînement, ce qui permet de chiffrer chaque leak en blindes. Aucun concurrent trouvé ne réunit tout cela dans un logiciel local (sous réserve des extraits de recherche).
- **Un moteur juste là où il est le plus utilisé** (Fait vérifié) : le push/fold du Spin correspond à l'équilibre recalculé indépendamment (2 à 4 BB, au dixième de point près).
- **Une transparence rare** : section Méthode, limites écrites, « mesure faite à l'intérieur du modèle », FAQ sur les règlements des rooms et sur les gains en euros.
- **Une base technique saine** : isolation Electron, calcul local, aucun traceur sur le site, application Mac signée et notarisée.

### Principaux freins
- **Les quatre bloquants ci-dessus.**
- **Une promesse qui dépasse l'existant sur plusieurs points précis** (Fait vérifié) :
  - « Spin complet », alors que la couverture va de 15 à 2 BB ;
  - « huit types calibrés sur de vraies statistiques », alors que ce sont des cibles écrites à la main ;
  - l'entraînement gratuit « sur tes erreurs de la veille », alors qu'il tire des situations au hasard ;
  - le verrouillage présenté comme « automatique dès qu'une table est ouverte ».
- **Un chiffrage des leaks fragile** (Fait vérifié) : le tracker Spin choisit parfois la mauvaise profondeur, convertit un tapis en relance en tournoi, ignore l'ICM et le jackpot, et compte en tournoi des « erreurs » plus petites que la marge du modèle. Or c'est **le cœur de la promesse**.
- **Une chaîne de production fragile** (Fait vérifié) : sources hors dépôt, téléversement manuel, 7 versions en 34 h, aucun test ni CI.
- **Aucune donnée d'usage** (Fait vérifié) : pas de mesure, pas de canal de retour des testeurs. Les compteurs GitHub ont été gonflés par l'audit lui-même.

### Ce qui manque de preuves
- **« 200 000 mains réelles » et « jusqu'à 25 BB d'amélioration » (Fait vérifié)** : aucune trace dans le dépôt, l'application ou l'historique.
- **« 25 BB »** : en l'état, aucune unité ne rend ce chiffre plausible comme moyenne.
- **Les règles des rooms et les prix des concurrents** : ils ne sont connus que par des extraits de recherche.

### Ce qui est convaincant
- Le moteur Spin en push/fold.
- L'honnêteté méthodologique.
- L'intégration solveur-tracker.
- La qualité visuelle cohérente entre le site et l'application.

---

## 2. Proposition de valeur

### Pour qui
- **Cible prioritaire (Recommandation) : les joueurs réguliers d'Expresso sur Winamax en France, des petites aux moyennes limites.** C'est là que l'outil est le plus juste (push/fold de 15 à 2 BB), que l'interface française compte, et que le Mac est un plus.
- **Cible secondaire :** les joueurs de tournois 6-max, pour l'étude préflop avec ICM dans « Calculer mon spot ».
- **Plus tard :** les joueurs PokerStars (historiques en anglais obligatoires ; HUD à clarifier) et le cash game, pour le seul suivi.

### Problème résolu
« Je joue beaucoup d'Expresso, je ne sais pas où je perds ni combien. Les tableaux de push/fold gratuits ne me disent pas lesquelles de mes décisions réelles me coûtent le plus. »

### Ce qui différencie (à dire)
1. Le même calcul juge les décisions du joueur et lui montre la bonne grille.
2. Les leaks sont classés par coût, pas par fréquence.
3. Tout est calculé en local.
4. L'outil existe en français, sur Mac comme sur Windows.

### Ce qui ne différencie pas (à ne pas mettre en avant)
- Mac, français, HUD, 10 mains gratuites par jour : d'autres outils les proposent déjà.
- Le HUD Expresso : Winamax a son propre HUD gratuit depuis octobre 2025.

### Formulations possibles, selon le positionnement retenu
Les variantes ci-dessous restent dans le ton actuel (tutoiement, sobriété) et ne promettent aucun gain. **Le choix vous revient.**

1. **Tracker d'abord** : « Tes erreurs préflop, chiffrées en blindes. Le solveur dit ce qu'il fallait faire, le tracker mesure ce que tu as fait, avec le même calcul. »
2. **Étude d'abord** : « Tapis, min-raise ou fold : la grille de chaque profondeur, de 15 à 2 BB en Spin et de 100 à 10 BB en tournoi 6-max. »
3. **Accroche actuelle conservée** : « Sais-tu où tu perds, et combien ? » Elle est bonne, mais le sous-titre doit nommer le produit et ses limites : « Solveur préflop et tracker pour l'Expresso et le tournoi 6-max : chaque écart avec le calcul est chiffré en blindes, sur ton ordinateur. »

**Titres de page proposés** (54 à 58 caractères, contre 103 aujourd'hui) :
- « Solveur préflop Spin et tournoi 6-max | Solve It Poker »
- « Solve It Poker : tes leaks préflop chiffrés en blindes »

**Meta description proposée** (sans l'essai, tant qu'il n'existe pas) : « Solveur préflop pour le Spin et le tournoi 6-max, tracker et HUD : chaque erreur préflop chiffrée en blindes. Mac et Windows, calcul en local. »

**Nom du produit (Recommandation).** Gardez « Solve It Poker ». Le nom de travail « Range Poker Expresso » contient la marque d'un opérateur (Expresso est utilisé par Winamax) : à éviter dans un nom de produit, de domaine ou d'URL principale (art. L713-6 CPI, usage seulement descriptif). L'enregistrement exact de la marque est à vérifier sur data.inpi.fr et l'EUIPO.

---

## 3. Produit et fonctionnalités

| Conserver | Améliorer | Ajouter | Repousser |
|---|---|---|---|
| Même référence pour le solveur, le tracker et l'entraînement | **Licence et paiement** derrière une couche à vous, avec un prestataire interchangeable | **Bêta fermée** à clés nominatives, versions de test qui expirent | PMU, Betclic, bet365 (règles défavorables ou inconnues) |
| Push/fold Spin de 15 à 2 BB | **Chiffrage des leaks** : tapis effectif correct, pas de tapis converti en relance, part « hors modèle » affichée, marge du modèle en tournoi, ICM et jackpot signalés | Page de téléchargement, contact, « Copier mon diagnostic » | Jugement des décisions après le flop |
| Transparence de la méthode | **Verrou** « fermé en cas de doute » : lobby compris, colonnes solveur masquées en session, alerte si la détection échoue | Parcours guidé jusqu'au premier leak chiffré | Version espagnole et italienne du marketing |
| Calcul local, aucune donnée de mains envoyée | **HUD** désactivé par défaut, avec un mode « statistiques numériques seules » | Formule gratuite qui entraîne sur **ses propres** erreurs | Solveur cash game |
| Profils par siège (le principe) | **Profils** propres au Spin, échantillon minimum plus élevé, exploitation partielle par défaut | Comparaison publiée de 30 à 50 spots avec une référence reconnue | Tables de 8 et 9 joueurs dans le solveur |
| Alertes de tilt, fenêtre d'export de 30 jours | **Ranges tournoi profondes** (connecteurs assortis) ou mention « bêta » au-delà de 25-30 BB | Couverture Spin de 16 à 25 BB, si le départ à 25 BB se confirme | — |
| Signature Mac | Signature **Windows**, notice testeurs, rythme de publication | Message de prévention et mention 18+ dans l'application | — |

**Arbitrage entre les experts.** Le marketing propose de mettre en avant le téléchargement gratuit ; la conformité et le produit demandent de retirer d'abord le binaire débloqué. **Décision recommandée :** d'abord une bêta fermée. Le téléchargement gratuit ne devient le bouton principal du site qu'une fois la licence en place, avec une formule gratuite bridée.

---

## 4. UX et site internet : changements prioritaires

L'identité est conservée partout : Barlow, fond #EEF0EC, rose #B34279, couleurs d'action, logo en grille.

### Site (page `index.html`)
| Zone | Changement | Statut |
|---|---|---|
| Barre du haut | Bouton « Essai gratuit » à remplacer par « Être prévenu de l'ouverture » tant que le paiement est fermé | **Votre accord requis** (B1) |
| Héros | Surtitre qui nomme le produit et les formats ; sous-titre court sur mobile pour faire remonter la démo ; « 7 jours d'essai, résiliable en ligne » à retirer tant que c'est faux | Votre accord requis |
| Démo | Accessible au lecteur d'écran, infobulle complète | **Fait par l'audit** |
| Démo | Charger plus tôt (moins de 1 s au lieu de 7 à 12 s en réseau lent) ; libellés lisibles à 768 px ; détail d'une main au toucher | À faire dans votre générateur |
| Bandeau « Nouveau » | À retirer ou à transformer en « Nouveautés de la v0.36 » | Votre accord requis |
| Fonctions | Corriger « Spin complet », « vraies statistiques », « situations ratées la veille » ; renommer les piliers ou les formules pour supprimer la collision Improve | Votre accord requis (textes proposés au § 8 et dans `06`) |
| Aperçu | 6 à 8 captures au lieu de 12, recadrées, un seul thème, en fichiers WebP `srcset` | À faire dans votre générateur |
| Méthode | Ajouter la définition de la perte, la marge du modèle en tournoi et le mélange ICM/chipEV | Votre accord requis |
| Tarifs | Contour `.todo` retiré, contrastes, lien de résiliation lisible sur mobile, message de paiement avec lien de contact | **Fait par l'audit** |
| Tarifs | Encadré « Paiement en cours de mise en place » ; un seul ordre de formules partout | Votre accord requis |
| FAQ | Verrouillage, changement de formule, essai, résiliation : réponses à aligner sur la réalité et les CGV | Votre accord requis |
| Dialogue de résiliation | Focus, erreurs annoncées, bouton « Annuler » | **Fait par l'audit** |
| Dialogue de résiliation | Sortie fonctionnelle : il faut un vrai service, qui dépend du prestataire | Bloquant, dépend du paiement |
| Pied de page | Polices locales, repères, adresse | **Fait par l'audit** (pages légales) |

### Pages légales
- **Fait par l'audit :** plus d'appel à Google Fonts, repère `header`, même rose que l'accueil, adresses sur plusieurs lignes.
- **À faire avec un conseil :** contenu (prestataire, résiliation, médiateur, téléphone, base légale, politique de confidentialité, dates).

### Application (source hors dépôt)
1. Faire apparaître la grille du solveur dès le premier écran (barre de contexte compacte, profils repliables).
2. Rendre visible le badge « toi » : les variables `--brand` et `--bg` manquent.
3. Rendre l'import possible au clavier.
4. Masquer le mode développement dans les versions publiques.
5. Rendre le HUD plus lisible : 85 % d'opacité, 9 à 10 px minimum, police déclarée, repères non colorés, thème daltonien.
6. Clarifier les libellés : distinguer « Adapter mes ranges » de « Adapter les ranges à cette table » ; remplacer « Suit le réglage du Mac » par « Suit le réglage du système ».

---

## 5. Marché et concurrence (résumé ; détail sourcé dans `04`)

- **Concurrence par brique :**
  - GTO Wizard pour l'étude et l'analyse ;
  - Poker Sciences pour le tracker et les ranges Spin en français ;
  - Xeester, Poker Copilot, PokerTracker 4 et Hand2Note pour les trackers ;
  - le HUD natif gratuit de Winamax ;
  - HRC et ICMIZER pour l'ICM ;
  - Kill Tilt, Poker Académie et Edgemy pour la formation.
- **Occasion de différenciation :** la boucle complète « grille, décision réelle, coût, entraînement » sur ses propres mains, en local et en français. À condition que le chiffrage soit fiable : c'est l'argument que les concurrents ne peuvent pas copier vite, mais aussi celui qu'un joueur expérimenté testera en premier.
- **Faiblesse face au marché :** la couverture Spin (15 BB contre 25 à 36 BB chez GTO Wizard, Spinwize et GTOBase, selon les extraits), et un essai plus court que la norme.
- **Limites de l'analyse :** les prix viennent d'extraits de moteur de recherche. Aucune page de tarifs n'a été lue en entier, et aucune donnée de demande n'est disponible.

---

## 6. Prix et formules (résumé ; options détaillées dans `04`)

**Recommandation : ne pas changer la grille actuelle avant d'avoir deux choses.**
1. Un paiement et une licence qui fonctionnent.
2. Des données réelles de bêta : entretiens, intention de payer, formats joués.

La grille actuelle (14,90 / 19,90 / 29,90 € par mois) est en milieu de marché et cohérente partout.

Points à décider ensuite :
- **Essai.** Essai de 7 jours avec carte, ou formule gratuite bridée (O2) et essai de 14 jours sans carte ? À tester. Le marché penche pour le sans-carte.
- **Formule centrée Expresso** (O1). À valider par les entretiens : un joueur de Spin pur paie aujourd'hui pour les tournois.
- **Licence fondateur** (O3), seulement une fois les CGV et la licence opérationnelles.
- **Libellé « Au lieu de 34,80 € »** à remplacer par « Track + Solve séparément : 34,80 € », pour éviter l'effet de prix barré (art. L112-1-1 C. conso., à faire valider).
- **Annuel** à n'ouvrir qu'une fois le taux de résiliation mensuel connu.

---

## 7. Marketing et lancement

### Messages
Fonctions et méthode ; jamais de promesse de résultat (voir § 8).

### Contenus
Huit guides prioritaires, qui ciblent les recherches des joueurs (« push or fold expresso », « tableau de nash expresso »…) :
1. Lire une grille push/fold Expresso de 15 à 2 BB.
2. Bouton entre 10 et 15 BB : min-raise ou tapis ?
3. ICM du gros jackpot.
4. Défendre la BB en Spin.
5. Mesurer un leak en BB, méthode et limites.
6. Variance en Expresso.
7. Trackers et HUD : ce que disent les règlements de Winamax et PokerStars.
8. Tournoi 6-max à 20 BB avec ante.

**Volumes de recherche à obtenir** avec Search Console, Keyword Planner et Trends : aucun volume fiable n'a pu être mesuré pendant l'audit.

### Canaux gratuits
- **Forums français** : Club Poker (section « Outils et logiciels », avec l'accord des modérateurs), Poker Académie, Kill Tilt. Toujours en se présentant comme l'éditeur.
- **Discord Spin** et **vidéos courtes** « un spot, une grille ».
- **Search Console.**

### Canaux payants
**Aucun budget publicitaire avant une pré-validation.**
- Google Ads réserve en France la certification « jeux » aux opérateurs agréés par l'ANJ et range certains logiciels de poker parmi les contenus liés au jeu (Hypothèse forte, sur extraits).
- Meta peut exiger une autorisation préalable.
- Avec des créateurs de contenu : contrat, mention « Collaboration commerciale » (loi n° 2023-451) et audience majeure.

### Étapes de lancement
- **Étape 0 — prérequis bloquants :**
  - prestataire de paiement ;
  - licence ;
  - résiliation fonctionnelle ;
  - CGV relues ;
  - binaire débloqué retiré ;
  - Windows signé ;
  - accord ou repositionnement du HUD ;
  - textes du site corrigés.
- **Étape 1 — bêta privée :** 3 à 4 semaines, 20 à 50 joueurs d'Expresso, licences de bêta, retours par e-mail ou Discord.
- **Étape 2 — pré-lancement :** pages par segment, 4 guides, Open Graph avec image, liste d'attente conforme, vidéo de 60 à 90 s.
- **Étape 3 — lancement :** envoi à la liste d'attente, fil de forum, vidéo. Pas de prix barré.
- **Étape 4 — de J+30 à J+90 :** créateurs de contenu et version anglaise selon les données.

### Indicateurs à suivre (sans traceur caché)
| Indicateur | Source |
|---|---|
| Impressions et clics par requête | Search Console |
| Téléchargements | Serveur de téléchargement (les compteurs GitHub ne sont pas fiables) |
| Inscriptions à la liste d'attente | Boîte mail ou outil retenu |
| Activations de licence, utilisateurs actifs par semaine | Serveur de licences, déjà prévu par la CGV 17.2 |
| Conversion essai → payant, résiliation à 1 et 3 mois | Tableau de bord du prestataire de paiement |
| Premier leak atteint, part de décisions hors modèle | Diagnostic copié volontairement |
| Motif de résiliation | Champ facultatif |
| Audience du site, si souhaitée | Outil configuré selon l'exemption CNIL, avec CGV 17.7 mise à jour |

---

## 8. Poker, confiance et conformité : à vérifier avant de commercialiser

### Règles des rooms (P0)
1. Envoyer une fiche technique honnête au service Intégrité de Winamax et au support de PokerStars : HUD avec icônes, notes et courbe ; capture d'écran et OCR des pseudos ; solveur présent dans le processus pendant le jeu ; tracker qui affiche la stratégie du solveur.
2. Obtenir des réponses **écrites**.
3. Ne mentionner « HUD Winamax » ou d'autres rooms qu'après ces réponses.
4. Ajuster le produit en conséquence : verrou fermé en cas de doute, HUD désactivé par défaut avec mode strict, capture et OCR expliqués et consentis.

### Droit de la consommation et données (P0 avant toute vente, avec un avocat et un DPO)
- CGV et mentions à refaire avec le nouveau prestataire.
- Résiliation en trois clics qui notifie vraiment.
- Médiateur de la consommation, téléphone.
- Essai cohérent avec la rétractation.
- Politique de confidentialité ; base légale des données d'adversaires.
- Identifiant aléatoire à la place du nom de l'ordinateur.
- Objet social de la société à vérifier.

### Présenter les performances : formulations prudentes
**Risque majeur (à confirmer par un avocat).** L'art. L121-4 du Code de la consommation range parmi les pratiques **toujours** trompeuses le fait d'affirmer qu'un produit augmente les chances de gagner aux jeux de hasard. Une partie de la jurisprudence qualifie le poker ainsi. **Même exacte, une phrase du type « jusqu'à +25 BB » peut donc être sanctionnée.** Gumroad, par exemple, exclut aussi « toute promesse de gain » de ses produits autorisés, et d'autres prestataires de paiement pourraient faire de même.

| À éviter | Proposé |
|---|---|
| « Améliore tes résultats en Spin jusqu'à 25 BB » | « Le tracker chiffre en blindes l'écart entre tes décisions préflop et le calcul du solveur. C'est une estimation du modèle, pas une prévision de gains. » |
| « Modèle testé sur plus de 200 000 mains réelles » | Seulement si c'est documenté, et sans le mot « testé » : « Le lecteur d'historiques a été vérifié sur N mains réelles de [rooms, période]. » Ou : « Profils calibrés sur les statistiques agrégées de N mains [origine, période] : méthode et limites ». Sinon, rien. |
| « La meilleure action préflop pour chaque main » | « La stratégie préflop d'équilibre du modèle, pour chacune des 169 mains » |
| « Spin complet. Aucune situation de Spin ne te prend au dépourvu. » | « Toutes les décisions préflop du Spin de 15 à 2 BB, à trois et en tête-à-tête, à tapis égaux dans la bibliothèque, à tapis différents dans “Calculer mon spot”. » |
| « Huit types calibrés sur de vraies statistiques » | « Huit types d'adversaires, calibrés sur des statistiques types (VPIP, relance, limp, 3bet) » |
| « Ce que chaque erreur te coûte vraiment » | « Ce que chaque erreur coûte selon le modèle, face à des adversaires qui joueraient l'équilibre » |
| « Le verrouille automatiquement dès qu'une table est ouverte » | « Le solveur se verrouille quand une table Winamax ou PokerStars est détectée sur cet ordinateur. Ce verrou ne remplace pas le respect du règlement de ta room. » |
| Témoignages | Réels, datés, avec accord écrit ; toute contrepartie mentionnée ; aucun avis rédigé par l'équipe |

**Si un résultat chiffré est publié un jour**, il faut un protocole (voir `02`, expert poker) et ce type de phrase : « Sur N joueurs suivis du [date] au [date], le taux de victoire a évolué de X points [IC 95 % : a ; b] par rapport au groupe témoin. Résultat passé, non garanti ; le poker comporte une forte part de hasard. » Le texte définitif est à faire valider par un avocat, au regard de l'art. L121-4.

---

## 9. Plan d'action

Le plan priorisé (impact, effort, dépendances, ordre) est dans `05-plan-daction.md`. Les cinq premières actions :
1. Retirer ou restreindre l'accès aux binaires débloqués publics.
2. Mettre le site dans un état honnête pendant la fermeture du paiement.
3. Écrire à Winamax et à PokerStars.
4. Choisir et faire pré-accepter par écrit un prestataire de paiement.
5. Faire relire les CGV, les mentions et la politique de confidentialité par un avocat.

---

## Annexe : contradictions entre rapports et arbitrages

| Sujet | Positions | Arbitrage du coordinateur |
|---|---|---|
| Signature Mac | Notice : « non signée » ; conformité : « signée, non notarisée ? » ; développement : signée et notarisée | **Fait vérifié : signée Developer ID et notarisée.** La notice est périmée ; seul Windows n'est pas signé. |
| Nombre de téléchargements | 12, 18, puis 49 selon l'heure | Compteurs gonflés par l'audit et par les mises à jour Mac. **Adoption inconnue** : à demander au porteur. |
| Tapis de départ de l'Expresso | 25 BB (classique) et 15 BB (Nitro), selon des extraits | **Hypothèse** à vérifier dans les lobbys Winamax. Elle conditionne la priorité de l'extension 16-25 BB. |
| Base juridique du risque sur les gains | Conformité : L121-2 (trompeuse selon le contexte) ; marketing : L121-4 (liste noire) | Retenir le **cas le plus strict** (L121-4) tant qu'un avocat ne s'est pas prononcé. Conséquence identique : aucune allégation de gain. |
| Bouton principal du site | Marketing : téléchargement gratuit ; produit et conformité : bêta fermée d'abord | **Bêta fermée maintenant**, téléchargement gratuit plus tard, quand la licence existe. |
| Prix | Marché : 5 options ; produit : rationaliser ; UX : réordonner | **Pas de changement de prix** avant paiement, licence et données de bêta. Seul l'ordre d'affichage peut être harmonisé tout de suite. |
| Images intégrées en base64 | UX et développement : extraire ; développement : ne pas le faire dans le dépôt | **À faire dans le générateur**, sinon le prochain téléversement l'efface. |
