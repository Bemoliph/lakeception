@echo OFF

set CURPATH=%cd%
set BINPATH=%~dp0
cd "%BINPATH%\.."
start pythonw -m lakeception %*
cd "%CURPATH%"