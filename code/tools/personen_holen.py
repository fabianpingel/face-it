"""
Vorbereitungs-Werkzeug fuer die Lehrkraft - NICHT fuer den Workshop selbst.
Wird nur auf dem BEAMER-Rechner gebraucht, so wie das Landmark-Modell.

Laedt Portraits bekannter Persoenlichkeiten aus Mathematik und Informatik nach
data/personen/. Sie sind die Beamer-Demo in Station 4b.

Warum dieser Satz zusaetzlich zu data/beispiele/?
  data/beispiele/ enthaelt Ersatzgesichter fuer SuS, die sich nicht fotografieren
  lassen moechten - acht verschiedene, demografisch gemischte Personen. Dieser
  Ordner ist das Gegenteil: MEHRERE Aufnahmen DERSELBEN Person aus verschiedenen
  Lebensaltern. Damit gehen Fragen, die mit acht Fremden nicht gehen:
      Erkennt das Modell Einstein als Kind und Einstein mit 41 wieder?
      Erkennt es Katherine Johnson 1966 und 2008 wieder?
  Die Klasse kann bei "ich gegen ich" nur Brille, Frisur und Licht veraendern.
  Zwanzig oder vierzig Jahre Abstand kann sie nicht herstellen.

Drei Regeln, nach denen die Liste zusammengestellt ist:
  1) Nur VERSTORBENE Personen. Ein Gesichtsvektor ist biometrische Verarbeitung
     nach Art. 9 DSGVO, und eine CC-Lizenz deckt nur das Urheberrecht, nicht
     Persoenlichkeitsrecht und Datenschutz. Bei lebenden Personen wuerde der
     Workshop genau das tun, was er an Clearview AI kritisiert.
  2) Nur PUBLIC DOMAIN, kein CC BY und kein CC BY-SA. Grund: diese Bilder landen
     am Beamer und auf Ausdrucken. Public Domain heisst keine Namensnennungs-
     pflicht und keine Share-alike-Folge fuer den zugeschnittenen Ausschnitt.
     (data/beispiele/ enthaelt CC-BY-Bilder - die bleiben deshalb lokal.)
  3) Feste, handgepruefte Dateiliste - KEINE Suche. Eine Commons-Suche nach
     Personennamen ist unzuverlaessig: unter "Willy Brandt" liefert sie ein Foto
     von Romy Schneider, unter "Adenauer" ein Fluechtlingsfoto, und
     "Gauss 1840 by Jensen" ist ein Gemaelde. Diese Liste IST der pruefbare
     Herkunftsnachweis - CREDITS.md liegt nur lokal und ist gitignoriert.

Die Bilder werden NICHT ins Repository eingecheckt (siehe .gitignore).

Aufruf (einmal vor dem Workshop, mit Internetverbindung):
    uv run code/tools/personen_holen.py
    uv run code/tools/personen_holen.py --klein     nur die sechs wichtigsten
    uv run code/tools/personen_holen.py --messen     nichts laden, nur neu messen
"""

import itertools
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import faceit  # noqa: E402

# Nur dieser Texthelfer wird geteilt - er saeubert die HTML-Reste, die die
# Commons-API in der Urheberangabe liefert. portraits_holen.py schuetzt sein
# main() mit __name__, der Import fuehrt also nichts aus.
from portraits_holen import html_weg  # noqa: E402

API = "https://commons.wikimedia.org/w/api.php"
KOPFZEILE = {"User-Agent": "FaceItWorkshop/1.0 (Schulprojekt Computer Vision)"}

# Absichtlich enger als in portraits_holen.py: siehe Regel 2 im Kopf.
ERLAUBTE_LIZENZEN = ("cc0", "public domain", "pd-", "cc-zero")

# WICHTIG fuer die Reproduzierbarkeit der Messwerte in docs/03_loesungen.md:
# Commons liefert ein Vorschaubild in der hier gewaehlten Breite. Eine andere
# Breite ergibt einen anderen Bildausschnitt nach alignCrop und damit andere
# Aehnlichkeitswerte. Wer diese Zahl aendert, muss die Tabelle in
# docs/03_loesungen.md neu messen. Sie steht deshalb auch in CREDITS.md.
THUMB_BREITE = 900

# Wikimedia beantwortet zu viele Anfragen in kurzer Folge mit HTTP 429 - das
# passiert schon bei einem Dutzend Dateien.
PAUSE = 0.5
VERSUCHE = 4

# ----------------------------------------------------------------------------
# Die Liste.
#   lokal      Dateiname bei uns. Der Teil vor dem ersten Unterstrich ist der
#              Personenschluessel; daran erkennen Skript und Tests, welche
#              Bilder dieselbe Person zeigen. Rein ASCII - der Commons-Titel
#              von Lise Meitner enthaelt einen Gedankenstrich.
#   titel      Commons-Titel, exakt. Wird NIE auf die Konsole gedruckt (eine
#              cp1252-Konsole bricht am Gedankenstrich ab), nur in CREDITS.md.
#   person     Klartext fuer CREDITS.md und die Ausgabe.
#   jahr       Aufnahmejahr, NUR wenn es auf Commons belegt ist. Sonst "?" -
#              geraten wird hier nichts.
#   klein      gehoert zur Sechser-Auswahl (--klein)
# ----------------------------------------------------------------------------
PERSONEN = [
    ("einstein_kind.jpg", "Albert Einstein as a child.jpg",
     "Albert Einstein als Kind (1879-1955)", "?", True),
    ("einstein_1920.jpg", "Albert Einstein photo 1920.jpg",
     "Albert Einstein mit 41", "1920", True),
    ("einstein_nobel.jpg", "Albert Einstein (Nobel).png",
     "Albert Einstein zum Nobelpreis", "?", False),

    ("johnson_1966.jpg", "Katherine Johnson at NASA, in 1966.jpg",
     "Katherine Johnson, NASA-Mathematikerin (1918-2020)", "1966", True),
    ("johnson_2008.jpg", "Katherine Johnson in 2008.jpg",
     "Katherine Johnson, 42 Jahre spaeter", "2008", True),

    ("turing_16.jpg", "Alan Turing Aged 16.jpg",
     "Alan Turing mit 16 (1912-1954)", "?", True),
    ("turing_1951.jpg", "Alan Turing (1951).jpg",
     "Alan Turing mit 39", "1951", True),

    ("hilbert_1886.jpg", "David Hilbert 1886.jpg",
     "David Hilbert mit 24 (1862-1943)", "1886", False),
    ("hilbert_spaet.jpg", "Hilbert.jpg",
     "David Hilbert als aelterer Mann", "?", False),

    ("noether.jpg", "Noether.jpg",
     "Emmy Noether, Algebra (1882-1935)", "?", False),
    ("hopper.jpg", "Grace Hopper.jpg",
     "Grace Hopper, Informatik (1906-1992)", "?", False),
    ("meitner_1953.jpg", "Lise Meitner (1878–1968) 1953 OeNB USIS 2955727.jpg",
     "Lise Meitner, Kernphysik (1878-1968)", "1953", False),
]


def abrufen(url):
    """Holt eine URL, wiederholt bei 429 oder 503 mit wachsender Pause."""
    wartezeit = 2.0
    for versuch in range(1, VERSUCHE + 1):
        try:
            anfrage = urllib.request.Request(url, headers=KOPFZEILE)
            with urllib.request.urlopen(anfrage, timeout=40) as antwort:
                return antwort.read()
        except urllib.error.HTTPError as fehler:
            if fehler.code not in (429, 503) or versuch == VERSUCHE:
                raise
            print(f"       (Server bremst mit HTTP {fehler.code}, "
                  f"warte {wartezeit:.0f}s und versuche es erneut)")
            time.sleep(wartezeit)
            wartezeit *= 2
    raise RuntimeError("nicht erreichbar")


def api(**parameter):
    parameter.setdefault("format", "json")
    parameter.setdefault("formatversion", "2")
    return json.loads(abrufen(API + "?" + urllib.parse.urlencode(parameter))
                      .decode("utf-8"))


def lizenz_ok(lizenz: str) -> bool:
    lizenz = (lizenz or "").lower()
    return any(erlaubt in lizenz for erlaubt in ERLAUBTE_LIZENZEN)


def urheber_saeubern(text: str) -> str:
    """
    Die Urheberangabe von Commons steckt oft in verschachteltem HTML. Nach dem
    Entfernen der Tags steht derselbe Name dann doppelt da
    ("Unknown authorUnknown author"). In einem Herkunftsnachweis sieht das
    schlampig aus, also wird die Verdopplung entfernt.
    """
    text = " ".join(text.split())
    haelfte = len(text) // 2
    if len(text) % 2 == 0 and text[:haelfte] == text[haelfte:]:
        return text[:haelfte]
    return text


def bild_holen(commons_titel):
    """
    Holt genau eine benannte Datei von Commons.
    Gibt (Bild, Lizenz, Urheber, Beschreibungsseite) zurueck - oder None.
    """
    daten = api(action="query", titles=f"File:{commons_titel}", prop="imageinfo",
                iiprop="url|extmetadata|size", iiurlwidth=THUMB_BREITE)
    seiten = daten.get("query", {}).get("pages", [])
    if not seiten or "imageinfo" not in seiten[0]:
        return None
    info = seiten[0]["imageinfo"][0]
    meta = info.get("extmetadata", {})
    url = info.get("thumburl") or info.get("url")
    if not url:
        return None
    bild = cv2.imdecode(np.frombuffer(abrufen(url), np.uint8), cv2.IMREAD_COLOR)
    return (bild,
            meta.get("LicenseShortName", {}).get("value", "?"),
            urheber_saeubern(
                html_weg(meta.get("Artist", {}).get("value", "unbekannt"))),
            info.get("descriptionurl", ""))


def genau_ein_gesicht(bild, detektor):
    """
    Dieselbe Pruefung wie in portraits_holen.py: brauchbar ist ein Bild nur,
    wenn genau ein Gesicht gross genug darauf ist. Bei Gruppenfotos wuesste
    niemand, wessen Gesicht gemessen wird.
    """
    if bild is None or min(bild.shape[:2]) < 200:
        return None
    gesichter = faceit.gesichter_finden(detektor, bild)
    if len(gesichter) != 1:
        return None
    _, _, breite, hoehe = gesichter[0][:4]
    if breite < 80 or hoehe < 80:
        return None
    return gesichter[0]


def person_aus_name(dateiname: str) -> str:
    """'einstein_1920.jpg' -> 'einstein'"""
    return dateiname.split("_")[0].replace(".jpg", "")


def paare(vektoren):
    """Teilt alle Paare in 'dieselbe Person' und 'verschiedene Personen'."""
    gleich, fremd = [], []
    for a, b in itertools.combinations(sorted(vektoren), 2):
        wert = faceit.aehnlichkeit(vektoren[a], vektoren[b])
        ziel = gleich if person_aus_name(a) == person_aus_name(b) else fremd
        ziel.append((wert, a, b))
    return gleich, fremd


def messen(ordner, erkenner, detektor):
    """Liest alle Bilder im Ordner und berechnet ihre 128 Zahlen."""
    vektoren = {}
    for pfad in sorted(ordner.glob("*.jpg")):
        bild = cv2.imread(str(pfad))
        gesicht = genau_ein_gesicht(bild, detektor)
        if gesicht is None:
            print(f"  [--] {pfad.name:20s} kein einzelnes Gesicht mehr zu finden")
            continue
        vektoren[pfad.name] = faceit.gesicht_zu_zahlen(erkenner, bild, gesicht)
    return vektoren


def bericht(vektoren):
    """Gibt die Messung aus und gibt (gleich, fremd) zurueck."""
    gleich, fremd = paare(vektoren)

    print(f"  Gemessen mit dem Modell des Workshops, Schwelle {faceit.SCHWELLE:.3f}:")
    print()
    if gleich:
        print("    Dieselbe Person, verschiedene Aufnahmen:")
        for wert, a, b in sorted(gleich, reverse=True):
            marke = "erkannt      " if wert >= faceit.SCHWELLE else "NICHT erkannt"
            print(f"      {wert:+.3f}  {marke}  {a} <-> {b}")
        print()
    if fremd:
        print("    Verschiedene Personen, die drei hoechsten Werte:")
        for wert, a, b in sorted(fremd, reverse=True)[:3]:
            marke = "UEBER Schwelle" if wert >= faceit.SCHWELLE else "unter Schwelle"
            print(f"      {wert:+.3f}  {marke}  {a} <-> {b}")
        print()

    if gleich and fremd:
        tief, hoch = min(gleich)[0], max(fremd)[0]
        if tief < hoch:
            print(f"    Die Bereiche ueberlappen: dieselbe Person bei {tief:.3f},")
            print(f"    zwei verschiedene bei {hoch:.3f}. Genau das ist die Aussage")
            print(f"    von Folie 7 - ohne eine einzige Aufnahme aus der Klasse.")
        else:
            print("    Hinweis: In diesem Satz trennen sich die Bereiche sauber.")
            print("    Fuer Folie 7 ist das der langweilige Fall - vermutlich hat")
            print("    Commons ein Bild durch einen besseren Scan ersetzt.")
        print()
        schnitt_gleich = sum(w for w, _, _ in gleich) / len(gleich)
        schnitt_fremd = sum(w for w, _, _ in fremd) / len(fremd)
        if schnitt_gleich <= schnitt_fremd:
            print("    WARNUNG: Aufnahmen derselben Person sind im Schnitt nicht")
            print("    aehnlicher als Aufnahmen verschiedener Personen. Vermutlich")
            print("    zeigt eine Datei eine andere Person als ihr Name sagt.")
            print("    Pruefe die Liste PERSONEN in diesem Skript.")
            print()
    return gleich, fremd


def credits_schreiben(ziel, gefunden, gleich, fremd):
    zeilen = [
        "# Bildnachweise - Vergleichsgesichter",
        "",
        "Portraits verstorbener Persoenlichkeiten aus Mathematik und Informatik,",
        "von Wikimedia Commons. Beamer-Demo fuer Station 4b.",
        "",
        "**Nicht als Ersatzgesicht gedacht.** Wer sich nicht fotografieren lassen",
        "moechte, arbeitet mit `data/beispiele/` - dieser Ordner hier ist",
        "Vergleichsmaterial fuer die Lehrkraft.",
        "",
        "Alle Bilder sind **Public Domain**, also ohne Namensnennungspflicht -",
        "deshalb duerfen sie projiziert und ausgedruckt werden. Es sind",
        "ausschliesslich verstorbene Personen: ein Gesichtsvektor ist biometrische",
        "Verarbeitung nach Art. 9 DSGVO, und eine Lizenz deckt nur das",
        "Urheberrecht, nicht Persoenlichkeitsrecht und Datenschutz.",
        "",
        "Mehrere Dateien mit gleichem Namensanfang zeigen **dieselbe Person** in",
        "verschiedenen Lebensaltern. Das ist Absicht.",
        "",
        "| Datei | Person | Jahr | Titel auf Commons | Urheber | Lizenz | Quelle |",
        "|---|---|---|---|---|---|---|",
    ]
    for e in gefunden:
        zeilen.append(
            f"| `{e['datei']}` | {e['person']} | {e['jahr']} "
            f"| {e['titel'].replace('|', '/')} | {e['urheber']} | {e['lizenz']} "
            f"| [Commons]({e['seite']}) |"
        )

    zeilen += [
        "",
        "## Gemessene Aehnlichkeiten",
        "",
        f"- Gemessen am **{date.today().isoformat()}**",
        f"- Vorschaubreite von Commons: **{THUMB_BREITE} px** "
        f"(andere Breite ergibt andere Werte!)",
        f"- OpenCV **{cv2.__version__}**, Schwellenwert **{faceit.SCHWELLE:.3f}**",
        "",
        "| Vergleich | Wert | Urteil des Programms | Richtig? |",
        "|---|---|---|---|",
    ]
    alle = [(w, a, b, True) for w, a, b in gleich] + \
           [(w, a, b, False) for w, a, b in fremd]
    for wert, a, b, ist_gleich in sorted(alle, reverse=True):
        urteil = "dieselbe Person" if wert >= faceit.SCHWELLE else "verschiedene Personen"
        richtig = "ja" if (wert >= faceit.SCHWELLE) == ist_gleich else "**nein**"
        zeilen.append(f"| {a} - {b} | {wert:+.3f} | {urteil} | {richtig} |")
    zeilen += [
        "",
        "Weichen diese Werte von der Tabelle in `docs/03_loesungen.md` ab, hat",
        "Commons ein Bild ersetzt. Neu messen:",
        "`uv run code/tools/personen_holen.py --messen`",
    ]
    (ziel / "CREDITS.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")


def main():
    nur_messen = "--messen" in sys.argv
    nur_klein = "--klein" in sys.argv
    liste = [e for e in PERSONEN if e[4]] if nur_klein else PERSONEN

    # Der Zielordner kommt ueber faceit, damit FACEIT_DATEN greift.
    # (Die Tests lesen bewusst direkt aus data/personen/.)
    ziel = faceit.daten_ordner("personen")
    detektor = faceit.detektor_laden()
    erkenner = faceit.erkenner_laden()

    if nur_messen:
        faceit.titel("Vergleichsgesichter neu messen",
                     f"Ordner: {ziel}")
        vektoren = messen(ziel, erkenner, detektor)
        if len(vektoren) < 2:
            faceit.abbruch(
                "In data/personen/ liegen weniger als zwei brauchbare Bilder.",
                "Erst laden:  uv run code/tools/personen_holen.py",
            )
        print()
        bericht(vektoren)
        return 0

    faceit.titel(
        "Vergleichsgesichter beschaffen (Vorbereitung)",
        "Mathematik und Informatik - mehrere Lebensalter pro Person.",
        f"{len(liste)} Bilder von Wikimedia Commons, alle Public Domain.",
    )

    gefunden, vektoren, fehlt = [], {}, []
    for nummer, (lokal, titel, person, jahr, _) in enumerate(liste):
        if nummer:
            time.sleep(PAUSE)      # hoeflich bleiben, sonst kommt HTTP 429

        # Ab hier wird NIE der Commons-Titel gedruckt: er kann Zeichen
        # enthalten, an denen eine cp1252-Konsole abbricht (Gedankenstrich).
        try:
            ergebnis = bild_holen(titel)
        except Exception as fehler:
            print(f"  [--] {lokal:20s} Abruf fehlgeschlagen: {type(fehler).__name__}")
            fehlt.append((lokal, "Abruf fehlgeschlagen"))
            continue
        if ergebnis is None:
            print(f"  [--] {lokal:20s} auf Commons nicht gefunden")
            fehlt.append((lokal, "auf Commons nicht gefunden - umbenannt?"))
            continue

        bild, lizenz, urheber, seite = ergebnis
        if not lizenz_ok(lizenz):
            print(f"  [--] {lokal:20s} nicht Public Domain: {lizenz}")
            fehlt.append((lokal, f"Lizenz {lizenz}"))
            continue

        gesicht = genau_ein_gesicht(bild, detektor)
        if gesicht is None:
            print(f"  [--] {lokal:20s} kein einzelnes, grosses Gesicht darauf")
            fehlt.append((lokal, "kein einzelnes Gesicht"))
            continue

        cv2.imwrite(str(ziel / lokal), bild)
        vektoren[lokal] = faceit.gesicht_zu_zahlen(erkenner, bild, gesicht)
        gefunden.append({"datei": lokal, "titel": titel, "person": person,
                         "jahr": jahr, "lizenz": lizenz, "urheber": urheber,
                         "seite": seite})
        print(f"  [ok] {lokal:20s} {lizenz:16s} {person}")

    if not gefunden:
        faceit.abbruch(
            "Es konnte kein Bild geladen werden.",
            "Pruefe die Internetverbindung und starte erneut.",
            "Die Commons-Titel stehen in der Liste PERSONEN in diesem Skript.",
        )

    gleich, fremd = paare(vektoren)
    credits_schreiben(ziel, gefunden, gleich, fremd)

    print()
    print(f"  {len(gefunden)} von {len(liste)} Bildern in {ziel}")
    print(f"  Bildnachweise und Messwerte in {ziel / 'CREDITS.md'}")
    print()
    bericht(vektoren)

    # Bei einer festen Liste ist jedes fehlende Bild ein fehlendes Testpaar -
    # das darf nicht still durchgehen.
    if fehlt:
        print(f"  ACHTUNG: {len(fehlt)} von {len(liste)} Bildern fehlen:")
        for lokal, grund in fehlt:
            print(f"    - {lokal:20s} {grund}")
        print()
        print("  Nochmal starten hilft oft: der haeufigste Grund ist, dass")
        print("  Wikimedia zu viele Anfragen in Folge abweist (HTTP 429).")
        print()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
