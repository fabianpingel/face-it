"""
Vorbereitungs-Werkzeug fuer die Lehrkraft - NICHT fuer den Workshop selbst.

Erzeugt den QR-Code fuer die letzte Folie ("zum Mitnehmen").
Das Ergebnis liegt danach als material/folien/qr.svg und wird von der
Folie automatisch angezeigt.

Braucht das Zusatzpaket segno:
    uv sync --extra werkzeuge

Aufruf:
    uv run code/tools/qr_erzeugen.py
    uv run code/tools/qr_erzeugen.py https://github.com/name/face-it
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import faceit  # noqa: E402

STANDARD_URL = "https://github.com/fabianpingel/face-it"

try:
    import segno
except ImportError:
    faceit.abbruch(
        "Das Paket segno fehlt.",
        "Installieren mit:   uv sync --extra werkzeuge",
        "",
        "Alternative ohne Installation: einen QR-Code online erzeugen und",
        "als material/folien/qr.svg oder qr.png ablegen.",
    )

url = sys.argv[1] if len(sys.argv) > 1 else STANDARD_URL

faceit.titel("QR-Code erzeugen (Vorbereitung)", f"Ziel: {url}")

ziel = faceit.MATERIAL / "folien" / "qr.svg"
ziel.parent.mkdir(parents=True, exist_ok=True)

# Farben wie im Workshop-Logo, damit die Folie einheitlich aussieht
segno.make(url, error="m").save(
    str(ziel), scale=8, border=2,
    dark="#0c1a2b", light="#ffffff",
)

print(f"  geschrieben: {ziel}")
print()
print("  Die Folie material/folien/index.html zeigt den Code jetzt automatisch an.")
print("  Kurz gegenprueft: einmal mit dem eigenen Handy scannen.")
print()
