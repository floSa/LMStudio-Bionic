# Bionic : plan détaillé des manuels

Plan des 15 manuels Bionic (00 à 14) avec, pour chacun, le contenu de chaque section. Version décrite : Bionic 1.1.7. Retour à l'[index Bionic](README.md) ; termes techniques : [glossaire](annexe-glossaire.md).

**Comment lire cette page** : chaque manuel est résumé en une phrase, puis ses sections sont listées avec ce qu'elles contiennent. Un clic sur une section ouvre le passage exact.

## Sommaire rapide

| Manuel | En une phrase |
|---|---|
| [00 — Notions fondamentales de l'agent](00-notions-agent.md) | Ce qui distingue un agent d'un chat : boucle d'actions, harnais, autorisations, contexte. |
| [01 — Présentation et installation](01-presentation-installation.md) | Ce qu'est Bionic, en quoi il diffère de LM Studio, installation, conflit entre les deux applications. |
| [02 — L'interface](02-interface.md) | Visite de l'écran : barre latérale, onglets, fil de session, zone de saisie, panneau de droite, raccourcis. |
| [03 — Les réglages](03-reglages.md) | Chaque page de Paramètres, ses champs, ses valeurs par défaut et des profils prêts à l'emploi. |
| [04 — Modèles](04-modeles.md) | Choisir, télécharger et régler un modèle pour l'agent ; mémoire AutoFit ; comparaison mesurée. |
| [05 — Projets et sessions](05-projets-et-sessions.md) | Organiser le travail : projets, dossier de travail, sessions, parallélisme, branches. |
| [06 — Documents et fichiers](06-documents.md) | Faire travailler l'agent sur des textes et des images : mémo, extraction de facture, contrôle du résultat. |
| [07 — Code, shell et autorisations](07-code-et-shell.md) | Confier une tâche de code : modes shell, scénario de correction de bogue, relecture, sécurité. |
| [08 — Compétences, palette `@` et MCP](08-competences-et-mcp.md) | Étendre l'agent : compétences réutilisables, références `@`, serveurs MCP (essai réel). |
| [09 — Saisie vocale](09-voix.md) | Dictée locale (non exécutée) : principe, mise en route, confidentialité. |
| [10 — Sécurité, compte, cloud, API locale](10-securite-compte-api.md) | Où vont les données, ce qui exige un compte, comment réduire les risques. |
| [11 — Recettes et dépannage](11-recettes-et-depannage.md) | Fiches par cas d'usage et diagnostic par symptôme. |
| [12 — Auto Review](12-auto-review.md) | Comment la vérification automatique décide d'exécuter une commande ; essais destructifs et incident. |
| [13 — Compétences en pratique](13-competences-en-pratique.md) | Une compétence de bout en bout : écrire, installer, déclencher, mesurer, faire créer par l'agent. |
| [14 — Commandes `/`, compaction, navigateur et fonctions annexes](14-commandes-compaction-navigateur.md) | Menu des commandes, compaction mesurée, navigateur intégré, Code Review, branches, recherche. |

---

## 00 — Notions fondamentales de l'agent

**Ce qui distingue un agent d'un chat : boucle d'actions, harnais, autorisations, contexte.** [Ouvrir le manuel](00-notions-agent.md).

| Section | Contenu |
|---|---|
| [1. Chat et agent](00-notions-agent.md#1-chat-et-agent) | Chat et agent : la différence. |
| [2. La boucle de l'agent](00-notions-agent.md#2-la-boucle-de-lagent) | Boucle de l'agent : réfléchir, appeler un outil, observer. |
| [3. Le harnais](00-notions-agent.md#3-le-harnais) | Harnais : le logiciel qui entoure le modèle. |
| [4. Où s'exécute le modèle](00-notions-agent.md#4-où-sexécute-le-modèle) | Où s'exécute le modèle : local, cloud, distant. |
| [5. Dossier de travail, fichiers du projet, fichiers externes](00-notions-agent.md#5-dossier-de-travail-fichiers-du-projet-fichiers-externes) | Dossier de travail, fichiers du projet, fichiers externes. |
| [6. Autorisations et niveaux de risque](00-notions-agent.md#6-autorisations-et-niveaux-de-risque) | Autorisations et niveaux de risque. |
| [7. Contexte et compaction](00-notions-agent.md#7-contexte-et-compaction) | Contexte et compaction. |
| [8. Compétences, MCP, sous-agents](00-notions-agent.md#8-compétences-mcp-sous-agents) | Compétences, MCP, sous-agents. |
| [9. Ce que la taille du modèle change](00-notions-agent.md#9-ce-que-la-taille-du-modèle-change) | Ce que la taille du modèle change (mesures sur deux postes). |
| [10. Lexique rapide](00-notions-agent.md#10-lexique-rapide) | Lexique rapide. |

## 01 — Présentation et installation

**Ce qu'est Bionic, en quoi il diffère de LM Studio, installation, conflit entre les deux applications.** [Ouvrir le manuel](01-presentation-installation.md).

| Section | Contenu |
|---|---|
| [1. Qu'est-ce que Bionic](01-presentation-installation.md#1-quest-ce-que-bionic) | Qu'est-ce que Bionic. |
| [2. Bionic et LM Studio : différences](01-presentation-installation.md#2-bionic-et-lm-studio--différences) | Différences avec LM Studio. |
| [3. Installation](01-presentation-installation.md#3-installation) | Installation. |
| [4. Premier lancement](01-presentation-installation.md#4-premier-lancement) | Premier lancement. |
| [5. Conflit avec LM Studio](01-presentation-installation.md#5-conflit-avec-lm-studio) | Conflit avec LM Studio : ne pas les ouvrir ensemble. |
| [6. Emplacements des données](01-presentation-installation.md#6-emplacements-des-données) | Emplacements des données. |
| [7. Mises à jour](01-presentation-installation.md#7-mises-à-jour) | Mises à jour. |
| [8. Ce qui fonctionne sans compte](01-presentation-installation.md#8-ce-qui-fonctionne-sans-compte) | Ce qui fonctionne sans compte. |
| [9. Désinstallation et nettoyage](01-presentation-installation.md#9-désinstallation-et-nettoyage) | Désinstallation et nettoyage. |

## 02 — L'interface

**Visite de l'écran : barre latérale, onglets, fil de session, zone de saisie, panneau de droite, raccourcis.** [Ouvrir le manuel](02-interface.md).

| Section | Contenu |
|---|---|
| [1. Vue d'ensemble](02-interface.md#1-vue-densemble) | Vue d'ensemble. |
| [2. Barre latérale gauche](02-interface.md#2-barre-latérale-gauche) | Barre latérale gauche : projets, sessions, conversations. |
| [3. Barre d'onglets](02-interface.md#3-barre-donglets) | Barre d'onglets. |
| [4. Fil de la session](02-interface.md#4-fil-de-la-session) | Fil de la session : messages, travail déplié, fichiers modifiés. |
| [5. Zone de saisie](02-interface.md#5-zone-de-saisie) | Zone de saisie : modèle, mode shell, pièces jointes. |
| [6. Panneau de droite](02-interface.md#6-panneau-de-droite) | Panneau de droite. |
| [7. Navigateur intégré](02-interface.md#7-navigateur-intégré) | Navigateur intégré. |
| [8. Indicateurs d'état](02-interface.md#8-indicateurs-détat) | Indicateurs d'état (« Action requise », contexte). |
| [9. Raccourcis](02-interface.md#9-raccourcis) | Raccourcis. |

## 03 — Les réglages

**Chaque page de Paramètres, ses champs, ses valeurs par défaut et des profils prêts à l'emploi.** [Ouvrir le manuel](03-reglages.md).

| Section | Contenu |
|---|---|
| [1. Accès et organisation](03-reglages.md#1-accès-et-organisation) | Accès et organisation. |
| [2. Général](03-reglages.md#2-général) | Général. |
| [3. Agent](03-reglages.md#3-agent) | Agent : modèle racine, modes shell, sites autorisés, sous-agents. |
| [4. Voix](03-reglages.md#4-voix) | Voix. |
| [5. Facturation et utilisation](03-reglages.md#5-facturation-et-utilisation) | Facturation et utilisation. |
| [6. Apparence](03-reglages.md#6-apparence) | Apparence. |
| [7. Sessions](03-reglages.md#7-sessions) | Sessions. |
| [8. Intégrations : MCP et Compétences](03-reglages.md#8-intégrations--mcp-et-compétences) | Intégrations : MCP et compétences. |
| [9. Appareils : LM Link](03-reglages.md#9-appareils--lm-link) | Appareils : LM Link. |
| [10. Modèles locaux](03-reglages.md#10-modèles-locaux) | Modèles locaux : instances, API, AutoFit, moteur. |
| [11. Tableau récapitulatif des valeurs par défaut](03-reglages.md#11-tableau-récapitulatif-des-valeurs-par-défaut) | Tableau récapitulatif des valeurs par défaut et profils. |

## 04 — Modèles

**Choisir, télécharger et régler un modèle pour l'agent ; mémoire AutoFit ; comparaison mesurée.** [Ouvrir le manuel](04-modeles.md).

| Section | Contenu |
|---|---|
| [1. Critères de choix pour un agent](04-modeles.md#1-critères-de-choix-pour-un-agent) | Critères de choix pour un agent. |
| [2. Le sélecteur de modèle](04-modeles.md#2-le-sélecteur-de-modèle) | Sélecteur de modèle. |
| [3. Télécharger un modèle](04-modeles.md#3-télécharger-un-modèle) | Télécharger un modèle. |
| [4. Effort de raisonnement](04-modeles.md#4-effort-de-raisonnement) | Effort de raisonnement. |
| [5. Mémoire, chargement et déchargement](04-modeles.md#5-mémoire-chargement-et-déchargement) | Mémoire, chargement et déchargement ; effet du minimum AutoFit. |
| [6. Comparaison mesurée](04-modeles.md#6-comparaison-mesurée) | Comparaison mesurée des tâches sur deux postes. |
| [7. Partage avec LM Studio](04-modeles.md#7-partage-avec-lm-studio) | Partage avec LM Studio. |

## 05 — Projets et sessions

**Organiser le travail : projets, dossier de travail, sessions, parallélisme, branches.** [Ouvrir le manuel](05-projets-et-sessions.md).

| Section | Contenu |
|---|---|
| [1. Principe](05-projets-et-sessions.md#1-principe) | Principe : projet, session, conversation. |
| [2. Créer un projet](05-projets-et-sessions.md#2-créer-un-projet) | Créer un projet. |
| [3. Dossier de travail ou fichiers du projet](05-projets-et-sessions.md#3-dossier-de-travail-ou-fichiers-du-projet) | Dossier de travail ou fichiers du projet. |
| [4. Créer et gérer des sessions](05-projets-et-sessions.md#4-créer-et-gérer-des-sessions) | Créer et gérer des sessions. |
| [5. Sessions hors projet](05-projets-et-sessions.md#5-sessions-hors-projet) | Sessions hors projet. |
| [6. Travail en parallèle](05-projets-et-sessions.md#6-travail-en-parallèle) | Travail en parallèle (mesures de sessions simultanées). |
| [7. Reprendre, modifier, ramifier](05-projets-et-sessions.md#7-reprendre-modifier-ramifier) | Reprendre, modifier, ramifier. |
| [8. Bonnes pratiques d'organisation](05-projets-et-sessions.md#8-bonnes-pratiques-dorganisation) | Bonnes pratiques d'organisation. |

## 06 — Documents et fichiers

**Faire travailler l'agent sur des textes et des images : mémo, extraction de facture, contrôle du résultat.** [Ouvrir le manuel](06-documents.md).

| Section | Contenu |
|---|---|
| [1. Principe](06-documents.md#1-principe) | Principe. |
| [2. Ajouter des fichiers](06-documents.md#2-ajouter-des-fichiers) | Ajouter des fichiers. |
| [3. Fichiers du projet](06-documents.md#3-fichiers-du-projet) | Fichiers du projet. |
| [4. Fichiers externes](06-documents.md#4-fichiers-externes) | Fichiers externes. |
| [5. Exemple 1 : rédiger un mémo](06-documents.md#5-exemple-1--rédiger-un-mémo) | Exemple : rédiger un mémo. |
| [6. Exemple 2 : extraire les données d'une facture](06-documents.md#6-exemple-2--extraire-les-données-dune-facture) | Exemple : extraire les données d'une facture. |
| [7. Formats pris en charge](06-documents.md#7-formats-pris-en-charge) | Formats pris en charge. |
| [8. Rédiger une bonne consigne documentaire](06-documents.md#8-rédiger-une-bonne-consigne-documentaire) | Rédiger une bonne consigne documentaire. |
| [9. Fiabilité et contrôle](06-documents.md#9-fiabilité-et-contrôle) | Fiabilité et contrôle. |

## 07 — Code, shell et autorisations

**Confier une tâche de code : modes shell, scénario de correction de bogue, relecture, sécurité.** [Ouvrir le manuel](07-code-et-shell.md).

| Section | Contenu |
|---|---|
| [1. Principe](07-code-et-shell.md#1-principe) | Principe. |
| [2. Mise en place](07-code-et-shell.md#2-mise-en-place) | Mise en place. |
| [3. Modes shell](07-code-et-shell.md#3-modes-shell) | Modes shell, y compris « Désactivé » et « Tout autoriser ». |
| [4. Scénario exécuté : corriger un bogue](07-code-et-shell.md#4-scénario-exécuté--corriger-un-bogue) | Scénario exécuté : corriger un bogue (deux postes, deux modèles). |
| [5. Relire les modifications](07-code-et-shell.md#5-relire-les-modifications) | Relire les modifications. |
| [6. Rédiger une bonne consigne de code](07-code-et-shell.md#6-rédiger-une-bonne-consigne-de-code) | Rédiger une bonne consigne de code. |
| [7. Limites constatées et parades](07-code-et-shell.md#7-limites-constatées-et-parades) | Limites constatées et parades. |
| [8. Sécurité : check-list](07-code-et-shell.md#8-sécurité--check-list) | Check-list de sécurité. |

## 08 — Compétences, palette `@` et MCP

**Étendre l'agent : compétences réutilisables, références `@`, serveurs MCP (essai réel).** [Ouvrir le manuel](08-competences-et-mcp.md).

| Section | Contenu |
|---|---|
| [1. Compétences : principe](08-competences-et-mcp.md#1-compétences--principe) | Compétences : principe. |
| [2. Gérer les compétences](08-competences-et-mcp.md#2-gérer-les-compétences) | Gérer les compétences. |
| [3. La palette `@`](08-competences-et-mcp.md#3-la-palette-) | Palette `@`. |
| [4. Écrire une compétence](08-competences-et-mcp.md#4-écrire-une-compétence) | Écrire une compétence. |
| [5. Serveurs MCP](08-competences-et-mcp.md#5-serveurs-mcp) | Serveurs MCP : ajout, appels, absence de confirmation. |
| [6. Sécurité](08-competences-et-mcp.md#6-sécurité) | Sécurité. |

## 09 — Saisie vocale

**Dictée locale (non exécutée) : principe, mise en route, confidentialité.** [Ouvrir le manuel](09-voix.md).

| Section | Contenu |
|---|---|
| [1. Principe](09-voix.md#1-principe) | Principe. |
| [2. Mise en route](09-voix.md#2-mise-en-route) | Mise en route. |
| [3. Réglage : chargement automatique du modèle](09-voix.md#3-réglage--chargement-automatique-du-modèle) | Chargement automatique du modèle vocal. |
| [4. Confidentialité](09-voix.md#4-confidentialité) | Confidentialité. |
| [5. Dépannage](09-voix.md#5-dépannage) | Dépannage. |

## 10 — Sécurité, compte, cloud, API locale

**Où vont les données, ce qui exige un compte, comment réduire les risques.** [Ouvrir le manuel](10-securite-compte-api.md).

| Section | Contenu |
|---|---|
| [1. Cartographie des flux de données](10-securite-compte-api.md#1-cartographie-des-flux-de-données) | Cartographie des flux de données. |
| [2. Mode entièrement local](10-securite-compte-api.md#2-mode-entièrement-local) | Mode entièrement local. |
| [3. Compte, crédits et facturation](10-securite-compte-api.md#3-compte-crédits-et-facturation) | Compte, crédits et facturation. |
| [4. LM Link](10-securite-compte-api.md#4-lm-link) | LM Link. |
| [5. API locale](10-securite-compte-api.md#5-api-locale) | API locale. |
| [6. Navigateur, recherche web, sites autorisés](10-securite-compte-api.md#6-navigateur-recherche-web-sites-autorisés) | Navigateur, recherche web, sites autorisés. |
| [7. Menaces et parades](10-securite-compte-api.md#7-menaces-et-parades) | Menaces et parades. |
| [8. Configurations recommandées](10-securite-compte-api.md#8-configurations-recommandées) | Configurations recommandées. |
| [9. Points non documentés à clarifier](10-securite-compte-api.md#9-points-non-documentés-à-clarifier) | Points non documentés à clarifier. |

## 11 — Recettes et dépannage

**Fiches par cas d'usage et diagnostic par symptôme.** [Ouvrir le manuel](11-recettes-et-depannage.md).

| Section | Contenu |
|---|---|
| [1. Méthode de réglage](11-recettes-et-depannage.md#1-méthode-de-réglage) | Méthode de réglage. |
| [2. Recettes](11-recettes-et-depannage.md#2-recettes) | Recettes. |
| [3. Dépannage par symptôme](11-recettes-et-depannage.md#3-dépannage-par-symptôme) | Dépannage par symptôme. |
| [4. Commandes de contrôle](11-recettes-et-depannage.md#4-commandes-de-contrôle) | Commandes de contrôle. |
| [5. Checklist avant la première tâche](11-recettes-et-depannage.md#5-checklist-avant-la-première-tâche) | Checklist avant la première tâche. |

## 12 — Auto Review

**Comment la vérification automatique décide d'exécuter une commande ; essais destructifs et incident.** [Ouvrir le manuel](12-auto-review.md).

| Section | Contenu |
|---|---|
| [1. Principe](12-auto-review.md#1-principe) | Principe. |
| [2. Observer les décisions : le journal des sessions](12-auto-review.md#2-observer-les-décisions--le-journal-des-sessions) | Observer les décisions dans le journal des sessions. |
| [3. Étage 1 : Shell Judge](12-auto-review.md#3-étage-1--shell-judge) | Étage 1 : Shell Judge (analyseur déterministe). |
| [4. Étage 2 : Shell Reviewer](12-auto-review.md#4-étage-2--shell-reviewer) | Étage 2 : Shell Reviewer (sous-agent modèle). |
| [5. Niveaux de risque et décision](12-auto-review.md#5-niveaux-de-risque-et-décision) | Niveaux de risque, décision et essais sur commandes destructives. |
| [6. Instructions personnalisées](12-auto-review.md#6-instructions-personnalisées) | Instructions personnalisées. |
| [7. Ce que l'Auto Review ne couvre pas](12-auto-review.md#7-ce-que-lauto-review-ne-couvre-pas) | Ce que l'Auto Review ne couvre pas (fichiers, MCP, isolation). |
| [8. Check-list et dépannage](12-auto-review.md#8-check-list-et-dépannage) | Check-list et dépannage. |

## 13 — Compétences en pratique

**Une compétence de bout en bout : écrire, installer, déclencher, mesurer, faire créer par l'agent.** [Ouvrir le manuel](13-competences-en-pratique.md).

| Section | Contenu |
|---|---|
| [1. Principe](13-competences-en-pratique.md#1-principe) | Principe. |
| [2. Anatomie d'une compétence](13-competences-en-pratique.md#2-anatomie-dune-compétence) | Anatomie d'une compétence. |
| [3. Essai A : une compétence de projet](13-competences-en-pratique.md#3-essai-a--une-compétence-de-projet) | Essai A : compétence de projet (avec et sans `@`). |
| [4. Essai B : installer une compétence globale](13-competences-en-pratique.md#4-essai-b--installer-une-compétence-globale) | Essai B : installer une compétence globale. |
| [5. Faire créer une compétence par l'agent](13-competences-en-pratique.md#5-faire-créer-une-compétence-par-lagent) | Faire créer une compétence par l'agent. |
| [6. Gérer et retirer les compétences](13-competences-en-pratique.md#6-gérer-et-retirer-les-compétences) | Gérer et retirer les compétences. |
| [7. Bonnes pratiques et sécurité](13-competences-en-pratique.md#7-bonnes-pratiques-et-sécurité) | Bonnes pratiques et sécurité. |
| [8. Dépannage](13-competences-en-pratique.md#8-dépannage) | Dépannage. |

## 14 — Commandes `/`, compaction, navigateur et fonctions annexes

**Menu des commandes, compaction mesurée, navigateur intégré, Code Review, branches, recherche.** [Ouvrir le manuel](14-commandes-compaction-navigateur.md).

| Section | Contenu |
|---|---|
| [1. Les commandes `/`](14-commandes-compaction-navigateur.md#1-les-commandes-) | Commandes `/`. |
| [2. Compacter une session : `/compact`](14-commandes-compaction-navigateur.md#2-compacter-une-session--compact) | Compacter une session (`/compact`). |
| [3. Retour arrière et branche](14-commandes-compaction-navigateur.md#3-retour-arrière-et-branche) | Retour arrière et branche. |
| [4. Le navigateur intégré](14-commandes-compaction-navigateur.md#4-le-navigateur-intégré) | Navigateur intégré. |
| [5. Fonctions essayées sur le poste à GPU dédié](14-commandes-compaction-navigateur.md#5-fonctions-essayées-sur-le-poste-à-gpu-dédié) | Fonctions essayées : Code Review, compaction automatique, Ctrl + P, référence de session, renommage, sous-agent, Canvas. |
| [6. Ce qui n'a pas pu être reproduit](14-commandes-compaction-navigateur.md#6-ce-qui-na-pas-pu-être-reproduit) | Ce qui n'a pas pu être reproduit. |
| [7. Dépannage](14-commandes-compaction-navigateur.md#7-dépannage) | Dépannage. |

---

## Par où commencer

- **Découverte** : 00 → 01 → 02 → 05 → 06.
- **Développeur** : 00 → 05 → 07 → 12 → 04 → 08 → 13.
- **Sécurité et conformité** : 00 (section 6) → 10 → 12 → 08 (section 5, MCP) → 07 (section 8).
- **Exploitation d'un poste (mémoire, vitesse)** : 01 → 03 (section 10) → 04 → 05 (section 6) → 11.
- **Fonctions annexes** : 14 (Code Review, compaction, navigateur).
