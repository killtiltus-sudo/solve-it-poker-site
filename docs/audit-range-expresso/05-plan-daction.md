# 05 — Plan d'action priorisé

Les tâches sont classées par ordre recommandé.

**Priorité**
- P0 : bloque la vente ou expose à un risque sérieux.
- P1 : important pour un lancement crédible.
- P2 : utile.
- P3 : optionnel.

**Effort**
- faible : moins d'une journée.
- moyen : quelques jours.
- élevé : plus d'une semaine.

« Porteur » désigne une décision ou une démarche qui vous revient. « Dév. » désigne du code, dans le générateur du site ou dans l'application, dont les sources sont hors du dépôt.

---

## Phase 0 — Cette semaine : arrêter les fuites et clarifier

| # | Tâche | Impact | Effort | Prio. | Dépend de | Qui |
|---|---|---|---|---|---|---|
| 0.1 | **Restreindre l'accès aux binaires débloqués** : rendre les releases privées ou passer par un dépôt privé ou un lien non public, et ne plus publier de version en « Mode développement » | Fin de la distribution gratuite et illimitée du produit complet | faible | P0 | — | Porteur |
| 0.2 | **Reporter dans la source du site les correctifs de l'audit** (commit `6c31691`, détail dans `06`), sinon le prochain téléversement les efface | Conserve les gains d'accessibilité et de confidentialité | faible | P0 | — | Porteur / Dév. |
| 0.3 | **Mettre le site dans un état honnête pendant la fermeture du paiement** (textes prêts dans `06`, § 4) : remplacer les boutons d'essai par « Être prévenu de l'ouverture » ; retirer « 7 jours d'essai, résiliable en ligne » et « en trois clics » ; retirer « Essai gratuit 7 jours » de la meta description | Évite une pratique trompeuse (offre affichée mais indisponible) | faible | P0 | Votre accord sur les textes | Porteur |
| 0.4 | **Corriger les affirmations inexactes** (textes prêts dans `03`, § 8, et `06`, § 4) : « Spin complet », « vraies statistiques », entraînement gratuit « sur tes erreurs de la veille », verrouillage « automatique », changement de formule « au prorata » | Crédibilité ; risque L121-2 | faible | P0 | Votre accord | Porteur |
| 0.5 | **Ne publier nulle part** « 200 000 mains » ni « jusqu'à 25 BB » | Évite le risque L121-4 et un refus des prestataires de paiement | faible | P0 | — | Porteur |
| 0.6 | Vérifier que le domaine est « vérifié » dans les réglages GitHub (Pages) ; ne plus supprimer `CNAME` | Ferme un risque de prise de contrôle du sous-domaine | faible | P1 | Accès DNS | Porteur |
| 0.7 | Mettre à jour la notice testeurs : le Mac est signé, donc supprimer la consigne `xattr` ; ajouter une adresse de contact | Confiance, sécurité, retours des testeurs | faible | P1 | — | Porteur |

## Phase 1 — Avant de rouvrir la vente (2 à 6 semaines)

| # | Tâche | Impact | Effort | Prio. | Dépend de | Qui |
|---|---|---|---|---|---|---|
| 1.1 | **Écrire au service Intégrité de Winamax et à PokerStars** avec une fiche technique honnête (HUD avec icônes et notes, capture d'écran et OCR, solveur dans le processus, colonnes solveur du tracker) ; obtenir des réponses écrites | Protège les comptes des clients ; fonde toute promesse sur le HUD | faible (délai long) | P0 | — | Porteur |
| 1.2 | **Choisir le prestataire de paiement** : dossier de pré-acceptation écrit envoyé en parallèle à Paddle et à Stripe en direct, avec le motif exact du refus de Lemon Squeezy | Débloque tout revenu | faible à moyen | P0 | 0.5 | Porteur |
| 1.3 | **Couche de licence à vous** (activation, validation, désactivation ; jetons signés côté serveur ; identifiant aléatoire au lieu du nom de l'ordinateur) ; builds « test » et « production » séparés | Rend la vente possible et le changement de prestataire indolore | moyen | P0 | 1.2 | Dév. |
| 1.4 | **CGV, mentions légales, politique de confidentialité** refaites avec un avocat et un DPO :<br>- prestataire ;<br>- résiliation en trois clics qui notifie vraiment, avec accusé de réception ;<br>- médiateur de la consommation, téléphone ;<br>- essai cohérent avec la rétractation ;<br>- formule gratuite ;<br>- base légale des données d'adversaires ;<br>- capture d'écran et OCR ;<br>- appel à `version.json` ;<br>- dates unifiées ;<br>- objet social de la société | Conformité (L215-1-1, L612-1, R111-1, L121-2, RGPD) | moyen | P0 | 1.2 | Porteur + conseil |
| 1.5 | **Résiliation fonctionnelle** sur le site et dans l'application (portail du prestataire ou service à vous, avec confirmation par e-mail et protection contre les abus) | Obligation légale | moyen | P0 | 1.2, 1.4 | Dév. |
| 1.6 | **Verrou « fermé en cas de doute »** :<br>- lobby compris (au moins PokerStars) ;<br>- colonnes « Solveur » et « % conseillé » masquées en session ;<br>- bandeau si la détection échoue ;<br>- FAQ corrigée | Conformité aux rooms | moyen | P0 | 1.1 | Dév. |
| 1.7 | **HUD désactivé par défaut** ; à l'activation, règle de la room et mode « statistiques numériques seules » | Réduit le risque de sanction pour les joueurs | moyen | P0 | 1.1 | Dév. |
| 1.8 | **Chiffrage des leaks fiable** :<br>- tapis effectif face à l'adversaire concerné ;<br>- plus de conversion d'un tapis en relance ;<br>- part des décisions hors modèle affichée ;<br>- marge du modèle en tournoi ;<br>- ICM et jackpot signalés | Fiabilise le cœur de la promesse | moyen | P0 | — | Dév. |
| 1.9 | **Signature Windows** (Authenticode) | Fin de l'alerte SmartScreen ; confiance | moyen | P1 | Certificat (coût annuel à chiffrer) | Porteur / Dév. |
| 1.10 | Restreindre la lecture de fichiers de l'application aux dossiers choisis ; vérifier l'émetteur des messages ; passer à une version d'Electron maintenue ; une seule instance | Sécurité | faible à moyen | P1 | — | Dév. |
| 1.11 | Journal d'erreurs local et « Copier mon diagnostic », sans mains ni pseudos | Support et bêta exploitables | faible | P1 | — | Dév. |
| 1.12 | Expliquer la capture d'écran et l'OCR dans l'application et demander le consentement avant la première capture ; ajouter un message de prévention et la mention 18+ | Loyauté ; jeu responsable | faible | P1 | 1.4 | Dév. |

## Phase 2 — Bêta privée (3 à 4 semaines, 20 à 50 joueurs d'Expresso)

| # | Tâche | Impact | Effort | Prio. | Dépend de | Qui |
|---|---|---|---|---|---|---|
| 2.1 | Licences de bêta nominatives et datées ; recrutement transparent (Club Poker avec l'accord des modérateurs, Discord Spin) | Cohorte mesurable | faible | P1 | 1.3 | Porteur |
| 2.2 | Parcours guidé jusqu'au premier leak chiffré | Activation | faible à moyen | P1 | 1.8 | Dév. |
| 2.3 | Entretiens (10 à 15) : formats joués, tapis de départ, intention de payer, essai avec ou sans carte | Données pour choisir les prix (options dans `04`) | faible | P1 | 2.1 | Porteur |
| 2.4 | Mesurer sur de vraies mains la part des décisions Spin au-delà de 15 BB et des décisions hors modèle | Décide de l'extension de 16 à 25 BB | faible | P1 | 1.11 | Porteur / Dév. |
| 2.5 | Comparaison de 30 à 50 spots avec une référence reconnue (HRC, ICMIZER ou GTO Wizard) | Preuve de pertinence ; détecte les biais des ranges tournoi | moyen | P1 | Licence d'un outil de référence | Dév. |
| 2.6 | Tests automatisés du moteur et des parseurs avec des historiques réels anonymisés, dont un test qui vérifie la phrase « un millième de BB » | Non-régression | moyen | P1 | Historiques fournis par le porteur | Dév. |
| 2.7 | Lisibilité du HUD (opacité, taille, police, repères non colorés) et accès clavier de l'application | Qualité perçue, accessibilité | faible à moyen | P1 | — | Dév. |

## Phase 3 — Pré-lancement et lancement

| # | Tâche | Impact | Effort | Prio. | Dépend de | Qui |
|---|---|---|---|---|---|---|
| 3.1 | **Sources du site dans un dépôt (privé si besoin), avec build et CI** : validation HTML, axe, liens, JSON, budget de poids | Fin des écrasements, revue | moyen | P1 | — | Dév. |
| 3.2 | Images et polices en fichiers, captures réduites à 6 à 8 et recadrées, `srcset` ; démo et prix générés au build | Démo prête en moins d'1 s au lieu de 7 à 12 s en réseau lent | faible à moyen | P1 | 3.1 | Dév. |
| 3.3 | Choix de la grille de prix et de l'essai, à partir des données de bêta | Conversion | faible | P1 | 2.3 | Porteur |
| 3.4 | Pages par segment (Expresso/Spin, tournoi 6-max, tracker/HUD, méthode) ; nouveau title et nouvelle meta ; image de partage 1200×630 | Référencement, partages | moyen | P1 | 3.1 | Porteur / Dév. |
| 3.5 | Quatre premiers guides (push/fold Expresso, bouton entre 10 et 15 BB, ICM du jackpot, mesure d'un leak) | Trafic organique | moyen | P1 | — | Porteur |
| 3.6 | Liste d'attente conforme (`mailto` ou formulaire avec information RGPD, case non pré-cochée) ; Search Console | Captation de la demande et mesure | faible | P1 | 1.4 | Porteur |
| 3.7 | Lancement : envoi à la liste d'attente, fil de forum, vidéo de 60 à 90 s ; pas de prix barré | Premiers clients | faible | P1 | Tout ce qui précède | Porteur |

## Phase 4 — Après le lancement (J+30 à J+90)

| # | Tâche | Impact | Effort | Prio. | Dépend de |
|---|---|---|---|---|---|
| 4.1 | Étendre l'arbre Spin : limp au bouton, call de la SB, isolation de la BB, profondeurs de 16 à 25 BB | Couverture réelle du Spin | élevé | P1 (si 2.4 le justifie) | 2.4 |
| 4.2 | Profils propres au Spin ; seuils d'étiquetage par format ; exploitation partielle par défaut | Conseils moins extrêmes | moyen | P1 | 2.5 |
| 4.3 | Réalisation d'équité par classe de main en tournoi profond, ou mention « bêta » au-delà de 25-30 BB | Ranges tournoi crédibles | élevé | P1 | 2.5 |
| 4.4 | Version anglaise indexable (`/en/` avec `hreflang`) | Marché international | moyen | P2 | 3.1 |
| 4.5 | Partenariats avec des créateurs de contenu, après une pré-validation des règles publicitaires | Notoriété | moyen | P2 | Avis du conseil |
| 4.6 | Abonnement annuel ou licence fondateur | Trésorerie | faible | P2 | Taux de résiliation connu |
| 4.7 | Nouvelles rooms (PMU, Betclic, bet365), seulement après lecture de leurs règlements | Élargissement | élevé | P3 | Réponses écrites des rooms |
| 4.8 | Nettoyage du code : `main.js` découpé, données de ranges chargées à la demande, une seule copie du solveur, traduction par identifiants | Maintenabilité | moyen à élevé | P3 | 2.6 |

---

## Chemin critique

```
0.1 binaires retirés ─┐
0.5 aucune promesse ──┼─> 1.2 prestataire ─> 1.3 licence ─> 1.4 CGV ─> 1.5 résiliation ─┐
1.1 rooms (écrit) ─────> 1.6 verrou + 1.7 HUD ───────────────────────────────────────────┼─> 2.x bêta ─> 3.x lancement
1.8 chiffrage des leaks ─────────────────────────────────────────────────────────────────┘
```

Le délai le plus incertain est celui des réponses des rooms (1.1) et du prestataire de paiement (1.2). **Lancez ces deux démarches en premier.**
