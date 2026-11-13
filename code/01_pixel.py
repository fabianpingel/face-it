"""
Station 1 - Ein Bild ist eine Tabelle.

Halte dein Gesicht in den Rahmen. Rechts siehst du live, was der Computer
daraus macht: ein Gitter aus Zahlen.

Jede Zahl sagt nur eines: wie hell ist dieser Punkt?
    0   = schwarz
    255 = weiss

Mehr weiss ein Computer ueber dein Gesicht an dieser Stelle nicht.

Tasten:
    Schieberegler oben   Gitter groesser oder kleiner
    z                    Zahlen anzeigen oder ausblenden
    Leertaste            Bild einfrieren, Zahlen ins Terminal schreiben
                         und das Arbeitsblatt zum Ausmalen erzeugen.
                         Noch einmal druecken: Livebild laeuft weiter.
    q                    beenden

Starten:
    uv run code/01_pixel.py
"""

import cv2
import numpy as np

import faceit

FENSTER = "Face it - Station 1"
REGLER = "Stufe"

# Der Schieberegler waehlt eine dieser Stufen aus. Feste Werte, damit die
# Klasse ueber dieselben Zahlen redet - und damit die interessanten
# Groessen sicher getroffen werden.
#   4 bis 8     man erkennt gerade noch, DASS da ein Gesicht ist
#   12 bis 20   man erkennt langsam, WER es ist
#   32 und 64   fast wie ein Foto
STUFEN = [4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64]
STANDARDSTUFE = STUFEN.index(16)

# So gross ist das Gitter auf dem Arbeitsblatt zum Ausmalen.
# Bei mehr als 16 x 16 dauert das Ausmalen zu lange.
BLATT_GROESSE = 16

# Aufbau des Fensters: zwei Bilder gleicher Hoehe nebeneinander,
# darunter eine Leiste mit den Hinweisen.
PANEL_HOEHE = 430
LEISTE_HOEHE = 120


# ======================================================================
#  ADVANCED - hier darfst du im Code herumprobieren
#
#  Nimm das Zeichen # vor einer Zeile weg und schau, was passiert.
#  Die Aenderung wirkt sofort im laufenden Bild.
# ======================================================================

def experimente(gitter):
    """Wird auf jedes Zahlengitter angewendet, bevor es angezeigt wird."""

    # Alles umdrehen: aus hell wird dunkel (Negativ)
    # gitter = 255 - gitter

    # Nur noch vier Helligkeitsstufen zulassen (Posterisierung)
    # gitter = gitter // 64 * 64

    # Alles heller machen. np.clip verhindert Werte ueber 255.
    # gitter = np.clip(gitter.astype(int) + 60, 0, 255).astype("uint8")

    # Nur die Haelfte des Bildes bearbeiten
    # gitter[:, gitter.shape[1] // 2:] = 255 - gitter[:, gitter.shape[1] // 2:]

    # Alles unter 100 auf schwarz, alles darueber auf weiss (Schwellenwert)
    # gitter = np.where(gitter < 100, 0, 255).astype("uint8")

    return gitter

# ======================================================================


def zielrahmen(bild):
    """
    Berechnet das Quadrat in der Bildmitte, in das das Gesicht gehoert.
    Nur dieser Bereich wird zu Zahlen umgerechnet - deshalb muss das
    Gesicht den Rahmen gut ausfuellen.
    """
    hoehe, breite = bild.shape[:2]
    kante = int(hoehe * 0.66)
    return (breite - kante) // 2, (hoehe - kante) // 2, kante


def gitter_berechnen(bild, groesse):
    """Aus dem Kamerabild wird ein Gitter aus groesse x groesse Zahlen."""
    grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
    x, y, kante = zielrahmen(bild)
    ausschnitt = grau[y:y + kante, x:x + kante]
    gitter = cv2.resize(ausschnitt, (groesse, groesse),
                        interpolation=cv2.INTER_AREA)
    return experimente(gitter), ausschnitt


def zahlenbild(gitter, seitenlaenge=620):
    """
    Malt das Zahlengitter als Bild: jedes Feld bekommt seine eigene
    Helligkeit als Hintergrund und die Zahl steht darin.
    So sieht man, dass die Zahlen das Bild SIND.
    """
    zellen = gitter.shape[0]

    if zellen > 20:
        tafel = np.full((260, 620, 3), 25, np.uint8)
        faceit.schrift(tafel, "Zu viele Zahlen zum Lesen.", (24, 90),
                       faceit.AKZENT, 0.85, 2)
        faceit.schrift(tafel, f"{zellen} x {zellen} = {zellen * zellen} Felder.",
                       (24, 135), faceit.WEISS, 0.7, 2)
        faceit.schrift(tafel, "Stell den Schieberegler auf 20 oder weniger.",
                       (24, 180), faceit.GRAU, 0.6, 1)
        return tafel

    zelle = seitenlaenge // zellen
    tafel = np.zeros((zelle * zellen, zelle * zellen, 3), np.uint8)
    schriftgroesse = zelle / 74

    for z in range(zellen):
        for s in range(zellen):
            wert = int(gitter[z, s])
            x, y = s * zelle, z * zelle
            cv2.rectangle(tafel, (x, y), (x + zelle, y + zelle),
                          (wert, wert, wert), -1)
            # Zahl in der Gegenfarbe, damit sie immer lesbar bleibt
            tinte = (0, 0, 0) if wert > 127 else (255, 255, 255)
            text = str(wert)
            breite_text = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX,
                                          schriftgroesse, 1)[0][0]
            cv2.putText(tafel, text,
                        (x + (zelle - breite_text) // 2, y + zelle // 2 + 6),
                        cv2.FONT_HERSHEY_SIMPLEX, schriftgroesse, tinte, 1,
                        cv2.LINE_AA)
    return tafel


def gitter_ausgeben(gitter):
    """Schreibt das Zahlengitter ins Terminal."""
    print()
    print("  " + faceit.bunt("Dein Gesicht als Zahlen:", "blau", "fett"))
    print()
    for zeile in gitter:
        print("   " + " ".join(f"{int(wert):3d}" for wert in zeile))
    print()
    print(f"  Das sind {gitter.size} Zahlen. "
          f"Das ist dein Gesicht fuer den Computer.")
    print()


def blatt_erzeugen(gitter, pfad):
    """
    Schreibt das Arbeitsblatt zum Ausmalen als HTML-Datei.
    Zum Drucken im Browser oeffnen und Strg+P druecken.

    Die beiden Schwellen werden aus dem eigenen Bild berechnet, damit das
    Ergebnis auch bei dunklen oder hellen Fotos gut aussieht.
    """
    dunkel = int(np.percentile(gitter, 33))
    hell = int(np.percentile(gitter, 66))
    zellen = gitter.shape[0]

    reihen = []
    for z in range(zellen):
        felder = "".join(f"<td>{int(wert)}</td>" for wert in gitter[z])
        reihen.append(f"<tr>{felder}</tr>")

    pfad.write_text(f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>Face it! &ndash; Malen nach Zahlen</title>
<link rel="stylesheet" href="{(faceit.MATERIAL / 'brand' / 'tokens.css').as_uri()}">
<style>
  h1, h2, h3 {{ font-family: var(--font-display); }}
  @page {{ size: A4 portrait; margin: 14mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: var(--font-sans);
         color: #1a2340; margin: 0; font-size: 11pt; line-height: 1.45; }}
  h1 {{ font-size: 20pt; margin: 0; color: #182145; }}
  h1 span {{ color: #2b5fe8; }}
  .unter {{ font-size: 12pt; color: #2b5fe8; margin: 2mm 0 0 0;
            font-weight: 600; }}
  .linie {{ height: 3px; background: #2b5fe8; margin: 3mm 0 6mm 0; }}
  .anleitung {{ display: flex; gap: 6mm; margin-bottom: 6mm; }}
  .stufe {{ flex: 1; border: 1px solid #dbe2f0; padding: 2.5mm 3mm; }}
  .stufe .probe {{ height: 9mm; margin-bottom: 2mm; border: 1px solid #b7c2dc; }}
  .stufe b {{ display: block; font-size: 10.5pt; }}
  .stufe span {{ color: #56658a; font-size: 9.5pt; }}
  table {{ border-collapse: collapse; margin: 0 auto; }}
  td {{ border: 1px solid #b7c2dc; width: 10.5mm; height: 10.5mm;
        text-align: center; vertical-align: middle; font-size: 10pt;
        color: #8a949e; font-variant-numeric: tabular-nums; }}
  .frage {{ margin-top: 7mm; color: #182145; font-weight: 600;
            font-size: 12pt; text-align: center; }}
  .fuss {{ margin-top: 6mm; font-size: 9pt; color: #56658a;
           text-align: center; }}
</style>
</head>
<body>

<h1>Face it! <span>&ndash;</span> Malen nach Zahlen</h1>
<p class="unter">Dein Gesicht in {zellen} &times; {zellen} Zahlen</p>
<div class="linie"></div>

<div class="anleitung">
  <div class="stufe">
    <div class="probe" style="background:#33393f"></div>
    <b>unter {dunkel}</b>
    <span>ganz ausmalen</span>
  </div>
  <div class="stufe">
    <div class="probe" style="background:repeating-linear-gradient(
         45deg,#8a949e 0,#8a949e 1px,#fff 1px,#fff 4px)"></div>
    <b>{dunkel} bis {hell}</b>
    <span>schraffieren</span>
  </div>
  <div class="stufe">
    <div class="probe" style="background:#fff"></div>
    <b>&uuml;ber {hell}</b>
    <span>frei lassen</span>
  </div>
</div>

<table>
{chr(10).join(reihen)}
</table>

<p class="frage">Was siehst du, wenn du fertig bist?</p>

<p class="fuss">{zellen} &times; {zellen} = {zellen * zellen} Zahlen zwischen
0 (schwarz) und 255 (wei&szlig;). Mehr wei&szlig; der Computer nicht.</p>

</body>
</html>
""", encoding="utf-8")
    return pfad


faceit.titel(
    "Station 1 - Ein Bild ist eine Tabelle",
    "[Schieberegler] Gitter groesser oder kleiner",
    "[Leertaste] einfrieren und Arbeitsblatt erzeugen",
    "[z] Zahlen einblenden     [q] beenden",
)
print("  Moegliche Gitter: " + " ".join(str(w) for w in STUFEN))
print()

kamera = faceit.kamera_oeffnen()
fotos = faceit.daten_ordner("fotos")
zaehler = 0
zahlen_an = False
eingefroren = False
bild = None

faceit.fenster(FENSTER)
faceit.regler_anlegen(FENSTER, REGLER, STANDARDSTUFE, len(STUFEN) - 1)

while True:
    # Beim Einfrieren wird kein neues Bild geholt - das alte bleibt stehen.
    if not eingefroren or bild is None:
        bild = faceit.bild_holen(kamera)

    # Der Schieberegler waehlt eine der festen Stufen aus.
    stufe = min(max(0, faceit.regler_wert(FENSTER, REGLER)), len(STUFEN) - 1)
    groesse = STUFEN[stufe]
    gitter, ausschnitt = gitter_berechnen(bild, groesse)

    # ---------------------------------------------------------- links
    # Alles ausserhalb des Zielrahmens wird abgedunkelt - so ist sofort
    # klar, welcher Teil des Bildes gezaehlt wird.
    x, y, kante = zielrahmen(bild)
    links = (bild * 0.35).astype("uint8")
    links[y:y + kante, x:x + kante] = bild[y:y + kante, x:x + kante]
    cv2.rectangle(links, (x, y), (x + kante, y + kante), faceit.AKZENT, 2)

    # Auf feste Hoehe bringen, das Seitenverhaeltnis bleibt erhalten.
    faktor = PANEL_HOEHE / links.shape[0]
    links = cv2.resize(links, (int(links.shape[1] * faktor), PANEL_HOEHE))
    faceit.schrift(links, "Gesicht in den hellen Bereich", (14, 32),
                   faceit.AKZENT, 0.6, 2)
    if eingefroren:
        faceit.schrift(links, "EINGEFROREN", (14, PANEL_HOEHE - 20),
                       faceit.GELB, 0.8, 2)

    # ---------------------------------------------------------- rechts
    rechts = cv2.cvtColor(
        cv2.resize(gitter, (PANEL_HOEHE, PANEL_HOEHE),
                   interpolation=cv2.INTER_NEAREST),
        cv2.COLOR_GRAY2BGR)

    oben = np.hstack([links, rechts])

    # ---------------------------------------------------------- Leiste unten
    breite = oben.shape[1]
    leiste = np.full((LEISTE_HOEHE, breite, 3), 26, np.uint8)
    cv2.line(leiste, (0, 0), (breite, 0), faceit.AKZENT, 2)

    faceit.schrift(leiste, f"{groesse} x {groesse} = {groesse * groesse} Zahlen",
                   (18, 44), faceit.AKZENT, 0.95, 2)
    faceit.schrift(leiste, f"Stufe {stufe + 1} von {len(STUFEN)}",
                   (18, 76), faceit.GRAU, 0.55, 1)

    hinweise = [
        "[Schieberegler]  Gitter groesser oder kleiner",
        "[Leertaste]  " + ("weiter mit dem Livebild" if eingefroren
                           else "einfrieren und Arbeitsblatt erzeugen"),
        "[z]  Zahlen " + ("ausblenden" if zahlen_an else "einblenden")
        + "        [q]  beenden",
    ]
    # Die Hinweise beginnen rechts neben der laengsten Zahlenzeile (64 x 64),
    # sonst ueberlappen sich die beiden Texte bei grossen Stufen.
    groesste = STUFEN[-1]
    spalte = 18 + 40 + cv2.getTextSize(
        f"{groesste} x {groesste} = {groesste * groesste} Zahlen",
        cv2.FONT_HERSHEY_SIMPLEX, 0.95, 2)[0][0]
    for i, zeile in enumerate(hinweise):
        faceit.schrift(leiste, zeile, (spalte, 34 + i * 30),
                       faceit.WEISS, 0.55, 1)

    ansicht = np.vstack([oben, leiste])
    faceit.zeigen(FENSTER, ansicht)
    faceit.fenster_anpassen(FENSTER, ansicht)

    if zahlen_an:
        faceit.zeigen("Face it - die Zahlen", zahlenbild(gitter))

    # ---------------------------------------------------------- Tasten
    gedrueckt = faceit.taste()
    if not faceit.fenster_offen(FENSTER):
        break

    if gedrueckt == "z":
        zahlen_an = not zahlen_an
        if not zahlen_an and not faceit.TESTMODUS:
            cv2.destroyWindow("Face it - die Zahlen")
        print(f"  Zahlenfenster: {'an' if zahlen_an else 'aus'}")

    elif gedrueckt == " ":
        if eingefroren:
            eingefroren = False
            print("  Livebild laeuft wieder.")
            print()
        else:
            eingefroren = True
            zaehler += 1
            gitter_ausgeben(gitter)

            # Das Arbeitsblatt bleibt immer bei 16 x 16 - sonst wird das
            # Ausmalen zu einer Strafarbeit.
            blatt_gitter = experimente(
                cv2.resize(ausschnitt, (BLATT_GROESSE, BLATT_GROESSE),
                           interpolation=cv2.INTER_AREA))
            blatt = blatt_erzeugen(
                blatt_gitter, fotos / f"malen_nach_zahlen_{zaehler:02d}.html")
            cv2.imwrite(str(fotos / f"station1_{zaehler:02d}.png"), ansicht)

            print("  " + faceit.bunt("Arbeitsblatt zum Ausdrucken:",
                                      "blau", "fett"))
            print(f"    {blatt}")
            print("    Im Browser oeffnen und Strg+P druecken.")
            print()
            print("  Das Bild ist jetzt eingefroren. Leertaste startet es wieder.")
            print()

    elif gedrueckt == "q":
        break

kamera.release()
faceit.fenster_schliessen()
print("  Weiter mit Station 2: uv run code/02_filter.py")
print()
