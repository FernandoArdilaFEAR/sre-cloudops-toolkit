<#
.SYNOPSIS
    Retrieves System event log errors from the last hour.
.EXAMPLE
    .\Get-RecentErrors.ps1
#>
param(
    [int]$Hours = 1
)

$since = (Get-Date).AddHours(-$Hours)
$filter = @{
    LogName   = 'System'
    Level     = 2               # Error
    StartTime = $since
}

Get-WinEvent -FilterHashtable $filter -ErrorAction SilentlyContinue |
    Select-Object TimeCreated, Id, ProviderName, Message |
    Format-Table -AutoSize -Wrap