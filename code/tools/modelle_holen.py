"""
Vorbereitungs-Werkzeug fuer die Lehrkraft - NICHT fuer den Workshop selbst.

Laedt die beiden vortrainierten Modelle nach models/ herunter.
Normalerweise liegen sie schon im Repository. Dieses Skript ist der
Ersatzweg, falls eine Datei fehlt oder beschaedigt ist.

Aufruf:
    uv run code/tools/modelle_holen.py
"""

import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import faceit  # noqa: E402

BASIS = "https://github.com/opencv/opencv_zoo/raw/main/models"

MODELLE = [
    (faceit.YUNET,
     f"{BASIS}/face_detection_yunet/face_detection_yunet_2023mar.onnx",
     "YuNet - findet Gesichter im Bild"),
    (faceit.SFACE,
     f"{BASIS}/face_recognition_sface/face_recognition_sface_2021dec.onnx",
     "SFace - rechnet ein Gesicht in 128 Zahlen um"),
]


def laden(ziel: Path, quelle: str, beschreibung: str):
    print(f"  {beschreibung}")
    print(f"    Quelle: {quelle}")
    anfrage = urllib.request.Request(
        quelle, headers={"User-Agent": "FaceItWorkshop/1.0"})
    with urllib.request.urlopen(anfrage, timeout=120) as antwort:
        daten = antwort.read()

    # ONNX-Dateien beginnen nicht mit HTML - so erkennen wir Fehlerseiten.
    if daten[:1] == b"<":
        faceit.abbruch(f"Statt des Modells kam eine Fehlerseite zurueck: {quelle}",
                       "Pruefe die Internetverbindung oder lade die Datei manuell.")

    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_bytes(daten)
    print(f"    gespeichert: {ziel}  ({len(daten) / 1024 / 1024:.1f} MB)")
    print()


faceit.titel("Modelle herunterladen (Vorbereitung)",
             "Aus dem OpenCV Model Zoo, Lizenz: Apache 2.0 bzw. MIT")

for ziel, quelle, beschreibung in MODELLE:
    laden(ziel, quelle, beschreibung)

# Zum Schluss pruefen, ob OpenCV die Dateien wirklich laden kann
detektor = faceit.detektor_laden()
erkenner = faceit.erkenner_laden()
print("  Beide Modelle wurden geladen und funktionieren.")
print()
