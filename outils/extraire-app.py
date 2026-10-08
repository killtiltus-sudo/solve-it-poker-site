#!/usr/bin/env python3
"""Récupère le code JavaScript de l'application publiée, pour la lire sans la reconstruire.

Le code source de l'application de bureau n'est pas dans ce dépôt : seuls les
binaires sont publiés dans les releases GitHub. Ce script télécharge le zip
Windows de la release (la plus récente par défaut), le décompresse et extrait
le paquet Electron (app.asar) dans un dossier HORS du dépôt.

Exemples :
  python3 outils/extraire-app.py                    # dernière release -> /tmp/solve-it-poker-app
  python3 outils/extraire-app.py -d ~/app -t v0.35.0

Ensuite, lire l'interface (13,5 Mo, données de ranges sur 4 lignes géantes) avec :
  python3 outils/vue-index.py -f /tmp/solve-it-poker-app/asar/app/index.html -g "motif"
"""
import argparse
import json
import os
import struct
import subprocess
import zipfile

DEPOT = "https://github.com/killtiltus-sudo/solve-it-poker-site/releases"
ZIP = "Solve-It-Poker-Windows.zip"


def extraire_asar(src, dst):
    with open(src, "rb") as f:
        data = f.read()
    _, hsize, _, slen = struct.unpack("<IIII", data[:16])
    entete = json.loads(data[16:16 + slen].decode("utf-8"))
    base = 8 + hsize

    def parcourir(noeud, chemin):
        for nom, ent in noeud.get("files", {}).items():
            p = os.path.join(chemin, nom)
            if "files" in ent:
                os.makedirs(p, exist_ok=True)
                parcourir(ent, p)
            elif "offset" in ent and not ent.get("unpacked"):
                debut = base + int(ent["offset"])
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "wb") as o:
                    o.write(data[debut:debut + ent["size"]])

    os.makedirs(dst, exist_ok=True)
    parcourir(entete, dst)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-d", "--dossier", default="/tmp/solve-it-poker-app", help="dossier de sortie (hors du dépôt)")
    p.add_argument("-t", "--tag", help="release voulue (ex. v0.35.0) ; par défaut la plus récente")
    a = p.parse_args()
    os.makedirs(a.dossier, exist_ok=True)
    url = f"{DEPOT}/download/{a.tag}/{ZIP}" if a.tag else f"{DEPOT}/latest/download/{ZIP}"
    zp = os.path.join(a.dossier, ZIP)
    print("Téléchargement :", url)
    subprocess.run(["curl", "-fsSL", "-o", zp, url], check=True)
    with zipfile.ZipFile(zp) as z:
        z.extractall(os.path.join(a.dossier, "zip"))
    asar = next(os.path.join(r, "app.asar") for r, _, fs in os.walk(os.path.join(a.dossier, "zip")) if "app.asar" in fs)
    extraire_asar(asar, os.path.join(a.dossier, "asar"))
    print("Code JavaScript :", os.path.join(a.dossier, "asar"))
    print("Moteur et OCR (fichiers non empaquetés) :", asar + ".unpacked")


if __name__ == "__main__":
    main()
