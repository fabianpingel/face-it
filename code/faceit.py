"""
Face it! - Gemeinsame Hilfsfunktionen fuer alle Workshop-Skripte.

Diese Datei musst du nicht lesen und nicht aendern.
Sie sorgt nur dafuer, dass die Kamera startet, die Modelle gefunden werden
und Fehlermeldungen auf Deutsch und verstaendlich sind.
"""

import sys
import os
from pathlib import Path
from typing import NoReturn

import cv2
import numpy as np

# Umlaute im Terminal auch unter Windows korrekt ausgeben
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- Terminal-Farben

def _windows_terminal_vorbereiten() -> bool:
    """
    Bringt die Windows-Konsole dazu, Farbcodes und UTF-8 zu verstehen.
    Gibt True zurueck, wenn beides geklappt hat.
    """
    if os.name != "nt":
        return True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32

        # UTF-8 als Ausgabe-Codepage, sonst werden Umlaute zu Kauderwelsch
        kernel32.SetConsoleOutputCP(65001)

        # Farbcodes einschalten (ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        handle = kernel32.GetStdHandle(-11)
        modus = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(modus)):
            return False
        return bool(kernel32.SetConsoleMode(handle, modus.value | 0x0004))
    except Exception:
        return False


def _farben_erlaubt() -> bool:
    """
    Farben nur, wenn die Ausgabe wirklich in einem Terminal landet.
    Mit FACEIT_FARBEN=1 oder 0 laesst sich das erzwingen.
    """
    erzwungen = os.environ.get("FACEIT_FARBEN")
    if erzwungen is not None:
        return erzwungen not in ("0", "nein", "no", "false")
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    return _windows_terminal_vorbereiten()


FARBIG = _farben_erlaubt()

# Emojis nur da, wo Farben funktionieren. Dass eine Konsole Farbcodes
# versteht, ist ein gutes Zeichen dafuer, dass sie auch Symbole zeichnet.
# Sehr alte Konsolen malen stattdessen leere Kaestchen - dafuer gibt es
# FACEIT_EMOJI=0 und den Selbsttest:  uv run code/start.py --farbtest
EMOJI = FARBIG
if os.environ.get("FACEIT_EMOJI") is not None:
    EMOJI = os.environ["FACEIT_EMOJI"] not in ("0", "nein", "no", "false")

_CODES = {
    "cyan": "96", "blau": "94", "gruen": "92", "rot": "91",
    "gelb": "93", "grau": "90", "fett": "1", "weiss": "97",
}


def bunt(text, *stile) -> str:
    """
    Faerbt Text fuer das Terminal, z. B. bunt('Hallo', 'cyan', 'fett').
    Wenn das Terminal keine Farben kann, kommt der Text unveraendert zurueck.
    """
    text = str(text)
    if not FARBIG or not stile:
        return text
    codes = ";".join(_CODES[stil] for stil in stile if stil in _CODES)
    return f"\033[{codes}m{text}\033[0m" if codes else text


def sym(emoji: str, ersatz: str) -> str:
    """Gibt das Emoji zurueck - oder ein schlichtes Zeichen, wenn es nicht geht."""
    return emoji if EMOJI else ersatz

# ---------------------------------------------------------------- Pfade

PROJEKT = Path(__file__).resolve().parent.parent
MODELLE = PROJEKT / "models"
MATERIAL = PROJEKT / "material"

# Normalerweise liegen alle Aufnahmen in data/ im Projektordner.
# FACEIT_DATEN kann das umlenken - die automatischen Tests benutzen das, damit
# sie niemals die echten Aufnahmen einer Klasse anfassen (99_cleanup.py loescht
# im Testmodus ohne Rueckfrage).
DATEN = Path(os.environ.get("FACEIT_DATEN") or PROJEKT / "data")

YUNET = MODELLE / "yunet.onnx"
SFACE = MODELLE / "sface.onnx"


def daten_ordner(unterordner: str = "") -> Path:
    """Gibt den data-Ordner zurueck und legt ihn an, falls er fehlt."""
    ziel = DATEN / unterordner if unterordner else DATEN
    ziel.mkdir(parents=True, exist_ok=True)
    return ziel


# ---------------------------------------------------------------- Farben (BGR, aus dem Workshop-Logo)

NAVY = (63, 38, 18)
CYAN = (230, 200, 30)
WEISS = (255, 255, 255)
GRUEN = (80, 220, 100)
ROT = (60, 60, 240)
GELB = (60, 200, 240)
GRAU = (150, 150, 150)


# ---------------------------------------------------------------- Text im Bild

_UMLAUTE = {
    "ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
    "ß": "ss", "–": "-", "—": "-", "„": '"', "“": '"', "”": '"', "…": "...",
    "·": "-", "°": "Grad",
}


def _ascii(text: str) -> str:
    """OpenCV kann keine Umlaute zeichnen - deshalb ersetzen wir sie."""
    for zeichen, ersatz in _UMLAUTE.items():
        text = text.replace(zeichen, ersatz)
    return text.encode("ascii", "replace").decode("ascii")


def schrift(bild, text, position, farbe=WEISS, groesse=0.7, dicke=2):
    """Schreibt Text mit dunklem Rand ins Bild - dadurch immer lesbar."""
    text = _ascii(str(text))
    cv2.putText(bild, text, position, cv2.FONT_HERSHEY_SIMPLEX,
                groesse, (0, 0, 0), dicke + 3, cv2.LINE_AA)
    cv2.putText(bild, text, position, cv2.FONT_HERSHEY_SIMPLEX,
                groesse, farbe, dicke, cv2.LINE_AA)
    return bild


def hinweisleiste(bild, zeilen):
    """Zeichnet unten im Bild eine Leiste mit Tastenhinweisen."""
    hoehe, breite = bild.shape[:2]
    leiste = hoehe - 12 - 26 * len(zeilen)
    overlay = bild.copy()
    cv2.rectangle(overlay, (0, leiste - 14), (breite, hoehe), NAVY, -1)
    cv2.addWeighted(overlay, 0.75, bild, 0.25, 0, bild)
    for i, zeile in enumerate(zeilen):
        schrift(bild, zeile, (14, leiste + 12 + 26 * i), CYAN, 0.55, 1)
    return bild


def hinweisleiste_unten(bild, zeilen, hoehe=None):
    """
    Haengt die Hinweise UNTER das Bild statt darueber.

    Bei kleinen Kacheln verdeckt eine Leiste im Bild sonst genau das,
    was man sehen will - zum Beispiel das Kinn der aufgenommenen Person.
    Gibt ein neues, hoeheres Bild zurueck.
    """
    breite = bild.shape[1]
    if hoehe is None:
        hoehe = 22 + 30 * len(zeilen)
    leiste = np.full((hoehe, breite, 3), 26, np.uint8)
    cv2.line(leiste, (0, 0), (breite, 0), CYAN, 2)
    for i, zeile in enumerate(zeilen):
        schrift(leiste, zeile, (16, 32 + i * 30), CYAN, 0.55, 1)
    return np.vstack([bild, leiste])


def balken(bild, wert, position, breite=320, hoehe=28, farbe=CYAN):
    """Zeichnet einen Fortschrittsbalken fuer einen Wert zwischen 0 und 1."""
    x, y = position
    wert = max(0.0, min(1.0, float(wert)))
    cv2.rectangle(bild, (x, y), (x + breite, y + hoehe), GRAU, 1)
    cv2.rectangle(bild, (x + 1, y + 1),
                  (x + int(breite * wert) - 1, y + hoehe - 1), farbe, -1)
    return bild


# ---------------------------------------------------------------- Kamera

# Damit alle Stationen gleich aussehen, arbeiten wir mit einer festen
# Bildbreite. 4K-Webcams wuerden sonst alles ausbremsen.
BILDBREITE = 1280
BILDHOEHE = 720



class _ErsatzKamera:
    """
    Notfall-Modus ohne Webcam: liefert immer dasselbe Bild aus einer Datei.
    Wird aktiv, wenn die Umgebungsvariable FACEIT_KAMERA auf ein Bild zeigt.
    Praktisch, wenn an einem Rechner die Kamera defekt oder belegt ist.
    """

    def __init__(self, pfad):
        self._bild = cv2.imread(str(pfad))
        if self._bild is None:
            abbruch(f"Das Ersatzbild laesst sich nicht laden: {pfad}")
        print(f"  [Notfall-Modus] Statt der Kamera wird benutzt: {pfad}")

    def isOpened(self):
        return True

    def read(self):
        return True, self._bild.copy()

    def set(self, *_):
        return False

    def release(self):
        return None


def kamera_oeffnen(index: int = 0):
    """
    Oeffnet die Webcam und beendet das Programm mit einer klaren Meldung,
    falls das nicht klappt.
    """
    ersatz = os.environ.get("FACEIT_KAMERA")
    if ersatz:
        return _ErsatzKamera(ersatz)

    backends = [cv2.CAP_DSHOW, cv2.CAP_ANY] if os.name == "nt" else [cv2.CAP_ANY]
    for backend in backends:
        kamera = cv2.VideoCapture(index, backend)
        if kamera.isOpened():
            # Wunschauflösung. Nicht jede Kamera macht mit - deshalb lesen
            # wir hinterher nach, was wir wirklich bekommen haben.
            kamera.set(cv2.CAP_PROP_FRAME_WIDTH, BILDBREITE)
            kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, BILDHOEHE)
            breite = int(kamera.get(cv2.CAP_PROP_FRAME_WIDTH))
            hoehe = int(kamera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"  Kamera liefert {breite} x {hoehe} Pixel.")
            return kamera
        kamera.release()

    abbruch(
        "Die Kamera laesst sich nicht oeffnen.",
        "1) Ist noch ein anderes Programm offen, das die Kamera benutzt?",
        "   (Teams, Zoom, Kamera-App, ein zweites Face-it-Fenster)",
        "2) Hat Windows den Zugriff erlaubt?",
        "   Einstellungen > Datenschutz > Kamera > Zugriff fuer Apps erlauben",
        "3) Hast du mehrere Kameras? Starte mit einer anderen Nummer:",
        "   uv run code/00_check.py 1",
        "",
        "Notfall-Modus ohne Kamera (arbeitet mit einem gespeicherten Bild):",
        "   Windows:  set FACEIT_KAMERA=data/beispiele/portrait_01.jpg",
        "   danach das Skript normal starten.",
    )


# ---------------------------------------------------------------- Fenster und Tasten

# Testmodus: statt Fenster zu oeffnen werden Bilder nach data/_test/ gespeichert.
# Damit lassen sich alle Skripte ohne Bildschirm pruefen (z. B. automatisiert).
TESTMODUS = bool(os.environ.get("FACEIT_TEST"))
_testschritt = {"nummer": 0}
_reglerwerte = {}


def fenster(name: str):
    """Legt ein Fenster an (nur noetig, wenn es einen Schieberegler bekommt)."""
    if not TESTMODUS:
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)


# Fenster, deren Groesse schon angepasst wurde
_angepasst = set()


def fenster_anpassen(name: str, bild, hoechstbreite: int = 1500):
    """
    Zieht das Fenster genau auf das Seitenverhaeltnis des Bildes.
    Ohne das wuerde OpenCV das Bild in ein vorgegebenes Fenster quetschen -
    und alles waere in der Breite gestaucht.
    Wirkt nur beim ersten Aufruf, damit die Lehrkraft danach frei ziehen kann.
    """
    if TESTMODUS or name in _angepasst:
        return
    hoehe, breite = bild.shape[:2]
    faktor = min(1.0, hoechstbreite / breite)
    cv2.resizeWindow(name, int(breite * faktor), int(hoehe * faktor))
    _angepasst.add(name)


def zeigen(fenstername: str, bild):
    """Zeigt ein Bild in einem Fenster an."""
    if TESTMODUS:
        sicher = "".join(z if z.isalnum() else "_" for z in fenstername)
        cv2.imwrite(str(daten_ordner("_test") / f"{sicher}.png"), bild)
        return
    cv2.imshow(fenstername, bild)


def taste(wartezeit: int = 1) -> str:
    """
    Wartet kurz und gibt die gedrueckte Taste als Buchstaben zurueck.
    Wenn nichts gedrueckt wurde, kommt ein leerer Text "" zurueck.
    """
    if TESTMODUS:
        folge = os.environ.get("FACEIT_TASTEN", "")
        i = _testschritt["nummer"]
        _testschritt["nummer"] += 1
        return folge[i] if i < len(folge) else "q"
    code = cv2.waitKey(wartezeit) & 0xFF
    if code == 255:
        return ""
    if code == 27:
        return "esc"
    if code == 32:
        return " "
    return chr(code) if 32 < code < 127 else ""


def fenster_schliessen():
    if not TESTMODUS:
        cv2.destroyAllWindows()


def regler_anlegen(fenstername: str, name: str, startwert: int, hoechstwert: int):
    """
    Legt einen Schieberegler oben im Fenster an.

    Klappt das nicht - etwa weil das Fenster fehlt -, laeuft die Station
    trotzdem weiter und benutzt den Startwert. Ein fehlender Regler ist
    aergerlich, ein Absturz mitten im Workshop ist schlimmer.
    """
    _reglerwerte[(fenstername, name)] = startwert
    if TESTMODUS:
        return
    try:
        cv2.createTrackbar(_ascii(name), fenstername, startwert, hoechstwert,
                           lambda wert: None)
    except cv2.error:
        print(f"  Hinweis: Der Schieberegler '{name}' konnte nicht angelegt "
              f"werden.")
        print(f"  Die Station laeuft weiter mit dem festen Wert {startwert}.")


def regler_wert(fenstername: str, name: str) -> int:
    """
    Liest den aktuellen Wert eines Schiebereglers.

    Wenn das Fenster inzwischen ueber das Kreuz geschlossen wurde, gibt es
    keinen Regler mehr - dann liefern wir den letzten bekannten Wert
    zurueck, statt das Programm mit einem Fehler abzubrechen.
    """
    if TESTMODUS:
        return int(os.environ.get("FACEIT_REGLER",
                                  _reglerwerte.get((fenstername, name), 0)))
    try:
        wert = cv2.getTrackbarPos(_ascii(name), fenstername)
    except cv2.error:
        return _reglerwerte.get((fenstername, name), 0)
    _reglerwerte[(fenstername, name)] = wert
    return wert


def fenster_offen(fenstername: str) -> bool:
    """
    Ist das Fenster noch da? Gibt False zurueck, sobald es ueber das Kreuz
    geschlossen wurde. Damit koennen die Stationen sauber beenden, statt
    mit einer Fehlermeldung abzustuerzen.
    """
    if TESTMODUS:
        return True
    try:
        return cv2.getWindowProperty(fenstername, cv2.WND_PROP_VISIBLE) >= 1
    except cv2.error:
        return False


def bild_holen(kamera, spiegeln: bool = True):
    """
    Holt ein Bild von der Kamera. Spiegelt es, damit es wie ein Spiegel wirkt,
    und begrenzt die Breite - sonst wird es bei grossen Kameras langsam.
    """
    ok, bild = kamera.read()
    if not ok:
        abbruch("Die Kamera liefert kein Bild mehr.",
                "Schliesse das Fenster und starte das Programm neu.")
    if bild.shape[1] > BILDBREITE:
        faktor = BILDBREITE / bild.shape[1]
        bild = cv2.resize(bild, None, fx=faktor, fy=faktor,
                          interpolation=cv2.INTER_AREA)
    return cv2.flip(bild, 1) if spiegeln else bild


# ---------------------------------------------------------------- Modelle

def detektor_laden(breite: int = 640, hoehe: int = 480,
                   schwelle: float = 0.85):
    """
    Laedt YuNet - ein modernes Modell, das Gesichter im Bild findet
    und dabei fuenf Punkte markiert (Augen, Nase, Mundwinkel).
    """
    if not YUNET.exists():
        abbruch(f"Die Modelldatei fehlt: {YUNET}",
                "Lade sie nach docs/02_technik_setup.md herunter.")
    return cv2.FaceDetectorYN.create(
        str(YUNET), "", (breite, hoehe),
        score_threshold=schwelle, nms_threshold=0.3, top_k=50,
    )


def erkenner_laden():
    """
    Laedt SFace - das Modell, das aus einem Gesicht 128 Zahlen macht.
    Diese 128 Zahlen nennt man einen "Embedding-Vektor".
    """
    if not SFACE.exists():
        abbruch(f"Die Modelldatei fehlt: {SFACE}",
                "Lade sie nach docs/02_technik_setup.md herunter.")
    return cv2.FaceRecognizerSF.create(str(SFACE), "")


def gesichter_finden(detektor, bild):
    """
    Gibt eine Liste der gefundenen Gesichter zurueck.
    Jedes Gesicht ist eine Zeile mit: x, y, breite, hoehe, 5 Punkte, Sicherheit.
    """
    hoehe, breite = bild.shape[:2]
    detektor.setInputSize((breite, hoehe))
    _, gesichter = detektor.detect(bild)
    return [] if gesichter is None else list(gesichter)


def gesicht_zu_zahlen(erkenner, bild, gesicht):
    """
    Macht aus einem gefundenen Gesicht die 128 Zahlen.
    Vorher wird das Gesicht automatisch gerade gedreht und zugeschnitten.
    """
    ausgerichtet = erkenner.alignCrop(bild, gesicht)
    return erkenner.feature(ausgerichtet).flatten()


def aehnlichkeit(a, b) -> float:
    """
    Vergleicht zwei Gesichts-Vektoren.
    Ergebnis: 1.0 = identisch, 0.0 = voellig verschieden.
    (Das ist die Kosinus-Aehnlichkeit - der Winkel zwischen zwei Pfeilen.)
    """
    a = np.asarray(a, dtype=np.float32).flatten()
    b = np.asarray(b, dtype=np.float32).flatten()
    laenge = np.linalg.norm(a) * np.linalg.norm(b)
    return 0.0 if laenge == 0 else float(np.dot(a, b) / laenge)


# Ab diesem Wert gilt bei SFace: "Das ist dieselbe Person."
# Der Wert ist eine Entscheidung von Menschen, kein Naturgesetz.
SCHWELLE = 0.363


def gesichtsrahmen(bild, gesicht, farbe=CYAN, punkte=True, beschriftung=None):
    """Zeichnet Rahmen und die fuenf Punkte um ein gefundenes Gesicht."""
    x, y, b, h = [int(v) for v in gesicht[:4]]
    cv2.rectangle(bild, (x, y), (x + b, y + h), farbe, 2)
    if punkte:
        for i in range(5):
            px, py = int(gesicht[4 + i * 2]), int(gesicht[5 + i * 2])
            cv2.circle(bild, (px, py), 3, farbe, -1)
    if beschriftung:
        schrift(bild, beschriftung, (x, max(24, y - 10)), farbe, 0.65, 2)
    return bild


# ---------------------------------------------------------------- Fehler und Start

def abbruch(*zeilen) -> NoReturn:
    """Bricht das Programm mit einer verstaendlichen Meldung ab."""
    strich = bunt("=" * 64, "rot")
    print()
    print(strich)
    print("  " + sym("🛑", "!!") + "  "
          + bunt("Da ist etwas schiefgelaufen", "rot", "fett"))
    print(strich)
    for zeile in zeilen:
        print("  " + str(zeile))
    print(strich)
    print()
    sys.exit(1)


def titel(stationsname: str, *zeilen):
    """Gibt eine Kopfzeile im Terminal aus."""
    strichzeichen = "─" if EMOJI else "-"
    print()
    print("  " + bunt("Face it!", "cyan", "fett")
          + "  |  " + bunt(stationsname, "weiss", "fett"))
    print("  " + bunt(strichzeichen * (len(stationsname) + 13), "cyan"))
    for zeile in zeilen:
        print("  " + bunt(str(zeile), "grau"))
    print()
