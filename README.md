# LM Studio et LM Studio Bionic : manuels pratiques

Documentation en français, illustrée et **vérifiée par l'essai**, pour faire tourner des modèles de langage **en local** sur un poste Windows avec deux applications :

- **LM Studio** : télécharger un modèle (Gemma, Qwen, OlmOCR…), le charger sur le GPU ou le CPU, discuter avec lui, et l'exposer à vos programmes par une API locale compatible OpenAI.
- **LM Studio Bionic** : l'application *agent* de LM Studio. Le modèle ne fait plus seulement répondre : il lit et modifie des fichiers, lance des commandes, travaille sur un projet, sous votre contrôle.

Rien ne quitte la machine : pas de compte, pas de cloud, les modèles tournent sur votre matériel.

## Ce que le projet apporte

Chaque manuel part de l'interface réelle (captures annotées) et de **mesures faites sur deux postes** : un portable à GPU intégré (Intel Arc 140T) et un PC fixe à GPU dédié (NVIDIA RTX 4060 Ti 16 Go). Quand une affirmation n'a pas pu être vérifiée, elle est étiquetée : **[Vérifié]**, **[Source]** (documentation officielle), **[Estimation]**, **[À tester]**.

On y trouve notamment :

- les notions de base expliquées simplement (quantification, VRAM, contexte, vitesse) et comment choisir un modèle adapté à sa machine ;
- les 21 paramètres de chargement, leur effet mesuré sur la mémoire et la vitesse ;
- l'OCR de documents, le serveur local, la ligne de commande `lms`, le SDK, MCP et l'appel d'outils ;
- le branchement d'outils de code (Claude Code, Codex, Cline, Continue, Aider) sur un modèle local ;
- la sécurité : exposition du serveur, jetons d'API, autorisations de l'agent, et un **avertissement** sur Auto Review de Bionic, qui a laissé passer une commande destructive lors des essais.

## Par où commencer

| Vous voulez… | Lire |
|---|---|
| Découvrir LM Studio sans prérequis | [Notions fondamentales](docs/lmstudio/00-notions-fondamentales.md) puis [Prise en main](docs/lmstudio/01-prise-en-main.md) |
| Trouver une information précise | [Plan détaillé LM Studio](docs/lmstudio/plan-des-manuels.md) · [Plan détaillé Bionic](docs/bionic/plan-des-manuels.md) |
| Appeler un modèle depuis du code | [Serveur local et API](docs/lmstudio/06-serveur-local-et-api.md) et les [exemples](exemples/) |
| Utiliser l'agent Bionic | [Notions de l'agent](docs/bionic/00-notions-agent.md) puis [l'index Bionic](docs/bionic/README.md) |

L'index complet, avec les parcours de lecture conseillés et les limites connues, est dans [docs/README.md](docs/README.md).

## Contenu du dépôt

```text
LMStudio-Bionic/
├── docs/
│   ├── README.md          index général, parcours, limites connues
│   ├── lmstudio/          18 manuels LM Studio (00 à 17) et glossaire
│   ├── bionic/            15 manuels Bionic (00 à 14) et glossaire
│   └── img/               captures et figures
├── exemples/              scripts Python d'appel à l'API locale (bibliothèque standard seulement)
├── outils/                scripts qui ont produit les captures et les mesures (inutiles pour lire)
└── RECHERCHE-fonctionnalites-avancees.md   notes de recherche ayant servi aux manuels avancés
```

## Lancer les exemples

1. Dans LM Studio, démarrer le serveur local (onglet *Developer*, ou `lms server start`) et charger un modèle.
2. Lancer un script, sans rien installer :

```bash
cd exemples
python 02_chat_simple.py
```

Variables facultatives : `LMSTUDIO_URL` (défaut `http://127.0.0.1:1234`), `LMSTUDIO_MODEL` (défaut `google/gemma-4-e4b`), `LMSTUDIO_TOKEN` si l'authentification est activée. Les sorties obtenues lors des essais sont dans [sorties_verifiees.txt](exemples/sorties_verifiees.txt).

## Versions décrites

LM Studio 0.4.25 (0.4.26 pour le manuel 17), Bionic 1.1.7, Windows 11, captures et mesures d'octobre 2026. Ces applications évoluent vite : libellés et valeurs par défaut peuvent changer.
