@echo off
setlocal
set path=%~dp0\tools\graphiz\bin;%~dp0\tools\msys\bin;%path%

%~dp0\eclipse\eclipse.exe

endlocal