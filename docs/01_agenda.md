# Face it! – Ablaufplan für die Lehrkraft

Gesamtdauer **270 Minuten** in **drei Doppelstunden à 90 Minuten**, an drei getrennten
Terminen, unterteilt in **sechs Blöcke**. Keine Uhrzeiten – jeder Termin steht für sich
und endet mit einem Cliffhanger. Sozialform: Partnerarbeit in **8 festen Gruppen**, bei
20 SuS also 2 bis 3 pro Rechner. Ein dritter im Team ist kein Problem, sondern ein
drittes Gesicht zum Vergleichen.

Legende: 🧑‍🏫 Input · 🔬 Experiment · 💻 Code · ✍️ Papier · 💬 Diskussion

## Die sechs Blöcke auf einen Blick

| Termin | Block | Titel | min | Fazit-Folie |
|---|---|---|---|---|
| **1** | **1** | Ein Bild ist eine Tabelle | 58 | Folie 2 · *Tabelle aus Zahlen* |
| **1** | **2** | Ein Filter ist eine Rechnung | 32 | Folie 3 · *Fläche 0, Kante 28* |
| **2** | **3** | Vom Handkernel zum neuronalen Netz | 33 | Folie 4 · *Kernel von Hand* |
| **2** | **4** | Finde das Gesicht | 57 | Folie 5 · *Gefunden ist nicht erkannt*<br>+ Folie 6 als Ausblick |
| **3** | **5** | Wer ist das? Sicherheit ist ein Schwellenwert | 36 | Folie 7 · *False Accept / False Reject* |
| **3** | **6** | Face it! Angriff und Verantwortung | 54 | Folie 8 · *Was du bauen kannst, kannst du überlisten* |

Dazu Folie 1 (Titel mit Drei-Termin-Fahrplan) und Folie 9 (Take-home) – **neun Folien**
in `material/folien/index.html`. Jeder Block endet mit seinem Fazit, und jedes Fazit
kommt **nach** dem Experiment, nie davor.

> **Die Stationsnummern bleiben unverändert.** „Station 1" bis „Station 5" stehen im
> Startmenü (`code/start.py`), in jedem Skript, auf allen Handouts und auf den Folien.
> Blöcke und Termine sind die Zeitebene darüber – eine Station darf über zwei Blöcke
> laufen.

**Was gegenüber dem alten Projektvormittag anders ist:** Die Diskussions- und
Einordnungsphasen wachsen von rund 33 auf rund 71 Minuten – das ist der Teil, in dem
die SuS abstrahieren und einordnen. Die angeleiteten Doing-Phasen sind dafür um etwa
20 Minuten gestrafft. Neu hinzu: eine ausführliche gemeinsame Einrichtung, ein echter
Wiedereinstieg pro Termin, 27 Minuten Zeitpuffer und **Hausaufgaben, die tragen**.

---

# Termin 1 — 90 min

**Aha-Ziel:** Der Computer sieht nur Zahlen, keine Gesichter. Und Rechnen mit diesen
Zahlen ist Bildbearbeitung.

## Block 1 · Ein Bild ist eine Tabelle — 58 min

| Zeit | Was | Details |
|---|---|---|
| 3 min | 🔬 **Der Selbstversuch** | "Nehmt alle euer Handy und entsperrt es mit dem Gesicht. Nochmal. Jetzt mit halb zugehaltenem Gesicht." Kein Vorlauf, keine Begrüßungsfolie. |
| 5 min | 💬 **Die Leitfrage** | *Was genau hat dein Handy gerade gemessen?* Alle Vermutungen unkommentiert aufs **Plakat** – auf Packpapier, **nicht an die Tafel**: es muss drei Wochen überleben. Nichts richtigstellen. Das Plakat wird eingerollt, mitgenommen und an jedem Termin neu aufgehängt. |
| 2 min | 🧑‍🏫 **Ansage mit Fahrplan** | **Folie 1** (Logo): "Wir bauen das in drei Doppelstunden nach. Am dritten Termin entsperrt sich dein Rechner mit deinem Gesicht. Und danach hackst du das System deines Nachbarn." Die Folie zeigt den Drei-Termin-Fahrplan – die SuS sollen wissen, wo sie stehen. |
| 18 min | 💻 **Gemeinsame Einrichtung** | Jetzt ausführlich, nicht als 5-Minuten-Startcheck.<br>**6 min** am Beamer vorgemacht: `start.bat` bzw. `uv run code/start.py`, was ein Skript ist, wo die Bilder landen (`data/`), warum nichts ins Netz geht.<br>**7 min** alle machen mit: `uv run code/00_check.py` → Webcam-Fenster mit Live-Bild, Bildgröße und Anzahl der Zahlenwerte. Wer sein Bild sieht, stellt die **Ampelkarte auf grün**.<br>**5 min** Organisation für alle drei Termine: **feste Gruppennummern G1–G8 und fester Rechner** (wer den Rechner wechselt, verliert seine Daten), Ampelkarte, Laufzettel, Zwei-Minuten-Regel (erst lesen, dann Nachbargruppe, dann rot). |
| 8 min | 💻 `01_pixel.py` | Links das Kamerabild, rechts live dasselbe als Zahlengitter. Alles außerhalb des cyanfarbenen Zielrahmens ist abgedunkelt – nur was im Rahmen liegt, wird umgerechnet. Mit `z` erscheint ein zweites Fenster, in dem **jedes Feld seine eigene Helligkeit als Hintergrund hat und die Zahl darin steht**: Man sieht das Gesicht im Zahlengitter. Erste Reaktion abwarten: "Das soll ich sein?" |
| 6 min | ✍️ **Malen nach Zahlen** | Leertaste **friert das Bild ein** und erzeugt das Arbeitsblatt als HTML in `data/fotos/` – fest bei 16×16, mit drei aus dem eigenen Bild berechneten Malstufen. **Drucken sofort anstoßen und im Hintergrund laufen lassen** – acht Browser-Druckdialoge hintereinander kosten sonst allein sechs Minuten. Ausgemalt wird zu Hause (HA 1b). Noch einmal Leertaste, und das Livebild läuft weiter. |
| 6 min | 💻 **Auflösungs-Regler** | Läuft **parallel zum Drucken**. Den Schieberegler durch alle elf Stufen ziehen – 4, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64. Das Pixelbild wächst live mit. Frage auf dem Laufzettel: *Ab wie vielen Pixeln erkennt man, DASS es ein Gesicht ist? Ab wie vielen, WER es ist?* Die Antworten liegen typisch bei rund 8 bis 12 bzw. 30 Pixeln – erstaunlich niedrig. |
| 6 min | 💻 **Eine Zeile aktivieren** | `# gitter = 255 - gitter` einkommentieren → Negativ. Danach `gitter = gitter // 64 * 64` → Posterisierung. Erkenntnis: Rechnen mit Zahlen ist Bildbearbeitung. Das ist jeder Instagram- oder Snapchat-Filter. |
| 4 min | 🧑‍🏫 **Fazit Block 1** | **Folie 2**: Pixel, Graustufe 0–255, Auflösung, Farbkanäle R/G/B – daneben das Zahlengitter eines Gesichts. Kernsatz: *Dein Gesicht. Mehr sieht der Computer nicht.* Erst jetzt, und nur vier Minuten. |

**Advanced für Schnelle:** Im Abschnitt `ADVANCED` oben in `01_pixel.py` das `#` vor einer
Zeile entfernen – Negativ, Posterisierung, Schwellenwert, halbseitige Bearbeitung. Die
Wirkung ist sofort im laufenden Bild zu sehen.

## Block 2 · Ein Filter ist eine Rechnung — 32 min

| Zeit | Was | Details |
|---|---|---|
| 6 min | 💬 **Einordnung 1** | *"Jede einzelne dieser 65 536 Zahlen kann man ändern – und ihr habt es gerade mit einer Zeile getan. Was ist ein Foto dann als Beweis noch wert?"* Sammeln, nicht auflösen. Das ist der Vorgriff auf die Hack-Challenge in Block 6 und auf Deepfakes. Zwei bis drei Sätze aufs Plakat. |
| 12 min | ✍️ **Faltung unplugged** | Arbeitsblatt B (`handout_B_faltung.html`), zwei Seiten.<br>**5 min** Seite 1 gemeinsam am Beamer: zwei vollständig ausgerechnete Beispiele mit farbigen Zahlen – einmal auf einer Kante (Ergebnis 8), einmal auf einer gleichmäßigen Fläche (Ergebnis 0).<br>**5 min** Seite 2: **jede der 8 Gruppen rechnet ihre zwei Felder** – eines in der Fläche, eines auf der Kante – **unter Aufsicht**. Das muss hier sitzen, sonst kommt die Hausaufgabe falsch zurück und Termin 2 startet mit einem löchrigen Gitter. Die Gruppentabelle auf dem Blatt ist genau auf acht Gruppen ausgelegt, es bleibt kein Feld übrig.<br>**2 min 🧑‍🏫 Fazit Block 2:** an der Tafel zusammensetzen, dazu **Folie 3**: in den Flächen steht **0**, auf der Kante **28**. Der Kernel reagiert nicht auf Helligkeit, sondern nur auf Veränderung – weil seine Zahlen sich zu null addieren. Satz der Stunde: *Ihr wart gerade gemeinsam ein Convolutional Layer.* Abfotografieren. |
| 2 min | ✍️ **Hausaufgabe** | HA 1a und 1b ansagen, siehe unten. Laufzettel einsammeln. |
| 3 min | 💻 **Gemeinsames Löschen** | `uv run code/99_cleanup.py` auf **jedem** Rechner, kontrolliert über die Ampelkarte. Das passiert am Ende **jedes** Termins – Gesichtsdaten liegen nicht wochenlang auf Schulrechnern. Vorher prüfen: ist das Malen-nach-Zahlen-Blatt ausgedruckt? |
| 9 min | **Puffer** | Reserve und, wenn nötig, eine Verschnaufpause in der Mitte des Termins. |

> **Cliffhanger aufs Plakat schreiben:** *"Was wir gerade auf Papier gerechnet haben –
> was passiert, wenn ein Rechner das 30-mal pro Sekunde macht?"* Diese Frage wird zu
> Beginn von Termin 2 als erstes vorgelesen.

---

# Termin 2 — 90 min

**Aha-Ziel:** Ich war gerade selbst ein neuronales Netz. Und: *Detektion* ist nicht
*Erkennung*.

## Block 3 · Vom Handkernel zum neuronalen Netz — 33 min

| Zeit | Was | Details |
|---|---|---|
| 8 min | 💬💻 **Wiedereinstieg** | Plakat aufhängen, Cliffhanger-Frage vorlesen.<br>**3 min** Galerie: die ausgemalten Malen-nach-Zahlen-Blätter (HA 1b) nebeneinander an die Wand. Alle erkennen sich – aus Zahlen.<br>**3 min** die angemalten Faltungsblätter (HA 1a) nebeneinanderlegen: in jedem tritt **dieselbe senkrechte Kante** als Bild hervor. *"Der Filter hat in jedem eurer Blätter dasselbe gefunden. Jetzt lassen wir ihn 30-mal pro Sekunde laufen."*<br>**2 min** Rechner und `00_check.py` – dabei startet je ein Partner den Rechner, während der andere zuhört. |
| 9 min | 💻 `02_filter.py` **mit Testmuster** | Derselbe Kernel, jetzt live auf der Webcam, umschaltbar mit den Tasten 0 bis 9. Dazu halten die Gruppen das **Testmuster** (`handout_F_testmuster.html`) vor die Kamera: vier Felder mit je einer Kante – senkrecht, waagerecht und die beiden Diagonalen. Sie tragen für jeden Kernel ein, welche Kante hell wird und welche dunkel bleibt.<br>Die Entdeckung: Taste 4 findet **alle** Richtungen, Taste 5 und 6 lassen jeweils **genau ein Feld völlig dunkel**. Dieses dunkle Feld verrät, für welche Richtung der Kernel blind ist. |
| 7 min | 🔬 **Kernel-Challenge** | Jetzt hat die Aufgabe einen Sinn: Für die **Diagonalen** gibt es keinen fertigen Kernel. Gesucht ist einer, der `/` hell zeigt und bei `` \ `` völlig dunkel bleibt – genau ein dunkles Feld.<br>Werkzeug: `uv run code/94_kernel_labor.py`, neun Schieberegler, Wirkung sofort sichtbar. Der Tipp steht auf dem Testmuster: Die Nullen liegen immer *entlang* der Kante, die gefunden wird.<br>Hier wird **entdeckt** – der rechnerische **Beweis** ist Hausaufgabe (HA 2a). Lösung und erwartete Messwerte in [03_loesungen.md](03_loesungen.md). |
| 3 min | 🧑‍🏫 **Fazit Block 3** | **Folie 4**: "Ein neuronales Netz macht genau das – aber es *lernt* seine Kernel selbst, tausende davon, in Schichten übereinander. Ihr habt einen von Hand gebaut, ein Netz hat Millionen." |
| 6 min | **Puffer** | |

## Block 4 · Finde das Gesicht — 57 min

| Zeit | Was | Details |
|---|---|---|
| 5 min | 💻 `03_detect.py` | Live-Webcam mit Rechteck ums Gesicht, Zähler "1 Gesicht gefunden". Mit `y` zwischen Haar-Cascade (2001) und YuNet (2023) umschalten. |
| 11 min | 🔬 **Experimente-Bingo** | Arbeitsblatt C (`handout_C_bingo.html`), 12 Felder – jede Gruppe versucht, möglichst viele abzuhaken. Ziel ist, das System **hereinzulegen**: Kopf 90 Grad drehen · Hand vor den Mund · Sonnenbrille · Licht aus · **Foto auf dem Handy-Display vor die Kamera halten** · Gesicht auf einem T-Shirt · gezeichnetes Gesicht · Poster an der Wand · Steckdose oder Autofront (Pareidolie) · zwei Gesichter dicht nebeneinander · Kapuze · Maske. |
| 5 min | 💻 **Parameter drehen** | `scaleFactor` und `minNeighbors` verändern, bis das Programm überall Gesichter sieht – an der Wand, auf dem Tisch, im Pullover. Danach so streng einstellen, dass es niemanden mehr findet. Aha: *Die Empfindlichkeit ist eine Einstellung, kein Naturgesetz.* |
| 16 min | 💬🧑‍🏫 **Einordnung 2 + Fazit Block 4** | Der Kern dieses Termins, deshalb ausführlich.<br>**3 min Bingo-Ernte:** Jede Gruppe nennt **genau einen** Trick, der funktioniert hat. Alles an die Tafel. Das Handy-Foto muss dabei sein und laut ausgesprochen werden – auf dem Bingo-Blatt steht "es kommt später wieder", und "später" ist Block 6.<br>**4 min Folie 5, das Fazit:** "Das Programm hat mein Gesicht gefunden. Weiß es, dass ich es bin?" – Nein. Die Folie stellt Detektion und Erkennung gegenüber und listet auf, was das Programm für ein Gesicht gehalten hat: Poster, Zeichnung, Handy-Foto, T-Shirt-Aufdruck – und wie es ein echtes Gesicht verliert, sobald eine Hand über den Augen liegt. Kernsatz: **Es prüft nicht, ob ein Mensch davorsteht.**<br>**2 min** `03b_landmarks.py` am Beamer: 68 Gesichtspunkte, zu einem Dreiecksnetz verbunden – genau das Bild aus dem Workshop-Logo. Mit `n` zwischen Netz und Punkten umschalten. Fehlt das Modell, gehen auch die fünf YuNet-Punkte.<br>**7 min Flipchart, zwei Spalten:** *Diese Punkte sagen, WIE ein Gesicht geformt ist – nicht, WER es ist. Was könnte man damit bauen?* Sortieren in **nützlich** und **unheimlich**. Erwartbar kommen Filter, Lächel-Auslöser und Müdigkeitswarner – und mit etwas Nachhilfe auch Aufmerksamkeitsmessung. Ideensammlung und Einordnung in [03_loesungen.md](03_loesungen.md).<br>**Der Bogen wird mitgenommen** und eröffnet Termin 3. |
| 6 min | 💻 `04a_embedding.py` | Foto von sich → das Skript druckt **128 Kommazahlen**. Nichts weiter. Bewusst nüchtern: "Das bist du. Für den Computer. Mehr weiß er nicht über dein Gesicht." Zweites Foto derselben Person → die Zahlen sind *ähnlich*, aber nicht gleich. |
| 4 min | 🧑‍🏫 **Ausblick auf Block 5** | **Folie 6**: Zwei Zahlen sind ein Punkt auf Papier, drei ein Punkt im Raum, 128 ein Punkt in einem Raum, den man nicht zeichnen kann. Ähnliche Gesichter liegen dort nah beieinander. *Das* ist Gesichtserkennung – ein Abstand. Kein Fazit, sondern die offene Tür: gemessen wird erst am dritten Termin. |
| 3 min | ✍️💻 **Hausaufgabe + Löschen** | HA 2a, 2b und 2c ansagen (drei Aufträge – ruhig aufschreiben lassen). Laufzettel einsammeln. Dann `99_cleanup.py` auf jedem Rechner. Wichtig ansagen: **die Aufnahmen von heute sind danach weg, und nächstes Mal nehmen wir neu auf.** Das ist kein Versehen, das ist der Punkt. |
| 7 min | **Puffer** | |

> **Cliffhanger aufs Plakat:** *"Das bist du – 128 Zahlen. Nächstes Mal bauen wir daraus
> ein Schloss. Und dann knackt ihr das Schloss eurer Nachbargruppe."*

**Advanced:** Im Kopf von `94_kernel_labor.py` stehen fünf weitere Aufgaben – Kernel zum
Verschieben des Bildes, Kernel ohne Wirkung, und die Frage, was eine einzelne `1`
außerhalb der Mitte anrichtet. Damit ist die Kernel-Challenge auch für Schnelle nicht
zu Ende.

---

# Termin 3 — 90 min 🔑

**Aha-Ziel:** Mein Gesicht ist eine Liste aus 128 Zahlen. Sicherheit ist ein
Schwellenwert – und er ist angreifbar, aber nicht bei allen Menschen gleich gut.

## Block 5 · Wer ist das? Sicherheit ist ein Schwellenwert — 36 min

| Zeit | Was | Details |
|---|---|---|
| 6 min | 💬 **Wiedereinstieg** | Plakat und den Flipchartbogen „nützlich / unheimlich" aufhängen, Cliffhanger vorlesen. **HA 2a im Tandem-Peercheck** – die Nachbargruppe prüft den Diagonal-Kernel, kein Plenum (spart fünf Minuten und alle sind beteiligt). Folie 6 noch einmal kurz: "Du bist 128 Zahlen." Rechner booten parallel. |
| 5 min | 💻 `04a_embedding.py` **Wiederaufnahme** | Die Aufnahmen von letzter Woche sind gelöscht – das war die Zusage. Also neu: **jede Person zwei Aufnahmen, eine bewusst schwierig** (Brille ab, Haare anders, Gegenlicht, Kopf leicht gedreht). Das ist technisch zwingend – `04b`, `04c` und `05_bias.py` lesen alle aus `data/gesichter/`, und **nur dieses Skript speichert dort**. Und es ist didaktisch zwingend: nur mit schwierigen Aufnahmen überlappen sich die beiden Verteilungen in `05_bias.py` später sichtbar. |
| 10 min | 💻 `04b_vergleich.py` | Zwei Fotos hinein, Ähnlichkeit in Prozent plus Balken heraus. Testreihe auf dem Laufzettel: ich–ich (gleiches Licht) · ich–ich (Brille ab/auf, Haare anders, Grimasse) · ich–Nachbar:in · Nachbar:in–Nachbar:in · ich–Portrait aus `data/beispiele/`.<br>**Klassentabelle auf einem vorgezeichneten Flipchart** – die Gruppen tragen selbst ein, während sie messen. Acht Gruppen einzeln an die Tafel zu rufen kostet sonst Wartezeit. Frage: Welches Paar erreicht die höchste Fremd-Ähnlichkeit? Geschwister und Cousins gewinnen zuverlässig.<br>**Parallel dazu am Beamer, während die Gruppen eintragen** (kostet keine eigene Minute, wie der Auflösungs-Regler in Block 1 parallel zum Drucken läuft): der Satz aus `data/personen/` – verstorbene Persönlichkeiten aus Mathematik und Informatik, mehrere Lebensalter pro Person. Die Klasse kann bei „ich–ich" nur Brille und Licht ändern; zwanzig oder vierzig Jahre Abstand kann sie nicht herstellen.<br>Drei Aufrufe, Pointe zuletzt: **Turing mit 16 gegen Turing 1951** → 0,653, erkannt. **Grace Hopper gegen Lise Meitner** → 0,356, zwei verschiedene Personen, knapp unter der Schwelle. **Katherine Johnson 1966 gegen 2008** → **0,309, dieselbe Person, nicht erkannt.** Satz dazu: *„Zwei Frauen, die sich nie getroffen haben, liegen bei 0,356. Eine Frau und sie selbst, 42 Jahre später, bei 0,309. Die Reihenfolge ist falsch."*<br>Befehle, Werte und – wichtig – **wie der Johnson-Wert einzuordnen ist, ohne einen Fehlschluss zu begünstigen**, stehen in [03_loesungen.md](03_loesungen.md). Nur die drei gezeigten Personen benennen, sonst kippt der Slot in ein Personenquiz. |
| 15 min | 💻🧑‍🏫 `04c_faceid.py` — **das Finale + Fazit Block 5** | Die eigene Handy-Entsperrung: einmal ein Foto aufnehmen (also "Face-ID einrichten"), dann live grün **ENTSPERRT** oder rot **GESPERRT**, mit Schieberegler für den Schwellenwert.<br>Choreografie, und die Fachbegriffe fallen **direkt im Moment des Ereignisses**: (1) Standardwert 0,36 – funktioniert. (2) Nachbar:in setzt sich davor – bleibt rot. (3) Regler auf 0,05 → **jeder** entsperrt. *Genau das ist ein **False Accept**: ein Fremder kommt herein.* (4) Regler auf 0,90 → **niemand**, nicht einmal man selbst. *Das ist ein **False Reject**: ich komme nicht in mein eigenes Gerät.*<br>Dazu **Folie 7 als Fazit**: die beiden Fehlerarten gegenübergestellt, mit der Frage "Wo würdest DU den Regler setzen – beim Handy? Bei einer Banktür? Bei einer Polizeifahndung?" Die Antwort ist bei jedem Anwendungsfall anders, und sie ist immer ein Kompromiss. |

**Advanced:** `90_anwesenheit.py` (mehrere Gesichter registrieren, Namen live ins Bild),
`93_durchschnitt.py` (Gesichter mischen und mitteln), `92_fehlerkurve.py` (FAR und FRR
als zwei Kurven mit Schnittpunkt) und – der stärkste für einen Mathekurs –
`91_gesichtsraum.py`: die Hauptkomponentenanalyse projiziert alle Aufnahmen der Klasse
in eine Ebene, und die eigenen Punkte liegen sichtbar als Gruppen zusammen. Alle
brauchen die Aufnahmen aus `04a`, laufen also nur an Termin 3.

## Block 6 · Face it! Angriff und Verantwortung — 54 min

| Zeit | Was | Details |
|---|---|---|
| 12 min | 🔬 **Hack-Challenge** | Auftrag: *Entsperre den Rechner der Nachbargruppe.* **Feste Angriffspaare** (G1↔G2, G3↔G4, G5↔G6, G7↔G8), damit niemand sucht. Das Angriffsmaterial ist aus HA 2b schon da – es im Termin herzustellen würde die Challenge auffressen.<br>Punkte pro erfolgreicher Methode (Arbeitsblatt D, `handout_D_hack.html`): Foto vom Handy-Display (3 P.) · Ausdruck (3 P.) · Video des Gesichts (4 P.) · Geschwisterkind oder ähnlich aussehende Person (5 P.) · Schwellenwert heimlich verstellen (2 P.) · gespeicherte Referenzdatei austauschen (5 P.). Die Gruppen tragen ihre Punkte selbst in die Rangliste ein. |
| 6 min | 💬 **Auswertung** | Welche Angriffe klappten? **Wer hat richtig vorhergesagt?** (Die Vorhersage stand in HA 2b.) Warum funktioniert das Handy-Foto? Weil die Kamera ein flaches Bild sieht und Haut nicht von Papier unterscheiden kann. Deshalb hat echtes Face-ID eine **Infrarot-Tiefenkamera**, projiziert rund 30 000 Punkte auf das Gesicht und prüft *Liveness*. Die Nachbargruppe hat gerade bewiesen, warum das nötig ist. |
| 5 min | 🔬 **Fehler messen, Bias einordnen** | **3 min an den Gruppenrechnern:** `uv run code/05_bias.py` – braucht keine Kamera, rechnet mit den heute aufgenommenen Gesichtern. Das Skript vergleicht alle Aufnahmen paarweise und zeigt zwei Verteilungen – gleiche Person gegen verschiedene Personen. Die beiden Bereiche **überlappen sich**, und eine Tabelle zeigt für jede Schwelle, wie viele Falschabweisungen und Falschakzeptanzen entstehen. Damit ist belegt: Es gibt keine fehlerfreie Schwelle.<br>**2 min am Beamer:** **Gender Shades** (Buolamwini und Gebru, MIT 2018), Fehlerrate bei der Geschlechtsbestimmung 0,8 Prozent bei hellhäutigen Männern gegen 34,7 Prozent bei dunkelhäutigen Frauen. **NIST FRVT Part 3** (2019, 189 Algorithmen): 10- bis 100-mal höhere Falschtrefferraten für west- und ostafrikanische sowie ostasiatische Gesichter. Grund: die Trainingsdaten.<br>*Bewusst getrennt:* gemessen wird mit Klassendaten, die demografischen Unterschiede kommen aus Studien – mit zwanzig Portraits lässt sich Bias nicht seriös selbst messen, und genau das ist auch eine Lehre. |
| 16 min | 💬🧑‍🏫 **Vier Ecken + Fazit Block 6** | Vier Aussagen, vier Raumecken, die SuS stellen sich hin und begründen in einem Satz – **mit einem technischen Argument aus den drei Terminen**. Jede:r hat aus HA 2c einen Satz in der Hand, also startet die Runde nicht im Schweigen, und die Stillen sind nicht aufgeschmissen.<br>**3 min Faktenrahmen, Folie 8 als Fazit des ganzen Workshops:** DSGVO Art. 9 (Biometrie ist eine besonders geschützte Datenkategorie), EU AI Act (biometrische Echtzeit-Fernidentifizierung im öffentlichen Raum grundsätzlich verboten), Fall **Clearview AI** (Milliarden Gesichter aus dem Netz gescrapt, Millionenbußgelder in mehreren EU-Staaten). Merksatz: Ein Passwort kann man ändern. Sein Gesicht nicht.<br>**4 Runden à ca. 3 min:** ① "Gesichtserkennung an Bahnhöfen macht uns sicherer." ② "Unsere Schule darf die Anwesenheit per Gesicht erfassen." ③ "Ich darf Fotos von Freunden hochladen, ohne zu fragen." ④ "Mein Gesicht ist ein sichereres Passwort als eine PIN."<br>**Bei 20 SuS:** der Raumwechsel kostet pro Runde etwa 30 Sekunden. Wenn die Zeit knapp wird, lieber **drei Runden à 4 Minuten** als vier Runden, in denen nur je zwei Leute reden. |
| 10 min | **Abschluss** | **4 min 💬 Zurück zum Plakat:** Das Plakat aus Termin 1 wird durchgegangen. Was war richtig, was war Mythos? Die SuS korrigieren selbst. Die Antwort auf die Leitfrage steht jetzt in ihren eigenen Worten da – die sechs Punkte, die am Ende dort stehen sollten, sind in [03_loesungen.md](03_loesungen.md) aufgelistet.<br>**3 min ✍️ Ein Satz, den ich behalte:** Jede:r schreibt einen Satz auf ein Post-it und klebt es auf das Logo-Poster. Bleibt als Foto für die Doku – nur Post-its, keine Gesichter.<br>**2 min 💻 Gemeinsames Löschen:** Alle führen gleichzeitig `uv run code/99_cleanup.py` aus. Das Skript zählt mit: "17 Bilder und 4 Gesichtsvektoren entfernt." Schlusssatz: "Genau das macht kaum ein Unternehmen freiwillig."<br>**1 min 🧑‍🏫 Take-home:** **Folie 9** mit QR-Code auf das Repository – läuft während des Löschens schon an der Wand. |
| 5 min | **Puffer** | Knapp, aber siehe Notfallplan: in diesem Termin liegen zehn weitere Minuten in kürzbaren Posten. |

---

## Hausaufgaben

Alle Aufgaben funktionieren **ohne Rechner** und werden im Folgetermin wirklich
gebraucht – sie sind kein Beschäftigungsmaterial, sondern Voraussetzung.

**Nach Termin 1 (Block 1–2)**

| | Aufgabe | Wird gebraucht |
|---|---|---|
| **1a** | Arbeitsblatt B, **Seite 2 zu Ende rechnen** – nicht nur die beiden eigenen Felder, sondern alle. Dann, wie es auf dem Blatt steht: *„Male jedes Feld an, in dem eine Zahl über 10 steht."* Die Kante tritt als Bild hervor. | Block 3, Minute 3–6: die angemalten Blätter eröffnen den Termin |
| **1b** | Das eigene **Malen-nach-Zahlen-Blatt** ausmalen (rund 10 min) und einen Satz dazu: *Ab wie vielen Pixeln erkennt man, DASS es ein Gesicht ist – ab wie vielen, WER?* | Block 3, Galerie im Wiedereinstieg; und die Brücke zur Haar-Cascade, die genau so ein grobes Hell-Dunkel-Muster sucht |

**Nach Termin 2 (Block 3–4)**

| | Aufgabe | Wird gebraucht |
|---|---|---|
| **2a** | Den **Diagonal-Kernel auf Papier beweisen**: das 3×3-Gitter so ausfüllen, dass `/` hell wird und `` \ `` exakt 0 ergibt – und dann **zwei Felder von Hand nachrechnen**. Regel aus dem Unterricht: die Nullen liegen entlang der Kante. | Block 5, Tandem-Peercheck im Wiedereinstieg |
| **2b** | **Angriffsmaterial bauen:** ein Foto eines **eigenen Gruppenmitglieds, mit dessen Einverständnis** – mindestens A6 ausgedruckt und dasselbe Bild auf dem Handy, optional ein 5-Sekunden-Video. Dazu **pro Angriff eine schriftliche Vorhersage**: klappt / klappt nicht, und warum. | Block 6, Hack-Challenge – macht die 12 Minuten überhaupt erst realistisch, und die Vorhersage kann widerlegt werden |
| **2c** | **Einen Satz** zu einer der vier Vier-Ecken-Aussagen – Pro oder Contra –, gestützt auf **ein technisches Argument aus Termin 1 oder 2** („weil ein Schwellenwert …", „weil Detektion nicht Erkennung ist", „weil der Filter nur Veränderung sieht"). Zettel mitbringen. | Block 6, Vier Ecken. Die Diskussion startet auf Argumentebene statt aus dem Bauch – die einzige Maßnahme, die die Diskussionstiefe erhöht, ohne eine Minute zu kosten |

---

## Was über drei Wochen trägt – und was nicht

Im Projektvormittag blieb alles einfach hängen. Über drei Termine bricht das, und zwar
an sieben Stellen:

| Was bricht | Maßnahme |
|---|---|
| **Das Leitfragen-Plakat** – eine Schultafel ist am nächsten Tag gewischt | Packpapier statt Tafel. Die Lehrkraft rollt es ein, nimmt es mit und hängt es an jedem Termin neu auf. Zusätzlich abfotografieren. Das Wiederaufhängen ist Teil des Wiedereinstiegs. |
| **Der Bogen „nützlich / unheimlich"** aus Block 4 – er ist der Aufhänger für Block 5 und 6 | Eigener Flipchartbogen, wandert mit. |
| **Das 0/28-Gitter** aus Block 2 | Abfotografieren, in Block 3 als Referenz zeigen. |
| **Gesichtsdaten in `data/`** – wochenlang auf Schulrechnern ist keine Option (DSGVO Art. 9), und nach der Hack-Challenge wäre jede Diskussion darüber unglaubwürdig | `99_cleanup.py` am Ende **jedes** Termins, kontrolliert über die Ampelkarte. Deshalb die Wiederaufnahme mit `04a` zu Beginn von Block 5 – die ist eingeplant, nicht vergessen. So bleibt die Zusage im Elternbrief („spätestens am selben Tag") wortwörtlich eingehalten. |
| **Gruppen und Rollentausch** – Fehltage zerreißen Paare, und Gesichtserkennung braucht zwingend ein zweites Gesicht | **Feste Gruppennummern G1–G8 und fester Rechner**, Sitzplan bei der Lehrkraft. Wer den Rechner wechselt, findet seine Daten nicht. Bei 20 SuS sitzen in manchen Gruppen drei – das ist ein Vorteil, nicht ein Problem. Rollentausch **pro Termin** statt pro Station. |
| **Laufzettel und Ampelkarten** gehen bis Woche 3 verloren | Am Ende jedes Termins einsammeln – das ist gleichzeitig die Hausaufgabenkontrolle – und zu Beginn wieder ausgeben. Bingo (C) und Hack (D) erst am jeweiligen Termin ausgeben. |
| **Das Momentum** „heute bauen wir das" stirbt nach 90 Minuten | Folie 1 zeigt den Drei-Termin-Fahrplan. Jeder Termin endet mit einer **Cliffhanger-Frage, die aufs Plakat geschrieben wird** und zu Beginn des nächsten Termins als erstes vorgelesen wird. |

---

## Zeitpuffer und Notfallplan

Puffer: **9 / 13 / 5 Minuten** pro Termin (Block 2: 9 · Block 3: 6 · Block 4: 7 ·
Block 6: 5). Zu beachten: eine 90-Minuten-Doppelstunde sind netto eher 85 Minuten –
Ankommen, Einpacken, acht Rechner booten. Der echte Puffer ist also kleiner als er
aussieht. Termin 1 kommt mit dem kleinsten Puffer aus, weil dort viel **kürzbarer**
Inhalt liegt; Termin 3 hat nach `04c` fast nichts mehr, das man kürzen könnte, ohne die
Diskussion zu opfern – dafür sind die letzten Posten komprimierbar.

Falls es klemmt, in dieser Reihenfolge kürzen:

**Block 1–2 (Termin 1)**
1. Auflösungs-Regler auf eine Beamer-Demo verkürzen — spart 4 min
2. „Eine Zeile aktivieren" ganz ins Take-home verschieben — spart 6 min

**Block 3–4 (Termin 2)**
1. Kernel-Challenge auf eine Demo am Beamer verkürzen — spart 5 min
2. `03b_landmarks.py` weglassen und die Zwei-Spalten-Frage mit den fünf YuNet-Punkten
   aus `03_detect.py` stellen — spart 2 min
3. „Parameter drehen" auf eine Beamer-Demo — spart 3 min

**Block 5–6 (Termin 3)**
1. `uv run code/05_bias.py --nur-studien` – überspringt die eigene Messung und zeigt
   nur die veröffentlichten Zahlen — spart 3 min
2. Post-it-Phase als Exit-Ticket im Hinausgehen — spart 2 min
3. Vier Ecken auf drei Runden à 4 min statt vier à 3 min — kostet nichts, ist bei
   20 SuS sogar die bessere Variante
4. Klassentabelle in `04b` nur von vier Gruppen ausfüllen lassen — spart 3 min

**Nicht kürzen:** `04c_faceid.py`, die Hack-Challenge und die **Vier Ecken**. Das sind
die Momente, an die sich die Schüler:innen in einem Jahr noch erinnern – und die Vier
Ecken sind die einzige Stelle, an der sie das Gelernte selbst einordnen müssen.

**Nicht kürzen, weil technisch zwingend:** die `04a`-Wiederaufnahme zu Beginn von
Block 5. Ohne sie ist `data/gesichter/` leer, und `04b`, `04c` und `05_bias.py` laufen
nicht (`05_bias.py` bricht unter vier Aufnahmen ab).

---

## Noch anzupassen

Diese Stellen stammen noch aus der Projektvormittag-Fassung und widersprechen jetzt
diesem Plan. Sie wurden bewusst nicht mit geändert:

| Datei | Stelle | Was dort steht und was daraus werden muss |
|---|---|---|
| `docs/00_konzept.md` | Z. 9 | „Dauer: **3,5 Stunden** (Projektvormittag)" → 3 × 90 min in drei Terminen, sechs Blöcke |
| `docs/00_konzept.md` | Z. 11 | „**12–15** Schüler:innen, Partnerarbeit an 6–8 Rechnern" → bis 20 SuS in **8 Gruppen** (2–3 pro Rechner). Die Rechnerzahl passt schon. |
| `docs/00_konzept.md` | Z. 76 | Grundsatz 1: „**Sechs Folien** im ganzen Workshop" → **neun** Folien, eine Fazit-Folie pro Block. Der Grundsatz selbst gilt weiter: jeder Input unter 5 Minuten und immer *nach* dem Experiment. |
| `docs/00_konzept.md` | Z. 70 | „Der **Abschlussblock** (Angriff & Ethik)" → **Block 6** |
| `docs/00_konzept.md` | — | Dem Konzept fehlt ein Grundsatz zu den **Hausaufgaben**. Die sind jetzt tragend, nicht optional. |
| `README.md` | Z. 10 | „**3,5 Stunden.**" → drei Doppelstunden |
| `docs/03_loesungen.md` | Z. 213 | „er trägt bis in **Block 5**" → bis in Block 6 (die Nummerierung hat sich verschoben!) |
| `docs/03_loesungen.md` | Z. 305 | „Am Ende wird das Plakat von **8:05** durchgegangen" → das Plakat aus Termin 1 |
| `material/handouts/handout_A_laufzettel.html` | Z. 80 | Die Frage zitiert `gitter = 255 - gitter`. Das stimmt mit dem Code überein – **nicht** ändern, falls die Bezeichner jemals englisch werden, dann aber zwingend mit. |
| `material/handouts/handout_A_laufzettel.html` | Z. 62–63, 120 | „Am Ende des **Vormittags** …"; und bei 4a „Ihr braucht sie in den nächsten beiden Stationen" – richtig wäre: am selben Termin, denn vorher wird gelöscht. Sinnvolle Ergänzung: ein Feld „Gruppe Nr." und drei HA-Kästchen. |

**Erledigt:** `material/folien/index.html` ist auf neun Folien erweitert und trägt jetzt
die Block-Nummerierung; die Dauer-Angabe auf Folie 1 ist korrigiert.
`docs/02_technik_setup.md` hat eine Checkliste für Termin 1 und eine Kurzliste für
Termin 2 und 3 – und vorne das neue `einrichten.bat`, das die Einzelschritte ersetzt.

**Nicht betroffen:** alles in `code/`, das Startmenü und die Handouts B bis F – dort
stehen nur Stationsnummern, und die sind unverändert gültig. `handout_B_faltung.html`
passt mit acht Gruppen genau, es bleibt kein Feld übrig.
