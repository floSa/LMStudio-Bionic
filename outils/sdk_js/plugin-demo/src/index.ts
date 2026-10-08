import { type PluginContext } from "@lmstudio/sdk";
import { toolsProvider } from "./toolsProvider";

export async function main(context: PluginContext) {
  // Enregistre le fournisseur d'outils : LM Studio le propose au modèle pendant la conversation.
  context.withToolsProvider(toolsProvider);
}
