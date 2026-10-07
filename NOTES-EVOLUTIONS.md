# Notes d'évolution du projet (demandes de l'utilisateur)

> Fichier de suivi : regroupe les souhaits exprimés pour éviter de les répéter. Les points marqués **[à valider]** attendent l'audit proposé avant toute modification.
> Dernière mise à jour : 7 octobre 2026.

## 1. Poste de test sans GPU dédié : compléter sur une machine avec GPU

Le poste utilisé pour la production des captures n'a **ni GPU dédié ni VRAM** (processeur Intel avec GPU intégré partageant la RAM). Conséquence : certains écrans et comportements n'ont pas pu être montrés.

**À compléter sur une machine avec GPU dédié** (le projet sera importé sur cette machine) :

- Dans **Model Search → Download Options** (LM Studio) et **Explorer** (Bionic) : montrer et expliquer les **indicateurs d'adéquation matérielle**, en particulier :
  - vert : modèle entièrement logeable en mémoire GPU (*Full GPU Offload Possible*) ;
  - réparti entre VRAM et RAM (*Partial GPU Offload Possible*) ;
  - rouge : trop volumineux, chargement impossible ou déconseillé (*Likely too large…*) ;
  - **capturer chacun des trois états** (impossible sans carte graphique dédiée) ;
- mesurer l'effet réel du curseur **GPU Offload** (vitesse selon le nombre de couches sur GPU) ;
- comparer moteurs **CUDA / Vulkan / CPU** ;
- reprendre les mesures de vitesse et de mémoire (les valeurs actuelles sont celles d'un GPU intégré).

Dans les manuels actuels, préciser partout que l'indicateur vert observé correspond à un **GPU intégré** (mémoire partagée) et non à une carte dédiée.

## 2. Plan et nommage des manuels LM Studio **[à valider]**

Les titres actuels de certains manuels ne sont pas assez parlants. Principe : **titres directs, centrés sur la tâche**.

| Actuel | Problème | Orientation souhaitée |
|---|---|---|
| 00 Notions fondamentales | Correct | Conserver |
| 01 Prise en main | Correct | Conserver (« le logiciel, ce qu'il fait, les bases ») |
| 02 Modèles : trouver, télécharger, gérer | Titre peu clair | Orienter vers **« Sélectionner et télécharger un modèle pertinent »** : comment chercher, comment juger qu'un modèle convient |
| 04 Chat et paramètres d'inférence | Titre à clarifier | Orienter vers **« Paramétrer l'inférence »** |
| 08 OCR avec OlmOCR 2 7B | Trop spécifique à un modèle | **Fusionner** avec le manuel 05 en un manuel « Vision, images et OCR » ; garder de l'OCR les **paramètres** et la méthode de choix |

## 3. Manuel « Sélectionner et télécharger un modèle » **[à valider]**

- Remplacer l'exemple **OlmOCR 2 7B** par un modèle généraliste courant, capable de tourner **entièrement en mémoire GPU** dans une quantification adaptée (ex. *Gemma 4 E4B*, ou un modèle *Qwen*).
- Expliquer, sur la capture de **Download Options** (figure 5 du manuel 02) : les quantifications (les différents `Q`, `K`, `S/M/L`, `IQ`, etc.), la signification des **indicateurs vert / réparti / rouge** et ce que chacun implique.
- **Compléter la liste des quantifications** : les manuels n'en citent que quelques-unes (`Q4_K_M`…). Ajouter les autres formes (suffixes `L`, `XL`, `S`, `IQ…`, `_0`, `_1`, formats récents, QAT, variantes « dynamiques ») avec une explication vulgarisée, pour qu'un utilisateur ne soit pas perdu face à un nom inconnu.
- Préciser que le cas rouge / réparti ne peut pas être illustré sur le poste actuel (point 1).

## 4. Corrections ponctuelles

- **Manuel 02, section 3.2 (Onglets Load et Inference)** : rogner l'image de l'onglet **Load** (figure 3) : les trois quarts inférieurs sont vides. Vérifier aussi les autres images étroites du manuel pour supprimer les zones inutiles.

## 5. Vision et OCR : fusionner et recentrer **[à valider]**

- Fusion des manuels « vision » et « OCR OlmOCR » (voir point 2).
- Conserver : choix de résolution (jusqu'où cela fonctionne), paramètres, choix d'un bon modèle, signification de la quantification pour la précision.
- Montrer l'usage **dans le chat** : joindre une image, tester ce que le modèle sait faire (tableaux, mémoire de conversation…), comme démonstration d'une conversation LM Studio.

## 6. Fonctionnalités avancées : audit et ajout **[à valider]**

L'impression est qu'on est passé à côté de nombreuses fonctionnalités, pour **LM Studio** comme pour **Bionic** (MCP, outils, plugins, etc.).

- Rechercher sur le web les fonctionnalités avancées de LM Studio et de Bionic, et la manière dont les utilisateurs s'en servent réellement.
- S'appuyer sur la documentation de la partie **Developer** de LM Studio.
- Les intégrer aux manuels : d'abord les usages (chat, conversation, image), puis les aspects plus techniques.
- À traiter de préférence dans une **nouvelle conversation**.

## 7. Méthode de travail souhaitée

1. **Audit d'abord** : réponse claire et structurée (points à ajouter, points à modifier) avant toute modification.
2. Validation par l'utilisateur, puis exécution selon sa sélection.
3. Ton impersonnel et direct, contenu générique illustré d'exemples, public novices et experts (voir mémoire du projet).

## 8. Audit du 7 octobre 2026 (en attente de validation)

- Recherche web consignée dans [RECHERCHE-fonctionnalites-avancees.md](RECHERCHE-fonctionnalites-avancees.md) : fonctionnalités avancées de LM Studio 0.4.25 et de Bionic 1.1.7, quantifications, badges d'adéquation matérielle, usages réels.
- L'audit structuré (points à modifier, points à ajouter, ordre proposé) a été remis dans la conversation ; la sélection de l'utilisateur sera reportée ici avant exécution.
- Constat à garder : les **badges vert / orange / rouge ne sont pas définis par la documentation officielle** (sens issus de sources tierces) : à vérifier sur la machine avec GPU.

## 9. Exécution du lot 1 (7 octobre 2026)

Sélection retenue : **lot 1 = A, B, C1-C2, F** (ordre proposé dans l'audit), sans téléchargement de modèle. Les lots 2 et 3 (D, E) restent à valider.

| Point | Statut | Détail |
|---|---|---|
| A1 Rognage des images | Fait | Figure 3 du manuel 02 (344 × 1330 → 344 × 380) et trois autres images à fond vide (LM Studio 01 et 04, Bionic 03). |
| A2 Vert = GPU intégré | Fait | Précisé dans le manuel 02 (section 6), le manuel 05 et le manuel Bionic 04. |
| A3 / B1 / B3 Renommages | Fait | 02 « Sélectionner et télécharger un modèle » ; 04 « Paramétrer l'inférence ». |
| B2 Exemple du manuel 02 | Fait | *Gemma 4 E4B* (dépôt `unsloth/gemma-4-E4B-it-GGUF`, lecture seule). Qwen non traité (aucun téléchargement autorisé). |
| B4 Fusion vision + OCR | Fait | Manuel 05 « Vision, images et OCR » (ancien 08 intégré en section 7, ancien 08 supprimé) ; conversation multi-tours ajoutée (section 3.3). |
| Renumérotation | Fait | 08 = recettes, 09 = dépannage (anciens 09 et 10). Liens et index mis à jour. |
| C1 / C2 Quantifications | Fait | Manuel 02 section 5 (catalogue complet, formats non chargeables) ; manuel 00 section 4.2 ; glossaire. |
| C3 Badges | Partiel | Section 6 du manuel 02 rédigée avec **les trois états capturés sur le poste actuel** : vert, **bleu** (« Partial », et non orange) et rouge (« Likely too large »). Reste à faire sur machine avec GPU dédié : seuils réels selon la VRAM, effet du contexte, vitesse selon l'offload. |
| F Nuances | Fait | Divergence documentation / terrain sur la cohabitation (Bionic 01), taille du modèle vocal (Bionic 09), contexte par défaut LM Studio / Bionic (manuel 03). « Show model load logs » : mention absente des manuels, rien à corriger. |

Constats nouveaux : dans la liste *Download Options* d'un dépôt Hugging Face, les lignes préfixées **Mtp** sont des modèles brouillons (2 Go) et la ligne recommandée par défaut peut être l'une d'elles ; pour *Gemma 4 E4B*, passer de Q8_0 à Q3_K_S ne divise la taille que par 1,75 ; le badge « partiel » apparaît pour le BF16 de 16,97 Go sur 17,9 Go de « VRAM » déclarés.

## 10. Exécution du lot 2 (7 octobre 2026)

Sélection retenue : **lot 2 = D1, D2, D5, D6, E1, E6**. Les lots 3 (D3, D4, D7 à D10, E2 à E5) et E7 (dictée) restent hors périmètre. Aucun téléchargement de modèle, aucune installation de paquet, aucun compte connecté.

| Point | Statut | Livrable | Constats principaux |
|---|---|---|---|
| D1 MCP et outils | Fait | LM Studio, manuel 10 | Serveur MCP local écrit pour l'occasion (`outils/serveur_mcp_demo.py`, stdio et HTTP) ; confirmation des appels, refus avec motif, « Always allow » (règle `serveur:outil` dans `settings.json`) ; fiabilité mesurée : *E4B* 32/32 avec 5 outils, 48/52 avec 17 outils, *12B QAT* 36/39, mêmes échecs (argument manquant deviné) ; motif de refus pris pour le résultat de l'outil |
| D2 Sécurité du serveur | Fait | LM Studio, manuel 11 | Jetons factices créés, testés (401 / 403 / 200, `x-api-key`), supprimés ; permissions MCP des jetons ; CORS testé (activé puis désactivé) ; règles pare-feu « LM Studio » en profil Public ; *Serve on Local Network* et `--bind` **jamais activés** ; secrets de `mcp.json` stockés en clair et recopiés |
| D5 API avancée | Fait | LM Studio, manuel 12 | Chat à état (branches, `store: false`, 30 jours) ; `/v1/responses` ignore `text.format` ; `/v1/messages` : réponse **vide** après `tool_result` avec outils redéclarés (E4B), `count_tokens` absent (HTTP 200 + erreur) ; sortie structurée : réflexion possible malgré `reasoning_effort: none` ; `tool_choice` nommé refusé ; `context_length` différent = seconde instance ; MCP par l'API : permission du jeton **et** réglage requis, serveurs à la volée limités aux adresses publiques |
| D6 Intégrations | Fait (partiel) | LM Studio, manuel 13 | Réglages fournis pour sept outils [Source / Source tierce] ; **aucun outil lancé** (installation, compte ou Docker requis) : rejeu des requêtes équivalentes (10 requêtes) ; clés factices (`lm-studio`, `dummy-api-key`) refusées dès que l'authentification est active |
| E1 Auto Review | Fait (partiel) | Bionic, manuel 12 | Mode d'approbation lu dans le journal des sessions (`approvalType`) ; Shell Judge sur `git status`, `git log`, `python --version` ; Shell Reviewer sur les commandes enveloppées dans `powershell -Command` ; faux positif du vérificateur avec *E4B* ; instruction personnalisée qui fait remonter une suppression demandée ; **`too_destructive` non reproduit** (aucun test sans danger) ; les outils de fichiers ne passent pas par Auto Review |
| E6 Compétences | Fait | Bionic, manuel 13 | Essai témoin / `@` / déclenchement automatique ; installation globale par `@Install Skill` (approbations) ; création assistée **non fiable** avec les modèles locaux (E4B : fichier mal placé, sans en-tête, annonce de réussite fausse ; 12B : interrompu après plus de 15 minutes) ; palette `@` sensible aux accents ; compétence de projet immédiate |

Fichiers modifiés : `docs/lmstudio/06-serveur-local-et-api.md`, `docs/bionic/03-reglages.md`, `07-code-et-shell.md`, `08-competences-et-mcp.md`, index (`README.md`, `docs/README.md`, `docs/bionic/README.md`, `outils/README.md`) et deux glossaires. Contrôle : `outils/verifier_docs.py` (7 alertes « ton », toutes des citations d'interface).

**Reste à la charge de l'utilisateur** : supprimer à la main les sessions de test du projet Bionic « Démo code » (menu **…** natif non pilotable) : « Mise à jour des tâches et validations (Finance) », « Suggestion de nom pour la conversation », « Migration du rapport mensuel et validation budgétaire », « Installation de Compétence Locale », « Création de Compétence Globale (Resume en Trois Points) », « Exécution de commande… » et les « Session sans nom » de ce projet (ne pas toucher à « Débogage de tarifs.py » ni à « Débogage et Correction de Code Python »).

## 11. Exécution partielle du lot 3 (7 octobre 2026)

Sélection : seulement ce qui se fait **sans compte, sans installation, sans téléchargement et sans GPU dédié**. Livrables : [manuel LM Studio 14](docs/lmstudio/14-personnaliser-les-modeles.md) et [manuel Bionic 14](docs/bionic/14-commandes-compaction-navigateur.md).

| Point | Statut | Constats principaux |
|---|---|---|
| D7 Presets, Hub, `model.yaml`, défauts par modèle, gabarit | Fait | Défaut de modèle (prompt système) **appliqué aux requêtes d'API sans message système** et supplanté par un message système explicite (mesuré) ; gabarit modifiable dans *Load → Advanced → Chat Template* (anciens emplacements de l'onglet *Inference* désormais renvois) ; vrai `model.yaml` analysé (hub\models) ; **modèle virtuel déposé à la main non reconnu** (absent de `lms ls` et de `/v1/models`, même après redémarrage). |
| D10 Divers (conversations, Mermaid) | Fait | Conversations en JSON (`.lmstudio\conversations`), chaque fichier embarque le gabarit du modèle (≈ 18 Ko à vide) ; rendu Mermaid avec barre d'outils ; diagramme libre de Gemma 4 E4B **invalide** (icône rouge), diagramme simple rendu. |
| E2 Points de sauvegarde | Non reproduit | Aucune interface repérée ; recommandation : Git. |
| E4 Compaction, sous-agents, introspection | Partiel | `/compact` mesuré (7,2 k → 6,9 k, ≈ 90 s, E4B) ; menu `/` complet relevé ; sous-agents et introspection restent décrits par la documentation (manuels 03 et 08). |
| E5 Canvas, éditeur, aperçus | Non reproduit ; navigateur intégré testé | Page locale affichée ; l'agent (E4B) **ouvre** l'adresse mais **ne lit pas** le contenu. |
| D3 LM Link, D4 llmster, D8 performance GPU, D9 plugins et SDK, E3 cloud, E7 dictée | **Non traités** | Compte requis (D3, E3), absent de la 0.4.25 (`lms daemon` / llmster), GPU dédié (D8), Node.js absent (D9), micro et modèle vocal à autoriser (E7). |

Rien n'a été téléchargé ni installé ; aucun compte connecté. Le serveur web de démonstration (port 3000, 127.0.0.1) a été arrêté.

**À supprimer à la main** (menu « … » natif de Bionic, non pilotable) : sessions de test du projet « Démo code » dont « Tâche de navigation et extraction… » et la session compactée ; elles s'ajoutent à celles de la section 10.
