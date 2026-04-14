param(
    [string]$BinaryPath = ".\\tools\\inveigh\\Inveigh.exe",
    [string]$OutputDir = ".\\results\\inveigh",
    [int]$RunTime = 30
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $BinaryPath)) {
    throw "Inveigh binary not found: $BinaryPath"
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$args = @(
    "-inspect", "y",
    "-sniffer", "n",
    "-smb", "n",
    "-fileoutput", "y",
    "-filedirectory", $OutputDir,
    "-console", "5",
    "-runtime", "$RunTime"
)

Write-Host "[+] Starting Inveigh inspect mode for $RunTime minutes"
& $BinaryPath @args
