@echo off
set ZIP=C:\PROGRA~1\7-Zip\7z.exe a -tzip -y -r
set REPO=hoochie_baby
set PACKID=1847358755
set VERSION=0.1.0


quick_manifest.exe "Hoochie Baby: QCtrl DLrnQ" "%PACKID%" >%REPO%\manifest.json
echo %VERSION% >%REPO%\VERSION

fsum -r -jm -md5 -d%REPO% * > checksum.md5
move checksum.md5 %REPO%\checksum.md5

%ZIP% %REPO%_v%VERSION%_Anki20.zip *.py %REPO%\*
cd %REPO%
%ZIP% ../%REPO%_v%VERSION%_Anki21.ankiaddon *
%ZIP% ../%REPO%_v%VERSION%_CCBC.adze *
