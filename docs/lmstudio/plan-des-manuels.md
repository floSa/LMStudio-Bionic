# LM Studio : plan détaillé des manuels

Plan des 17 manuels LM Studio (00 à 16) avec, pour chacun, le contenu de chaque section. Version décrite : LM Studio 0.4.25. Retour à l'[index général](../README.md) ; termes techniques : [glossaire](annexe-glossaire.md).

**Comment lire cette page** : chaque manuel est résumé en une phrase, puis ses sections sont listées avec ce qu'elles contiennent. Un clic sur une section ouvre le passage exact.

## Sommaire rapide

| Manuel | En une phrase |
|---|---|
| [00 — Notions fondamentales](00-notions-fondamentales.md) | Vulgarisation : ce qu'est un modèle local, ce qui fait sa taille, sa vitesse et sa consommation de mémoire. |
| [01 — Prise en main](01-prise-en-main.md) | Premier tour de l'application : installation, interface, raccourcis, réglages, stockage. |
| [02 — Sélectionner et télécharger un modèle](02-selectionner-et-telecharger-un-modele.md) | Choisir un modèle adapté, comprendre les quantifications et les pastilles de compatibilité, télécharger ou importer. |
| [03 — Charger un modèle](03-charger-un-modele.md) | Les paramètres de chargement un par un, la mémoire qu'ils consomment et leur effet mesuré sur la vitesse. |
| [04 — Paramétrer l'inférence](04-parametrer-l-inference.md) | Régler la conversation : prompt système, raisonnement, échantillonnage, sortie structurée, presets. |
| [05 — Vision, images et OCR](05-vision-images-et-ocr.md) | Lire des images et des documents : réglages, choix du modèle, protocole d'extraction mesuré avec OlmOCR 2. |
| [06 — Serveur local et API](06-serveur-local-et-api.md) | Démarrer le serveur de LM Studio et l'appeler comme une API compatible OpenAI, avec des exemples exécutés. |
| [07 — Ligne de commande `lms`](07-cli-lms.md) | Piloter LM Studio au terminal : modèles, serveur, moteurs, estimation mémoire, scripts. |
| [08 — Recettes par cas d'usage](08-recettes-par-cas-usage.md) | Fiches prêtes à l'emploi : quelle machine, quel modèle, quels réglages pour une tâche donnée. |
| [09 — Dépannage et FAQ](09-depannage-faq.md) | Diagnostic par symptôme : installation, mémoire, qualité, vitesse, API, images, réseau. |
| [10 — MCP et appel d'outils](10-mcp-et-appel-d-outils.md) | Donner des outils au modèle : déclarer un serveur MCP, confirmer les appels, connaître la fiabilité réelle. |
| [11 — Sécuriser le serveur local](11-securiser-le-serveur.md) | Ce que le serveur expose et comment le protéger : niveaux d'exposition, jetons, CORS. |
| [12 — API avancée](12-api-avancee.md) | Les routes au-delà du chat simple : chat à état, Responses, compatibilité Anthropic, statistiques, outils. |
| [13 — Intégrations avec des outils tiers](13-integrations-outils-tiers.md) | Brancher des assistants de code et des interfaces sur LM Studio : réglages par outil, essais réels. |
| [14 — Personnaliser les modèles](14-personnaliser-les-modeles.md) | Défauts par modèle, gabarit de conversation, fichier `model.yaml`, Hub, stockage des conversations. |
| [15 — Performances sur GPU dédié](15-performances-gpu-dedie.md) | Toutes les mesures de la RTX 4060 Ti 16 Go, comparées au GPU intégré. |
| [16 — SDK et plugins](16-sdk-et-plugins.md) | Aller au-delà de `lms load` : kit de développement, paramètres cachés, plugin local, mode sans interface. |

---

## 00 — Notions fondamentales

**Vulgarisation : ce qu'est un modèle local, ce qui fait sa taille, sa vitesse et sa consommation de mémoire.** [Ouvrir le manuel](00-notions-fondamentales.md).

| Section | Contenu |
|---|---|
| [1. Ce que fait un modèle de langage](00-notions-fondamentales.md#1-ce-que-fait-un-modèle-de-langage) | Ce que fait un modèle de langage : prédire le mot suivant. |
| [2. La taille d'un modèle](00-notions-fondamentales.md#2-la-taille-dun-modèle) | Taille d'un modèle en milliards de paramètres et ce qu'elle change. |
| [3. Le fichier du modèle : GGUF, MLX, mmproj](00-notions-fondamentales.md#3-le-fichier-du-modèle--gguf-mlx-mmproj) | Formats de fichier : GGUF, MLX et fichier de vision `mmproj`. |
| [4. La quantification : décoder `Q4_K_M`](00-notions-fondamentales.md#4-la-quantification--décoder-q4_k_m) | Quantification : lire un nom comme `Q4_K_M` et en déduire taille et qualité. |
| [5. Le matériel : CPU, GPU, RAM, VRAM](00-notions-fondamentales.md#5-le-matériel--cpu-gpu-ram-vram) | Matériel : processeur, carte graphique, RAM, VRAM (mémoire de la carte). |
| [6. Les moteurs (runtimes) : CPU, CUDA, Vulkan, Metal, Harmony](00-notions-fondamentales.md#6-les-moteurs-runtimes--cpu-cuda-vulkan-metal-harmony) | Moteurs d'exécution (CPU, CUDA, Vulkan, Metal) et mesures sur les deux postes. |
| [7. Calculer la RAM nécessaire](00-notions-fondamentales.md#7-calculer-la-ram-nécessaire) | Calcul de la RAM nécessaire pour un modèle et un contexte donnés. |
| [8. Le contexte et le cache KV](00-notions-fondamentales.md#8-le-contexte-et-le-cache-kv) | Contexte et cache KV : pourquoi la mémoire grandit avec la longueur. |
| [9. La vitesse : tokens par seconde](00-notions-fondamentales.md#9-la-vitesse--tokens-par-seconde) | Vitesse : lecture du prompt et génération, en jetons par seconde. |
| [10. Capacités : raisonnement, vision, outils, embeddings](00-notions-fondamentales.md#10-capacités--raisonnement-vision-outils-embeddings) | Capacités : raisonnement, vision, outils, embeddings. |
| [11. Le choix du mot suivant : température et échantillonnage](00-notions-fondamentales.md#11-le-choix-du-mot-suivant--température-et-échantillonnage) | Température et échantillonnage : comment le mot suivant est choisi. |
| [12. Lexique express](00-notions-fondamentales.md#12-lexique-express) | Lexique express des termes de base. |
| [13. Parcours selon le profil](00-notions-fondamentales.md#13-parcours-selon-le-profil) | Parcours de lecture selon le profil. |

## 01 — Prise en main

**Premier tour de l'application : installation, interface, raccourcis, réglages, stockage.** [Ouvrir le manuel](01-prise-en-main.md).

| Section | Contenu |
|---|---|
| [1. Présentation](01-prise-en-main.md#1-présentation) | Présentation de LM Studio et de ce qu'il fait. |
| [2. Installation et emplacement des fichiers](01-prise-en-main.md#2-installation-et-emplacement-des-fichiers) | Installation et emplacement des fichiers sur le disque. |
| [3. Interface](01-prise-en-main.md#3-interface) | Interface : barre latérale, onglets, zones principales. |
| [4. Raccourcis clavier](01-prise-en-main.md#4-raccourcis-clavier) | Raccourcis clavier. |
| [5. Developer Mode](01-prise-en-main.md#5-developer-mode) | Developer Mode : ce qu'il débloque. |
| [6. Réglages de l'application](01-prise-en-main.md#6-réglages-de-lapplication) | Réglages de l'application, page par page, avec le matériel détecté (section Hardware). |
| [7. Stockage des données](01-prise-en-main.md#7-stockage-des-données) | Stockage des données : modèles, conversations, configuration. |
| [8. Points de vigilance](01-prise-en-main.md#8-points-de-vigilance) | Points de vigilance. |
| [9. Check-list de première configuration](01-prise-en-main.md#9-check-list-de-première-configuration) | Check-list de première configuration. |

## 02 — Sélectionner et télécharger un modèle

**Choisir un modèle adapté, comprendre les quantifications et les pastilles de compatibilité, télécharger ou importer.** [Ouvrir le manuel](02-selectionner-et-telecharger-un-modele.md).

| Section | Contenu |
|---|---|
| [1. Notions](02-selectionner-et-telecharger-un-modele.md#1-notions) | Notions utiles avant de chercher. |
| [2. Choisir un modèle pertinent](02-selectionner-et-telecharger-un-modele.md#2-choisir-un-modèle-pertinent) | Critères pour choisir un modèle pertinent. |
| [3. Model Search : le catalogue](02-selectionner-et-telecharger-un-modele.md#3-model-search--le-catalogue) | Catalogue Model Search : filtres, fiches, options de téléchargement. |
| [4. Exemple guidé avec Gemma 4 E4B](02-selectionner-et-telecharger-un-modele.md#4-exemple-guidé-avec-gemma-4-e4b) | Exemple guidé pas à pas avec Gemma 4 E4B. |
| [5. Les quantifications](02-selectionner-et-telecharger-un-modele.md#5-les-quantifications) | Quantifications : lesquelles choisir et pourquoi. |
| [6. Les indicateurs d'adéquation matérielle](02-selectionner-et-telecharger-un-modele.md#6-les-indicateurs-dadéquation-matérielle) | Pastilles d'adéquation matérielle (vert, bleu, rouge) et seuils mesurés. |
| [7. Télécharger](02-selectionner-et-telecharger-un-modele.md#7-télécharger) | Télécharger un modèle. |
| [8. Installer un modèle sans connexion](02-selectionner-et-telecharger-un-modele.md#8-installer-un-modèle-sans-connexion) | Installer un modèle hors connexion (import de fichier). |
| [9. Suivre les téléchargements](02-selectionner-et-telecharger-un-modele.md#9-suivre-les-téléchargements) | Suivre les téléchargements. |
| [10. Organisation des fichiers et modèles installés](02-selectionner-et-telecharger-un-modele.md#10-organisation-des-fichiers-et-modèles-installés) | Organisation des fichiers et des modèles installés. |
| [11. Charger un modèle : le sélecteur](02-selectionner-et-telecharger-un-modele.md#11-charger-un-modèle--le-sélecteur) | Charger un modèle depuis le sélecteur. |
| [12. Check-list de choix](02-selectionner-et-telecharger-un-modele.md#12-check-list-de-choix) | Check-list de choix. |

## 03 — Charger un modèle

**Les paramètres de chargement un par un, la mémoire qu'ils consomment et leur effet mesuré sur la vitesse.** [Ouvrir le manuel](03-charger-un-modele.md).

| Section | Contenu |
|---|---|
| [1. Principe : ce que « charger » signifie](03-charger-un-modele.md#1-principe--ce-que--charger--signifie) | Ce que « charger » signifie. |
| [2. Composition de la mémoire](03-charger-un-modele.md#2-composition-de-la-mémoire) | Composition de la mémoire : poids, cache KV, calculs. |
| [3. Ouvrir la fenêtre de chargement](03-charger-un-modele.md#3-ouvrir-la-fenêtre-de-chargement) | Ouvrir la fenêtre de chargement. |
| [4. Référence des paramètres](03-charger-un-modele.md#4-référence-des-paramètres) | Référence des paramètres : rôle, valeur par défaut, risque. |
| [5. Effets mesurés](03-charger-un-modele.md#5-effets-mesurés) | Effets mesurés : contexte, offload GPU, Flash Attention, cache K/V, vitesse, concurrence. |
| [6. Réglages types par cas d'usage](03-charger-un-modele.md#6-réglages-types-par-cas-dusage) | Réglages types par cas d'usage. |
| [7. Mémoriser, automatiser, décharger](03-charger-un-modele.md#7-mémoriser-automatiser-décharger) | Mémoriser, automatiser, décharger. |
| [8. Dépannage](03-charger-un-modele.md#8-dépannage) | Dépannage du chargement. |

## 04 — Paramétrer l'inférence

**Régler la conversation : prompt système, raisonnement, échantillonnage, sortie structurée, presets.** [Ouvrir le manuel](04-parametrer-l-inference.md).

| Section | Contenu |
|---|---|
| [1. Principe : paramètres de chargement et d'inférence](04-parametrer-l-inference.md#1-principe--paramètres-de-chargement-et-dinférence) | Paramètres de chargement contre paramètres d'inférence. |
| [2. Premier échange et lecture de l'interface](04-parametrer-l-inference.md#2-premier-échange-et-lecture-de-linterface) | Premier échange et lecture de l'interface de chat. |
| [3. Gérer les conversations](04-parametrer-l-inference.md#3-gérer-les-conversations) | Gérer les conversations. |
| [4. Le panneau de paramètres](04-parametrer-l-inference.md#4-le-panneau-de-paramètres) | Panneau de paramètres. |
| [5. Prompt système](04-parametrer-l-inference.md#5-prompt-système) | Prompt système. |
| [6. Raisonnement (thinking)](04-parametrer-l-inference.md#6-raisonnement-thinking) | Raisonnement (thinking) : activer, limiter, lire. |
| [7. Paramètres de génération et d'échantillonnage](04-parametrer-l-inference.md#7-paramètres-de-génération-et-déchantillonnage) | Température, Top P, Top K, pénalités, graine. |
| [8. Sortie structurée](04-parametrer-l-inference.md#8-sortie-structurée) | Sortie structurée (JSON conforme à un schéma). |
| [9. Presets](04-parametrer-l-inference.md#9-presets) | Presets : enregistrer et réutiliser un jeu de réglages. |
| [10. Réglages types par cas d'usage](04-parametrer-l-inference.md#10-réglages-types-par-cas-dusage) | Réglages types par cas d'usage. |
| [11. Mesures de l'effet des paramètres](04-parametrer-l-inference.md#11-mesures-de-leffet-des-paramètres) | Mesures de l'effet des paramètres. |
| [12. Dépannage](04-parametrer-l-inference.md#12-dépannage) | Dépannage. |

## 05 — Vision, images et OCR

**Lire des images et des documents : réglages, choix du modèle, protocole d'extraction mesuré avec OlmOCR 2.** [Ouvrir le manuel](05-vision-images-et-ocr.md).

| Section | Contenu |
|---|---|
| [1. Principe : comment un modèle « voit » une image](05-vision-images-et-ocr.md#1-principe--comment-un-modèle--voit--une-image) | Comment un modèle « voit » une image. |
| [2. Prérequis d'un modèle de vision](05-vision-images-et-ocr.md#2-prérequis-dun-modèle-de-vision) | Prérequis d'un modèle de vision. |
| [3. Joindre une image dans le chat](05-vision-images-et-ocr.md#3-joindre-une-image-dans-le-chat) | Joindre une image dans le chat. |
| [4. Résolution : le facteur décisif](05-vision-images-et-ocr.md#4-résolution--le-facteur-décisif) | Résolution : le facteur décisif de la qualité. |
| [5. Réglages recommandés pour l'OCR](05-vision-images-et-ocr.md#5-réglages-recommandés-pour-locr) | Réglages recommandés pour l'OCR (reconnaissance de texte). |
| [6. Choisir un modèle pour lire des images](05-vision-images-et-ocr.md#6-choisir-un-modèle-pour-lire-des-images) | Choisir un modèle pour lire des images. |
| [7. Exemple : un modèle d'OCR dédié, OlmOCR 2 7B](05-vision-images-et-ocr.md#7-exemple--un-modèle-docr-dédié-olmocr-2-7b) | OlmOCR 2 7B : procédure et résultats mesurés (4 pages fictives, exactitude, mémoire). |
| [8. Joindre un document (texte, PDF)](05-vision-images-et-ocr.md#8-joindre-un-document-texte-pdf) | Joindre un document texte ou PDF. |
| [9. Utiliser la vision par l'API](05-vision-images-et-ocr.md#9-utiliser-la-vision-par-lapi) | Vision par l'API. |
| [10. Fiabiliser une extraction](05-vision-images-et-ocr.md#10-fiabiliser-une-extraction) | Fiabiliser une extraction. |
| [11. Limites](05-vision-images-et-ocr.md#11-limites) | Limites. |
| [12. Dépannage](05-vision-images-et-ocr.md#12-dépannage) | Dépannage. |

## 06 — Serveur local et API

**Démarrer le serveur de LM Studio et l'appeler comme une API compatible OpenAI, avec des exemples exécutés.** [Ouvrir le manuel](06-serveur-local-et-api.md).

| Section | Contenu |
|---|---|
| [1. Principe](06-serveur-local-et-api.md#1-principe) | Principe du serveur local. |
| [2. Démarrer et arrêter le serveur](06-serveur-local-et-api.md#2-démarrer-et-arrêter-le-serveur) | Démarrer et arrêter le serveur. |
| [3. La page Developer](06-serveur-local-et-api.md#3-la-page-developer) | Page Developer. |
| [4. Réglages du serveur](06-serveur-local-et-api.md#4-réglages-du-serveur) | Réglages du serveur. |
| [5. Sécurité](06-serveur-local-et-api.md#5-sécurité) | Sécurité de base. |
| [6. Les endpoints](06-serveur-local-et-api.md#6-les-endpoints) | Endpoints disponibles. |
| [7. Appeler l'API : exemples exécutés](06-serveur-local-et-api.md#7-appeler-lapi--exemples-exécutés) | Appels d'API exécutés, avec résultats. |
| [8. Paramètres et valeurs par défaut](06-serveur-local-et-api.md#8-paramètres-et-valeurs-par-défaut) | Paramètres et valeurs par défaut. |
| [9. Chargement des modèles, JIT et TTL](06-serveur-local-et-api.md#9-chargement-des-modèles-jit-et-ttl) | Chargement à la demande (JIT) et durée de vie (TTL). |
| [10. Journaux](06-serveur-local-et-api.md#10-journaux) | Journaux. |
| [11. Dépannage](06-serveur-local-et-api.md#11-dépannage) | Dépannage. |

## 07 — Ligne de commande `lms`

**Piloter LM Studio au terminal : modèles, serveur, moteurs, estimation mémoire, scripts.** [Ouvrir le manuel](07-cli-lms.md).

| Section | Contenu |
|---|---|
| [1. Présentation](07-cli-lms.md#1-présentation) | Présentation de la commande `lms`. |
| [2. Vue d'ensemble des commandes](07-cli-lms.md#2-vue-densemble-des-commandes) | Vue d'ensemble des commandes et limites constatées. |
| [3. Modèles : lister, charger, décharger](07-cli-lms.md#3-modèles--lister-charger-décharger) | Lister, charger, décharger un modèle ; estimation mémoire sans chargement. |
| [4. Serveur local](07-cli-lms.md#4-serveur-local) | Serveur local. |
| [5. Conversation en ligne de commande](07-cli-lms.md#5-conversation-en-ligne-de-commande) | Conversation en ligne de commande. |
| [6. Moteurs d'inférence (runtime)](07-cli-lms.md#6-moteurs-dinférence-runtime) | Moteurs d'inférence. |
| [7. Télécharger et importer des modèles](07-cli-lms.md#7-télécharger-et-importer-des-modèles) | Télécharger et importer des modèles. |
| [8. Journaux](07-cli-lms.md#8-journaux) | Journaux. |
| [9. Mode sans interface : `llmster`](07-cli-lms.md#9-mode-sans-interface--llmster) | Mode sans interface (`llmster`). |
| [10. Scripts et automatisation](07-cli-lms.md#10-scripts-et-automatisation) | Scripts et automatisation. |
| [11. Dépannage](07-cli-lms.md#11-dépannage) | Dépannage. |

## 08 — Recettes par cas d'usage

**Fiches prêtes à l'emploi : quelle machine, quel modèle, quels réglages pour une tâche donnée.** [Ouvrir le manuel](08-recettes-par-cas-usage.md).

| Section | Contenu |
|---|---|
| [1. Dimensionner la machine](08-recettes-par-cas-usage.md#1-dimensionner-la-machine) | Dimensionner la machine. |
| [2. Tableau de synthèse](08-recettes-par-cas-usage.md#2-tableau-de-synthèse) | Tableau de synthèse des recettes. |
| [3. Fiches](08-recettes-par-cas-usage.md#3-fiches) | Fiches détaillées par cas d'usage. |
| [4. Prompts types](08-recettes-par-cas-usage.md#4-prompts-types) | Prompts types. |
| [5. Méthode de réglage](08-recettes-par-cas-usage.md#5-méthode-de-réglage) | Méthode de réglage pas à pas. |

## 09 — Dépannage et FAQ

**Diagnostic par symptôme : installation, mémoire, qualité, vitesse, API, images, réseau.** [Ouvrir le manuel](09-depannage-faq.md).

| Section | Contenu |
|---|---|
| [1. Méthode de diagnostic](09-depannage-faq.md#1-méthode-de-diagnostic) | Méthode de diagnostic. |
| [2. Commandes de contrôle](09-depannage-faq.md#2-commandes-de-contrôle) | Commandes de contrôle. |
| [3. Installation, lancement, mises à jour](09-depannage-faq.md#3-installation-lancement-mises-à-jour) | Installation, lancement, mises à jour. |
| [4. Modèles et téléchargements](09-depannage-faq.md#4-modèles-et-téléchargements) | Modèles et téléchargements. |
| [5. Chargement et mémoire](09-depannage-faq.md#5-chargement-et-mémoire) | Chargement et mémoire. |
| [6. Qualité des réponses](09-depannage-faq.md#6-qualité-des-réponses) | Qualité des réponses. |
| [7. Performances](09-depannage-faq.md#7-performances) | Performances. |
| [8. Serveur et API](09-depannage-faq.md#8-serveur-et-api) | Serveur et API. |
| [9. Images, OCR, documents](09-depannage-faq.md#9-images-ocr-documents) | Images, OCR, documents. |
| [10. Réseau, sécurité, données](09-depannage-faq.md#10-réseau-sécurité-données) | Réseau, sécurité, données. |
| [11. FAQ](09-depannage-faq.md#11-faq) | Questions fréquentes. |
| [12. Informations à joindre à une demande de support](09-depannage-faq.md#12-informations-à-joindre-à-une-demande-de-support) | Informations à joindre à une demande de support. |

## 10 — MCP et appel d'outils

**Donner des outils au modèle : déclarer un serveur MCP, confirmer les appels, connaître la fiabilité réelle.** [Ouvrir le manuel](10-mcp-et-appel-d-outils.md).

| Section | Contenu |
|---|---|
| [1. Principe](10-mcp-et-appel-d-outils.md#1-principe) | Principe de l'appel d'outil et du protocole MCP. |
| [2. Déclarer un serveur MCP : `mcp.json`](10-mcp-et-appel-d-outils.md#2-déclarer-un-serveur-mcp--mcpjson) | Déclarer un serveur dans `mcp.json`. |
| [3. Un serveur MCP minimal pour tester](10-mcp-et-appel-d-outils.md#3-un-serveur-mcp-minimal-pour-tester) | Serveur MCP minimal de démonstration. |
| [4. Utiliser les outils dans le chat](10-mcp-et-appel-d-outils.md#4-utiliser-les-outils-dans-le-chat) | Utiliser les outils dans le chat. |
| [5. Confirmer, refuser, autoriser](10-mcp-et-appel-d-outils.md#5-confirmer-refuser-autoriser) | Confirmer, refuser, autoriser un appel. |
| [6. Fiabilité et limites des petits modèles](10-mcp-et-appel-d-outils.md#6-fiabilité-et-limites-des-petits-modèles) | Fiabilité et limites des petits modèles (mesures). |
| [7. Serveurs distants, authentification et partage](10-mcp-et-appel-d-outils.md#7-serveurs-distants-authentification-et-partage) | Serveurs distants, authentification, partage. |
| [8. Dépannage](10-mcp-et-appel-d-outils.md#8-dépannage) | Dépannage. |

## 11 — Sécuriser le serveur local

**Ce que le serveur expose et comment le protéger : niveaux d'exposition, jetons, CORS.** [Ouvrir le manuel](11-securiser-le-serveur.md).

| Section | Contenu |
|---|---|
| [1. Principe : ce que le serveur expose](11-securiser-le-serveur.md#1-principe--ce-que-le-serveur-expose) | Ce que le serveur expose. |
| [2. Trois niveaux d'exposition](11-securiser-le-serveur.md#2-trois-niveaux-dexposition) | Trois niveaux d'exposition. |
| [3. Authentification et jetons](11-securiser-le-serveur.md#3-authentification-et-jetons) | Authentification et jetons d'API. |
| [4. Permissions des jetons et MCP](11-securiser-le-serveur.md#4-permissions-des-jetons-et-mcp) | Permissions des jetons et MCP. |
| [5. CORS](11-securiser-le-serveur.md#5-cors) | CORS (autorisation d'appel depuis une page web). |
| [6. Ce qu'il ne faut pas exposer](11-securiser-le-serveur.md#6-ce-quil-ne-faut-pas-exposer) | Ce qu'il ne faut pas exposer. |
| [7. Check-list et vérifications](11-securiser-le-serveur.md#7-check-list-et-vérifications) | Check-list et vérifications. |
| [8. Dépannage](11-securiser-le-serveur.md#8-dépannage) | Dépannage. |

## 12 — API avancée

**Les routes au-delà du chat simple : chat à état, Responses, compatibilité Anthropic, statistiques, outils.** [Ouvrir le manuel](12-api-avancee.md).

| Section | Contenu |
|---|---|
| [1. Panorama des routes](12-api-avancee.md#1-panorama-des-routes) | Panorama des routes. |
| [2. Chat à état : `/api/v1/chat`](12-api-avancee.md#2-chat-à-état--apiv1chat) | Chat à état (`/api/v1/chat`). |
| [3. API *Responses* : `/v1/responses`](12-api-avancee.md#3-api-responses--v1responses) | API Responses (`/v1/responses`). |
| [4. Compatibilité Anthropic : `/v1/messages`](12-api-avancee.md#4-compatibilité-anthropic--v1messages) | Compatibilité Anthropic (`/v1/messages`). |
| [5. Statistiques de génération et flux](12-api-avancee.md#5-statistiques-de-génération-et-flux) | Statistiques de génération et flux. |
| [6. Appel d'outils par l'API](12-api-avancee.md#6-appel-doutils-par-lapi) | Appel d'outils par l'API. |
| [7. Sortie structurée](12-api-avancee.md#7-sortie-structurée) | Sortie structurée. |
| [8. MCP par l'API](12-api-avancee.md#8-mcp-par-lapi) | MCP par l'API. |
| [9. Raisonnement et options de `/api/v1/chat`](12-api-avancee.md#9-raisonnement-et-options-de-apiv1chat) | Raisonnement et options du chat à état. |
| [10. Dépannage](12-api-avancee.md#10-dépannage) | Dépannage. |

## 13 — Intégrations avec des outils tiers

**Brancher des assistants de code et des interfaces sur LM Studio : réglages par outil, essais réels.** [Ouvrir le manuel](13-integrations-outils-tiers.md).

| Section | Contenu |
|---|---|
| [1. Principe](13-integrations-outils-tiers.md#1-principe) | Principe de l'intégration. |
| [2. Réglages par outil](13-integrations-outils-tiers.md#2-réglages-par-outil) | Réglages outil par outil (Claude Code, Codex, Cline, Roo Code, Continue, Open WebUI, Aider). |
| [3. Comportement avec l'authentification](13-integrations-outils-tiers.md#3-comportement-avec-lauthentification) | Comportement avec l'authentification activée. |
| [4. Vérification par simulation](13-integrations-outils-tiers.md#4-vérification-par-simulation) | Vérification par simulation des requêtes. |
| [4 bis. Essais réels (7 octobre 2026)](13-integrations-outils-tiers.md#4-bis-essais-réels-7-octobre-2026) | Essais réels des outils sur GPU dédié. |
| [5. Modèle et contexte pour les outils de code](13-integrations-outils-tiers.md#5-modèle-et-contexte-pour-les-outils-de-code) | Choisir modèle et contexte pour les outils de code. |
| [6. Dépannage](13-integrations-outils-tiers.md#6-dépannage) | Dépannage. |

## 14 — Personnaliser les modèles

**Défauts par modèle, gabarit de conversation, fichier `model.yaml`, Hub, stockage des conversations.** [Ouvrir le manuel](14-personnaliser-les-modeles.md).

| Section | Contenu |
|---|---|
| [1. Qui l'emporte : les niveaux de réglage](14-personnaliser-les-modeles.md#1-qui-lemporte--les-niveaux-de-réglage) | Qui l'emporte entre les niveaux de réglage. |
| [2. Les défauts d'un modèle](14-personnaliser-les-modeles.md#2-les-défauts-dun-modèle) | Défauts d'un modèle. |
| [3. Le gabarit de conversation (chat template)](14-personnaliser-les-modeles.md#3-le-gabarit-de-conversation-chat-template) | Gabarit de conversation (chat template). |
| [4. `model.yaml` et modèles virtuels](14-personnaliser-les-modeles.md#4-modelyaml-et-modèles-virtuels) | `model.yaml` et modèles virtuels. |
| [5. Le Hub](14-personnaliser-les-modeles.md#5-le-hub) | Hub de la communauté. |
| [6. Les conversations : stockage et diagrammes](14-personnaliser-les-modeles.md#6-les-conversations--stockage-et-diagrammes) | Stockage des conversations et diagrammes. |
| [7. Dépannage](14-personnaliser-les-modeles.md#7-dépannage) | Dépannage. |

## 15 — Performances sur GPU dédié

**Toutes les mesures de la RTX 4060 Ti 16 Go, comparées au GPU intégré.** [Ouvrir le manuel](15-performances-gpu-dedie.md).

| Section | Contenu |
|---|---|
| [0. Poste, modèles et méthode](15-performances-gpu-dedie.md#0-poste-modèles-et-méthode) | Poste, modèles et méthode de mesure. |
| [1. Ce qu'il faut retenir](15-performances-gpu-dedie.md#1-ce-quil-faut-retenir) | Les résultats à retenir, en bref. |
| [2. Moteurs et nombre de couches sur le GPU](15-performances-gpu-dedie.md#2-moteurs-et-nombre-de-couches-sur-le-gpu) | Moteurs et nombre de couches sur le GPU. |
| [3. Parallélisme : le débit total augmente](15-performances-gpu-dedie.md#3-parallélisme--le-débit-total-augmente) | Parallélisme : le débit total augmente. |
| [4. Flash Attention, lots et cache K/V](15-performances-gpu-dedie.md#4-flash-attention-lots-et-cache-kv) | Flash Attention, lots et cache K/V. |
| [5. Mémoire réelle et estimation](15-performances-gpu-dedie.md#5-mémoire-réelle-et-estimation) | Mémoire réelle contre estimation. |
| [6. Modèles plus gros que la VRAM](15-performances-gpu-dedie.md#6-modèles-plus-gros-que-la-vram) | Modèles plus gros que la VRAM : offload partiel, experts MoE sur le CPU. |
| [7. Décodage spéculatif](15-performances-gpu-dedie.md#7-décodage-spéculatif) | Décodage spéculatif (MTP, modèle brouillon). |
| [8. Avant / après : GPU intégré et GPU dédié](15-performances-gpu-dedie.md#8-avant--après--gpu-intégré-et-gpu-dédié) | Avant / après : GPU intégré et GPU dédié. |
| [9. Reproduire les mesures](15-performances-gpu-dedie.md#9-reproduire-les-mesures) | Reproduire les mesures. |
| [10. Limites](15-performances-gpu-dedie.md#10-limites) | Limites. |

## 16 — SDK et plugins

**Aller au-delà de `lms load` : kit de développement, paramètres cachés, plugin local, mode sans interface.** [Ouvrir le manuel](16-sdk-et-plugins.md).

| Section | Contenu |
|---|---|
| [1. Choisir entre API, SDK et plugin](16-sdk-et-plugins.md#1-choisir-entre-api-sdk-et-plugin) | Choisir entre API, SDK et plugin. |
| [2. Le SDK JavaScript](16-sdk-et-plugins.md#2-le-sdk-javascript) | SDK JavaScript : installation et premiers appels. |
| [3. Paramètres de chargement accessibles par le SDK](16-sdk-et-plugins.md#3-paramètres-de-chargement-accessibles-par-le-sdk) | Paramètres de chargement accessibles par le SDK. |
| [4. Écrire un plugin](16-sdk-et-plugins.md#4-écrire-un-plugin) | Écrire un plugin (`lms dev`). |
| [5. Le mode sans interface : llmster](16-sdk-et-plugins.md#5-le-mode-sans-interface--llmster) | Mode sans interface (llmster). |
| [6. Pièges constatés](16-sdk-et-plugins.md#6-pièges-constatés) | Pièges constatés. |

---

## Par où commencer

- **Débutant** : 00 → 01 → 02 → 04.
- **Régler la mémoire et la vitesse** : 00 (sections 4, 7, 9) → 03 → 15 (si carte graphique dédiée).
- **OCR de documents** : 02 → 03 → 05 → 08.
- **Développeur / API** : 06 → 12 → 07 → 16, puis 10 pour les outils.
- **Sécurité** : 06 (section 5) → 11 → 10 (section 5).
- **En cas de problème** : 09, puis le dépannage du manuel concerné.
- **Brancher un assistant de code** : 03 → 06 → 13.
