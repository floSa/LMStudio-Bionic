# Annexe — Glossaire Bionic

Termes utilisés dans les manuels Bionic. Les notions de modèle, de quantification et de contexte sont définies dans le [glossaire LM Studio](../lmstudio/annexe-glossaire.md).

| Terme | Définition |
|---|---|
| **Agent** | Modèle de langage doté d'outils, qui enchaîne des actions pour accomplir une tâche. ([00](00-notions-agent.md#1-chat-et-agent)) |
| **Appel d'outil** (*tool calling*) | Capacité d'un modèle à produire des appels structurés vers des outils (lire un fichier, lancer une commande). |
| **`approvalType`** | Champ du journal des sessions qui indique qui a approuvé une commande : `shellJudge` ou `autoReviewer` ([12](12-auto-review.md#2-observer-les-décisions--le-journal-des-sessions)). |
| **Archiver** | Retirer une session de la barre latérale en la conservant (Réglages → Sessions). |
| **Auto Review** | Fonction de la vérification automatique : analyseur déterministe (*Shell Judge*) puis sous-agent (*Shell Reviewer*) décident d'exécuter, de bloquer ou de soumettre une commande ([12](12-auto-review.md)). |
| **AutoFit** | Ajustement automatique des paramètres de chargement d'un modèle local ; sa longueur de contexte minimale se règle dans Réglages. |
| **Branche** (*fork*) | Nouvelle session qui part d'une réponse d'une session existante. ([05](05-projets-et-sessions.md#7-reprendre-modifier-ramifier)) |
| **Canal** | Flux de mises à jour de l'application (Stable). |
| **Checkpoint** | Point de sauvegarde automatique de fichiers avant modification [Source]. |
| **Cloud** (modèle) | Modèle exécuté dans le LM Studio Secure Cloud ; compte et crédits requis. ([10](10-securite-compte-api.md)) |
| **Compaction** | Résumé des échanges anciens pour libérer du contexte ; déclenchée par la commande `/compact` ou automatiquement ([Manuel 14](14-commandes-compaction-navigateur.md#2-compacter-une-session--compact)). |
| **Navigateur intégré** | Onglet de Bionic qui affiche une page web à côté de la session ; l'agent peut y ouvrir une adresse ([Manuel 14](14-commandes-compaction-navigateur.md#4-le-navigateur-intégré)). |
| **Compétence** (*skill*) | Dossier contenant un fichier `SKILL.md` d'instructions réutilisables. ([08](08-competences-et-mcp.md)) |
| **Compétence globale / de projet** | Compétence stockée dans `~/.lmstudio/skills` (tous les projets) ou dans `<projet>/.agents/skills` (ce projet seul) ([13](13-competences-en-pratique.md)). |
| **Contexte** | Mémoire de travail du modèle, comptée en tokens ; compteur affiché sous la zone de saisie. |
| **CORS** | Mécanisme autorisant un site web à appeler une API locale ; désactivé par défaut. |
| **Crédits** | Unité de consommation des modèles cloud. |
| **Diff** | Comparaison avant/après d'un fichier (lignes ajoutées en vert, supprimées en rouge). |
| **Dossier de travail** (*working directory*) | Dossier réel sur lequel l'agent travaille ; choisi à la création du projet. ([05](05-projets-et-sessions.md#3-dossier-de-travail-ou-fichiers-du-projet)) |
| **Effort de raisonnement** | Réglage du sélecteur de modèle activant ou non la phase de réflexion du modèle. ([04](04-modeles.md)) |
| **Fichiers du projet** (*Project files*) | Espace de fichiers géré par Bionic, partagé entre les sessions d'un projet. |
| **Fichiers externes** (*External files*) | Fichiers ou dossiers connectés au projet, modifiés directement à leur emplacement d'origine. ([06](06-documents.md#4-fichiers-externes)) |
| **GGUF** | Format de fichier de modèle utilisé par llama.cpp. |
| **Harnais** | Logiciel qui entoure le modèle : outils, autorisations, affichage ; Bionic en est un. |
| **Introspection** | Capacité de l'agent à relire des messages antérieurs ou d'autres sessions (`@`). |
| **JIT** (*just-in-time*) | Chargement d'un modèle à la première requête qui le demande. |
| **LM Link** | Liaison chiffrée entre appareils pour utiliser les modèles de l'un depuis l'autre. |
| **MCP** | *Model Context Protocol* : protocole de connexion d'outils externes à un agent. ([08](08-competences-et-mcp.md#5-serveurs-mcp)) |
| **Modèle racine** (*root model*) | Modèle par défaut des nouvelles sessions (Réglages → Agent). |
| **Palette `@`** | Liste de références (fichiers, compétences, sessions) ouverte par la saisie de `@`. |
| **Projet** | Regroupement de sessions et de fichiers autour d'un objectif. |
| **Remote** (modèle) | Modèle exécuté sur un autre appareil via LM Link. |
| **Session** | Conversation et fil de tâche, dans un projet ou hors projet. |
| **Shell** | Interpréteur de commandes (PowerShell sous Windows). |
| **Shell Judge** | Étage déterministe d'Auto Review : analyse la structure de la commande et approuve celles dont le pire effet est sûr, sans appel de modèle ([12](12-auto-review.md#3-étage-1--shell-judge)). |
| **Shell Reviewer** | Sous-agent d'Auto Review : note le risque (`low`, `high`, `too_destructive`), l'autorisation et la correction d'une commande ([12](12-auto-review.md#4-étage-2--shell-reviewer)). |
| **Sous-agent** | Agent auxiliaire lancé par l'agent principal (exploration de fichiers, analyse d'images). |
| **Sous-agent de vision** | Modèle désigné pour analyser les images à la place d'un modèle texte seul. |
| **Vérification automatique** | Mode shell : commandes sûres approuvées automatiquement, autres examinées par un agent de vérification distinct. |
| **Voxtral** | Modèle de transcription vocale multilingue (Mistral AI) utilisé pour la dictée. |
| **ZDR** | *Zero Data Retention* : engagement de non-conservation des données par le service cloud. |
