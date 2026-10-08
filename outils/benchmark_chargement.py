"""Benchmark de paramètres de chargement (GPU offload, parallélisme) sur Gemma 4 E4B via `lms` + API locale.
Résultats : outils/resultats/benchmark_chargement.json (ou le fichier donné par la variable SORTIE_JSON). Le modèle est rechargé dans sa configuration d'origine à la fin."""
import json, os, subprocess, threading, time, urllib.request

BASE = "http://127.0.0.1:1234"
MODEL = "google/gemma-4-e4b"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats")
FILLER = "La production d'électricité repose sur un ensemble de procédés industriels complexes. " * 140


def lms(*args, timeout=600):
    t0 = time.time()
    r = subprocess.run(["lms", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return time.time() - t0, (r.stdout + r.stderr).strip()


def stream(prompt, max_tokens, model_id):
    body = {"model": model_id, "messages": [{"role": "user", "content": prompt}], "stream": True,
            "temperature": 0, "max_tokens": max_tokens, "reasoning_effort": "none"}
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time(); first = None; n = 0
    with urllib.request.urlopen(req, timeout=900) as r:
        for line in r:
            line = line.decode().strip()
            if not line.startswith("data:") or line.endswith("[DONE]"):
                continue
            ch = json.loads(line[5:])
            if ch.get("choices") and ch["choices"][0]["delta"].get("content"):
                if first is None:
                    first = time.time() - t0
                n += 1
    end = time.time() - t0
    return {"ttft": first, "chunks": n, "total": end, "decode_tok_s": (n - 1) / (end - first) if first and n > 1 and end > first else None}


def run(label, gpu, ctx, parallel):
    lms("unload", "--all")
    dt, out = lms("load", MODEL, "--gpu", gpu, "-c", str(ctx), "--parallel", str(parallel), "--identifier", "bench", "-y")
    res = {"label": label, "gpu": gpu, "ctx": ctx, "parallel": parallel, "load_s": round(dt, 1)}
    stream("ok", 3, "bench")  # échauffement
    pp = stream(FILLER + "\n\nRésume en une phrase.", 40, "bench")
    res["prompt_2100_tokens_ttft_s"] = round(pp["ttft"], 2)
    res["prompt_eval_tok_s"] = round(2119 / pp["ttft"], 0) if pp["ttft"] else None
    gen = stream("Écris un paragraphe de 120 mots sur l'histoire de l'électricité.", 200, "bench")
    res["decode_tok_s_single"] = round(gen["decode_tok_s"], 2) if gen["decode_tok_s"] else None
    if parallel > 1:
        results = []
        def worker():
            results.append(stream("Écris un paragraphe de 120 mots sur l'histoire de l'électricité.", 150, "bench"))
        ths = [threading.Thread(target=worker) for _ in range(parallel)]
        t0 = time.time()
        [t.start() for t in ths]; [t.join() for t in ths]
        wall = time.time() - t0
        toks = sum(r["chunks"] for r in results)
        res["parallel_total_tok_s"] = round(toks / wall, 2)
        res["parallel_per_request_tok_s"] = round(sum(r["decode_tok_s"] or 0 for r in results) / len(results), 2)
    print(json.dumps(res, ensure_ascii=False), flush=True)
    return res


if __name__ == "__main__":
    est = {}
    for ctx in (2048, 8192, 32768, 131072):
        _, out = lms("load", MODEL, "-c", str(ctx), "--estimate-only", "-y")
        est[str(ctx)] = out
        print("estimate", ctx, out.replace("\n", " | ")[:300], flush=True)
    results = [run("GPU max, parallel 4 (défaut)", "max", 8192, 4),
              run("GPU max, parallel 1", "max", 8192, 1),
              run("GPU 50 %, parallel 1", "0.5", 8192, 1),
              run("GPU off (CPU), parallel 1", "off", 8192, 1)]
    json.dump({"estimates": est, "runs": results}, open(os.path.join(OUT, os.environ.get("SORTIE_JSON", "benchmark_chargement.json")), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    lms("unload", "--all")
    dt, out = lms("load", MODEL, "--gpu", "max", "-c", "8192", "--parallel", "4", "--identifier", MODEL, "-y")
    print("restauré", round(dt, 1), out[-200:], flush=True)
