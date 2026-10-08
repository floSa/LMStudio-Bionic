# Manuel Bionic 11 — Recettes par cas d'usage et dépannage

> **Objet** : fiches de configuration prêtes à l'emploi par cas d'usage, méthode de réglage, et diagnostic par symptôme.
> **Prérequis** : [Manuels Bionic 03, 05, 07](README.md).
> **Version décrite** : Bionic 1.1.7, Windows 11.
> **Statut des informations** : [Vérifié] observé sur le poste de test ; [Estimation] ; [À tester].

---

## Sommaire

1. [Méthode de réglage](#1-méthode-de-réglage)
2. [Recettes](#2-recettes)
3. [Dépannage par symptôme](#3-dépannage-par-symptôme)
4. [Commandes de contrôle](#4-commandes-de-contrôle)
5. [Checklist avant la première tâche](#5-checklist-avant-la-première-tâche)

---

## 1. Méthode de réglage

Ordre conseillé pour qu'un agent local donne un résultat exploitable :

| Étape | Action | Critère de réussite |
|---|---|---|
| 1 | **Choisir le modèle** : capacité outils, taille adaptée à la RAM ([Manuel 04](04-modeles.md)) | Le modèle se charge ; le sélecteur affiche l'effort de raisonnement |
| 2 | **Cadrer le projet** : dossier de travail ou fichiers du projet ([Manuel 05](05-projets-et-sessions.md)) | L'agent retrouve les fichiers au premier essai |
| 3 | **Fixer le mode shell** : *Demander à chaque fois* pour une première utilisation | Chaque commande est lisible et confirmée |
| 4 | **Tester sur une tâche courte** (un fichier, une action) | Résultat correct, durée mesurée |
| 5 | **Élargir** : plus de fichiers, tâche plus longue, mode *Vérification automatique* | Pas de dérive (chemins, langue, outils) |
| 6 | **Capitaliser** : consigne type, compétence, modèle racine ([Manuel 08](08-competences-et-mcp.md)) | Résultats reproductibles |

**Principe** : changer **un seul paramètre à la fois** (modèle, effort de raisonnement, mode shell, consigne), noter la durée et la qualité.

---

## 2. Recettes

### Recette A — Rédiger un document court à partir d'instructions

| Paramètre | Valeur |
|---|---|
| Modèle | Local, ≥ 4 Md de paramètres (*Gemma 4 E4B* suffit) |
| Projet | Sans répertoire de travail ; livrable dans *Fichiers du projet* |
| Mode shell | **Désactivé** (aucune commande utile) |
| Raisonnement | Désactivé pour la rapidité ; activé pour un contenu argumenté |
| Consigne type | « Rédige un mémo de 6 lignes maximum sur [sujet] et enregistre-le dans [nom].md. » |

> **Résultat mesuré** — mémo de 7 lignes enregistré en **2 min 4 s** avec *Gemma 4 E4B* (GPU intégré) ; fichier créé dans *Fichiers du projet* (`+7 −0`). **GPU dédié (RTX 4060 Ti)** : **29 s** (raisonnement activé), **≈ 15 s** (désactivé).

### Recette B — Corriger un bogue dans un dépôt

| Paramètre | Valeur |
|---|---|
| Modèle | Local de 12 Md ou plus recommandé ; 4 Md acceptable pour un bogue simple et cadré |
| Projet | **Répertoire de travail** = racine du dépôt |
| Mode shell | **Demander à chaque fois** (puis *Vérification automatique*) |
| Consigne type | « Dans [fichier], [symptôme]. Corrige sans modifier les tests et vérifie avec [commande de test]. » |
| Contrôles | Diff en ligne, `git diff`, exécution indépendante des tests |

> **Résultat mesuré** — bogue de formule corrigé en **6 min 22 s** avec *Gemma 4 E4B* ; deux obstacles rencontrés (dossier connecté, `pytest` absent) : voir [Manuel 07](07-code-et-shell.md#7-limites-constatées-et-parades).

### Recette C — Explorer et expliquer une base de code

| Paramètre | Valeur |
|---|---|
| Modèle | Local, contexte élevé |
| Mode shell | **Désactivé** ou *Demander à chaque fois* (lecture seule suffisante) |
| Agents d'exploration | **Activés** (Réglages → Agent) |
| Consigne type | « Explique l'architecture de ce dépôt : points d'entrée, modules, flux de données. Ne modifie aucun fichier. » |

### Recette D — Exploiter des documents joints (images, PDF)

| Paramètre | Valeur |
|---|---|
| Modèle | Modèle avec **vision**, ou **sous-agent de vision** (Réglages → Agent) |
| Fichiers | Ajouter dans *Fichiers du projet* |
| Consigne type | « Extrais du fichier [nom] [champs], et enregistre le résultat dans [nom].json. » |
| Contrôle | Comparer chaque valeur au document source |

Voir [Manuel 06](06-documents.md).

### Recette E — Travail strictement confidentiel

| Paramètre | Valeur |
|---|---|
| Modèle | **Local** uniquement |
| Compte | Non connecté |
| Recherche web | Désactivée ; liste de sites vide |
| API locale | Journaux **masqués** ; CORS désactivé |
| Mode shell | *Demander à chaque fois* |

Voir [Manuel 10](10-securite-compte-api.md#8-configurations-recommandées).

### Recette F — Intégrer le modèle à un script

| Paramètre | Valeur |
|---|---|
| Application | Bionic **ouvert** (serveur sur `127.0.0.1:1234`) |
| Modèle | Identifiant de `GET /v1/models` ; chargement à la demande activé |
| Appel | `POST /v1/chat/completions` ([Manuel 10](10-securite-compte-api.md#5-api-locale)) |
| Exemples | [`exemples/`](../../exemples/) |

---

## 3. Dépannage par symptôme

| Symptôme | Cause probable | Action |
|---|---|---|
| Écran **« Bionic cannot start »** | LM Studio est ouvert | **Quit LM Studio and continue** ([Manuel 01](01-presentation-installation.md#5-conflit-avec-lm-studio)). |
| Bouton d'envoi **inactif** | Aucun modèle sélectionné | Choisir un modèle (« Choisir un modèle ») ; définir un *Modèle racine*. |
| Liste de modèles vide | Aucun modèle téléchargé | Réglages → **Explorer** → télécharger ([Manuel 04](04-modeles.md)). |
| L'agent « ne trouve pas » le dossier | Dossier **connecté** au lieu d'un dossier de travail | Créer le projet avec un **répertoire de travail** ([Manuel 05](05-projets-et-sessions.md#3-dossier-de-travail-ou-fichiers-du-projet)). |
| Session bloquée avec pastille **Action requise** | Commande en attente de confirmation | Ouvrir la session ; **Yes**, **Non…** ou **Annuler**. |
| L'agent propose un outil absent (`pytest`) | Hypothèse du modèle | Citer la commande exacte dans la consigne ; refuser avec instruction. |
| Chemin de dossier incorrect dans une commande | Petit modèle | Refuser (**Non, demander autre chose**), préciser le chemin. |
| Réponses en anglais | Modèle peu stable en français | Consigne « Répondre en français » ; modèle plus grand. |
| Tâche très lente | Modèle local sur GPU intégré (sur GPU dédié, une tâche courte dure 15 à 60 s) ; trop d'étapes | Réduire la tâche ; modèle plus petit ou plus rapide ; désactiver le raisonnement. |
| **Contexte** élevé, réponses dégradées | Session trop longue | Nouvelle session ; consigne de reprise concise. |
| Modèle qui ne se charge pas | Mémoire insuffisante ; protection de chargement | Réglages → **Paramètres par défaut des modèles locaux** : assouplir la protection ou réduire le contexte minimal ; modèle plus petit. |
| RAM libre quasi nulle après le chargement d'un modèle | Contexte chargé très grand (ex. 262 144 tokens : 14 Go occupés pour un modèle de 7 Go, mesuré) | Décharger le modèle (Réglages → Instances chargées) ; fermer des applications ; charger le modèle avec un contexte réduit dans LM Studio ([Manuel 04](04-modeles.md#5-mémoire-chargement-et-déchargement)). |
| Système lent pendant l'exécution | Mémoire saturée (modèle + modèle vocal + autres applications) | Décharger les modèles (Instances chargées) ; fermer des applications. |
| `curl` sur `127.0.0.1:1234` sans réponse | Bionic fermé, ou autre application sur le port | `Get-NetTCPConnection -LocalPort 1234 -State Listen` ([section 4](#4-commandes-de-contrôle)). |
| Recherche web inutilisable | Non connecté | Connexion au compte requise ([Manuel 10](10-securite-compte-api.md)). |
| Compétences de Claude Code absentes | Option d'import désactivée | Réglages → Compétences → activer **Claude Code** ([Manuel 08](08-competences-et-mcp.md#2-gérer-les-compétences)). |
| Le navigateur intégré refuse un site | Site non autorisé | Réglages → Agent → **Sites web autorisés** ([Manuel 03](03-reglages.md#3-agent)). |
| Dictée sans effet | Modèle vocal non prêt ; micro non autorisé | [Manuel 09](09-voix.md#5-dépannage). |
| Version qui change sans action | Mises à jour automatiques | Réglages → Général ([Manuel 01](01-presentation-installation.md#7-mises-à-jour)). |

---

## 4. Commandes de contrôle

| Besoin | Commande (PowerShell) |
|---|---|
| Qui écoute sur le port 1234 | `Get-NetTCPConnection -LocalPort 1234 -State Listen \| Select-Object LocalAddress, OwningProcess` |
| Nom du processus | `(Get-Process -Id (Get-NetTCPConnection -LocalPort 1234 -State Listen).OwningProcess).ProcessName` |
| Modèles servis | `curl.exe http://127.0.0.1:1234/v1/models` |
| Taille des modèles | `Get-ChildItem $env:USERPROFILE\.lmstudio\models -Recurse -Filter *.gguf \| Select-Object Name, @{n='Go';e={[math]::Round($_.Length/1GB,2)}}` |
| Journaux du serveur | `Get-ChildItem $env:USERPROFILE\.lmstudio\apps\bionic\server-logs` |
| Mémoire disponible | `Get-CimInstance Win32_OperatingSystem \| Select-Object @{n='LibreGo';e={[math]::Round($_.FreePhysicalMemory/1MB,1)}}` |
| État Git avant une tâche | `git status --short` ; après : `git diff` |

---

## 5. Checklist avant la première tâche

- [ ] Une seule des deux applications (LM Studio ou Bionic) est ouverte.
- [ ] Modèle sélectionné et chargé ; effort de raisonnement choisi.
- [ ] Projet créé avec le bon **répertoire de travail** (code) ou *Fichiers du projet* (documents).
- [ ] Mode shell adapté (par défaut : *Vérification automatique* ; première fois : *Demander à chaque fois*).
- [ ] Dépôt Git propre ; aucun secret dans le dossier de travail.
- [ ] Consigne : lieu, objectif, vérification, contraintes.
- [ ] Compteur de **contexte** surveillé pendant la tâche.
- [ ] Diff relu et tests exécutés avant de conserver les modifications.
