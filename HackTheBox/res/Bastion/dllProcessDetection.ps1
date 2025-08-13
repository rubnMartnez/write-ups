# Replace with the full or partial name of the DLL
$dllName = "wlbsctrl.dll"
$found = $false

# Enumerate all processes
foreach ($proc in Get-Process) {
    try {
        foreach ($mod in $proc.Modules) {
            if ($mod.ModuleName -like "*$dllName*") {
                Write-Output "DLL '$dllName' is loaded in process '$($proc.ProcessName)' (PID: $($proc.Id))"
                $found = $true
            }
        }
    } catch {
        # Skip processes that we don't have access to
        continue
    }
}

if (-not $found) {
    Write-Output "DLL '$dllName' is not loaded in any running process."
}
