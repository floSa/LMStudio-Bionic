"""Mesure l'effet de chaque paramètre de chargement sur l'« Estimated Memory Usage » affichée par LM Studio (aucun chargement réel)."""
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lmcdp import LM

lm = LM(width=1440, height=1500)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats")

ROW_JS = """((lab) => { const d=document.querySelector('[role=dialog]');
  const leaf=[...d.querySelectorAll('*')].filter(e=>e.children.length===0 && (e.textContent||'').trim()===lab)[0]; if(!leaf) return null;
  let p=leaf.parentElement, best=null;
  for (let i=0;i<6 && p && p!==d;i++) {
     if (p.getBoundingClientRect().height > 70) break;
     const ctl=[...p.querySelectorAll('input,button')].filter(b=>{const r=b.getBoundingClientRect();return r.width>0 && r.x>leaf.getBoundingClientRect().x+60 && !(b.className||'').toString().includes('cursor-help')});
     if (ctl.length) best=ctl;
     p=p.parentElement; }
  return best ? best.map(b=>{const r=b.getBoundingClientRect();return [b.tagName, r.x+r.width/2, r.y+r.height/2, (b.innerText||b.value||'').trim()]}) : null; })(%s)"""


def controls(label):
    return lm.ev(ROW_JS % json.dumps(label))


def raw_est():
    t = lm.ev("document.querySelector('[role=dialog]').innerText")
    head = t.split("Model file")[0].replace("\n", " ")
    nums = re.findall(r"(?:GPU|Total)\s+([\d.]+)\s*(GB|MB)", head)
    vals = [float(a) / (1 if b == "GB" else 1000) for a, b in nums]
    return (vals[0], vals[1]) if len(vals) >= 2 else (None, head[:120])


def est():
    """Attend que l'estimation soit stable (3 lectures identiques)."""
    last, same = None, 0
    t0 = time.time()
    while time.time() - t0 < 12:
        time.sleep(0.8)
        cur = raw_est()
        same = same + 1 if cur == last else 0
        last = cur
        if same >= 3:
            break
    return {"gpu": last[0], "total": last[1]}


def set_num(label, value):
    c = controls(label)
    inp = [x for x in c if x[0] == "INPUT"][0]
    lm.set_value(inp[1], inp[2], value)


def toggle(label):
    c = controls(label)
    b = [x for x in c if x[0] == "BUTTON"][0]
    lm.click_xy(b[1], b[2])


def open_loader():
    lm.close_dialogs(); lm.wait(1)
    lm.click_xy(21, 90); lm.wait(1)
    lm.send("Input.dispatchKeyEvent", type="keyDown", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
    lm.send("Input.dispatchKeyEvent", type="keyUp", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
    lm.wait(1.5)
    r = lm.rect(selector="[role=dialog] *", text="Gemma 4 E4B", exact=False)
    lm.click_xy(r[0] + 20, r[1] + r[3] / 2); lm.wait(2)
    assert "Estimated Memory Usage" in lm.ev("document.querySelector('[role=dialog]').innerText"), "chargeur non ouvert"


def pick_quant(label, value):
    """Coche la quantification (si besoin) puis choisit une valeur dans la liste déroulante."""
    c = controls(label)
    chk = [x for x in c if x[0] == "BUTTON"][0]
    sel = [x for x in c if x[0] == "BUTTON"]
    if len(sel) == 1:                     # seulement la case : la cocher fait apparaître la liste
        lm.click_xy(chk[1], chk[2]); lm.wait(0.8)
        c = controls(label); sel = [x for x in c if x[0] == "BUTTON"]
    drop = sel[-1]
    lm.click_xy(drop[1], drop[2]); lm.wait(0.8)
    lm.click(selector="[role=option]", text=value, exact=True); lm.wait(0.8)


res = {}
open_loader()
res["valeurs_initiales"] = lm.ev("[...document.querySelectorAll('[role=dialog] input')].map(e=>e.value)")
set_num("Context Length", 8192); res["ctx8192_ref"] = est()
set_num("Max Concurrent Predictions", 1); res["ctx8192_parallel1"] = est()
set_num("Max Concurrent Predictions", 4)
for ngl in (0, 12, 24, 36, 42):
    set_num("GPU Offload", ngl); res[f"ctx8192_gpu{ngl}"] = est()
set_num("GPU Offload", 42); est()
for pb in (128, 1024, 2048):
    set_num("Physical Batch Size", pb); res[f"physical_batch_{pb}"] = est()
set_num("Physical Batch Size", 512); est()
for ev_ in (512, 8192):
    set_num("Evaluation Batch Size", ev_); res[f"eval_batch_{ev_}"] = est()
set_num("Evaluation Batch Size", 2048); est()
toggle("Offload KV Cache to GPU Memory"); res["ctx8192_kv_cpu"] = est(); toggle("Offload KV Cache to GPU Memory"); est()
print(json.dumps(res, indent=1), flush=True)

for ctx in (32768, 131072):
    set_num("Context Length", ctx); res[f"ctx{ctx}_F16_F16"] = est()
    pick_quant("K Cache Quantization Type", "Q8_0"); res[f"ctx{ctx}_K_Q8_V_F16"] = est()
    pick_quant("V Cache Quantization Type", "Q8_0"); res[f"ctx{ctx}_K_Q8_V_Q8"] = est()
    pick_quant("K Cache Quantization Type", "Q4_0"); pick_quant("V Cache Quantization Type", "Q4_0"); res[f"ctx{ctx}_K_Q4_V_Q4"] = est()
    # retour aux valeurs par défaut : décocher les cases
    for lab in ("K Cache Quantization Type", "V Cache Quantization Type"):
        c = controls(lab); chk = [x for x in c if x[0] == "BUTTON"][0]; lm.click_xy(chk[1], chk[2]); lm.wait(0.6)
    print(ctx, {k: v for k, v in res.items() if k.startswith(f"ctx{ctx}")}, flush=True)
set_num("Context Length", 8192)
json.dump(res, open(os.path.join(OUT, "estimation_gui.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
lm.click(selector="[role=dialog] button", text="Cancel"); lm.wait(1)
lm.close_dialogs()
