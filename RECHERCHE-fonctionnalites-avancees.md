# Recherche : fonctionnalités avancées de LM Studio et de Bionic

> Synthèse de la recherche web du 7 octobre 2026 (rien n'a été téléchargé ni installé). Base de travail pour les évolutions des manuels.
> Versions de référence : LM Studio **0.4.25** (19 sept. 2026), Bionic **1.1.7** (1er oct. 2026).
> Statuts : **[DOC]** documentation officielle (dépôt `lmstudio-ai/docs`) ; **[OFF]** blog ou changelog officiel ; **[TIERS]** source tierce ; **[INCERT]** non confirmé, ancien ou contradictoire.
> Limites : certaines pages du dépôt de documentation sont vides (paramètres de chargement et d'inférence, runtimes) ; d'autres sont périmées (modes d'interface, décodage spéculatif). Les pages ont été lues via un outil qui peut les résumer : revérifier avant publication.

---

## 1. LM Studio : fonctionnalités avancées

### 1.1 MCP et outils

| Fonctionnalité | Résumé | Où / comment | Statut |
|---|---|---|---|
| **Hôte MCP, `mcp.json`** | Format « notation Cursor » ; fichier `%USERPROFILE%\.lmstudio\mcp.json` ; serveurs locaux via `npx` ou `uvx` ; rechargé à l'enregistrement | Program → Install → Edit mcp.json | [DOC] |
| **Approbation des outils** | Dialogue à chaque appel : relire et éditer les arguments, autoriser « une fois » ou « toujours » | Réglages (Tools & Integrations) | [OFF] |
| **OAuth pour MCP distants** | Entrée `url` dans `mcp.json` ; Notion, Linear, Atlassian, Sentry | `mcp.json` | [OFF] |
| **Deeplink « Add to LM Studio »** | `lmstudio://add_mcp?name=…&config=<JSON base64>` | Lien | [DOC] |
| **MCP par l'API** | `integrations` : `ephemeral_mcp` (serveur distant à la volée, `allowed_tools`) ou `mcp/<nom>` (serveur de `mcp.json`) ; deux réglages serveur requis, dont un exige l'authentification | `POST /api/v1/chat` | [DOC] |
| **Tool use / function calling** | Support natif (template d'outils reconnu) ou par prompt de substitution ; `tool_choice` ; streaming de `tool_calls` | `/v1/chat/completions`, `/v1/responses`, `/v1/messages` | [DOC] |
| **Plugin `js-code-sandbox`** | Exécution JS/TS dans un bac à sable Deno | Hub → chat | [DOC] |

### 1.2 Plugins, SDK, Hub, presets

| Fonctionnalité | Résumé | Statut |
|---|---|---|
| **Plugins (TypeScript)** | Trois types : *Tools Provider*, *Prompt Preprocessor* (le RAG intégré en est un), *Generator* (remplace le LLM). Développement : `lms dev`, publication : `lms push`. Plugins Python : « en développement » | [DOC] |
| **SDK `lmstudio-js` et `lmstudio-python`** | Chat, `act()` avec outils, sortie structurée, embeddings, tokenisation, image, annulation, décodage spéculatif, gestion des modèles | [DOC] |
| **Hub** | Dépôt communautaire de presets, plugins, modèles ; compte requis pour publier seulement | [DOC] |
| **Presets** | Prompt système + paramètres d'inférence (les paramètres de chargement n'en font plus partie) ; import fichier ou URL du Hub, export, publication, *Pull* ; stockés dans `~\.lmstudio\config-presets` | [DOC] |
| **`model.yaml` / modèles virtuels** | Fichier portable décrivant un modèle et ses variantes ; champs `model`, `base`, `metadataOverrides`, `config`, `customFields` ; `lms clone`, `lms push` | [DOC] |
| **Défauts par modèle** | Engrenage dans My Models ; s'applique aussi à `lms load` et à l'API | [DOC] |
| **Surcharge du prompt template** | Mode Jinja ou mode manuel (préfixes/suffixes par rôle) ; possible pour GGUF depuis 0.4.17 | [DOC] [OFF] |

### 1.3 API et serveur

| Fonctionnalité | Résumé | Statut |
|---|---|---|
| **API REST v1 `/api/v1/*`** | `chat`, `models`, `models/load`, `models/unload`, `models/download` ; statistiques de réponse (tokens/s, TTFT, temps de chargement) ; paramètre `reasoning` | [DOC] |
| **Chat à état** | `response_id` puis `previous_response_id`, ramification possible | [DOC] |
| **Compatibilité OpenAI / Anthropic** | `/v1/models`, `/v1/chat/completions`, `/v1/responses`, `/v1/embeddings`, `/v1/completions` ; `/v1/messages` (Anthropic) depuis 0.4.1 | [DOC] [OFF] |
| **Jetons d'API et permissions** | « Require Authentication » ; Manage Tokens (nom + permissions, visible une seule fois) ; `Authorization: Bearer` | [DOC] |
| **Réglages du serveur** | Port, authentification, *Serve on Local Network*, MCP par requête, MCP de `mcp.json`, CORS, JIT, déchargement auto, un seul modèle JIT | [DOC] |
| **Servir sur le réseau** | `lms server start --bind 0.0.0.0` ; tout bind autre que 127.0.0.1 expose le serveur : activer l'authentification | [DOC] |
| **JIT, TTL, auto-evict** | TTL inactif par défaut 60 min ; réglable par requête (`ttl`), en CLI, globalement | [DOC] |
| **Requêtes parallèles** | *Max Concurrent Predictions* (4 par défaut), *Unified KV Cache*, `lms load --parallel N` ; batching continu MLX depuis 0.4.2 | [DOC] [OFF] |
| **Sortie structurée** | `response_format.json_schema` ; grammaire llama.cpp (GGUF), Outlines (MLX) ; peu fiable sous ~7 Md | [DOC] |
| **Logs** | `lms log stream --source model|server --filter input,output --json --stats` | [DOC] |

### 1.4 Headless, LM Link, CLI

| Fonctionnalité | Résumé | Statut |
|---|---|---|
| **llmster / daemon** | Cœur sans interface (serveurs, CI) ; installation par script ; `lms daemon up|down|status|update` ; unité systemd | [DOC] |
| **Mode headless de l'application** | Serveur lancé à la connexion de session ; fermeture de fenêtre = réduction dans la zone de notification | [DOC] |
| **LM Link** | Utiliser un modèle d'un autre appareil comme s'il était local ; chiffrement de bout en bout via Tailscale (réseau dédié) ; compte requis ; `lms link enable|disable|status|set-device-name|set-preferred-device` ; application mobile *Locally* | [DOC] [OFF] |
| **`lms`** | `get` (nom@quantif, `--mlx`, `--gguf`), `ls` (`--variants`, `--json`, `--detailed`), `ps`, `load` (`--gpu`, `--context-length`, `--ttl`, `--identifier`, `--estimate-only`, `--parallel`), `unload`, `import` (`--copy`, `--hard-link`, `--symbolic-link`, `--dry-run`), `chat` (`-p`, `-s`, `--stats`, `/reasoning`), `server`, `log stream`, `runtime`, `dev`, `clone`, `push`, `login`, `daemon`, `link` | [DOC] |

### 1.5 Moteur, performance, mémoire

| Fonctionnalité | Résumé | Statut |
|---|---|---|
| **Runtimes** | llama.cpp (GGUF), MLX (Apple Silicon) ; variantes CUDA, Vulkan, Metal, ROCm ; mise à jour automatique ; `lms runtime` | [OFF] |
| **LM Studio Engine Protocol** | Architecture de moteur à mise à jour fréquente ; activé par défaut depuis 0.4.19 ; apporte templates surchargeables, spéculatif au chargement, surcharges d'arguments llama.cpp (0.4.24) | [OFF] |
| **Flash Attention** | Activé par défaut (CUDA, Vulkan, Metal) | [OFF] |
| **Quantification du cache KV** | Réduit la mémoire du contexte (llama.cpp) | [OFF] |
| **Offload GPU / multi-GPU** | Activation par GPU, ordre de priorité, limite à la mémoire dédiée, tensor parallelism CUDA (0.4.15), *Physical Batch Size* | [OFF] |
| **Experts MoE sur CPU** | Force les experts en RAM quand la VRAM manque | [OFF] |
| **Décodage spéculatif** | Modèle principal + petit modèle de même vocabulaire (ex. 7 Md + 1 Md) ; gains annoncés 1,4× à 2,4× ; MTP, DFlash, DSpark depuis 0.4.14 / 0.4.22 | [DOC] [OFF] |
| **Politique de dépassement de contexte** | *Rolling Window*, *Truncate Middle*, *Stop at Limit* | [TIERS] |
| **Garde-fous de chargement** | Estimation mémoire avant chargement ; bouton « Load anyway » (interface seulement) ; `lms load --estimate-only` | [OFF] [TIERS] |
| **Raisonnement** | Bloc repliable ; champ `reasoning` ; niveaux off/low/medium/high/on ; `/reasoning` en CLI | [OFF] |
| **Splash** | Moteur expérimental Apple Silicon (Mac M3+, macOS 26.4+, 36 Go minimum) | [OFF] |

### 1.6 Chat, interface, intégrations

| Fonctionnalité | Résumé | Statut |
|---|---|---|
| **Chat avec documents (RAG)** | `.docx`, `.pdf`, `.txt` ; document court injecté en entier, long : passages récupérés ; seuils exacts propres à des plugins tiers | [DOC] [TIERS] |
| **Mise en page du chat** | Dossiers, vue scindée, branches, génération multiple, recherche (chat / tous les chats), corbeille, export PDF/Markdown/texte, diagrammes Mermaid, comptage de tokens en direct ; conversations en JSON dans `~\.lmstudio\conversations` | [DOC] [OFF] |
| **Modes d'interface** | *User* / *Developer* ; Developer Mode fusionne les anciens modes depuis 0.4.0 | [DOC] [OFF] |
| **Intégrations** | Claude Code (`ANTHROPIC_BASE_URL`), Codex (`codex --oss`), Cline, Roo Code, Continue, Open WebUI, Aider (clé factice obligatoire) | [DOC] [TIERS] |

---

## 2. Bionic : fonctionnalités

| Domaine | Fonctionnalités | Statut |
|---|---|---|
| **Projets, sessions** | Projet unifié (« Allow coding » facultatif) ; chats sans projet ; fork ; onglets côte à côte ; déplacement entre projets ; sessions latérales ; fichiers jusqu'à 100 MiB ; dossiers en pièce jointe | [DOC] [OFF] |
| **Navigation** | Ouverture rapide (Cmd/Ctrl+P : fichiers, URL, sessions) ; mentions `@` (fichiers externes, compétences, autres sessions) | [OFF] |
| **Interface** | Navigateur intégré ; éditeur Markdown et sources ; **Canvas** (export PNG, SVG, Excalidraw) ; fenêtre toujours au premier plan ; 7 langues | [OFF] |
| **Modèles** | Cloud (crédits, ZDR), local, distant (LM Link) ; sélecteur de modèle ; modèle racine ; téléchargement dans Explorer avec informations d'adéquation à l'appareil et choix de l'appareil de destination | [DOC] |
| **Performance Mac** | Splash ; accélération M5 ; cache disque du prompt MLX ; MTP | [OFF] |
| **Code et shell** | Quatre modes (désactivé, manuel, **Auto Review**, tout autoriser) ; préférences persistantes ; garde-fous Git ; diffs en ligne | [OFF] |
| **Auto Review** | Deux étages : *Shell Judge* (analyseur déterministe, jusqu'à 82 % des commandes approuvées sans modèle d'après l'éditeur) puis *Shell Reviewer* (sous-agent : risque `low`/`high`/`too_destructive`, autorisation `explicitly_yes`/`neutral`/`explicitly_no`) ; une commande `too_destructive` n'est jamais exécutée | [OFF] |
| **Sauvegarde** | *Checkpoints* automatiques ; invites si une opération dépasse leurs limites ; ne couvrent que les fichiers suivis, pas les effets de bord [TIERS] | [OFF] |
| **Sous-agents** | Vision (modèle texte + modèle image) ; exploration ; reviewer d'Auto Review | [OFF] |
| **Introspection** | Relecture des transcriptions persistées (après compaction ou autre session) ; autorisation explicite pour une autre session | [OFF] |
| **Documents** | Word (commentaires, suivi des modifications), PDF (commentaires), PowerPoint, tableurs ; aperçus | [OFF] |
| **Compétences** | `SKILL.md` ; `@`, `/install-skill`, `/create-skill` ; import depuis Codex et Claude Code ; découverte `.agents` | [DOC] [OFF] |
| **MCP** | OAuth, délais réglables, MCP gérés par l'organisation | [OFF] |
| **Voix** | Voxtral local ; « voice keyboard » dans d'autres applications (annoncé) ; chargement automatique | [DOC] [OFF] |
| **Sécurité réseau** | Règles d'accès aux sites avec jokers ; recherche web activable ; ZDR pour le cloud | [OFF] |
| **Plateformes** | Windows, macOS, Linux (depuis 1.1.2) | [OFF] |

Points de vigilance :

- La documentation de Bionic est mince ; l'essentiel vient du changelog et du blog.
- **Cohabitation avec LM Studio** : la documentation indique que LM Studio reste utilisable « à côté » de Bionic ; sur le poste de test, un écran bloquant « Bionic cannot start » exige de quitter LM Studio. Constat de terrain à conserver, source documentaire ambiguë.
- Taille du modèle vocal : valeurs contradictoires entre sources tierces (≈ 3 Go, ≈ 10 Go).

---

## 3. Quantification : noms à connaître (GGUF)

### 3.1 Lire un nom

| Élément | Signification |
|---|---|
| **Q + chiffre** | Quantifié ; nombre de bits approximatif par poids |
| **_0 / _1** | Anciennes méthodes par blocs de 32 : `_0` = valeur × échelle ; `_1` ajoute un décalage (un peu plus précis, un peu plus gros) |
| **K (K-quants)** | Super-blocs de 256 poids ; échelles elles-mêmes quantifiées : meilleure qualité à taille égale |
| **S / M / L** | Small / Medium / Large : recettes qui mélangent les précisions selon les tenseurs (ex. Q3_K_S, Q3_K_M, Q3_K_L) |
| **IQ (I-quants)** | Très bas débit (1 à 4 bits), guidés par une matrice d'importance ; plus lents sur CPU |
| **XXS / XS / S / M / NL** | Sous-variantes d'une famille IQ (XXS < XS < S < M) ; `IQ4_NL` : bloc non linéaire |
| **imatrix / « i1 »** | Matrice d'importance calculée sur un texte de calibration : protège les poids importants (utile de 2 à 5 bits) |
| **UD** (*Unsloth Dynamic*) | Précision variable couche par couche, calibration maison [TIERS] |
| **XL** (ex. `UD-Q4_K_XL`) | Variante « plus large » : plus de tenseurs critiques en haute précision [INCERT] |
| **QAT** | *Quantization-Aware Training* : modèle entraîné pour être compressé, dégradation moindre |
| **F32 / F16 / BF16** | Non quantifiés ; référence |

### 3.2 Familles

| Famille | Types | Bits/poids ≈ | Commentaire |
|---|---|---|---|
| Très bas débit | IQ1_S, IQ1_M | 1,6 – 1,75 | Quasi expérimental |
| Bas débit | IQ2_XXS/XS/S, Q2_K | 2,1 – 3,0 | Faire tenir un gros modèle ; qualité variable |
| 3 bits | IQ3_XXS/S/M, Q3_K_S/M/L | 3,1 – 4,0 | Compromis serré |
| 4 bits | Q4_K_S, **Q4_K_M** (4,89), IQ4_XS (4,25), IQ4_NL, Q4_0, Q4_1 | 4,25 – 5 | Valeur sûre par défaut |
| 5 bits | Q5_K_S, **Q5_K_M** (5,70), Q5_0, Q5_1 | 5,5 – 6 | Meilleure fidélité (code) |
| 6 bits | **Q6_K** (6,56) | 6,56 | Très proche du non quantifié |
| 8 bits | **Q8_0** (8,50) | 8,5 | « Presque sans perte » |
| Non quantifié | F16, BF16, F32 | 16 – 32 | Référence |
| Ternaire | TQ1_0, TQ2_0 | 1,6 – 2,1 | Modèles entraînés en ternaire |
| **MXFP4** | — | ≈ 4,25 | Flottant 4 bits « microscaling » (blocs de 32, exposant partagé) ; natif de gpt-oss |
| **NVFP4** | — | ≈ 4,5 | Variante NVIDIA (blocs de 16) ; accélération réelle sur GPU Blackwell seulement [TIERS] |

Formats : LM Studio ne charge que **GGUF** et **MLX** (MLX : 4 ou 8 bits par groupes de 64 ou 128 poids). **AWQ et GPTQ ne sont pas chargeables** [TIERS].

---

## 4. Indicateurs d'adéquation matérielle (Download options)

La documentation officielle **ne définit pas** les badges ; les sens suivants viennent de sources tierces [TIERS] et sont à **vérifier sur une machine avec GPU dédié** (vérifié depuis : [Manuel LM Studio 02, section 6](docs/lmstudio/02-selectionner-et-telecharger-un-modele.md#6-les-indicateurs-dadéquation-matérielle)).

| Badge | Sens |
|---|---|
| **Full GPU Offload Possible** (vert) | Le modèle entier, au contexte par défaut, tient dans la mémoire GPU |
| **Partial GPU Offload Possible** (orange) | Une partie des couches tient en VRAM, le reste en RAM / CPU : fonctionne, plus lent |
| **Likely too large for this machine** (rouge) | Dépasse les ressources estimées, même en offload partiel |

**Calcul de l'estimation** [OFF] : taille du modèle, longueur de contexte, pourcentage d'offload, Flash Attention, présence de vision ; affichée dans l'interface et par `lms load --estimate-only`. Formule générique [TIERS] : poids ≈ taille du fichier (+ ~10 %) ; cache KV ≈ 2 × couches × têtes KV × dimension de tête × contexte × octets.

**Limites connues** : estimations parfois très supérieures à la réalité (22,9 Go annoncés pour ~11,5 Go réels) ; « Load anyway » absent du CLI et de l'API ; « GPU offload : Max » est une demande, pas un résultat (vérifier « offloaded n/m layers » dans les logs). Sur le poste de test, le GPU intégré (mémoire partagée) reçoit aussi le badge vert.

---

## 5. Usages réels

**Cas fréquents** : chat local confidentiel avec RAG ; backend d'API pour outils de code (Cline, Roo Code, Continue, Aider, Claude Code, Codex) et interfaces web ; essai rapide de modèles et de quantifications ; agents avec MCP ; serveur partagé (réseau local, LM Link, llmster) ; travail agentique avec Bionic.

**Pièges courants** : contexte par défaut trop court (8 192 depuis 0.4.16) ; offload « Max » non effectif ; moteur obsolète après une mise à jour ; petits modèles et appels d'outils mal formés ; MCP non fiables ; exposition réseau sans authentification ; clé d'API factice exigée par certains clients ; Bionic : modèle cloud actif sans s'en apercevoir, RAM saturée par modèle + voix + agent.

---

## 6. Sources principales

- Documentation : `https://raw.githubusercontent.com/lmstudio-ai/docs/main/` (dossiers `0_app`, `0_bionic`, `1_developer`, `2_typescript`, `3_cli`, `4_integrations`, `5_lmlink`).
- Changelog : `https://lmstudio.ai/changelog` (versions `lmstudio-v0.4.x`, `bionic-v1.x.y`).
- Blog : `https://lmstudio.ai/blog` (dont `introducing-lm-studio-bionic`, `how-auto-review-works`, `introducing-introspection`, `skills`, `splash-engine`, `0.4.0`, `claudecode`, `locally-lm-link`).
- Quantification : `https://raw.githubusercontent.com/ggml-org/llama.cpp/master/tools/quantize/README.md`, `https://huggingface.co/docs/hub/gguf`, `https://github.com/ggml-org/llama.cpp/pull/1684`, `https://github.com/ggml-org/llama.cpp/pull/4861`, `https://unsloth.ai/docs/basics/dynamic-3.0-ggufs.md`, `https://docs.mistral.ai/cookbooks/concept-deep-dive-quantization-methods-gguf`.
- Badges et mémoire : `https://github.com/lmstudio-ai/lms/issues/499`, `https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/2312`, `https://fast.io/resources/lm-studio-context-length/`.
- Bionic (tiers) : `https://www.heise.de/en/news/LM-Studio-Bionic-Local-AI-agent-system-for-open-models-11373476.html`, `https://www.bitdoze.com/lm-studio-bionic/`, `https://runaihome.com/blog/lm-studio-bionic-local-ai-agent-hardware-guide-2026/`.
- Intégrations (tiers) : `https://docs.cline.bot/running-models-locally/lm-studio`, `https://docs.openwebui.com/alternatives/lm-studio.md`, `https://aider.chat/docs/llms/lm-studio.html`, `https://docs.roocode.com/providers/lmstudio`.
