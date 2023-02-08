@echo off
rem This script is used to execute IDM from the command line
"C:\Program Files (x86)\Internet Download Manager\IDMan.exe" /s
TIMEOUT /T 5 <null
EXIT /B