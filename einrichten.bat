@echo off
rem ======================================================================
rem  Face it!  -  Arbeitsumgebung einrichten
rem
rem  Doppelklick genuegt. Das Skript installiert uv, holt das Projekt,
rem  legt die Python-Umgebung an, prueft die Modelle und die Kamera-
rem  Freigabe und laesst am Ende die automatischen Tests laufen.
rem
rem  Es braucht KEINE Administratorrechte und aendert KEINE Windows-
rem  Einstellungen.
rem
rem  Fuer die Schul-IT:
rem    einrichten.bat /trocken    nur anzeigen, nichts veraendern
rem    einrichten.bat /neu        alles neu pruefen
rem    einrichten.bat /still      fuer den Autostart (schweigt bei Erfolg)
rem
rem  Exit-Code:  0 = bereit   1 = Fehler   2 = laeuft, aber unvollstaendig
rem ======================================================================

chcp 65001 >nul
cd /d "%~dp0"

set ARGUMENTE=
:naechstes
if "%~1"=="" goto starten
if /i "%~1"=="/trocken" set ARGUMENTE=%ARGUMENTE% -Trockenlauf
if /i "%~1"=="/neu"     set ARGUMENTE=%ARGUMENTE% -Neu
if /i "%~1"=="/still"   set ARGUMENTE=%ARGUMENTE% -Still
shift
goto naechstes

:starten
rem -ExecutionPolicy Bypass gilt nur fuer diesen einen Aufruf. Die Richtlinie
rem des Rechners bleibt unveraendert - das ist der Grund, warum die Logik in
rem einer .ps1 steckt und nicht hier: Batch kann keine Hashes, kein JSON und
rem keine Zeitgrenzen fuer Netzzugriffe.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0einrichten.ps1" %ARGUMENTE%
set ERGEBNIS=%ERRORLEVEL%

rem Im Autostart darf kein Fenster stehen bleiben und auf Enter warten.
echo %ARGUMENTE% | find /i "-Still" >nul
if errorlevel 1 pause

exit /b %ERGEBNIS%
