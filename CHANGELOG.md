# Changelog

Alle nennenswerten Änderungen an diesem Workshop. Format nach
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionsnummern nach
[Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Hinzugefügt

- Erscheinungsbild von PINGEL AI Solutions: Schriften Red Hat Display und Red Hat Text
  (selbst gehostet unter `material/brand/`, kein Abruf bei Google), Farben Navy und
  Signalblau, Absender in den Fußzeilen der Handouts und auf den Folien.
- Neues Workshop-Logo als Vektorgrafik (`images/logo.svg`): Erkennungsrahmen, halbes
  Gesicht mit Netz und den fünf Gesichtspunkten von YuNet.
- Laufzettel: Feld für die Gruppennummer und Kästchen für die fünf Hausaufgaben.
- Grundsatz 8 im Konzept: Hausaufgaben, die tragen.
- `LICENSE.md` mit beiden Lizenzen (CC BY-NC 4.0 für Material, MIT für Code) und den
  Ausnahmen; `CHANGELOG.md`; Beta-Hinweis und Abschnitte „Teil einer Workshop-Reihe“
  und „Rückmeldung“ in der README.

### Geändert

- Folien hell statt dunkel: besser lesbar am Beamer bei Tageslicht.
- Programmfenster und Terminal: Akzentfarbe Hellblau statt Cyan, Hinweisleisten in Navy.
- Laufzettel, Konzept, README und Technik-Setup an den Ablauf mit drei Terminen
  angepasst (Dauer, Gruppengröße, neun Folien, Block 6).
- Laufzettel verweist für Fehlerhilfe auf die Ampelkarte, statt sie doppelt abzudrucken.
- Version auf 0.9.0b1 gesetzt: Beta bis zum ersten Durchlauf im Unterricht.

### Behoben

- Laufzettel, Arbeitsblatt B und Elternbrief liefen beim Drucken auf eine zusätzliche
  Seite über. Jetzt: Laufzettel 2 Seiten, Arbeitsblatt B 2 Seiten, Elternbrief 3 Seiten
  (Brief und Einwilligung).
- Testsuite auf einem frisch geklonten Rechner: Fehlen die Ersatzportraits, werden die
  Stationstests übersprungen statt mit Fehlern abzubrechen.
- Station 1: In der unteren Leiste überlappten die Zahlenzeile und die Tastenhinweise.
- `.ps1`-Dateien werden mit CRLF ausgecheckt.

## Erste Fassung – 2026-09-11

Damals als 1.0.0 nummeriert, inzwischen als Beta eingestuft. Erste vollständige Fassung: sechs Blöcke an drei Terminen, Stationen 0 bis 5, fünf
Advanced-Programme, Handouts A bis F, Folien, Elternbrief, Einrichtungsskript mit
Ampelbericht und automatische Testsuite.
