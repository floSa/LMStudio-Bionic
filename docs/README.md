# Documentation LM Studio et LM Studio Bionic

Manuels et tutoriels illustrés pour installer, configurer et utiliser **LM Studio** (inférence locale de modèles de langage) et **LM Studio Bionic** (application agent), avec des exemples sur *Gemma 4 E4B*, *Gemma 4 12B QAT* et *OlmOCR 2 7B*.

**Deux ensembles de manuels** : [LM Studio](#manuels-lm-studio) (ci-dessous) et [Bionic](#manuels-bionic) (après).

**Pour savoir où se trouve une information** : [plan détaillé des manuels LM Studio](lmstudio/plan-des-manuels.md) et [plan détaillé des manuels Bionic](bionic/plan-des-manuels.md) (une phrase par manuel, puis le contenu de chaque section, avec liens).

| | |
|---|---|
| **Version décrite** | LM Studio 0.4.25 (Build 1), Windows 11 |
| **Date des captures et mesures** | 6 octobre 2026 (manuels 00 à 09, poste à GPU intégré) ; 7 octobre 2026 (manuels 10 à 14, puis passage sur GPU dédié : manuels 15 et 16 et mises à jour des manuels 00 à 13) |
| **Postes de test** | (1) Intel Core Ultra 7 255H, 31 Go de RAM, GPU intégré Intel Arc 140T (Vulkan) ; (2) AMD Ryzen 5 9600X, 61,6 Go de RAM, **NVIDIA RTX 4060 Ti 16 Go** (CUDA 12, pilote 616.92). Les valeurs du poste (1) sont conservées entre parenthèses « GPU intégré : … » |
| **Langue de l'interface** | Anglais (les libellés sont cités tels quels) |

## Manuels LM Studio

| N° | Manuel | Contenu |
|---|---|---|
| 00 | [Notions fondamentales](lmstudio/00-notions-fondamentales.md) | Vulgarisation : taille, quantification (Q4_K_M), CPU / GPU / CUDA / Vulkan / Harmony, calcul de la RAM, contexte, vitesse |
| 01 | [Prise en main](lmstudio/01-prise-en-main.md) | Interface, raccourcis, Developer mode, réglages de l'application, stockage, points de vigilance |
| 02 | [Sélectionner et télécharger un modèle](lmstudio/02-selectionner-et-telecharger-un-modele.md) | Choisir un modèle pertinent, catalogue, quantifications et badges, import hors ligne, My Models |
| 03 | [Charger un modèle](lmstudio/03-charger-un-modele.md) | Les 21 paramètres de chargement, mémoire, mesures, réglages types |
| 04 | [Paramétrer l'inférence](lmstudio/04-parametrer-l-inference.md) | Conversation, prompt système, thinking, échantillonnage, sortie structurée, presets |
| 05 | [Vision, images et OCR](lmstudio/05-vision-images-et-ocr.md) | Images dans le chat, résolution, choix d'un modèle d'OCR (exemple OlmOCR 2), documents joints, fiabilisation |
| 06 | [Serveur local et API](lmstudio/06-serveur-local-et-api.md) | Réglages du serveur, sécurité, endpoints, exemples exécutés, JIT/TTL |
| 07 | [Ligne de commande `lms`](lmstudio/07-cli-lms.md) | Commandes, estimation mémoire, scripts |
| 08 | [Recettes par cas d'usage](lmstudio/08-recettes-par-cas-usage.md) | Fiches de configuration, dimensionnement, méthode de réglage |
| 09 | [Dépannage et FAQ](lmstudio/09-depannage-faq.md) | Diagnostic par symptôme, commandes de contrôle |
| 10 | [MCP et appel d'outils](lmstudio/10-mcp-et-appel-d-outils.md) | `mcp.json`, serveur MCP de démonstration, confirmation des appels, fiabilité des petits modèles |
| 11 | [Sécuriser le serveur local](lmstudio/11-securiser-le-serveur.md) | Niveaux d'exposition, jetons d'API et permissions, CORS, données conservées |
| 12 | [API avancée](lmstudio/12-api-avancee.md) | Chat à état, *Responses*, compatibilité Anthropic, statistiques, outils, sortie structurée, MCP par l'API |
| 13 | [Intégrations avec des outils tiers](lmstudio/13-integrations-outils-tiers.md) | Claude Code, Codex, Cline, Roo Code, Continue, Open WebUI, Aider |
| 14 | [Personnaliser les modèles](lmstudio/14-personnaliser-les-modeles.md) | Niveaux de réglage, défauts d'un modèle (effet mesuré sur l'API), gabarit de conversation, `model.yaml`, Hub, stockage des conversations, diagrammes Mermaid |
| 15 | [Performances sur GPU dédié](lmstudio/15-performances-gpu-dedie.md) | RTX 4060 Ti 16 Go : moteurs, offload, Flash Attention, lots, cache K/V, mémoire réelle et estimation, modèles plus gros que la VRAM (MoE, `--n-cpu-moe`), décodage spéculatif, contexte maximal |
| 16 | [SDK et plugins](lmstudio/16-sdk-et-plugins.md) | `@lmstudio/sdk` : paramètres de chargement absents de `lms load`, plugin `lms dev`, mode sans interface (llmster) |
| 17 | [LM Link](lmstudio/17-lm-link.md) | Utiliser les modèles d'un autre appareil : principe, mise en place, `lms link`, API, outils de code, Bionic, sécurité, essai réel sur deux machines (portable et PC fixe) : chargement, réglage et discussion avec un modèle distant ; points restant à vérifier |
| — | [Glossaire](lmstudio/annexe-glossaire.md) | Termes techniques |

## Manuels Bionic

Application agent (code, documents, recherche, voix). Version décrite : Bionic 1.1.7, Windows 11, interface en français. Index détaillé : [bionic/README.md](bionic/README.md).

| N° | Manuel | Contenu |
|---|---|---|
| 00 | [Notions fondamentales de l'agent](bionic/00-notions-agent.md) | Chat et agent, boucle d'actions, harnais, lieux d'exécution, autorisations, contexte |
| 01 | [Présentation et installation](bionic/01-presentation-installation.md) | Différences avec LM Studio, conflit entre applications, données, mises à jour |
| 02 | [L'interface](bionic/02-interface.md) | Zones, onglets, zone de saisie, panneau de droite, navigateur intégré |
| 03 | [Les réglages](bionic/03-reglages.md) | Chaque page de Paramètres, valeurs par défaut, profils |
| 04 | [Modèles](bionic/04-modeles.md) | Choisir, télécharger, régler ; effort de raisonnement ; mesures |
| 05 | [Projets et sessions](bionic/05-projets-et-sessions.md) | Dossier de travail, sessions, parallélisme, fork |
| 06 | [Documents et fichiers](bionic/06-documents.md) | Travail documentaire, images, fichiers externes |
| 07 | [Code, shell et autorisations](bionic/07-code-et-shell.md) | Scénario exécuté, modes shell, relecture, sécurité |
| 08 | [Compétences, `@`, MCP](bionic/08-competences-et-mcp.md) | Compétences, serveurs MCP |
| 09 | [Saisie vocale](bionic/09-voix.md) | Dictée locale |
| 10 | [Sécurité, compte, API locale](bionic/10-securite-compte-api.md) | Flux de données, **offres et prix (Free, Bionic+, Pro)**, crédits, LM Link, API, menaces |
| 11 | [Recettes et dépannage](bionic/11-recettes-et-depannage.md) | Fiches par cas d'usage, diagnostic |
| 12 | [Auto Review](bionic/12-auto-review.md) | Shell Judge, Shell Reviewer, niveaux de risque, instructions personnalisées, limites |
| 13 | [Compétences en pratique](bionic/13-competences-en-pratique.md) | Compétence de bout en bout : création, déclenchement avec `@`, résultat mesuré |
| 14 | [Commandes `/`, compaction, navigateur](bionic/14-commandes-compaction-navigateur.md) | Menu `/`, `/compact` mesuré, navigateur intégré et essai avec l'agent, fonctions non reproduites |
| — | [Glossaire Bionic](bionic/annexe-glossaire.md) | Termes techniques |

Limites connues de la partie Bionic : cloud, crédits, recherche web et serveurs MCP du catalogue décrits sans exécution (LM Link essayé, [manuel LM Studio 17](lmstudio/17-lm-link.md)) ; dictée vocale non exécutée ; Canvas et points de sauvegarde non reproduits ; niveau `too_destructive` d'Auto Review **non obtenu** malgré des essais destructifs réels. **Un essai (`shred` sur `~/*.txt`, modèle 26B) a été approuvé automatiquement et a détruit un fichier réel** : lire le [manuel Bionic 12](bionic/12-auto-review.md#essais-sur-des-commandes-destructives-poste-à-gpu-dédié) avant tout essai.

**Parcours conseillés (LM Studio)**

- *Découverte (novices)* : **00** → 01 → 02 → 04.
- *Maîtrise des réglages* : 00 (sections 4, 7, 9) → 03 → 09.
- *OCR de documents* : 02 → 03 → 05 → 08.
- *Intégration applicative* : 03 → 06 → 07, avec les [exemples exécutables](../exemples/).
- *Exploitation et sécurité* : 01 (section 8) → 06 (section 5) → 11 → 10.
- *Agents et outils (MCP)* : 04 → 10 → 12 → 13.
- *Assistants de code locaux* : 03 → 06 → 11 → 13.
- *Machine à GPU dédié* : 00 (section 4) → 03 (section 5) → **15** → 16.

## Conventions

- **Exemple** : les valeurs numériques « du poste de test » illustrent un principe général ; elles dépendent du modèle et de la machine.
- **Étiquettes de fiabilité** (manuel 08 et passages concernés) : **[Vérifié]** observé ou mesuré ; **[Source]** documentation officielle ; **[Estimation]** calcul à mesurer ; **[À tester]** non documenté.
- **Statut des commandes** (manuel 07) : **[Testée]** ou **[Aide]**.
- Les figures numérotées dans les captures renvoient aux tableaux qui les suivent.

## Limites connues

- **OlmOCR 2 7B** (Q4_K_M et Q8_0) a été **testé sur le poste à GPU dédié** (4 pages fictives, 100 % d'exactitude) : [Manuel 05, section 7](lmstudio/05-vision-images-et-ocr.md). Aucun scan réel ni PDF volumineux n'a été essayé.
- Les mesures de vitesse sont données **pour les deux postes** ; elles restent propres à ces deux configurations. Le comportement en concurrence est inverse (GPU intégré : pas de gain ; GPU dédié : × 3,4 avec 4 requêtes).
- **Non exécutés** : `lms get`, `lms import` (cas nominal), `lms daemon up` / `down` / `update` et l'installation de `llmster` ; quantification **Q6_K** (non installée) ; lignes « **Mtp** » du catalogue (téléchargement évité : le décodage spéculatif a été testé avec les modèles installés) ; **Roo Code** (extension sans ligne de commande) et **Open WebUI** (Docker absent, création de compte). Les jetons d'API ont été créés, testés puis supprimés ([Manuel 11](lmstudio/11-securiser-le-serveur.md)).
- Les outils tiers du [Manuel 13](lmstudio/13-integrations-outils-tiers.md) **ont été lancés** (Claude Code, Cline, Continue, Aider ; Codex connecté mais bac à sable en lecture seule) ; *Serve on Local Network* et `--bind` n'ont jamais été activés.
- **LM Studio Bionic** est documenté dans un ensemble distinct ([docs/bionic](bionic/README.md)).

## Arborescence

```text
LMStudio-Bionic/
├── docs/
│   ├── README.md                (cette page)
│   ├── lmstudio/                (manuels 00 à 17 et glossaire)
│   ├── bionic/                  (manuels Bionic 00 à 14 et glossaire)
│   └── img/                     (captures et figures : lmstudio/, bionic/)
├── exemples/                    (scripts d'API exécutables, sans dépendance)
└── outils/                      (production des captures et des mesures)
```

## Ce qui reste ouvert

- **Non traité** : quantification Q6_K (non installée) ; lignes « Mtp » (téléchargement) ; Roo Code, Open WebUI ; `lms daemon up/down/update` ; conflit LM Studio / Bionic rejoué ; test d'usage de la compétence créée par Qwen ; serveurs MCP du catalogue Bionic, dictée vocale, cloud, LM Link, recherche web (comptes ou téléchargements).
- **Décisions en attente** : télécharger un brouillon « Mtp » (≈ 2 Go) pour le décodage spéculatif ; assouplir le bac à sable de Codex (`workspace-write`) pour la comparaison ; rejouer le niveau `too_destructive` d'Auto Review dans une machine virtuelle.
- **À faire à la main** : supprimer les projets et sessions de test de Bionic (« Démo documents », « Démo code », « Démo jetable ») et les dossiers `~\.lmstudio\scratchpads\*
esume-en-trois-points`.
- **Version** : LM Studio 0.4.26 constaté le 11 octobre 2026 ; les manuels décrivent la 0.4.25 (manuel 17 : 0.4.26).
