# LM Link : manuel utilisateur

Version testée : LM Studio 0.4.26, Windows 11.
Configuration testée : un portable (client) et un PC fixe avec une NVIDIA GeForce RTX 4060 Ti 16 Go (hôte).

Chaque capture comporte des encadrés rouges. Quand plusieurs encadrés sont présents, ils sont numérotés. Le texte renvoie à ces numéros.

---

## En bref

Utiliser un PC distant avec LM Link, en six étapes :

1. Activer LM Link sur le portable et se connecter au compte (section 3).
2. Ouvrir la fiche du PC fixe dans l'onglet LM Link (section 4).
3. Charger un de ses modèles, en réglant si besoin le contexte et la mémoire (sections 8 et 9).
4. Choisir ce modèle dans le Chat (section 10).
5. Discuter. Le calcul se fait sur le PC fixe (section 11).
6. Éjecter le modèle pour libérer la carte graphique (section 12).

---

## Sommaire

1. [Comprendre LM Link](#1-comprendre-lm-link)
2. [Prérequis](#2-prérequis)
3. [Activer LM Link](#3-activer-lm-link)
4. [Lire l'écran LM Link](#4-lire-lécran-lm-link)
5. [Régler ce portable](#5-régler-ce-portable)
6. [Ajouter un appareil](#6-ajouter-un-appareil)
7. [Gérer le réseau](#7-gérer-le-réseau)
8. [Charger un modèle du PC fixe](#8-charger-un-modèle-du-pc-fixe)
9. [Régler le PC fixe à distance](#9-régler-le-pc-fixe-à-distance)
10. [Discuter avec le modèle distant](#10-discuter-avec-le-modèle-distant)
11. [Vérifier que le modèle tourne sur le PC fixe](#11-vérifier-que-le-modèle-tourne-sur-le-pc-fixe)
12. [Éjecter le modèle](#12-éjecter-le-modèle)
13. [Compte rendu du test](#13-compte-rendu-du-test)
14. [Points d'attention](#14-points-dattention)

---

## 1. Comprendre LM Link

LM Link relie plusieurs appareils entre eux. Un appareil peut utiliser les modèles installés sur un autre.

Exemple de ce manuel :

- Le PC fixe stocke les modèles et possède la carte graphique (16 Go de VRAM).
- Le portable affiche le chat et envoie les questions.
- Le calcul se fait sur le PC fixe. Le portable ne fait que l'affichage.

Vocabulaire :

| Terme | Sens |
|---|---|
| Appareil | Une machine connectée à LM Link (portable, PC fixe, téléphone, serveur). |
| Réseau personnel | L'ensemble des appareils liés au même compte. Nom affiché : « Personal Network ». |
| Appareil distant | Un autre appareil du réseau. Ici, le PC fixe. |
| Modèle distant | Un modèle stocké et exécuté sur un appareil distant. |

LM Studio annonce un chiffrement de bout en bout entre les appareils.

---

## 2. Prérequis

- LM Studio installé sur chaque appareil, en version récente.
- Un compte LM Studio. Le même compte doit être utilisé partout.
- LM Link activé sur le PC fixe. Il est déjà actif dans ce test.
- Le PC fixe allumé, avec LM Studio lancé.
- Une connexion Internet sur les deux machines.

---

## 3. Activer LM Link

À faire une seule fois par appareil.

### 3.1 Ouvrir la page LM Link

Cliquer sur **LM Link** dans la barre latérale gauche (repère 1). Cliquer ensuite sur **Login & Enable LM Link** (repère 2).

![Page d'accueil LM Link](images/annotees/01-accueil-lm-link.png)

### 3.2 Terminer dans le navigateur

Le bouton devient **Complete in the browser...**. La connexion se termine dans le navigateur web.

1. Passer dans le navigateur.
2. Se connecter au compte LM Studio.
3. Valider.
4. Revenir dans LM Studio.

![Connexion en cours dans le navigateur](images/annotees/02-connexion-navigateur.png)

Les identifiants se saisissent uniquement dans le navigateur, jamais dans LM Studio.

### 3.3 Résultat

Une fois connecté, la page affiche les appareils du réseau. Une infobulle explique que les modèles du PC fixe apparaissent dans la liste de droite.

1. Compteur d'appareils connectés, avec un point vert.
2. Le PC fixe, listé sous « Network Devices ».
3. Infobulle d'aide. La fermer avec la croix, ou cocher « Do not show this message again ».

![Premier affichage après connexion](images/annotees/03-appareil-connecte.png)

---

## 4. Lire l'écran LM Link

Cliquer sur le PC fixe dans la barre latérale pour ouvrir sa fiche.

![Fiche de l'appareil distant](images/annotees/04-fiche-appareil.png)

| Repère | Contenu |
|---|---|
| 1 | Nom de l'appareil : « PC-Fixe GPU 4060TI 16GO ». |
| 2 | Carte graphique : NVIDIA GeForce RTX 4060 Ti, 16,0 Go, CUDA. |
| 3 | VRAM : 16,0 Go. Mémoire vive : 61,6 Go. |
| 4 | Propriétaire, statut (Connected), dernière activité, identifiant de l'appareil, lien de réseau. |
| 5 | Liste des modèles installés sur le PC fixe. |

L'identifiant de l'appareil est flouté sur les captures.

Modèles trouvés sur le PC fixe :

| Modèle | Taille indiquée |
|---|---|
| Gemma 4 26B A4B | 26B-A4B |
| Qwen3.8 27B | 27B |
| Gemma 4 E4B | 7,5B |
| Olmocr 2 7B | 7B |
| Nomic Embed Text v1.5 | gguf (modèle d'embedding) |

Le champ **Filter models...** filtre la liste par nom.

### Appareil préféré

En bas de la fiche, l'option **Set as preferred device** (repère 2) demande à LM Studio de charger les modèles sur cet appareil quand c'est possible.

![Option appareil préféré](images/annotees/05-appareil-prefere.png)

Cette option est désactivée par défaut. Elle n'a pas été modifiée pendant le test.

---

## 5. Régler ce portable

Dans la barre latérale, section **This device**, cliquer sur l'engrenage à côté du nom du portable.

![Réglages de cet appareil](images/annotees/06-cet-appareil.png)

| Repère | Rôle |
|---|---|
| 1 | Nom de l'appareil, visible par les autres appareils. Le crayon permet de le modifier. |
| 2 | Identifiant aléatoire de l'appareil dans le réseau. Il est flouté sur la capture. |
| 3 | Interrupteur **Allow loading models on this machine**. Désactivé, les autres appareils ne voient plus les modèles de cette machine et ne peuvent plus les charger. |

Pour partager les modèles d'une machine, laisser l'interrupteur activé. Pour la protéger, le désactiver.

Ce réglage se fait sur la machine concernée. Pour empêcher le portable de servir de modèle aux autres, il se règle donc sur le portable. Pour le PC fixe, il se règle sur le PC fixe.

---

## 6. Ajouter un appareil

Cliquer sur le bouton bleu **+** à côté de « Network Devices ». L'assistant propose trois types d'appareil.

![Choix du type d'appareil](images/annotees/07-ajouter-appareil.png)

| Repère | Type | Usage |
|---|---|---|
| 1 | iPhone ou iPad | Utiliser les gros modèles depuis un téléphone. Option marquée « NEW ». |
| 2 | Computer | Mac, Windows ou Linux avec LM Studio. |
| 3 | Headless | Serveur ou machine sans écran, pilotée par le terminal. Option « Advanced ». |

Cliquer sur une carte ouvre directement les instructions. Le bouton **Back** revient au choix. Le bouton **Done** ferme l'assistant.

### 6.1 Ajouter un ordinateur

![Ajouter un ordinateur](images/annotees/08-ajout-ordinateur.png)

1. Télécharger et installer LM Studio sur l'autre appareil. Adresse : `https://lmstudio.ai/download` (repère 1).
2. Cliquer sur l'icône LM Link dans la barre latérale et suivre les étapes d'activation (repère 2).
3. Les appareils se connectent ensuite automatiquement (repère 3).

### 6.2 Ajouter un serveur sans écran (Headless)

![Ajouter un serveur headless](images/annotees/09-ajout-headless.png)

Trois commandes à lancer dans le terminal du serveur, dans cet ordre :

| Repère | Commande | Rôle |
|---|---|---|
| 1 | `curl -fsSL https://lmstudio.ai/install.sh \| bash` | Installe `llmster`, la version sans interface. |
| 2 | `lms login` | Connecte le serveur au compte. |
| 3 | `lms link enable` | Active LM Link. |

L'icône de copie à droite de chaque commande la place dans le presse-papiers.

Ces commandes sont celles de l'assistant (installation pour Linux et macOS). Elles n'ont pas été exécutées pendant ce test.

### 6.3 Ajouter un iPhone ou un iPad

![Ajouter un iPhone ou un iPad](images/annotees/10-ajout-iphone.png)

1. Installer l'application **Locally** sur l'iPhone ou l'iPad (repère 1). Le QR code mène à l'App Store (repère 2).
2. Se connecter avec le même compte LM Studio.
3. Vérifier que la connexion LM Link est activée.

Locally est l'application iPhone de LM Studio. Elle n'a pas été installée pendant ce test.

---

## 7. Gérer le réseau

En bas de la barre latérale, le bloc **Personal Network** affiche le nom du réseau et son état (Online).

Le bouton **...** (repère 1) ouvre un menu avec une seule entrée : **Manage on web** (repère 2). Elle ouvre la gestion du réseau sur le site de LM Studio.

![Menu du réseau](images/annotees/11-menu-reseau.png)

Cette entrée n'a pas été ouverte pendant le test, car elle sort de l'application.

À côté de « Network Devices », le bouton circulaire fléché actualise la liste des appareils.

---

## 8. Charger un modèle du PC fixe

Test réalisé avec **Gemma 4 E4B**. Ce modèle est assez léger pour la 4060 Ti.

### 8.1 Lancer le chargement

1. Ouvrir la fiche du PC fixe.
2. Dans « Models on Remote Device », cliquer sur le bouton lecture à droite du modèle.

La fenêtre de chargement s'ouvre. Ses réglages s'appliquent sur le PC fixe, pas sur le portable.

![Fenêtre de chargement d'un modèle distant](images/annotees/12-charger-modele-distant.png)

| Repère | Élément | Valeur du test |
|---|---|---|
| 1 | Estimation de mémoire (bêta). Valeur calculée pour le PC fixe. | 9,26 Go de GPU, 9,26 Go au total |
| 2 | Identifiant d'API. Nom utilisé par les programmes qui appellent le modèle. | `google/gemma-4-e4b` |
| 3 | Longueur de contexte. Quantité de texte que le modèle garde en mémoire. | 8192 (maximum du modèle : 131072) |
| 4 | Déchargement GPU. Nombre de couches placées sur la carte graphique. | 42 (maximum) |
| 5 | Interrupteur des réglages avancés. | Désactivé |
| 6 | Bouton de lancement. Raccourci : Ctrl + Entrée. | |

Règle pratique : l'estimation du repère 1 doit rester sous la VRAM de l'appareil (16 Go ici). Un contexte plus long augmente la mémoire utilisée.

Les cases suivantes sont aussi présentes :

- **Auto Unload If Idle (TTL)** : décharge le modèle après un temps d'inactivité.
- **Remember settings for ...** : mémorise ces réglages pour ce modèle.

### 8.2 Réglages avancés

Activer **Show advanced settings** (repère 1) pour voir d'autres paramètres, comme la taille du pool de threads CPU (4 ici) et la taille de lot d'évaluation (2048).

![Réglages avancés](images/annotees/13-reglages-avances.png)

Pour un premier usage, laisser ces valeurs par défaut.

### 8.3 Valider

Cliquer sur **Load Model** (repère 2 de la capture précédente).

Une pastille en haut de l'écran indique le chargement, avec une barre de progression (repère 1). Le modèle affiche le badge orange **Loading** (repère 2).

![Chargement en cours](images/annotees/14-chargement-en-cours.png)

Environ 15 secondes plus tard, un message **Model loaded successfully** apparaît (repère 1). Le badge devient vert, **Loaded** (repère 2).

![Modèle chargé](images/annotees/15-modele-charge.png)

Le bouton **...** à droite du badge ouvre le menu du modèle. Il contient l'entrée **Eject**.

![Menu du modèle chargé](images/annotees/16-menu-ejecter.png)

---

## 9. Régler le PC fixe à distance

Trois niveaux de réglage existent depuis le portable. Chacun agit sur le modèle qui tourne sur le PC fixe.

| Niveau | Où | Portée |
|---|---|---|
| Au chargement | Fenêtre « Load Model » | Cette session de chargement. |
| Par défaut du modèle | Onglet Library, panneau du modèle | Chaque futur chargement ou chat avec ce modèle. |
| Par conversation | Onglet Chat, panneau de droite | La conversation en cours. |

### 9.1 Réglages au chargement

La fenêtre « Load Model » s'ouvre de deux façons :

- Depuis la fiche du PC fixe, bouton lecture du modèle (section 8).
- Depuis la bibliothèque, bouton **Load Model** du panneau du modèle (section 9.2).

Test réalisé : charger Gemma 4 E4B avec un contexte de 16384 au lieu de 8192, et avec le déchargement automatique activé.

1. Saisir `16384` dans le champ **Context Length** (repère 3).
2. Cocher **Auto Unload If Idle (TTL)** (repère 2). Un champ de durée apparaît, réglé sur 60 minutes.
3. Constater la nouvelle estimation (repère 1) : 9,66 Go au lieu de 9,26 Go.
4. Cliquer sur **Load Model**.

![Chargement avec contexte et TTL modifiés](images/annotees/30-chargement-contexte-ttl.png)

Vérification dans l'onglet **Model Server**. La pastille **Idle TTL 60 min** apparaît sur la ligne du modèle.

![Pastille de déchargement automatique](images/annotees/31-ttl-applique.png)

Dans le panneau de droite, onglet **Load**, le contexte affiche 16384 (repère 1). La pastille TTL est repérée en 2.

![Contexte vérifié](images/annotees/32-contexte-verifie.png)

Résultat : les réglages choisis sur le portable sont appliqués au modèle du PC fixe.

Ces réglages ne sont pas mémorisés, car la case « Remember settings for ... » était décochée. Au chargement suivant, les valeurs par défaut reviennent.

### 9.2 Réglages par défaut du modèle (bibliothèque)

L'onglet **Library** liste tous les modèles, locaux et distants.

![Bibliothèque](images/annotees/25-bibliotheque.png)

| Repère | Contenu |
|---|---|
| 1 | Modèles distants : la colonne « Device » affiche une icône de lien. |
| 2 | Modèles du portable : la colonne « Device » affiche « Local ». |

Cliquer sur l'engrenage d'une ligne ouvre le panneau du modèle, à droite.

![Panneau d'un modèle distant](images/annotees/26-bibliotheque-modele-distant.png)

| Repère | Contenu |
|---|---|
| 1 | « Hosted on » : l'appareil qui héberge le modèle (le PC fixe). |
| 2 | **Use in New Chat** ouvre un chat avec ce modèle. **Load Model** ouvre la fenêtre de chargement. |
| 3 | Trois onglets : Info, Load, Inference. |
| 4 | Étiquette « Customized » : le modèle a des réglages personnalisés. |

**Onglet Load.** Réglages de chargement par défaut : longueur de contexte et déchargement GPU. La section **Advanced** donne accès aux réglages avancés.

![Onglet Load](images/annotees/27-reglages-chargement-defaut.png)

**Onglet Inference.** Réglages de génération par défaut. Huit sections :

![Onglet Inference](images/annotees/28-reglages-inference.png)

| Section | Rôle |
|---|---|
| System Prompt | Consigne donnée au modèle avant chaque conversation. |
| Custom Fields | Champs personnalisés propres au modèle. |
| Reasoning | Réglages de la phase de réflexion. |
| Settings | Réglages généraux de génération. |
| Reasoning Parsing | Séparation entre la réflexion et la réponse. |
| Sampling | Choix des mots : voir ci-dessous. |
| Structured Output | Forcer un format de réponse (par exemple JSON). |
| Prompt Template | Modèle de mise en forme du prompt. |

La section **Sampling** contrôle le côté aléatoire des réponses :

![Section Sampling](images/annotees/29-echantillonnage.png)

| Paramètre | Valeur relevée |
|---|---|
| Top K Sampling | 64 |
| Repeat Penalty | 1,1 (activé) |
| Presence Penalty | Désactivé |
| Top P Sampling | 0,95 (activé) |
| Min P Sampling | 0,05 (activé) |

Ces valeurs par défaut n'ont pas été modifiées pendant le test.

### 9.3 Réglages par conversation (Chat)

Dans l'onglet **Chat**, le panneau de droite regroupe les paramètres de la conversation en cours. Il s'ouvre avec l'icône en haut à droite.

![Paramètres du chat](images/annotees/33-parametres-du-chat.png)

| Repère | Contenu |
|---|---|
| 1 | Bascule entre les outils (marteau) et les paramètres du modèle (curseurs). |
| 2 | Preset : enregistrer un ensemble de réglages sous un nom. |
| 3 | Sections : System Prompt, Custom Fields, Reasoning, Settings, Sampling, Structured Output. |

Test réalisé : donner une consigne système au modèle du PC fixe.

1. Déplier **System Prompt**.
2. Saisir la consigne : `Tu es un pirate. Réponds toujours en une seule phrase courte, avec un vocabulaire de pirate.`
3. Écrire une question dans la zone de saisie : `Quelle est la capitale de la France ?`
4. Envoyer avec Entrée.

![Consigne système et question saisies](images/annotees/34-consigne-systeme-saisie.png)

Le panneau affiche « Unsaved Preset » : la consigne n'est pas enregistrée. Le bouton **Discard unsaved** l'annule.

Réponse du modèle : « Parbleu, c'est Paris qui est la capitale de cette terre ! »

![Effet de la consigne système](images/annotees/35-consigne-systeme-effet.png)

| Repère | Contenu |
|---|---|
| 1 | Consigne système active. |
| 2 | Réponse en vocabulaire de pirate : la consigne est appliquée. |
| 3 | Vitesse : 46,37 tokens par seconde. |

Résultat : les réglages du chat agissent sur le modèle du PC fixe. La vitesse reste identique à celle du premier test.

### 9.4 Ce qui ne se règle pas depuis le portable

- **Téléchargement de modèles.** L'onglet **Model Search** n'offre pas de choix d'appareil. Le bouton **Download** indique la taille du fichier pour le portable. Rien n'a été téléchargé pendant le test. Pour ajouter un modèle au PC fixe, passer par LM Studio sur le PC fixe.

![Recherche de modèles](images/annotees/36-recherche-modeles.png)

- **Partage des modèles.** L'interrupteur « Allow loading models on this machine » se règle sur la machine concernée (section 5).

---

## 10. Discuter avec le modèle distant

### 10.1 Ouvrir le sélecteur de modèle

Aller dans l'onglet **Chat**. Appuyer sur **Ctrl + L**, ou cliquer sur la barre « Select a model to load ».

![Sélecteur de modèle](images/annotees/17-selecteur-chat.png)

| Repère | Contenu |
|---|---|
| 1 | Section « Currently Loaded » : le modèle chargé sur le PC fixe, avec l'icône de lien. |
| 2 | Les modèles du PC fixe, identifiables à l'icône de lien devant leur nom. Les modèles du portable n'ont pas cette icône. |
| 3 | « Memory Consumption : 0 GB / 15 GB ». C'est la mémoire utilisée sur le portable : elle reste à zéro. |

Une icône de lien signifie : modèle distant.

### 10.2 Choisir le modèle

Cliquer sur la ligne du modèle chargé (repère 1).

La barre du haut affiche alors le nom du modèle avec l'icône de lien (repère 1). L'icône d'éjection est à côté (repère 2).

![Modèle distant sélectionné](images/annotees/18-modele-selectionne.png)

### 10.3 Créer un chat

Cliquer sur **New chat**. La zone de saisie apparaît en bas de l'écran.

![Nouveau chat](images/annotees/19-nouveau-chat.png)

### 10.4 Poser une question

Cliquer dans la zone de saisie (repère 1) et écrire le message. Envoyer avec **Entrée** ou avec la flèche (repère 2).

Message du test : `Bonjour ! Présente-toi en deux phrases courtes.`

![Message saisi](images/annotees/20-message-saisi.png)

### 10.5 Lire la réponse

![Réponse du modèle du PC fixe](images/annotees/21-reponse-du-pc-fixe.png)

| Repère | Contenu |
|---|---|
| 1 | Barre du modèle, avec l'icône de lien. |
| 2 | Réponse du modèle. Le bloc « Thought for 5.45 seconds » est la phase de réflexion, repliée. |
| 3 | Statistiques de génération. |

Statistiques du test :

| Mesure | Valeur |
|---|---|
| Vitesse | 46,53 tokens par seconde |
| Longueur | 294 tokens (réflexion comprise) |
| Délai avant le premier mot | 0,46 s |
| Arrêt | « EOS Token Found » : le modèle a terminé sa réponse normalement |

---

## 11. Vérifier que le modèle tourne sur le PC fixe

Le nom du modèle est le même sur le portable et sur le PC fixe. La vérification passe par l'onglet **Model Server**.

![Preuves que le modèle est distant](images/annotees/22-preuve-modele-distant.png)

| Repère | Ce qu'il montre |
|---|---|
| 1 | Badge « PC-Fixe GPU 4060TI 16GO » sur la ligne du modèle chargé. |
| 2 | « Hosted on PC-Fixe GPU 4060TI 16GO » : la machine qui héberge le modèle. |
| 3 | Fichier utilisé : `gemma-4-E4B-it-Q8_0.gguf`. |
| 4 | Taille : 9,02 Go. |

Indices supplémentaires :

- Le portable possède aussi un Gemma 4 E4B, mais en quantification Q4_K_M (5,89 Go). Le fichier du test est en Q8_0 : c'est celui du PC fixe.
- La mémoire consommée sur le portable est restée à 0 Go (voir la capture de la section 10.1).
- À l'éjection depuis le Chat, LM Studio affiche « You are about to unload a model loaded on PC-Fixe GPU 4060TI 16GO » (section 12).

Contrôle côté PC fixe : ouvrir le Gestionnaire des tâches, onglet Performance, GPU. Environ 9 Go de VRAM doivent être occupés par LM Studio pendant le chargement du modèle.

Sur cette page, le serveur local du portable est arrêté (« Status: Stopped »). Le chat fonctionne sans lui.

---

## 12. Éjecter le modèle

Un modèle chargé occupe de la VRAM sur le PC fixe, même sans discussion en cours. Il faut l'éjecter après usage. Sinon, le déchargement automatique (TTL) s'en charge, s'il a été activé.

Trois endroits permettent de l'éjecter :

- Le bouton **Eject** dans l'onglet Model Server. L'éjection est immédiate.
- L'entrée **Eject** du menu **...** dans la fiche du PC fixe.
- L'icône d'éjection à droite de la barre de modèle du Chat. Une confirmation s'affiche d'abord.

### 12.1 Depuis le Chat

![Confirmation d'éjection](images/annotees/37-confirmation-ejection.png)

1. Message de confirmation : « Ejecting remote model. You are about to unload a model loaded on PC-Fixe GPU 4060TI 16GO. Continue? »
2. Cliquer sur **Eject** pour confirmer, ou sur **Cancel** pour annuler.

Après confirmation, la barre du Chat revient à « Select a model to load ». Un bouton **Reload last used model** (Ctrl + R) permet de relancer le modèle.

### 12.2 Depuis Model Server

![Après éjection](images/annotees/23-modele-ejecte.png)

La liste « Loaded Models » est vide (repère 1) et le panneau de droite affiche « No model selected » (repère 2).

### 12.3 Retour sur la page LM Link

Le PC fixe reste connecté et ses modèles restent disponibles, sans badge « Loaded ».

![État final](images/annotees/24-etat-final.png)

---

## 13. Compte rendu du test

| Étape | Résultat |
|---|---|
| Affichage de la page LM Link avant connexion | Réussi |
| Connexion au compte via le navigateur | Réussi (saisie faite par l'utilisateur) |
| Détection du PC fixe | Réussi : statut Connected, 4060 Ti, 16 Go, 61,6 Go de RAM |
| Liste des modèles distants | Réussi : 5 modèles |
| Réglages de ce portable | Consultés, non modifiés |
| Assistant d'ajout : Computer, Headless, iPhone/iPad | Consultés, non exécutés |
| Chargement d'un modèle distant (Gemma 4 E4B) | Réussi, environ 15 s |
| Chargement avec réglages modifiés (contexte 16384, TTL 60 min) | Réussi, réglages vérifiés sur le PC fixe |
| Bibliothèque : modèles distants, réglages Load et Inference | Consultés, non modifiés |
| Sélection du modèle distant dans le Chat | Réussi |
| Envoi d'un message et réponse | Réussi, 46,53 tokens par seconde |
| Consigne système sur le modèle distant | Réussi, consigne respectée, 46,37 tokens par seconde |
| Confirmation de l'exécution sur le PC fixe | Réussi (section 11) |
| Éjection depuis Model Server et depuis le Chat | Réussi |

Non testé :

- Les gros modèles Qwen3.8 27B (16,52 Go) et Gemma 4 26B A4B (16,76 Go). Leur fichier dépasse la VRAM de 16 Go. Le comportement dans ce cas n'a pas été vérifié.
- Olmocr 2 7B et le modèle d'embedding Nomic.
- L'interrupteur « Set as preferred device ».
- Le menu « Manage on web ».
- L'enregistrement de réglages par défaut (case « Remember settings for ... », presets).
- L'utilisation d'un modèle distant via le serveur local (API) du portable.
- Le téléchargement d'un modèle (aucun choix d'appareil observé).
- L'ajout réel d'un deuxième appareil, d'un serveur sans écran ou d'un iPhone.

---

## 14. Points d'attention

- **Même nom, deux machines.** Un modèle local et un modèle distant peuvent porter le même nom. Repérer l'icône de lien.
- **VRAM du PC fixe.** Un modèle chargé reste en VRAM tant qu'il n'est pas éjecté. Cela bloque aussi les jeux et autres usages de la carte graphique. Le contexte long augmente la mémoire utilisée.
- **PC fixe éteint ou LM Studio fermé.** Les modèles distants disparaissent de la liste.
- **Partage.** L'interrupteur « Allow loading models on this machine » contrôle ce que les autres appareils voient.
- **Compte.** Toute personne connectée au même compte voit les mêmes appareils. Le nom du compte est visible sur les captures de ce manuel.
- **Identifiants d'appareil.** Ils sont floutés sur les captures annotées. Les images originales (`images/originaux`) contiennent encore ces identifiants. Ne pas les publier telles quelles.
