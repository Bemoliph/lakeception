@echo OFF

set CURPATH=%cd%
set BINPATH=%~dp0
cd "%BINPATH%\.."
python -m lakeception %*
cd "%CURPATH%"