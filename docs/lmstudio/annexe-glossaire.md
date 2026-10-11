# Annexe — Glossaire

Termes utilisés dans les manuels LM Studio, par ordre alphabétique.

| Terme | Définition |
|---|---|
| **`--n-cpu-moe N`** | Option de llama.cpp (via `llamaCppArgumentsOverride` du SDK) qui laisse sur le **CPU** les experts des N premières couches d'un modèle MoE : sur 16 Go de VRAM, *Gemma 4 26B A4B* passe de 36,7 à **54,6 tok/s** avec `--n-cpu-moe 8` ([Manuel 15, section 6.2](15-performances-gpu-dedie.md#62-experts-moe-sur-le-cpu---n-cpu-moe-via-le-sdk)). |
| **Anchor text** | Dans olmOCR (v1), texte extrait du PDF et fourni au modèle en plus de l'image pour l'aider. Les modèles olmOCR 2 **n'utilisent plus** l'anchor text. |
| **API compatible OpenAI** | Interface HTTP qui reprend le format de l'API d'OpenAI (`/v1/chat/completions`…) : les outils et bibliothèques prévus pour OpenAI fonctionnent en changeant seulement l'adresse (`http://127.0.0.1:1234/v1`). |
| **Appel d'outil** (*tool call*) | Demande structurée (nom + arguments JSON) produite par le modèle ; l'application l'exécute et renvoie le résultat ([Manuel 10](10-mcp-et-appel-d-outils.md#1-principe)). |
| **AWQ / GPTQ** | Formats de quantification destinés à d'autres moteurs (vLLM, Transformers) : **non chargeables** dans LM Studio ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#54-formats-qui-ne-se-chargent-pas)). |
| **Bande passante mémoire** | Débit (Go/s) de lecture de la mémoire ; elle limite la vitesse de génération ([Manuel 00](00-notions-fondamentales.md#9-la-vitesse--tokens-par-seconde)). |
| **BF16 / F16 / F32** | Formats de nombres sur 16 ou 32 bits : modèle **non quantifié**, de qualité maximale et de taille maximale. |
| **Bionic (LM Studio Bionic)** | Application *agent* distincte de LM Studio, éditée par la même société (code, documents). Décrite dans les [manuels Bionic](../bionic/README.md). |
| **Cache KV (KV cache)** | Mémoire où le modèle conserve les représentations des tokens déjà lus pour ne pas les recalculer. Sa taille croît avec la longueur du contexte et est le principal poste de mémoire après les poids. |
| **Chat à état** | Conversation conservée côté serveur : chaque réponse reçoit un `response_id`, à fournir en `previous_response_id` pour poursuivre ([Manuel 12](12-api-avancee.md#2-chat-à-état--apiv1chat)). |
| **Champ personnalisé (custom field)** | Réglage ajouté par un `model.yaml` à l'interface d'un modèle, avec un effet (par exemple *Enable Thinking* qui écrit une variable du gabarit) ([Manuel 14](14-personnaliser-les-modeles.md#4-modelyaml-et-modèles-virtuels)). |
| **Chat template** | Gabarit qui transforme une conversation (système / utilisateur / assistant) en texte compris par le modèle, avec ses balises spéciales. Chaque famille de modèles a le sien. |
| **Contexte (context length)** | Nombre maximal de tokens que le modèle traite en une fois : consigne + historique + réponse. |
| **CORS** | Mécanisme de sécurité des navigateurs. L'activer permet à des **pages web** d'appeler le serveur local ; à n'activer que si nécessaire. |
| **CPU (runtime)** | Variante du moteur qui calcule sur le processeur ; fonctionne partout, la plus lente. |
| **CUDA** | Plateforme de calcul des cartes graphiques **Nvidia** ; le runtime CUDA est le plus rapide sur ce matériel et inutilisable sans carte Nvidia. |
| **Décodage spéculatif (speculative decoding)** | Technique qui accélère la génération grâce à un petit modèle « brouillon » (*drafter*) dont le grand modèle valide les propositions. |
| **Download Options** | Liste des fichiers téléchargeables d'une fiche de modèle (variante, quantification, taille, indicateur d'adéquation) ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#4-exemple-guidé-avec-gemma-4-e4b)). |
| **Embedding (vecteur de sens)** | Représentation numérique d'un texte, utilisée pour comparer des sens (recherche sémantique, RAG). Produite par un modèle *Text Embedding*. |
| **EOS token** | « End Of Sequence » : jeton par lequel le modèle indique qu'il a fini sa réponse (`Stop reason: EOS Token Found`). |
| **Flash Attention** | Méthode de calcul de l'attention plus économe en mémoire et souvent plus rapide ; prérequise pour quantifier le cache V. |
| **Full / Partial GPU Offload Possible, Likely too large** | Indicateurs d'adéquation matérielle de *Download Options* : vert (tient en mémoire graphique), bleu (partiel), rouge (trop gros) ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#6-les-indicateurs-dadéquation-matérielle)). |
| **GGUF** | Format de fichier de modèle utilisé par *llama.cpp* et donc LM Studio (extension `.gguf`). |
| **GPU intégré / dédié** | Intégré : partage la RAM de l'ordinateur ; dédié : carte séparée avec sa propre mémoire (VRAM). |
| **GPU offload** | Part des couches du modèle calculées sur le GPU plutôt que sur le CPU. |
| **Guardrails (garde-fous)** | Contrôles de LM Studio qui empêchent de charger un modèle trop gros pour la mémoire disponible. |
| **Harmony** | Format de conversation défini par OpenAI ; le composant « Harmony » de LM Studio décode les messages, étapes de raisonnement et appels d'outils : **ce n'est pas un moteur de calcul**. |
| **Hub (LM Studio Hub)** | Dépôt communautaire en ligne de modèles (fiches), presets, plugins et compétences ; compte requis seulement pour publier ([Manuel 14](14-personnaliser-les-modeles.md#5-le-hub)). |
| **Hugging Face** | Plate-forme publique où sont publiés la plupart des modèles. |
| **imatrix (matrice d'importance)** | Calibration qui indique quels poids protéger lors d'une quantification très poussée (≤ 4 bits) ; utilisée par les i-quants (`IQ`) et les fichiers « i1 ». |
| **Inférence** | Fait de **faire fonctionner** un modèle pour obtenir une réponse (par opposition à l'entraînement). |
| **IQ (i-quants)** | Quantifications à très bas débit (1 à 4 bits), guidées par une matrice d'importance : `IQ2_M`, `IQ3_XXS`, `IQ4_XS`… |
| **Jeton d'API** (*API token*) | Secret à placer dans `Authorization: Bearer …` quand l'authentification est activée ; affiché une seule fois, avec des permissions propres ([Manuel 11](11-securiser-le-serveur.md#3-authentification-et-jetons)). |
| **JIT (Just-in-Time) loading** | Chargement automatique d'un modèle à la première requête API qui le demande. |
| **K-quants** | Famille de quantifications par super-blocs de 256 poids (`Q4_K_M`, `Q6_K`…) : meilleure qualité que les anciennes `_0` / `_1` à taille égale. |
| **llama.cpp** | Moteur open source d'inférence sur lequel s'appuie LM Studio pour les modèles GGUF. |
| **LLM** | *Large Language Model*, modèle de langage. |
| **llmster** | Version « sans interface » de LM Studio pour serveurs ; sous Windows 0.4.25, `lms daemon` et `lms status` existent mais sont **absentes de `lms --help`** ([Manuel 16, section 5](16-sdk-et-plugins.md#5-le-mode-sans-interface--llmster)). |
| **LM Link** | Fonction de LM Studio qui relie plusieurs appareils d'un même compte (réseau privé chiffré) pour utiliser leurs modèles à distance ; préversion, compte requis. ([17](17-lm-link.md)) |
| **`lms`** | Programme en ligne de commande de LM Studio. |
| **Lot physique** (*physical batch size*) | Nombre de jetons du prompt traités par passe de calcul ; sous 256, la lecture du prompt perd 25 à 30 % de vitesse sur la RTX 4060 Ti ([Manuel 15, section 4](15-performances-gpu-dedie.md#4-flash-attention-lots-et-cache-kv)). |
| **MCP (Model Context Protocol)** | Protocole standard pour donner à un modèle accès à des outils et sources de données externes. |
| **`mcp.json`** | Fichier `%USERPROFILE%\.lmstudio\mcp.json` qui déclare les serveurs MCP (commande locale ou URL distante) ([Manuel 10](10-mcp-et-appel-d-outils.md#2-déclarer-un-serveur-mcp--mcpjson)). |
| **Min P / Top P / Top K** | Réglages d'échantillonnage qui limitent l'ensemble des mots candidats à chaque étape. Voir le [Manuel 04](04-parametrer-l-inference.md). |
| **mmap** | Technique de chargement d'un fichier en mémoire sans le copier entièrement, qui accélère le démarrage. |
| **mmproj** | Fichier GGUF auxiliaire (« projecteur multimodal ») qui permet à un modèle de lire des images. |
| **model.yaml / modèle virtuel** | Fichier ouvert qui décrit un modèle de façon portable (fichiers de base, métadonnées, défauts, champs personnalisés) sans contenir les poids ([Manuel 14](14-personnaliser-les-modeles.md#4-modelyaml-et-modèles-virtuels)). |
| **MoE (Mixture of Experts)** | Modèle composé d'« experts » dont seuls quelques-uns travaillent à chaque token : mémoire de la taille totale, vitesse de la taille active (ex. « 26B A4B »). |
| **MTP** (*Multi-Token Prediction*) | Tête de prédiction de plusieurs jetons **intégrée au fichier** du modèle : sert de brouillon au **décodage spéculatif** sans second modèle. Refusé sur un fichier sans tête MTP ; sur *Qwen3.8 27B* : jusqu'à +31 % en code, −11 à −41 % en prose ([Manuel 15](15-performances-gpu-dedie.md)). |
| **MXFP4 / NVFP4** | Formats flottants 4 bits à échelle partagée par blocs (≈ 4,25 et ≈ 4,5 bits par poids) ; MXFP4 est le format natif de certains modèles (*gpt-oss*). |
| **OCR** | *Optical Character Recognition* : extraction du texte d'une image ou d'un scan. |
| **olmOCR** | Famille de modèles et boîte à outils de l'Allen Institute for AI, spécialisés dans la conversion de documents PDF/images en texte. |
| **Parallélisme** (*max concurrent predictions*) | Nombre de requêtes servies simultanément par un modèle chargé (défaut 4). Sur GPU dédié, le débit total croît presque linéairement (45 → 264 tok/s pour 1 → 8 requêtes) ; sur GPU intégré, il ne croît pas ([Manuel 03, section 5.5](03-charger-un-modele.md#55-concurrence-selon-le-matériel)). |
| **Plugin (`lms dev`)** | Extension locale (outils, prétraitement du prompt) lancée en développement par `lms dev` ; utilisable depuis le chat de LM Studio avec confirmation d'appel d'outil ([Manuel 16](16-sdk-et-plugins.md)). |
| **Preset** | Jeu de paramètres enregistré sous un nom, réutilisable d'une conversation à l'autre. |
| **Prompt (invite)** | Texte envoyé au modèle. Le **prompt système** définit son rôle et ses règles ; le **prompt utilisateur** contient la demande. |
| **Q4_K_M (décodage)** | **Q** = quantifié ; **4** = ≈ 4 bits par poids ; **K** = méthode K-quants (compression par blocs) ; **M** = medium (S small, L large). |
| **QAT** | *Quantization-Aware Training* : modèle entraîné en tenant compte de la compression, qui perd moins de qualité en 4 bits. |
| **Quantification** | Compression des poids d'un modèle (ex. 4 bits au lieu de 16) : fichier plus petit, légère perte de précision. |
| **RAG** | *Retrieval-Augmented Generation* : le modèle répond à partir de passages de documents retrouvés par similarité. |
| **Raisonnement (reasoning / thinking)** | Phase pendant laquelle le modèle « réfléchit » avant de répondre ; visible dans le bloc *Thought for … seconds*. Plus lent, souvent plus fiable. |
| **RoPE** | *Rotary Positional Embedding* : mécanisme par lequel le modèle repère la position des tokens ; ses réglages permettent d'étendre le contexte. |
| **Runtime (moteur)** | Composant logiciel qui exécute le modèle (Vulkan, CPU, CUDA…). |
| **S / M / L / XL, XXS / XS / NL** | Suffixes des quantifications : taille de la recette (*Small*, *Medium*, *Large*, *XL* chez Unsloth) et sous-variantes `IQ` (*extra-extra-small*, *extra-small*, *non-linear*) ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#51-lire-un-nom)). |
| **SDK** (*Software Development Kit*) | Kit de développement : `@lmstudio/sdk` (JavaScript) et `lmstudio` (Python) donnent accès à des paramètres de chargement absents de `lms load` (ratio GPU, quantification du cache K/V, experts MoE sur CPU) ([Manuel 16](16-sdk-et-plugins.md)). |
| **Seed (graine)** | Valeur qui fixe le tirage aléatoire ; à graine et réglages identiques, la réponse est reproductible. |
| **Serve on Local Network** | Réglage qui fait écouter le serveur sur toutes les interfaces (`0.0.0.0`) au lieu de `127.0.0.1` ; équivalent de `--bind` ([Manuel 11](11-securiser-le-serveur.md#2-trois-niveaux-dexposition)). |
| **Serveur MCP** | Programme (local, par stdio) ou service (distant, par URL) qui expose des outils à une application hôte ([Manuel 10](10-mcp-et-appel-d-outils.md)). |
| **Structured output** | Sortie contrainte à un format (JSON conforme à un schéma). |
| **Température** | Réglage de la « créativité » : 0 = réponse la plus probable (déterministe) ; valeurs élevées = réponses plus variées. |
| **Token** | Unité de découpage du texte (≈ ¾ de mot en français ; un mot long ou rare en compte plusieurs). La vitesse se mesure en **tokens par seconde (tok/s)**. |
| **TQ1_0 / TQ2_0** | Quantifications ternaires, réservées aux modèles entraînés en ternaire. |
| **TTFT** | *Time To First Token* : délai avant l'apparition du premier token de la réponse. |
| **TTL** | *Time To Live* : durée d'inactivité après laquelle un modèle est déchargé automatiquement. |
| **UD (Unsloth Dynamic)** | Quantifications d'éditeur à précision variable selon les couches (`UD-Q4_K_XL`) ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#53-les-suffixes-et-les-recettes)). |
| **Vision (VLM)** | Capacité d'un modèle à comprendre des images ; un *Vision-Language Model* a besoin d'un fichier `mmproj`. |
| **VRAM** | Mémoire propre à une carte graphique dédiée, très rapide ; le modèle doit y tenir pour un déchargement complet. |
| **Vulkan** | Interface graphique standard utilisée ici par le moteur d'inférence pour exploiter le GPU Intel Arc. |
