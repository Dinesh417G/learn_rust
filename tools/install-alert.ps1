# FALLBACK ONLY. Since 2026-11-16 the alert runs on home-pi (tools/pi-alert-setup.sh).
# Do not install both, or every push arrives twice.
# Installs the Windows task "rcnc innings alert": every day at 20:00 it runs
# `python tools/score.py alert`, which pushes the board to the phone (coach ntfy) only
# when today's over is not green or a wicket fell. Run once, as the student:
#   pwsh -File tools/install-alert.ps1          (add -Test to also send one test push)
param([switch]$Test)
$repo = Split-Path -Parent $PSScriptRoot
$py = (Get-Command python).Source
$act = New-ScheduledTaskAction -Execute $py -Argument "`"$repo\tools\score.py`" alert" -WorkingDirectory $repo
$trg = New-ScheduledTaskTrigger -Daily -At 20:00
$set = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName 'rcnc innings alert' -Action $act -Trigger $trg -Settings $set `
    -Description 'Phone push at 20:00 if the Ardan innings over is not green (learn_rust/tools/score.py alert)' -Force |
    Select-Object TaskName, State
if ($Test) { & $py "$repo\tools\score.py" alert --test }
