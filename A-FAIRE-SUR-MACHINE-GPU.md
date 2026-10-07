# À faire sur une machine avec GPU dédié

> Liste de contrôle pour compléter les manuels après import du projet. Le poste de production n'avait **pas de GPU dédié** (Intel Core Ultra 7 255H, 31 Go de RAM, GPU intégré, moteur Vulkan) : toutes les mesures de vitesse et de mémoire des manuels viennent de cette configuration.
> Suivi complet des demandes : [NOTES-EVOLUTIONS.md](NOTES-EVOLUTIONS.md) (points 1, 8, 9, 10, 11). Dernière mise à jour : 7 octobre 2026.

## 0. Préparation

1. Copier le dossier `EDF` **hors de OneDrive** si possible (milliers de fichiers dans les dossiers d'images et d'environnement).
2. Installer LM Studio **0.4.25** (même version que les manuels ; noter toute différence) et télécharger *Gemma 4 E4B* (Q4_K_M, 6,33 Go). *Gemma 4 12B QAT* (7,15 Go) pour les essais Bionic.
3. Python 3.12, environnement virtuel avec `websocket-client` et `pillow` ([outils/README.md](outils/README.md)).
4. Relever la configuration : GPU, VRAM, pilote, RAM, système ; **Hardware** (`Ctrl + Maj + H`) → comparer à la section 6 du [Manuel 01](docs/lmstudio/01-prise-en-main.md).
5. **Ne jamais ouvrir LM Studio et Bionic en même temps.** Ne rien publier, ne se connecter à aucun compte pour ces essais.

## 1. Badges d'adéquation (priorité 1)

Objet : [Manuel 02, section 6](docs/lmstudio/02-selectionner-et-telecharger-un-modele.md#6-les-indicateurs-dadéquation-matérielle).

- [ ] Rouvrir *Model Search* → dépôt `unsloth/gemma-4-E4B-it-GGUF` → liste *Download Options* (lecture seule, **sans cliquer sur Download**) : relever la couleur de chaque ligne (de `UD-IQ2_M` à `BF16`).
- [ ] Même relevé avec un modèle plus gros (par exemple *Gemma 4 26B A4B*) pour trouver les seuils vert / bleu / rouge **selon la VRAM**.
- [ ] Vérifier si la couleur change avec le **contexte par défaut** (*Settings → Model Defaults*).
- [ ] Capturer les trois états sur la machine GPU et **remplacer** la figure 5 du manuel 02 ; corriger les phrases « sur ce poste, GPU intégré » et la sous-section « Ce qui a été mesuré ».
- [ ] Comparer l'estimation affichée avec la consommation réelle (`lms load --estimate-only` puis `Get-Process`, ou le moniteur de ressources de LM Studio) : consigner l'écart.

## 2. Offload et moteurs (priorité 2)

Objet : [Manuel 03](docs/lmstudio/03-charger-un-modele.md) (sections 5.3 à 5.5) et [Manuel 00, section 6](docs/lmstudio/00-notions-fondamentales.md#6-les-moteurs-runtimes--cpu-cuda-vulkan-metal-harmony).

- [ ] Rejouer [outils/benchmark_chargement.py](outils/benchmark_chargement.py) : vitesse de génération et de traitement du prompt selon le nombre de couches sur GPU (0, moitié, maximum) et selon le moteur (**CUDA**, **Vulkan**, CPU).
- [ ] Rejouer [outils/mesures_estimation_gui.py](outils/mesures_estimation_gui.py) : l'estimation de mémoire change-t-elle avec un GPU dédié ?
- [ ] **Parallélisme** (*Max Concurrent Predictions*) : le gain de débit absent sur GPU intégré existe-t-il ? Mettre à jour [Manuel 03, section 5.5](docs/lmstudio/03-charger-un-modele.md#55-concurrence-sur-gpu-intégré).
- [ ] Effet de **Flash Attention**, de la **quantification du cache K/V** et de **Physical Batch Size** sur vitesse et mémoire.
- [ ] Gros contexte : charger *Gemma 4 12B QAT* à 8 192 puis à 262 144 tokens ; relever la VRAM et la RAM ([Manuel Bionic 04](docs/bionic/04-modeles.md) : 14,1 Go de RAM mesurés sur le poste de test).
- [ ] Modèle à experts (MoE) avec experts forcés sur CPU, si la VRAM est insuffisante.
- [ ] Décodage spéculatif : les lignes « Mtp » des listes de téléchargement ([Manuel 02, section 4](docs/lmstudio/02-selectionner-et-telecharger-un-modele.md#4-exemple-guidé-avec-gemma-4-e4b)) servent-elles de modèle brouillon ? Gain mesuré.

## 3. Reprise des vitesses annoncées

Remplacer, **en conservant l'ancienne valeur entre parenthèses** (« GPU intégré : … »), les chiffres suivants :

- [ ] Manuels [03](docs/lmstudio/03-charger-un-modele.md) et [04](docs/lmstudio/04-parametrer-l-inference.md) : tok/s, TTFT, durées de chargement, mesures de l'effet des paramètres.
- [ ] Manuel [05](docs/lmstudio/05-vision-images-et-ocr.md) : durée de la facture (25 à 37 s), jetons par seconde, conversation multi-tours (7,5 / 15,0 / 32,6 s).
- [ ] Manuels [06](docs/lmstudio/06-serveur-local-et-api.md), [10](docs/lmstudio/10-mcp-et-appel-d-outils.md), [12](docs/lmstudio/12-api-avancee.md) : latences de l'API et de l'appel d'outils (rejouer [outils/experiences_api.py](outils/experiences_api.py), `experiences_api_lot2.py`, `mesure_outils_fiabilite.py`).
- [ ] Manuels Bionic [05](docs/bionic/05-projets-et-sessions.md) à [07](docs/bionic/07-code-et-shell.md), [11](docs/bionic/11-recettes-et-depannage.md) et [14](docs/bionic/14-commandes-compaction-navigateur.md) : durées de tâches (mémo 2 min 4 s, facture, bogue de code 6 min 22 s / 4 min 50 s, `/compact` ≈ 90 s).
- [ ] [Manuel Bionic 14, section 4](docs/bionic/14-commandes-compaction-navigateur.md#4-le-navigateur-intégré) : refaire l'essai « l'agent lit une page du navigateur » avec *Gemma 4 12B QAT*.

## 4. Essais bloqués par l'absence de matériel ou d'outil

- [ ] **Outils tiers** du [Manuel 13](docs/lmstudio/13-integrations-outils-tiers.md) : installer Node.js (ou Docker pour Open WebUI) puis lancer réellement Claude Code, Codex, Cline, Continue, Aider ; comparer avec les requêtes rejouées par `simuler_clients_tiers.py`.
- [ ] **Auto Review** niveau `too_destructive` ([Manuel Bionic 12](docs/bionic/12-auto-review.md)) : à reproduire dans une **machine virtuelle ou un dossier jetable**, jamais sur un dossier contenant des données réelles.
- [ ] **Plugins et SDK** (`lms dev`, `lmstudio-js`) : nécessitent Node.js ; non documentés à ce jour.
- [ ] **llmster / `lms daemon`** : absent de la 0.4.25 sur le poste de test ; vérifier sur la version installée.
- [ ] OlmOCR 2 7B ([Manuel 05, section 7](docs/lmstudio/05-vision-images-et-ocr.md#7-exemple--un-modèle-docr-dédié-olmocr-2-7b)) : suivre le protocole de la section 7.8 **après accord** pour le téléchargement.

## 5. Règles à conserver

- Même style que les manuels : ton impersonnel, « Essentiel » puis « Pour aller plus loin », étiquettes **[Vérifié]** / **[Source]** / **[Estimation]** / **[À tester]**.
- Convertir chaque **[Estimation]** ou **[À tester]** résolu en **[Vérifié]** et dater la mesure.
- Ne jamais capturer l'écran entier autour des dialogues natifs ; masquer les conversations personnelles ; vérifier qu'aucun jeton, nom de profil Windows ou chemin personnel n'apparaît sur une capture.
- À la fin : `python outils\verifier_docs.py` (liens, ancres, ton ; les 7 alertes « ton » existantes sont des citations d'interface), puis mettre à jour [NOTES-EVOLUTIONS.md](NOTES-EVOLUTIONS.md).
