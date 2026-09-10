# Technik-Setup

Diese Seite ist für die Lehrkraft und für die Schul-IT. Die Schülerinnen und
Schüler brauchen sie nicht.

Es gibt genau zwei Python-Pakete und keinen Cloud-Dienst. Nach der einmaligen
Installation läuft der komplette Workshop **offline**.

---

## Kurzfassung

```bash
# einmal pro Rechner, mit Internetverbindung
uv sync

# Test
uv run code/00_check.py
```

Wer sich die Befehle nicht merken will: unter Windows `start.bat` doppelklicken.
Das erledigt `uv sync` und öffnet ein Menü mit allen Stationen. Die Kennung im
Menü ist dieselbe wie die Stationsnummer: `1`, `2`, `3`, `4a`, `4b`, `4c`, `5`.

Das Menü nutzt Farben und Symbole. Ob deine Konsole das kann, zeigt in zwei
Sekunden:

```bash
uv run code/start.py --farbtest
```

Erscheinen leere Kästchen statt Symbolen, hilft `set FACEIT_EMOJI=0`; erscheinen
Zeichenfolgen wie `[96m`, dann `set FACEIT_FARBEN=0`. Beides lässt sich auch
dauerhaft in `start.bat` setzen.

---

## 1. uv installieren

[uv](https://docs.astral.sh/uv/) ist ein einzelnes Programm, das Python und alle
Pakete verwaltet. Es braucht **keine Administratorrechte** und legt alles im
Benutzerprofil ab – der entscheidende Vorteil auf Schulrechnern.

**Windows** (PowerShell):

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**macOS und Linux**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Danach das Terminal einmal schließen und neu öffnen, dann prüfen:

```bash
uv --version
```

uv installiert bei Bedarf auch die passende Python-Version selbst. Es muss also
vorher **kein Python** auf dem Rechner sein.

## 2. Projekt auf den Rechner bringen

```bash
git clone https://github.com/fabianpingel/face-it.git
cd face-it
```

Ohne Git: das Repository als ZIP herunterladen und entpacken. Ein Kopieren des
entpackten Ordners per USB-Stick auf die anderen Rechner funktioniert ebenfalls –
der Ordner `.venv` sollte dabei aber **nicht** mitkopiert werden, den legt
`uv sync` auf jedem Rechner selbst an.

## 3. Umgebung anlegen

```bash
uv sync
```

Das dauert beim ersten Mal etwa eine Minute und lädt rund 90 MB. Ergebnis:

| Paket | Version | Wofür |
|---|---|---|
| `opencv-contrib-python` | 4.14 | Kamera, Bildverarbeitung, Gesichtserkennung, Landmarks |
| `numpy` | 2.x | Rechnen mit Zahlengittern |

> **Warum OpenCV 4 und nicht 5?**
> In OpenCV 5 sind die klassischen Haar-Cascades nicht mehr im Paket enthalten –
> Station 3 vergleicht aber genau dieses Verfahren von 2001 mit einem modernen
> neuronalen Netz. Deshalb ist die Version in `pyproject.toml` auf `>=4.10,<5`
> festgelegt. Bitte nicht „aktualisieren".
>
> **Warum die contrib-Variante?**
> Sie enthält alles von `opencv-python` und zusätzlich `cv2.face` für die
> optionale Station 3b. Beide Pakete gleichzeitig zu installieren wäre ein Fehler:
> Sie liefern dasselbe Modul `cv2`, und wer eines davon deinstalliert, reißt dem
> anderen die Dateien weg – danach ist gar kein `cv2` mehr da. Ein Paket für alle
> Rechner erspart diese Falle. Falls sie doch einmal zuschlägt, hilft
> `uv sync --reinstall-package opencv-contrib-python`.

## 4. Vorbereitung durch die Lehrkraft

Diese Schritte einmal vor dem Workshop ausführen, mit Internetverbindung:

```bash
# Ersatzportraits für alle, die nicht fotografiert werden möchten
uv run code/tools/portraits_holen.py

# Arbeitsblatt B (Faltung von Hand) samt Lösung erzeugen
uv run code/tools/handout_faltung.py
```

Das erste Skript lädt acht freie Portraitfotos von Wikimedia Commons nach
`data/beispiele/` und schreibt Urheber und Lizenz in `data/beispiele/CREDITS.md`.
Diese Bilder liegen bewusst **nicht** im Repository, sondern werden lokal geholt.

Danach die Handouts ausdrucken – alle liegen als HTML in `material/`:

| Datei | Anzahl |
|---|---|
| `material/handouts/handout_A_laufzettel.html` | einmal pro Zweiergruppe (2 Seiten) |
| `material/handouts/handout_B_faltung.html` | einmal pro Zweiergruppe |
| `material/handouts/handout_B_faltung_loesung.html` | einmal für dich |
| `material/handouts/handout_C_bingo.html` | einmal pro Zweiergruppe |
| `material/handouts/handout_D_hack.html` | einmal pro Zweiergruppe |
| `material/handouts/handout_E_ampelkarte.html` | einmal pro Zweiergruppe, **in Farbe und beidseitig** |
| `material/elternbrief_und_einwilligung.html` | einmal pro Schüler:in, **vorher** |

Zum Drucken die Datei im Browser öffnen und `Strg+P` drücken.

## 5. Optional: das Gesichtsnetz (Station 3b)

Station 3b legt 68 Punkte auf das Gesicht und verbindet sie zu einem
Dreiecksnetz – genau das Bild aus dem Workshop-Logo. Dafür fehlt nur noch ein
Modell (54 MB), das bewusst nicht im Repository liegt:

```bash
uv run code/tools/landmark_modell_holen.py
uv run code/03b_landmarks.py
```

Fehlt das Modell, läuft die Station trotzdem und zeigt die fünf Punkte von
YuNet. Sie bricht nicht ab. Für den Beamer-Rechner lohnt der Download, für die
Schüler-Rechner ist er nicht nötig.

> **Warum kein MediaPipe?**
> Naheliegend wäre MediaPipe mit seinen 468 Punkten. In der Praxis ist das eine
> Falle: Version 1.x hat die API `mp.solutions` entfernt, mit der man das Netz
> zeichnet, und die Wheels der 0.10er-Reihe sind unter Windows mit Python 3.12
> unvollständig. Obendrein zieht MediaPipe `opencv-contrib-python 5` mit und
> bringt damit eine abweichende OpenCV-Version auf den Rechner. Die Variante mit
> OpenCV allein ist stabil, braucht kein zusätzliches Paket – und das
> Delaunay-Netz entspricht dem Logo sogar genauer.

---

## Was die Schul-IT freigeben muss

**Netzwerk** – nur für die Installation, nicht während des Workshops:

| Adresse | Wofür |
|---|---|
| `astral.sh` | uv installieren |
| `pypi.org`, `files.pythonhosted.org` | die zwei Python-Pakete |
| `github.com` | Projekt herunterladen |
| `commons.wikimedia.org`, `upload.wikimedia.org` | Ersatzportraits (nur Vorbereitung) |
| `raw.githubusercontent.com` | Landmark-Modell für die optionale Station 3b |

**Kamera** – Windows blockiert den Zugriff sonst stillschweigend:

> Einstellungen → Datenschutz und Sicherheit → Kamera →
> „Apps den Zugriff auf die Kamera erlauben" aktivieren, ebenso
> „Desktop-Apps den Zugriff erlauben".

**Nicht nötig:** Administratorrechte, ein Google- oder Microsoft-Konto, eine
Internetverbindung während des Workshops, eine GPU.

---

## Checkliste

**Am Vortag**

- [ ] `uv sync` auf jedem Rechner gelaufen
- [ ] `uv run code/00_check.py` zeigt auf jedem Rechner ein Kamerabild
- [ ] `uv run code/04c_faceid.py` einmal komplett durchgespielt
- [ ] Handouts gedruckt, Einwilligungen eingesammelt
- [ ] Ampelkarten gedruckt, gefaltet und auf die Plätze gelegt
- [ ] Plakat für die Einstiegsfrage vorbereitet, Post-its besorgt
- [ ] Beamer-Rechner: `uv run code/tools/landmark_modell_holen.py` für Station 3b

**30 Minuten vorher**

- [ ] Teams, Zoom und Kamera-App auf allen Rechnern geschlossen
- [ ] `data/`-Ordner leer (`uv run code/99_cleanup.py --ja`)
- [ ] Ein zweiter Rechner mit fertig eingerichteter Face ID für die Hack-Challenge
- [ ] Ein ausgedrucktes Portrait als Reserve für den Foto-Angriff

---

## Fehlerbehebung

| Meldung oder Symptom | Ursache und Lösung |
|---|---|
| „Die Kamera lässt sich nicht öffnen" | Ein anderes Programm belegt sie. Teams, Zoom, Kamera-App und alle weiteren Face-it-Fenster schließen. |
| Kamerabild bleibt schwarz | Windows-Kameraberechtigung fehlt (siehe oben). Bei mehreren Kameras: `uv run code/00_check.py 1` |
| Tastendruck wirkt nicht | Das Bildfenster muss den Fokus haben. Mit der Maus hineinklicken, dann die Taste drücken. |
| „Die Modelldatei fehlt" | Der Befehl wurde im falschen Ordner gestartet. Er muss dort laufen, wo `pyproject.toml` liegt. |
| `uv: command not found` | Terminal nach der uv-Installation nicht neu geöffnet. |
| Fenster hängt, nichts reagiert | Im Terminal `Strg+C` drücken. Das beendet das Skript sauber. |
| Kein Gesicht wird erkannt | Zu dunkel oder zu weit weg. Licht von vorn, Gesicht formatfüllend. |
| Umlaute im Terminal falsch | Nur eine Anzeigefrage der Konsole, ohne Auswirkung auf die Ergebnisse. |

### Notfall-Modus ohne Kamera

Wenn an einem Rechner die Webcam ausfällt, kann jedes Skript stattdessen mit einem
gespeicherten Bild arbeiten:

```powershell
# Windows PowerShell
$env:FACEIT_KAMERA = "data/beispiele/portrait_01.jpg"
uv run code/03_detect.py
```

```bash
# macOS und Linux
FACEIT_KAMERA=data/beispiele/portrait_01.jpg uv run code/03_detect.py
```

Alle Stationen laufen dann durch, nur eben mit einem unbewegten Bild. Gut genug,
damit niemand zuschauen muss.

### Ohne uv, nur mit pip

Falls uv nicht installiert werden darf:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS und Linux
pip install -r requirements.txt
python code/00_check.py
```

---

## Die Modelle

Im Ordner `models/` liegen zwei vortrainierte Modelle aus dem
[OpenCV Model Zoo](https://github.com/opencv/opencv_zoo):

| Datei | Größe | Aufgabe |
|---|---|---|
| `yunet.onnx` | 0,2 MB | findet Gesichter im Bild und markiert fünf Punkte |
| `sface.onnx` | 38 MB | rechnet ein Gesicht in 128 Zahlen um |
| `lbfmodel.yaml` | 54 MB | 68 Landmarks für die optionale Station 3b – **nicht** im Repository, wird bei Bedarf geladen |

Beide liegen im Repository, damit während des Workshops nichts geladen werden
muss. Neu holen kann man sie mit:

```bash
uv run code/tools/modelle_holen.py
```
