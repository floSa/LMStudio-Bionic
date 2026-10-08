# Manuel Bionic 06 — Documents, fichiers et images

> **Objet** : confier à Bionic un travail sur des documents : rédiger, résumer, extraire des données d'une image ou d'un PDF, produire des fichiers ; comprendre où vont les fichiers et comment les contrôler.
> **Prérequis** : [Manuel Bionic 05](05-projets-et-sessions.md).
> **Version décrite** : Bionic 1.1.7, Windows 11, interface en français.
> **Statut des informations** : [Vérifié] observé et mesuré sur le poste de test ; [Source] documentation officielle ; [Estimation] ; [À tester].

---

## Sommaire

1. [Principe](#1-principe)
2. [Ajouter des fichiers](#2-ajouter-des-fichiers)
3. [Fichiers du projet](#3-fichiers-du-projet)
4. [Fichiers externes](#4-fichiers-externes)
5. [Exemple 1 : rédiger un mémo](#5-exemple-1--rédiger-un-mémo)
6. [Exemple 2 : extraire les données d'une facture](#6-exemple-2--extraire-les-données-dune-facture)
7. [Formats pris en charge](#7-formats-pris-en-charge)
8. [Rédiger une bonne consigne documentaire](#8-rédiger-une-bonne-consigne-documentaire)
9. [Fiabilité et contrôle](#9-fiabilité-et-contrôle)

---

## 1. Principe

### Essentiel

Pour le travail documentaire, Bionic fournit un **espace de travail géré** où l'agent crée et modifie des fichiers : documents, tableurs, présentations, PDF, images, fichiers texte [Source]. Le shell n'est généralement pas nécessaire : le mode **Désactivé** convient.

Flux type :

1. Créer un projet (sans répertoire de travail).
2. Joindre des sources (glisser-déposer, bouton **+** ou **Ajouter un fichier**).
3. Formuler un **livrable précis** (contenu, format, nom de fichier).
4. Relire la réponse et le fichier produit (panneau de droite).
5. Itérer dans la même session, ou ouvrir une nouvelle session pour une autre tâche.

### Pour aller plus loin

La documentation évoque un **bac à sable géré** (*managed sandbox*) pour le travail documentaire, des **points de sauvegarde automatiques** et des aperçus selon le format [Source]. Le périmètre exact de l'isolation n'est pas précisé : les **fichiers externes** sont modifiés directement, et les commandes shell, si elles sont autorisées, s'exécutent dans le dossier choisi ([Manuel 10](10-securite-compte-api.md#9-points-non-documentés-à-clarifier)).

---

## 2. Ajouter des fichiers

| Méthode | Résultat | Statut |
|---|---|---|
| **Glisser-déposer** sur la zone de saisie | Le fichier apparaît sous forme de pastille dans la zone de saisie (avec une croix pour le retirer) et est envoyé avec la consigne | [Vérifié] |
| Bouton **+** de la zone de saisie (« Ajouter des fichiers, des dossiers ou des compétences ») | Sélecteur de fichiers ou de compétences | [Source] ; menu non capturé [À tester] |
| **Ajouter un fichier** (panneau de droite) | Sélecteur de fichiers de Windows ; le fichier est copié dans les **fichiers du projet** | [Vérifié pour l'ouverture du sélecteur] |
| **Connecter un dossier** (panneau de droite) | Dossier **externe** ([section 4](#4-fichiers-externes)) | [Vérifié pour l'ouverture du sélecteur] |
| Palette `@` | Référence à un fichier du projet | [Source] |

![Pièce jointe dans la zone de saisie](../img/bionic/06-documents/02-fichier-joint-composer.png)
*Figure 1 — Fichier glissé sur la zone de saisie : pastille « facture_test_1288.png » avec croix de retrait.*

> **Précaution** — les sélecteurs de fichiers ouvrent les dossiers personnels de l'utilisateur. Ne joindre que ce qui est nécessaire à la tâche.

---

## 3. Fichiers du projet

Zone **Fichiers du projet** du panneau de droite : fichiers **gérés par le projet**, partagés par **toutes les sessions** du projet. Les fichiers créés par l'agent y apparaissent. Un clic ouvre le fichier dans un onglet ([Manuel 02](02-interface.md#3-barre-donglets)).

| Caractéristique | Détail |
|---|---|
| Emplacement physique | `~\.lmstudio\apps\bionic\projects\<identifiant>\workspace` [Vérifié] |
| Partage | Toutes les sessions du projet |
| Suppression du projet | Les fichiers du projet résident dans les dossiers de l'application : conserver une copie des livrables importants ailleurs |

---

## 4. Fichiers externes

**Connecter un dossier** rend un dossier de l'ordinateur accessible à l'agent **sans le copier**. Il reste à son emplacement d'origine et s'affiche dans le panneau de droite.

| Point | Détail |
|---|---|
| Modification | **Directe sur l'original** : « When Bionic edits an external file, the change is made directly to that original file. » [Source] |
| Risque | Écrasement d'un fichier source |
| Parade | Travailler sur une **copie** ; versionner (Git) ; demander à l'agent de **créer un nouveau fichier** plutôt que de modifier l'original |
| Code | Un dossier **connecté** n'est **pas** un dossier de travail : voir [Manuel 05](05-projets-et-sessions.md#3-dossier-de-travail-ou-fichiers-du-projet) |

---

## 5. Exemple 1 : rédiger un mémo

**Consigne** : « Rédige un mémo de 6 lignes maximum sur les avantages d'un modèle de langage utilisé en local, et enregistre-le dans un fichier memo-ia-locale.md. »

| Paramètre | Valeur |
|---|---|
| Modèle | *Gemma 4 E4B* (local), raisonnement **Activé** |
| Mode shell | Vérification automatique (aucune commande nécessaire) |
| Durée | **2 min 4 s** (GPU dédié : **29 s** ; raisonnement désactivé : **≈ 15 s**) |
| Résultat | Fichier `memo-ia-locale.md` créé dans *Fichiers du projet* (**+7 −0** : 7 lignes ajoutées) |

![Mémo généré](../img/bionic/06-documents/01-memo-genere.png)
*Figure 2 — Réponse et fichier créé (bloc « Fichiers modifiés »), `memo-ia-locale.md` dans le panneau de droite.*

**Sur GPU dédié** (RTX 4060 Ti, 7 octobre 2026, modèle vérifié dans la base de sessions) : *Gemma 4 E4B*, raisonnement **Activé** : **29 s** ; **Désactivé** : **≈ 15 s** (mesuré de l'envoi à la fin) ; fichier créé dans les deux cas. Le **gain du raisonnement désactivé** reste d'environ moitié (GPU intégré : 2 min 4 s → 1 min 23 s, environ un tiers).

**Observation** : le fichier contient 7 lignes pour une consigne de « 6 lignes maximum » : les contraintes numériques sont à **vérifier** ; un petit modèle les respecte approximativement. Contenu rédigé en français, en 5 points (confidentialité, sécurité, hors ligne, personnalisation, coûts).

---

## 6. Exemple 2 : extraire les données d'une facture

Document : facture **fictive** (image PNG) comportant un numéro, une date, un client, trois lignes et des totaux.

**Consigne** : « Lis la facture jointe et enregistre dans un fichier facture.json : le numéro de facture, la date, le nom du client et le total TTC. Réponds en français. »

Deux modèles ont été comparés (même consigne, même image, une session par essai) :

| | *Gemma 4 E4B* (≈ 4 Md) | *Gemma 4 12B QAT* (≈ 12 Md) |
|---|---|---|
| Durée affichée | **55 s** | **4 min 25 s** (premier usage : inclut le chargement du modèle) |
| Valeurs lues | Correctes : `F-2026-0042`, `06/10/2026`, `Atelier Démo SARL`, `3060.00` | Correctes : `F-2026-0042`, `06/10/2026`, `Atelier Démo SARL`, `3 060,00 €` |
| Appel d'outil réel | **Aucun** | **Oui** (fichier créé) |
| Bloc **Fichiers modifiés** | **Absent** | `facture.json` **+6 −0** |
| `facture.json` sur le disque | **Inexistant** | Présent dans *Fichiers du projet* |
| Langue de la réponse | Français | Français |

**Rejeu sur GPU dédié** (7 octobre 2026, modèle vérifié dans la base de sessions ; l'ancienne valeur est entre parenthèses) :

| | *Gemma 4 E4B* | *Gemma 4 26B A4B* (remplace le 12B QAT, absent du poste) |
|---|---|---|
| Durée | **31 s** affichés (55 s) | **≈ 51 s** mesurés (12B : 4 min 25 s, chargement compris) |
| Valeurs lues | Correctes : `F-2026-0042`, `06/10/2026`, `Atelier Démo SARL`, `3060.00` | Correctes |
| Fichier `facture.json` | **Non créé** : le JSON est affiché dans la réponse, sans appel d'outil | **Créé** (bloc *Fichiers modifiés* `facture.json` **+6 −0**) |

Le constat d'**annonce d'action sans exécution** se **reproduit** avec l'E4B sur le GPU dédié, malgré une vitesse multipliée par ≈ 2 : la **vitesse du matériel ne corrige pas** le défaut. Le 26B réalise l'action demandée.

![Résultat avec Gemma 4 E4B](../img/bionic/06-documents/04-resultat-facture.png)
*Figure 3 — *Gemma 4 E4B* : réponse en 55 s, contenu juste, mais aucun fichier créé.*

![Résultat avec Gemma 4 12B QAT](../img/bionic/06-documents/05-resultat-facture-12b.png)
*Figure 4 — *Gemma 4 12B QAT* : fichier `facture.json` créé et listé dans « Fichiers du projet ».*

> **Constat essentiel — annonce d'action sans exécution.** Avec le petit modèle, la réponse indiquait : « J'ai utilisé l'outil `replace_file` pour créer et enregistrer ce fichier dans votre répertoire de travail. Le processus est terminé… ». **Aucun appel d'outil n'avait eu lieu** : ni ligne « 1 outil appelé », ni bloc *Fichiers modifiés*, et le fichier n'existait pas sur le disque. Le JSON affiché dans la réponse était exact, mais le livrable demandé (un fichier) n'existait pas.
>
> **Règle de contrôle** : après toute tâche qui doit produire un fichier, vérifier **(1)** la présence du bloc *Fichiers modifiés*, **(2)** le fichier dans le panneau de droite, **(3)** son contenu. Ne jamais se fier à la seule phrase de conclusion de l'agent.

Observations complémentaires [Vérifié] :

- Le fichier du modèle 12B utilise des clés accentuées (`numéro_de_facture`) et un total sous forme de **texte** (`"3 060,00 €"`) ; le petit modèle avait proposé des clés sans accents et un **nombre** (`3060.00`). Imposer le **schéma** dans la consigne (« clés : numero_facture, date, client, total_ttc ; total_ttc en nombre ») pour obtenir une sortie exploitable par un programme.
- Une image envoyée **sans texte** (pastille seule) est traitée comme une demande de description : le petit modèle a transcrit toute la facture (en anglais, avec des libellés traduits).

---

## 7. Formats pris en charge

| Type | Statut |
|---|---|
| Texte, Markdown, code | Création et modification [Vérifié : `.md`, `.py`] |
| Images (PNG, JPEG) | Lecture par un modèle à **vision** ou un **sous-agent de vision** [Vérifié : PNG] |
| Documents Word, tableurs, présentations, PDF | Pris en charge selon la documentation, avec aperçus et suivi des modifications [Source : journal des modifications] ; non testé [À tester] |

La liste exacte des extensions éditables et les limites de taille ne sont pas documentées [À tester].

---

## 8. Rédiger une bonne consigne documentaire

| Élément | Exemple |
|---|---|
| **Livrable** | « Un fichier `note.md` » |
| **Format** | « Tableau à trois colonnes : constat, risque, action » |
| **Longueur** | « 10 lignes maximum » |
| **Public / ton** | « Pour un comité de direction, ton impersonnel et direct » |
| **Sources** | « À partir des deux fichiers joints uniquement » |
| **Langue** | « Réponds en français » |
| **Interdits** | « Ne pas inventer de chiffres ; indiquer `non précisé` si l'information manque » |

Consigne type : « Compare les trois propositions jointes. Produis une note de décision avec une recommandation, les risques et un tableau comparatif. Enregistre-la sous `note-decision.md`. »

---

## 9. Fiabilité et contrôle

- **Toujours comparer** les valeurs extraites au document source (numéros, montants, dates).
- Demander à l'agent de **signaler les champs illisibles** plutôt que de les deviner.
- Pour un contenu à enjeu : **deux passes** (extraction, puis vérification des totaux par recalcul).
- Un modèle plus grand ou le raisonnement activé améliore la fiabilité au prix du temps ([Manuel 04](04-modeles.md#4-effort-de-raisonnement)).
- Les images sont consommatrices de contexte ; une session riche en images peut déclencher la **compaction** automatique [Source].
