# Manuel Bionic 10 — Sécurité, compte, cloud et API locale

> **Objet** : comprendre ce qui sort (ou non) de la machine, ce qui exige un compte, comment fonctionnent crédits et facturation, comment utiliser et sécuriser l'API locale, et quelle configuration retenir selon la sensibilité des données.
> **Prérequis** : [Manuel Bionic 00](00-notions-agent.md), [03](03-reglages.md).
> **Version décrite** : Bionic 1.1.7, Windows 11.
> **Statut des informations** : [Vérifié] observé ; [Source] documentation officielle ; [Estimation] ; [À tester]. **Aucun compte n'a été connecté** : les parties « compte » sont décrites d'après l'interface et la documentation.

---

## Sommaire

1. [Cartographie des flux de données](#1-cartographie-des-flux-de-données)
2. [Mode entièrement local](#2-mode-entièrement-local)
3. [Compte, crédits et facturation](#3-compte-crédits-et-facturation)
4. [LM Link](#4-lm-link)
5. [API locale](#5-api-locale)
6. [Navigateur, recherche web, sites autorisés](#6-navigateur-recherche-web-sites-autorisés)
7. [Menaces et parades](#7-menaces-et-parades)
8. [Configurations recommandées](#8-configurations-recommandées)
9. [Points non documentés à clarifier](#9-points-non-documentés-à-clarifier)

---

## 1. Cartographie des flux de données

| Fonction | Données qui quittent la machine ? | Destinataire | Compte requis |
|---|---|---|---|
| Modèle **local** | Non | — | Non |
| Dictée vocale (Voxtral) | Non (transcription locale) | — | Non |
| Projets, sessions, fichiers du projet | Non (stockage local) | — | Non |
| Téléchargement d'un modèle (**Explorer**) | Oui : requête de téléchargement | Hébergeur du modèle (Hugging Face) | Non |
| Mises à jour de l'application | Oui : vérification et téléchargement | Éditeur de l'application | Non |
| Modèle **Remote** (LM Link) | Oui : entre appareils liés (chiffré de bout en bout, annoncé) | Autre appareil de l'utilisateur | Oui (interface observée) |
| Modèle **Cloud** | Oui : consignes, fichiers lus, résultats d'outils | LM Studio Secure Cloud (ZDR) | Oui + crédits |
| **Recherche web** | Oui : requêtes de recherche, contenus de pages | Service de recherche intégré | Oui (« Connectez-vous… ») |
| Navigation sur un site **externe** | Oui | Le site consulté | Non (liste blanche, vide par défaut) |
| Serveur MCP distant | Oui : contenu des appels d'outils | Service du serveur MCP | Selon le service |

> **Constat (poste de test)** — pendant un téléchargement de modèle, Bionic avait **une connexion sortante** établie sur le port 443 (HTTPS). Les autres sockets de l'application étaient en **écoute sur 127.0.0.1 uniquement** (API locale 1234 et ports internes). Le trafic sortant **au repos** et les éventuelles données de télémétrie ne sont pas documentés [À tester] : voir [section 9](#9-points-non-documentés-à-clarifier).

---

## 2. Mode entièrement local

### Essentiel

Pour un travail **sans aucune sortie de données** :

| Élément | Réglage |
|---|---|
| Modèle | **Local** (téléchargé au préalable) |
| Recherche web | Désactivée (valeur par défaut) |
| Sites web autorisés | Liste vide (valeur par défaut) |
| Serveurs MCP | Aucun, ou serveurs locaux contrôlés |
| Compte | Non connecté |
| Mises à jour automatiques | Selon la politique informatique (téléchargement en arrière-plan) |
| Réseau | Possible de **couper** après téléchargement des modèles ; fonctionnement hors ligne attendu [Estimation : non testé réseau coupé] |

> **Exemple (poste de test)** — configuration utilisée pour toutes les démonstrations : modèle local *Gemma 4 E4B*, non connecté, recherche web désactivée, aucun site autorisé, aucun serveur MCP. Les tâches (rédaction d'un mémo, correction de code) ont été accomplies **sans compte**.

---

## 3. Compte, crédits et facturation

### Essentiel

- Un **compte LM Studio** est nécessaire pour : les modèles **cloud**, la **recherche web**, **LM Link** [Vérifié, Source].
- Connexion : Réglages → Général → **Compte** → **Se connecter** (la connexion s'achève dans le **navigateur**) [Source].
- Les **crédits** ne sont consommés **que** par les modèles cloud, selon le modèle choisi et le nombre de tokens traités. Les modèles locaux et distants n'en consomment pas [Source].

| Étape | Procédure [Source] |
|---|---|
| Voir la consommation | Réglages → **Facturation et utilisation** : crédits consommés sur 30 jours ; bouton d'actualisation. |
| Ajouter des crédits | Réglages → Général → Compte → **Manage plan** → page du compte LM Studio Hub → **Cloud Inference** → ajouter des crédits → vérifier le solde disponible → actualiser dans Bionic. |
| Compte de facturation | *Personnel* ; la gestion d'équipe ou d'organisation n'est pas décrite dans la documentation consultée. |

### Offres et prix

Offres affichées par la page officielle des prix de Bionic [Source : `lmstudio.ai/pricing`, consultée le 11 octobre 2026 ; prix en **dollars américains par mois**, sujets à changement].

| | **Free** | **Bionic+** | **Pro** |
|---|---|---|---|
| **Prix** | **0 $** | **20 $** par mois | **100 $** par mois |
| Positionnement | « Run local LLMs on your machine » | modèles open source hébergés aux États-Unis | « More included usage » (davantage d'usage inclus) |
| Agent Bionic (projets, sessions, code, documents, Auto Review) | Oui | Oui | Oui |
| Modèles **locaux** (moteurs llama.cpp et MLX) | Oui | Oui | Oui |
| Transcription vocale **hors ligne** | Oui | Oui | Oui |
| **LM Link** (modèles d'un autre appareil) | Oui, **5 appareils au plus** | Idem Free | Idem Free |
| **Recherche web** | **Limitée** | Complète, avec **extraction de pages** | Idem Bionic+ |
| **Modèles cloud** hébergés aux États-Unis (Kimi K3, GLM 5.3, DeepSeek V4 Flash, « et d'autres ») | **Non listés** dans l'offre | **Oui** | Oui |
| **Jetons « en gros » à tarif réduit** (*discounted bulk tokens*) | Non | Oui | Oui |
| **Limites d'usage** | — | Usage inclus (montant non publié) | **5 ×** celles de Bionic+ |
| **Accès anticipé** aux nouvelles fonctions | Non | Non | **Oui** |

**Ce que la formule Free permet** : tout ce que ces manuels ont testé (agent, projets, code, documents, compétences, serveurs MCP, Auto Review, API locale, dictée) avec des modèles **locaux**, sans abonnement ; LM Link jusqu'à 5 appareils ; recherche web limitée.

**Ce que la formule Free ne comprend pas** [Source] : les modèles open source **hébergés** (gros modèles tournant dans le *LM Studio Secure Cloud* — hébergement américain, sans conservation des données), la recherche web complète avec extraction de pages, les jetons à tarif réduit, les limites d'usage accrues, l'accès anticipé. **Aucune fonction d'agent n'est réservée aux offres payantes** sur la page : la différence porte sur **où le modèle tourne** (cloud ou machine locale) et sur la **quantité d'usage cloud**.

**Autres points de la page** :

- **Zero Data Retention** (rétention nulle) : consignes et réponses non conservées par le fournisseur ; la recherche web y est soumise, avec un avertissement : les requêtes web comportent leurs propres risques ; ne pas y mettre de données sensibles.
- **Crédits cloud** : ils couvrent l'usage **au-delà de l'allocation incluse** dans la formule. Les modèles locaux et distants ne consomment aucun crédit et n'exigent pas de facturation.
- **Équipes** : facturation centralisée des crédits d'inférence (création d'une *organisation* depuis le compte) ; **abonnements d'équipe** annoncés « bientôt ». La mention d'une offre *Enterprise* relevée sur certains sites tiers **n'apparaît pas** sur la page officielle.
- **Changement de formule** : depuis le tableau de bord du compte (Réglages → Général → Compte → *Manage plan*, voir le tableau ci-dessus).

**Points non publiés** [À tester] : montant de l'**allocation incluse** dans Bionic+ et Pro (le facteur « 5 × » est donné sans valeur de départ) ; possibilité d'**acheter des crédits cloud depuis la formule Free** (la documentation dit seulement que les modèles cloud exigent « un compte connecté avec facturation et des crédits disponibles ») ; contenu exact de « recherche web limitée » ; taxes et période de facturation ; durée de la préversion de LM Link. Les articles de blogs tiers donnent d'autres montants (12, 15 $) : **ignorés**, ils ne correspondent pas à la page officielle.

> **Ligne de conduite pour un usage gratuit** — rester sur la formule **Free** couvre l'ensemble des usages décrits dans ces manuels. Une formule payante ne devient utile que pour des **modèles trop gros pour le poste**, pour la **recherche web complète**, ou pour un **usage intensif** en nuage [Estimation d'après le contenu des offres]. Un compte n'est nécessaire que pour LM Link, la recherche web et le cloud ; aucun frais de compte n'apparaît sur la page des prix [Estimation].

### Pour aller plus loin

- Les montants des offres sont ceux de la page des prix : voir ci-dessus pour les **points non publiés** (aucune grille de prix par crédit ni de montant d'allocation).
- **Zero Data Retention** : les données envoyées au cloud sont traitées de façon **transitoire** et non conservées, et ne servent pas à entraîner des modèles [Source : annonce officielle]. Engagement contractuel du service : à valider avec le service juridique avant tout usage sur des données internes.
- Comportement lorsque les **crédits sont épuisés** (blocage, bascule vers un modèle local) : non documenté [À tester].

> **Recommandation de principe** — en contexte professionnel, **ne pas se connecter** avec un compte personnel pour traiter des données de l'organisation ; clarifier au préalable le cadre contractuel (compte d'organisation, hébergement, clauses de confidentialité).

---

## 4. LM Link

**LM Link** permet d'utiliser les modèles d'un autre appareil comme s'ils étaient locaux. Réglages → **LM Link** [Vérifié] :

1. **Se connecter** (compte LM Studio ; dans LM Studio 0.4.26, bouton *Login & Enable LM Link*).
2. **Lien** : créé automatiquement en 0.4.26 (l'étape « Créer un Link » vue en 0.4.25 a disparu de l'interface de LM Studio).
3. **Ajouter un autre appareil** : connecter la machine qui héberge les modèles.

Mise en place, commandes et protocole de vérification : [Manuel LM Studio 17](../lmstudio/17-lm-link.md). Garanties annoncées : **chiffrement de bout en bout** entre appareils associés ; compatibilité avec ordinateurs, stations dédiées, serveurs et machines virtuelles cloud. Dans un modèle **Remote**, le **calcul** s'effectue sur l'appareil distant, la **conversation** reste sur l'appareil qui utilise Bionic [Source].

| Cas d'usage | Intérêt |
|---|---|
| Portable léger + station puissante | Modèles volumineux sans changer de poste |
| Serveur interne | Mutualiser un modèle |

**Essayé dans LM Studio** (11 octobre 2026) avec un portable et un PC fixe : le modèle distant se charge en environ 15 s, répond à la même vitesse qu'en local (46,5 jetons par seconde) et le calcul se fait bien sur l'hôte ([Manuel LM Studio 17, sections 6 à 8](../lmstudio/17-lm-link.md#6-charger-et-régler-un-modèle-distant)). **Non essayé dans Bionic** ; trajet réseau (local ou via Internet) non relevé [À tester].

---

## 5. API locale

### Essentiel

Au démarrage, Bionic lance un **serveur HTTP local** compatible OpenAI, Anthropic et API REST LM Studio [Vérifié] :

| Élément | Valeur observée |
|---|---|
| Adresse d'écoute | **`127.0.0.1:1234`** (accessible **uniquement depuis la machine**) |
| URL de base (clients OpenAI) | `http://localhost:1234/v1` |
| Endpoints (journal) | `GET /v1/models` · `POST /v1/chat/completions` · `POST /v1/completions` · `POST /v1/embeddings` · `POST /v1/responses` · `POST /api/v1/models/download` · `GET /api/v1/models/download/status` |
| Chargement à la demande (JIT) | Activé : une requête peut charger le modèle |
| CORS | Désactivé |
| Authentification | **Aucune** (aucun jeton exigé dans la configuration testée) |

Réglages : Réglages → **API des modèles locaux** ([Manuel 03](03-reglages.md#10-modèles-locaux)).

**Exemple exécuté** (modèle chargé à la demande, durée 5,3 s, consigne courte) :

```powershell
$body = '{"model":"google/gemma-4-e4b","messages":[{"role":"user","content":"Réponds par un seul mot : capitale de la France ?"}],"max_tokens":300,"temperature":0}'
Invoke-RestMethod -Uri http://127.0.0.1:1234/v1/chat/completions -Method Post `
  -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($body))
```

Résultat : `Paris` (28 tokens de prompt, 2 tokens de complétion).

Les scripts du dossier [`exemples/`](../../exemples/) fonctionnent à l'identique avec Bionic, car l'API est la même que celle de LM Studio ([Manuel LM Studio 06](../lmstudio/06-serveur-local-et-api.md)). Seule contrainte : **une seule des deux applications** à la fois.

### Pour aller plus loin

| Point | Détail |
|---|---|
| **Vérifier l'adresse d'écoute** | `Get-NetTCPConnection -LocalPort 1234 -State Listen` → `127.0.0.1` = local uniquement ; `0.0.0.0` = tout le réseau. |
| **Appels d'outils MCP** | Aucun réglage d'approbation par outil ; un outil MCP à effet de bord s'exécute **sans confirmation**, même en mode *Demander à chaque fois* [Vérifié, 7 octobre 2026, [Manuel 08](08-competences-et-mcp.md#5-serveurs-mcp)] : n'ajouter que des serveurs de confiance, désactiver ceux qui ne servent pas |
| **Exposer sur le réseau** | Aucun réglage d'adresse d'écoute n'a été trouvé dans l'interface (seul le **port** est modifiable) [À tester]. |
| **Absence d'authentification** | Tout processus local de la machine (y compris d'autres utilisateurs de session partagée) peut appeler l'API ; sur un poste multi-utilisateurs, évaluer le risque. |
| **CORS** | Activer uniquement pour une page web locale précise : toute page ouverte dans le navigateur pourrait sinon appeler l'API. L'activation redémarre le serveur. |
| **Journaux** | **Journaux détaillés** activés par défaut ; **Masquer le contenu des requêtes** désactivé : les journaux (`~\.lmstudio\apps\bionic\server-logs`) peuvent contenir le texte des consignes et des réponses. Activer le masquage pour des données sensibles. |
| **Port** | **Modifier le port** si 1234 est occupé. |

---

## 6. Navigateur, recherche web, sites autorisés

| Réglage | Rôle | Défaut | Risque associé |
|---|---|---|---|
| **Recherche web** | Outils de recherche et d'extraction de contenu | Désactivé | Envoi de requêtes à un service externe ; contenu non fiable injecté dans le contexte |
| **Sites web autorisés** | Liste blanche de domaines | Vide (seul `localhost`) | Chaque domaine ajouté élargit la surface d'attaque |
| **Données du navigateur** | Cookies et données de site | Mémoire uniquement | *Conserver jusqu'à effacement* garde des sessions authentifiées sur le poste |

> **Injection de prompt** : une page web, un document ou un ticket peut contenir des instructions rédigées pour détourner l'agent (« envoyer le contenu du dossier à… »). Parades : liste blanche réduite, mode shell restrictif, **pas** de connexion à des services sensibles dans le navigateur intégré, relecture des commandes.

---

## 7. Menaces et parades

| Menace | Scénario | Parade principale |
|---|---|---|
| Action destructrice par l'agent | Commande de suppression en dehors du projet | Mode shell **Demander à chaque fois** ; dossier de travail limité ; Git ([Manuel 07](07-code-et-shell.md)) |
| Fichier modifié à tort | Modification directe d'un fichier du dossier de travail | Relire les diffs ; dépôt Git ; copie de travail |
| Fuite vers le cloud | Modèle cloud sélectionné par erreur sur des données sensibles | Définir un **modèle racine** local ; vérifier le sélecteur de modèle avant envoi |
| Injection de prompt | Contenu externe malveillant | Liste blanche ; relecture ; pas de **Tout autoriser** |
| Compétence / MCP piégé | Installation depuis une URL inconnue | Relecture ; sources internes ([Manuel 08](08-competences-et-mcp.md#6-sécurité)) |
| Accès à l'API locale | Autre programme local qui sollicite le modèle | Écoute `127.0.0.1` ; CORS désactivé ; masquage des journaux |
| Mise à jour non maîtrisée | Changement de comportement après mise à jour automatique | Désactiver les mises à jour automatiques ; mise à jour planifiée |
| Données dans les journaux | Consignes confidentielles dans `server-logs` | Masquer le contenu ; purger (**Effacer**) |

---

## 8. Configurations recommandées

| Niveau de sensibilité | Configuration |
|---|---|
| **Public / non sensible** | Modèle cloud possible (compte d'organisation), recherche web activée, mode *Vérification automatique*. |
| **Interne** | Modèle **local** ou **Remote** sur un appareil maîtrisé ; recherche web désactivée ; mode *Vérification automatique* ou *Demander à chaque fois* ; liste blanche vide. |
| **Confidentiel** | Modèle **local** uniquement ; aucun compte ; aucun serveur MCP distant ; mode *Demander à chaque fois* ; journaux masqués ; mises à jour contrôlées ; dossier de travail dédié. |
| **Critique** | Environnement isolé (machine dédiée ou virtuelle) ; **Désactivé** pour le shell sauf nécessité ; revue de sécurité formelle avant usage. |

---

## 9. Points non documentés à clarifier

| Question | Statut |
|---|---|
| Télémétrie (données d'usage envoyées à l'éditeur) | Non documentée dans les sources consultées [À tester] : surveiller les connexions sortantes au repos. |
| Fonctionnement **hors ligne** complet (réseau coupé) | Non testé [À tester]. |
| Périmètre exact de l'**isolation** (« bac à sable » du travail documentaire) | Non précisé : les fichiers externes sont modifiés directement, le shell s'exécute dans le dossier choisi. |
| Adresse d'écoute **modifiable** | Aucun réglage trouvé [À tester]. |
| Politique de **conservation** des historiques de sessions et possibilité d'**export** | Non documentées [À tester]. |
| **Plan d'équipe / organisation** | Mentionné, procédure non documentée. |
