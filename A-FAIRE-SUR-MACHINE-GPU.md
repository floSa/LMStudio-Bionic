# À faire sur une machine avec GPU dédié

> Liste de contrôle pour compléter les manuels après import du projet. Le poste de production n'avait **pas de GPU dédié** (Intel Core Ultra 7 255H, 31 Go de RAM, GPU intégré, moteur Vulkan) : toutes les mesures de vitesse et de mémoire des manuels viennent de cette configuration.
> Suivi complet des demandes : [NOTES-EVOLUTIONS.md](NOTES-EVOLUTIONS.md) (points 1, 8, 9, 10, 11, 12). Dernière mise à jour : 7 octobre 2026.
>
> **Passage du 7 octobre 2026 effectué** sur un poste à GPU dédié (AMD Ryzen 5 9600X, 61,6 Go de RAM, NVIDIA RTX 4060 Ti 16 Go, pilote 616.92, CUDA 13.4 ; LM Studio 0.4.25, Bionic 1.1.7) avec **les modèles déjà installés** (*Gemma 4 E4B* en Q8_0, *Gemma 4 26B A4B*, *Qwen3.8 27B*, OlmOCR 2 7B Q4_K_M et Q8_0), **sans téléchargement ni compte**. Les cases ci-dessous indiquent ce qui est fait ; les cases non cochées expliquent pourquoi. **Compléments du même jour** : MCP ajouté et appelé dans Bionic, Code Review, compaction automatique, sessions simultanées, modes shell extrêmes, minimum AutoFit (manuels Bionic 04, 05, 07, 08, 14). **Reste à faire à la main** : supprimer les projets et sessions de test de Bionic (« Démo documents », « Démo code », « Démo jetable »), vérifier le dossier personnel après l'incident décrit au [Manuel Bionic 12](docs/bionic/12-auto-review.md#essais-sur-des-commandes-destructives-poste-à-gpu-dédié).

## 0. Préparation

1. Copier le dossier `EDF` **hors de OneDrive** si possible (milliers de fichiers dans les dossiers d'images et d'environnement).
2. Installer LM Studio **0.4.25** (même version que les manuels ; noter toute différence) et télécharger *Gemma 4 E4B* (Q4_K_M, 6,33 Go). *Gemma 4 12B QAT* (7,15 Go) pour les essais Bionic.
3. Python 3.12, environnement virtuel avec `websocket-client` et `pillow` ([outils/README.md](outils/README.md)).
4. Relever la configuration : GPU, VRAM, pilote, RAM, système ; **Hardware** (`Ctrl + Maj + H`) → comparer à la section 6 du [Manuel 01](docs/lmstudio/01-prise-en-main.md).
5. **Ne jamais ouvrir LM Studio et Bionic en même temps.** Ne rien publier, ne se connecter à aucun compte pour ces essais.

## 1. Badges d'adéquation (priorité 1)

Objet : [Manuel 02, section 6](docs/lmstudio/02-selectionner-et-telecharger-un-modele.md#6-les-indicateurs-dadéquation-matérielle).

- [x] Rouvrir *Model Search* → dépôt `unsloth/gemma-4-E4B-it-GGUF` → liste *Download Options* (lecture seule, **sans cliquer sur Download**) : relever la couleur de chaque ligne (de `UD-IQ2_M` à `BF16`). **Fait (7 octobre 2026)** : 8 dépôts relevés (≈ 240 fichiers) : [Manuel 02, section 6](docs/lmstudio/02-selectionner-et-telecharger-un-modele.md#6-les-indicateurs-dadéquation-matérielle) ; résultats bruts `outils/resultats/gpu_badges_*.json`.
- [x] Même relevé avec un modèle plus gros (par exemple *Gemma 4 26B A4B*) pour trouver les seuils vert / bleu / rouge **selon la VRAM**. **Fait (7 octobre 2026)** : vert → bleu entre 14,5 et 14,8 Go (≈ 91–93 % de la VRAM), bleu → rouge entre 59,1 et 60,5 Go (≈ 96–98 % de la RAM seule).
- [x] Vérifier si la couleur change avec le **contexte par défaut** (*Settings → Model Defaults*). **Fait (7 octobre 2026)** : aucun effet du contexte par défaut, des garde-fous ni de « Limit Model Offload ».
- [x] Capturer les trois états sur la machine GPU et **remplacer** la figure 5 du manuel 02 ; corriger les phrases « sur ce poste, GPU intégré » et la sous-section « Ce qui a été mesuré ». **Fait (7 octobre 2026)** : figure 5 régénérée (`outils/captures/capture_02b_badges_gpu_dedie.py`), textes corrigés.
- [x] Comparer l'estimation affichée avec la consommation réelle (`lms load --estimate-only` puis `Get-Process`, ou le moniteur de ressources de LM Studio) : consigner l'écart. **Fait (7 octobre 2026)** : l'estimation **surestime** de +2,7 à +7,5 Go ; [Manuel 15, section 5](docs/lmstudio/15-performances-gpu-dedie.md#5-mémoire-réelle-et-estimation).

## 2. Offload et moteurs (priorité 2)

Objet : [Manuel 03](docs/lmstudio/03-charger-un-modele.md) (sections 5.3 à 5.5) et [Manuel 00, section 6](docs/lmstudio/00-notions-fondamentales.md#6-les-moteurs-runtimes--cpu-cuda-vulkan-metal-harmony).

- [x] Rejouer [outils/benchmark_chargement.py](outils/benchmark_chargement.py) : vitesse de génération et de traitement du prompt selon le nombre de couches sur GPU (0, moitié, maximum) et selon le moteur (**CUDA**, **Vulkan**, CPU). **Fait (7 octobre 2026)** : [Manuel 15, section 2](docs/lmstudio/15-performances-gpu-dedie.md#2-moteurs-et-nombre-de-couches-sur-le-gpu) (CUDA 3 746 / Vulkan 2 659 / CPU 49 tok/s de prompt).
- [x] Rejouer [outils/mesures_estimation_gui.py](outils/mesures_estimation_gui.py) : l'estimation de mémoire change-t-elle avec un GPU dédié ? **Fait (7 octobre 2026)** : [Manuel 03, section 5.2](docs/lmstudio/03-charger-un-modele.md).
- [x] **Parallélisme** (*Max Concurrent Predictions*) : le gain de débit absent sur GPU intégré existe-t-il ? Mettre à jour [Manuel 03, section 5.5](docs/lmstudio/03-charger-un-modele.md#55-concurrence-sur-gpu-intégré). **Fait (7 octobre 2026)** : le gain existe (45 → 264 tok/s pour 1 → 8 requêtes) ; section 5.5 renommée « Concurrence selon le matériel ».
- [x] Effet de **Flash Attention**, de la **quantification du cache K/V** et de **Physical Batch Size** sur vitesse et mémoire. **Fait (7 octobre 2026)** : [Manuel 15, section 4](docs/lmstudio/15-performances-gpu-dedie.md#4-flash-attention-lots-et-cache-kv).
- [x] Gros contexte : charger *Gemma 4 12B QAT* à 8 192 puis à 262 144 tokens ; relever la VRAM et la RAM ([Manuel Bionic 04](docs/bionic/04-modeles.md) : 14,1 Go de RAM mesurés sur le poste de test). **Fait (7 octobre 2026)** : le *12B QAT* est absent du poste : *Gemma 4 26B A4B* (262 144 jetons : 15,2 Go de VRAM + 19 Go de RAM) et *Qwen3.8 27B* (37 Go de RAM).
- [x] Modèle à experts (MoE) avec experts forcés sur CPU, si la VRAM est insuffisante. **Fait (7 octobre 2026)** : `--n-cpu-moe 8` : 54,6 tok/s contre 36,7 en automatique ([Manuel 15, section 6.2](docs/lmstudio/15-performances-gpu-dedie.md#62-experts-moe-sur-le-cpu---n-cpu-moe-via-le-sdk)).
- [ ] Décodage spéculatif : les lignes « Mtp » des listes de téléchargement ([Manuel 02, section 4](docs/lmstudio/02-selectionner-et-telecharger-un-modele.md#4-exemple-guidé-avec-gemma-4-e4b)) servent-elles de modèle brouillon ? Gain mesuré. **Non fait (7 octobre 2026)** : MTP intégré testé sur Qwen (code jusqu'à +31 %, prose −11 à −41 %) et brouillon E4B pour le 26B (dégradation à 3,6 tok/s) ; les **lignes « Mtp » du catalogue n'ont pas été téléchargées** (consigne : aucun téléchargement de modèle).

## 3. Reprise des vitesses annoncées

Remplacer, **en conservant l'ancienne valeur entre parenthèses** (« GPU intégré : … »), les chiffres suivants :

- [x] Manuels [03](docs/lmstudio/03-charger-un-modele.md) et [04](docs/lmstudio/04-parametrer-l-inference.md) : tok/s, TTFT, durées de chargement, mesures de l'effet des paramètres. **Fait (7 octobre 2026)** : manuels 03, 04 et 15.
- [x] Manuel [05](docs/lmstudio/05-vision-images-et-ocr.md) : durée de la facture (25 à 37 s), jetons par seconde, conversation multi-tours (7,5 / 15,0 / 32,6 s). **Fait (7 octobre 2026)** : facture, conversation multi-tours (2,4 / 6,3 / 14,2 s) et protocole OlmOCR.
- [x] Manuels [06](docs/lmstudio/06-serveur-local-et-api.md), [10](docs/lmstudio/10-mcp-et-appel-d-outils.md), [12](docs/lmstudio/12-api-avancee.md) : latences de l'API et de l'appel d'outils (rejouer [outils/experiences_api.py](outils/experiences_api.py), `experiences_api_lot2.py`, `mesure_outils_fiabilite.py`). **Fait (7 octobre 2026)** : bancs rejoués, résultats dans `outils/resultats/gpu_dedie/`.
- [x] Manuels Bionic [05](docs/bionic/05-projets-et-sessions.md) à [07](docs/bionic/07-code-et-shell.md), [11](docs/bionic/11-recettes-et-depannage.md) et [14](docs/bionic/14-commandes-compaction-navigateur.md) : durées de tâches (mémo 2 min 4 s, facture, bogue de code 6 min 22 s / 4 min 50 s, `/compact` ≈ 90 s). **Fait (7 octobre 2026)** : durées mesurées avec le modèle réel vérifié dans la base de sessions ; *Gemma 4 26B A4B* remplace le *12B QAT* (absent).
- [x] [Manuel Bionic 14, section 4](docs/bionic/14-commandes-compaction-navigateur.md#4-le-navigateur-intégré) : refaire l'essai « l'agent lit une page du navigateur » avec *Gemma 4 12B QAT*. **Fait (7 octobre 2026)** : avec le 26B (le 12B est absent) : page ouverte, contenu non lu.

## 4. Essais bloqués par l'absence de matériel ou d'outil

- [x] **Outils tiers** du [Manuel 13](docs/lmstudio/13-integrations-outils-tiers.md) : installer Node.js (ou Docker pour Open WebUI) puis lancer réellement Claude Code, Codex, Cline, Continue, Aider ; comparer avec les requêtes rejouées par `simuler_clients_tiers.py`. **Fait (7 octobre 2026)** : Claude Code, Cline, Continue (réussis), Aider (édition exacte, `pytest` absent de l'environnement), Codex (connecté, bac à sable en lecture seule : assouplissement refusé par le classifieur de sécurité, non insisté). **Roo Code** (extension sans ligne de commande) et **Open WebUI** (Docker absent, création de compte) **non lancés** : [Manuel 13](docs/lmstudio/13-integrations-outils-tiers.md).
- [ ] **Auto Review** niveau `too_destructive` ([Manuel Bionic 12](docs/bionic/12-auto-review.md)) : à reproduire dans une **machine virtuelle ou un dossier jetable**, jamais sur un dossier contenant des données réelles. **Non fait (7 octobre 2026)** : `too_destructive` **non obtenu** malgré `rm -rf ~`, `find -delete`, `Remove-Item` et `shred`. **Incident** : `shred -u -z ~/*.txt` approuvé automatiquement par le modèle 26B a détruit au moins un fichier réel (`HOME` non redirigé) : [Manuel Bionic 12](docs/bionic/12-auto-review.md#essais-sur-des-commandes-destructives-poste-à-gpu-dédié). Reste à faire dans une **machine virtuelle**.
- [x] **Plugins et SDK** (`lms dev`, `lmstudio-js`) : nécessitent Node.js ; non documentés à ce jour. **Fait (7 octobre 2026)** : [Manuel 16](docs/lmstudio/16-sdk-et-plugins.md) ; plugin `lms dev` fonctionnel ; l'API refuse `integrations` de type plugin (permission).
- [ ] **llmster / `lms daemon`** : absent de la 0.4.25 sur le poste de test ; vérifier sur la version installée. **Non fait (7 octobre 2026)** : `lms daemon` et `lms status` **existent** (cachées de `lms --help`) ; `up`, `down` et `update` **non exécutées** (arrêt de l'application ou téléchargement) ; installateur de llmster non exécuté.
- [x] OlmOCR 2 7B ([Manuel 05, section 7](docs/lmstudio/05-vision-images-et-ocr.md#7-exemple--un-modèle-docr-dédié-olmocr-2-7b)) : suivre le protocole de la section 7.8 **après accord** pour le téléchargement. **Fait (7 octobre 2026)** : déjà installé sur le poste (aucun téléchargement) : 4 pages fictives, 100 % d'exactitude (Q4_K_M, Q8_0, Gemma) ; [Manuel 05, section 7](docs/lmstudio/05-vision-images-et-ocr.md#7-exemple--un-modèle-docr-dédié-olmocr-2-7b).

## 5. Règles à conserver

- Même style que les manuels : ton impersonnel, « Essentiel » puis « Pour aller plus loin », étiquettes **[Vérifié]** / **[Source]** / **[Estimation]** / **[À tester]**.
- Convertir chaque **[Estimation]** ou **[À tester]** résolu en **[Vérifié]** et dater la mesure.
- Ne jamais capturer l'écran entier autour des dialogues natifs ; masquer les conversations personnelles ; vérifier qu'aucun jeton, nom de profil Windows ou chemin personnel n'apparaît sur une capture.
- À la fin : `python outils\verifier_docs.py` (liens, ancres, ton ; les 7 alertes « ton » existantes sont des citations d'interface), puis mettre à jour [NOTES-EVOLUTIONS.md](NOTES-EVOLUTIONS.md).
