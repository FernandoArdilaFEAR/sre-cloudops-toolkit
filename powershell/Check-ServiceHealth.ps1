<#
.SYNOPSIS
    Checks the status of specified Windows services and restarts them if stopped.
.DESCRIPTION
    Demonstrates service management, try/catch, and verbose output.
.EXAMPLE
    .\Check-ServiceHealth.ps1 -ServiceNames 'W3SVC','Spooler'
#>
param(
    [Parameter(Mandatory=$true)]
    [string[]]$ServiceNames
)

$ErrorActionPreference = 'Stop'

foreach ($name in $ServiceNames) {
    try {
        $svc = Get-Service -Name $name -ErrorAction Stop
        Write-Host "$name : $($svc.Status)"
        if ($svc.Status -eq 'Stopped') {
            Write-Warning "$name is stopped. Attempting restart..."
            Start-Service $name
            Write-Host "$name restarted successfully." -ForegroundColor Green
        }
    }
    catch {
        Write-Error "Failed to process service $name`: $_"
    }
}