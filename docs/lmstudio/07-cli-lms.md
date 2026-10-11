# Manuel 07 — La ligne de commande `lms`

> **Objet** : piloter LM Studio sans interface graphique : lister, charger et décharger des modèles, gérer le serveur et les moteurs, converser, automatiser.
> **Prérequis** : [Manuel 01](01-prise-en-main.md). Notions de chargement : [Manuel 03](03-charger-un-modele.md).
> **Version décrite** : `lms` livré avec LM Studio 0.4.25.
> **Statut des commandes** : chaque commande est marquée **[Testée]** (exécutée sur le poste de test, résultat constaté) ou **[Aide]** (décrite d'après `lms <commande> --help`, non exécutée).

---

## Sommaire

1. [Présentation](#1-présentation)
2. [Vue d'ensemble des commandes](#2-vue-densemble-des-commandes)
3. [Modèles : lister, charger, décharger](#3-modèles--lister-charger-décharger)
4. [Serveur local](#4-serveur-local)
5. [Conversation en ligne de commande](#5-conversation-en-ligne-de-commande)
6. [Moteurs d'inférence (runtime)](#6-moteurs-dinférence-runtime)
7. [Télécharger et importer des modèles](#7-télécharger-et-importer-des-modèles)
8. [Journaux](#8-journaux)
9. [Mode sans interface : `llmster`](#9-mode-sans-interface--llmster)
10. [Scripts et automatisation](#10-scripts-et-automatisation)
11. [Dépannage](#11-dépannage)

---

## 1. Présentation

`lms` est un programme en ligne de commande installé avec LM Studio dans `%USERPROFILE%\.lmstudio\bin\lms.exe`. Il dialogue avec le **service LM Studio** (l'application ou le démon `llmster`) : une commande `lms` réveille ce service s'il est arrêté (message « Waking up LM Studio service… »).

Intérêts : scripts reproductibles, déploiement sur serveur, chargement de modèles avec des paramètres précis, diagnostics rapides.

Le programme est accessible depuis n'importe quel terminal si `%USERPROFILE%\.lmstudio\bin` figure dans le `PATH` (cas du poste de test) :

```powershell
Get-Command lms | Select-Object Source
lms --help
```

> **Astuce PowerShell** — Les messages d'information de `lms` sont écrits sur la sortie d'erreur ; PowerShell peut les afficher comme des erreurs sans que la commande ait échoué. Se fier au code de sortie (`$LASTEXITCODE`).

---

## 2. Vue d'ensemble des commandes

| Famille | Commande | Rôle |
|---|---|---|
| **Modèles locaux** | `lms ls` | Lister les modèles présents sur le disque |
| | `lms ps` | Lister les modèles chargés en mémoire |
| | `lms load` | Charger un modèle |
| | `lms unload` | Décharger un modèle |
| | `lms get` | Rechercher et télécharger un modèle |
| | `lms import` | Importer un fichier de modèle existant |
| | `lms chat` | Converser avec un modèle |
| **Serveur** | `lms server start / stop / status` | Gérer le serveur local |
| | `lms log stream` | Suivre les journaux en direct |
| **Moteurs** | `lms runtime ls / select / get / update / remove / survey` | Gérer les moteurs d'inférence |
| **Divers** | `lms status` | État global de LM Studio (« Server: ON (port: 1234) », modèles chargés) **[Testée]** ; absente de `lms --help` |
| | `lms daemon up / down / status / update` | Gérer le démon `llmster` |
| | `lms link …` | Gérer LM Link (`enable`, `disable`, `status`, `set-device-name`, `set-preferred-device` ; [Manuel 17, section 6](17-lm-link.md#10-les-commandes-lms-link)) |
| | `clone`, `push`, `dev`, `login`, `logout`, `whoami` | Publication d'artefacts sur le Hub (bêta, hors périmètre) |

---

## 3. Modèles : lister, charger, décharger

### 3.1 `lms ls` — modèles installés **[Testée]**

```powershell
lms ls
```

Résultat constaté :

```text
You have 2 models, taking up 6.41 GB of disk space.

LLM                               PARAMS    ARCH      SIZE       DEVICE
google/gemma-4-e4b (1 variant)    7.5B      gemma4    6.33 GB    Local     ✓ LOADED

EMBEDDING                               PARAMS    ARCH          SIZE        DEVICE
text-embedding-nomic-embed-text-v1.5              Nomic BERT    84.11 MB    Local     ✓ LOADED
```

| Option | Effet |
|---|---|
| `--llm` / `--embedding` | Restreindre à un type de modèle |
| `--variants` | Afficher les variantes (quantifications) de chaque modèle |
| `--json` | Sortie JSON : clé du modèle, format, quantification, capacités (`vision`, `trainedForToolUse`), contexte maximal… exploitable dans un script |
| `<clé-modèle>` | Afficher les variantes d'un modèle précis |

### 3.2 `lms ps` — modèles chargés **[Testée]**

```powershell
lms ps
```

```text
IDENTIFIER            MODEL                 STATUS    SIZE       CONTEXT    PARALLEL    DEVICE    TTL
google/gemma-4-e4b    google/gemma-4-e4b    IDLE      6.33 GB    8192       4           Local
```

| Colonne | Signification |
|---|---|
| **IDENTIFIER** | Nom à utiliser dans l'API (`"model": "…"`) |
| **STATUS** | `IDLE` (en attente) ou en génération |
| **CONTEXT** / **PARALLEL** | Paramètres de chargement actifs |
| **TTL** | Durée d'inactivité restante avant déchargement automatique (modèles chargés à la demande) |

`--json` produit la même information au format JSON.

### 3.3 `lms load` — charger **[Testée]**

```powershell
lms load google/gemma-4-e4b --gpu max -c 8192 --parallel 1 --identifier gemma -y
```

| Option | Effet |
|---|---|
| `<clé-modèle>` | Modèle à charger (mode interactif si omis) |
| `--gpu <off \| max \| 0-1>` | Part des couches sur GPU : `off` (aucune), `max` (toutes), ou ratio (`0.5` = moitié). Sans option : choix automatique. |
| `-c, --context-length <n>` | Taille de contexte |
| `--parallel <n>` | Prédictions simultanées maximales |
| `--ttl <secondes>` | Déchargement automatique après inactivité |
| `--identifier <nom>` | Identifiant attribué dans l'API |
| `--estimate-only` | **Calcule l'estimation mémoire sans charger** |
| `--speculative-draft-mtp` / `--no-speculative-draft-mtp` | Active ou désactive le décodage spéculatif **MTP** (tête de prédiction multi-jetons **intégrée au fichier** du modèle) **[Testée]** : refusé pour un fichier sans tête MTP (« *requires a GGUF model with a bundled supported MTP head* ») |
| `--speculative-draft-simple` + `--speculative-draft-model <modèle>` | Décodage spéculatif avec un **modèle brouillon séparé** **[Testée]** |
| `--speculative-draft-max-tokens`, `--speculative-draft-min-tokens`, `--speculative-draft-min-continue-probability` | Longueur et seuil des brouillons (exigent l'un des deux modes) |
| `-y, --yes` | Répondre oui aux questions (scripts) |
| `--auto` | Choix automatique du contexte et du placement : réservé à Bionic |

> **Limites constatées sur `lms load`** — (1) Pas d'option pour Flash Attention, la taille des lots, la quantification du cache K/V, le lot physique ni les experts MoE : utiliser l'API `POST /api/v1/models/load` ([Manuel 06](06-serveur-local-et-api.md)) ou le **SDK** ([Manuel 16](16-sdk-et-plugins.md#3-paramètres-de-chargement-accessibles-par-le-sdk)). (2) Une **variante** listée par `lms ls` peut ne pas se charger (« *Model not found* » pour `olmocr-2-7b-1025@q8_0`) alors que le SDK la charge **[Vérifié]**. (3) Avec `--gpu max` sur un modèle plus gros que la VRAM, la carte déborde en mémoire partagée : **moins rapide** que l'automatique ([Manuel 15, section 6.1](15-performances-gpu-dedie.md#61-offload-partiel-modèle-moe-gemma-4-26b-a4b-q4_k_m-1799-go-contexte-8-192)).

**Estimation sans chargement** **[Testée]** :

```powershell
lms load google/gemma-4-e4b -c 32768 --estimate-only -y
```

```text
Model: google/gemma-4-e4b
Context Length: 32 768
Estimated GPU Memory:   7.85 GiB
Estimated Total Memory: 7.85 GiB

Estimate: This model may be loaded based on your resource guardrails settings.
```

Cette commande permet de **dimensionner une machine avant déploiement** (voir [Manuel 03](03-charger-un-modele.md#2-composition-de-la-mémoire)). Les valeurs sont en **GiB**. Sur un poste à GPU dédié, la sortie comporte une ligne supplémentaire `Confidence: LOW` et l'estimation **surestime** la VRAM réellement occupée ([Manuel 15, section 5](15-performances-gpu-dedie.md#5-mémoire-réelle-et-estimation)) : la lire comme un **maximum**. À la fin d'un vrai chargement, la valeur « (8.40 GiB) » imprimée est la **taille du modèle**.

### 3.4 `lms unload` — décharger **[Testée]**

```powershell
lms unload gemma        # par identifiant
lms unload --all        # tous les modèles
```

---

## 4. Serveur local

**[Testée]**

```powershell
lms server status     # « The server is running on port 1234. » ou « The server is not running. »
lms server stop       # « Stopped the server on port 1234. »
lms server start      # « Success! Server is now running on port 1234 »
```

Le serveur reprend les réglages de *Developer → Server Settings* (port, réseau, authentification, JIT…) décrits au [Manuel 06](06-serveur-local-et-api.md). Vérification de l'adresse d'écoute :

```powershell
Get-NetTCPConnection -LocalPort 1234 -State Listen | Select-Object LocalAddress, LocalPort
```

`127.0.0.1` = accessible **uniquement depuis la machine** ; `0.0.0.0` = accessible depuis le réseau.

`lms status` résume l'état global **[Testée]** :

```text
Server: ON (port: 1234)

Loaded Models
  · google/gemma-4-e4b - 6.33 GB
  · text-embedding-nomic-embed-text-v1.5 - 84.11 MB
```

---

## 5. Conversation en ligne de commande

`lms chat` ouvre une conversation interactive ou renvoie une réponse unique **[Testée]** :

```powershell
lms chat google/gemma-4-e4b -p "Réponds en une phrase : à quoi sert un fichier GGUF ?" --reasoning off --stats -y
```

Résultat constaté :

```text
Un fichier GGUF est un format optimisé pour stocker et charger des modèles de langage (LLMs) afin de permettre
leur exécution efficace sur du matériel grand public, y compris les CPU.

Prediction Stats:
  Stop Reason: eosFound
  Tokens/Second: 15.60
  Time to First Token: 1.038s
  Prompt Tokens: 48
  Predicted Tokens: 42
  Total Tokens: 90
```

| Option | Effet |
|---|---|
| `-p, --prompt <texte>` | Affiche la réponse sur la sortie standard puis quitte (mode scriptable) |
| `-s, --system-prompt <texte>` | Prompt système |
| `--stats` | Statistiques détaillées de génération |
| `--reasoning <mode>` | Mode de raisonnement de la session (`off` constaté valide) |
| `--ttl <secondes>` | Durée de maintien du modèle après la fin de la conversation |
| `-y, --yes` | Répondre oui à toutes les questions |

---

## 6. Moteurs d'inférence (runtime)

### 6.1 Lister **[Testée]**

```powershell
lms runtime ls
```

```text
LLM ENGINE                                      SELECTED    MODEL FORMAT
llama.cpp-win-x86_64-avx2@2.28.2                                GGUF
llama.cpp-win-x86_64-nvidia-cuda-avx2@2.28.2                    GGUF
llama.cpp-win-x86_64-vulkan-avx2@2.52.0            ✓            GGUF
llama.cpp-win-x86_64-vulkan-avx2@2.51.0                         GGUF
…
```

Lecture : le **moteur sélectionné** (✓) est utilisé pour les modèles GGUF ; plusieurs versions d'un même moteur peuvent coexister (les anciennes ne sont pas supprimées automatiquement).

### 6.2 Diagnostic matériel **[Testée]**

```powershell
lms runtime survey
```

```text
Survey by llama.cpp-win-x86_64-vulkan-avx2 (2.52.0)
GPU/ACCELERATORS                                        VRAM
Intel(R) Arc(TM) 140T GPU (16GB) (Vulkan, Integrated)   17.90 GiB

CPU: x86_64 (AVX, AVX2)
RAM: 31.40 GiB
```

### 6.3 Autres sous-commandes **[Aide]**

| Commande | Rôle |
|---|---|
| `lms runtime select <moteur>` | Choisir le moteur utilisé |
| `lms runtime get` | Télécharger ou lister les extensions de moteur disponibles |
| `lms runtime update` | Mettre à jour les extensions installées |
| `lms runtime remove` | Supprimer une extension installée (libère de l'espace disque) |

> **Connexion limitée** — `update` et `get` téléchargent de 7 à plus de 200 Mo par moteur. Ne les exécuter que sur un réseau non limité.

---

## 7. Télécharger et importer des modèles

### 7.1 `lms get` **[Aide]**

```powershell
lms get <nom>                       # recherche dans le catalogue puis télécharge
lms get qwen/qwen3.5-9b@q8_0        # « @ » : choisir la quantification
lms get --gguf <nom>                # restreindre au format GGUF
lms get --select <nom>              # choisir la variante avant téléchargement
lms get https://huggingface.co/...  # URL Hugging Face complète
```

`-y` approuve automatiquement ; en cas de plusieurs variantes, la variante présélectionnée selon le matériel est retenue.

### 7.2 `lms import` **[Aide]**

```powershell
lms import --copy --user-repo allenai/olmOCR-2-7B-1025-GGUF D:\transfert\modele.gguf
```

Options : `--user-repo <éditeur/dépôt>`, `-c/--copy`, `-L/--hard-link`, `-l/--symbolic-link`, `--dry-run`, `-y`. Sans `--copy` ni lien, le fichier est **déplacé**. Détails au [Manuel 02](02-selectionner-et-telecharger-un-modele.md#8-installer-un-modèle-sans-connexion).

> **Point d'attention constaté** — Lancé sur un fichier déjà situé dans le dossier des modèles, `lms import --dry-run -y` n'a pas rendu la main. Utiliser la commande sur un fichier extérieur au dossier des modèles.

---

## 8. Journaux

```powershell
lms log stream
```

**[Aide]** — Affiche en continu les messages entrants et sortants du serveur (utile pour vérifier les requêtes reçues et les paramètres appliqués). Les mêmes journaux sont visibles dans *Developer → Developer Logs* ([Manuel 06](06-serveur-local-et-api.md)) et enregistrés dans `%USERPROFILE%\.lmstudio\server-logs\`.

---

## 9. Mode sans interface : `llmster`

`llmster` est le cœur de LM Studio packagé **sans interface graphique**, destiné aux serveurs et aux environnements automatisés. **Constat sur Windows (0.4.25)** : `lms daemon` et `lms status` **existent** mais **n'apparaissent pas** dans `lms --help` ; `lms daemon status` désigne l'application ouverte (« *LM Studio v0.4.25+1 is running* ») ; `up`, `down` et `update` n'ont pas été exécutées ([Manuel 16, section 5](16-sdk-et-plugins.md#5-le-mode-sans-interface--llmster)).

| Commande **[Aide]** | Rôle |
|---|---|
| `lms daemon up` | Démarrer le démon |
| `lms daemon status` | Vérifier son état |
| `lms daemon down` | L'arrêter |
| `lms daemon update` | Le mettre à jour |

Séquence type de déploiement serveur (d'après la documentation officielle) : installer `llmster`, `lms daemon up`, `lms get <modèle>`, `lms load <modèle> …`, `lms server start`. L'installateur de `llmster` est un script distinct à télécharger depuis le site officiel ; **à faire valider par la sécurité** avant tout usage sur un poste ou serveur d'entreprise.

---

## 10. Scripts et automatisation

### 10.1 Charger un modèle et attendre sa disponibilité

```powershell
lms unload --all
lms load google/gemma-4-e4b --gpu max -c 8192 --parallel 1 --identifier gemma -y
lms server start
Invoke-RestMethod http://127.0.0.1:1234/v1/models | ConvertTo-Json -Depth 3
```

### 10.2 Dimensionner avant de charger

```powershell
foreach ($ctx in 4096, 16384, 65536) {
    "--- contexte $ctx"
    lms load google/gemma-4-e4b -c $ctx --estimate-only -y
}
```

### 10.3 Inventaire exploitable

```powershell
lms ls --json | ConvertFrom-Json |
    Select-Object modelKey, paramsString, @{n='Go'; e={[math]::Round($_.sizeBytes/1GB,2)}}, vision, maxContextLength |
    Format-Table
```

### 10.4 Réponse unique dans un script

```powershell
$reponse = lms chat google/gemma-4-e4b -p "Résume en 10 mots : ..." --reasoning off -y 2>$null
```

---

## 11. Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `lms` introuvable | Dossier `bin` absent du `PATH`, ou CLI non installée | Vérifier `%USERPROFILE%\.lmstudio\bin\lms.exe` ; relancer LM Studio (installation automatique du CLI au démarrage) |
| Message « Waking up LM Studio service… » puis latence | Service arrêté | Normal : le service démarre à la première commande |
| `lms load` : modèle introuvable | Clé erronée | `lms ls` pour lire la clé exacte |
| `lms load` bloqué par un garde-fou | Estimation > limite autorisée | Réduire `-c` ou la quantification ; voir [Manuel 03](03-charger-un-modele.md#8-dépannage) |
| Erreur « port déjà utilisé » au démarrage du serveur | Autre programme sur le port 1234 | Changer le port dans *Server Settings* ou libérer le port |
| PowerShell affiche des erreurs rouges pour des messages normaux | Sortie d'information sur stderr | Ignorer ; contrôler `$LASTEXITCODE` |
| Commande qui n'en finit pas | Question interactive en attente | Ajouter `-y` ; fermer et relancer |
