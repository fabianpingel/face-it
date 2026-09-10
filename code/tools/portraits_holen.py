"""
Vorbereitungs-Werkzeug fuer die Lehrkraft - NICHT fuer den Workshop selbst.

Laedt freie Portraitfotos von Wikimedia Commons nach data/beispiele/.
Diese Bilder brauchen wir fuer Schuelerinnen und Schueler, die sich nicht
fotografieren lassen moechten - sie arbeiten dann mit diesen Gesichtern.

Es werden ausschliesslich Bilder heruntergeladen, die
  - unter CC0 oder Public Domain stehen (also frei verwendbar),
  - genau ein klar erkennbares Gesicht enthalten.
Zu jedem Bild wird Quelle, Urheber und Lizenz in data/beispiele/CREDITS.md
protokolliert.

Aufruf (einmal vor dem Workshop, mit Internetverbindung):
    uv run code/tools/portraits_holen.py
"""

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import faceit  # noqa: E402

API = "https://commons.wikimedia.org/w/api.php"
KOPFZEILE = {"User-Agent": "FaceItWorkshop/1.0 (Schulprojekt Computer Vision)"}

# Freie Lizenzen. Die Bilder werden NICHT ins Repository eingecheckt, sondern
# bleiben lokal - deshalb genuegt die Nennung von Urheber und Lizenz in CREDITS.md.
ERLAUBTE_LIZENZEN = ("cc0", "public domain", "pd-", "cc-zero",
                     "cc by 2.0", "cc by 3.0", "cc by 4.0",
                     "cc by-sa 2.0", "cc by-sa 3.0", "cc by-sa 4.0")

# Erst CC0 (meist moderne Fotos, vielfaeltigere Auswahl), dann Public Domain
SUCHBEGRIFFE = [
    "face portrait photograph woman smiling",
    "face portrait photograph man smiling",
    "headshot photograph teenager face",
    "face portrait photograph elderly woman",
    "face portrait photograph african person",
    "face portrait photograph asian person",
    "face portrait photograph south american person",
    "portrait photograph face person neutral background",
]

# Gemaelde und Zeichnungen aussortieren - wir brauchen Fotos
MALEREI = ("painting", "oil on canvas", "drawing", "engraving", "lithograph",
           "etching", "sketch", "watercolor", "aquarell", "portrait of",
           "self-portrait", "gemaelde", "gemälde", "zeichnung", "statue",
           "bust", "sculpture", "coin", "stamp", "medal", "museum", "gallery",
           "anonymous", "unknown painter", "portret", "bildnis", "-1 -", "17th",
           "18th", "19th century")

ANZAHL = 8


def api(**parameter):
    parameter.setdefault("format", "json")
    parameter.setdefault("formatversion", "2")
    url = API + "?" + urllib.parse.urlencode(parameter)
    anfrage = urllib.request.Request(url, headers=KOPFZEILE)
    with urllib.request.urlopen(anfrage, timeout=30) as antwort:
        return json.load(antwort)


def lizenz_ok(lizenz: str) -> bool:
    lizenz = (lizenz or "").lower()
    return any(erlaubt in lizenz for erlaubt in ERLAUBTE_LIZENZEN)


def kandidaten(begriff, anzahl=12):
    daten = api(action="query", generator="search", gsrsearch=f"filetype:bitmap {begriff}",
                gsrnamespace=6, gsrlimit=anzahl, prop="imageinfo",
                iiprop="url|extmetadata|size", iiurlwidth=600)
    for seite in daten.get("query", {}).get("pages", []):
        info = seite.get("imageinfo", [{}])[0]
        meta = info.get("extmetadata", {})
        yield {
            "titel": seite["title"],
            "url": info.get("thumburl") or info.get("url"),
            "seite": info.get("descriptionurl", ""),
            "lizenz": meta.get("LicenseShortName", {}).get("value", "?"),
            "urheber": meta.get("Artist", {}).get("value", "unbekannt"),
        }


def html_weg(text: str) -> str:
    """Entfernt HTML-Reste aus den Urheberangaben der API."""
    ergebnis, in_tag = [], False
    for zeichen in text:
        if zeichen == "<":
            in_tag = True
        elif zeichen == ">":
            in_tag = False
        elif not in_tag:
            ergebnis.append(zeichen)
    return " ".join("".join(ergebnis).split())[:90]


def genau_ein_gesicht(rohdaten: bytes, detektor):
    bild = cv2.imdecode(np.frombuffer(rohdaten, np.uint8), cv2.IMREAD_COLOR)
    if bild is None or min(bild.shape[:2]) < 200:
        return None
    gesichter = faceit.gesichter_finden(detektor, bild)
    if len(gesichter) != 1:
        return None
    _, _, breite, hoehe = gesichter[0][:4]
    if breite < 80 or hoehe < 80:      # Gesicht zu klein fuer ein gutes Embedding
        return None
    return bild


def main():
    faceit.titel("Portraits beschaffen (Vorbereitung)",
                 "Laedt freie Portraitfotos fuer den Workshop herunter.")
    ziel = faceit.daten_ordner("beispiele")
    detektor = faceit.detektor_laden()
    erkenner = faceit.erkenner_laden()

    gefunden, gesehen, vektoren = [], set(), []
    for begriff in SUCHBEGRIFFE:
        if len(gefunden) >= ANZAHL:
            break
        print(f"  Suche: {begriff}")
        try:
            liste = list(kandidaten(begriff))
        except Exception as fehler:
            print(f"    Suche fehlgeschlagen: {fehler}")
            continue

        # Hoechstens zwei Bilder pro Suchbegriff - sonst kommen alle Portraits
        # aus derselben Suche und die Auswahl wird einseitig.
        pro_begriff = 0
        for kandidat in liste:
            if len(gefunden) >= ANZAHL or pro_begriff >= 2:
                break
            if kandidat["titel"] in gesehen or not kandidat["url"]:
                continue
            gesehen.add(kandidat["titel"])
            if not lizenz_ok(kandidat["lizenz"]):
                continue
            titel_klein = kandidat["titel"].lower()
            if any(wort in titel_klein for wort in MALEREI):
                continue
            try:
                anfrage = urllib.request.Request(kandidat["url"], headers=KOPFZEILE)
                with urllib.request.urlopen(anfrage, timeout=30) as antwort:
                    rohdaten = antwort.read()
            except Exception:
                continue

            bild = genau_ein_gesicht(rohdaten, detektor)
            if bild is None:
                continue

            # Doppelte Bilder erkennen - mit genau dem Modell, das wir im
            # Workshop benutzen. Zwei Fassungen desselben Fotos waeren als
            # Beispielmaterial nutzlos.
            gesicht = faceit.gesichter_finden(detektor, bild)[0]
            vektor = faceit.gesicht_zu_zahlen(erkenner, bild, gesicht)
            if any(faceit.aehnlichkeit(vektor, vorhanden) > 0.7
                   for vorhanden in vektoren):
                print("    (uebersprungen: dieselbe Person ist schon dabei)")
                continue
            vektoren.append(vektor)

            nummer = len(gefunden) + 1
            dateiname = f"portrait_{nummer:02d}.jpg"
            cv2.imwrite(str(ziel / dateiname), bild)
            kandidat["datei"] = dateiname
            gefunden.append(kandidat)
            pro_begriff += 1
            print(f"    [{nummer}/{ANZAHL}] {dateiname}  ({kandidat['lizenz']})")

    if not gefunden:
        faceit.abbruch("Es konnte kein passendes Bild geladen werden.",
                       "Pruefe die Internetverbindung und starte erneut.")

    zeilen = [
        "# Bildnachweise",
        "",
        "Die Portraits in diesem Ordner stammen von Wikimedia Commons und stehen",
        "unter CC0 oder Public Domain. Sie dienen als Ersatzgesichter fuer alle,",
        "die sich im Workshop nicht selbst fotografieren moechten.",
        "",
        "| Datei | Titel | Urheber | Lizenz | Quelle |",
        "|---|---|---|---|---|",
    ]
    for eintrag in gefunden:
        titel_kurz = eintrag["titel"].replace("File:", "").replace("|", "/")
        zeilen.append(
            f"| `{eintrag['datei']}` | {titel_kurz} | {html_weg(eintrag['urheber'])} "
            f"| {eintrag['lizenz']} | [Commons]({eintrag['seite']}) |"
        )
    (ziel / "CREDITS.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")

    print()
    print(f"  Fertig: {len(gefunden)} Portraits in {ziel}")
    print(f"  Bildnachweise in {ziel / 'CREDITS.md'}")
    print()


if __name__ == "__main__":
    main()
