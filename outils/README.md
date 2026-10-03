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
| `resultats/` | Résultats bruts (JSON) et images de test fictives |

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
