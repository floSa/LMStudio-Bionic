# Manuel 08 — Recettes par cas d'usage

> **Objet** : fiches de configuration prêtes à adapter pour les usages courants : modèle, paramètres de chargement, paramètres d'inférence, prompt, contrôles et pièges.
> **Prérequis** : Manuels [03](03-charger-un-modele.md) et [04](04-parametrer-l-inference.md).
> **Nature des valeurs** : points de départ à **valider sur des exemples réels** ; la recommandation de l'éditeur du modèle prévaut. Les valeurs chiffrées issues du poste de test sont signalées.

---

## Sommaire

1. [Dimensionner la machine](#1-dimensionner-la-machine)
2. [Tableau de synthèse](#2-tableau-de-synthèse)
3. [Fiches](#3-fiches)
4. [Prompts types](#4-prompts-types)
5. [Méthode de réglage](#5-méthode-de-réglage)

---

## 1. Dimensionner la machine

Ordres de grandeur généraux pour le format GGUF (**[Estimation]**, à confirmer avec l'*Estimated Memory Usage* de LM Studio et `lms load --estimate-only`) :

| RAM disponible (hors système) | Modèles envisageables | Contexte raisonnable | Remarques |
|---|---|---|---|
| **8 Go** | ≤ 3-4 Md de paramètres en Q4_K_M | 2 048 – 4 096 | Usage léger ; peu de marge |
| **16 Go** | 7-8 Md en Q4_K_M à Q6_K | 4 096 – 16 384 | Configuration courante |
| **32 Go** | 7-8 Md en Q8_0 ; 12-14 Md en Q4_K_M à Q6_K | 8 192 – 32 768 | Poste de test (31 Go) |
| **64 Go et plus** | 30 Md et plus, modèles *mixture-of-experts* | 32 768 et plus | Souvent avec GPU dédié |

Calcul détaillé et calculateur : [Manuel 00, section 7](00-notions-fondamentales.md#7-calculer-la-ram-nécessaire).

Règles :

- **Mémoire nécessaire ≈ fichier + cache KV + 0,5 Go**, soit ≈ fichier + (contexte × coût par token) ; voir [Manuel 03](03-charger-un-modele.md#2-composition-de-la-mémoire).
- Garder **≥ 20 % de RAM libre** pour le système et les autres applications.
- La **vitesse de génération** dépend surtout de la **bande passante mémoire** : un modèle deux fois plus gros génère environ deux fois plus lentement.
- Un GPU **intégré** accélère modérément (≈ +30 % mesuré en génération, [Manuel 03](03-charger-un-modele.md#54-vitesse-selon-le-déchargement-gpu)) ; un GPU **dédié** change l'échelle de performance (**× 5** en génération par rapport au CPU seul, **× 77** en lecture du prompt : [Manuel 15](15-performances-gpu-dedie.md)).

> **Exemple (poste de test)** — Modèle de 7,5 Md (Q4_K_M, 6,33 Go) : ≈ 15 tok/s en génération, ≈ 340 tok/s en traitement du prompt ; mémoire estimée 6,6 Go à 8 192 tokens. **Sur un GPU dédié de 16 Go** (même modèle en Q8_0, 9,02 Go) : ≈ 45 tok/s et ≈ 3 700 tok/s ; VRAM réelle 6,1 Go à 8 192 tokens (estimation 9,1 Gio).

---

## 2. Tableau de synthèse

| Cas d'usage | Modèle | Contexte | Température | Thinking | Remarque clé |
|---|---|---|---|---|---|
| [A. Rédaction, reformulation, résumé](#a-rédaction-reformulation-résumé) | Généraliste Q4_K_M | 4 096 – 8 192 | 0,3 – 0,8 | Désactivé | Préciser ton, longueur, public |
| [B. Questions sur documents](#b-questions-sur-documents-internes) | Généraliste | ≥ taille du document + 2 000 | 0,1 – 0,3 | Désactivé | Demander des citations |
| [C. Extraction structurée](#c-extraction-structurée-json) | Généraliste | 4 096 | **0** | Désactivé | *Structured Output* (JSON Schema) |
| [D. OCR de pages](#d-ocr-de-pages) | Vision / OCR dédié | ≥ 16 384 | 0 – 0,1 | Désactivé | Résolution ; Repeat = 1,0 |
| [E. Classification en lot](#e-classification--étiquetage-en-lot) | Petit modèle rapide | 2 048 | **0** | Désactivé | Sortie courte ; `seed` |
| [F. Assistance au code](#f-assistance-au-code) | Modèle orienté code | 8 192 et plus | 0,1 – 0,3 | Selon complexité | Contexte large |
| [G. Raisonnement, calcul](#g-raisonnement-calcul) | Modèle à raisonnement | 8 192 et plus | Recommandation éditeur | **Activé** | Prévoir temps et tokens |
| [H. Service d'équipe](#h-service-dapi-déquipe) | Selon la charge | Par utilisateur × nombre | 0,2 – 0,5 | Désactivé | Authentification, file d'attente |
| [I. Machine à ressources limitées](#i-machine-à-ressources-limitées) | ≤ 4 Md, Q4_K_M | 2 048 – 4 096 | 0,3 – 0,7 | Désactivé | Fermer les autres applications |

---

## 3. Fiches

### A. Rédaction, reformulation, résumé

| | |
|---|---|
| **Chargement** | Contexte 8 192 ; GPU offload maximum ; 1 requête simultanée ; Flash Attention activé |
| **Inférence** | Température 0,3 (résumé) à 0,8 (rédaction) ; Top P 0,95 ; Min P 0,05 ; *Repeat Penalty* 1,05 – 1,15 ; thinking désactivé |
| **Prompt système** | Rôle, public, ton, langue, longueur maximale, format de sortie |
| **Contrôle** | Relecture humaine ; comparaison avec le texte source (aucune information ajoutée) |
| **Pièges** | Informations inventées dans un résumé ; style générique ; dérive de langue |

### B. Questions sur documents internes

| | |
|---|---|
| **Méthode** | Joindre le document au chat ([Manuel 05](05-vision-images-et-ocr.md#8-joindre-un-document-texte-pdf)) : injection intégrale si le document tient dans le contexte, sinon récupération par passages |
| **Chargement** | Contexte ≥ document + question + réponse (marge de 2 000 tokens) |
| **Inférence** | Température 0,1 – 0,3 ; thinking désactivé |
| **Prompt système** | « Répondre uniquement à partir du document ; citer le passage ; répondre "information absente" si nécessaire. » |
| **Contrôle** | Vérifier chaque citation dans le document |
| **Pièges** | Réponse tirée de la connaissance générale du modèle et non du document ; document tronqué si le contexte est trop petit |
| **Exemple mesuré** | Glossaire de 6 Ko : question sur une définition → réponse exacte, stratégie *inject-full-content*, 3,7 s avant le premier token |

### C. Extraction structurée (JSON)

| | |
|---|---|
| **Chargement** | Contexte 4 096 ; 1 requête |
| **Inférence** | Température **0** ; *Structured Output* avec JSON Schema ([Manuel 04](04-parametrer-l-inference.md#8-sortie-structurée)) ; thinking désactivé |
| **API** | `response_format` de type `json_schema` ([`exemples/04_sortie_json_schema.py`](../../exemples/04_sortie_json_schema.py)) |
| **Contrôle** | Validation du schéma (garantie par le moteur) **et** des valeurs (cohérence métier : sommes, dates) |
| **Pièges** | Schéma conforme mais valeurs fausses : le schéma garantit la **forme**, pas l'**exactitude** |
| **Exemple mesuré** | Facture fictive → 4 champs corrects, 73 tokens, 8,8 s |

### D. OCR de pages

| | |
|---|---|
| **Modèle** | Modèle de vision généraliste (*Gemma 4 E4B*) ; pour un volume important, modèle d'OCR dédié tel qu'OlmOCR 2 7B ([Manuel 05, section 6](05-vision-images-et-ocr.md#6-choisir-un-modèle-pour-lire-des-images)) |
| **Chargement** | Contexte ≥ 16 384 ; 1 requête ; cache KV en F16 |
| **Inférence** | Température 0 – 0,1 ; *Repeat Penalty* 1,0 ; *Context Overflow* = *Stop at Limit* ; réponse limitée à 8 000 tokens ; thinking désactivé |
| **Entrée** | Une page par requête, image à la résolution attendue (1288 px de grand côté pour OlmOCR 2), page à l'endroit |
| **Contrôle** | Jeu de test annoté ; contrôles de cohérence automatiques sur les montants |
| **Pièges** | Colonnes décalées à basse résolution ; erreurs silencieuses sur les chiffres ; historique d'images dans une même conversation |
| **Exemple mesuré** | 1288 px : exact ; 640 px : tableau décalé |

### E. Classification / étiquetage en lot

| | |
|---|---|
| **Chargement** | Petit modèle rapide ; contexte 2 048 ; 1 requête |
| **Inférence** | Température **0** ; `seed` fixe ; réponse courte (limite de 20 – 50 tokens) ; sortie structurée (liste fermée de valeurs) |
| **Méthode** | Boucle côté script ; une requête par élément ; journalisation des résultats |
| **Contrôle** | Matrice de confusion sur un échantillon étiqueté à la main |
| **Pièges** | Étiquettes hors liste (corrigé par le schéma) ; dérive entre versions de modèle |

### F. Assistance au code

| | |
|---|---|
| **Chargement** | Contexte 8 192 et plus (le code consomme du contexte) ; GPU offload maximum |
| **Inférence** | Température 0,1 – 0,3 ; *Repeat Penalty* 1,0 ; thinking activé pour les problèmes complexes |
| **Prompt** | Langage, version, contraintes, tests attendus ; fournir les extraits pertinents plutôt que tout le dépôt |
| **Contrôle** | Exécution des tests ; relecture ; analyse de sécurité du code généré |
| **Pièges** | API ou bibliothèques inexistantes ; code non sécurisé ; plugin d'exécution de code : confirmation manuelle ([Manuel 04](04-parametrer-l-inference.md#41-longlet-integrations)) |

### G. Raisonnement, calcul

| | |
|---|---|
| **Chargement** | Contexte 8 192 et plus (la réflexion consomme des tokens) |
| **Inférence** | Thinking **activé** ; paramètres recommandés par l'éditeur ; *Reasoning Budget* si un plafond est nécessaire |
| **Contrôle** | Vérification indépendante du résultat |
| **Exemple mesuré** | Calcul 17 × 23 : thinking actif = 394 tokens (15 s de réflexion) ; désactivé = 224 tokens ; résultat correct dans les deux cas ([Manuel 04](04-parametrer-l-inference.md#6-raisonnement-thinking)) |
| **Pièges** | Temps de réponse multiplié par ≈ 2 pour un gain nul sur les tâches simples |

### H. Service d'API d'équipe

| | |
|---|---|
| **Sécurité** | Profil B du [Manuel 06](06-serveur-local-et-api.md#5-sécurité) : réseau activé **seulement** avec authentification, jeton par application, pare-feu, journaux |
| **Chargement** | Contexte = besoin par requête × concurrence ; *Max Concurrent Predictions* ajusté après **mesure du débit total** |
| **Mesure clé** | Sur GPU intégré, 4 requêtes simultanées : 12,8 tok/s au total (contre 14,8 tok/s pour une seule) — la concurrence **n'augmente pas** le débit. **Sur GPU dédié** (RTX 4060 Ti) : **152 à 160 tok/s** pour 4 requêtes (45 pour une), **264 tok/s** pour 8 — la concurrence **multiplie** le débit : toujours mesurer sur le matériel cible |
| **Architecture** | File d'attente côté application ; délais d'attente ; relance ; ne pas dépendre d'une erreur sur nom de modèle erroné (redirection vers le modèle chargé) |
| **Contrôle** | Test de charge avec le nombre réel d'utilisateurs ; supervision de la mémoire |

### I. Machine à ressources limitées

| | |
|---|---|
| **Modèle** | ≤ 4 Md de paramètres, Q4_K_M ; éventuellement Q3_K_M |
| **Chargement** | Contexte 2 048 – 4 096 ; *Keep Model in Memory* désactivé ; *Try mmap()* activé ; cache KV en Q8_0 (si besoin) ; GPU offload partiel |
| **Hygiène** | Fermer les applications gourmandes ; vérifier l'*Estimated Memory Usage* et la marge de RAM |
| **Pièges** | Swap disque (lenteur extrême) ; garde-fous contournés avec `Alt` |

---

## 4. Prompts types

À adapter ; exemples de structure, non validés sur un modèle précis sauf mention.

**Résumé**

```text
Rôle : assistant de synthèse pour des responsables techniques.
Tâche : résumer le texte fourni en 5 puces maximum, chaque puce de 20 mots maximum.
Règles : ne rien ajouter qui ne figure pas dans le texte ; conserver les chiffres exacts ; répondre en français.
```

**Questions sur document**

```text
Répondre uniquement à partir du document joint.
Citer entre guillemets le passage qui justifie chaque réponse.
Si l'information est absente du document, répondre exactement : « Information absente du document ».
```

**Extraction**

```text
Extraire les champs demandés du texte. Si un champ est absent, renvoyer null. Ne rien déduire, ne rien reformuler.
```

**OCR (modèle généraliste)** *(utilisé dans les essais du [Manuel 05](05-vision-images-et-ocr.md))*

```text
Transcris fidèlement tout le texte de ce document en Markdown (conserve le tableau). Ne rajoute aucun commentaire.
```

**OCR (OlmOCR 2)** : prompt officiel du [Manuel 05, section 7.4](05-vision-images-et-ocr.md#74-prompt), à recopier tel quel.

---

## 5. Méthode de réglage

1. **Fixer l'objectif mesurable** (taux d'erreur, temps par document, qualité jugée par un relecteur).
2. **Constituer un jeu de test** de 10 à 20 cas représentatifs, avec réponse attendue.
3. **Partir de la fiche** du cas d'usage ; ne modifier **qu'un paramètre à la fois**.
4. **Rejouer** le jeu de test avec une graine fixe et une température 0 pour comparer proprement.
5. **Relever** : qualité, durée, tokens (statistiques du chat ou champ `usage` de l'API), mémoire.
6. **Enregistrer** la configuration retenue dans un **preset** ([Manuel 04](04-parametrer-l-inference.md#9-presets)) et dans les valeurs par défaut du modèle ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#104-onglets-load-et-inference--valeurs-par-défaut-du-modèle)).
7. **Documenter** : modèle (nom exact, quantification), version de LM Studio et du moteur, paramètres, résultats.
