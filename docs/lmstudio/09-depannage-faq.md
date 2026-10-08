# Manuel 09 — Dépannage et FAQ

> **Objet** : diagnostic rapide des problèmes courants, commandes de contrôle et réponses aux questions fréquentes.
> **Version décrite** : LM Studio 0.4.25.
> Les tableaux de dépannage détaillés figurent aussi à la fin des manuels concernés ; cette page les regroupe par symptôme.

---

## Sommaire

1. [Méthode de diagnostic](#1-méthode-de-diagnostic)
2. [Commandes de contrôle](#2-commandes-de-contrôle)
3. [Installation, lancement, mises à jour](#3-installation-lancement-mises-à-jour)
4. [Modèles et téléchargements](#4-modèles-et-téléchargements)
5. [Chargement et mémoire](#5-chargement-et-mémoire)
6. [Qualité des réponses](#6-qualité-des-réponses)
7. [Performances](#7-performances)
8. [Serveur et API](#8-serveur-et-api)
9. [Images, OCR, documents](#9-images-ocr-documents)
10. [Réseau, sécurité, données](#10-réseau-sécurité-données)
11. [FAQ](#11-faq)
12. [Informations à joindre à une demande de support](#12-informations-à-joindre-à-une-demande-de-support)

---

## 1. Méthode de diagnostic

1. **Reproduire** le problème et noter le message exact.
2. **Isoler** : modèle (essayer un autre), chargement (réglages par défaut), interface ou API (comparer `lms chat` et l'interface).
3. **Vérifier l'état** : `lms status`, `lms ps`, page *Hardware* (mémoire), *Developer Logs*.
4. **Changer un seul paramètre à la fois**, puis rejouer.
5. **Consulter les journaux** : *Developer Logs*, `lms log stream`, `Settings → General → Open app logs`.

---

## 2. Commandes de contrôle

| Objectif | Commande (PowerShell) |
|---|---|
| État général | `lms status` |
| Modèles chargés | `lms ps` |
| Modèles installés | `lms ls` |
| Serveur démarré ? | `lms server status` |
| Serveur joignable ? | `curl.exe http://127.0.0.1:1234/v1/models` |
| Adresse d'écoute du serveur | `Get-NetTCPConnection -LocalPort 1234 -State Listen \| Select-Object LocalAddress, LocalPort` |
| Matériel vu par le moteur | `lms runtime survey` |
| Moteurs installés | `lms runtime ls` |
| Estimation mémoire sans charger | `lms load <modèle> -c <contexte> --estimate-only -y` |
| Intégrité du dossier de modèles | `Get-ChildItem $env:USERPROFILE\.lmstudio\models -Recurse -File \| Measure-Object Length -Sum` |
| Journaux en direct | `lms log stream` |
| Mémoire libre | *Settings → Hardware → Resource Monitor* ou le Gestionnaire des tâches |

---

## 3. Installation, lancement, mises à jour

| Symptôme | Cause probable | Action |
|---|---|---|
| L'application ne démarre pas | Instance précédente bloquée ; profil corrompu | Terminer les processus `LM Studio` dans le Gestionnaire des tâches ; relancer |
| La commande `lms` est introuvable | `PATH` sans `…\.lmstudio\bin` | Ajouter le dossier au `PATH` ; relancer le terminal ([Manuel 07](07-cli-lms.md#11-dépannage)) |
| Téléchargements non sollicités, consommation de données | Mise à jour automatique des moteurs ; proxy Hugging Face | *Settings → Runtime* : désactiver l'auto-update ; contrôler le panneau *Downloads* ([Manuel 01](01-prise-en-main.md#8-points-de-vigilance)) |
| Interface en anglais | Langue par défaut | *Settings → General → App Language* (fonction « en développement ») |
| Comportement différent après une mise à jour | Nouveau moteur ou nouveau réglage | Comparer avec la version précédente du moteur (`lms runtime ls`) ; sélectionner l'ancien moteur si besoin |
| Une page du chat reste vide après un redimensionnement de fenêtre | Défaut d'affichage | Recharger l'interface (redémarrer l'application) |

---

## 4. Modèles et téléchargements

| Symptôme | Cause probable | Action |
|---|---|---|
| Modèle copié à la main **absent de la liste** | Structure de dossier incorrecte ; liste non actualisée | Respecter `models\<éditeur>\<dépôt>\` ; *Refresh model list* ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#101-organisation-des-fichiers)) |
| Le modèle **ne voit pas les images** | Fichier `mmproj` absent | Placer `mmproj-*.gguf` dans le dossier du modèle |
| Mauvaise catégorie (LLM / embedding) | Détection erronée | *My Models → Info → Domain Control* |
| Téléchargement impossible ou très lent | Réseau filtré ou limité | Télécharger ailleurs puis importer ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#8-installer-un-modèle-sans-connexion)) |
| `lms import` reste en attente | Fichier déjà dans le dossier des modèles ; question interactive | Utiliser un fichier extérieur ; ajouter `-y` |
| Espace disque insuffisant | Modèles volumineux | *Settings → General → Models Directory → Change…* ; supprimer les modèles inutiles |

---

## 5. Chargement et mémoire

| Symptôme | Cause probable | Action |
|---|---|---|
| Chargement **bloqué par un garde-fou** | Estimation > limite | Réduire contexte ou quantification ; libérer la mémoire ; ajuster les garde-fous (déconseillé) |
| **Échec de chargement** / plantage | Mémoire insuffisante | Diminuer *Context Length* ; réduire *GPU Offload* ; désactiver *Offload KV Cache* |
| Machine très **lente** après chargement | Mémoire saturée | Estimation < 80 % de la RAM libre ; quantification inférieure |
| Estimation différente entre l'interface et `lms` | Valeurs par défaut différentes ; unités GB / GiB | Comparer à paramètres identiques |
| Un réglage de chargement « ne change rien » | Rechargement nécessaire | Décharger puis recharger |
| Le contexte demandé n'est pas appliqué | Maximum du modèle atteint | Consulter *Model supports up to … tokens* |

Détail : [Manuel 03](03-charger-un-modele.md#8-dépannage).

---

## 6. Qualité des réponses

| Symptôme | Cause probable | Action |
|---|---|---|
| Réponses **coupées** | *Limit Response Length* ; contexte plein | Augmenter la limite ; augmenter le contexte (recharger) |
| Réponses **différentes** à chaque essai | Température > 0 | Température 0 ou graine fixe |
| **Répétitions**, boucles | Température trop basse ; pas de pénalité | *Repeat Penalty* 1,05 – 1,15 |
| Texte **incohérent** | Température ou Top P élevés | Baisser la température ; Top P ≤ 0,95 |
| Chiffres altérés (OCR, extraction) | *Repeat Penalty* > 1 ; température | Repeat = 1,0 ; température 0 – 0,1 |
| Début de conversation **oublié** | Contexte saturé | Augmenter le contexte ; résumer l'historique |
| Informations **inventées** | Limite du modèle | Fournir la source ; exiger des citations ; vérifier |
| **Réflexion** dans une autre langue | Comportement du modèle (réflexion en anglais pour une question en français) | Normal ; la réponse finale suit la langue de la question |
| Mélange de langues dans la réponse | Prompt ambigu ; modèle peu entraîné au français | Préciser la langue dans le prompt système |

Détail : [Manuel 04](04-parametrer-l-inference.md#12-dépannage).

---

## 7. Performances

| Symptôme | Cause probable | Action |
|---|---|---|
| Génération lente | Couches sur CPU ; contexte plein ; plusieurs requêtes | Vérifier *GPU Offload* ; vider le contexte ; 1 requête à la fois |
| Délai long avant le premier mot | Thinking actif ; long prompt ; première requête (chauffe du moteur) | Désactiver le thinking ; réduire le prompt ; ignorer la première requête dans les mesures |
| Débit total identique avec plusieurs requêtes | GPU intégré limité par la bande passante | Normal **sur GPU intégré** ; sur GPU dédié le débit total doit croître : vérifier *Max Concurrent Predictions* ([Manuel 03](03-charger-un-modele.md#55-concurrence-selon-le-matériel)) |
| Modèle plus gros que la VRAM : génération lente avec `GPU Offload : max` | La carte déborde dans la mémoire partagée (bus PCIe) | Laisser le réglage **automatique**, ou un ratio (0,75), ou placer les experts d'un modèle MoE sur le CPU ([Manuel 15, section 6](15-performances-gpu-dedie.md#6-modèles-plus-gros-que-la-vram)) |
| Lecture du prompt 3 fois plus lente qu'attendue sur GPU dédié | Flash Attention désactivée, lot d'évaluation ou lot physique trop petit (< 256) | Réactiver Flash Attention ; revenir aux lots par défaut ([Manuel 15, section 4](15-performances-gpu-dedie.md#4-flash-attention-lots-et-cache-kv)) |
| L'estimation annonce « trop gros » alors que le modèle tient | L'estimation **surestime** la VRAM (jusqu'à × 2 à grand contexte) | Charger avec un contexte réduit puis mesurer ; lire l'estimation comme un maximum ([Manuel 15, section 5](15-performances-gpu-dedie.md#5-mémoire-réelle-et-estimation)) |
| `Model not found` avec `lms load` sur une variante listée par `lms ls` | Limite de la ligne de commande | Charger par le SDK ou par l'interface ([Manuel 16](16-sdk-et-plugins.md#3-paramètres-de-chargement-accessibles-par-le-sdk)) |
| Vitesse très inférieure à une autre machine | Matériel, moteur ou quantification différents | Comparer moteur, quantification, contexte, offload |
| Variation de vitesse d'un essai à l'autre | Mesure sur un seul essai ; charge de la machine | Répéter 3 fois ; fermer les applications |

---

## 8. Serveur et API

| Symptôme | Cause probable | Action |
|---|---|---|
| Connexion refusée | Serveur arrêté ; port | `lms server status` ; port dans *Server Settings* |
| Inaccessible depuis un autre poste | *Serve on Local Network* désactivé ; pare-feu | Voir [Manuel 06](06-serveur-local-et-api.md#5-sécurité) avant toute ouverture |
| `401` | Authentification activée sans jeton | En-tête `Authorization: Bearer <jeton>` |
| Erreur « CORS » dans un navigateur | *Enable CORS* désactivé | L'activer pour une page maîtrisée uniquement |
| Réponse malgré un nom de modèle erroné | Redirection vers le modèle chargé | Contrôler le champ `model` de la réponse |
| Premier appel très long | Chargement JIT | Charger le modèle à l'avance |
| Accents corrompus (PowerShell) | Encodage du corps de requête | Envoyer en UTF-8 explicite |
| Réflexion trop longue | Modèle à raisonnement | `reasoning_effort: "none"` |
| Valeurs de sampling inattendues | Défauts du modèle appliqués aux paramètres absents | Préciser `temperature`, `top_p`, `seed` |

Détail : [Manuel 06](06-serveur-local-et-api.md#11-dépannage).

---

## 9. Images, OCR, documents

| Symptôme | Cause probable | Action |
|---|---|---|
| « Aucune image » perçue | `mmproj` absent ; modèle sans vision | Vérifier la pastille Vision et le `mmproj` |
| Tableau décalé, petits caractères faux | Résolution insuffisante | Image au grand côté recommandé |
| Page tronquée | Contexte ou limite insuffisants | Augmenter contexte et *Limit Response Length* |
| Résultat influencé par une image précédente | Historique de conversation | Une conversation vierge par essai |
| Document ignoré | Fichier non joint ; vide | Rejoindre ; vérifier le contenu |
| Très lent | Thinking actif ; image volumineuse | Désactiver le thinking ; résolution adaptée |

Détail : [Manuel 05, dépannage](05-vision-images-et-ocr.md#12-dépannage), [Manuel 05, limites d'OlmOCR 2](05-vision-images-et-ocr.md#79-limites-et-pièges-de-ce-modèle).

---

## 10. Réseau, sécurité, données

| Sujet | Contrôle | Action |
|---|---|---|
| Exposition du serveur | `Get-NetTCPConnection -LocalPort 1234 -State Listen` | `127.0.0.1` attendu ; sinon désactiver *Serve on Local Network*. Le serveur peut **redémarrer seul** au lancement de l'application : contrôler après chaque démarrage ([Manuel 06](06-serveur-local-et-api.md#2-démarrer-et-arrêter-le-serveur)) |
| Conversations en clair | `%USERPROFILE%\.lmstudio\conversations` | Exclure de la synchronisation ; chiffrer le disque |
| Journaux et historique d'API | `server-logs\`, `.internal\api-prediction-history\` | Contiennent des prompts : confidentialité identique aux conversations |
| Connexion à un compte (LM Link, Hub) | *Account* : « Signed out » | Ne pas se connecter sans validation ; ne pas publier de presets internes (*Publish…*) |
| Outils / MCP | *Settings → Integrations*, `mcp.json` | Garder la confirmation manuelle ; aucun serveur MCP à accès disque exposé à des clients non authentifiés |
| Téléchargements | Panneau *Downloads* | Désactiver les mises à jour automatiques sur réseau limité |

---

## 11. FAQ

**Pourquoi un modèle « 4B » est-il affiché « 7.5B » ?**
Le chiffre affiché inclut des tables d'*embeddings* par couche ; le modèle est conçu pour calculer sur ≈ 4,5 Md de paramètres « effectifs ». La taille mémoire suit le chiffre affiché.

**Quelle quantification choisir ?**
Q4_K_M par défaut ; Q6_K ou Q8_0 pour la précision (OCR, chiffres). Voir [Manuel 02](02-selectionner-et-telecharger-un-modele.md#5-les-quantifications).

**Le contexte maximal annoncé (131 072 tokens) peut-il être utilisé ?**
Techniquement oui, au prix d'une mémoire multipliée (≈ +50 Ko par token pour un modèle de 7-8 Md) : 12,7 Go au lieu de 6,6 Go dans l'exemple mesuré. Dimensionner selon le besoin réel.

**Le GPU intégré apporte-t-il beaucoup ?**
Modérément : ≈ +30 % de vitesse de génération et ≈ +65 % de traitement du prompt dans l'exemple mesuré ([Manuel 03](03-charger-un-modele.md#54-vitesse-selon-le-déchargement-gpu)).

**Plusieurs requêtes simultanées accélèrent-elles le service ?**
Pas sur ce type de matériel : le débit total reste constant, chaque requête est ralentie.

**Faut-il désactiver le thinking ?**
Pour les tâches mécaniques (extraction, OCR, classification, reformulation) : oui. Pour le calcul, la logique et le code complexe : non ([Manuel 04](04-parametrer-l-inference.md#6-raisonnement-thinking)).

**Comment obtenir des réponses reproductibles ?**
Température 0, ou graine fixe avec les mêmes paramètres ; préciser ces paramètres dans chaque requête d'API.

**Les données quittent-elles le poste ?**
Pas pour l'inférence locale. Restent à surveiller : mises à jour automatiques de moteurs, proxy Hugging Face, LM Link, publication de presets, exposition réseau du serveur.

**Peut-on utiliser LM Studio sans connexion Internet ?**
Oui, une fois l'application, les moteurs et les modèles installés. Importer les modèles par copie ([Manuel 02](02-selectionner-et-telecharger-un-modele.md#8-installer-un-modèle-sans-connexion)).

**Quelle est la différence entre LM Studio et Bionic ?**
Bionic est une application agent distincte (code, documents) ; LM Studio fournit l'inférence et l'API. Manuels dédiés à venir.

**Où sont stockés les réglages ?**
`%USERPROFILE%\.lmstudio\settings.json` (application) et `config-presets\` (presets) ; valeurs par défaut par modèle dans `.internal\`.

**Comment déplacer le dossier des modèles ?**
*Settings → General → Models Directory → Change…*, après avoir copié les modèles vers le nouvel emplacement ; puis *Refresh model list*.

---

## 12. Informations à joindre à une demande de support

- version de LM Studio et du moteur (`lms runtime ls`) ;
- résumé matériel (*Settings → Hardware → Copy Info* ou `lms runtime survey`) ;
- modèle (nom exact, quantification, taille) et paramètres de chargement (capture de la fenêtre de chargement) ;
- paramètres d'inférence (preset ou capture) ;
- message d'erreur exact et extrait de *Developer Logs* (**sans données confidentielles**) ;
- étapes de reproduction minimales.
