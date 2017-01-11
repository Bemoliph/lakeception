@echo OFF

set BINPATH=%~dp0
cd "%BINPATH%\.."
python -m lakeception %*
cd "%BINPATH%"