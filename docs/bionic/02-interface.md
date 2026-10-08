# Manuel Bionic 02 — L'interface

> **Objet** : décrire chaque zone de l'interface de Bionic, les boutons de la zone de saisie, les onglets, le panneau de droite et les indicateurs d'état.
> **Prérequis** : [Manuel Bionic 01](01-presentation-installation.md).
> **Version décrite** : Bionic 1.1.7, Windows 11, interface en français.
> **Statut des informations** : [Vérifié] observé sur le poste de test ; [Source] documentation officielle ; [À tester].

---

## Sommaire

1. [Vue d'ensemble](#1-vue-densemble)
2. [Barre latérale gauche](#2-barre-latérale-gauche)
3. [Barre d'onglets](#3-barre-donglets)
4. [Fil de la session](#4-fil-de-la-session)
5. [Zone de saisie](#5-zone-de-saisie)
6. [Panneau de droite](#6-panneau-de-droite)
7. [Navigateur intégré](#7-navigateur-intégré)
8. [Indicateurs d'état](#8-indicateurs-détat)
9. [Raccourcis](#9-raccourcis)

---

## 1. Vue d'ensemble

![Interface annotée](../img/bionic/03-interface/01-vue-session-annotee.png)
*Figure 1 — Une session de code ouverte.*

| N° | Zone | Rôle | Section |
|---|---|---|---|
| ① | **Barre latérale** | Projets, sessions, conversations hors projet, accès aux réglages | [2](#2-barre-latérale-gauche) |
| ② | **Onglets** | Une session, un fichier ou un navigateur par onglet | [3](#3-barre-donglets) |
| ③ | **Fil de la session** | Consigne, travail de l'agent, réponse, fichiers modifiés | [4](#4-fil-de-la-session) |
| ④ | **Panneau de droite** | Dossier de travail et fichiers du projet | [6](#6-panneau-de-droite) |
| ⑤ | **Zone de saisie** | Consigne à confier à l'agent | [5](#5-zone-de-saisie) |
| ⑥ | **Bouton +** | Ajouter fichiers, dossiers ou compétences | [5](#5-zone-de-saisie) |
| ⑦ | **Mode shell** | Niveau d'autorisation des commandes | [5](#5-zone-de-saisie) |
| ⑧ | **Sélecteur de modèle** | Modèle et effort de raisonnement | [5](#5-zone-de-saisie) |
| ⑨ | **Compteur de contexte** | Tokens utilisés dans la session | [8](#8-indicateurs-détat) |

---

## 2. Barre latérale gauche

### Essentiel

De haut en bas :

| Élément | Fonction |
|---|---|
| Icône de panneau (en haut à gauche) | Masquer / afficher la barre latérale (infobulle **« Masquer la barre latérale »**). |
| Icône de crayon | **Créer une session** (dans le projet courant ou hors projet). |
| **Projets** → **Nouveau projet** | Création d'un projet ([Manuel 05](05-projets-et-sessions.md#2-créer-un-projet)). |
| Nom de projet (ex. *Démo documents*) | Déplie / replie les sessions du projet. Le bouton **+** apparaissant au survol crée une session *dans ce projet*. |
| Session sous un projet | Un clic l'ouvre dans un onglet. Le bouton **…** (« Options de la session ») ouvre le menu de la session. |
| **Conversations** → **Nouvelle conversation** | Sessions **hors projet** (discussion libre, sans dossier de travail). |
| **Paramètres** (en bas) | Ouvre les réglages ([Manuel 03](03-reglages.md)). |

Menu **Options de la session** [Vérifié] :

![Menu de la session](../img/bionic/05-sessions/01-menu-session.png)
*Figure 2 — Menu d'une session.*

| Entrée | Effet |
|---|---|
| **Épingler** | Maintient la session en haut de la liste. |
| **Renommer** | Modifie le titre (généré automatiquement à partir du premier message). |
| **Archiver** | Retire la session de la barre latérale ; elle reste consultable dans Réglages → Sessions. |
| **Ouvrir dans un nouvel onglet** | Ouvre la session dans un onglet distinct. |
| **Déplacer…** | Déplace la session vers un autre projet [Source : déplacements entre projets]. |
| **Supprimer** | Suppression de la session. |

### Pour aller plus loin

- Les **titres de session** sont générés dans la langue du message initial [Source].
- Un projet n'a pas besoin d'être sélectionné pour créer une session : le **projet cible** est rappelé sous la zone de saisie d'un nouvel onglet (sélecteur de projet) [Vérifié].
- La barre latérale peut être **opaque ou translucide** (Réglages → Apparence).

---

## 3. Barre d'onglets

![Accueil d'un nouvel onglet](../img/bionic/03-interface/02-accueil-nouvel-onglet.png)
*Figure 3 — Onglet vide : mascotte, zone de saisie, bouton d'envoi.*

### Essentiel

Chaque **onglet** contient une session. Les onglets sont indépendants : lancer une tâche dans l'un, puis passer à un autre **ne l'interrompt pas** ; l'agent poursuit en arrière-plan [Source, Vérifié].

| Action | Résultat |
|---|---|
| Clic sur **Nouvel onglet** | Onglet vide prêt pour une consigne. |
| Bouton **Close tab** (croix de l'onglet) | Ferme l'onglet (la session est conservée). |
| Ouverture d'un fichier du panneau de droite | Onglet **visionneuse** (aperçu avec numéros de ligne pour le code). |
| **Navigateur** (icône globe) | Onglet navigateur intégré ([section 7](#7-navigateur-intégré)). |
| Glisser un onglet sur la moitié gauche ou droite de la zone | Affichage **côte à côte** [Source]. |

Les libellés des boutons d'onglets sont en partie en **anglais** (« Close tab ») dans cette version.

### Pour aller plus loin

![Visionneuse de fichier](../img/bionic/05-sessions/03-visionneuse-fichier.png)
*Figure 4 — Un fichier ouvert à droite de la session (côte à côte).*

La visionneuse permet de **relire** un fichier avant ou après intervention de l'agent. Les fichiers créés ou modifiés « qui demandent de l'attention » peuvent s'ouvrir dans un éditeur latéral [Source].

---

## 4. Fil de la session

### Essentiel

Le fil se lit de haut en bas :

| Élément | Description |
|---|---|
| **Bulle de consigne** | Le message envoyé. Au survol : **Revenir en arrière et modifier** (reprendre la session à ce point avec un message modifié) et **Copy**. |
| **« Travail effectué en … »** | Ligne repliable résumant la durée du travail. Dépliée, elle montre le raisonnement (« Réflexion terminée »), chaque outil appelé (« 1 outil appelé, 1 fichier modifié ») et les sorties. |
| **Réponse** | Texte final de l'agent, avec blocs de code (bouton **Copy code**). |
| **Fichiers modifiés** | Bloc listant chaque fichier avec **+N** lignes ajoutées (vert) et **−N** supprimées (rouge). Un clic sur la flèche déplie le **diff en ligne**. |
| **Boutons sous la réponse** | **Copy** (copier la réponse) et **Créer une branche** (*fork* : nouvelle session qui part de ce point). |

![Travail déplié](../img/bionic/05-sessions/02-travail-deplie.png)
*Figure 5 — Travail déplié : réflexion, appel d'outil, résultat et fichiers modifiés.*

Lecture d'un **diff en ligne** :

![Diff en ligne](../img/bionic/07-code/06-resultat-diff.png)
*Figure 6 — Diff de `tarifs.py` : ligne supprimée en rouge, ligne ajoutée en vert.*

| Marque | Signification |
|---|---|
| Fond rouge, marge rouge | Ligne **supprimée** (état précédent). |
| Fond vert, marge verte | Ligne **ajoutée** (nouvel état). |
| Numéros | Numéros de ligne du fichier. |

### Pour aller plus loin

- La disposition du diff (**Unifié** ou autre) se règle dans Réglages → Apparence → *Disposition des différences dans la conversation*.
- Le *fork* conserve la session d'origine intacte ; le réglage Réglages → Sessions → *Renommer après la création d'une branche* propose un nouveau nom.
- Les liens `localhost` de la réponse peuvent s'ouvrir dans le navigateur intégré [Source].

---

## 5. Zone de saisie

![Sélecteur de modèle](../img/bionic/03-interface/03-popover-modele.png)
*Figure 7 — Sélecteur de modèle ouvert.*

### Essentiel

De gauche à droite :

| Bouton | Libellé de l'infobulle | Fonction |
|---|---|---|
| **+** | « Ajouter des fichiers, des dossiers ou des compétences » | Joindre du matériau à la session ; appeler une compétence. Détail : [Manuel 06](06-documents.md) et [08](08-competences-et-mcp.md). |
| **Bouclier** / **main** | « Mode shell » | Niveau d'autorisation des commandes : [Manuel 07](07-code-et-shell.md#3-modes-shell). L'icône change selon le mode. |
| **Modèle** | « Modèle » | Ouvre le sélecteur : filtre, liste, effort de raisonnement ([Manuel 04](04-modeles.md)). |
| **Micro** | « Configurer la transcription vocale » | Dictée ([Manuel 09](09-voix.md)). |
| **Flèche** | « Envoyer » | Envoie la consigne. Pendant l'exécution, devient un **carré** (arrêt). |

Icônes du mode shell [Vérifié] :

![Modes du shell](../img/bionic/03-interface/04-modes-shell.png)
*Figure 8 — Menu du mode shell : Désactivé, Demander à chaque fois, Vérification automatique (coché), Tout autoriser.*

Entrée envoie la consigne ; **Maj + Entrée** insère un saut de ligne [Estimation, usage standard : à confirmer].

### Pour aller plus loin

- Pendant qu'une tâche tourne, le champ devient **« Envoyez un autre message »** : un message complémentaire peut être ajouté en cours d'exécution [Vérifié sur le libellé].
- Le sélecteur de modèle montre le **format** (GGUF) et l'état « Activé / Désactivé » du raisonnement pour la session.
- La saisie `@` ouvre la **palette de références** ([Manuel 08](08-competences-et-mcp.md#3-la-palette-)).

---

## 6. Panneau de droite

Le panneau de droite s'ouvre et se ferme par l'icône située tout en haut à droite (« Masquer le panneau de droite »).

| Zone | Contenu |
|---|---|
| **Titre** | Nom du projet (ex. *Démo code*). |
| **Icône globe** | Ouvre / ferme le navigateur intégré (« Fermer le navigateur » quand actif). |
| **Connecter un dossier** | Ajoute un dossier comme **fichiers externes** ([Manuel 06](06-documents.md#4-fichiers-externes)). |
| **Ajouter un fichier** | Copie un fichier dans les **fichiers du projet**. |
| **Fichiers du projet** | Fichiers gérés par le projet (ex. `memo-ia-locale.md`). |
| **Dossier de travail** (ex. `bionic-demo`) | Arborescence réelle ; menu **Options du répertoire de travail** pour le changer ; chaque fichier a son menu **Options de …**. |

![Projet avec dossier de travail](../img/bionic/04-projets/02-projet-avec-repertoire.png)
*Figure 9 — Un projet de code : arborescence du dossier de travail à droite.*

> **Exemple (poste de test)** — après la tâche documentaire, `memo-ia-locale.md` apparaît dans **Fichiers du projet** ; le dossier `bionic-demo` (dossier de travail du second projet) montre `README.md`, `tarifs.py` et `test_tarifs.py`.

---

## 7. Navigateur intégré

![Navigateur intégré](../img/bionic/03-interface/05-navigateur-integre.png)
*Figure 10 — Onglet **Navigateur** ouvert à droite de la session (adresse par défaut : `localhost:3000`).*

### Essentiel

Le navigateur intégré s'ouvre dans un onglet **Navigateur** avec les contrôles **Retour**, **Avancer**, **Recharger**, une barre d'adresse et un menu **Options du navigateur**. Il sert à **voir le résultat** d'un travail web (application en cours de développement) sans quitter Bionic.

### Pour aller plus loin

- Les cookies et données de site se règlent dans Réglages → Agent → *Données du navigateur* (**Mémoire uniquement** par défaut) ; l'accès aux sites **externes** est limité par la liste *Sites web autorisés* (aucun site autorisé par défaut ; `localhost` reste accessible) [Vérifié] : voir [Manuel 03](03-reglages.md#3-agent) et [Manuel 10](10-securite-compte-api.md).
- Le contenu navigué a été testé avec l'agent : l'agent **ouvre** la page mais **ne lit pas** son contenu ([Manuel 14, section 4](14-commandes-compaction-navigateur.md#4-le-navigateur-intégré)) [Vérifié, 7 octobre 2026].

---

## 8. Indicateurs d'état

| Indicateur | Où | Signification |
|---|---|---|
| **Contexte : 9,2 k** | Sous la zone de saisie, à droite | Tokens occupés dans la session (voir [Manuel 00](00-notions-agent.md#7-contexte-et-compaction)). |
| Nom du projet | Sous la zone de saisie, à gauche | Projet de la session ; **« Sans projet »** dans une session hors projet. Si le dossier de travail est un dépôt Git : **« projet • branche »** (ex. « Démo code • master »). |
| **Chargement du modèle : n %** | Début du fil, pendant le démarrage d'une tâche | Le modèle se charge en mémoire (premier message après un changement de modèle). |
| Pastille animée sur la session | Barre latérale | L'agent travaille ; le titre « Session sans nom » est remplacé par un titre généré à la fin. |
| **Travail effectué en …** | Fil | Durée du dernier tour de l'agent. |
| Pastille **Action requise** (violette) | Barre latérale, à côté d'une session | L'agent attend une **confirmation** (commande à valider). |
| Icône sur une session | Barre latérale | L'agent a terminé en arrière-plan [Source]. |
| Notification système | Bureau Windows | Fin de session lorsque la fenêtre n'est pas au premier plan (Réglages → Général → *Notifications de fin de session*). |

![Confirmation de commande](../img/bionic/07-code/07-confirmation-pytest.png)
*Figure 11 — Session en attente : pastille « Action requise » dans la barre latérale et boîte « Confirm shell command ».*

---

## 9. Raccourcis

| Action | Raccourci | Statut |
|---|---|---|
| Fermer l'onglet courant | `Ctrl + W` | [Vérifié] |
| Ouverture rapide (sessions, fichiers, URL) | `Ctrl + P` | [Source : « Cmd + P » sur macOS, adaptation Windows non vérifiée] |
| Arrêter l'agent | Bouton carré de la zone de saisie | [Vérifié] |

> La liste complète des raccourcis n'est pas documentée dans les pages consultées. Vérifiés le 7 octobre 2026 : `Ctrl + ,` (réglages), `Ctrl + P` (recherche de sessions, [Manuel 14, section 5.3](14-commandes-compaction-navigateur.md#53-recherche-ctrl--p)) ; saisie `/` (commandes) et `@` (références). Les autres restent **[À tester]**.
