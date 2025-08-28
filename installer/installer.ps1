# Variables
$installDir = "$Env:ProgramFiles\WikiCLI"
$exeName = "wiki.exe"
$repoUrl = "https://github.com/TheCamelCaseGuy/WikiCLI/releases/download/v1.0.0/wiki.exe"
$tempFile = "$env:TEMP\WikiCLI.exe"

Write-Host "Installing WikiCLI..." -ForegroundColor Cyan

# Create install directory if not exists
if (-Not (Test-Path $installDir)) {
    Write-Host "Creating install directory at $installDir"
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

# Download latest release exe
Write-Host "Downloading WikiCLI from $repoUrl ..."
Invoke-WebRequest -Uri $repoUrl -OutFile $tempFile -UseBasicParsing

# Move and rename to wiki.exe
Write-Host "Placing executable in $installDir"
Move-Item -Path $tempFile -Destination "$installDir\$exeName" -Force

# Add install dir to PATH (for current user)
$oldPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if ($oldPath -notlike "*$installDir*") {
    Write-Host "Adding $installDir to PATH..."
    $newPath = "$oldPath;$installDir"
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")
} else {
    Write-Host "PATH already contains $installDir"
}

Write-Host "`nInstallation complete! You can now run 'wiki' from any terminal." -ForegroundColor Green
