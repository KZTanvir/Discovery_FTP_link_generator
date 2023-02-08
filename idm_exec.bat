@echo off
rem This script is used to execute IDM from the command line
set arg1=%1
"C:\Program Files (x86)\Internet Download Manager\IDMan.exe" /n /a /d "%arg1%"
EXIT /B