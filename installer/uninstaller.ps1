$installDir = "$Env:ProgramFiles\WikiCLI"

Write-Host "Uninstalling WikiCLI..." -ForegroundColor Cyan

# Remove PATH entry if exists
$oldPath = [System.Environment]::GetEnvironmentVariable("Path", "User")

if ($oldPath -like "*$installDir*") {
    Write-Host "Removing $installDir from PATH..."
    $newPath = ($oldPath.Split(";") | Where-Object { $_ -ne $installDir }) -join ";"
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
} else {
    Write-Host "PATH does not contain $installDir"
}

# Delete install directory
if (Test-Path $installDir) {
    Write-Host "Removing install directory at $installDir"
    Remove-Item -Recurse -Force $installDir
} else {
    Write-Host "No install directory found at $installDir"
}

Write-Host "`nWikiCLI has been uninstalled successfully." -ForegroundColor Green
