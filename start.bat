@echo off
REM Root-level quick start for Windows (CMD)
REM Double-click this file to start, or run from terminal.

set SCRIPT_DIR=%~dp0
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%start.ps1" %*
