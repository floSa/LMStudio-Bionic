# Manuel 15 — Performances sur GPU dédié

> **Objet** : mesurer et expliquer l'effet d'une carte graphique dédiée (16 Go de VRAM) sur la vitesse et la mémoire : moteurs CUDA / Vulkan / CPU, nombre de couches sur le GPU, parallélisme, Flash Attention, lots, cache K/V, grand contexte, modèles plus gros que la VRAM, experts MoE sur le CPU, décodage spéculatif.
> **Prérequis** : [Manuel 00](00-notions-fondamentales.md) (VRAM, quantification, contexte), [Manuel 03](03-charger-un-modele.md) (paramètres de chargement).
> **Version décrite** : LM Studio 0.4.25 (Build 1), moteur *llama.cpp* CUDA 12 2.53.0, Windows 11 Pro. Mesures du **7 octobre 2026**.
> **Poste de mesure (GPU dédié)** : AMD Ryzen 5 9600X (6 cœurs, AVX2), **61,6 Go de RAM**, **NVIDIA GeForce RTX 4060 Ti, 16,00 Go de VRAM** (pilote 616.92, CUDA 13.4). Le poste des autres manuels (Intel Core Ultra 7 255H, 31 Go de RAM, GPU intégré, Vulkan) est appelé ci-dessous **« GPU intégré »**.
> **Contrainte** : **aucun modèle n'a été téléchargé** pour ces essais ; seuls les modèles déjà présents ont servi (tableau de la [section 0](#0-poste-modèles-et-méthode)).
> **Étiquettes** : **[Vérifié]** mesuré ; **[Source]** documentation ; **[Estimation]** interprétation non prouvée ; **[À tester]**.

---

## Sommaire

0. [Poste, modèles et méthode](#0-poste-modèles-et-méthode)
1. [Ce qu'il faut retenir](#1-ce-quil-faut-retenir)
2. [Moteurs et nombre de couches sur le GPU](#2-moteurs-et-nombre-de-couches-sur-le-gpu)
3. [Parallélisme : le débit total augmente](#3-parallélisme--le-débit-total-augmente)
4. [Flash Attention, lots et cache K/V](#4-flash-attention-lots-et-cache-kv)
5. [Mémoire réelle et estimation](#5-mémoire-réelle-et-estimation)
6. [Modèles plus gros que la VRAM](#6-modèles-plus-gros-que-la-vram)
7. [Décodage spéculatif](#7-décodage-spéculatif)
8. [Avant / après : GPU intégré et GPU dédié](#8-avant--après--gpu-intégré-et-gpu-dédié)
9. [Reproduire les mesures](#9-reproduire-les-mesures)
10. [Limites](#10-limites)

---

## 0. Poste, modèles et méthode

### Modèles utilisés (déjà installés)

| Modèle | Nature | Fichier | Remarque |
|---|---|---|---|
| **Gemma 4 E4B** | dense effectif ≈ 4 Md (7,5 Md avec les embeddings), vision | **Q8_0, 9,02 Go** | **Autre quantification** que dans les manuels 03 à 06 (Q4_K_M, 6,33 Go) : les écarts « avant / après » mêlent donc **GPU et quantification** ; la comparaison reste indicative. |
| **Gemma 4 26B A4B** | **MoE** (26 Md au total, ≈ 4 Md actifs), vision | Q4_K_M, 17,99 Go | Dépasse la VRAM : sert aux essais d'offload partiel et d'experts sur le CPU. |
| **Qwen3.8 27B** | dense, vision, badge **MTP** | Q4_K_M, 17,74 Go | Dépasse la VRAM ; sert au décodage spéculatif MTP. |
| **OlmOCR 2 7B** | dense, vision, OCR | Q4_K_M (6,04 Go) et Q8_0 (9,45 Go) | Voir [Manuel 05, section 7](05-vision-images-et-ocr.md#7-exemple--un-modèle-docr-dédié-olmocr-2-7b). |

### Méthode

- Chargement par `lms load` (nombre de couches, contexte, parallélisme), par l'API `POST /api/v1/models/load` (Flash Attention, lot d'évaluation, cache K/V en RAM) ou par le **SDK** ([Manuel 16](16-sdk-et-plugins.md)) pour ce qui n'existe ni en ligne de commande ni dans l'API (quantification du cache K/V, lot physique, arguments `llama.cpp`, décodage spéculatif).
- **VRAM** : `nvidia-smi` avant / après chargement (en **Gio**, comme l'affiche LM Studio sous le nom « GB »). **RAM** : mémoire privée du processus `llama-server` et variation de la mémoire système.
- **Vitesse** : réponse en flux ; *traitement du prompt* = jetons du prompt ÷ délai avant le premier jeton (prompt de ≈ 1 770 jetons, ou ≈ 5 300 jetons) ; *génération* = (jetons − 1) ÷ durée de génération (200 jetons, température 0, raisonnement désactivé). Une requête d'échauffement précède chaque mesure.
- Une mesure par configuration (écart observé entre deux répétitions : ≈ 2 à 5 %). Résultats bruts : `outils/resultats/gpu_*.json`.

---

## 1. Ce qu'il faut retenir

| Question | Réponse mesurée |
|---|---|
| Gain du GPU dédié par rapport au GPU intégré ? | **Génération ≈ × 3** (14,8 → ≈ 45–47 tok/s) et **lecture du prompt ≈ × 11** (353 → ≈ 3 700–3 900 tok/s) sur le même modèle, quantification différente (section 8). |
| Quel moteur ? | **CUDA** (≈ 3 700 tok/s en lecture du prompt) devant **Vulkan** (≈ 2 700) ; la génération est identique (≈ 45–46 tok/s). Le moteur **CPU** reste à 9 tok/s et 49 tok/s en lecture. |
| Le parallélisme sert-il ? | **Oui** sur GPU dédié : le débit total passe de 45 à **264 tok/s** avec 8 requêtes simultanées (l'inverse du GPU intégré). |
| Flash Attention ? | **À laisser activée** : lecture du prompt × 3 plus rapide à 8 192 jetons ; −1,2 Go de VRAM à 65 536 jetons. |
| Quantifier le cache K/V ? | Économise 0,16 à 0,56 Go à 65 536 jetons pour ce modèle, **sans perte de vitesse** et sans échec de rappel sur un texte de 44 000 jetons (essai simple). |
| Désactiver *Offload KV Cache to GPU* ? | **Non** : génération −18 %, lecture du prompt −21 %, pour 0,06 Go de VRAM gagnés. |
| Un modèle de 18 Go sur 16 Go de VRAM ? | **Oui** en offload partiel ; **ne pas forcer `max`** : le modèle MoE tourne à 26 tok/s en `max` contre **37 tok/s** en automatique et **55 tok/s** avec les experts des 8 premières couches sur le CPU (section 6). |
| L'estimation de LM Studio est-elle fiable ? | Elle **surestime la mémoire GPU** de 2,7 à 7,5 Go pour Gemma 4 E4B (section 5) ; la mémoire de la RAM reste mobilisée (≈ 8 Go) même modèle entièrement sur le GPU. |

---

## 2. Moteurs et nombre de couches sur le GPU

### Essentiel

Gemma 4 E4B Q8_0, contexte 8 192, une requête à la fois, `lms load --gpu <réglage>`. Le moteur se choisit dans *Settings → Runtime* ou par `lms runtime select`.

| Moteur | Couches sur le GPU | VRAM (Go) | Lecture du prompt (tok/s) | Génération (tok/s) | Délai 1er jeton (court) |
|---|---|---|---|---|---|
| **CUDA 12** (2.53.0) | **max** (42) | 6,20 | **3 746** | **45,0** | 0,09 s |
| CUDA 12 (2.53.0) | 0,75 | 5,07 | 1 644 | 22,4 | 0,27 s |
| CUDA 12 (2.53.0) | 0,5 | 4,06 | 1 247 | 13,7 | 0,40 s |
| CUDA 12 (2.53.0) | 0,25 | 3,04 | 888 | 10,0 | 0,73 s |
| CUDA 12 (2.53.0) | off (0) | 1,35 | 700 | 8,9 | 0,73 s |
| CUDA 12 (2.51.0) | max | 6,21 | 3 608 | 45,0 | 0,09 s |
| **Vulkan** (2.51.0) | max | 6,10 | 2 659 | **46,0** | 0,19 s |
| Vulkan (2.51.0) | 0,5 | 3,94 | 1 078 | 13,0 | 0,55 s |
| Vulkan (2.51.0) | off | 1,23 | **142** | 8,5 | 0,90 s |
| **CPU AVX2** (2.51.0) | — | 0,00 | **48,5** | 8,8 | 0,73 s |

Chargement : 6,3 à 9,1 s selon la configuration (modèle déjà dans le cache de fichiers).

```text
Génération (tok/s)          Lecture du prompt (tok/s)
CUDA max     ████████████████████████████████████████████ 45     ████████████████████████████████████████████ 3746
Vulkan max   █████████████████████████████████████████████ 46     ███████████████████████████████ 2659
CUDA 50 %    █████████████ 13,7                                  ███████████████ 1247
CUDA 0       █████████ 8,9                                       ████████ 700
CPU AVX2     █████████ 8,8                                       █ 48,5
```

### Lecture

- **La génération dépend presque uniquement de la part de couches sur le GPU** : elle progresse **plus que proportionnellement** (8,9 → 10,0 → 13,7 → 22,4 → 45,0 tok/s pour 0 / 25 / 50 / 75 / 100 % des couches), car chaque couche restée sur le CPU ralentit tout le trajet. Un modèle qui tient **entièrement** dans la VRAM est donc nettement plus rapide qu'un modèle « presque » entièrement chargé.
- **Le moteur CUDA accélère la lecture du prompt même avec 0 couche sur le GPU** (700 tok/s au lieu de 48,5 pour le moteur CPU) : le calcul des gros lots de prompt reste sur la carte **[Estimation : cause non documentée]**. Le moteur Vulkan ne le fait pas (142 tok/s à 0 couche).
- **Vulkan en génération = CUDA** : la génération est limitée par la **bande passante mémoire**, identique pour les deux interfaces sur la même carte ; la lecture du prompt, limitée par le **calcul**, favorise CUDA (+ 41 %).
- **CUDA 2.51.0 et 2.53.0** : écart de 3 % en lecture du prompt (3 608 contre 3 746), génération identique.
- **Garder le moteur CUDA** pour une carte NVIDIA. Vulkan est utile pour une carte AMD ou Intel.

> **Comparaison avec les manuels 03 et 00** — Sur le GPU intégré : 14,8 tok/s en génération et 353 tok/s en lecture du prompt à 100 % de GPU, **11,2 tok/s et 215 tok/s sans GPU**. Le gain du passage « CPU seul → GPU » est ici de **× 5 en génération** et **× 77 en lecture du prompt** (moteur CPU), au lieu de × 1,3 et × 1,6.

---

## 3. Parallélisme : le débit total augmente

### Essentiel

*Max Concurrent Predictions* (`--parallel`) autorise plusieurs requêtes simultanées. Mesure : n requêtes de 150 jetons lancées en même temps (Gemma 4 E4B Q8_0, tout sur le GPU, contexte 8 192).

| Requêtes simultanées | Débit total (tok/s) | Par requête (tok/s) | VRAM (Go) | Lecture du prompt (tok/s) |
|---|---|---|---|---|
| 1 | 45 | 45,2 | 6,19 | 3 681 |
| 2 | **83** | 42,5 | 6,23 | 3 573 |
| 4 | **152** | 39,2 | 6,26 | 3 572 |
| 8 | **264** | 34,2 | 6,34 | 3 675 |

Une requête isolée n'est **pas ralentie** par un parallélisme élevé réglé au chargement. Le coût mémoire est faible (cache unifié : +0,15 Go pour 8 emplacements).

### Lecture

- Sur un GPU dédié, la génération d'une requête n'occupe qu'une partie du calcul disponible : les autres requêtes utilisent le reste. Le débit total croît presque linéairement jusqu'à 8 requêtes ; le temps par requête ne baisse que de 24 %.
- **Sur le GPU intégré, l'inverse a été mesuré** : 4 requêtes simultanées donnaient 12,8 tok/s au total (contre 14,8 pour une seule) car la bande passante était saturée ([Manuel 03, section 5.5](03-charger-un-modele.md#55-concurrence-selon-le-matériel)). **La règle dépend donc du matériel.**
- Réglage conseillé sur GPU dédié : **4 emplacements** (défaut) pour un usage multi-outils (chat + assistant de code + indexation), **1** pour du traitement séquentiel (OCR par lot) afin de réserver tout le contexte à une requête.

---

## 4. Flash Attention, lots et cache K/V

### 4.1 Flash Attention (API `flash_attention`)

| Contexte | Flash Attention | VRAM (Go) | Lecture du prompt, 2 000 jetons (tok/s) | Lecture, 5 300 jetons (tok/s) | Génération (tok/s) |
|---|---|---|---|---|---|
| 8 192 | **activée** | 6,21 | **3 885** | — | 47,5 |
| 8 192 | désactivée | 6,49 | 1 227 | — | 46,7 |
| 65 536 | **activée** | 7,13 | 3 883 | **6 795** | 47,4 |
| 65 536 | désactivée | 8,35 | 1 249 | 3 840 | 46,7 |

Désactiver Flash Attention **divise par 3 la lecture du prompt** à 8 192 jetons, ajoute 0,3 Go de VRAM à 8 192 jetons et **1,2 Go à 65 536**. La génération ne change presque pas. **À laisser activée.**

### 4.2 Taille de lot d'évaluation (`eval_batch_size`) et lot physique

| Réglage | VRAM (Go) | Lecture, 2 000 jetons | Lecture, 5 300 jetons | Génération |
|---|---|---|---|---|
| **Lot d'évaluation** 128 | 6,24 | 2 971 | 5 001 | 47,4 |
| 512 | 6,34 | 3 875 | 6 773 | 47,3 |
| 2 048 (défaut) | 6,34 | 3 874 | 6 817 | 47,4 |
| 8 192 | 6,34 | 3 854 | 6 709 | 47,4 |
| **Lot physique** 128 (lot d'évaluation 2 048) | 6,30 | 2 837 | 4 805 | 47,5 |
| 256 | 6,33 | 3 554 | 6 177 | 47,4 |
| **512 (défaut)** | 6,40 | 3 694 | 6 530 | 47,4 |
| 1 024 | 6,54 | 3 614 | 6 590 | 47,4 |
| 2 048 | 6,81 | 3 665 | 6 115 | 47,4 |

**Au-dessous de 256, la lecture du prompt baisse de 25 à 30 %** ; au-dessus de 512 le gain est nul et la VRAM augmente (+0,4 Go à 2 048). Les valeurs par défaut sont les bonnes. *Le lot physique ne se règle que dans la fenêtre de chargement ou par le SDK.*

### 4.3 Cache K/V : en VRAM ou en RAM, quantifié ou non

*Offload KV Cache to GPU* (contexte 32 768) :

| Cache K/V | VRAM (Go) | RAM privée (Go) | Génération (tok/s) | Lecture, 5 300 jetons (tok/s) |
|---|---|---|---|---|
| Sur le GPU (défaut) | 6,60 | 7,73 | **47,4** | **6 821** |
| En RAM | 6,54 | 8,20 | 38,8 (**−18 %**) | 5 363 (**−21 %**) |

Désactiver l'offload du cache K/V ne libère que 0,06 Go de VRAM pour ce modèle (cache petit) et coûte de la vitesse. **À réserver aux cas où la VRAM manque réellement.**

*Quantification du cache K/V* (contexte 65 536, Flash Attention activée, prérequis de la quantification de V) :

| K / V | VRAM (Go) | Écart vs F16 | Génération (tok/s) | Lecture, 5 300 jetons (tok/s) | Rappel d'un code dans un texte de 26 451 et de 44 151 jetons |
|---|---|---|---|---|---|
| F16 / F16 | 7,19 | — | 47,2 | 6 406 | trouvé (2/2) |
| Q8_0 / F16 | 7,03 | −0,16 | 46,6 | 6 469 | trouvé (1/1) |
| Q8_0 / Q8_0 | 6,91 | −0,28 | 46,4 | 6 380 | trouvé (2/2) |
| Q4_0 / Q4_0 | 6,63 | **−0,56** | 46,1 | 6 334 | trouvé (2/2) |

- **Pas de perte de vitesse** et un **rappel intact** sur ce test (un code placé au milieu d'un texte répétitif) **[Vérifié, test simple]**. Ce test **ne mesure pas** la qualité sur des tâches fines (raisonnement, code) : à valider sur ses propres cas, comme le recommande l'infobulle de LM Studio.
- Le **gain est modeste** pour Gemma 4 E4B (cache réel ≈ 17 Ko par jeton). Il devient important pour les modèles à gros cache (voir qwen3.8 27B : 37 Go de RAM privée à 262 144 jetons, section 6.4).
- Un essai à contexte 65 536, cache F16 et *Flash Attention*, a produit **une fois** l'erreur « Engine protocol predict request failed: fetch failed » sur la requête de 26 451 jetons ; le moteur s'est rétabli et l'essai n'a **pas été reproduit** (deux répétitions correctes).

---

## 5. Mémoire réelle et estimation

### 5.1 Gemma 4 E4B Q8_0 : estimation contre mesure

*Estimated Memory Usage* (`lms load --estimate-only`, en Gio) contre la VRAM réellement occupée après chargement (tout le modèle sur le GPU, parallélisme 1) :

| Contexte | Estimation GPU = Total (Gio) | VRAM mesurée (Go) | Écart | RAM privée du moteur (Go) |
|---|---|---|---|---|
| 2 048 | 8,77 | 6,08 | +2,7 | 7,20 |
| 4 096 | 8,88 | 6,15 | +2,7 | 7,23 |
| 8 192 | 9,10 | 6,12 | +3,0 | 7,31 |
| 16 384 | 9,55 | 6,30 | +3,3 | 7,44 |
| 32 768 | 10,44 | 6,62 | +3,8 | 7,73 |
| 65 536 | 12,21 | 7,20 | +5,0 | 8,30 |
| 131 072 | 15,77 | 8,22 | **+7,5** | 9,42 |

- **L'estimation surestime la mémoire GPU** et l'écart **croît avec le contexte** : le cache K/V réel de Gemma 4 E4B coûte ≈ **17 Ko par jeton** (attention à fenêtre glissante) contre ≈ **57 Ko par jeton** supposés par l'estimation **[Vérifié par différence ; cause : Estimation]**. L'estimation reste **prudente** (jamais en dessous de la réalité) : elle ne risque pas de laisser charger un modèle qui ne tient pas, mais elle peut afficher « trop gros » à tort. La ligne `Confidence: LOW` de `lms load --estimate-only` le signale.
- **La RAM reste mobilisée même quand tout est sur le GPU** : ≈ **7 à 9 Go** de mémoire privée du processus `llama-server` (les embeddings par couche de Gemma 4 E4B et la copie mémoire du fichier) et ≈ **8 Go** de variation de la mémoire système **[Vérifié]**. Le contexte de 131 072 jetons tient en VRAM (8,2 Go) alors que l'estimation annonce 15,8 Go.
- La valeur « (8,40 GiB) » imprimée par `lms load` en fin de chargement est la **taille du modèle** (poids), non la mémoire consommée.

> **Avant (GPU intégré, Q4_K_M)** — estimation 6,31 Go à 2 048 jetons et 12,69 Go à 131 072 ([Manuel 03, section 5.1](03-charger-un-modele.md#51-taille-de-contexte-et-mémoire)). Les valeurs de l'**interface** (fenêtre de chargement) sur ce poste : 9,26 Go à 8 192 jetons, 10,47 Go à 32 768 ; avec 0 couche sur le GPU, la part GPU affichée tombe à 0,002 Go.

### 5.2 Modèles plus gros que la VRAM

| Modèle (contexte) | Estimation (Gio) | VRAM mesurée (Go) | RAM privée du moteur (Go) |
|---|---|---|---|
| Gemma 4 26B A4B (8 192) | 17,91 | 12,14 | 13,23 |
| Gemma 4 26B A4B (32 768) | 19,85 | 12,69 | 13,90 |
| Gemma 4 26B A4B (131 072) | 27,62 | 14,39 | 16,08 |
| Gemma 4 26B A4B (262 144) | 37,97 | 15,20 | 19,35 |
| Qwen3.8 27B (8 192) | 19,24 | 14,97 | 18,63 |
| Qwen3.8 27B (32 768) | 22,15 | 15,24 | 20,38 |
| Qwen3.8 27B (131 072) | 33,79 | 15,26 | 27,56 |
| Qwen3.8 27B (262 144) | 49,32 | 15,24 | **37,09** |

LM Studio **charge sans erreur** ces configurations avec les garde-fous en *Relaxed* : la VRAM se remplit (≈ 15 Go) et le reste va en RAM. À 262 144 jetons, Qwen3.8 27B mobilise **37 Go de RAM** (61,6 Go disponibles ici) : sur une machine de 32 Go, la même configuration serait refusée ou saturerait le système ([Manuel 01, section 6.5](01-prise-en-main.md#65-model-defaults)).

---

## 6. Modèles plus gros que la VRAM

### 6.1 Offload partiel, modèle MoE (Gemma 4 26B A4B, Q4_K_M, 17,99 Go, contexte 8 192)

| Réglage | VRAM (Go) | RAM privée (Go) | Lecture, 2 000 jetons (tok/s) | Génération (tok/s) |
|---|---|---|---|---|
| **Automatique** (sans `--gpu`) | 12,14 | 13,23 | 935 | **36,7** |
| `--gpu max` | 14,92 | 18,58 | 339 | 25,9 |
| `--gpu 0.75` | 13,64 | 14,71 | 1 197 | **43,2** |
| `--gpu 0.5` | 10,06 | 11,22 | 727 | 27,9 |
| `--gpu off` | 1,71 | 2,98 | 365 | 16,3 |

**Forcer `max` est contre-productif** : le modèle (18 Go) ne tient pas dans 16 Go ; LM Studio laisse alors la carte **déborder dans la mémoire partagée** (réglage *Limit Model Offload to Dedicated GPU Memory* désactivé, [section 6.5](#65-réglages-de-déchargement-du-matériel)), ce qui passe par le bus PCIe et ralentit la génération de 30 % (25,9 contre 36,7 tok/s). Un ratio intermédiaire (0,75) fait mieux que `max`.

### 6.2 Experts MoE sur le CPU (`--n-cpu-moe`, via le SDK)

Un modèle **MoE** n'active que quelques experts par jeton : placer les experts de **certaines couches** sur le CPU libère de la VRAM pour le reste (attention, embeddings) **sans** ralentir autant qu'un déchargement de couches entières. Option `llama.cpp` `--n-cpu-moe N` (experts des **N premières couches** sur le CPU), transmise par `llamaCppArgumentsOverride` ([Manuel 16](16-sdk-et-plugins.md)) ; contexte 8 192, `gpu: max`.

| Experts sur le CPU | VRAM (Go) | RAM privée (Go) | Lecture, 2 000 jetons (tok/s) | Génération (tok/s) |
|---|---|---|---|---|
| aucune couche (0) = `max` | 15,26 | 19,17 | 330 | 26,6 |
| **8 couches** | 14,75 | 15,71 | **1 371** | **54,6** |
| 16 couches | 11,05 | 12,01 | 804 | 42,5 |
| 30 couches (**tous** les experts, `--cpu-moe`) | 4,43 | 5,38 | 450 | 26,9 |
| *(automatique, pour mémoire)* | 12,50 | 13,84 | 924 | 37,0 |

```text
Génération (tok/s) selon le nombre de couches dont les experts vont sur le CPU
  0 (max)  ██████████████████████████ 26,6
  8        ██████████████████████████████████████████████████████ 54,6   ← meilleur
 16        ██████████████████████████████████████████ 42,5
 30 (tous) ██████████████████████████ 26,9
```

Le **meilleur compromis** (8 couches : **+ 48 % de génération et × 4 en lecture du prompt** par rapport à l'automatique et à `max`) remplit la VRAM sans la dépasser. Avec **tous** les experts sur le CPU, le modèle de 18 Go ne mobilise que **4,4 Go de VRAM** et génère encore à **27 tok/s** : utile pour garder la carte disponible pour autre chose (même vitesse que `max`). **[Vérifié sur ce modèle ; la valeur optimale de N dépend du modèle, du contexte et de la VRAM libre.]**

Avec un contexte de 65 536 jetons et 14 couches sur le CPU, le même modèle occupe **13,1 Go de VRAM** et génère à **38 tok/s** (lecture du prompt : 819 tok/s à 1 800 jetons, 1 217 tok/s à 10 600 jetons) : configuration utilisée pour les [assistants de code](13-integrations-outils-tiers.md).

### 6.3 Offload partiel, modèle dense (Qwen3.8 27B, Q4_K_M, 17,74 Go, contexte 8 192)

| Réglage | VRAM (Go) | Lecture, 2 000 jetons (tok/s) | Génération (tok/s) |
|---|---|---|---|
| Automatique | 14,97 | 524 | **18,8** |
| `--gpu max` | 15,09 | 75 | 12,2 |
| `--gpu 0.75` | 13,83 | 448 | 11,1 |
| `--gpu 0.5` | 9,98 | 313 | 6,5 |
| `--gpu off` | 1,52 | 192 | 3,3 |

Sur un modèle **dense**, chaque jeton lit **tous** les poids : toute couche laissée sur le CPU coûte cher, la génération s'effondre dès que le modèle déborde (3,3 tok/s sans GPU contre 18,8). **La répartition automatique n'est pas stable** : la même configuration (contexte 8 192) a donné 18,8 tok/s lors d'un premier chargement et **10,5 tok/s** lors de chargements suivants (lecture du prompt 70 tok/s au lieu de 524) **[Vérifié]** ; elle dépend de l'état de la mémoire au chargement. **Un modèle dense de 27 Md est à la limite d'une carte de 16 Go** ; préférer un modèle MoE, un modèle plus petit ou une quantification plus basse.

### 6.4 Grand contexte

| Modèle | Contexte | VRAM (Go) | RAM privée (Go) | Génération (tok/s) | Lecture, 5 300 jetons (tok/s) |
|---|---|---|---|---|---|
| Gemma 4 E4B Q8_0 | 8 192 | 6,21 | 7,31 | 47,4 | — |
| Gemma 4 E4B Q8_0 | 32 768 | 6,60 | 7,73 | 47,0 | 6 804 |
| Gemma 4 E4B Q8_0 | **131 072** (maximum) | 8,20 | 9,42 | 47,4 | 6 799 |
| Gemma 4 26B A4B (auto) | 32 768 | 12,69 | 13,90 | 36,6 | 1 766 |
| Gemma 4 26B A4B (auto) | 131 072 | 14,39 | 16,08 | 36,9 | 1 784 |
| Gemma 4 26B A4B (auto) | **262 144** (maximum) | 15,20 | 19,35 | 36,6 | **893** |
| Qwen3.8 27B (auto) | 32 768 | 15,24 | 20,38 | 10,6 | 88 |
| Qwen3.8 27B (auto) | 131 072 | 15,26 | 27,56 | 10,5 | 82 |
| Qwen3.8 27B (auto) | **262 144** (maximum) | 15,24 | **37,09** | 10,5 | 81 |

- **La génération ne dépend presque pas de la longueur du contexte** (47 → 47 tok/s pour 8 192 → 131 072 jetons) ; **la lecture du prompt, si** pour le modèle qui déborde (26B : 1 784 → 893 tok/s à 262 144).
- Le contexte maximal d'un petit modèle (131 072 jetons) **tient** dans la VRAM (8,2 Go), contre une estimation de 15,8 Go.
- Pour Bionic, l'ajustement automatique (*AutoFit*) a choisi **131 072 jetons** pour Gemma 4 E4B et **16 384** pour Gemma 4 26B A4B et Qwen3.8 27B sur ce poste ([Manuel Bionic 04](../bionic/04-modeles.md#5-mémoire-chargement-et-déchargement)).

### 6.5 Réglages de déchargement du matériel

*Settings → Hardware* (`Ctrl + Maj + H`) propose deux interrupteurs absents du poste à GPU intégré : **Limit Model Offload to Dedicated GPU Memory** (désactivé : « autoriser les poids à déborder dans la mémoire partagée si la mémoire dédiée est pleine ») et **Offload KV Cache to GPU Memory**. Le premier **ne modifie pas les indicateurs d'adéquation** du catalogue ([Manuel 02, section 6](02-selectionner-et-telecharger-un-modele.md#6-les-indicateurs-dadéquation-matérielle)) **[Vérifié, trois dépôts]** ; son effet sur la vitesse d'un modèle qui déborde n'a pas été isolé **[À tester]** (le ralentissement de `max` en section 6.1 suit la même logique).

---

## 7. Décodage spéculatif

### Essentiel

Le décodage spéculatif accélère la génération : un **brouillon** propose plusieurs jetons, le modèle principal les valide en une seule passe. `lms load` accepte `--speculative-draft-mtp` (tête de prédiction multi-jetons **intégrée au fichier**), `--speculative-draft-simple` avec `--speculative-draft-model` (modèle brouillon séparé), `--speculative-draft-max-tokens`, `--speculative-draft-min-tokens` et `--speculative-draft-min-continue-probability`.

| Essai | Résultat |
|---|---|
| **MTP sur Gemma 4 E4B Q8_0** | **Refusé** : « MTP speculative decoding requires a GGUF model with a bundled supported MTP head ». Le fichier installé n'embarque pas de tête MTP. |
| **MTP sur Qwen3.8 27B** (badge **MTP** dans le sélecteur de modèles) | Chargement accepté ; effet **faible et variable** (tableau ci-dessous). |
| **Brouillon séparé** : Gemma 4 26B A4B avec Gemma 4 E4B comme brouillon (`--speculative-draft-simple`) | **Dégradation : 3,6 tok/s** contre 36,7 sans brouillon (VRAM 15,2 Go au lieu de 12,5) : le brouillon est trop gros (9 Go) et déplace le modèle principal hors de la VRAM. |
| Lignes **Mtp** du catalogue (≈ 2 Go) | **Non testées** : exigent un téléchargement. |

Qwen3.8 27B, offload automatique, contexte 8 192, génération de 200 jetons (tok/s), deux répétitions par cas :

| Réglage | Prose | Code |
|---|---|---|
| Sans décodage spéculatif | 10,5 / 10,5 | 10,5 / 10,5 |
| MTP, 2 jetons de brouillon | 9,9 / 9,7 | 11,7 / 11,7 |
| MTP, 3 jetons | 8,8 / 8,7 | 11,8 / 11,7 |
| MTP, 4 jetons | 9,4 / 9,3 | **13,8** / 13,8 |
| MTP, 8 jetons | 6,2 / 6,2 | 11,6 / 10,4 |
| MTP, réglages par défaut | 8,1 / 8,2 | 10,7 / 10,8 |

### Lecture

- Le gain n'apparaît que sur du **texte prévisible** (code : jusqu'à **+ 31 %** avec 4 jetons) et le décodage spéculatif **ralentit la prose** (−11 % à −41 %). Il n'est **pas** un réglage « gratuit » ; l'activer pour un usage de code, le désactiver pour de la rédaction **[Vérifié sur ce seul modèle, partiellement déchargé]**.
- Un **brouillon séparé** doit être **petit** (≪ 1 Go à quelques Go) et partager le vocabulaire du modèle principal : un brouillon de 9 Go est contre-productif.
- La RAM augmente de 2 à 6 Go avec MTP (têtes supplémentaires et cache).
- L'effet sur un modèle **entièrement dans la VRAM**, où la génération est déjà rapide, n'a pas pu être mesuré (aucun modèle installé ne le permet sans téléchargement du brouillon) **[À tester]**.

---

## 8. Avant / après : GPU intégré et GPU dédié

Gemma 4 E4B ; **avant** : Q4_K_M (6,33 Go), GPU intégré Intel Arc 140T (Vulkan), 31 Go de RAM ; **après** : Q8_0 (9,02 Go), RTX 4060 Ti 16 Go (CUDA 12), 61,6 Go de RAM.

| Mesure | GPU intégré (avant) | GPU dédié (après) |
|---|---|---|
| Lecture du prompt, 100 % GPU, 2 100 jetons | 353 tok/s | **3 737–3 986 tok/s** |
| Génération, 100 % GPU | 14,8 tok/s | **47,1 tok/s** |
| Génération / lecture, 50 % des couches | 13,3 tok/s / 250 tok/s | 14,6 tok/s / 1 271 tok/s |
| Génération / lecture, CPU seul (réglage `off`) | 11,2 tok/s / 215 tok/s | 9,1 tok/s / 734 tok/s |
| 4 requêtes simultanées : débit total | 12,8 tok/s | **160 tok/s** |
| 4 requêtes simultanées : par requête | 3,3 tok/s | **41,2 tok/s** |
| Chargement | 15 à 20 s | 6 à 7 s |
| Temps de réponse typique d'une question courte | 4,6 s (62 jetons) | 1,5 s (61 jetons) |
| Facture fictive lue par vision (1288 px) | 25 à 37 s | 6,7 à 7,8 s |
| Conversation d'images, 3 tours | 7,5 / 15,0 / 32,6 s | 2,4 / 6,3 / 14,2 s |
| Délai avant premier jeton (flux) | 0,94 s | 0,09 à 0,13 s |

Mesures du banc d'origine rejouées par `outils/benchmark_chargement.py` (résultats : `outils/resultats/benchmark_chargement_gpu_dedie.json`).

---

## 9. Reproduire les mesures

| Script (dossier `outils/`) | Mesure |
|---|---|
| `gpu_bench.py` | Bibliothèque : chargement, VRAM / RAM, vitesse, concurrence |
| `gpu_offload_moteurs.py` | Section 2 (moteurs, couches sur le GPU) ; rétablit le moteur choisi au départ |
| `gpu_parametres_charge.py` | Sections 3 et 4 (parallélisme, Flash Attention, lots, cache K/V en RAM) |
| `gpu_sdk_params.py` | Sections 4.2, 4.3, 6.2, 7 (par le SDK) |
| `gpu_gros_modeles.py` | Sections 5.2 et 6 (modèles qui dépassent la VRAM, grand contexte) |
| `gpu_contexte_memoire.py` | Section 5.1 (mémoire réelle et estimation) |
| `gpu_decodage_specul.py` | Section 7 (MTP) |
| `benchmark_chargement.py`, `mesures_estimation_gui.py` | Banc d'origine (variable `SORTIE_JSON` pour ne pas écraser l'ancien relevé) |

Prérequis : Python 3.12, `psutil`, Node.js (SDK), LM Studio lancé, aucun autre programme gourmand en VRAM (≈ 0,7 Go sont occupés par le bureau Windows).

---

## 10. Limites

- **Une seule carte** (RTX 4060 Ti 16 Go) et un seul processeur : les valeurs absolues ne se transposent pas ; les **tendances** (surestimation de l'estimation, avantage de Flash Attention, débit parallèle, experts MoE) sont générales **[Estimation]**.
- **Quantification différente** pour la comparaison avec le GPU intégré (Q8_0 contre Q4_K_M).
- **Aucun téléchargement** : brouillon MTP, autres modèles MoE et gabarits de test n'ont pas été essayés ; le modèle « 12B QAT » des manuels Bionic n'est pas installé sur ce poste et a été remplacé par Gemma 4 26B A4B.
- Mesures **courtes** (200 jetons, une répétition) ; la température du GPU n'a pas été relevée (carte à 47 °C au repos).
- Le test de rappel du cache K/V quantifié est **élémentaire**.
