# Manuel Bionic 08 — Compétences, palette `@` et serveurs MCP

> **Objet** : étendre les capacités de l'agent avec des **compétences** (instructions réutilisables) et des **serveurs MCP** (outils externes), et référencer des fichiers ou d'autres sessions avec la palette `@`.
> **Prérequis** : [Manuel Bionic 00](00-notions-agent.md#8-compétences-mcp-sous-agents), [03](03-reglages.md#8-intégrations--mcp-et-compétences).
> **Version décrite** : Bionic 1.1.7, Windows 11, interface en français.
> **Statut des informations** : [Vérifié] observé sur le poste de test ; [Source] documentation officielle ; [Estimation] ; [À tester].

---

## Sommaire

1. [Compétences : principe](#1-compétences--principe)
2. [Gérer les compétences](#2-gérer-les-compétences)
3. [La palette `@`](#3-la-palette-)
4. [Écrire une compétence](#4-écrire-une-compétence)
5. [Serveurs MCP](#5-serveurs-mcp)
6. [Sécurité](#6-sécurité)

---

## 1. Compétences : principe

### Essentiel

Une **compétence** (*skill*) est un dossier contenant un fichier **`SKILL.md`** : des instructions rédigées en langage naturel pour une tâche répétable (relire un contrat selon une check-list, appliquer un guide de style, produire un rapport au format attendu). L'agent la charge **quand elle est pertinente** ou **sur demande explicite** (palette `@`) [Source].

Intérêt : ne pas répéter les mêmes consignes à chaque session ; capitaliser un savoir-faire.

| Sans compétence | Avec compétence |
|---|---|
| Rappeler à chaque fois le format, le ton, la check-list | Écrire une fois, l'invoquer par `@` |
| Résultat variable selon la formulation | Résultat plus homogène |

> **Exemple** — compétence « Note de synthèse » : consignes de structure (contexte, constats, risques, recommandation), longueur maximale, ton impersonnel, nom de fichier. Invoquée par `@Note de synthèse` avec une pièce jointe, elle produit un document conforme sans rédiger de consigne détaillée.

### Pour aller plus loin

- Format standard **Agent Skills** (`SKILL.md` avec en-tête de métadonnées et fichiers de support facultatifs) [Source : agentskills.io]. Les compétences d'autres applications compatibles (Claude Code, Codex) peuvent être réutilisées.
- Les compétences sont des **instructions**, non du code signé : leur contenu influence directement ce que l'agent fait ([section 6](#6-sécurité)).

---

## 2. Gérer les compétences

Réglages → **Compétences**.

![Ajouter une compétence](../img/bionic/08-skills-mcp/01-ajouter-competence.png)
*Figure 1 — Menu « Ajouter une compétence » : Créer avec Bionic, Installer une compétence.*

### Compétences Bionic

Compétences créées ou installées **dans Bionic**, disponibles dans **tous les projets**.

| Action | Procédure |
|---|---|
| **Créer avec Bionic** | Une session démarre pour concevoir la compétence avec l'agent (questions de clarification, rédaction). Avec les modèles locaux testés, résultat **peu fiable** : [Manuel Bionic 13, section 5](13-competences-en-pratique.md#5-faire-créer-une-compétence-par-lagent). |
| **Installer une compétence…** | Depuis un fichier, un dossier ou une URL (dépôt GitHub, lien direct) [Source]. Installation par `@Install Skill` testée : approbation de l'utilisateur exigée ([Manuel Bionic 13, section 4](13-competences-en-pratique.md#4-essai-b--installer-une-compétence-globale)). |
| **Désactiver / retirer** | Menu **…** de la compétence : *Activer cette compétence*, *Afficher dans l'Explorateur de fichiers*, *Retirer* [Vérifié]. |

L'état initial est « Aucune compétence Bionic installée. » [Vérifié].

### Compétences d'autres applications

| Champ | Observé |
|---|---|
| **Claude Code** | **6 compétences** détectées dans `~\.claude\skills` ; interrupteur **désactivé** par défaut |

L'activation rend ces compétences **visibles** pour Bionic ; chacune peut ensuite être désactivée individuellement [Source]. Elles ne sont pas copiées : Bionic lit le dossier de l'autre application.

> **Point d'attention** — activer cette option expose à Bionic des instructions écrites pour un autre outil, qui peuvent supposer des fonctions absentes de Bionic. Les activer **une par une** après lecture.

---

## 3. La palette `@`

![Palette @](../img/bionic/08-skills-mcp/05-palette-arobase.png)
*Figure 2 — Saisie de `@` dans la zone de saisie : palette « Saisissez du texte pour trouver des fichiers, dossiers et compétences ».*

### Essentiel

Taper **`@`** dans la zone de saisie ouvre une palette de **références**. Elle propose, dans l'ordre observé :

| Entrée | Description affichée | Usage |
|---|---|---|
| **Create Skill** | « Create reusable guidance to perform certain tasks » | Faire créer une compétence à partir d'une tâche réussie. |
| **Install Skill** | « Install a skill from a file, a folder, or a URL » | Installer une compétence. |
| *Titres de sessions* | Sessions existantes, avec leur projet | Faire **relire à l'agent** une autre session (introspection). |

La saisie de texte après `@` **filtre** la liste : fichiers du projet, dossiers, compétences installées.

Les deux entrées « Create Skill » et « Install Skill » sont affichées en **anglais** dans la version testée.

### Pour aller plus loin

- La référence insère un **jeton** dans la consigne ; l'agent inspecte alors le fichier, la compétence ou la session désignée et décide comment l'appliquer [Source].
- Référencer une **autre session** donne à l'agent accès à son historique : utile pour reprendre un travail, à utiliser avec précaution si cette session contient des données sensibles.
- Des commandes `/install-skill` et `/create-skill` sont mentionnées dans le journal des modifications [Source] ; leur saisie directe n'a pas été testée [À tester]. Les entrées **Create Skill** et **Install Skill** de la palette `@` ont, elles, été exécutées ([Manuel Bionic 13](13-competences-en-pratique.md)).
- La palette filtre sur le **nom affiché** : `@resume` ne retrouve pas une compétence nommée « Résumé… » (accent) ; une compétence de **projet** (`.agents\skills`) apparaît **immédiatement**, sans installation.

---

## 4. Écrire une compétence

### Essentiel

Structure minimale :

```text
note-de-synthese/
└── SKILL.md
```

```markdown
---
name: note-de-synthese
description: Produit une note de synthèse d'une page à partir de documents fournis.
---

# Note de synthèse

## Quand l'utiliser
Lorsqu'une synthèse structurée de documents est demandée.

## Procédure
1. Lire tous les documents fournis.
2. Rédiger : Contexte, Constats, Risques, Recommandation.
3. Limiter à une page ; ton impersonnel et direct.
4. Enregistrer le résultat dans `note-de-synthese.md`.

## Contraintes
- Ne pas inventer de chiffres : signaler les données manquantes.
```

Les champs **`name`** et **`description`** de l'en-tête servent à l'agent pour **décider** de charger la compétence : une description précise (quand, pour quoi) améliore le déclenchement [Source].

### Pour aller plus loin

Bonnes pratiques [Source, complétées par l'usage courant] :

| Principe | Détail |
|---|---|
| Un objectif par compétence | Éviter les compétences « fourre-tout ». |
| Exemples et livrables | Inclure un exemple de sortie attendue. |
| Contraintes explicites | Interdits, limites, format de fichier. |
| Relecture | Relire toute compétence créée ou installée avant de s'y fier pour un travail important. |
| Création assistée | Après une tâche réussie : « Créer une compétence à partir de ce que l'on vient de faire. » |

> **Test de bout en bout** : réalisé et décrit dans le [Manuel Bionic 13](13-competences-en-pratique.md) : compétence de projet (déclenchement manuel et automatique, essai témoin), installation globale par `@Install Skill`, création assistée (peu fiable avec les modèles locaux testés).

---

## 5. Serveurs MCP

### Essentiel

**MCP** (*Model Context Protocol*) est un protocole ouvert qui permet de brancher des **outils externes** à un agent : lecture de tickets, de pages, de dépôts, de bases de données. Chaque serveur MCP expose des **outils** que l'agent peut appeler comme ses outils intégrés.

Réglages → **MCP** :

![Page MCP](../img/bionic/02-reglages/07-mcp.png)
*Figure 3 — Catalogue de serveurs MCP.*

| Zone | Contenu |
|---|---|
| **Serveurs MCP connectés** | Compteur (0 à l'état initial). |
| **MCP populaires** | **GitHub** (dépôts, tickets, pull requests), **Linear** (tickets, projets), **Notion** (pages, bases), **Sentry** (erreurs, traces), **Atlassian** (Jira, Confluence). Bouton **Configurer**. |
| **Configuration manuelle du serveur MCP** | **Ajouter un serveur MCP personnalisé**. |

Les serveurs du catalogue exigent en général une **authentification** auprès du service (compte, jeton) [Estimation : non testé].

### Serveur MCP personnalisé

![MCP personnalisé](../img/bionic/08-skills-mcp/02-serveur-mcp-personnalise.png)
*Figure 4 — « MCP personnalisé » : connexion « Sur cet ordinateur ».*

| Champ | Rôle |
|---|---|
| **État** (interrupteur) | Active ou désactive le serveur (« Prêt à se connecter »). |
| **Nom** | Nom affiché (ex. « Mon MCP »). |
| **Connexion** | **Sur cet ordinateur** (programme local lancé par Bionic) ou **Adresse web** (serveur distant). |
| **Commande** | Programme qui démarre le serveur (ex. `mcp-server`). |
| **Ajouter un MCP** | Valide (inactif tant que les champs obligatoires sont vides). |

**Paramètres avancés** (interrupteur *Afficher les options avancées*) :

![Options avancées](../img/bionic/08-skills-mcp/03-mcp-options-avancees.png)
*Figure 5 — Options avancées d'un serveur local.*

| Champ | Rôle |
|---|---|
| **Arguments** | Arguments de ligne de commande (un champ par argument : **Ajouter un argument**). |
| **Variables d'environnement** | Paires nom/valeur transmises au programme (clés d'API, etc.). |
| **Répertoire de travail** | Dossier d'exécution (chemin absolu). |
| **Délai d'expiration de la requête (secondes)** | Durée maximale de détection des outils et de chaque appel d'outil ; **60 s** par défaut. |

Connexion **Adresse web** :

![MCP adresse web](../img/bionic/08-skills-mcp/04-mcp-adresse-web.png)
*Figure 6 — Connexion à un serveur distant.*

| Champ | Rôle |
|---|---|
| **Adresse du serveur** | URL du serveur MCP. |
| **Authentification** | **Automatique** (connexion dans le navigateur au besoin) ou **Jeton d'accès**. |
| **En-têtes de requête** | En-têtes HTTP supplémentaires. |
| **Détails du client OAuth** | À laisser vides si le serveur gère l'enregistrement automatique du client. |
| **Portées OAuth** | **Automatique** ou **Personnalisé** (limiter les autorisations demandées ; certains outils peuvent ne pas fonctionner avec des portées réduites). |
| **Délai d'expiration** | Comme ci-dessus. |

### Pour aller plus loin

- Un **serveur local** exécute un programme **sur l'ordinateur, avec les droits de l'utilisateur**. Un serveur « Adresse web » envoie le contenu des appels d'outils à un **service externe**.
- La documentation mentionne des **serveurs MCP gérés par l'organisation** (déploiements d'entreprise) [Source : journal des modifications] ; leur configuration n'est pas décrite.
- Aucun serveur MCP n'a été **ajouté dans Bionic** pendant les tests : les écrans ont été décrits sans enregistrement. Le fonctionnement d'un serveur MCP (déclaration, outils, confirmation) a été testé dans LM Studio avec un serveur local de démonstration ([Manuel LM Studio 10](../lmstudio/10-mcp-et-appel-d-outils.md)).

---

## 6. Sécurité

| Risque | Exemple | Parade |
|---|---|---|
| **Compétence malveillante ou erronée** | Une compétence téléchargée demande d'« envoyer le contenu du dossier à une adresse » | Lire `SKILL.md` en entier avant installation ; préférer les compétences internes. |
| **MCP tiers** | Un serveur local lance un programme inconnu avec les droits de l'utilisateur | N'ajouter que des serveurs de source connue ; limiter les variables d'environnement transmises. |
| **Fuite de données** | Un MCP distant reçoit des contenus de fichiers | Vérifier ce que l'outil envoie ; privilégier des jetons à portée limitée (OAuth personnalisé). |
| **Injection d'instructions** | Une page web ou un ticket contient « ignore les consignes précédentes… » | Mode shell restrictif ; relecture des commandes et des diffs. |
| **Compétences d'une autre application** | Instructions supposant des outils absents | Activer au cas par cas. |

Règle générale : tout ce qui élargit les capacités de l'agent élargit aussi ce qu'une consigne erronée ou piégée peut faire. Le mode shell et la relecture des modifications ([Manuel 07](07-code-et-shell.md)) restent les **dernières protections**.
