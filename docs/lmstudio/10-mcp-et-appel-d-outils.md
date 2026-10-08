# Manuel 10 — MCP et appel d'outils

> **Objet** : permettre à un modèle local d'agir (convertir, lire un fichier, interroger un service) grâce aux **outils**, déclarer des serveurs **MCP**, confirmer ou refuser les appels et mesurer la fiabilité d'un modèle avant de lui confier un outil.
> **Prérequis** : [Manuel 03](03-charger-un-modele.md) (contexte), [Manuel 04](04-parametrer-l-inference.md) (réflexion). Les appels par l'API sont détaillés au [Manuel 12](12-api-avancee.md) et la sécurité au [Manuel 11](11-securiser-le-serveur.md).
> **Version décrite** : LM Studio 0.4.25, Windows 11.
> **Statut des informations** : [Vérifié] observé ou mesuré sur le poste de test (Intel Core Ultra 7 255H, 31 Go de RAM, **GPU intégré**, modèles *Gemma 4 E4B* et *Gemma 4 12B QAT*) ; [Source] documentation officielle ; [Source tierce] ; [Estimation] ; [À tester].
> **Aucun serveur MCP tiers n'a été installé** : tous les essais utilisent un petit serveur écrit pour l'occasion ([`outils/serveur_mcp_demo.py`](../../outils/serveur_mcp_demo.py), bibliothèque standard de Python).

---

## Sommaire

1. [Principe](#1-principe)
2. [Déclarer un serveur MCP : `mcp.json`](#2-déclarer-un-serveur-mcp--mcpjson)
3. [Un serveur MCP minimal pour tester](#3-un-serveur-mcp-minimal-pour-tester)
4. [Utiliser les outils dans le chat](#4-utiliser-les-outils-dans-le-chat)
5. [Confirmer, refuser, autoriser](#5-confirmer-refuser-autoriser)
6. [Fiabilité et limites des petits modèles](#6-fiabilité-et-limites-des-petits-modèles)
7. [Serveurs distants, authentification et partage](#7-serveurs-distants-authentification-et-partage)
8. [Dépannage](#8-dépannage)

---

## 1. Principe

### Essentiel

Un modèle de langage ne produit que du texte. Un **outil** est une fonction que l'application peut exécuter à sa place (convertir une unité, lire un fichier, interroger un ticket). Le modèle reçoit la **liste des outils** (nom, description, paramètres) ; s'il juge qu'un outil est utile, il répond par une **demande d'appel** structurée (nom + arguments en JSON). L'application exécute l'outil, renvoie le **résultat** au modèle, qui rédige la réponse finale.

![Boucle d'appel d'outil](../img/lmstudio/10-mcp/00-boucle-appel-outil.png)
*Figure 1 — Le modèle demande, l'application confirme et exécute, le résultat revient dans le contexte.*

**MCP** (*Model Context Protocol*) est un protocole ouvert qui standardise la façon dont une application (l'**hôte**) découvre et appelle les outils d'un **serveur**. LM Studio est un hôte MCP : un même serveur peut servir plusieurs applications (LM Studio, Bionic, autres clients) [Source].

| Terme | Rôle | Exemple (poste de test) |
|---|---|---|
| **Hôte** | Application qui parle au modèle et appelle les serveurs | LM Studio |
| **Serveur MCP** | Programme qui expose des outils | `demo-notes` (local), `demo-http` (distant) |
| **Outil** | Fonction appelable avec des arguments | `convertir_temperature(valeur, de, vers)` |
| **Appel d'outil** | Demande du modèle, exécutée par l'hôte | `{"de":"C","valeur":100,"vers":"F"}` |

> **Exemple** — Question : « Convertis 100 degrés Celsius en Fahrenheit en utilisant l'outil disponible. » Le modèle demande `convertir_temperature` avec `de = "C"`, `valeur = 100`, `vers = "F"` ; le serveur renvoie `100 C = 212.0 F` ; le modèle répond : « 100 degrés Celsius équivaut à 212.0 degrés Fahrenheit. » [Vérifié]

### Pour aller plus loin

- **Deux niveaux de prise en charge** : un modèle entraîné à l'appel d'outils avec un modèle de conversation adapté (*native*) appelle les outils de façon fiable ; les autres reçoivent un prompt de substitution (*default*) et donnent des résultats variables [Source]. Le bandeau *Capabilities* d'un modèle indique « Tool use » quand le modèle est reconnu [Vérifié].
- **Un outil n'est pas un plugin.** Les *plugins* de LM Studio (par exemple `js-code-sandbox`, `rag-v1`) apparaissent dans le même panneau *Integrations* ; les serveurs MCP y apparaissent sous le préfixe `mcp/` [Vérifié].
- **Coût en contexte** : chaque outil déclaré est ajouté au prompt de **chaque** requête, utilisé ou non ([section 6](#6-fiabilité-et-limites-des-petits-modèles)).

---

## 2. Déclarer un serveur MCP : `mcp.json`

### Essentiel

Les serveurs sont décrits dans le fichier **`%USERPROFILE%\.lmstudio\mcp.json`** (vide par défaut : `{"mcpServers": {}}`) [Vérifié]. Accès depuis l'application : panneau *Integrations* (icône d'outils, à droite) → **Install** → **Edit mcp.json**, ou bouton **mcp.json** de la page *Developer*.

![Avertissement à l'ouverture de l'éditeur](../img/lmstudio/10-mcp/01a-avertissement-mcp.png)
*Figure 2 — Avertissement affiché à l'ouverture de l'éditeur : ① texte, ② case « ne plus afficher », ③ validation.*

Le texte de l'avertissement : un serveur MCP peut exécuter du code arbitraire sur l'ordinateur ; ne jamais ajouter un serveur de source non fiable [Vérifié].

![Éditeur mcp.json](../img/lmstudio/10-mcp/01b-editeur-mcp-json.png)
*Figure 3 — Éditeur intégré : ① contenu, ② rappel « Saving this file will reload your MCP servers », ③ enregistrement (Ctrl + S), ④ abandon (Ctrl + Échap).*

L'enregistrement **recharge** les serveurs. Une modification du fichier faite **hors de l'application** est aussi détectée : l'ajout d'une entrée a affiché la notification « MCP Server Added! » et la liste d'intégrations s'est mise à jour sans redémarrage [Vérifié].

### Les deux formes d'entrée

```json
{
  "mcpServers": {
    "demo-notes": {
      "command": "python",
      "args": ["C:\\chemin\\vers\\serveur_mcp_demo.py"],
      "env": { "PYTHONIOENCODING": "utf-8" }
    },
    "demo-http": {
      "url": "http://127.0.0.1:8765/mcp",
      "headers": { "Authorization": "Bearer jeton-distant-factice" }
    }
  }
}
```

| Champ | Forme | Rôle |
|---|---|---|
| `command`, `args`, `env` | **Local** (stdio) | Programme lancé par LM Studio avec les droits de l'utilisateur ; dialogue par entrée et sortie standard |
| `url`, `headers` | **Distant** (HTTP) | Service joint par le réseau ; `headers` transmet une authentification |

> **Exemple (poste de test)** — Le nom d'entrée `demo-notes` devient l'intégration `mcp/demo-notes` ; `demo-http` devient `mcp/demo-http`. Les deux ont exposé les cinq mêmes outils [Vérifié].

### Pour aller plus loin

- **Notation** : format dit « Cursor » (`mcpServers`), compatible avec les fichiers d'autres applications [Source]. Pour un copier-coller, ne reprendre que le contenu entre `"mcpServers": {` et l'accolade fermante correspondante [Source].
- **Lien d'installation** : `lmstudio://add_mcp?name=<nom>&config=<JSON de l'entrée en base64>` ouvre LM Studio et propose l'ajout du serveur [Source ; non testé : à tester].
- **OAuth** : pour un service distant qui l'exige, l'application ouvre le navigateur sur la page d'autorisation et conserve le jeton ; un client OAuth personnalisé s'ajoute par un objet `auth` dans l'entrée, avec la redirection `http://127.0.0.1:33389/mcp-oauth-callback` [Source ; non testé, aucun compte connecté].
- **Secrets en clair** : les `headers` et `env` d'`mcp.json` sont stockés **en clair**, et recopiés dans `%USERPROFILE%\.lmstudio\.internal\last-synced-mcp-state.json` [Vérifié]. Ne pas partager ces fichiers ; préférer des jetons à portée limitée.
- **Gros serveurs** : certains serveurs exposent des dizaines d'outils et saturent le contexte d'un petit modèle ([section 6](#6-fiabilité-et-limites-des-petits-modèles)). Les outils peuvent être décochés un par un.

---

## 3. Un serveur MCP minimal pour tester

### Essentiel

Pour essayer MCP **sans rien installer**, un serveur de quelques dizaines de lignes suffit : [`outils/serveur_mcp_demo.py`](../../outils/serveur_mcp_demo.py). Il n'utilise que la bibliothèque standard de Python et expose cinq outils inoffensifs.

| Outil | Rôle | Effet de bord |
|---|---|---|
| `convertir_temperature` | Celsius, Fahrenheit, Kelvin | Aucun |
| `calculer_statistiques` | Minimum, maximum, moyenne, médiane | Aucun |
| `lister_notes` | Noms des fichiers du dossier fictif `outils/mcp_demo_notes/` | Lecture |
| `lire_note` | Contenu d'une note (sortie du dossier refusée) | Lecture |
| `ecrire_note` | Crée un fichier `.txt` dans ce dossier | **Écriture** |

Chaque appel est consigné dans `outils/resultats/mcp_demo_appels.log` : la preuve qu'un outil a réellement été appelé ne dépend pas de ce que le modèle affirme.

### Pour aller plus loin

Un serveur local **stdio** lit une ligne JSON par message sur l'entrée standard et répond par une ligne JSON sur la sortie standard (JSON-RPC 2.0). Trois méthodes suffisent :

| Message du client | Réponse du serveur |
|---|---|
| `initialize` | Version du protocole, capacités (`tools`), nom du serveur |
| `tools/list` | Liste des outils avec `name`, `description`, `inputSchema` (JSON Schema) |
| `tools/call` | `{"content":[{"type":"text","text":"…"}],"isError":false}` |

Échanges réels, rejoués par [`outils/tester_serveur_mcp.py`](../../outils/tester_serveur_mcp.py) (client minimal, sans application hôte) [Vérifié] :

```text
>> {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"convertir_temperature","arguments":{"valeur":100,"de":"C","vers":"F"}}}
<< {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"100 C = 212.0 F"}],"isError":false}}
```

Règles apprises pendant l'écriture :

- **Ne rien écrire d'autre sur la sortie standard** que des messages JSON (les journaux vont sur la sortie d'erreur ou dans un fichier) ; un `print` de débogage casse le protocole.
- **Signaler une erreur d'outil par `isError: true`** et un texte explicite : le modèle lit ce texte et peut corriger son appel.
- **Valider les chemins** : `lire_note("..\\..\\README.md")` doit être refusé, ce qui a été vérifié ([Manuel 11](11-securiser-le-serveur.md#6-ce-quil-ne-faut-pas-exposer)).
- Le **mode distant** du même script (`python serveur_mcp_demo.py --http 8765`) écoute sur `127.0.0.1` et traite un message JSON-RPC par requête POST [Vérifié].

---

## 4. Utiliser les outils dans le chat

### Essentiel

1. Charger un modèle capable d'outils ([Manuel 03](03-charger-un-modele.md)).
2. Panneau **Integrations** : activer l'interrupteur du serveur (`mcp/demo-notes`). Une pastille du même nom apparaît dans la zone de saisie.
3. Poser une question qui appelle un outil ; **confirmer** l'appel ([section 5](#5-confirmer-refuser-autoriser)).

![Panneau Integrations](../img/lmstudio/10-mcp/02-integration-mcp-outils.png)
*Figure 4 — Serveur déplié : ① interrupteur du serveur, ② politique globale (« Per Tool »), ③ outils exposés (cases à cocher), ④ politique de chaque outil (« Ask »), ⑤ rechargement de la liste.*

| N° | Élément | Rôle |
|---|---|---|
| ① | Interrupteur `mcp/<nom>` | Active le serveur **pour la conversation en cours** |
| ② | **Per Tool** | Politique de confirmation : par outil |
| ③ | Cases des outils | Un outil décoché n'est pas déclaré au modèle (gain de contexte, moins de risques) |
| ④ | **Ask** / **Always allow** | « Ask before running » : confirmation à chaque appel ; « Always allow » : exécution directe |
| ⑤ | Icône de rechargement | Relit la liste d'outils du serveur |

![Résultat d'un appel d'outil](../img/lmstudio/10-mcp/04-resultat-appel-outil.png)
*Figure 5 — Résultat : ① réflexion du modèle, ② appel (nom de l'outil et serveur), ③ arguments, ④ résultat, ⑤ réponse finale.*

Le bloc d'appel se déplie : les **arguments** et le **résultat brut** renvoyé par le serveur restent consultables après coup. C'est la source de vérité en cas de doute sur la réponse.

> **Exemple (poste de test)** — Trois consignes, un outil chacune, *Gemma 4 E4B*, réflexion active (par défaut dans le chat) [Vérifié] :
>
> | Consigne | Outil appelé | Arguments | Réponse |
> |---|---|---|---|
> | « Convertis 100 degrés Celsius en Fahrenheit… » | `convertir_temperature` | `de=C, valeur=100, vers=F` | 212.0 °F (réflexion : 8,3 s ; **GPU dédié : 4,1 s** au total, 139 tokens de réflexion) |
> | « Calcule la moyenne et la médiane de 12, 7, 9, 15, 3. » | `calculer_statistiques` | `nombres=[12,7,9,15,3]` | 9.2 et 9 (réflexion : 12,3 s ; **GPU dédié : 5,5 s** au total, 204 tokens de réflexion) |
> | « Lis la note reunion.txt et donne le budget alloué. » | `lire_note` | `nom=reunion.txt` | appel refusé volontairement ([section 5](#5-confirmer-refuser-autoriser)) |

### Pour aller plus loin

- **Un seul serveur à la fois par nom d'outil.** Deux serveurs qui exposent des outils de même nom (cas des deux serveurs de démonstration) rendent la désignation ambiguë pour le modèle : en désactiver un.
- ![Deux serveurs, local et distant](../img/lmstudio/10-mcp/02b-deux-serveurs-local-et-distant.png)
  *Figure 6 — Un serveur local (`mcp/demo-notes`, ①) et un serveur distant (`mcp/demo-http`, ②) déclarés ensemble ; ③ outils du premier.*
- **Durée** : la réflexion précède chaque appel (8 à 12 s sur le GPU intégré ; **4 à 5,5 s sur le GPU dédié**, mesure par l'API). Désactiver la réflexion accélère nettement (**0,8 s** sur le GPU dédié pour les mêmes consignes, appels corrects), au prix d'une fiabilité parfois moindre ([Manuel 04](04-parametrer-l-inference.md#6-raisonnement-thinking)).

---

## 5. Confirmer, refuser, autoriser

### Essentiel

Avant chaque exécution, LM Studio **suspend** la génération et affiche la demande. Rien n'est exécuté sans réponse.

![Confirmation d'un appel](../img/lmstudio/10-mcp/03-confirmation-appel-outil.png)
*Figure 7 — « Model wants to call » : ① serveur activé, ② outil demandé, ③ arguments, ④ Proceed, ⑤ Deny, ⑥ « Always allow ».*

| N° | Élément | Effet |
|---|---|---|
| ③ | **Arguments** + bouton **Edit** | Lire, et au besoin **corriger**, les arguments avant l'exécution [Source] |
| ④ | **Proceed** (Ctrl + Entrée) | Exécute l'appel |
| ⑤ | **Deny** (Ctrl + Échap) | Refuse ; le modèle est informé du refus |
| ⑤ | **Deny with Reason…** | Refuse avec un **motif** transmis au modèle |
| ⑥ | **Always allow `<outil>` from `<serveur>`** | Autorise cet outil sans confirmation à l'avenir |
| ⑥ | **Always allow any tool from `<serveur>`** | Autorise tous les outils du serveur |

**Lire la confirmation, c'est lire trois choses** : le **nom** de l'outil (est-ce bien celui attendu ?), le **serveur** (local ou distant ?), les **arguments** (chemin, destinataire, quantité). Un chemin qui sort du dossier prévu ou un argument que la consigne ne justifie pas est un motif de refus.

### Refuser avec un motif

![Refus avec motif](../img/lmstudio/10-mcp/05-refus-avec-motif.png)
*Figure 8 — Saisie du motif : ① champ (prérempli « Error: User declined the tool call. »), ② retour, ③ envoi.*

![Après le refus](../img/lmstudio/10-mcp/06-apres-refus.png)
*Figure 9 — Après un refus : ① ligne « Tool call … denied by user », ② réponse du modèle, ③ conclusion.*

> **Constat (poste de test)** — Motif saisi : « Refusé : cette note est confidentielle, ne pas la lire. » Le journal du serveur ne contient **aucun** appel `lire_note` : le refus a bien empêché l'exécution. Mais *Gemma 4 E4B* a répondu : « Le contenu de la note "reunion.txt" indique que : "Refusé : cette note est confidentielle, ne pas la lire." » : le modèle a pris le **motif du refus pour le contenu du fichier** [Vérifié]. Conséquence : un refus protège l'exécution, **pas la cohérence de la réponse** ; relire la réponse d'un petit modèle après un refus.

### « Always allow » : persistance et retrait

![Always allow](../img/lmstudio/10-mcp/07-toujours-autoriser.png)
*Figure 10 — Cocher ① (un outil) ou ② (tout le serveur), puis ③ Proceed.*

Cocher la case enregistre une règle dans `settings.json`, clé `chat.skipToolConfirmationPatterns`, au format `<serveur>:<outil>` [Vérifié] :

```json
"skipToolConfirmationPatterns": ["mcp/demo-notes:calculer_statistiques"]
```

Les appels suivants du même outil sont exécutés **sans dialogue** (vérifié : la consigne « Donne le minimum, le maximum et la moyenne de 4, 8, 15, 16, 23, 42 » a produit l'appel, consigné dans le journal du serveur, sans demande de confirmation).

![Appel autorisé sans dialogue](../img/lmstudio/10-mcp/08-appel-autorise-sans-dialogue.png)
*Figure 11 — Appel exécuté directement ; le bloc reste dépliable pour relire arguments et résultat.*

La liste des autorisations permanentes se gère dans **Settings → Integrations → Tool Call Confirmation** :

![Réglage Tool Call Confirmation](../img/lmstudio/10-mcp/09-reglages-confirmation.png)
*Figure 12 — ① liste des outils autorisés sans confirmation ; ② retrait d'une règle.*

Le retrait a été vérifié : la liste redevient vide et `skipToolConfirmationPatterns` repasse à `[]` [Vérifié].

### Pour aller plus loin

| Réglage | Valeur par défaut | Recommandation |
|---|---|---|
| `neverAskForToolConfirmation` (`settings.json`) | `false` | Laisser à `false` |
| Règles « Always allow » | Aucune | N'autoriser durablement que des outils **en lecture seule** et sans donnée sensible (par exemple `calculer_statistiques`) |
| Outils à effet de bord (écriture, suppression, envoi) | — | Toujours en « Ask », y compris pour un serveur de confiance |

- Les règles portent sur le couple **serveur + nom d'outil** (`mcp/demo-notes:calculer_statistiques`). La règle « any tool from `<serveur>` » couvre vraisemblablement aussi les outils ajoutés plus tard par une mise à jour du serveur [Estimation : forme exacte de la règle non relevée].
- L'avertissement général [Source] : relire les arguments, n'autoriser « une fois » que ce qui est compris.

---

## 6. Fiabilité et limites des petits modèles

### Essentiel

La documentation prévient que les petits modèles, ou ceux qui n'ont pas été entraînés à l'appel d'outils, peuvent produire des appels mal formés que LM Studio ne sait pas interpréter [Source]. Mesurer vaut mieux que supposer : [`outils/mesure_outils_fiabilite.py`](../../outils/mesure_outils_fiabilite.py) rejoue des consignes, vérifie l'outil appelé **et** la valeur des arguments, sans rien exécuter.

> **Exemple (poste de test, GPU intégré)** — *Gemma 4 E4B* (7,5 Md de paramètres, Q4_K_M), `/v1/chat/completions`, `reasoning_effort = none`, température 0,7. Consignes en français : trois conversions ou calculs, une liste, une lecture, une écriture, deux questions **sans** outil attendu ; chaque consigne répétée 4 fois [Vérifié].
>
> | Configuration | Essais | Corrects | Durée moyenne |
> |---|---|---|---|
> | **5 outils** déclarés | 32 | **32 (100 %)** | 4,3 s (GPU dédié : **1,1 s**) |
> | **17 outils** déclarés (12 outils proches ajoutés : `calculer_moyenne`, `convertir_longueur`, `supprimer_note`…) | 52 | **48 (92,3 %)** | 2,8 s (GPU dédié : **0,8 s**) |
>
> **Rejeu sur le poste à GPU dédié (7 octobre 2026)**, mêmes consignes et mêmes seuils, trois modèles installés [Vérifié] : *Gemma 4 E4B* (Q8_0) **32/32** et **48/52** ; *Gemma 4 26B A4B* **32/32** (4,3 s en moyenne) et **48/52** (2,6 s) ; *Qwen3.8 27B* **32/32** (6,8 s) et **49/52** (94,2 % ; 5,4 s). **Les échecs portent sur la même consigne** (« Convertis 100 en Fahrenheit. » : unité de départ devinée) pour les trois modèles : la fiabilité mesurée **ne dépend pas de la taille** du modèle sur ce test, seule la **vitesse** change.
>
> Les quatre échecs de la seconde série portent sur **une seule consigne** : « Convertis 100 en Fahrenheit. » (unité de départ absente). Le modèle a **deviné** `de = "C"` au lieu de demander l'unité. Les deux consignes sans outil attendu (« capitale du Portugal », « faut-il une veste à 20 degrés ? ») n'ont déclenché **aucun appel inutile**.

| Constat | Détail | Parade |
|---|---|---|
| **Arguments devinés** | Un paramètre absent de la consigne est inventé plutôt que demandé | Rédiger des descriptions d'outil qui disent quand **demander** ; relire les arguments à la confirmation |
| **Refus mal interprété** | Le motif d'un refus est repris comme résultat ([section 5](#5-confirmer-refuser-autoriser)) | Relire la réponse suivant un refus |
| **Coût en contexte** | Voir ci-dessous | Décocher les outils inutiles ; contexte ≥ 8 192 |
| **Annonce sans appel** | Dans Bionic, le même modèle a annoncé avoir écrit un fichier sans appel réel ([Manuel Bionic 11](../bionic/11-recettes-et-depannage.md)) | Vérifier l'effet (fichier, journal du serveur), pas l'annonce |
| **Réflexion** | 8 à 12 s avant chaque appel avec la réflexion active sur GPU intégré (4 à 5,5 s sur GPU dédié) | Désactiver la réflexion pour les tâches simples |

**Coût en contexte** — tokens du prompt pour le message « Bonjour » avec *Gemma 4 E4B* [Vérifié] :

| Outils déclarés | Tokens du prompt |
|---|---|
| 0 | 10 |
| 1 | 153 |
| 5 | 427 |

Soit **environ 80 tokens par outil supplémentaire** pour des descriptions courtes (cinq outils ≈ 420 tokens, soit plus de 5 % d'un contexte de 8 192). Un serveur réel avec des descriptions longues et des schémas détaillés peut coûter plusieurs milliers de tokens [Estimation].

### Pour aller plus loin

- **Méthode de qualification d'un modèle** : (1) écrire 8 à 10 consignes représentatives, dont des cas **sans** outil et des cas **ambigus** ; (2) les rejouer 3 à 5 fois à température non nulle ; (3) compter les appels corrects, inutiles, mal formés ; (4) refaire la mesure avec le **vrai** jeu d'outils, dans la langue réelle.
- **Un outil à la fois** : certains modèles produisent plusieurs appels dans la même réponse. *Gemma 4 E4B* l'a fait correctement pour « Convertis 0 degré Celsius en Fahrenheit, puis 100 degrés Celsius en Kelvin » (deux appels dans un même message) [Vérifié, API].

**Comparatif de taille** — même série à 17 outils, 3 répétitions par consigne, mêmes réglages [Vérifié] :

| Modèle (poste de test, GPU intégré) | Essais | Corrects | Durée moyenne | Échecs |
|---|---|---|---|---|
| *Gemma 4 E4B* (7,5 Md, 6,3 Go) | 52 (4 répétitions) | 48 (92,3 %) | 2,8 s | « Convertis 100 en Fahrenheit. » : unité devinée |
| *Gemma 4 12B QAT* (12 Md, 7,2 Go) | 39 (3 répétitions) | **36 (92,3 %)** | **13,9 s** | **Les mêmes** : unité devinée (3 / 3) |

Le modèle plus grand n'a **pas** corrigé le défaut (arguments devinés) et s'est montré **cinq fois plus lent** sur ce poste. La taille n'est donc pas, à elle seule, un gage de fiabilité aux outils : la qualité des **descriptions d'outils** et la relecture des arguments comptent davantage. Chaque série est un échantillon réduit : les écarts d'un point ne sont pas significatifs.

---

## 7. Serveurs distants, authentification et partage

### Essentiel

Un serveur déclaré par `url` se comporte, dans le chat, comme un serveur local : mêmes cases, mêmes confirmations. La différence tient au **chemin des données** : les arguments et résultats traversent le réseau.

![Confirmation avec un serveur distant](../img/lmstudio/10-mcp/03b-confirmation-serveur-distant.png)
*Figure 13 — Appel de `convertir_temperature` sur `mcp/demo-http` (serveur HTTP local sur le port 8765) : le serveur `mcp/demo-notes` est désactivé pour éviter l'ambiguïté.*

Vérifications faites sur le poste de test [Vérifié] :

- L'en-tête `Authorization` déclaré dans `headers` arrive bien au serveur distant (le journal du serveur de démonstration consigne `auth=oui`).
- Un serveur distant à l'adresse `127.0.0.1` est accepté **dans le chat** par `mcp.json` ; en revanche l'API refuse, pour les serveurs transmis **dans la requête**, toute adresse non publique ([Manuel 12](12-api-avancee.md#8-mcp-par-lapi)).

### Pour aller plus loin

- **Service tiers réel** (GitHub, Notion, Sentry…) : authentification par `headers` (jeton) ou OAuth ; le contenu des appels est envoyé au service. Les règles de la [section 2](#2-déclarer-un-serveur-mcp--mcpjson) s'appliquent. Aucun service externe n'a été joint pendant la production de ce manuel.
- **MCP et API du serveur local** : les serveurs d'`mcp.json` ne sont accessibles aux clients de l'API que si le réglage *Allow calling servers from mcp.json* est activé, avec authentification obligatoire et un jeton qui porte la permission correspondante ([Manuel 11](11-securiser-le-serveur.md#4-permissions-des-jetons-et-mcp)).
- **Partage d'une configuration** : un `mcp.json` copié sur un autre poste y exécute les mêmes programmes ; vérifier les chemins et retirer les secrets.

---

## 8. Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| Le serveur n'apparaît pas dans *Integrations* | JSON invalide ; entrée sans `command` ni `url` | Rouvrir l'éditeur ; contrôler la syntaxe ; enregistrer |
| Serveur local « en échec » | Commande introuvable, mauvais chemin, programme qui écrit autre chose que du JSON sur la sortie standard | Lancer la commande à la main ; tester avec un client minimal ([section 3](#3-un-serveur-mcp-minimal-pour-tester)) |
| Accents corrompus dans les résultats | Encodage de la console du serveur | Variable `PYTHONIOENCODING=utf-8` dans `env` |
| Le modèle n'appelle jamais l'outil | Modèle sans prise en charge des outils ; descriptions vagues ; outil décoché | Vérifier « Tool use » dans *Capabilities* ; préciser la description ; mesurer ([section 6](#6-fiabilité-et-limites-des-petits-modèles)) |
| Le modèle annonce une action sans appel | Hallucination d'exécution | Contrôler le bloc d'appel et le journal du serveur |
| Appel avec des arguments erronés | Argument absent de la consigne, modèle trop petit | Corriger dans **Edit** ; reformuler la consigne ; modèle plus grand |
| Réponse vide après un résultat d'outil | Propre à certaines routes d'API (voir [Manuel 12](12-api-avancee.md#6-appel-doutils-par-lapi)) | Tester la route et le modèle choisis |
| Contexte saturé | Trop d'outils déclarés | Décocher les outils inutiles ; augmenter le contexte |
| Confirmation jamais demandée | Règle « Always allow » ou `neverAskForToolConfirmation` | *Settings → Integrations → Tool Call Confirmation* |
