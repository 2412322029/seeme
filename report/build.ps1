function Execute-Command {
    param (
        [string]$command
    )
    Write-Host "Executing: $command"
    $output = Invoke-Expression $command
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error occurred: $output" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

# 构建 report_gui.py
$reportGuiCommand = @(
    "nuitka",
    "--standalone",
    "--follow-imports",
    "--lto=yes",
    "--enable-plugin=tk-inter",
    "--windows-icon-from-ico=icon.ico",
    "--output-filename=report.exe",
    "--output-dir=dist",
    "--no-deployment-flag=self-execution",
    "--windows-console-mode=disable",
    "report_gui.py"
) -join " "
Execute-Command $reportGuiCommand

$reportCommand = @(
    "nuitka",
    "--standalone",
    "--follow-imports",
    "--lto=yes",
    "--output-filename=report_cli.exe",
    "--output-dir=dist",
    "report.py"
) -join " "
Execute-Command $reportCommand

# 复制 icon.ico 到 dist 目录
$iconSource = "icon.ico"
$iconDestination = "dist\report_gui.dist\icon.ico"

if (Test-Path $iconSource) {
    Copy-Item -Path $iconSource -Destination $iconDestination -Force
    Write-Host "Copied icon.ico to dist directory." -ForegroundColor Cyan
} else {
    Write-Host "icon.ico not found. Skipping copy." -ForegroundColor Yellow
}
Write-Host "Build completed." -ForegroundColor Green

$sourcePath = "dist\report.dist\report_cli.exe"
$destinationPath = "dist\report_gui.dist\"
$upxPath = "upx"
$sevenZipPath = "7z"
if (-Not (Test-Path -Path $destinationPath))
{
    New-Item -ItemType Directory -Path $destinationPath
}
Copy-Item -Path $sourcePath -Destination $destinationPath -Force

& $upxPath "$destinationPath\report_cli.exe"
& $sevenZipPath a -tzip "dist\report_gui.dist.zip" "$destinationPath\*"