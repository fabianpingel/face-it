# Face it! – Ablaufplan für die Lehrkraft

Gesamtdauer **210 Minuten** (3,5 h) inkl. 15 min Pause.
Beispielzeiten für einen Start um 8:00 Uhr. Sozialform: Partnerarbeit, 2 SuS pro Rechner.

Legende: 🧑‍🏫 Input · 🔬 Experiment · 💻 Code · ✍️ Papier · 💬 Diskussion

---

## Block 0 · Ankommen und Aufhänger — 15 min (8:00–8:15)

| Zeit | Was | Details |
|---|---|---|
| 3 min | 🔬 **Der Selbstversuch** | "Nehmt alle euer Handy und entsperrt es mit dem Gesicht. Nochmal. Jetzt mit halb zugehaltenem Gesicht." Kein Vorlauf, keine Begrüßungsfolie. |
| 5 min | 💬 **Die Tafelfrage** | *Was genau hat dein Handy gerade gemessen?* Alle Vermutungen unkommentiert an die Tafel bzw. aufs Plakat. Nichts richtigstellen – das Plakat bleibt bis zum Schluss hängen. |
| 2 min | 🧑‍🏫 **Ansage** | Folie 1 (Logo): "Wir bauen das heute nach. In drei Stunden entsperrt sich dein Rechner mit deinem Gesicht. Und danach hackst du das System deines Nachbarn." |
| 5 min | 💻 **Startcheck** | `uv run code/00_check.py` → Webcam-Fenster mit Live-Bild, Bildgröße und der Anzahl der Zahlenwerte. Jede Gruppe, die ihr Bild sieht, ist einsatzbereit. Wer Fehler hat: Fehlerkarte am Platz. |

> **Warum so:** Der erste Erfolg fällt in die erste Viertelstunde. Nullvorkenntnisse
> verzeihen keinen 20-minütigen Einstiegsvortrag.

---

## Block 1 · Station 1: Ein Bild ist eine Tabelle — 35 min (8:15–8:50)

**Aha-Ziel:** Der Computer sieht nur Zahlen, keine Gesichter.

| Zeit | Was | Details |
|---|---|---|
| 7 min | 💻 `01_pixel.py` | Leertaste = Foto. Im Live-Bild liegt ein cyanfarbener Zielrahmen – das Gesicht muss ihn ausfüllen, denn nur dieser Ausschnitt wird umgerechnet. Das Skript verkleinert ihn auf 16×16 Graustufen und druckt die **Zahlen** ins Terminal. Erste Reaktion abwarten: "Das soll ich sein?" |
| 8 min | ✍️ **Malen nach Zahlen** | Jede Gruppe bekommt ihr Zahlengitter als Ausdruck (wird von `01_pixel.py` automatisch als druckfertige Datei erzeugt). Dunkle Werte ausmalen, helle frei lassen. Die Gruppe erkennt sich selbst – nur aus Zahlen. Ergebnisse an die Tafel. |
| 8 min | 💻 **Auflösungs-Regler** | Wert `GROESSE = 16` ganz oben im Code auf 8, 32, 64 und 200 ändern. Frage auf dem Laufzettel: *Ab wie vielen Pixeln erkennt man, WER es ist? Ab wie vielen, DASS es ein Gesicht ist?* Die Antworten liegen typisch bei rund 30 bzw. 10 Pixeln – erstaunlich niedrig. |
| 7 min | 💻 **Eine Zeile aktivieren** | `# img = 255 - img` einkommentieren → Negativ. Danach `img = img // 64 * 64` → Posterisierung. Erkenntnis: Rechnen mit Zahlen ist Bildbearbeitung. Das ist jeder Instagram-Filter. |
| 5 min | 🧑‍🏫 **Begriffe nachliefern** | Folie 2: Pixel, Graustufe 0–255, Auflösung, Farbkanäle R/G/B. Erst jetzt, und nur vier Minuten. |

**Bonus für Schnelle:** Nur einen Farbkanal anzeigen. Bild spiegeln. Ein zweites Gesicht dazuschalten und beide Zahlengitter voneinander abziehen.

---

## Block 2 · Station 2: Filter und Faltung — 30 min (8:50–9:20)

**Aha-Ziel:** Ich war gerade selbst ein neuronales Netz.

| Zeit | Was | Details |
|---|---|---|
| 12 min | ✍️ **Faltung unplugged** | Arbeitsblatt B (`material/handouts/handout_B_faltung.html`): ein 6×6-Zahlengitter, darüber der Sobel-Kernel `[[-1,0,1],[-2,0,2],[-1,0,1]]`. Das Bild ist links dunkel und rechts hell, die Werte gehen nur von 0 bis 9 – so ist es im Kopf rechenbar. **Jede Gruppe rechnet nur zwei Zellen** – multiplizieren, aufaddieren, eintragen. Jede Gruppe bekommt ein Feld in der gleichmäßigen Fläche und eines auf der Kante. An der Tafel zusammengesetzt: in den Flächen steht **0**, auf der Kante **28**. Der Kernel reagiert nicht auf Helligkeit, sondern nur auf Veränderung. Satz der Stunde: *Ihr wart gerade gemeinsam ein Convolutional Layer.* |
| 10 min | 💻 `02_filter.py` | Derselbe Kernel, jetzt live auf der Webcam. Der Kernel steht als 3×3-Liste ganz oben im Code und ist editierbar. Tastenpresets: `1` Original, `2` Weichzeichnen, `3` Schärfen, `4` Kanten, `5` Sobel senkrecht. |
| 5 min | 🔬 **Kernel-Challenge** | Aufgabe: Finde durch Ausprobieren einen Kernel, der **nur senkrechte** Kanten hervorhebt. Wer zuerst ein sinnvolles Ergebnis hat, zeigt es am Beamer. |
| 3 min | 🧑‍🏫 **Die Brücke** | Folie 3: "Ein neuronales Netz macht genau das – aber es *lernt* seine Kernel selbst, tausende davon, in Schichten übereinander. Ihr habt einen von Hand gebaut, ein Netz hat Millionen." |

**Bonus:** Kernelsumme ungleich 1 → Bild wird heller oder dunkler. Warum? Und was macht ein 5×5-Weichzeichner gegenüber einem 3×3?

---

## 🕐 Pause — 15 min (9:20–9:35)

---

## Block 3 · Station 3: Finde das Gesicht — 30 min (9:35–10:05)

**Aha-Ziel:** Erkennung ist Statistik, nicht Wahrheit. Und: *Detektion* ist nicht *Erkennung*.

| Zeit | Was | Details |
|---|---|---|
| 5 min | 💻 `03_detect.py` | Live-Webcam mit Rechteck ums Gesicht, Zähler "1 Gesicht gefunden". Mit `y` zwischen Haar-Cascade (2001) und YuNet (2023) umschalten. |
| 12 min | 🔬 **Experimente-Bingo** | Arbeitsblatt C (`handout_C_bingo.html`), 12 Felder – jede Gruppe versucht, möglichst viele abzuhaken. Ziel ist, das System **hereinzulegen**: Kopf 90 Grad drehen · Hand vor den Mund · Sonnenbrille · Licht aus · **Foto auf dem Handy-Display vor die Kamera halten** · Gesicht auf einem T-Shirt · gezeichnetes Gesicht · Poster an der Wand · Steckdose oder Autofront (Pareidolie) · zwei Gesichter dicht nebeneinander · Kapuze · Maske. |
| 6 min | 💻 **Parameter drehen** | `scaleFactor` und `minNeighbors` verändern, bis das Programm überall Gesichter sieht – an der Wand, auf dem Tisch, im Pullover. Danach so streng einstellen, dass es niemanden mehr findet. Aha: *Die Empfindlichkeit ist eine Einstellung, kein Naturgesetz.* |
| 4 min | 💬 **Die entscheidende Frage** | "Das Programm hat mein Gesicht gefunden. Weiß es, dass ich es bin?" – Nein. Die Trennung Detektion/Erkennung an der Tafel festhalten. Und notieren: Das Handy-Foto wurde akzeptiert. Das kommt im Abschlussblock wieder. |
| optional | 💻 `03b_landmarks.py` | 68 Gesichtspunkte, zu einem Dreiecksnetz verbunden – genau das Bild aus dem Workshop-Logo, live auf dem eigenen Gesicht. Mit `n` zwischen Netz und reinen Punkten umschalten. Reiner Wow-Effekt, nur wenn Zeit ist. Braucht einmalige Vorbereitung, siehe Technik-Setup. |

---

## Block 4 · Station 4: Wer ist das? — 40 min (10:05–10:45) 🔑 **Kernstation**

**Aha-Ziel:** Mein Gesicht ist eine Liste aus 128 Zahlen. Sicherheit ist ein Schwellenwert.

| Zeit | Was | Details |
|---|---|---|
| 6 min | 💻 `04_embedding.py` | Foto von sich → das Skript druckt **128 Kommazahlen**. Nichts weiter. Bewusst nüchtern: "Das bist du. Für den Computer. Mehr weiß er nicht über dein Gesicht." Zweites Foto derselben Person → die Zahlen sind *ähnlich*, aber nicht gleich. |
| 12 min | 💻 `05_vergleich.py` | Zwei Fotos hinein, Ähnlichkeit in Prozent plus Balken heraus. Testreihe auf dem Laufzettel: ich–ich (gleiches Licht) · ich–ich (Brille ab/auf, Haare anders, Grimasse) · ich–Nachbar:in · Nachbar:in–Nachbar:in · ich–Portrait aus `data/beispiele/`. **Klassentabelle an der Tafel:** Welches Paar erreicht die höchste Fremd-Ähnlichkeit? Geschwister und Cousins gewinnen zuverlässig. |
| 4 min | 🧑‍🏫 **Vektor-Bild** | Folie 4: Zwei Zahlen sind ein Punkt auf Papier, drei ein Punkt im Raum, 128 ein Punkt in einem Raum, den man nicht zeichnen kann. Ähnliche Gesichter liegen dort nah beieinander. *Das* ist Gesichtserkennung – ein Abstand. |
| 14 min | 💻 `06_faceid.py` — **das Finale** | Die eigene Handy-Entsperrung: einmal ein Foto aufnehmen (also "Face-ID einrichten"), dann live grün **ENTSPERRT** oder rot **GESPERRT**, mit Schieberegler für den Schwellenwert.<br>Choreografie: (1) Standardwert 0,36 – funktioniert. (2) Nachbar:in setzt sich davor – bleibt rot. (3) Regler auf 0,05 → **jeder** entsperrt. (4) Regler auf 0,90 → **niemand**, nicht einmal man selbst. |
| 4 min | 💬 **Begriffe zuletzt** | Jetzt und keine Minute früher: *False Accept* (ein Fremder kommt hinein) und *False Reject* (ich komme nicht hinein). Frage: "Wo würdest DU den Regler setzen – beim Handy? Bei einer Banktür? Bei einer Polizeifahndung?" Die Antwort ist bei jedem Anwendungsfall anders, und sie ist immer ein Kompromiss. |

**Bonus:** Anwesenheitsliste für die Tischgruppe (`07_bonus_anwesenheit.py`): mehrere Gesichter registrieren, Namen live ins Bild schreiben.

---

## Block 5 · Face it! Angriff und Verantwortung — 30 min (10:45–11:15)

**Aha-Ziel:** Was ich baue, kann ich brechen – und es bricht nicht bei allen Menschen gleich oft.

| Zeit | Was | Details |
|---|---|---|
| 12 min | 🔬 **Hack-Challenge** | Auftrag: *Entsperre den Rechner der Nachbargruppe.* Punkte pro erfolgreicher Methode (Arbeitsblatt D, `handout_D_hack.html`): Foto vom Handy-Display (3 P.) · Ausdruck (3 P.) · Video des Gesichts (4 P.) · Geschwisterkind oder ähnlich aussehende Person (5 P.) · Schwellenwert heimlich verstellen (2 P.) · gespeicherte Referenzdatei austauschen (5 P.). Rangliste an die Tafel. |
| 5 min | 💬 **Auswertung** | Welche Angriffe klappten? Warum funktioniert das Handy-Foto? Weil die Kamera ein flaches Bild sieht und Haut nicht von Papier unterscheiden kann. Deshalb hat echtes Face-ID eine **Infrarot-Tiefenkamera**, projiziert Tausende Punkte auf das Gesicht und prüft *Liveness*. Die Nachbargruppe hat gerade bewiesen, warum das nötig ist. |
| 7 min | 🔬 **Fehler messen, Bias einordnen** | `uv run code/08_bias.py` – braucht keine Kamera, rechnet mit den Gesichtern, die die Klasse in Station 4 aufgenommen hat.<br>**Teil 1, eigene Daten:** Das Skript vergleicht alle Aufnahmen paarweise und zeigt zwei Verteilungen – gleiche Person gegen verschiedene Personen. Die beiden Bereiche **überlappen sich**, und eine Tabelle zeigt für jede Schwelle, wie viele Falschabweisungen und Falschakzeptanzen entstehen. Damit ist belegt: Es gibt keine fehlerfreie Schwelle.<br>**Teil 2, veröffentlichte Zahlen:** **Gender Shades** (Buolamwini und Gebru, MIT 2018), Fehlerrate bei der Geschlechtsbestimmung 0,8 Prozent bei hellhäutigen Männern gegen 34,7 Prozent bei dunkelhäutigen Frauen. **NIST FRVT Part 3** (2019, 189 Algorithmen): 10- bis 100-mal höhere Falschtrefferraten für west- und ostafrikanische sowie ostasiatische Gesichter. Grund: die Trainingsdaten.<br>*Bewusst getrennt:* gemessen wird mit Klassendaten, die demografischen Unterschiede kommen aus Studien – mit zwölf Portraits lässt sich Bias nicht seriös selbst messen, und genau das ist auch eine Lehre. |
| 6 min | 💬 **Vier Ecken** | Vier Aussagen, vier Raumecken, die SuS stellen sich hin und begründen in einem Satz – **mit einem technischen Argument von heute Vormittag**.<br>① "Gesichtserkennung an Bahnhöfen macht uns sicherer." ② "Unsere Schule darf die Anwesenheit per Gesicht erfassen." ③ "Ich darf Fotos von Freunden hochladen, ohne zu fragen." ④ "Mein Gesicht ist ein sichereres Passwort als eine PIN."<br>Faktenrahmen in 90 Sekunden: DSGVO Art. 9 (Biometrie ist eine besonders geschützte Datenkategorie), EU AI Act (biometrische Echtzeit-Fernidentifizierung im öffentlichen Raum grundsätzlich verboten), Fall **Clearview AI** (Milliarden Gesichter aus dem Netz gescrapt, Millionenbußgelder in mehreren EU-Staaten). Und der Merksatz: Ein Passwort kann man ändern. Sein Gesicht nicht. |

---

## Abschluss — 15 min (11:15–11:30)

| Zeit | Was | Details |
|---|---|---|
| 6 min | 💬 **Zurück zum Plakat** | Das Tafelbild von 8:05 wird durchgegangen. Was war richtig, was war Mythos? Die SuS korrigieren selbst. Die Antwort auf die Leitfrage steht jetzt in ihren eigenen Worten da. |
| 4 min | ✍️ **Ein Satz, den ich behalte** | Jede:r schreibt einen Satz auf ein Post-it und klebt es auf das Logo-Poster. Bleibt als Foto für die Doku – nur Post-its, keine Gesichter. |
| 3 min | 💻 **Gemeinsames Löschen** | Alle führen gleichzeitig `python code/99_cleanup.py` aus. Alle Gesichtsdaten des Vormittags werden gelöscht, das Skript zählt mit: "17 Bilder und 4 Gesichtsvektoren entfernt." Schlusssatz: "Genau das macht kaum ein Unternehmen freiwillig." |
| 2 min | 🧑‍🏫 **Take-home** | Folie 5 mit QR-Code auf das Repository: alle Skripte, Lösungen, vier Bonusprojekte und das Glossar zum Weiterbasteln zu Hause. |

---

## Zeitpuffer und Notfallplan

Falls es klemmt, in dieser Reihenfolge kürzen:

1. `03b_landmarks.py` (ist ohnehin optional) — spart 5 min
2. Kernel-Challenge in Block 2 auf eine Demo am Beamer verkürzen — spart 5 min
3. Bias-Messung von Gruppenarbeit auf eine Beamer-Demo umstellen — spart 5 min
4. Bonus-Aufgaben streichen — sie sind nur für Schnelle gedacht

**Nicht kürzen:** Block 4 und die Hack-Challenge. Das sind die Momente, an die sich die
Schüler:innen in einem Jahr noch erinnern.
