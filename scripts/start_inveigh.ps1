param(
    [string]$BinaryPath = ".\\tools\\inveigh\\Inveigh.exe",
    [string]$OutputDir = ".\\results\\inveigh",
    [int]$RunTime = 0
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $BinaryPath)) {
    throw "Inveigh binary not found: $BinaryPath"
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$args = @(
    "-sniffer", "n",
    "-smb", "n",
    "-llmnr", "y",
    "-nbns", "y",
    "-mdns", "y",
    "-dns", "y",
    "-fileoutput", "y",
    "-filedirectory", $OutputDir,
    "-console", "5"
)

if ($RunTime -gt 0) {
    $args += @("-runtime", "$RunTime")
}

Write-Host "[+] Starting Inveigh with output dir: $OutputDir"
& $BinaryPath @args
