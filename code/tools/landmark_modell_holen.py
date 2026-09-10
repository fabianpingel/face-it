"""
Vorbereitungs-Werkzeug fuer die Lehrkraft - NICHT fuer den Workshop selbst.

Laedt das Landmark-Modell fuer die optionale Station 3b nach
models/lbfmodel.yaml herunter (rund 54 MB).

Station 3b legt 68 Punkte auf das Gesicht und verbindet sie zu einem
Dreiecksnetz - genau das Bild aus dem Workshop-Logo. Ohne dieses Modell
laeuft die Station trotzdem, zeigt dann aber nur die fuenf Punkte von YuNet.

Aufruf:
    uv run code/tools/landmark_modell_holen.py
"""

import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import faceit  # noqa: E402

QUELLE = ("https://raw.githubusercontent.com/kurnianggoro/GSOC2017/"
          "master/data/lbfmodel.yaml")

faceit.titel("Landmark-Modell herunterladen (Vorbereitung)",
             "Fuer die optionale Station 3b - rund 54 MB, das dauert einen Moment.")

try:
    import cv2
    if not hasattr(cv2, "face"):
        faceit.abbruch(
            "Dieses OpenCV kennt das Modul cv2.face nicht.",
            "Erwartet wird opencv-contrib-python. Bitte ausfuehren:",
            "    uv sync",
        )
except ImportError:
    faceit.abbruch("OpenCV ist nicht installiert. Bitte 'uv sync' ausfuehren.")

ziel = faceit.MODELLE / "lbfmodel.yaml"
ziel.parent.mkdir(parents=True, exist_ok=True)

# Schon vorhanden? Dann nicht noch einmal 54 MB laden.
if ziel.exists() and ziel.stat().st_size > 50_000_000 and "--neu" not in sys.argv:
    marker = cv2.face.createFacemarkLBF()
    marker.loadModel(str(ziel))
    print(f"  Das Modell ist schon da und funktioniert: {ziel}")
    print(f"  ({ziel.stat().st_size / 1024 / 1024:.1f} MB)")
    print()
    print("  Noch einmal laden erzwingen:  uv run code/tools/landmark_modell_holen.py --neu")
    print()
    sys.exit(0)

print(f"  Quelle: {QUELLE}")
anfrage = urllib.request.Request(QUELLE, headers={"User-Agent": "FaceItWorkshop/1.0"})
with urllib.request.urlopen(anfrage, timeout=300) as antwort:
    daten = antwort.read()

if not daten.startswith(b"%YAML"):
    faceit.abbruch("Die geladene Datei ist kein YAML-Modell.",
                   "Pruefe die Internetverbindung und starte erneut.")

ziel.write_bytes(daten)
print(f"  gespeichert: {ziel}  ({len(daten) / 1024 / 1024:.1f} MB)")
print()

# Gegenpruefen: kann OpenCV das Modell wirklich laden?
marker = cv2.face.createFacemarkLBF()
marker.loadModel(str(ziel))
print("  Das Modell wurde geladen und funktioniert.")
print()
print("  Weiter mit:  uv run code/03b_landmarks.py")
print()
