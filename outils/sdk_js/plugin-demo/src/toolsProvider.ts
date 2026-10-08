import { text, tool, type Tool, type ToolsProviderController } from "@lmstudio/sdk";
import { z } from "zod";

// Deux outils inoffensifs : un calcul pur et la lecture de l'heure locale. Aucun accès aux fichiers ni au réseau.
export async function toolsProvider(_ctl: ToolsProviderController) {
  const tools: Tool[] = [];

  tools.push(
    tool({
      name: "prix_avec_remise",
      description: text`
        Calcule le prix final après une remise exprimée en pourcentage.
        Paramètres : prix (nombre), remise_pourcent (nombre entre 0 et 100).
      `,
      parameters: { prix: z.number(), remise_pourcent: z.number().min(0).max(100) },
      implementation: async ({ prix, remise_pourcent }) => {
        return { prix_initial: prix, remise_pourcent, prix_final: Math.round(prix * (1 - remise_pourcent / 100) * 100) / 100 };
      },
    }),
  );

  tools.push(
    tool({
      name: "heure_locale",
      description: "Donne la date et l'heure locales de l'ordinateur (format ISO 8601).",
      parameters: {},
      implementation: async () => ({ heure_locale: new Date().toString() }),
    }),
  );

  return tools;
}
