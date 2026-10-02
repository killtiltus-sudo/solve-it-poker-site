# 06 — Changements de code

## 1. À lire d'abord

1. **Branche de travail, rien n'est publié.** Les changements sont sur `claude/range-poker-expresso-audit-2ofzgo`. Rien n'a été fusionné dans `main` : le site en ligne (GitHub Pages) **n'a pas changé**. Il n'y a eu ni déploiement, ni achat, ni prise de contact externe, ni modification de données de production.
2. **Corrections écrasées au prochain téléversement.** Votre site est généré hors du dépôt (`scripts_v5.js`…) puis téléversé à la main. Si vous ne reportez pas ces corrections dans votre source, **le prochain téléversement les effacera**. Le diff complet se lit avec :
   ```
   git diff ffefc4c 6c31691 -- index.html cgv.html mentions-legales.html
   ```
   Plus les nouveaux fichiers `fonts/`, `robots.txt` et `sitemap.xml`. La ligne du dictionnaire `I18N` est très longue : seul son début change (2 entrées ajoutées).
3. **Ne pas fusionner `docs/` dans `main`.** GitHub Pages publierait ces rapports sous `www.solve-it-poker.com/docs/…`. Le dépôt est déjà public : cette branche et ses rapports sont lisibles par tous.
4. **Le texte anglais suit le texte français à l'identique.** La traduction du site fonctionne par texte français exact. Toute modification d'un texte français doit aussi modifier la **clé** correspondante dans le dictionnaire `I18N`, sinon la version anglaise affiche le français.

Commits :
- `fab2acf` : état des lieux ;
- `6c31691` : correctifs du site ;
- les commits suivants : rapports.

---

## 2. Changements effectués

Tous sont circonscrits, sans effet sur la logique poker, les prix ni l'identité visuelle (mêmes polices, même rose, mêmes couleurs d'action).

| # | Problème observé | Changement | Bénéfice | Fichiers |
|---|---|---|---|---|
| 1 | La classe de travail `.todo` dessinait un contour pointillé rose autour des 3 prix et des 3 boutons d'essai sur la page publique, et masquait le contour de focus clavier de ces boutons (WCAG 2.4.7) | Classe retirée des 6 éléments (la règle CSS reste, inutilisée) | Page présentable ; focus de nouveau visible | `index.html` |
| 2 | Contrastes insuffisants : badge « Le plus complet » et numéros de la section Méthode à 3,58:1 ; « 3 mois offerts » sélectionné à 3,26:1 | Texte blanc sur rose (5,29:1), comme le bandeau « Nouveau » ; rose clair `#FF7AB6` sur fond sombre (6,94:1) | Conformité AA | `index.html` |
| 3 | Dialogue de résiliation : focus perdu après « Continuer », erreurs non annoncées, champs non marqués invalides, pas d'« Annuler » à l'étape 2, erreur dans le rose de la marque | Focus sur « Étape n sur 3 » à chaque étape ; `role="alert"` sur les erreurs ; `aria-invalid` sur les champs ; bouton « Annuler » à l'étape 2 ; erreur en rouge `--shove` (5,95:1) | Parcours utilisable au clavier et au lecteur d'écran | `index.html` |
| 4 | En anglais, l'erreur « Renseigne ton nom… » restait en français (la classe `.r-err` était exclue de la traduction) | L'exclusion ne vise plus que le message dynamique `#r-err2` | Version anglaise correcte | `index.html` |
| 5 | Message « Le paiement ouvre bientôt. Écris-nous… » : sans lien, non annoncé, jamais retraduit au changement de langue | « Écris-nous » devient un lien `mailto:contact@solve-it-poker.com` ; `role="status"` ; texte recalculé au changement de langue | Sortie de secours actionnable en attendant la réouverture du paiement | `index.html` |
| 6 | Démo : le curseur annonçait « 6 » au lieu de « 30 BB » ; libellé de la grille figé et non traduit ; l'infobulle omettait le limp et disait « fold » là où la légende dit « Se coucher » | `aria-valuetext` (« 30 BB ») ; libellé recalculé (« Grille des 169 mains au bouton à 30 BB : min-raise 45,4 %, se coucher 54,6 % ») en français et en anglais ; infobulle avec les 4 actions et les mots de la légende | Démo compréhensible sans la vue ; bug latent du limp corrigé | `index.html` |
| 7 | Sous 520 px, le lien « Résilier votre contrat » des tarifs et du pied de page se cassait en deux lignes minuscules (règles mobiles prévues pour la barre du haut) | Règles limitées à `.navr .resil-link` | Lien obligatoire lisible sur mobile | `index.html` |
| 8 | 2 textes alternatifs (captures du HUD) absents du dictionnaire anglais | 2 entrées ajoutées à `I18N` (texte anglais à relire) | Version anglaise complète pour les lecteurs d'écran | `index.html` |
| 9 | Éléments mal balisés : `aria-label` sur un `div` sans rôle (bandeau Nouveautés), `aria-labelledby` sur un `div` sans rôle (démo), champs sans `type` | `<nav>` pour le bandeau, `role="group"` pour la démo, `type="text"` | Sémantique valide (html-validate) | `index.html` |
| 10 | Aucune URL canonique ni aperçu de partage | `<link rel="canonical">` et balises Open Graph reprenant **mot pour mot** le titre et la description existants (sans image : à produire) | Partages propres ; pas de nouveau texte commercial | `index.html` |
| 11 | `cgv.html` et `mentions-legales.html` chargeaient Google Fonts, ce qui transmet l'adresse IP des visiteurs à Google, alors que la CGV 17.7 affirme qu'aucune donnée de navigation n'est collectée | Polices servies par le site : 5 fichiers woff2 extraits de `index.html` et Barlow Bold converti depuis la police de l'application ; licence OFL jointe | Plus aucune requête externe ; CGV 17.7 exacte sur ce point | `cgv.html`, `mentions-legales.html`, `fonts/` |
| 12 | Pages légales : contenu hors repère (axe), rose différent de l'accueil (#B8327F contre #B34279), adresses de l'éditeur et de l'hébergeur affichées en un seul bloc | `<header>` ; rose #B34279 en thème clair (le thème sombre est inchangé) ; `<br>` dans les adresses | Accessibilité, cohérence, lisibilité. **Aucun mot des textes légaux n'a changé.** | `cgv.html`, `mentions-legales.html` |
| 13 | Ni `robots.txt` ni `sitemap.xml` | Ajoutés (3 pages) | Indexation maîtrisée, Search Console | `robots.txt`, `sitemap.xml` |

---

## 3. Vérifications

Toutes les vérifications ont été faites sur une copie de travail, puis rejouées sur le dépôt après application (fichiers identiques octet pour octet).

| Contrôle | Avant | Après |
|---|---|---|
| JSON (`version.json`, `maj-mac-*.json`) et XML (`sitemap.xml`) | valides | valides |
| Syntaxe des scripts inline (`node --check`) | OK | OK |
| axe-core, 3 pages, à 1280 et 360 px | contraste `.badge` sur l'accueil (aux 2 largeurs) ; `region` sur la CGV et les mentions | **0 violation** |
| html-validate, hors règles de style | 6 erreurs d'accessibilité ou de sémantique | 2 restantes (`<label>` lié à l'`<output>` de la démo ; formulaire sans bouton d'envoi, voulu) |
| Erreurs JavaScript dans Chromium | 0 | 0 |
| Débordement horizontal à 360 px | 0 | 0 |
| Requêtes externes (3 pages) | Google Fonts sur 2 pages | **aucune** |
| Polices chargées sur les pages légales | Google (bloqué dans l'environnement d'audit) | Barlow 400/600/700 et Semi Condensed 700, en local |
| Prix affichés (mensuel et annuel) | 19,90 / 29,90 / 14,90 € ; 179 / 269 / 134 € | identiques |
| Message de paiement, en FR puis en EN | FR seulement, sans lien | FR et EN, lien `mailto` |
| Erreur de résiliation en EN | en français | « Enter your name and a valid email address. » |
| Focus après « Continuer » | `<body>` (perdu) | « Étape 2 sur 3 » |
| Infobulle d'une main avec limp (données simulées) | « AA · tapis 54 % » (limp absent) | « AA · tapis 54 %, limp 54 % » |
| `alt` restés en français en mode EN | 2 | 0 |

Scripts de vérification utilisés (Playwright + axe-core, hors dépôt) : `check.mjs`, `verify_fixes.mjs`, `verify_ux.mjs`, `limp_test.mjs`, `alt_en.mjs`. Ils peuvent servir de base à la CI proposée (tâche 3.1 du plan).

**Non vérifié :** le rendu sur Safari et Firefox (seul Chromium a été testé) et le comportement sur le site en ligne (inaccessible depuis l'environnement d'audit). L'application n'a pas été modifiée : son code source n'est pas dans le dépôt.

### Points résiduels connus
- Si l'on change de langue pendant que le dialogue de résiliation est ouvert, « Étape n sur 3 » et « non renseignée » restent dans l'ancienne langue jusqu'à la réouverture. C'est mineur.
- La classe CSS `l` (case où le limp domine) n'a toujours pas de style. Sans effet aujourd'hui : aucune case de la démo n'a de limp dominant.
- La règle `.todo` reste dans la feuille de style, sans élément qui l'utilise.

---

## 4. Propositions non appliquées : votre accord est requis

Ces changements touchent au message commercial, aux engagements légaux ou à la chaîne de production. Les numéros de ligne sont ceux de `index.html` **après** les correctifs (commit `6c31691`). Les textes sont prêts ; **dites-moi lesquels appliquer**. Chaque texte français modifié demandera aussi la mise à jour de sa clé dans `I18N` (voir § 1, point 4).

### 4.1 État honnête du site pendant la fermeture du paiement (P0)
| Emplacement | Texte actuel | Proposition |
|---|---|---|
| Barre du haut (l. 334) | « Essai gratuit » | « Être prévenu » (lien vers `#tarif`) |
| Héros, bouton (l. 351) | « Essayer 7 jours gratuitement » | « Être prévenu de l'ouverture » (`mailto` prérempli, objet « Prévenez-moi de l'ouverture ») |
| Héros, sous le bouton (l. 354) | « 7 jours d'essai gratuit, résiliable en ligne à tout moment. Pour Mac… » | « Ouverture des abonnements en préparation. Pour Mac (puce Apple et Intel) et Windows. » |
| Tarifs, titre (l. 560) | « Essaie sept jours, décide après » | Inchangé, avec en plus un encadré : « Le paiement n'est pas encore ouvert. Laisse-nous ton e-mail pour être prévenu. » |
| Tarifs, introduction (l. 561) | « … la résiliation se fait en ligne en trois clics, sans écrire à personne. » | À retirer tant que la résiliation ne fonctionne pas. À rétablir ensuite, en vérifiant que « Aucune formule ne se renouvelle sans que tu l'aies voulu » reste exact avec la reconduction automatique (CGV 6.3). |
| Boutons de formule (l. 579, 588, 596) | « Démarrer l'essai gratuit » | « Être prévenu » (même `mailto`) |
| Meta description | « Essai gratuit 7 jours. Solve It Poker calcule… » | « Solveur préflop pour le Spin et le tournoi 6-max, tracker et HUD : chaque erreur préflop chiffrée en blindes. Mac et Windows, calcul en local. » |

Attention : un `mailto` qui recueille des e-mails pour vous prévenir constitue un fichier de contacts. Il faut l'indiquer dans la CGV 17.7 ou dans la politique de confidentialité (finalité, durée, suppression après l'ouverture).

### 4.2 Affirmations à corriger (P0)
| Emplacement | Texte actuel | Proposition |
|---|---|---|
| Fonctions, « Spin complet » (l. 393) | « Spin complet » / « Aucune situation de Spin ne te prend au dépourvu. Les 14 tapis de 15 à 2 BB… » | « Spin de 15 à 2 BB » / « Toutes les décisions préflop du Spin de 15 à 2 BB, à trois et en tête-à-tête. Les 14 tapis, chaque option chiffrée en blindes, et le gros jackpot calculé en ICM et en euros de ton buy-in. » |
| Fonctions, « Profils » (l. 395) | « huit types calibrés sur de vraies statistiques » | « huit types calibrés sur des statistiques types » (à conserver tel quel seulement si vous avez une source de population) |
| Fonctions, « Entraînement » (l. 416) | « Pas des situations au hasard : celles que tu as ratées la veille, sur une vraie table… » | « Dix mains par jour, gratuites, sans carte bancaire, sur des situations tirées au hasard. Avec le tracker, l'entraînement te refait aussi jouer tes propres erreurs, avec la correction expliquée. Illimité avec Improve. » (Règle exacte d'accès à « Mes erreurs » selon la formule : **à confirmer** dans l'application.) |
| Fonctions, « Tes leaks, chiffrés » (l. 413) | « classées par ce qu'elles te coûtent vraiment » | « ce qu'elles te coûtent selon le modèle » |
| FAQ « Puis-je utiliser… pendant que je joue ? » (l. 608) | « … le verrouille automatiquement dès qu'une table est ouverte… » | « Le solveur, non : il est interdit pendant le jeu. Solve It Poker le verrouille quand il détecte une table Winamax ou PokerStars sur cet ordinateur, et jusqu'à deux minutes après ta dernière main. Ce verrou ne remplace pas le respect du règlement de ta room. » (suite inchangée) |
| FAQ « Puis-je changer de formule ? » (l. 610) et ligne des tarifs (l. 600) | « Oui, à tout moment… au prorata » | **À trancher** : la CGV art. 4 dit l'inverse. Soit la FAQ devient « Pas encore : pour changer de formule, résilie puis souscris la nouvelle », soit la CGV est modifiée quand le prestataire le permet. |
| Fonctions, « Adversaires et rapports » (l. 406) | « … pour repérer ceux qu'il faut éviter — et ceux qu'il faut chercher » | « … pour mieux connaître les réguliers de tes tables » (supprime la contradiction avec la CGV 5.4 et le risque de sélection de tables) |

### 4.3 Autres propositions
| Proposition | Pourquoi elle n'a pas été appliquée |
|---|---|
| Titre de page plus court (54 à 58 caractères, voir `03`, § 2) | Choix de message et de mots-clés : le vôtre |
| Couleur de survol des boutons roses : #8E2F5C au lieu du vert #247260, proche du vert « limp » | Change un jeton de la charte, partagé avec l'application |
| Images et polices en fichiers séparés, captures réduites | Gain majeur (HTML compressé de 2,3 Mo à environ 35 Ko ; démo prête en 0,36 s au lieu de 11,8 s en réseau lent), mais à faire **dans votre générateur**, sinon effacé au prochain téléversement |
| Script de la démo chargé avant les captures | Même raison (générateur) |
| Politique de confidentialité, CGV, mentions (prestataire, médiateur, téléphone, base légale, OCR, dates) | Textes juridiques : à faire avec un conseil |
| Lien « Résilier votre contrat » sur les pages légales (promis par la FAQ « en haut et en bas de chaque page ») | Inutile tant que le service de résiliation n'existe pas ; à ajouter avec lui |
| CSP par `<meta>` | Faisable (testé sans violation), mais les empreintes doivent être recalculées à chaque modification : nécessite un build |
| Correction des fichiers `maj-mac-*.json` (format attendu par `serverType: "json"`) | Exige un test réel de mise à jour sur Mac |
| Image de partage `og:image` 1200×630 | À produire (visuel) |
