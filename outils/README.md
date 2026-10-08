# Outils de production de la documentation

Ces scripts ont servi à **produire les captures d'écran et les mesures** des manuels. Ils ne sont pas nécessaires pour **lire** la documentation.

## Principe

LM Studio et Bionic sont des applications Electron. Lancées avec `--remote-debugging-port=9222` (9223 pour Bionic : `LM(port=9223)`), elles exposent le protocole Chrome DevTools (CDP) sur `127.0.0.1`. La bibliothèque `lmcdp.py` pilote l'application par ce port : clics, saisie, captures, annotations numérotées, glisser-déposer de fichiers.

## Contenu

| Fichier | Rôle |
|---|---|
| `lancer_lmstudio_debug.ps1` | Relance LM Studio avec le port de debug |
| `lmcdp.py` | Bibliothèque de pilotage (clic, saisie, capture, annotation, masquage des conversations existantes, cadrage de fenêtres modales, glisser-déposer) |
| `captures/capture_NN_*.py` | Scripts de capture, un par manuel (rejouables) |
| `experiences_api.py` | Mesures via l'API locale (température, graine, sortie structurée, flux, outils, embeddings, vision, vitesse du prompt) |
| `benchmark_chargement.py` | Comparatif GPU / CPU et parallélisme via `lms` et l'API |
| `mesures_estimation_gui.py` | Effet de chaque paramètre de chargement sur l'estimation mémoire |
| `figures_notions.py` | Génère les figures pédagogiques du Manuel 00 (décodage de `Q4_K_M`, tailles, mémoire, pile logicielle) |
| `figures_bionic.py` | Génère les figures du manuel Bionic 00 (boucle de l'agent, lieux d'exécution, modes shell) |
| `bionic_run.py` | Lance une session Bionic (modèle, pièce jointe, consigne), mesure la durée et capture le résultat |
| `serveur_mcp_demo.py` | Serveur MCP de démonstration (cinq outils inoffensifs, stdio ou HTTP local), bibliothèque standard |
| `tester_serveur_mcp.py` | Client MCP minimal qui rejoue le protocole contre le serveur de démonstration |
| `mesure_outils_fiabilite.py` | Mesure la fiabilité de l'appel d'outils d'un modèle (5 ou 17 outils, `DIFFICILE=1`) |
| `experiences_api_lot2.py` | Chat à état, `/v1/responses`, `/v1/messages`, statistiques, sortie structurée, outils, raisonnement |
| `experiences_mcp_api.py` | MCP par l'API (`integrations`) avec un jeton de test |
| `tester_authentification.py`, `tester_cors.py` | Essais d'authentification, de permissions de jeton et de CORS |
| `simuler_clients_tiers.py` | Rejoue les requêtes de Claude Code, Codex, Cline, Roo Code, Continue, Open WebUI, Aider |
| `bionic_lib.py` | Fonctions de pilotage de Bionic (CDP, port 9223) partagées par les scripts du lot 2 |
| `lire_approbations_bionic.py` | Lit dans la base de sessions de Bionic le mode d'approbation (`shellJudge`, `autoReviewer`) de chaque commande |
| `figures_lot2.py`, `figures_competences.py` | Figures pédagogiques du lot 2 (boucle d'outil, exposition, chat à état, Auto Review, intégrations, compétences) |
| `competences_demo/`, `mcp_demo_notes/` | Compétences et notes **fictives** utilisées pour les essais |
| `verifier_docs.py` | Contrôle liens, ancres et ton de la documentation |
| `nettoyer_conversations_test.py` | Supprime les conversations de test créées pendant la production |
| `gpu_bench.py` | Bibliothèque des mesures sur GPU dédié (chargement par l'API, vitesse du prompt et de la génération, VRAM par `nvidia-smi`, RAM du moteur) |
| `gpu_offload_moteurs.py` | Moteurs (CUDA, Vulkan, CPU) et part de couches sur le GPU ([Manuel 15, section 2](../docs/lmstudio/15-performances-gpu-dedie.md#2-moteurs-et-nombre-de-couches-sur-le-gpu)) |
| `gpu_parametres_charge.py` | Flash Attention, lots, cache K/V en VRAM ou en RAM, parallélisme (API `/api/v1/models/load`) |
| `gpu_sdk_params.py` | Paramètres de chargement absents de `lms load`, par le SDK (quantification du cache K/V, `--n-cpu-moe`, lot physique) |
| `gpu_gros_modeles.py` | Modèles plus gros que la VRAM (MoE 26B, dense 27 Md) : répartition, vitesse, grand contexte |
| `gpu_contexte_memoire.py` | Mémoire réelle (VRAM, RAM) selon le contexte, comparée à l'estimation de `lms load --estimate-only` |
| `gpu_decodage_specul.py` | Décodage spéculatif : MTP intégré et modèle brouillon séparé |
| `essai_olmocr.py` | Protocole OCR du [Manuel 05, section 7](../docs/lmstudio/05-vision-images-et-ocr.md) (4 pages fictives, exactitude par champ, VRAM) |
| `sdk_js/` | `charger.mjs`, `essai_sdk.mjs` et `plugin-demo/` (plugin `lms dev`) ; `npm install` crée `node_modules/` (ignoré par Git) |
| `captures/capture_02b_badges_gpu_dedie.py` | Régénère la figure des badges d'adéquation sur le poste à GPU dédié |
| `bionic_tache.py` | Lance **une tâche** dans une nouvelle session Bionic (projet, modèle, effort, mode shell, consigne), mesure la durée, relève le **modèle réel** dans la base de sessions, les commandes et leur approbation ; résultat `resultats/gpu_dedie/bionic_<étiquette>.json` |
| `bionic_compact.py` | Mesure `/compact` (contexte avant et après, durée, modèles réels des sous-sessions) |
| `bionic_arobase.py` | Déclenchement manuel d'une compétence de projet avec `@` (palette) dans une nouvelle session, avec modèle réel vérifié |
| `bionic_essai.py` | Essai libre dans une nouvelle session (consigne ou commande `/`), avec mode shell, capture et relevé du modèle réel, des outils et de la réponse ; **`MSYS_NO_PATHCONV=1`** est nécessaire sous Git Bash pour passer un texte commençant par `/` |
| `bionic_parallele.py` | Sessions Bionic **simultanées** (N sessions lancées à 15 s d'intervalle) ; durées lues dans la base de sessions (`durees_sessions`) |
| `bionic_memoire.py` | Mémoire occupée par un modèle chargé par Bionic (AutoFit : contexte, VRAM, RAM du moteur) |
| `resultats/` | Résultats bruts (JSON) et images de test fictives ; `resultats/gpu_dedie/` : série du poste à GPU dédié |

## Prérequis

- Python 3.12 et un environnement virtuel **hors de OneDrive** (milliers de fichiers) avec `websocket-client` et `pillow` ;
- LM Studio lancé avec le port de debug.

```powershell
python -m venv $env:TEMP\venv-lmcdp
& $env:TEMP\venv-lmcdp\Scripts\python.exe -m pip install websocket-client pillow
.\outils\lancer_lmstudio_debug.ps1
& $env:TEMP\venv-lmcdp\Scripts\python.exe .\outils\captures\capture_01_prise_en_main.py
```

## Précautions

- Aucune capture ne montre les conversations préexistantes de l'utilisateur (masquage dans `LM.MASK`).
- Les téléchargements de modèles sont lancés **à la main ou sur instruction explicite** ; aucun script ne cible un bouton de téléchargement.
- Bionic et LM Studio ne peuvent pas être ouverts en même temps : lancer l'un après avoir quitté l'autre.
- Les sélecteurs de fichiers natifs de Windows ne se pilotent pas par CDP : pour joindre un fichier, utiliser le glisser-déposer simulé (`LM.drop_files`) et ne jamais capturer l'écran entier (dossiers personnels visibles).
- Un rechargement de page (`Page.reload`) rend parfois impossible l'envoi de messages dans une nouvelle conversation ; éviter de recharger avant une séquence d'envois.
- Après un changement de taille de fenêtre émulée, le panneau de chat peut ne plus s'afficher : recharger la page, puis reprendre.
- Les images de test (`resultats/facture_test_*.png`) sont **fictives**.
- Lot 2 : aucun serveur MCP tiers ni outil externe n'est installé ; les jetons d'API des essais sont **factices**, créés puis supprimés ; *Serve on Local Network* n'est jamais activé. Les journaux `resultats/mcp_demo_appels.log` et `resultats/lot2_*.json` ne contiennent aucun jeton.
- Les menus contextuels de Bionic (menu **…** des sessions) sont natifs : non pilotables par CDP ; les sessions de test se suppriment à la main.
- **Pilote Bionic (`bionic_lib.py`)** : (1) la fenêtre est **mise en plein écran** à chaque connexion et l'émulation de taille (1440 × 900) est **levée** en fin de script, sinon la page n'occupe qu'une partie de la fenêtre ; (2) l'écran peut être scindé en **colonnes** : le pilote agit sur la colonne de la session qu'il vient de créer (`COLX`) ; (3) **ne jamais lancer deux scripts de pilotage en même temps** : ils se disputent l'interface ; (4) le modèle sélectionné est **vérifié** sur le bouton, puis relu dans la base (`modele_reel`) : un résultat dont le modèle réel diffère du modèle demandé est à écarter.
- **Essais destructifs** : jamais sur le vrai profil. Un essai `shred -u -z ~/*.txt` (modèle 26B) a été **approuvé automatiquement par Auto Review** alors que `HOME` n'était pas redirigé : au moins un fichier réel a été détruit ([Manuel Bionic 12](../docs/bionic/12-auto-review.md#essais-sur-des-commandes-destructives-poste-à-gpu-dédié)). Exiger une variable `HOME` factice **et** des chemins explicites.
- Les options d'approbation automatique de `bionic_tache.py` (`--oui-shell`) valident **toutes** les boîtes « Yes », y compris l'installation d'une compétence globale : à réserver à un projet jetable.
