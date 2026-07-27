# Daily Student-app QA run + Slack report. Point Windows Task Scheduler at this file.
# Uses a local .venv if present, otherwise the system `python`.
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
$venvPy = Join-Path $here ".venv\Scripts\python.exe"
$py = if (Test-Path $venvPy) { $venvPy } else { "python" }
& $py "$here\run_daily.py" @args
exit $LASTEXITCODE
