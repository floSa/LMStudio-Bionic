# Lance LM Studio avec le port de debug (CDP) utilisé par lmcdp.py pour produire les captures d'écran.
# Le port n'écoute que sur 127.0.0.1. À n'utiliser que pour la production de documentation.
param([int]$Port = 9222)

Get-Process 'LM Studio' -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 3
$exe = @("$env:LOCALAPPDATA\Programs\LM Studio\LM Studio.exe", "C:\Program Files\LM Studio\LM Studio.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $exe) { throw "LM Studio.exe introuvable (emplacements testés : %LOCALAPPDATA%\Programs et Program Files)." }
Start-Process $exe -ArgumentList "--remote-debugging-port=$Port"
Start-Sleep 8
try {
    (Invoke-RestMethod "http://127.0.0.1:$Port/json/version").Browser
} catch {
    Write-Warning "Le port de debug $Port ne répond pas : $_"
}
