// Charge un modèle avec une configuration complète par le SDK JavaScript (paramètres absents de `lms load` et de l'API REST :
// quantification du cache K/V, taille de lot physique, arguments llama.cpp libres, décodage spéculatif…).
// Le modèle reste chargé sous l'identifiant donné ; la mesure se fait ensuite par l'API compatible OpenAI.
//
// Usage : node charger.mjs <cle-modele> <identifiant> '<configuration JSON>'
// Exemple : node charger.mjs google/gemma-4-e4b bench '{"contextLength":32768,"flashAttention":true,"llamaKCacheQuantizationType":"q8_0","llamaVCacheQuantizationType":"q8_0"}'
import { LMStudioClient } from "@lmstudio/sdk";

const [modele, identifiant, json] = process.argv.slice(2);
if (!modele || !identifiant) {
  console.error("usage: node charger.mjs <cle-modele> <identifiant> '<json>'");
  process.exit(2);
}
const config = json ? JSON.parse(json) : {};
const client = new LMStudioClient();
const t0 = Date.now();
try {
  const m = await client.llm.load(modele, { identifier: identifiant, config });
  const info = await m.getModelInfo();
  console.log(JSON.stringify({ ok: true, secondes: (Date.now() - t0) / 1000, identifiant: m.identifier, contexte: info.contextLength, config }));
} catch (e) {
  console.log(JSON.stringify({ ok: false, secondes: (Date.now() - t0) / 1000, erreur: String(e?.message ?? e).slice(0, 400), config }));
  process.exit(1);
}
process.exit(0);
