@echo off
title mytool - Setup
color 0B

echo.
echo ============================================================
echo                    mytool - Setup
echo                     by BasedF
echo ============================================================
echo.

REM ============================================================
REM  ETAPE 1 - Verification de Python
REM ============================================================

echo [*] Verification de Python...
where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] Python introuvable dans le PATH.
    echo.
    echo     Installe Python 3.11+ depuis :
    echo     https://www.python.org/downloads/
    echo.
    echo     IMPORTANT : coche "Add Python to PATH" pendant l'installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [+] Python %PYVER% detecte.

REM ============================================================
REM  ETAPE 2 - Verification du fichier mytool.py
REM ============================================================

if not exist "mytool.py" (
    echo.
    echo [!] mytool.py introuvable dans le dossier courant.
    echo     Mets setup.bat dans le meme dossier que mytool.py.
    echo.
    pause
    exit /b 1
)
echo [+] mytool.py trouve.

REM ============================================================
REM  ETAPE 3 - Mise a jour de pip
REM ============================================================

echo.
echo [*] Mise a jour de pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [!] Echec mise a jour pip. On continue quand meme.
)

REM ============================================================
REM  ETAPE 4 - Installation des dependances obligatoires
REM ============================================================

echo.
echo [*] Installation des dependances obligatoires...
echo     (requests, aiohttp, phonenumbers, pyautogui, pyperclip)
echo.

python -m pip install --upgrade requests aiohttp phonenumbers pyautogui pyperclip
if errorlevel 1 (
    echo.
    echo [!] Une ou plusieurs dependances ont echoue.
    echo     Verifie ta connexion internet et relance.
    echo.
    pause
    exit /b 1
)
echo [+] Dependances obligatoires installees.

REM ============================================================
REM  ETAPE 5 - Installation des dependances optionnelles
REM ============================================================

echo.
echo [*] Installation des dependances optionnelles...
echo     (selenium, mss, pynput, opencv-python, sounddevice, scipy, pywin32, pycryptodome, bcrypt, curl_cffi)
echo.

python -m pip install --upgrade selenium mss pynput opencv-python sounddevice scipy pywin32 pycryptodome bcrypt curl_cffi
echo [+] Dependances optionnelles installees (les echecs sont toleres).

REM ============================================================
REM  ETAPE 6 - Verification rapide des imports
REM ============================================================

echo.
echo [*] Verification des imports obligatoires...
python -c "import requests, aiohttp, phonenumbers, pyautogui, pyperclip; print('[+] Tous les imports obligatoires OK')"
if errorlevel 1 (
    echo.
    echo [!] Un ou plusieurs imports obligatoires ont echoue.
    echo     Relance setup.bat ou installe manuellement.
    echo.
    pause
    exit /b 1
)

echo.
echo [*] Verification des imports optionnels...
python -c "import selenium, mss, pynput, cv2, sounddevice, scipy, win32crypt, Crypto, bcrypt" 2>nul
if errorlevel 1 (
    echo [i] Certains imports optionnels manquent - pas bloquant.
    echo     Les options concernees afficheront un message dans le tool.
) else (
    echo [+] Tous les imports optionnels OK
)

REM ============================================================
REM  ETAPE 7 - Resultat final
REM ============================================================

echo.
echo ============================================================
echo                     SETUP TERMINE
echo ============================================================
echo.
echo   Tout est installe. Pour lancer le tool :
echo.
echo     python mytool.py
echo.
echo ============================================================
echo.

call :start

:start 
for /f %%A in ('"prompt $H &echo on &for %%B in (1) do rem"') do set BS=%%A

echo Si tu veux lancer Mytool.py appuie sur 1

if /I "%input%" EQU "1" start mytool.py
set /p "input=.%BS%         >