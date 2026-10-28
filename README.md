# LM Studio et LM Studio Bionic : manuels pratiques

Faire tourner des modèles de langage en local, sans compte ni cloud :

- **LM Studio** : télécharger un modèle, le charger, discuter avec lui, l'appeler depuis du code par une API compatible OpenAI.
- **LM Studio Bionic** : l'application agent. Le modèle lit et modifie des fichiers, lance des commandes, travaille sur un projet.

Chaque manuel a été vérifié par l'essai : captures de l'interface, commandes exécutées, mesures réelles.

## Ce qu'on y apprend

- Choisir un modèle selon sa machine (quantification, mémoire, contexte, vitesse).
- Régler le chargement et l'inférence, faire de l'OCR sur des documents.
- Utiliser le serveur local, la commande `lms`, le SDK, MCP et l'appel d'outils.
- Brancher des outils de code (Claude Code, Codex, Cline, Continue, Aider) sur un modèle local.
- Sécuriser le serveur et encadrer l'agent. Attention : lors des essais, Auto Review de Bionic a laissé passer une commande destructive ([manuel Bionic 12](docs/bionic/12-auto-review.md)).

## Par où commencer

| Objectif | Lire |
|---|---|
| Découvrir LM Studio | [Notions fondamentales](docs/lmstudio/00-notions-fondamentales.md), puis [Prise en main](docs/lmstudio/01-prise-en-main.md) |
| Appeler un modèle depuis du code | [Serveur local et API](docs/lmstudio/06-serveur-local-et-api.md) et les [exemples](exemples/) |
| Utiliser l'agent Bionic | [Notions de l'agent](docs/bionic/00-notions-agent.md), puis l'[index Bionic](docs/bionic/README.md) |
| Trouver une information précise | Plans détaillés [LM Studio](docs/lmstudio/plan-des-manuels.md) et [Bionic](docs/bionic/plan-des-manuels.md) |

Index complet et parcours de lecture : [docs/README.md](docs/README.md).

## Contenu

```text
docs/lmstudio/   manuels LM Studio (00 à 17) et glossaire
docs/bionic/     manuels Bionic (00 à 14) et glossaire
exemples/        scripts Python d'appel à l'API locale, sans dépendance
outils/          scripts ayant produit les captures et les mesures
```

## Lancer un exemple

Démarrer le serveur local dans LM Studio (ou `lms server start`), charger un modèle, puis :

```bash
cd exemples
python 02_chat_simple.py
```

L'adresse, le modèle et le jeton se changent avec `LMSTUDIO_URL`, `LMSTUDIO_MODEL` et `LMSTUDIO_TOKEN`.
