<#
.SYNOPSIS
    Checks if systemd services are active (cross‑platform).
.EXAMPLE
    pwsh ./Test-DaemonHealth.ps1 -ServiceNames sshd,nginx
#>
param(
    [Parameter(Mandatory=$true)]
    [string[]]$ServiceNames
)

if ($IsLinux -or $IsMacOS) {
    foreach ($svc in $ServiceNames) {
        $status = (systemctl is-active $svc) 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Error "$svc is NOT active"
        } else {
            Write-Host "$svc : $status"
        }
    }
} else {
    Write-Error "This script requires Linux/macOS with systemd."
}