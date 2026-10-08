// Essai du SDK JavaScript de LM Studio (@lmstudio/sdk 2.0.0) : modèles disponibles, génération avec statistiques, sortie structurée,
// agent à outils (`act`), embeddings. Aucune donnée réelle. Le serveur LM Studio doit tourner (port 1234).
//
// Usage : node essai_sdk.mjs [cle-modele]      (défaut : google/gemma-4-e4b)
import { LMStudioClient, tool } from "@lmstudio/sdk";
import { z } from "zod";

const cle = process.argv[2] ?? "google/gemma-4-e4b";
const client = new LMStudioClient();
const sortie = {};

// 1. Version et modèles présents sur le disque
sortie.version = await client.system.getLMStudioVersion?.().catch(() => null);
sortie.modeles = (await client.system.listDownloadedModels()).map((m) => ({ cle: m.modelKey, type: m.type, taille_go: +(m.sizeBytes / 2 ** 30).toFixed(2) }));

// 2. Chargement paramétré puis génération avec statistiques
await client.llm.unload("essai-sdk").catch(() => {}); // reprise après un essai interrompu
const modele = await client.llm.load(cle, { identifier: "essai-sdk", config: { contextLength: 8192, flashAttention: true }, verbose: false });
const t0 = Date.now();
const r = await modele.respond([{ role: "user", content: "Réponds en une phrase : à quoi sert le cache KV ?" }], { temperature: 0, maxTokens: 1500 });
sortie.generation = { texte: r.content.slice(0, 200), secondes: (Date.now() - t0) / 1000, stats: r.stats };

// 3. Sortie structurée (schéma zod). maxTokens doit couvrir la réflexion : à 120 jetons, la réflexion de Gemma 4 E4B épuise la limite
//    avant le JSON et le SDK lève « Failed to parse structured output » (constaté le 7 octobre 2026).
const schema = z.object({ numero: z.string(), total_ttc: z.number() });
try {
  const s = await modele.respond([{ role: "user", content: "Extrais : Facture F-2026-0042, total TTC 3060 euros." }], { structured: schema, temperature: 0, maxTokens: 1500 });
  sortie.structure = { parsed: s.parsed };
} catch (e) {
  // Constaté avec SDK 2.0.0 + Gemma 4 E4B (modèle à réflexion) : le contenu renvoyé contient la réflexion, un marqueur interne
  // (__LM_STUDIO_INTERNAL_LSEP_SYNTHETIC_REASONING_END_…__) puis le JSON valide ; l'analyse automatique échoue sur la réflexion.
  const brut = JSON.parse(String(e.message).replace(/^Failed to parse structured output: /, ""));
  const apres = brut.split(/__LM_STUDIO_INTERNAL_LSEP_SYNTHETIC_REASONING_END_[0-9a-f]+__/)[1];
  sortie.structure = { erreur_sdk: String(e.message).slice(0, 80), json_apres_marqueur: apres ? JSON.parse(apres) : null };
}

// 4. Agent : le modèle appelle un outil local défini en JavaScript
const appels = [];
const convertir = tool({
  name: "convertir_temperature",
  description: "Convertit une température entre Celsius (C) et Fahrenheit (F).",
  parameters: { valeur: z.number(), de: z.enum(["C", "F"]), vers: z.enum(["C", "F"]) },
  implementation: ({ valeur, de, vers }) => {
    appels.push({ valeur, de, vers });
    if (de === vers) return String(valeur);
    return de === "C" ? String((valeur * 9) / 5 + 32) : String(((valeur - 32) * 5) / 9);
  },
});
const a0 = Date.now();
const res = await modele.act("Combien font 100 degrés Celsius en Fahrenheit ? Utilise l'outil.", [convertir], { onMessage: () => {} });
sortie.agent = { appels, secondes: (Date.now() - a0) / 1000, tours: res.rounds, reponse_finale: undefined };

// 5. Embeddings
const emb = await client.embedding.model("text-embedding-nomic-embed-text-v1.5");
const v = await emb.embed(["La centrale produit de l'électricité.", "Une usine génère du courant électrique."]);
sortie.embeddings = { dimension: v[0].embedding.length };

await modele.unload?.().catch(() => {});
console.log(JSON.stringify(sortie, null, 1));
process.exit(0);
