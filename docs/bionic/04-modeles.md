# Manuel Bionic 04 — Modèles : choisir, télécharger, régler

> **Objet** : choisir le modèle adapté à une tâche d'agent, le télécharger depuis Bionic, comprendre la liste du sélecteur, l'effort de raisonnement et la gestion de la mémoire.
> **Prérequis** : [Manuel Bionic 00](00-notions-agent.md#4-où-sexécute-le-modèle), [Manuel LM Studio 00](../lmstudio/00-notions-fondamentales.md) (taille, quantification, contexte).
> **Version décrite** : Bionic 1.1.7, Windows 11.
> **Statut des informations** : [Vérifié] observé et mesuré sur **deux postes** : GPU intégré (Intel Core Ultra 7 255H, 31 Go de RAM, 6 octobre 2026) et **GPU dédié** (Ryzen 5 9600X, 61,6 Go de RAM, RTX 4060 Ti de 16 Go, 7 octobre 2026) ; [Source] documentation officielle ; [Estimation] ; [À tester]. Les valeurs du GPU intégré sont conservées entre parenthèses (« GPU intégré : … »).

---

## Sommaire

1. [Critères de choix pour un agent](#1-critères-de-choix-pour-un-agent)
2. [Le sélecteur de modèle](#2-le-sélecteur-de-modèle)
3. [Télécharger un modèle](#3-télécharger-un-modèle)
4. [Effort de raisonnement](#4-effort-de-raisonnement)
5. [Mémoire, chargement et déchargement](#5-mémoire-chargement-et-déchargement)
6. [Comparaison mesurée](#6-comparaison-mesurée)
7. [Partage avec LM Studio](#7-partage-avec-lm-studio)

---

## 1. Critères de choix pour un agent

### Essentiel

Un modèle utilisé comme agent doit réunir quatre qualités :

| Critère | Pourquoi | Où le vérifier |
|---|---|---|
| **Appel d'outils** | Sans lui, aucune action (fichier, commande) | Étiquette **Outils** dans l'Explorer |
| **Taille suffisante** | Suivre un plan, éviter les erreurs de chemin | Nombre de paramètres (4 Md, 12 Md, 27 Md…) |
| **Vision** *(si images)* | Lire captures, scans, factures | Étiquette **Vision** |
| **Raisonnement** *(si tâches complexes)* | Réfléchir avant d'agir | Étiquette **Raisonnement** ; réglage dans le sélecteur |

| Taille | Usage réaliste en local |
|---|---|
| ≈ 4 Md (*Gemma 4 E4B*) | Tâches courtes, cadrées ; une action à la fois |
| ≈ 12 Md (*Gemma 4 12B QAT*) | Documents, code de taille raisonnable |
| ≈ 26 Md dont 4 Md actifs (*Gemma 4 26B A4B*, MoE — *Mixture of Experts*, « mélange d'experts ») | Documents, code, enchaînement d'outils fiable ; fichier de 18 Go, **plus gros que les 16 Go de VRAM** d'une RTX 4060 Ti : une partie reste en RAM (voir section 5) |
| ≥ 27 Md (*Qwen3.8 27B*, dense) | Tâches complexes ; mémoire importante (≈ 18 Go en Q4_K_M pour 27 Md) ; niveaux de raisonnement propres (« Moyen » affiché par défaut dans le sélecteur) |
| Cloud | Tâches longues et multi-fichiers ([Manuel 10](10-securite-compte-api.md)) |

### Pour aller plus loin

- **Mémoire à prévoir** = taille du fichier du modèle + cache de contexte (**KV cache**) + marge du système. Pour un agent, le contexte utile est de **plusieurs dizaines de milliers de tokens** ([Manuel LM Studio 00](../lmstudio/00-notions-fondamentales.md), calcul de la RAM).
- Les modèles **QAT** (*Quantization-Aware Training*) sont entraînés en tenant compte de la compression : qualité proche de la version non compressée pour une taille réduite [Source : fiche du modèle].
- Les modèles de type **MoE** (*Mixture of Experts*, ex. *Gemma 4 26B A4B*) n'activent qu'une partie de leurs paramètres par token : vitesse proche d'un petit modèle, mémoire d'un grand [Estimation].

---

## 2. Le sélecteur de modèle

![Sélecteur de modèles](../img/bionic/04-modeles/07-selecteur-deux-modeles.png)
*Figure 1 — Sélecteur : filtre, modèles disponibles, effort de raisonnement.*

| Élément | Rôle |
|---|---|
| **Filtrer les modèles** | Recherche dans la liste |
| **Liste** | Modèles disponibles : nom, format (**GGUF**) ; coche = modèle de la session |
| **Effort de raisonnement** | Sous-menu ([section 4](#4-effort-de-raisonnement)) |
| Bouton du composeur | Nom du modèle + état du raisonnement (« Gemma 4 E4B Activé ») ; **« Choisir un modèle »** s'il n'y en a pas |

Le modèle se choisit **par session** ; le modèle par défaut des nouvelles sessions est le **Modèle racine** (Réglages → Agent, [Manuel 03](03-reglages.md#3-agent)).

Les modèles **Remote** (LM Link) et **Cloud** apparaissent dans la même liste lorsque le compte est connecté et que l'appareil lié est disponible [Source].

---

## 3. Télécharger un modèle

### Essentiel

Réglages → **Modèles locaux** → **Explorer**.

![Explorer annoté](../img/bionic/04-modeles/03-explorer-options-telechargement.png)
*Figure 2 — Explorer : fiche de *Gemma 4 12B QAT* et options de téléchargement.*

| N° | Élément | Rôle |
|---|---|---|
| ① | **Options de téléchargement** | Format (**GGUF**), variante et quantification (ici *Gemma 4 12B Instruct QAT*, **Q4_0**), taille (**7,15 GB**), mention **Recommandé**, indicateur d'adéquation à la machine (**Full GPU Offload Possible**) |
| ② | **Télécharger sur** | Appareil de destination (**Cet appareil** ; autres appareils si LM Link) |
| ③ | **Télécharger** | Lance le téléchargement |
| ④ | **Sélection de l'équipe / Recommandé** | Filtre et tri du catalogue ; recherche sur Hugging Face |

> **Lecture de l'indicateur d'adéquation** — Sur le poste à **GPU intégré**, le vert correspond à la mémoire partagée avec la RAM. Sur le poste à **GPU dédié** (16 Go de VRAM), le passage vert → bleu se situe entre **14,5 et 14,8 Go** (≈ 91–93 % de la VRAM) et le passage bleu → rouge entre 59,1 et 60,5 Go (≈ 96–98 % de la RAM seule) **[Vérifié]**. Les trois états (vert, bleu « partiel », rouge « trop grand »), leur sens et les quantifications de la liste sont décrits dans le [Manuel LM Studio 02](../lmstudio/02-selectionner-et-telecharger-un-modele.md#6-les-indicateurs-dadéquation-matérielle).

Colonne de gauche : liste des modèles avec, pour chacun, trois pictogrammes (Vision, Outils, Raisonnement), l'ancienneté de la mise à jour et un résumé. La fiche (droite) donne le nombre de **paramètres**, l'**architecture**, les **formats** (GGUF, MLX), les **fonctionnalités** et le **README**.

Marche à suivre :

1. Choisir un modèle dans la liste.
2. Contrôler les **fonctionnalités** (Outils obligatoire pour un agent) et la **taille** par rapport à la RAM.
3. Choisir l'appareil de destination.
4. **Télécharger**.
5. Suivre l'avancement : bouton **Téléchargements** (en haut), puis revenir à l'application. Le modèle apparaît dans le sélecteur à la fin.

![Panneau de téléchargements](../img/bionic/04-modeles/05-panneau-telechargements.png)
*Figure 3 — Panneau « Téléchargements » : volume reçu, débit, temps restant, pause, annulation.*

> **Exemple mesuré (poste de test)** — *Gemma 4 12B QAT* : fichier du modèle **6,98 Go** + projecteur de vision (**mmproj**) **0,18 Go** = **7,15 Go**. Débit observé : **≈ 14 Mo/s** au début, ralenti ensuite ; durée totale de l'ordre de **15 à 20 minutes** sur la connexion du poste. Le bouton affiche **« Téléchargement : n % »** pendant l'opération.

### Pour aller plus loin

| Point | Détail |
|---|---|
| **Stockage** | `~\.lmstudio\models\<éditeur>\<modèle>\` ; ex. `lmstudio-community\gemma-4-12B-it-QAT-GGUF\` contenant le modèle (`.gguf`) et le projecteur de vision (`mmproj-….gguf`) |
| **Fichier en cours** | Préfixe `downloading_` et extension `.part` jusqu'à la fin |
| **Pause / reprise / annulation** | Boutons de la ligne de téléchargement ; la documentation indique aussi la possibilité de réessayer [Source] |
| **Formats** | **GGUF** (llama.cpp : Windows, Linux, macOS) ; **MLX** (Mac Apple Silicon) |
| **Quantification** | Une seule variante était proposée pour ce modèle ; d'autres modèles en proposent plusieurs (voir le [Manuel LM Studio 02](../lmstudio/02-selectionner-et-telecharger-un-modele.md)) |
| **Espace disque** | Prévoir la taille du modèle + marge ; le dossier se change dans Réglages → Bibliothèque |

> **Point d'attention (réseau d'entreprise)** — le catalogue est interrogé et les fichiers sont téléchargés depuis des services externes (connexion sortante HTTPS sur le port 443 observée pendant le téléchargement). Sur un poste d'entreprise, vérifier que cet usage est autorisé et, pour des modèles volumineux, éviter les connexions partagées ou facturées au volume.

---

## 4. Effort de raisonnement

![Effort de raisonnement](../img/bionic/04-modeles/01-effort-raisonnement.png)
*Figure 4 — Sous-menu « Effort de raisonnement » : Désactivé / Activé.*

### Essentiel

Le **raisonnement** (*thinking*) est une phase où le modèle rédige ses réflexions avant de répondre ou d'agir. Dans le fil, elle apparaît comme **« Réflexion terminée »** dans le travail déplié.

| Réglage | Effet | Quand l'utiliser |
|---|---|---|
| **Activé** | Réflexion avant action ; meilleure fiabilité sur les tâches à plusieurs étapes ; plus lent, consomme davantage de contexte | Code, analyse, tâches ambiguës |
| **Désactivé** | Réponse directe ; plus rapide | Rédaction simple, reformulation, extraction cadrée |

Le réglage se fait **par session**, dans le sélecteur de modèle. Pour les modèles testés, deux niveaux seulement sont proposés (Désactivé / Activé) ; d'autres modèles peuvent proposer plusieurs niveaux (« reasoning level ») [Source].

### Pour aller plus loin

L'effet exact sur la durée et la qualité est présenté en [section 6](#6-comparaison-mesurée).

---

## 5. Mémoire, chargement et déchargement

| Notion | Description | Où |
|---|---|---|
| **Chargement à la demande** (JIT) | Le modèle se charge au premier message d'une session ou à la première requête d'API | Réglages → API des modèles locaux (activé par défaut) |
| **Instances chargées** | Liste des modèles présents en mémoire | Réglages → Instances chargées |
| **AutoFit** | Choix automatique des paramètres de chargement ; longueur de contexte minimale réglable | Réglages → Paramètres par défaut des modèles locaux |
| **Protection du chargement** | Refuse un chargement dangereux pour la stabilité du système | Idem (*Désactivée*, *Souple*, *Équilibrée*, *Stricte*, *Personnalisée*) |
| **Moteur** | Moteur d'exécution (Vulkan, CPU, CUDA) | Réglages → Moteur d'exécution |

Bionic **n'expose pas** les réglages détaillés de chargement de LM Studio (nombre de couches sur GPU, quantification du KV cache, etc.). Pour un contrôle fin, charger le modèle dans LM Studio ([Manuel LM Studio 03](../lmstudio/03-charger-un-modele.md)) — sans oublier que les deux applications ne cohabitent pas.

![Instance chargée](../img/bionic/04-modeles/09-instance-chargee.png)
*Figure 6 — Réglages → Instances chargées : modèle, taille, format, quantification, **contexte chargé** (262 144), état, bouton **Décharger**.*

> **Mesure importante (poste de test, 31 Go de RAM)** — *Gemma 4 12B QAT* (fichier de 7,15 Go) chargé par Bionic avec le contexte par défaut de **262 144 tokens** : le processus du moteur (`llama-server`) occupait **14,1 Go** de mémoire physique (**18,9 Go** de mémoire privée) et il restait **0,4 Go** de RAM libre sur le poste (autres applications comprises). Le modèle seul pèse 7 Go ; le reste est le **cache de contexte** (KV cache), réservé pour la longueur maximale.
>
> **Mesure sur GPU dédié (RTX 4060 Ti 16 Go, 61,6 Go de RAM)** — Mémoire occupée **après chargement par Bionic** (ajustement automatique *AutoFit*, `lms ps` + `nvidia-smi` + processus `llama-server`, 7 octobre 2026) **[Vérifié]** :
>
> | Modèle | Fichier | Contexte chargé | VRAM occupée | RAM du moteur (physique / privée) |
> |---|---|---|---|---|
> | *Gemma 4 E4B* (Q8_0) | 9,02 Go | **131 072** | **8,28 Go** | 8,47 / 9,87 Go |
> | *Gemma 4 26B A4B* (Q4_K_M) | 17,99 Go | **16 384** | **14,03 Go** | 17,17 / 16,14 Go |
> | *Qwen3.8 27B* (Q4_K_M) | 17,74 Go | **16 384** | **11,67 Go** | 19,06 / 16,87 Go |
>
> VRAM de base du poste sans modèle : 1,0 Go (bureau Windows). Le chargement est limité à **4 requêtes parallèles** (`parallel = 4`). **Le contexte de 16 384 jetons des deux gros modèles n'est pas une limite de mémoire** : c'est la valeur de **« Longueur de contexte minimale pour AutoFit »** (Réglages → Paramètres par défaut des modèles locaux), qui vaut **16 384** par défaut ([Manuel 03](03-reglages.md#10-modèles-locaux)). Le petit modèle obtient 131 072 parce que l'ajustement automatique lui accorde davantage ; les modèles de 26 à 27 Md reçoivent **exactement le minimum**. Conséquence directe : une requête de **18,6 k jetons échoue avec le 26B** (« *The selected model was loaded with a context length that is too small for this request* ») alors que l'E4B la traite ([Manuel 14, section 2](14-commandes-compaction-navigateur.md#2-compacter-une-session--compact)).

![Paramètres par défaut : contexte minimal d'AutoFit](../img/bionic/04-modeles/10-autofit-contexte-minimal.png)
*Figure 7 — Réglages → Paramètres par défaut des modèles locaux : ① longueur de contexte minimale pour AutoFit (16 384), ② protection lors du chargement (*Souple*).*

**Effet du minimum AutoFit** [Vérifié, 7 octobre 2026 ; modèle déchargé avant chaque mesure ; `lms ps`, `nvidia-smi`, processus `llama-server`] :

| Minimum réglé | Modèle | Contexte chargé | VRAM occupée | RAM du moteur (physique / privée) |
|---|---|---|---|---|
| **16 384** (défaut) | *Gemma 4 26B A4B* | 16 384 | 14,03 Go | 17,17 / 16,14 Go |
| 32 768 | idem | 32 768 | 13,95 Go | 17,21 / 16,10 Go |
| 65 536 | idem | 65 536 | 14,02 Go | 17,27 / 16,24 Go |
| 131 072 | idem | 131 072 | 14,03 Go | 17,41 / 16,39 Go |
| 262 144 | idem | **262 144** | 13,74 Go | 17,70 / 16,38 Go |
| 16 384 (défaut) | *Qwen3.8 27B* | 16 384 | 11,67 Go | 19,06 / 16,87 Go |
| 65 536 | idem | 65 536 | 11,61 Go | 21,25 / 18,97 Go |
| 262 144 | idem | 262 144 | 11,35 Go | **32,89 / 30,38 Go** |

- Pour le **26B**, relever le minimum à **262 144 ne coûte presque rien en mémoire** (VRAM inchangée, RAM +0,5 Go) **et ne ralentit pas** la génération : texte de 1 500 mots en **71,9 s** à 262 144 contre **73,3 s** à 16 384. La lecture complète du fichier de 18,6 k jetons, qui échouait, **réussit** dès le minimum à 32 768 (code d'archivage et résumé corrects).
- Pour **Qwen3.8 27B**, la RAM du moteur augmente avec le minimum (**+2 Go** à 65 536, **+14 Go** à 262 144) : **65 536** est un compromis raisonnable sur 61,6 Go de RAM ; la vitesse de Qwen à grand contexte n'a pas été mesurée [À tester].
- Le refus de chargement annoncé pour un minimum inatteignable n'a **pas** été provoqué (tous les essais ont réussi, jusqu'à 262 144, sur 61,6 Go de RAM) [À tester sur un poste à moins de RAM].
- Le réglage est **global** (tous les modèles locaux) : il a été **remis à 16 384** après les essais.

> **Conséquences** : (1) un grand contexte peut **saturer** la mémoire d'un poste ordinaire (poste à GPU intégré, 31 Go : 12B à 262 144 jetons = 14,1 Go de RAM physique, 0,4 Go de RAM libre) ; (2) la **taille de contexte chargée** est le principal levier de mémoire **pour les modèles denses** (Qwen) mais **très peu pour le MoE** testé (26B) ; (3) Bionic n'expose pas ce réglage **par modèle** : une seule valeur minimale pour tous. Pour un agent qui lit des fichiers volumineux, **relever le minimum d'AutoFit** plutôt que de charger le modèle dans LM Studio.

---

## 6. Comparaison mesurée

Deux séries de mesures, **une seule tâche à la fois** : (1) **GPU intégré**, moteur Vulkan (6 octobre 2026) ; (2) **GPU dédié** RTX 4060 Ti, moteur CUDA 12 (7 octobre 2026), avec le **modèle réellement utilisé vérifié dans la base de sessions de Bionic** (champ `modelSpecifier`). Les durées de la seconde série sont **mesurées de l'envoi à la fin de la réponse** (modèle déjà chargé, sauf mention) ; la valeur affichée par Bionic (« Travail effectué en … ») est donnée quand elle est lisible. Les durées de la première série incluent le chargement initial du modèle lorsqu'il n'était pas déjà en mémoire.

| Tâche | Modèle | Raisonnement | Durée affichée | Résultat |
|---|---|---|---|---|
| Mémo de 6 lignes dans un fichier | *Gemma 4 E4B* | Activé | 2 min 4 s | Fichier créé (`+7`) |
| Idem | *Gemma 4 E4B* | **Désactivé** | **1 min 23 s** | Fichier créé (`+7`) |
| Facture (image) → `facture.json` | *Gemma 4 E4B* | Activé | 55 s | Valeurs justes, **aucun fichier créé** |
| Idem | *Gemma 4 12B QAT* | Activé | 4 min 25 s (chargement inclus) | Fichier créé (`+6`), valeurs justes |
| Correction d'un bogue + tests | *Gemma 4 E4B* | Activé | 6 min 22 s | Corrigé, après deux obstacles |
| Idem (consigne précisant la commande) | *Gemma 4 12B QAT* | Activé | 4 min 50 s | Corrigé, 2 confirmations, chemins corrects |

**GPU dédié** (RTX 4060 Ti ; la valeur du GPU intégré figure entre parenthèses) :

| Tâche | Modèle | Raisonnement | Durée | Résultat |
|---|---|---|---|---|
| Mémo dans un fichier | *Gemma 4 E4B* | Activé | **29 s** (GPU intégré : 2 min 4 s) | Fichier créé |
| Idem | *Gemma 4 E4B* | **Désactivé** | **≈ 15 s** (1 min 23 s) | Fichier créé |
| Facture (image) → `facture.json` | *Gemma 4 E4B* | Activé | **31 s** (55 s) | Valeurs justes, **aucun fichier créé** (comme sur GPU intégré) |
| Idem | *Gemma 4 26B A4B* | Activé | **≈ 51 s** (4 min 25 s avec le 12B, chargement inclus) | **`facture.json` créé** |
| Correction d'un bogue + tests | *Gemma 4 E4B* | Activé | **1 min 38 s** (6 min 22 s) | Code corrigé ; **tests non lancés** ; réponse **en anglais** |
| Idem | *Gemma 4 26B A4B* | Activé | **43 s** (4 min 50 s avec le 12B) | Corrigé ; `pytest` lancé (2 confirmations) |
| `/compact` d'une session de 18,5 k jetons | *Gemma 4 E4B* | Désactivé | **12 s** (≈ 90 s, 7,2 → 6,9 k) | 18,5 k → 6,7 k |
| `/compact` d'une session de 12,3 k jetons | *Gemma 4 26B A4B* | Désactivé | **10 s** | 12,3 k → 6,8 k ; sous-session « Compaction » enregistrée en 26B |

![Mémo sans raisonnement](../img/bionic/04-modeles/08-memo-raisonnement-desactive.png)
*Figure 5 — Mémo avec raisonnement désactivé : 1 min 23 s, même résultat (`+7 −0`).*

**Enseignements** [Vérifié, un essai par cas] :

- **Désactiver le raisonnement** a réduit d'environ **un tiers** la durée d'une tâche de rédaction simple (2 min 4 s → 1 min 23 s) sans effet visible sur le résultat.
- Le **modèle de 12 Md** est plus lent sur une tâche cadrée (≈ 4 à 5 min) mais **réalise réellement les actions** (fichier créé, commandes correctes), là où le petit modèle a **annoncé** une création de fichier sans l'effectuer.
- Les durées incluent le **chargement** du modèle lorsqu'il n'était pas déjà en mémoire (indicateur « Chargement du modèle : n % » dans le fil). Sur GPU dédié, une courte tâche (« Réponds uniquement par le mot OK ») lancée **modèle déchargé** dure **15 s** (E4B), **34 s** (26B) et **64 s** (Qwen), chargement à la demande compris **[Vérifié]**.
- Sur GPU dédié, le **gain du raisonnement désactivé** reste d'environ **moitié** (29 s → 15 s) pour le mémo. Le **26B** réalise réellement les actions (fichier créé, tests lancés) en **moins d'une minute**, là où l'E4B n'écrit pas le fichier de la facture et ne lance pas les tests : l'écart de fiabilité des outils (voir [Manuel 07](07-code-et-shell.md)) pèse plus que l'écart de vitesse.
- Les consignes n'avaient pas la même précision (celle du 12 Md pour le code nommait la commande de test) : la comparaison est **indicative**.

---

## 7. Partage avec LM Studio

- Bionic et LM Studio utilisent le **même dossier de modèles** (`~\.lmstudio\models`) : un modèle téléchargé par l'un est **visible** par l'autre [Vérifié : *Gemma 4 E4B*, téléchargé pour LM Studio, apparaît dans Bionic].
- Les **fichiers `mmproj`** (projecteur de vision) accompagnent le modèle dans le même dossier.
- Les paramètres de chargement par modèle (contexte, offload) **ne sont pas partagés** [Estimation]. Les deux applications ne cohabitent pas (voir [Manuel 01](01-presentation-installation.md)) : LM Studio doit être **fermé** avant d'ouvrir Bionic, et inversement ; sur le poste à GPU dédié, la même carte de 16 Go est utilisée par l'un ou l'autre.
- Sur le poste à GPU dédié, `lms ps` (la CLI de LM Studio) **liste le modèle chargé par Bionic** (contexte, parallélisme) : c'est le moyen de relever ce que fait AutoFit [Vérifié].
