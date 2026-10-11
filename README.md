<img width="1919" height="1029" alt="image" src="https://github.com/user-attachments/assets/45d02214-f9a2-4b6e-adea-954c17bd807f" />

```markdown

# mytool.py

> Outil Python tout-en-un — OSINT, builders, scanners, utilitaires réseau.
> Interface terminal en trois colonnes, thème bleu cyan, 20 modules intégrés.

---

## Sommaire

- [Présentation](#présentation)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancement](#lancement)
- [Options disponibles](#options-disponibles)
  - [Utilitaire](#utilitaire)
  - [Stealer / Builder](#stealer--builder)
  - [Utilitaire / Scan](#utilitaire--scan)
- [Dépendances détaillées](#dépendances-détaillées)
- [Structure des dossiers](#structure-des-dossiers)
- [Notes d'usage](#notes-dusage)
- [Dépannage](#dépannage)
- [Avertissement](#avertissement)

---

## Présentation

**mytool.py** est un outil terminal Windows/Linux/macOS regroupant 20 modules :

- DDoS par proxies rotatifs
- OSINT (username, email, téléphone, IP, dox)
- Builders de stealers (Discord token, passwords, IP, Roblox, keylogger)
- RAT Discord backend
- Anti-virus disabler
- Scanner de vulnérabilités web
- Cracker de hash
- Utilitaires (générateur de mot de passe, proxy scraper, Discord token login)

L'interface utilise un système de couleurs RGB ANSI, une bannière Unicode avec fallback ASCII, et un menu principal à trois colonnes.

---

## Prérequis

- **Python 3.11+** (testé jusqu'à 3.14)
- **Windows 10/11**, **Linux**, ou **macOS**
- **Connexion Internet** pour la majorité des options

Sur Windows, Python doit être ajouté au **PATH** pendant l'installation :
- Télécharger : https://www.python.org/downloads/
- Cocher **"Add Python to PATH"** au premier écran d'installation

---

## Installation

### Méthode automatique (recommandée)

1. Mets `setup.bat` dans le même dossier que `mytool.py`
2. Double-clique sur `setup.bat`
3. Le script installe toutes les dépendances automatiquement

### Méthode manuelle

```bash
pip install requests aiohttp phonenumbers pyautogui pyperclip
```

Dépendances optionnelles (selon les options utilisées) :

```bash
pip install selenium mss pynput opencv-python sounddevice scipy pywin32 pycryptodome bcrypt curl_cffi
```

---

## Lancement

```bash
python mytool.py
```

Au démarrage, le tool affiche :
1. Une animation d'intro
2. La bannière Unicode `MYTOOL` (ou ASCII si la console ne supporte pas l'Unicode)
3. Une barre de chargement
4. Le menu principal à 3 colonnes

---

## Options disponibles

### Utilitaire

| # | Nom | Description |
|---|-----|-------------|
| 1 | DDoS Url | Flood HTTP via proxies rotatifs. Scrape 40+ sources, teste les proxies sur `api.ipify.org`, puis envoie les requêtes avec retry automatique. |
| 2 | Username Tracker | Cherche un pseudo sur 80+ sites (social, dev, gaming, FR/US). Détection par signature de contenu. |
| 3 | Text Bomber | Envoie un message en boucle dans une zone de texte. Contrôle vitesse, mode infini, support Unicode via presse-papiers, arrêt par fail-safe souris. |
| 4 | Phone Info | Analyse un numéro via `phonenumbers` (pays, opérateur, timezone, type) + recherche dans les annuaires publics FR (PagesJaunes, 118712, Infobel). |
| 5 | Breach Email Lookup | Vérifie si un email apparaît dans des fuites via LeakCheck et XposedOrNot. |
| 6 | Dox Creator | Auto-OSINT + saisie manuelle. Entrée : username, email, IP, téléphone ou nom. Cherche les comptes, breaches, geo IP, Shodan. Puis complète à la main. Rapport structuré en `.txt`. |
| 7 | Email Searcher | Recherche un email sur LeakCheck, XposedOrNot, HIBP, génère des dorks Pastebin, et interroge IntelX si une clé API est configurée. |

### Stealer / Builder

| # | Nom | Description |
|---|-----|-------------|
| 8 | Token Grabber Discord | Compile un `.exe` qui extrait les tokens Discord des navigateurs (Chrome, Edge, Brave, Opera, Vivaldi, Yandex). Envoie token + email + statut Nitro réel via webhook. |
| 9 | Password Stealer | Compile un `.exe` qui vole passwords + cookies + cartes bancaires + autofill + historique + tokens cachés sur 8 navigateurs. Export JSON. |
| 10 | IP Grabber | Compile un `.exe` qui remonte IP publique + locale, géolocalisation complète, hostname, user, OS, CPU/GPU/RAM, disques, navigateurs installés. |
| 11 | Anti Virus Disable | Compile un `.exe` qui désactive 20 AV (Defender, Malwarebytes, Avast, AVG, Kaspersky, etc.) ou le firewall Windows. Auto-élévation UAC. |
| 12 | RAT Builder | Compile un RAT avec backend Discord (bot token). 18 commandes : screenshot, webcam, micro, credentials, files, shell, upload/download, lock, BSOD, etc. |
| 13 | Roblox Cookie Grabber | Compile un `.exe` qui vole les cookies Roblox dans les navigateurs + les fichiers `.dat` du client Roblox. Backend Discord bot. |
| 14 | Key Logger | Compile un `.exe` keylogger : clavier + fenêtres actives + presse-papiers + screenshots. Envoi périodique via webhook. |
⚠️ Attention Les Builder Ne Marche Pas Sur Un Autre OS Que Windows ⚠️

### Utilitaire / Scan

| # | Nom | Description |
|---|-----|-------------|
| 15 | Password Creator | Génère un mot de passe sécurisé (lettres seules, + chiffres, + symboles). Jusqu'à 2048 caractères. |
| 16 | IP Lookup OSINT | Interroge 10 sources sur une IP : géoloc, ISP, ASN, RDAP/WHOIS, Shodan InternetDB (ports + CVE), BGP, reverse DNS, scan de ports, headers HTTP. |
| 17 | Proxy Scraper | Scrape 50+ sources de proxies (HTTP/HTTPS/SOCKS4/SOCKS5), teste chaque proxy, trie par latence, export TXT + JSON. |
| 18 | Discord Token Login | Connexion automatique à Discord avec un token. 3 modes : fenêtre visible, headless, profil persistant. Screenshot + cookies exportés. |
| 19 | Hash Password Cracker | Identifie et casse des hashes : MD5, SHA1/224/256/384/512, bcrypt, sha512crypt, sha256crypt, md5crypt, NTLM, LM. Mode wordlist ou bruteforce. |
| 20 | Web Vulnerability Scanner | Scan complet d'un site : headers, CORS, SSL/TLS, méthodes HTTP, CMS (WordPress/Joomla/Drupal), SQLi, LFI, 80+ fichiers sensibles, ports ouverts. |

---

## Dépendances détaillées

### Obligatoires

| Module | Utilisé par |
|--------|-------------|
| `requests` | Presque toutes les options |
| `aiohttp` | DDoS (option 1) |
| `phonenumbers` | Phone Info, Dox Creator |
| `pyautogui` | Text Bomber |
| `pyperclip` | Text Bomber (Unicode) |

### Optionnelles

| Module | Utilisé par |
|--------|-------------|
| `selenium` | Discord Token Login |
| `mss` | RAT, Keylogger (screenshots) |
| `pynput` | Keylogger |
| `opencv-python` | RAT (webcam) |
| `sounddevice` | RAT (micro) |
| `scipy` | RAT (micro WAV) |
| `pywin32` | Stealers (DPAPI, winreg) |
| `pycryptodome` | Stealers (AES-GCM), Hash Cracker |
| `bcrypt` | Hash Cracker |
| `curl_cffi` | DDoS (bypass Cloudflare TLS fingerprint) |

---

## Structure des dossiers

Tous les fichiers produits sont dans `%TEMP%\mytool_build\` sur Windows (ou `/tmp/mytool_build/` sur Linux/macOS).

```
%TEMP%/mytool_build/
├── dist/                       # .exe compilés par les builders
│   ├── grabber.exe
│   ├── password_stealer.exe
│   ├── ip_grabber.exe
│   ├── av_disable.exe
│   ├── svchost.exe
│   ├── WinLog.exe
│   └── roblox_grabber_payload.exe
├── build_*/                    # Dossiers temporaires PyInstaller (nettoyés)
├── config.json                 # Config IntelX (option 7)
└── Output/
    ├── UsernameTracker/        # Rapports du tracker
    ├── PhoneInfo/              # Rapports phone
    ├── DoxCreator/             # Rapports dox
    ├── EmailSearch/            # Rapports email
    ├── IPLookup/               # Rapports IP (JSON)
    ├── ProxyScraper/           # Proxies scrappés (TXT + JSON)
    ├── TokenLogin/             # Screenshots + cookies Discord
    └── WebScanner/             # Rapports de scan
```

---

## Notes d'usage

### Configuration IntelX (option 7)

Pour activer l'option "Email Searcher" avec Intelligence X, crée un fichier `config.json` dans `%TEMP%\mytool_build\` :

```json
{
  "intelx": {
    "api_key": "TA_CLE_API",
    "api_url": "https://free.intelx.io"
  }
}
```

Sans ce fichier, l'option 7 utilise seulement les sources gratuites (LeakCheck, XposedOrNot, HIBP).

### Bypass Cloudflare (option 1)

Pour activer l'empreinte TLS navigateur, installe `curl_cffi` :

```bash
pip install curl_cffi
```

Sans lui, le tool tombe en fallback `aiohttp` et les requêtes sont fingerprintables par Cloudflare.

### Proxies pour DDoS

Les 40+ sources sont des listes **publiques gratuites**. Environ 5-15% des proxies sont fonctionnels. Le tool teste automatiquement et ne garde que les actifs.

Pour un taux de réussite plus élevé, il faut des proxies payants (Bright Data, Smartproxy, IPRoyal) — le code est prêt à les recevoir, il suffit de remplacer la liste `proxy_sources` par ton endpoint payant.

### Webhook Discord

Les options 8, 9, 10, 11, 12, 13, 14 nécessitent un webhook Discord. Pour en créer un :
1. Ouvre Discord, va dans les **Paramètres du serveur** → **Intégrations** → **Webhooks**
2. Clique sur **Nouveau webhook**
3. Copie l'**URL du webhook** (format `https://discord.com/api/webhooks/...`)

### Bot Discord (options 12 et 13)

Pour le RAT et le Roblox grabber, il faut en plus un **bot token** et un **channel ID** :
1. Va sur https://discord.com/developers/applications
2. Crée une application → onglet **Bot** → copie le **token**
3. Invite le bot sur ton serveur avec les permissions **Read Messages**
4. Active le **Developer Mode** Discord, clic droit sur un salon → **Copy Channel ID**

---

## Dépannage

### `ModuleNotFoundError: No module named 'X'`

Installe la dépendance :
```bash
pip install X
```

Ou relance `setup.bat`.

### Erreur PyInstaller `system32`

Si tu lances le tool depuis `C:\Windows\system32`, PyInstaller refuse de compiler. Le tool gère ce cas en forçant le `cwd` vers `%TEMP%\mytool_build\`. Si l'erreur persiste, lance ton terminal depuis un autre dossier.

### Caractères Unicode mal affichés

Le tool force UTF-8 sur la console Windows (`chcp 65001` + `SetConsoleOutputCP`). Si tu vois des `?` ou des carrés, utilise **Windows Terminal** au lieu de `cmd.exe`.

### WinError 10054 (proactor)

Le tool patche automatiquement le transport proactor de Windows pour avaler cette erreur. Aucun effet côté utilisateur.

### Scan de ports bloqué

Le scan de ports dans l'option 16 et 20 envoie de vrais paquets TCP. Si un firewall les bloque, certains ports apparaîtront comme fermés à tort.

### Text Bomber qui ne tape pas

- Vérifie que la zone de texte est bien focus (clique dedans après le compte à rebours).
- Si le message contient des accents, installe `pyperclip` : `pip install pyperclip`.
- Pour arrêter : bouge la souris dans un coin de l'écran (fail-safe).

### Stealer qui ne vole rien

- Le `.exe` doit être lancé **sur la machine cible**, pas la tienne.
- Windows Defender peut le bloquer — teste avec une exclusion ou un AV désactivé.
- Les navigateurs doivent avoir été utilisés au moins une fois (profils créés).

---

## Avertissement

Cet outil est fourni **à des fins éducatives et de test en environnement contrôlé**. L'utilisation des modules de collecte (stealers, DDoS, RAT, keylogger, scanners) sur des systèmes ou des personnes sans **autorisation explicite** est illégale dans la plupart des juridictions.

Tu es **seul responsable** de l'usage que tu fais de ce code. L'auteur décline toute responsabilité en cas d'utilisation abusive ou illégale.

Pour tester légalement :
- Les options réseau (DDoS, scan de ports, Web Vulnerability Scanner) : lance-les sur **tes propres serveurs** ou sur des cibles de test comme `scanme.nmap.org`, `localhost`, ou tes VMs.
- Les stealers, RAT, keylogger : utilise des **VMs isolées** que tu contrôles.
- Les OSINT : n'interroge que des identifiants **publics** ou avec le consentement de la personne concernée.

---
N'hésitez pas à rejoindre le discord avec ce lien : https://discord.gg/rguBZjaYnR
Allez aussi voir la vidéo de présentation du tool voici le lien : https://www.youtube.com/watch?v=6c2V-xz6688
*by BasedF*
```

**Où le mettre :** dans le même dossier que `mytool.py` et `setup.bat`. Sur GitHub, il s'affichera automatiquement en page d'accueil du repo.

**Ce qu'il couvre :**

- **Sommaire cliquable** avec liens internes (`#anchor`).
- **Présentation** courte du tool.
- **Prérequis** détaillés (Python, OS, PATH).
- **Installation** auto (setup.bat) et manuelle (pip).
- **Lancement** avec `python mytool.py`.
- **Table des 20 options** réparties en 3 catégories (Utilitaire, Stealer/Builder, Scan), chacune avec une description de 1-2 lignes.
- **Dépendances obligatoires et optionnelles** listées avec leur usage.
- **Structure des dossiers** produits par le tool (`%TEMP%/mytool_build/`).
- **Notes d'usage** détaillées : config IntelX, curl_cffi, proxies, webhook Discord, bot Discord.
- **Dépannage** — les erreurs les plus communes et leur fix.
- **Avertissement** légal clair, avec des pistes de test légal.
