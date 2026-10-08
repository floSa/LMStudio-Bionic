"""Supprime (via l'interface, donc vers la corbeille) les conversations de test créées pendant la production de la documentation.
Seuls les noms listés ci-dessous sont ciblés ; les conversations préexistantes de l'utilisateur ne sont jamais touchées."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lmcdp import LM

NOMS = ["Explique en trois ph", "Multiplication simple expliquée", "Multiplication de nombres entiers",
        "Multiplication Mathématiques Simple", "Quantification de LLMs expliquée", "Transcris fidèlement",
        "Glossaire LM Studio Définitions", "Invoice Transcription Formatting", "Facturation Service B2B",
        "Facture analyse des coûts", "Invoice Line Item Analysis",
        "Celsius to Fahrenheit Conversion", "LM Studio API Request Flow",
        "Calcul de Remise"]   # lot 2 : conversation de test des outils MCP

lm = LM(width=1440, height=900)
lm.close_dialogs(); lm.click_xy(21, 90); lm.wait(1.5)
supprimees = 0
for _ in range(25):
    cible = None
    for nom in NOMS:
        r = lm.rect(text=nom, exact=True)
        if r and r[0] < 280:
            cible = (nom, r)
            break
    if not cible:
        break
    nom, r = cible
    lm.click_xy(r[0] + 20, r[1] + r[3] / 2); lm.wait(0.8)            # sélectionne (fait apparaître le menu « … »)
    lm.click_xy(255, r[1] + r[3] / 2); lm.wait(0.8)                    # menu « … »
    d = lm.rect(text="Delete", exact=True)
    if not d:
        print("menu Delete introuvable pour", nom); lm.key("Escape"); break
    lm.click_xy(d[0] + 20, d[1] + d[3] / 2); lm.wait(1.0)
    c = lm.ev("""(() => { const d=document.querySelector('[role=dialog]'); if(!d) return null;
        const b=[...d.querySelectorAll('button')].filter(x=>/^delete/i.test((x.innerText||'').trim()))[0]; if(!b) return null;
        const r=b.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2]; })()""")
    if c:
        lm.click_xy(*c); lm.wait(1.5)
    supprimees += 1
    print("supprimée :", nom, flush=True)
print("total :", supprimees)
