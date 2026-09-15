<#
.SYNOPSIS
  Checks one local development port for start-dev.bat / stop-dev.bat.

.DESCRIPTION
  Looks at every TCP socket on the port (Listen, Bound, ...), not only LISTENING ones,
  because a crashed "uvicorn --reload" parent can keep a port Bound without serving.

  Exit codes (consumed by the .bat files):
    0  port is free
    10 port is served by this project (backend: problem+json 401 from /api/v1/auth/session;
       frontend: Vite dev server answering /@vite/client)
    20 port is held by something else; details are printed
    21 (with -Stop) the foreign process was stopped after confirmation
    22 (with -Stop) the user declined, or stopping failed

.PARAMETER Port
  TCP port to check.
.PARAMETER Kind
  "backend" or "frontend" - how to recognise this project's own server.
.PARAMETER Stop
  Offer to stop a foreign or unresponsive process holding the port (asks for confirmation).
  A working server of this project is left running (exit 10) unless -IncludeOwn is given.
.PARAMETER IncludeOwn
  With -Stop: also stop this project's own server (used by stop-dev.bat).
.PARAMETER Force
  With -Stop: stop without asking. Only used by stop-dev.bat after its own confirmation.
#>
param(
  [Parameter(Mandatory = $true)][int]$Port,
  [Parameter(Mandatory = $true)][ValidateSet("backend", "frontend")][string]$Kind,
  [switch]$Stop,
  [switch]$IncludeOwn,
  [switch]$Force
)

$ErrorActionPreference = "Stop"

function Test-OwnServer {
  try {
    if ($Kind -eq "backend") {
      $response = Invoke-WebRequest -UseBasicParsing -TimeoutSec 3 -Uri "http://127.0.0.1:$Port/api/v1/auth/session"
      return $false  # a 2xx without a session is not this API
    }
    $response = Invoke-WebRequest -UseBasicParsing -TimeoutSec 3 -Uri "http://localhost:$Port/@vite/client"
    return $response.StatusCode -eq 200
  } catch [System.Net.WebException] {
    # Windows PowerShell 5.1 has already read the error body into ErrorDetails; the response stream is then empty.
    $body = $_.ErrorDetails.Message
    if (-not $body -and $_.Exception.Response) {
      $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
      $body = $reader.ReadToEnd()
    }
    return ($Kind -eq "backend" -and $body -and $body.Contains("urn:platform:problem"))
  } catch {
    return $false
  }
}

$connections = @(Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue)
if ($connections.Count -eq 0) { exit 0 }

$own = Test-OwnServer
if ($own -and -not ($Stop -and $IncludeOwn)) { exit 10 }

$owners = $connections | Select-Object -ExpandProperty OwningProcess -Unique | Where-Object { $_ -gt 0 }
Write-Host ""
if ($own) {
  Write-Host "Port $Port is used by this project's ${Kind}:"
} else {
  Write-Host "Port $Port is held by a process that is NOT a working $Kind for this project"
  Write-Host "(it may be another app, or a crashed/stale server that no longer answers):"
}
foreach ($id in $owners) {
  $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$id" -ErrorAction SilentlyContinue
  $states = ($connections | Where-Object { $_.OwningProcess -eq $id } | Select-Object -ExpandProperty State -Unique) -join ", "
  if ($proc) {
    Write-Host ("  PID {0}  {1}  [{2}]" -f $id, $proc.Name, $states)
    Write-Host ("  Command: {0}" -f $proc.CommandLine)
  } else {
    Write-Host ("  PID {0}  (process details unavailable)  [{1}]" -f $id, $states)
  }
}

if (-not $Stop) { exit 20 }

if (-not $Force) {
  $answer = Read-Host "Stop the process(es) above? [y/N]"
  if ($answer -notmatch "^[yY]") { exit 22 }
}
try {
  foreach ($id in $owners) {
    # /T also stops reloader children (uvicorn --reload, npm -> node).
    & taskkill.exe /PID $id /T /F | Out-Null
  }
  Start-Sleep -Seconds 1
  if (@(Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue).Count -gt 0) {
    Write-Host "Port $Port is still in use after stopping. Close the owning window manually."
    exit 22
  }
  Write-Host "Stopped. Port $Port is free."
  exit 21
} catch {
  Write-Host "Could not stop the process: $($_.Exception.Message)"
  exit 22
}
