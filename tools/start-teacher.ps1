# Opens the Rust teacher (Claude Code) in learn_rust.
# Started at logon by the "Rust Teacher" shortcut in the Windows Startup folder.
# -DryRun checks everything up to launching Claude and prints what it would run.
param([switch]$DryRun)

$root = 'D:\RustroverProjects\learn_rust'
Set-Location $root

# Claude needs the network, which can take a while to come up after logon.
$deadline = (Get-Date).AddSeconds(120)
while (-not (Test-Connection -TargetName api.anthropic.com -TcpPort 443 -Quiet -TimeoutSeconds 2)) {
    if ((Get-Date) -gt $deadline) { Write-Warning 'Network still down; starting anyway.'; break }
    Start-Sleep -Seconds 3
}

$prompt = 'Start my Rust lesson.'
if ($DryRun) {
    "dry run OK: would run claude `"$prompt`" in $(Get-Location)" |
        Tee-Object -FilePath (Join-Path $env:TEMP 'rust-teacher-dryrun.txt')
    return
}
claude $prompt
