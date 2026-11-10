@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0src\python"
set "PY="

rem 1) Python launcher: py
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 -V >nul 2>nul
    if !errorlevel!==0 set "PY=py -3"
)

rem 2) python on PATH, skip the Microsoft Store stub
if not defined PY (
    for /f "delims=" %%p in ('where python 2^>nul') do (
        if not defined PY (
            echo %%p | findstr /i "WindowsApps" >nul
            if !errorlevel!==1 set "PY=%%p"
        )
    )
)

rem 3) portable Python shipped with this bundle
if not defined PY (
    if exist "%~dp0..\_tools\python-embed\python.exe" for %%i in ("%~dp0..\_tools\python-embed\python.exe") do set "PY=%%~fi"
)

if not defined PY goto nopy
echo 使用的 Python: %PY%
%PY% -V
echo.
echo ============ 规定的 4 项测试 ============
%PY% test_status_rule.py
set "RC=%ERRORLEVEL%"
echo.
echo 退出码: %RC%   ^(0 表示全部通过^)
echo.
echo ============ 17 项补充测试 ============
%PY% -m unittest test_repair_service
echo.
echo 把上面的 Summary 与退出码原样贴到 docs\test-results.md 的“原始输出”。
pause
exit /b %RC%

:nopy
echo [错误] 没有找到可用的 Python。
echo 请到 python.org 安装 Python 3.10 以上版本，安装时勾选 "Add python.exe to PATH"；
echo 或保留 D:\rjgc1110\_tools\python-embed 便携版后再试。
pause
exit /b 1
