# Documentation LM Studio Bionic

Manuels et tutoriels illustrés pour installer, configurer et utiliser **LM Studio Bionic** (application agent : code, documents, recherche, voix), avec des exemples exécutés sur des modèles locaux (*Gemma 4 E4B*, *Gemma 4 12B QAT*).

| | |
|---|---|
| **Version décrite** | Bionic 1.1.7 (build 7), canal Stable, Windows 11 |
| **Date des captures et mesures** | 6 octobre 2026 |
| **Poste de test** | Intel Core Ultra 7 255H, 31 Go de RAM, GPU intégré Intel Arc 140T (moteur Vulkan) |
| **Langue de l'interface** | Français (quelques libellés restent en anglais, cités tels quels) |
| **Comptes** | Aucun compte connecté pendant les tests |

## Manuels

| N° | Manuel | Contenu |
|---|---|---|
| 00 | [Notions fondamentales de l'agent](00-notions-agent.md) | Chat et agent, boucle d'actions, harnais, lieux d'exécution, autorisations, contexte, compétences et MCP |
| 01 | [Présentation, installation, premier lancement](01-presentation-installation.md) | Différences avec LM Studio, conflit entre les deux applications, emplacements de données, mises à jour |
| 02 | [L'interface](02-interface.md) | Barre latérale, onglets, fil de session, zone de saisie, panneau de droite, navigateur intégré |
| 03 | [Les réglages](03-reglages.md) | Chaque page de Paramètres, champs, valeurs par défaut, profils de réglage |
| 04 | [Modèles](04-modeles.md) | Choisir, télécharger et régler un modèle pour l'agent ; effort de raisonnement ; mesures |
| 05 | [Projets et sessions](05-projets-et-sessions.md) | Créer un projet, dossier de travail, sessions, parallélisme, fork |
| 06 | [Documents et fichiers](06-documents.md) | Travail documentaire, fichiers du projet, fichiers externes, images |
| 07 | [Code, shell et autorisations](07-code-et-shell.md) | Scénario de correction de code exécuté, modes shell, relecture, sécurité |
| 08 | [Compétences, palette `@`, MCP](08-competences-et-mcp.md) | Écrire et gérer des compétences, serveurs MCP |
| 09 | [Saisie vocale](09-voix.md) | Dictée locale (Voxtral), réglage, limites |
| 10 | [Sécurité, compte, cloud, API locale](10-securite-compte-api.md) | Flux de données, crédits, LM Link, API locale, menaces, configurations types |
| 11 | [Recettes et dépannage](11-recettes-et-depannage.md) | Fiches par cas d'usage, diagnostic par symptôme |
| 12 | [Auto Review](12-auto-review.md) | Shell Judge, Shell Reviewer, niveaux de risque, instructions personnalisées, limites |
| 13 | [Compétences en pratique](13-competences-en-pratique.md) | Compétence de bout en bout : création, déclenchement avec `@`, résultat mesuré |
| 14 | [Commandes `/`, compaction, navigateur](14-commandes-compaction-navigateur.md) | Menu `/`, `/compact` mesuré, navigateur intégré et essai avec l'agent, fonctions non reproduites |
| — | [Glossaire](annexe-glossaire.md) | Termes techniques |

**Parcours conseillés**

- *Découverte* : **00** → 01 → 02 → 05 → 06.
- *Développeur* : 00 → 05 → 07 → 12 → 04 → 08 → 13.
- *Sécurité et conformité* : 00 (section 6) → 10 → 12 → 03 (section 11) → 07 (section 8).
- *Exploitation d'un poste* : 01 → 03 → 04 → 11.

## Conventions

- **Exemple** : les valeurs « du poste de test » illustrent un principe général ; elles dépendent du modèle et de la machine.
- **Étiquettes de fiabilité** : **[Vérifié]** observé ou mesuré sur le poste de test ; **[Source]** documentation officielle ; **[Estimation]** déduction ; **[À tester]** non documenté et non testé.
- Les chemins contenant `<utilisateur>` remplacent le nom du profil Windows du poste de test ; **certaines captures montrent ce chemin en clair**.

## Limites connues

- **Aucun compte connecté** : modèles cloud, crédits, recherche web, LM Link et gestion de plan sont décrits d'après l'interface et la documentation, non exécutés.
- **Dictée vocale** non exécutée (pas de microphone ni de téléchargement du modèle vocal).
- **Compétences** : essai de bout en bout réalisé ([manuel 13](13-competences-en-pratique.md)) ; **MCP** : serveurs décrits dans le manuel 08, essai réalisé côté LM Studio ([manuel LM Studio 10](../lmstudio/10-mcp-et-appel-d-outils.md)).
- **Auto Review** : niveau `too_destructive` non reproduit (aucun test sans danger).
- Les performances mesurées dépendent du GPU intégré du poste de test.
- Bionic évolue vite : les libellés, valeurs par défaut et fonctions peuvent changer entre versions.

## Dossiers associés

```text
EDF/
├── docs/
│   ├── README.md                (index général)
│   ├── lmstudio/                (manuels LM Studio)
│   ├── bionic/                  (cette page et les manuels Bionic)
│   └── img/bionic/              (captures, un dossier par manuel)
├── exemples/                    (scripts d'API ; fonctionnent aussi avec Bionic)
└── outils/                      (production des captures et des figures)
```
