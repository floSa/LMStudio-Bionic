"""Calculateur d'ordre de grandeur de la mémoire nécessaire pour charger un modèle de langage (format GGUF).

Formules :
    poids       = paramètres × bits par poids / 8
    cache KV    = 2 × couches × têtes KV × dimension d'une tête × octets par valeur × contexte
    total       ≈ poids (ou taille du fichier) + cache KV + tampons de calcul (≈ 0,5 Go)

Limites : le cache KV de certains modèles (attention à fenêtre glissante, modèles hybrides) est bien plus petit que la formule ;
l'« Estimated Memory Usage » de LM Studio ou `lms load <modèle> --estimate-only` fait foi.

Exemples :
    python 09_calculateur_memoire.py --params 7.62 --quant Q6_K --couches 28 --tetes-kv 4 --dim-tete 128 --contexte 16384
    python 09_calculateur_memoire.py --fichier-go 6.33 --ko-par-token 50 --contexte 8192
"""
import argparse

# Bits par poids effectifs (valeurs approchées déduites des tailles réelles de fichiers GGUF d'un modèle de 7,6 Md de paramètres)
BITS_PAR_POIDS = {
    "F32": 32.0, "F16": 16.0, "BF16": 16.0, "Q8_0": 8.5, "Q6_K": 6.56, "Q5_K_M": 5.7, "Q5_K_S": 5.5, "Q4_K_M": 4.9,
    "Q4_K_S": 4.7, "Q4_0": 4.5, "Q3_K_M": 4.0, "Q2_K": 3.2,
}
GO = 1e9
GIB = 2 ** 30


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--params", type=float, help="nombre de paramètres en milliards (ex. 7.62)")
    ap.add_argument("--quant", default="Q4_K_M", choices=sorted(BITS_PAR_POIDS), help="quantification des poids")
    ap.add_argument("--fichier-go", type=float, help="taille du fichier GGUF en Go (remplace paramètres × bits)")
    ap.add_argument("--couches", type=int, help="nombre de couches du modèle")
    ap.add_argument("--tetes-kv", type=int, help="nombre de têtes d'attention KV")
    ap.add_argument("--dim-tete", type=int, help="dimension d'une tête d'attention (souvent 64, 128 ou 256)")
    ap.add_argument("--ko-par-token", type=float, help="coût du cache KV par token en Ko (mesuré ou connu), remplace la formule")
    ap.add_argument("--contexte", type=int, default=8192, help="taille de contexte en tokens")
    ap.add_argument("--kv-bits", type=float, default=16, help="précision du cache KV : 16 (F16), 8,5 (Q8_0), 4,5 (Q4_0)")
    ap.add_argument("--tampons-go", type=float, default=0.5, help="marge pour les tampons de calcul")
    a = ap.parse_args()

    if a.fichier_go is not None:
        poids = a.fichier_go * GO
        origine = f"fichier de {a.fichier_go:.2f} Go"
    elif a.params:
        poids = a.params * GO * BITS_PAR_POIDS[a.quant] / 8
        origine = f"{a.params} Md de paramètres × {BITS_PAR_POIDS[a.quant]} bits / 8"
    else:
        ap.error("préciser --params ou --fichier-go")

    if a.ko_par_token is not None:
        kv_par_token = a.ko_par_token * 1000
    elif a.couches and a.tetes_kv and a.dim_tete:
        kv_par_token = 2 * a.couches * a.tetes_kv * a.dim_tete * (a.kv_bits / 8)
    else:
        kv_par_token = 0
    kv = kv_par_token * a.contexte
    total = poids + kv + a.tampons_go * GO

    print(f"Poids du modèle    : {poids / GO:6.2f} Go  ({origine})")
    print(f"Cache KV           : {kv / GO:6.2f} Go  ({kv_par_token / 1000:.0f} Ko/token × {a.contexte} tokens)" if kv_par_token else
          "Cache KV           :   n/d   (préciser --couches/--tetes-kv/--dim-tete ou --ko-par-token)")
    print(f"Tampons de calcul  : {a.tampons_go:6.2f} Go")
    print(f"TOTAL estimé       : {total / GO:6.2f} Go  ({total / GIB:.2f} Gio)")
    print(f"RAM conseillée     : {total / GO / 0.8:6.2f} Go  (marge de 20 % pour le système)")


if __name__ == "__main__":
    main()
