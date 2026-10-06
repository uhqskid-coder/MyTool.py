#!/usr/bin/env bash
# ============================================================
#                    mytool - Setup Linux
#                      by BasedF
# ============================================================

set -u

# Couleurs ANSI
R="\033[0m"
B="\033[38;2;0;170;255m"      # bleu
C="\033[38;2;0;235;255m"      # cyan
G="\033[38;2;80;145;190m"     # gris
Y="\033[38;2;255;200;80m"     # jaune
RD="\033[38;2;255;80;80m"     # rouge
GR="\033[38;2;80;255;140m"    # vert

echo ""
echo -e "${C}============================================================${R}"
echo -e "${C}                mytool - Setup Linux${R}"
echo -e "${C}                    by BasedF${R}"
echo -e "${C}============================================================${R}"
echo ""

# ============================================================
#  ETAPE 1 - Verification distribution
# ============================================================

if [ ! -f /etc/arch-release ]; then
    echo -e "${Y}[!] Ce script est fait pour Arch/BlackArch.${R}"
    echo -e "${G}[i] Sur une autre distro, installe manuellement :${R}"
    echo -e "${G}    python3, python-pip, gcc, libxcb, libxkbcommon, xdotool${R}"
    echo ""
    read -rp "Continuer quand meme ? (y/n) : " CONT
    if [ "$CONT" != "y" ] && [ "$CONT" != "Y" ]; then
        exit 1
    fi
fi

# ============================================================
#  ETAPE 2 - Verification Python
# ============================================================

echo -e "${B}[*] Verification de Python...${R}"
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RD}[!] python3 introuvable.${R}"
    echo -e "${G}    Installation via pacman...${R}"
    sudo pacman -S --needed --noconfirm python python-pip
else
    PYVER=$(python3 --version 2>&1)
    echo -e "${GR}[+] $PYVER detecte.${R}"
fi

# ============================================================
#  ETAPE 3 - Verification mytool.py
# ============================================================

if [ ! -f "mytool.py" ]; then
    echo -e "${RD}[!] mytool.py introuvable dans le dossier courant.${R}"
    echo -e "${G}    Mets setup.sh dans le meme dossier que mytool.py.${R}"
    exit 1
fi
echo -e "${GR}[+] mytool.py trouve.${R}"

# ============================================================
#  ETAPE 4 - Detection X11 / Wayland
# ============================================================

SESSION_TYPE="${XDG_SESSION_TYPE:-unknown}"
echo ""
echo -e "${B}[*] Detection de la session graphique...${R}"
if [ "$SESSION_TYPE" = "wayland" ]; then
    echo -e "${Y}[!] Session Wayland detectee.${R}"
    echo -e "${Y}    pyautogui ne fonctionne PAS nativement sur Wayland.${R}"
    echo -e "${G}    Fallback conseille : installe ydotool et utilise XWayland.${R}"
    echo -e "${G}    L'option 3 (Text Bomber) peut ne pas marcher correctement.${R}"
elif [ "$SESSION_TYPE" = "x11" ]; then
    echo -e "${GR}[+] Session X11 detectee. pyautogui fonctionnera.${R}"
else
    echo -e "${Y}[i] Type de session inconnu ($SESSION_TYPE).${R}"
fi

# ============================================================
#  ETAPE 5 - Installation des paquets systeme
# ============================================================

echo ""
echo -e "${B}[*] Installation des paquets systeme (pacman)...${R}"
echo -e "${G}    gcc, python-pip, xorg-server, libxcb, libxkbcommon, scrot, xdotool,${R}"
echo -e "${G}    tk, libjpeg-turbo, opencv, portaudio, espeak-ng, sqlite, openssl${R}"
echo ""

# Paquets Arch officiels
PKGS=(
    base-devel
    python
    python-pip
    xorg-server
    xorg-xinit
    libxcb
    libxkbcommon
    libxkbcommon-x11
    xdotool
    scrot
    tk
    libjpeg-turbo
    libpng
    sqlite
    openssl
    opencv
    portaudio
    espeak-ng
    ffmpeg
    alsa-utils
    pulseaudio-utils
)

sudo pacman -S --needed --noconfirm "${PKGS[@]}"
if [ $? -ne 0 ]; then
    echo -e "${Y}[!] Certains paquets ont echoue. On continue quand meme.${R}"
fi

# ============================================================
#  ETAPE 6 - Mise a jour de pip
# ============================================================

echo ""
echo -e "${B}[*] Mise a jour de pip...${R}"
python3 -m pip install --upgrade pip --user 2>/dev/null || \
    python3 -m pip install --upgrade pip --break-system-packages 2>/dev/null || true

# Detection du mode pip (system-wide vs --user vs --break-system-packages)
PIP_MODE=""
if python3 -m pip install --help 2>/dev/null | grep -q "break-system-packages"; then
    PIP_MODE="--break-system-packages"
fi

# ============================================================
#  ETAPE 7 - Dependances Python OBLIGATOIRES
# ============================================================

echo ""
echo -e "${B}[*] Installation des dependances Python obligatoires...${R}"
echo -e "${G}    requests, aiohttp, phonenumbers, pyautogui, pyperclip${R}"
echo ""

python3 -m pip install $PIP_MODE --upgrade \
    requests \
    aiohttp \
    phonenumbers \
    pyautogui \
    pyperclip

if [ $? -ne 0 ]; then
    echo -e "${RD}[!] Echec sur une dependance obligatoire.${R}"
    echo -e "${G}    Verifie ta connexion internet et relance.${R}"
    exit 1
fi
echo -e "${GR}[+] Dependances obligatoires installees.${R}"

# ============================================================
#  ETAPE 8 - Dependances Python OPTIONNELLES
# ============================================================

echo ""
echo -e "${B}[*] Installation des dependances optionnelles...${R}"
echo -e "${G}    selenium, mss, pynput, opencv-python, sounddevice, scipy,${R}"
echo -e "${G}    pycryptodome, bcrypt, curl_cffi, pillow, colorama${R}"
echo ""

python3 -m pip install $PIP_MODE --upgrade \
    selenium \
    mss \
    pynput \
    opencv-python \
    sounddevice \
    scipy \
    pycryptodome \
    bcrypt \
    curl_cffi \
    pillow \
    colorama

echo -e "${G}[i] Certains imports optionnels ont pu echouer (pas bloquant).${R}"

# ============================================================
#  ETAPE 9 - Verification des imports
# ============================================================

echo ""
echo -e "${B}[*] Verification des imports obligatoires...${R}"
python3 - <<'PYEOF'
try:
    import requests, aiohttp, phonenumbers, pyautogui, pyperclip
    print("\033[38;2;80;255;140m[+] Tous les imports obligatoires OK\033[0m")
except ImportError as e:
    print(f"\033[38;2;255;80;80m[!] Import manquant : {e}\033[0m")
    raise SystemExit(1)
PYEOF

if [ $? -ne 0 ]; then
    echo -e "${RD}[!] Un ou plusieurs imports obligatoires ont echoue.${R}"
    echo -e "${G}    Relance setup.sh ou installe manuellement.${R}"
    exit 1
fi

echo ""
echo -e "${B}[*] Verification des imports optionnels...${R}"
python3 - <<'PYEOF'
modules = ["selenium", "mss", "pynput", "cv2", "sounddevice", "scipy", "Crypto", "bcrypt"]
missing = []
for m in modules:
    try:
        __import__(m)
    except ImportError:
        missing.append(m)

if missing:
    print(f"\033[38;2;255;200;80m[i] Optionnels manquants : {', '.join(missing)}\033[0m")
    print("\033[38;2;80;145;190m    Les options concernees afficheront un message dans le tool.\033[0m")
else:
    print("\033[38;2;80;255;140m[+] Tous les imports optionnels OK\033[0m")
PYEOF

# ============================================================
#  ETAPE 10 - Resultat final
# ============================================================

echo ""
echo -e "${C}============================================================${R}"
echo -e "${C}                    SETUP TERMINE${R}"
echo -e "${C}============================================================${R}"
echo ""
echo -e "${GR}  Tout est installe. Pour lancer le tool :${R}"
echo ""
echo -e "${C}      python3 mytool.py${R}"
echo ""
echo -e "${G}  Note : les builders (options 8-14) produisent des binaires${R}"
echo -e "${G}         Linux, pas des .exe Windows. Pour cibler Windows,${R}"
echo -e "${G}         lance mytool.py depuis une machine Windows.${R}"
echo ""
echo -e "${C}============================================================${R}"
echo ""