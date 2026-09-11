# Technik-Setup

Diese Seite ist für die Lehrkraft und für die Schul-IT. Die Schülerinnen und
Schüler brauchen sie nicht.

Es gibt genau zwei Python-Pakete und keinen Cloud-Dienst. Nach der einmaligen
Installation läuft der komplette Workshop **offline**.

---

## Der einfache Weg: `einrichten.bat`

**Doppelklick, fertig.** Das Skript macht alles, was in den Abschnitten 1 bis 3
von Hand beschrieben ist, und prüft danach automatisch, ob es geklappt hat:

```text
einrichten.bat
```

Es installiert `uv`, holt das Projekt, legt die Python-Umgebung an, prüft die
Modelle und die Windows-Kamerafreigabe und lässt am Ende die Testsuite laufen.
Zum Schluss steht ein Ampelbericht da:

| | Bedeutung | Exit-Code |
|---|---|---|
| **GRÜN** | Der Rechner ist bereit. | 0 |
| **GELB** | Der Workshop läuft, aber etwas fehlt (z. B. Teams belegt die Kamera). | 2 |
| **ROT** | So läuft es nicht. Die fehlenden Punkte stehen einzeln darunter. | 1 |

Zusätzlich schreibt es einen Bericht nach `%USERPROFILE%\face-it-bericht.txt` –
mit Rechnername und Zeitstempel, damit die IT die Berichte einsammeln und auf
einen Blick sehen kann, welcher Raum fertig ist.

**Es braucht keine Administratorrechte** (`uv` und Python landen im
Benutzerprofil) und **es ändert keine Windows-Einstellungen**. Die
Kamerafreigabe wird nur geprüft und gemeldet – setzen muss sie die IT.

Schalter:

```text
einrichten.bat /trocken   zeigt nur, was passieren würde - verändert nichts
einrichten.bat /neu       ignoriert den Stempel und prüft alles neu
einrichten.bat /still     schweigt bei Erfolg (für den Autostart)
```

Feinere Einstellungen gehen direkt über das PowerShell-Skript:

```powershell
.\einrichten.ps1 -Quelle https://github.com/<konto>/face-it -Stand v1.0 -Ziel C:\face-it
```

> **`-Quelle` muss auf das eigene Repository zeigen.** Der eingebaute
> Standardwert ist die Adresse von der Abschlussfolie und nicht geprüft. Vor dem
> ersten Einsatz einmal mit `/trocken` gegentesten.

### Für die Schul-IT: Autostart

Das Skript ist dafür gebaut, im Autostart zu liegen. Verknüpfung mit dem Ziel

```text
C:\Pfad\zu\face-it\einrichten.bat /still
```

nach `shell:startup` legen. Beim Login passiert dann:

- Ist alles in Ordnung und die letzte Prüfung jünger als 7 Tage, **beendet sich
  das Skript in unter einer Zehntelsekunde ohne jede Ausgabe.** Es hält
  niemanden auf.
- Sonst richtet es ein bzw. prüft nach und schreibt den Bericht.
- Steht das Netz morgens noch nicht, läuft es mit Zeitgrenze durch statt zu
  hängen.

Drei Dinge, die dabei wichtig sind:

1. **Kein automatisches `git pull` am Workshop-Tag.** Das Skript aktualisiert
   auf den mit `-Stand` angegebenen Stand. Gib dafür einen **Tag** an, keinen
   Zweig – sonst kann ein neuer Commit am Morgen alle Rechner gleichzeitig
   lahmlegen.
2. Die Stempeldatei `.einrichtung-geprueft.json` liegt im Projektordner. Löschen
   erzwingt eine vollständige Neuprüfung.
3. `-ExecutionPolicy Bypass` gilt nur für diesen einen Aufruf. Die Richtlinie des
   Rechners bleibt unverändert.

---

## Die Testsuite

Prüft, ob ein Rechner bereit ist – ohne Bildschirm und ohne Webcam:

```bash
uv run --extra tests pytest
```

| Datei | Was geprüft wird |
|---|---|
| `tests/test_1_umgebung.py` | Python 3.10–3.12, numpy, OpenCV **4.x**, `cv2.face` (also wirklich die contrib-Variante), Haar-Cascade |
| `tests/test_2_modelle.py` | `yunet.onnx` und `sface.onnx` sind vollständig **und laden**; `lbfmodel.yaml` optional |
| `tests/test_3_erkennung.py` | Die Fachlogik: Faltung (Fläche 0, Kante ≠ 0, Richtungsabhängigkeit), Gesicht finden, 128 Zahlen, Ähnlichkeit – auf den Beispielportraits |
| `tests/test_4_stationen.py` | **Jede Station startet** ohne Absturz, `04a` legt Vektoren an, `05_bias` rechnet, `99_cleanup` löscht wirklich |
| `tests/test_5_kamera.py` | Echte Webcam: liefert ein Bild, Größe, Farbe, nicht schwarz, Windows-Freigabe. Wird ohne Kamera **übersprungen**, nicht als Fehler gemeldet |
| `tests/test_6_personen.py` | Der Vergleichssatz in `data/personen/`: ein Gesicht je Bild, Relationen statt fester Messwerte, `04b_vergleich.py` im **Dateimodus**, und dass `99_cleanup.py` beide Bildordner verschont. Wird ohne den Ordner **übersprungen** – auf allen Rechnern außer dem Beamer planmäßig |

Die Tests laufen über drei Umgebungsvariablen, die schon in `faceit.py`
eingebaut sind: `FACEIT_TEST` unterdrückt die Fenster, `FACEIT_KAMERA` ersetzt
die Webcam durch ein Standbild, `FACEIT_TASTEN` speist Tastendrücke ein.

> **Wichtig:** `FACEIT_DATEN` lenkt den `data`-Ordner um, und die Tests nutzen
> das. Ohne diese Umlenkung würden sie die Aufnahmen einer Klasse löschen –
> `99_cleanup.py` fragt im Testmodus nicht nach. `tests/test_1_umgebung.py`
> bricht deshalb ab, wenn die Umlenkung fehlt.

Übersprungene Tests sind hier die eigentliche Information: die Begründung sagt,
was auf diesem Rechner fehlt.

---

## Von Hand, wenn das Skript nicht in Frage kommt

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

# Vergleichsgesichter für die Beamer-Demo in Station 4b
# – nur auf dem Beamer-Rechner nötig
uv run code/tools/personen_holen.py
```

Das erste Skript lädt acht freie Portraitfotos von Wikimedia Commons nach
`data/beispiele/` und schreibt Urheber und Lizenz in `data/beispiele/CREDITS.md`.
Diese Bilder liegen bewusst **nicht** im Repository, sondern werden lokal geholt.

### Die zwei Bildordner nicht verwechseln

| Ordner | Zweck | Lizenzlage |
|---|---|---|
| `data/beispiele/` | **Ersatzgesicht** für SuS, die sich nicht fotografieren lassen möchten. Acht verschiedene, demografisch gemischte Personen. So im Elternbrief zugesagt. | Gemischt: teils Public Domain, überwiegend **CC BY / CC BY-SA** → Namensnennungspflicht. Nur lokal am Rechner benutzen. |
| `data/personen/` | **Vergleichsmaterial** für die Beamer-Demo: mehrere Aufnahmen *derselben* Person aus verschiedenen Lebensaltern. Mathematik und Informatik, ausschließlich verstorbene Personen. | Ausschließlich **Public Domain** → keine Namensnennungspflicht, darf projiziert und ausgedruckt werden. |

Für Folien, Ausdrucke und Doku-Fotos deshalb **immer `data/personen/`** nehmen. Der
Grund für „nur verstorbene Personen": Ein Gesichtsvektor ist biometrische Verarbeitung
nach Art. 9 DSGVO, und eine Lizenz deckt nur das Urheberrecht, nicht
Persönlichkeitsrecht und Datenschutz. Ein Workshop, der Clearview AI für genau diese
Verarbeitung kritisiert, sollte sie nicht selbst an lebenden Personen vornehmen.

`personen_holen.py` endet mit **Exit-Code 1**, wenn ein Bild fehlt – bei einer festen
Liste ist jedes fehlende Bild ein fehlendes Vergleichspaar. Der häufigste Grund ist, dass
Wikimedia zu viele Anfragen in Folge mit `HTTP 429` abweist; dann hilft einfach ein
zweiter Aufruf. Neu messen, ohne erneut zu laden: `--messen`.

**`einrichten.bat` ruft die Bilddownloads absichtlich nicht auf.** Auf acht Rechnern
wären das rund 160 Commons-Abrufe. Beides sind Handschritte der Lehrkraft.

Danach die Handouts ausdrucken – alle liegen als HTML in `material/`:

| Datei | Anzahl |
|---|---|
| `material/handouts/handout_A_laufzettel.html` | einmal pro Zweiergruppe (2 Seiten) |
| `material/handouts/handout_B_faltung.html` | einmal pro Zweiergruppe (**2 Seiten**: Erklärung und Aufgabe) |
| `material/handouts/handout_B_faltung_loesung.html` | einmal für dich |
| `material/handouts/handout_C_bingo.html` | einmal pro Zweiergruppe |
| `material/handouts/handout_D_hack.html` | einmal pro Zweiergruppe |
| `material/handouts/handout_E_ampelkarte.html` | einmal pro Zweiergruppe, **in Farbe und beidseitig** |
| `material/handouts/handout_F_testmuster.html` | einmal pro Zweiergruppe (Station 2, wird vor die Kamera gehalten) |
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

Der Workshop läuft über **drei Termine** (siehe [01_agenda.md](01_agenda.md)).
Die große Checkliste gilt nur vor Termin 1; danach genügt die Kurzliste.

### Vor Termin 1 – am Vortag

- [ ] `einrichten.bat` auf **jedem** Rechner gelaufen und **grün** (oder gelb mit
      bekanntem Grund)
- [ ] Berichte eingesammelt: `%USERPROFILE%\face-it-bericht.txt`
- [ ] `uv run code/00_check.py` auf jedem Rechner: ein Mensch hat ein Kamerabild
      gesehen (das kann kein Test ersetzen)
- [ ] Beamer-Rechner: `uv run code/tools/landmark_modell_holen.py` für Station 3b
- [ ] Beamer-Rechner: `uv run code/tools/personen_holen.py` für die Vergleichs-Demo
      in Block 5 (muss mit **Exit-Code 0** enden, sonst fehlt ein Bildpaar)
- [ ] Handouts A und B gedruckt, Einwilligungen eingesammelt
- [ ] Ampelkarten gedruckt, gefaltet und auf die Plätze gelegt
- [ ] **Packpapier** für das Leitfragen-Plakat besorgt – keine Tafel, es muss
      drei Wochen überleben
- [ ] Gruppeneinteilung G1–G8 festgelegt, Sitzplan notiert

### Vor Termin 2 und 3 – Kurzliste, 10 Minuten

- [ ] `einrichten.bat` (läuft mit gültigem Stempel in unter einer Sekunde durch)
- [ ] Teams, Zoom und Kamera-App auf allen Rechnern geschlossen
- [ ] `data/`-Ordner leer (`uv run code/99_cleanup.py --ja`) – das sollte nach
      dem letzten Termin schon passiert sein
- [ ] **Plakat und Flipchartbögen** vom letzten Termin dabei
- [ ] Laufzettel und Ampelkarten wieder ausgegeben
- [ ] Hausaufgaben-Blätter der SuS da? Ohne sie startet der Wiedereinstieg nicht
- [ ] Nur vor Termin 2: Handout C (Bingo) und F (Testmuster) gedruckt
- [ ] Nur vor Termin 3: Handout D (Hack) gedruckt, ein ausgedrucktes Portrait als
      Reserve für den Foto-Angriff

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
