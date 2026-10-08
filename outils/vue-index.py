#!/usr/bin/env python3
"""Vue économe de index.html (et des autres pages) pour Claude Code et les humains.

Tronque les lignes trop longues (DEMO, I18N) et remplace tout base64 restant
par <B64:…Ko>, en gardant les numéros de ligne d'origine.

Exemples :
  python3 outils/vue-index.py                      # tout le fichier, allégé
  python3 outils/vue-index.py 560 620              # lignes 560 à 620
  python3 outils/vue-index.py -g "PAIEMENT|RESIL"  # lignes qui contiennent le motif
  python3 outils/vue-index.py -f cgv.html 1 40     # autre fichier
"""
import argparse
import re
import sys

B64 = re.compile(r"(data:[a-z]+/[a-z0-9+.-]+;base64,)([A-Za-z0-9+/=]{200,})")


def alleger(ligne, maxlen):
    ligne = B64.sub(lambda m: f"{m.group(1)}<B64:{len(m.group(2)) * 3 // 4 // 1024} Ko>", ligne)
    if len(ligne) > maxlen:
        ligne = ligne[:maxlen] + f" …[tronqué : {len(ligne)} caractères]"
    return ligne


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("debut", nargs="?", type=int, default=1)
    p.add_argument("fin", nargs="?", type=int, default=None)
    p.add_argument("-f", "--fichier", default="index.html")
    p.add_argument("-g", "--grep", help="expression régulière : n'affiche que les lignes qui la contiennent")
    p.add_argument("-l", "--max", type=int, default=400, help="longueur maximale d'une ligne affichée (défaut 400)")
    a = p.parse_args()
    motif = re.compile(a.grep) if a.grep else None
    with open(a.fichier, encoding="utf-8") as fh:
        for n, ligne in enumerate(fh, 1):
            if n < a.debut:
                continue
            if a.fin and n > a.fin:
                break
            ligne = ligne.rstrip("\n")
            if motif and not motif.search(ligne):
                continue
            sys.stdout.write(f"{n:>5}  {alleger(ligne, a.max)}\n")


if __name__ == "__main__":
    main()
