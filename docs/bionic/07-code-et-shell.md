# Manuel Bionic 07 — Code, shell et autorisations

> **Objet** : confier une tâche de code à Bionic (comprendre, corriger, tester), maîtriser les autorisations de commandes, relire les modifications et limiter les risques.
> **Prérequis** : [Manuel Bionic 00](00-notions-agent.md), [05](05-projets-et-sessions.md).
> **Version décrite** : Bionic 1.1.7, Windows 11, interface en français.
> **Statut des informations** : [Vérifié] observé sur le poste de test (scénario exécuté de bout en bout) ; [Source] documentation officielle ; [Estimation] ; [À tester].

---

## Sommaire

1. [Principe](#1-principe)
2. [Mise en place](#2-mise-en-place)
3. [Modes shell](#3-modes-shell)
4. [Scénario exécuté : corriger un bogue](#4-scénario-exécuté--corriger-un-bogue)
5. [Relire les modifications](#5-relire-les-modifications)
6. [Rédiger une bonne consigne de code](#6-rédiger-une-bonne-consigne-de-code)
7. [Limites constatées et parades](#7-limites-constatées-et-parades)
8. [Sécurité : check-list](#8-sécurité--check-list)

---

## 1. Principe

### Essentiel

En mode code, l'agent peut dans le **dossier de travail** : chercher dans les fichiers, lire, **modifier**, utiliser **Git** et **exécuter des commandes** (tests, compilation, scripts) [Source]. Il observe les sorties (échec d'un test, message d'erreur) et corrige en conséquence.

Deux garde-fous distincts :

| Garde-fou | Porte sur | Mode par défaut |
|---|---|---|
| **Mode shell** | Les **commandes** exécutées | Vérification automatique |
| **Relecture des diffs** | Les **fichiers modifiés** | Aucune confirmation préalable : relecture **après** coup |

> **Point d'attention** — sur le poste de test, une modification de fichier dans le dossier de travail a été appliquée **directement**, sans demande de confirmation. La protection contre une mauvaise modification repose sur la relecture du diff et sur **Git** (retour arrière).

### Pour aller plus loin

Les **sessions** décident des autorisations : « les autorisations d'exécution de code se règlent désormais par session » (boîte de création de projet). Une session sans mode shell défini utilise le mode par défaut ; chaque session peut ensuite recevoir un mode différent.

---

## 2. Mise en place

1. Créer un projet avec un **répertoire de travail** = racine du dépôt ([Manuel 05](05-projets-et-sessions.md#3-dossier-de-travail-ou-fichiers-du-projet)).
2. Choisir un modèle **capable d'outils** et de taille suffisante ([Manuel 04](04-modeles.md)).
3. Vérifier le **mode shell** (bouton à gauche du sélecteur de modèle).
4. Pour un dépôt Git : valider un état propre (`git status` vide) avant de lancer la tâche, afin que `git diff` ne montre que le travail de l'agent.

> **Exemple (poste de test)** — projet fictif `bionic-demo` : `tarifs.py` (fonctions `total_ttc` et `remise`), `test_tarifs.py` (tests `unittest`), `README.md`. Un bogue volontaire : `total_ttc` renvoyait `prix_ht * taux_tva` (la seule TVA) au lieu de `prix_ht * (1 + taux_tva)` (TTC).

---

## 3. Modes shell

![Menu des modes shell](../img/bionic/03-interface/04-modes-shell.png)
*Figure 1 — Menu « Choisissez comment Bionic obtient l'autorisation d'exécuter des commandes ».*

| Mode (libellé de l'application) | Description affichée | Comportement |
|---|---|---|
| **Désactivé** | « Ne pas autoriser les commandes shell » | Aucune commande. L'agent ne peut pas lancer de tests. |
| **Demander à chaque fois** | « Vérifier chaque commande avant son exécution » | Confirmation manuelle de chaque commande. Icône : main. |
| **Vérification automatique** *(défaut, recommandé)* | « L'agent vérifie les commandes pour vous » | Les commandes reconnues comme sûres sont approuvées automatiquement ; les autres sont confiées à un **agent de vérification distinct**. |
| **Tout autoriser** | « Autoriser l'agent à exécuter n'importe quelle commande » | Aucune vérification. |

### Première utilisation

À la première demande d'exécution, Bionic affiche une boîte d'information :

![Première autorisation du shell](../img/bionic/07-code/02-autorisation-shell-premiere-fois.png)
*Figure 2 — « Votre agent souhaite exécuter des commandes shell. »*

| N° | Choix | Effet |
|---|---|---|
| ① | **Vérification automatique (recommandée)** | Approbation automatique des commandes sûres ; vérification des autres par un agent distinct. |
| ② | **Vérification manuelle** | Confirmation de chaque commande. |
| ③ | **Non** | Aucune commande shell. |

Le texte précise qu'« un agent malveillant en abuse, il peut endommager l'ordinateur » : le choix est un arbitrage entre **confort** et **maîtrise**.

### Pour aller plus loin

- La zone **Réglages → Agent → Vérification automatique des commandes** permet d'ajouter des **instructions personnalisées** au vérificateur ([Manuel 03](03-reglages.md#3-agent)).
- Le journal des modifications mentionne des préférences d'approbation **persistantes** et moins d'invites pour certaines commandes en lecture seule. Le fonctionnement de la vérification automatique (analyseur déterministe, sous-agent vérificateur, niveaux de risque, instructions personnalisées) est détaillé et testé au [Manuel Bionic 12](12-auto-review.md).
- **Tout autoriser** : réservé aux environnements jetables (machine virtuelle, conteneur, copie de travail sans secrets).

---

## 4. Scénario exécuté : corriger un bogue

### Consigne

> « Exécute les tests, trouve la cause de l'échec dans tarifs.py, corrige-la puis relance les tests. »

Mode shell : **Demander à chaque fois**. Modèle : *Gemma 4 E4B* (local, ≈ 4 Md de paramètres, GPU intégré).

### Déroulé observé

| Étape | Ce qui s'affiche | Action requise |
|---|---|---|
| 1 | L'agent propose d'exécuter `pytest` | Confirmation demandée |
| 2 | Boîte **Confirm shell command** + pastille **Action requise** dans la barre latérale | Choisir **Yes**, **Non…** ou **Annuler** |
| 3 | `pytest` n'est pas installé : refus avec instruction (« Utilise python -m unittest … ») | Saisie d'une consigne + **Submit** |
| 4 | L'agent lit `tarifs.py`, remplace la ligne fautive | Aucune (modification directe) |
| 5 | Réponse : correction appliquée, bloc **Fichiers modifiés** `tarifs.py  +1 −1` | Relecture du diff |
| 6 | Durée affichée : **6 min 22 s** | — |

![Boîte de confirmation](../img/bionic/07-code/04-commande-refusable.png)
*Figure 3 — « Confirm shell command » : ① dossier d'exécution, ② commande, ③ Yes, ④ refus avec instruction, ⑤ Annuler.*

| N° | Élément | Rôle |
|---|---|---|
| ① | **Working directory** | Dossier dans lequel la commande s'exécute : **à contrôler à chaque fois**. |
| ② | **Do you want to run …?** | Commande exacte proposée. |
| ③ | **Yes** | Exécute la commande. |
| ④ | **Non, demander autre chose à l'agent** | Refuse et donne une instruction libre. |
| ⑤ | **Annuler** | Abandonne la commande. |

Refus avec instruction :

![Refus avec instruction](../img/bionic/07-code/05-refus-avec-instruction.png)
*Figure 4 — ① champ d'instruction, ② Submit.*

> **Observation** — le dossier d'exécution proposé était `C:\Users\<utilisateur>\bionic-demo\Working directory` : le modèle avait **ajouté** un segment inexistant au chemin. Ce type d'erreur est fréquent avec un petit modèle et justifie le mode **Demander à chaque fois** pendant la phase de découverte.

### Résultat

![Résultat avec diff](../img/bionic/07-code/06-resultat-diff.png)
*Figure 5 — Correction appliquée et diff de `tarifs.py`.*

Vérification indépendante (hors Bionic) :

```powershell
cd C:\Users\<utilisateur>\bionic-demo
python -m unittest
```

Les tests passent après la correction [Vérifié].

### Même tâche avec un modèle plus grand

Après remise en place du bogue (dépôt Git initialisé, état initial validé) et consigne précisant la commande de test (« exécute les tests avec `python -m unittest` … Réponds en français »), la tâche a été rejouée avec *Gemma 4 12B QAT*, raisonnement **Activé**, mode **Demander à chaque fois**.

| | *Gemma 4 E4B* (≈ 4 Md) | *Gemma 4 12B QAT* (≈ 12 Md) |
|---|---|---|
| Durée affichée | 6 min 22 s | **4 min 50 s** (chargement du modèle inclus) |
| Confirmations demandées | plusieurs, dont `pytest` (absent) | **2**, toutes deux `python -m unittest test_tarifs.py` |
| Dossier d'exécution | segment erroné ajouté au chemin | **`C:\Users\<utilisateur>\bionic-demo`** (correct) |
| Langue de la réponse | mélange français / anglais | **Français** |
| Diff | `+1 −1` | **`+1 −1`**, ligne exacte |
| Tests après correction | passent | **passent** (contrôle indépendant) |

![Confirmation avec le modèle de 12 Md](../img/bionic/07-code/08-confirmation-12b.png)
*Figure 6 — Confirmation de `python -m unittest test_tarifs.py` : dossier d'exécution correct.*

![Résultat avec le modèle de 12 Md](../img/bionic/07-code/09-resultat-12b.png)
*Figure 7 — Réponse en quatre étapes (exécution, identification, correction, vérification), bloc « Fichiers modifiés » `tarifs.py +1 −1`, pied de zone de saisie « Démo code • master » (dépôt Git détecté).*

Diff relevé par `git diff` (dépôt de démonstration) :

```diff
-    return prix_ht * taux_tva  # BUG volontaire : devrait être prix_ht * (1 + taux_tva)
+    return prix_ht * (1 + taux_tva)
```

> **Lecture** — le gain porte moins sur la vitesse que sur la **fiabilité** : chemins corrects, outil de test adapté, résumé exact. Le nombre réduit de confirmations (2) allège aussi la charge de relecture. Un seul essai par modèle a été réalisé : ces résultats illustrent une tendance, ils ne constituent pas une statistique.

**Indicateur Git** : dans un projet dont le dossier de travail est un dépôt Git, le pied de la zone de saisie affiche **« projet • branche »** (ici « Démo code • master ») et le panneau de droite ajoute une icône de branche à côté du dossier [Vérifié].

---

## 5. Relire les modifications

| Source de relecture | Où | Utilité |
|---|---|---|
| **Diff en ligne** | Bloc *Fichiers modifiés* de la réponse | Voir précisément ce qui change ([Manuel 02](02-interface.md#4-fil-de-la-session)). |
| **Visionneuse de fichier** | Clic sur le fichier du panneau de droite | Lire le fichier complet, numéros de ligne. |
| **`git diff`** | Terminal | Vue indépendante de l'application. |
| **Tests** | Terminal ou demande à l'agent | Vérifier le comportement. |
| **Commande exécutée** | Ligne « Exécuter … » du travail déplié | Contrôler ce qui a réellement été lancé. |

Règle pratique : **ne jamais conserver une modification sans avoir lu son diff et exécuté les tests** [Source : « Review Bionic's diffs and command output before keeping the changes »].

---

## 6. Rédiger une bonne consigne de code

### Essentiel

Une consigne efficace précise : **où** (dossier, fichier), **quoi** (comportement attendu), **comment vérifier** (commande de test), **contraintes** (ne pas modifier tel fichier).

| Faible | Efficace |
|---|---|
| « Corrige le bogue. » | « Dans `tarifs.py`, `total_ttc` renvoie la TVA seule au lieu du prix TTC. Corrige la fonction sans toucher aux tests et vérifie avec `python -m unittest`. » |
| « Améliore le code. » | « Ajoute une fonction `remise_plafonnee` dans `tarifs.py` avec un plafond de 50 % et un test dans `test_tarifs.py`. » |

### Pour aller plus loin

Procédure **inspecter → confirmer → modifier → tester → relire** [Source] :

1. Demander d'**expliquer** le code concerné (aucune modification).
2. **Valider** le plan et les contraintes.
3. Laisser l'agent **modifier**.
4. Demander des **tests ciblés**.
5. **Relire** les diffs (et `git diff`).

Pour un grand chantier, demander de **découper** l'investigation ; l'agent peut utiliser des sous-sessions en parallèle [Source].

> **Indiquer la commande de test** évite les écarts constatés sur le poste de test : l'agent a proposé `pytest` alors que le projet utilisait `unittest`.

---

## 7. Limites constatées et parades

| Constat (poste de test) | Cause probable | Parade |
|---|---|---|
| Échec de la tâche dans un projet à dossier **connecté** | Les commandes s'exécutaient dans un espace du projet, pas dans le dossier réel | Utiliser un **répertoire de travail** ([Manuel 05](05-projets-et-sessions.md#3-dossier-de-travail-ou-fichiers-du-projet)). |
| Commande proposée avec un chemin erroné | Petit modèle, ambiguïté de chemin | Mode **Demander à chaque fois** ; indiquer le chemin dans la consigne. |
| Outil de test inexistant (`pytest`) | Hypothèse du modèle | Citer la commande exacte dans la consigne. |
| Réponses parfois en anglais | Modèle peu stable en français | Ajouter « Répondre en français » à la consigne [Estimation]. |
| Durée de 6 min 22 s pour un bogue simple | Modèle local sur GPU intégré, plusieurs étapes | Modèle plus puissant ; tâche plus ciblée. |

---

## 8. Sécurité : check-list

- [ ] Dépôt Git propre avant la tâche ; branche dédiée.
- [ ] Dossier de travail limité au projet (pas la racine d'un disque ni le profil utilisateur).
- [ ] Aucun secret (clés, mots de passe) dans le dossier de travail ou les fichiers lisibles.
- [ ] Mode shell adapté : *Demander à chaque fois* pour une première utilisation d'un modèle ou d'un dépôt.
- [ ] Lecture du **dossier d'exécution** et de la **commande** avant chaque **Yes**.
- [ ] Relecture du diff, exécution des tests, `git diff` avant validation.
- [ ] Compétences et serveurs MCP tiers relus avant usage ([Manuel 08](08-competences-et-mcp.md#6-sécurité)).
- [ ] Aucune URL ou contenu externe non fiable collé dans la consigne (risque d'injection d'instructions).
