<#
    Face it! - Arbeitsumgebung einrichten und pruefen

    Richtet einen Rechner komplett fuer den Workshop ein: uv installieren,
    Projekt holen, Umgebung anlegen, Modelle pruefen, Tests laufen lassen.
    Danach steht ein Ampelbericht auf dem Bildschirm.

    Dieses Skript aendert KEINE Windows-Einstellungen. Es prueft die
    Kamera-Freigabe und meldet sie, wenn sie fehlt - setzen muss sie die IT.

    Es braucht KEINE Administratorrechte: uv und Python landen im
    Benutzerprofil.

    Aufruf (normalerweise ueber einrichten.bat):
        .\einrichten.ps1
        .\einrichten.ps1 -Trockenlauf      nur anzeigen, nichts tun
        .\einrichten.ps1 -Neu              alles neu pruefen, Stempel ignorieren
        .\einrichten.ps1 -Still            fuer den Autostart, schweigt bei Erfolg

    Exit-Code:  0 = bereit   1 = Fehler   2 = laeuft, aber unvollstaendig
#>

[CmdletBinding()]
param(
    # Wohin das Projekt soll. Standard: Benutzerprofil, damit keine
    # Administratorrechte noetig sind.
    [string] $Ziel = (Join-Path $env:USERPROFILE "face-it"),

    # Woher das Projekt kommt. MUSS auf das eigene Repository zeigen.
    [string] $Quelle = "https://github.com/fabianpingel/face-it",

    # Welcher Stand geholt wird. Fuer den Workshop besser ein Tag als ein
    # Zweig: dann kann ein neuer Commit nicht am Morgen alle Rechner lahmlegen.
    [string] $Stand = "main",

    # Nur anzeigen, was passieren wuerde.
    [switch] $Trockenlauf,

    # Stempeldatei ignorieren und alles neu pruefen.
    [switch] $Neu,

    # Fuer den Autostart: bei Erfolg nichts ausgeben.
    [switch] $Still,

    # Wohin der Bericht geschrieben wird.
    [string] $Bericht = (Join-Path $env:USERPROFILE "face-it-bericht.txt")
)

$ErrorActionPreference = "Stop"

# Wie lange ein Stempel gilt. Danach wird wieder voll geprueft.
$STEMPEL_TAGE = 7

# Windows PowerShell 5.1 nimmt sonst TLS 1.0 und scheitert an github.com.
try {
    [Net.ServicePointManager]::SecurityProtocol =
        [Net.SecurityProtocolType]::Tls12
} catch {}

# Liegt dieses Skript in einem fertigen Projektordner, ist DAS das Ziel - und
# das muss hier schon feststehen, nicht erst in Test-Projekt. Sonst wird die
# Stempeldatei im Standardpfad gesucht, der Schnellausstieg greift nie, und
# der Autostart prueft bei jedem Login alles neu.
$script:SkriptOrdner = Split-Path -Parent $PSCommandPath
if (Test-Path (Join-Path $script:SkriptOrdner "pyproject.toml")) {
    $Ziel = $script:SkriptOrdner
}


# ===================================================== Ausgabe und Protokoll

$script:Protokoll = New-Object System.Collections.ArrayList
$script:Ergebnisse = New-Object System.Collections.ArrayList

function Schreibe {
    param([string] $Text, [string] $Farbe = "Gray")
    [void] $script:Protokoll.Add($Text)
    if (-not $Still) { Write-Host $Text -ForegroundColor $Farbe }
}

function Titel {
    param([string] $Text)
    Schreibe ""
    Schreibe "  $Text" "White"
    Schreibe ("  " + ("-" * $Text.Length)) "DarkGray"
}

function Schritt {
    param([string] $Text)
    Schreibe "  ... $Text" "DarkGray"
}

# Ergebnis eines Pruefpunkts festhalten. Zustand: Ok, Warnung, Fehler, Uebersprungen
function Ergebnis {
    param(
        [string] $Punkt,
        [string] $Zustand,
        [string] $Hinweis = ""
    )
    [void] $script:Ergebnisse.Add([pscustomobject]@{
        Punkt   = $Punkt
        Zustand = $Zustand
        Hinweis = $Hinweis
    })

    $zeichen = "?"
    $farbe = "Gray"
    if ($Zustand -eq "Ok")            { $zeichen = "OK  "; $farbe = "Green" }
    elseif ($Zustand -eq "Warnung")   { $zeichen = "!   "; $farbe = "Yellow" }
    elseif ($Zustand -eq "Fehler")    { $zeichen = "FEHL"; $farbe = "Red" }
    elseif ($Zustand -eq "Uebersprungen") { $zeichen = "--  "; $farbe = "DarkGray" }

    $zeile = "  [$zeichen] $Punkt"
    if ($Hinweis) { $zeile += "  ($Hinweis)" }
    [void] $script:Protokoll.Add($zeile)
    if (-not $Still) { Write-Host $zeile -ForegroundColor $farbe }
}

function Tun {
    <# Fuehrt etwas aus - oder sagt im Trockenlauf nur, was es waere. #>
    param([string] $Was, [scriptblock] $Block)
    if ($Trockenlauf) {
        Schreibe "  [TROCKEN] $Was" "Cyan"
        return $true
    }
    Schritt $Was
    & $Block
    return $true
}

function Starte {
    <#
        Ruft ein externes Programm auf und faengt beide Ausgabekanaele ein.

        Warum eigens dafuer eine Funktion: In Windows PowerShell 5.1 verpackt
        "2>&1" jede stderr-Zeile eines nativen Programms in einen ErrorRecord.
        Zusammen mit $ErrorActionPreference = "Stop" wird daraus ein Abbruch -
        auch dann, wenn das Programm selbst Exit-Code 0 liefert. uv schreibt
        seinen Fortschritt nach stderr, also wuerde jedes "uv sync" das Skript
        abbrechen. Deshalb wird die Einstellung hier lokal gelockert und
        danach zurueckgesetzt; bewertet wird allein der Exit-Code.
    #>
    param([string] $Programm, [string[]] $Argumente = @())

    $alt = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $text = (& $Programm @Argumente 2>&1 | Out-String)
        return [pscustomobject]@{ Code = $LASTEXITCODE; Text = $text.Trim() }
    } catch {
        return [pscustomobject]@{ Code = 9009; Text = $_.Exception.Message }
    } finally {
        $ErrorActionPreference = $alt
    }
}


# ===================================================== einzelne Pruefungen

function Test-Vorbedingungen {
    Titel "1. Vorbedingungen"

    $ps = $PSVersionTable.PSVersion
    if ($ps.Major -lt 5) {
        Ergebnis "PowerShell $ps" "Fehler" "5.1 oder neuer gebraucht"
        return $false
    }
    Ergebnis "PowerShell $ps" "Ok"

    # Schreibrecht im Zielverzeichnis - ohne das geht gar nichts.
    $eltern = Split-Path $Ziel -Parent
    try {
        if (-not (Test-Path $eltern)) {
            New-Item -ItemType Directory -Path $eltern -Force | Out-Null
        }
        $probe = Join-Path $eltern ".faceit-schreibprobe"
        Set-Content -Path $probe -Value "x" -Encoding utf8
        Remove-Item $probe -Force
        Ergebnis "Schreibrecht in $eltern" "Ok"
    } catch {
        Ergebnis "Schreibrecht in $eltern" "Fehler" $_.Exception.Message
        return $false
    }

    # Internet. Mit kurzem Timeout, damit das Skript im Autostart nicht haengt,
    # wenn das Schul-WLAN morgens noch nicht steht.
    $erreichbar = $false
    try {
        $anfrage = [Net.HttpWebRequest]::Create("https://astral.sh")
        $anfrage.Method = "HEAD"
        $anfrage.Timeout = 8000
        $antwort = $anfrage.GetResponse()
        $antwort.Close()
        $erreichbar = $true
    } catch {}

    if ($erreichbar) {
        Ergebnis "Internetverbindung" "Ok"
    } else {
        Ergebnis "Internetverbindung" "Warnung" "astral.sh nicht erreichbar"
    }
    return $true
}

function Test-Uv {
    Titel "2. uv (Paket- und Python-Verwalter)"

    # uv landet unter %USERPROFILE%\.local\bin. Frisch installiert ist das noch
    # nicht im PATH dieses Prozesses - deshalb vorsorglich ergaenzen.
    $lokal = Join-Path $env:USERPROFILE ".local\bin"
    if ((Test-Path $lokal) -and ($env:PATH -notlike "*$lokal*")) {
        $env:PATH = "$lokal;$env:PATH"
    }

    $uv = Get-Command uv -ErrorAction SilentlyContinue
    if ($uv) {
        Ergebnis "uv vorhanden" "Ok" (Starte "uv" @("--version")).Text
        return $true
    }

    if ($Trockenlauf) {
        Ergebnis "uv wuerde installiert werden" "Uebersprungen" "Trockenlauf"
        return $true
    }

    Schritt "uv wird installiert (Benutzerprofil, keine Adminrechte)"
    try {
        $skript = (Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" `
                    -UseBasicParsing -TimeoutSec 60).Content
        Invoke-Expression $skript
    } catch {
        Ergebnis "uv installieren" "Fehler" $_.Exception.Message
        return $false
    }

    if ((Test-Path $lokal) -and ($env:PATH -notlike "*$lokal*")) {
        $env:PATH = "$lokal;$env:PATH"
    }
    $uv = Get-Command uv -ErrorAction SilentlyContinue
    if (-not $uv) {
        Ergebnis "uv installieren" "Fehler" "uv ist nach der Installation nicht im PATH"
        return $false
    }
    Ergebnis "uv installiert" "Ok" (Starte "uv" @("--version")).Text
    return $true
}

function Test-Projekt {
    Titel "3. Projekt holen"

    # Laeuft dieses Skript schon aus einem fertigen Projektordner?
    $hier = Split-Path -Parent $PSCommandPath
    if (Test-Path (Join-Path $hier "pyproject.toml")) {
        $script:Ziel = $hier
        Ergebnis "Projekt liegt bereits hier" "Ok" $hier
        return $true
    }

    if (Test-Path (Join-Path $Ziel "pyproject.toml")) {
        Ergebnis "Projekt vorhanden" "Ok" $Ziel
        # Wenn es ein git-Klon ist, auf den gewuenschten Stand bringen.
        if ((Test-Path (Join-Path $Ziel ".git")) -and
            (Get-Command git -ErrorAction SilentlyContinue)) {
            Tun "Projekt auf Stand '$Stand' bringen" {
                Push-Location $Ziel
                try {
                    $hol = Starte "git" @("fetch", "--depth", "1", "origin", $Stand)
                    if ($hol.Code -eq 0) {
                        Starte "git" @("checkout", "--force", $Stand) | Out-Null
                        Starte "git" @("reset", "--hard", "origin/$Stand") | Out-Null
                    } else {
                        Schreibe "  Aktualisieren nicht moeglich - der vorhandene Stand wird benutzt." "Yellow"
                    }
                } finally { Pop-Location }
            } | Out-Null
        }
        return $true
    }

    if ($Trockenlauf) {
        Ergebnis "Projekt wuerde geholt werden" "Uebersprungen" "nach $Ziel"
        return $true
    }

    # Weg 1: git. Der bevorzugte Weg, weil spaeter aktualisierbar.
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Schritt "git clone von $Quelle"
        $klon = Starte "git" @("clone", "--depth", "1", "--branch", $Stand,
                               "$Quelle.git", $Ziel)
        if ($klon.Code -eq 0 -and (Test-Path (Join-Path $Ziel "pyproject.toml"))) {
            Ergebnis "Projekt geklont (git)" "Ok" $Ziel
            return $true
        }
        Schreibe "  git hat nicht geklappt - es wird der ZIP-Weg versucht." "Yellow"
        Schreibe ("  " + $klon.Text) "DarkGray"
    } else {
        Schreibe "  git ist nicht installiert - es wird der ZIP-Weg benutzt." "DarkGray"
    }

    # Weg 2: ZIP. Braucht kein git und keine Adminrechte.
    # /archive/<Stand>.zip funktioniert fuer Zweige und Tags gleichermassen.
    $zipUrl = "$Quelle/archive/$Stand.zip"
    $zipDatei = Join-Path $env:TEMP "face-it-$Stand.zip"
    $entpackt = Join-Path $env:TEMP "face-it-entpackt"
    try {
        Schritt "ZIP herunterladen: $zipUrl"
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipDatei -UseBasicParsing `
            -TimeoutSec 300

        Schritt "ZIP entpacken"
        if (Test-Path $entpackt) { Remove-Item $entpackt -Recurse -Force }
        Expand-Archive -Path $zipDatei -DestinationPath $entpackt -Force

        # GitHub packt alles in einen Unterordner "<repo>-<stand>".
        $inhalt = Get-ChildItem $entpackt -Directory | Select-Object -First 1
        if (-not $inhalt) { throw "Das ZIP war leer." }

        New-Item -ItemType Directory -Path $Ziel -Force | Out-Null
        Copy-Item (Join-Path $inhalt.FullName "*") $Ziel -Recurse -Force

        Remove-Item $zipDatei -Force
        Remove-Item $entpackt -Recurse -Force

        if (-not (Test-Path (Join-Path $Ziel "pyproject.toml"))) {
            throw "pyproject.toml fehlt nach dem Entpacken."
        }
        Ergebnis "Projekt geholt (ZIP)" "Warnung" `
            "ohne git - Aktualisieren heisst: neu herunterladen"
        return $true
    } catch {
        Ergebnis "Projekt holen" "Fehler" $_.Exception.Message
        Schreibe ""
        Schreibe "  Pruefe die Adresse: $Quelle" "Yellow"
        Schreibe "  Sie muss auf ein erreichbares Repository zeigen." "Yellow"
        Schreibe "  Anders angeben:  .\einrichten.ps1 -Quelle <URL>" "Yellow"
        return $false
    }
}

function Test-Umgebung {
    Titel "4. Python-Umgebung anlegen"

    if ($Trockenlauf) {
        Ergebnis "uv sync wuerde laufen" "Uebersprungen" "Trockenlauf"
        return $true
    }

    Push-Location $Ziel
    try {
        Schritt "uv sync --extra tests (holt auch Python, falls noetig)"
        $lauf = Starte "uv" @("sync", "--extra", "tests")
        if ($lauf.Code -ne 0) {
            Ergebnis "uv sync" "Fehler" "Exit-Code $($lauf.Code)"
            Schreibe $lauf.Text "DarkGray"
            return $false
        }
        Ergebnis "Umgebung angelegt" "Ok" "opencv-contrib + numpy + pytest"

        $py = Starte "uv" @("run", "python", "-c",
              "import sys; print('.'.join(map(str, sys.version_info[:3])))")
        if ($py.Code -eq 0) {
            Ergebnis "Python $($py.Text)" "Ok"
        } else {
            Ergebnis "Python startet" "Fehler" $py.Text
            return $false
        }
        return $true
    } finally {
        Pop-Location
    }
}

function Test-Modelle {
    Titel "5. Modelle"

    $modelle = @(
        @{ Name = "yunet.onnx"; Min = 200000;
           Zweck = "Gesichter finden (Station 3 und 4)" },
        @{ Name = "sface.onnx"; Min = 30000000;
           Zweck = "128 Zahlen pro Gesicht (Station 4)" }
    )

    $alleDa = $true
    foreach ($m in $modelle) {
        $datei = Join-Path $Ziel "models\$($m.Name)"
        if (-not (Test-Path $datei)) {
            Ergebnis $m.Name "Fehler" "fehlt - $($m.Zweck)"
            $alleDa = $false
            continue
        }
        $groesse = (Get-Item $datei).Length
        if ($groesse -lt $m.Min) {
            Ergebnis $m.Name "Fehler" `
                ("nur " + [math]::Round($groesse / 1MB, 1) + " MB - Download abgebrochen")
            $alleDa = $false
            continue
        }
        Ergebnis $m.Name "Ok" ([math]::Round($groesse / 1MB, 1).ToString() + " MB")
    }

    if (-not $alleDa -and -not $Trockenlauf) {
        Push-Location $Ziel
        try {
            Schritt "Fehlende Modelle nachladen"
            $lauf = Starte "uv" @("run", "code/tools/modelle_holen.py")
            if ($lauf.Code -ne 0) {
                Schreibe "  Nachladen fehlgeschlagen:" "Yellow"
                Schreibe $lauf.Text "DarkGray"
            }
        } finally { Pop-Location }
    }

    # lbfmodel.yaml ist Kuer und liegt absichtlich nicht im Repository.
    $lbf = Join-Path $Ziel "models\lbfmodel.yaml"
    if (Test-Path $lbf) {
        Ergebnis "lbfmodel.yaml (Station 3b)" "Ok" "vorhanden"
    } else {
        Ergebnis "lbfmodel.yaml (Station 3b)" "Uebersprungen" `
            "nur fuer den Beamer-Rechner noetig"
    }
    return $alleDa
}

function Test-Kamera {
    Titel "6. Kamera-Freigabe von Windows"

    # Nur pruefen, nicht setzen. Die Datenschutzeinstellung gehoert der IT.
    $pfad = "HKCU:\Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam"
    try {
        $wert = (Get-ItemProperty -Path $pfad -Name Value -ErrorAction Stop).Value
        if ($wert -eq "Allow") {
            Ergebnis "Apps duerfen die Kamera benutzen" "Ok"
        } else {
            Ergebnis "Apps duerfen die Kamera benutzen" "Fehler" "steht auf '$wert'"
            Schreibe ""
            Schreibe "  Zu setzen unter:" "Yellow"
            Schreibe "    Einstellungen > Datenschutz und Sicherheit > Kamera" "Yellow"
            Schreibe "    'Apps den Zugriff auf die Kamera erlauben' einschalten," "Yellow"
            Schreibe "    ebenso 'Desktop-Apps den Zugriff erlauben'." "Yellow"
            Schreibe "  Dieses Skript aendert die Einstellung absichtlich nicht." "DarkGray"
        }
    } catch {
        Ergebnis "Kamera-Freigabe" "Uebersprungen" "Schluessel nicht gesetzt (normal)"
    }

    # Belegt ein anderes Programm die Kamera? Haeufigster Stolperstein.
    $stoerer = @("Teams", "ms-teams", "Zoom", "WindowsCamera", "Skype")
    $laufen = @()
    foreach ($name in $stoerer) {
        if (Get-Process -Name $name -ErrorAction SilentlyContinue) {
            $laufen += $name
        }
    }
    if ($laufen.Count -gt 0) {
        Ergebnis "Kein Programm belegt die Kamera" "Warnung" `
            ("laeuft: " + ($laufen -join ", "))
    } else {
        Ergebnis "Kein Programm belegt die Kamera" "Ok"
    }
}

function Test-Tests {
    Titel "7. Automatische Tests"

    if ($Trockenlauf) {
        Ergebnis "pytest wuerde laufen" "Uebersprungen" "Trockenlauf"
        return $true
    }

    Push-Location $Ziel
    try {
        $lauf = Starte "uv" @("run", "--extra", "tests", "pytest")

        # Die Zusammenfassungszeile von pytest herausziehen.
        $zeile = ($lauf.Text -split "`n" |
                  Where-Object { $_ -match "passed|failed|error" } |
                  Select-Object -Last 1)
        if ($zeile) { $zeile = $zeile.Trim() } else { $zeile = "keine Zusammenfassung" }

        if ($lauf.Code -eq 0) {
            Ergebnis "Testsuite" "Ok" $zeile
            # Uebersprungene Tests sind hier die eigentliche Information:
            # sie sagen, was auf diesem Rechner fehlt (Webcam, Landmarks).
            foreach ($z in ($lauf.Text -split "`n")) {
                if ($z -match "^SKIPPED") {
                    Schreibe ("      " + $z.Trim()) "DarkGray"
                }
            }
            return $true
        }
        Ergebnis "Testsuite" "Fehler" $zeile
        Schreibe ""
        Schreibe $lauf.Text "DarkGray"
        return $false
    } finally {
        Pop-Location
    }
}


# ===================================================== Stempel (fuer Autostart)

function Stempelpfad { Join-Path $Ziel ".einrichtung-geprueft.json" }

function Stempel-Gueltig {
    if ($Neu -or $Trockenlauf) { return $false }
    $pfad = Stempelpfad
    if (-not (Test-Path $pfad)) { return $false }
    try {
        $stempel = Get-Content $pfad -Raw | ConvertFrom-Json
        $alter = (Get-Date) - [datetime]$stempel.Geprueft
        if ($alter.TotalDays -gt $STEMPEL_TAGE) { return $false }
        if ($stempel.Zustand -ne "bereit") { return $false }
        # Zwei schnelle Stichproben - ein Stempel allein beweist nichts.
        if (-not (Test-Path (Join-Path $Ziel "models\sface.onnx"))) { return $false }
        if (-not (Test-Path (Join-Path $Ziel ".venv"))) { return $false }
        return $true
    } catch {
        return $false
    }
}

function Stempel-Schreiben {
    param([string] $Zustand)
    if ($Trockenlauf) { return }
    try {
        @{
            Zustand  = $Zustand
            Geprueft = (Get-Date).ToString("o")
            Rechner  = $env:COMPUTERNAME
            Benutzer = $env:USERNAME
        } | ConvertTo-Json | Set-Content -Path (Stempelpfad) -Encoding utf8
    } catch {}
}


# ===================================================== Hauptlauf

if (Stempel-Gueltig) {
    # Autostart-Schnellausstieg: alles war vor Kurzem in Ordnung.
    if (-not $Still) {
        Write-Host ""
        Write-Host "  Face it! ist auf diesem Rechner bereits eingerichtet und geprueft." -ForegroundColor Green
        Write-Host "  Erneut vollstaendig pruefen:  .\einrichten.ps1 -Neu" -ForegroundColor DarkGray
        Write-Host ""
    }
    exit 0
}

if (-not $Still) {
    Write-Host ""
    Write-Host "  ============================================" -ForegroundColor Cyan
    Write-Host "   Face it!  -  Arbeitsumgebung einrichten" -ForegroundColor Cyan
    Write-Host "  ============================================" -ForegroundColor Cyan
    if ($Trockenlauf) {
        Write-Host "   TROCKENLAUF - es wird nichts veraendert" -ForegroundColor Yellow
    }
}

Schreibe ""
Schreibe "  Rechner:  $env:COMPUTERNAME"
Schreibe "  Benutzer: $env:USERNAME"
Schreibe "  Ziel:     $Ziel"
Schreibe "  Zeit:     $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

$abbruch = $false
if (-not (Test-Vorbedingungen)) { $abbruch = $true }
if (-not $abbruch -and -not (Test-Uv))       { $abbruch = $true }
if (-not $abbruch -and -not (Test-Projekt))  { $abbruch = $true }
if (-not $abbruch -and -not (Test-Umgebung)) { $abbruch = $true }

if (-not $abbruch) {
    Test-Modelle | Out-Null
    Test-Kamera
    Test-Tests | Out-Null
}


# ===================================================== Bericht

$fehler   = @($script:Ergebnisse | Where-Object { $_.Zustand -eq "Fehler" })
$warnung  = @($script:Ergebnisse | Where-Object { $_.Zustand -eq "Warnung" })

Titel "Ergebnis"

if ($fehler.Count -eq 0 -and $warnung.Count -eq 0) {
    Schreibe ""
    Schreibe "  GRUEN - dieser Rechner ist bereit fuer den Workshop." "Green"
    Schreibe ""
    Schreibe "  Starten mit:  start.bat" "White"
    $code = 0
    Stempel-Schreiben "bereit"
} elseif ($fehler.Count -eq 0) {
    Schreibe ""
    Schreibe "  GELB - der Workshop laeuft, aber etwas fehlt:" "Yellow"
    foreach ($w in $warnung) { Schreibe "    - $($w.Punkt): $($w.Hinweis)" "Yellow" }
    Schreibe ""
    Schreibe "  Starten mit:  start.bat" "White"
    $code = 2
    Stempel-Schreiben "unvollstaendig"
} else {
    Schreibe ""
    Schreibe "  ROT - so laeuft der Workshop nicht:" "Red"
    foreach ($f in $fehler) { Schreibe "    - $($f.Punkt): $($f.Hinweis)" "Red" }
    Schreibe ""
    Schreibe "  Einzelschritte und Fehlerbehebung: docs/02_technik_setup.md" "White"
    $code = 1
    Stempel-Schreiben "fehler"
}

# Bericht wegschreiben, damit die IT ihn einsammeln kann.
try {
    $kopf = @(
        "Face it! - Einrichtungsbericht",
        "Rechner:  $env:COMPUTERNAME",
        "Benutzer: $env:USERNAME",
        "Zeit:     $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
        "Zustand:  " + @("bereit", "FEHLER", "unvollstaendig")[$code],
        ""
    )
    ($kopf + $script:Protokoll) | Set-Content -Path $Bericht -Encoding utf8
    Schreibe ""
    Schreibe "  Bericht: $Bericht" "DarkGray"
} catch {
    Schreibe "  Der Bericht liess sich nicht schreiben: $($_.Exception.Message)" "Yellow"
}

Schreibe ""
exit $code
