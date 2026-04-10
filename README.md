# RedTeam-Agent

<div align="center">

<img src="assets/logo.png" alt="RedTeam-Agent" width="200"/>

### AI-Powered Autonomous Red Team Framework

**Let AI Become Your Security Audit Hacker**

[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge)](https://www.python.org/)
[![Skill](https://img.shields.io/badge/Workflow-Skill--First-brightgreen?style=for-the-badge)](./.github/skills/redteam/SKILL.md)
[![Stars](https://img.shields.io/github/stars/ktol1/RedTeam-Agent?style=for-the-badge)](https://github.com/ktol1/RedTeam-Agent/stargazers)

[English](./README.md) · [中文](./README_zh.md) · [Documentation](./.github/skills/redteam/SKILL.md) · [Quick Start](#-quick-start)

</div>

---

## 🎯 Overview

RedTeam-Agent is an AI-powered red team penetration testing framework now uses a **Skill-first terminal workflow**. AI reads the project skill, discovers tools, and executes commands directly in terminal to complete internal network penetration testing, Active Directory attacks, vulnerability exploitation, and other red team tasks.

> **Core Philosophy**: No manual operation required. AI takes over all penetration tools for truly automated security testing.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🚀 **Plug & Play** | 15+ tools auto-install, one-click Windows deployment |
| 🤖 **AI-Driven** | AI calls penetration tools directly via Skill + terminal |
| 💰 **Token Optimized** | Smart output compression, saves 80% tokens |
| 🛡️ **Full AD Coverage** | BloodHound + impacket + Responder full chain |
| 🌐 **Multi-Client** | Cursor, Claude Desktop, VS Code Cline |

---

## 🛠️ Tool Matrix

### Network Scanning

| Tool | Function | Use Case |
|------|----------|----------|
| [gogo](./.github/skills/redteam/SKILL.md#tool-1-gogo-fast-asset-probe) | Fast asset discovery | Internal host detection |
| [fscan](./.github/skills/redteam/SKILL.md#tool-2-fscan-comprehensive-scanner) | Comprehensive scanner | Port/vulnerability/weak password |

### Web Security

| Tool | Function | Use Case |
|------|----------|----------|
| [httpx](./.github/skills/redteam/SKILL.md#tool-3-httpx-web-fingerprinting) | Web fingerprinting | Tech stack identification |
| [nuclei](./.github/skills/redteam/SKILL.md#tool-4-nuclei-vulnerability-poc-scanner) | POC batch scanning | Known vulnerability detection |
| [ffuf](./.github/skills/redteam/SKILL.md#tool-5-ffuf-directory-fuzzing) | Directory fuzzing | Web directory brute force |

### Active Directory Attacks 🏆

| Tool | Function | Use Case |
|------|----------|----------|
| [SharpHound](./.github/skills/redteam/SKILL.md#tool-8-sharphound-ad-permission-graph-windows) | Windows collector | Domain data collection |
| [bloodhound-python](./.github/skills/redteam/SKILL.md#tool-7-bloodhound) | Cross-platform collector | Linux/macOS data collection |
| [GetNPUsers](./.github/skills/redteam/SKILL.md#impacket-getnpusersas-rep-roasting) | AS-REP Roast | Enumerate no-preauth users |
| [GetUserSPNs](./.github/skills/redteam/SKILL.md#impacket-getuserspnskerberoasting) | Kerberoasting | Request SPN ticket cracking |
| [secretsdump](./.github/skills/redteam/SKILL.md#impacket-secretsdump-lsass-dump) | LSASS Dump | Extract plaintext and hashes |
| [ntlmrelayx](./.github/skills/redteam/SKILL.md#impacket-ntlmrelayx) | NTLM Relay | Relay attacks |
| [pywerview](./.github/skills/redteam/SKILL.md#tool-9-powerview-domain-enumeration) | Domain enumeration | Users/computers/groups |
| [ldapdomaindump](./.github/skills/redteam/SKILL.md#tool-10-ldapdomaindump-ldap-domain-dump) | LDAP dump | Domain info snapshot |

### Lateral Movement

| Tool | Function | Use Case |
|------|----------|----------|
| [nxc](./.github/skills/redteam/SKILL.md#tool-6-netexec-nxc-lateral-movement) | NetExec | SMB/WinRM/SSH |
| [wmiexec](./.github/skills/redteam/SKILL.md#impacket-wmiexec) | WMI execution | Fileless lateral |
| [psexec](./.github/skills/redteam/SKILL.md#impacket-psexec) | PSEXEC | Service execution |

### Proxy & Credentials

| Tool | Function | Use Case |
|------|----------|----------|
| [chisel](./.github/skills/redteam/SKILL.md#proxy-automation-proxy-setup) | HTTP tunnel | Port forwarding |
| [responder](./.github/skills/redteam/SKILL.md#tool-11-responder-llmnrntbns-spoofing) | LLMNR spoofing | Hash collection |

---

## 🚀 Quick Start

### 1️⃣ Requirements

```
Python 3.8+
Windows 10/11 or Linux/macOS
8GB+ RAM (recommended)
```

### 2️⃣ Installation

```bash
# Clone repository
git clone https://github.com/ktol1/RedTeam-Agent.git
cd RedTeam-Agent/redteam-server

# Create virtual environment
python -m venv venv

# Activate venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download binary tools (auto-downloads gogo, fscan, httpx, nuclei, etc.)
python install_tools.py
```

### 3️⃣ Configure MCP

#### Cursor IDE

Open `Settings` → `Features` → `MCP Servers` → `Add New Server`

```json
{
  "mcpServers": {
    "RedTeam-Agent": {
      "command": "D:\\RedTeam-Agent\\redteam-server\\venv\\Scripts\\python.exe",
      "args": ["D:\\RedTeam-Agent\\redteam-server\\server.py"]
    }
  }
}
```

#### Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "RedTeam-Agent": {
      "command": "D:\\RedTeam-Agent\\redteam-server\\venv\\Scripts\\python.exe",
      "args": ["D:\\RedTeam-Agent\\redteam-server\\server.py"]
    }
  }
}
```

### 4️⃣ Start Using

Tell your AI:

```
🎯 Scan 192.168.1.0/24, find all Windows hosts and identify open services

🎯 Use SharpHound to collect corp.local domain info, analyze attack paths

🎯 Set up chisel proxy on 192.168.1.100 to access 10.10.10.0/24 network

🎯 Perform Kerberoasting attack on 192.168.1.50
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│    ██████╗ ██████╗ ███████╗███╗   ███╗███████╗ ██████╗ ██╗    │
│    ██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔════╝██╔═══██╗██║    │
│    ██████╔╝██████╔╝███████╗██╔████╔██║█████╗  ██║   ██║██║    │
│    ██╔═══╝ ██╔══██╗╚════██║██║╚██╔╝██║██╔══╝  ██║   ██║╚═╝    │
│    ██║     ██║  ██║███████║██║ ╚═╝ ██║███████╗╚██████╔╝██╗    │
│    ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝    │
│                                                                 │
│                    Model Context Protocol                        │
│                                                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │  Cursor   │   │  Claude  │   │  Cline   │
       │    IDE    │   │  Desktop │   │ (VS Code)│
       └──────────┘   └──────────┘   └──────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
    ┌─────────────────────┐       ┌─────────────────────┐
    │   MCP Server (Python)│       │   MCP Server (Node)│
    │                     │       │                     │
    │  ┌───────────────┐  │       │  ┌───────────────┐  │
    │  │   server.py   │  │       │  │ @playwright/mcp│  │
    │  │               │  │       │  │               │  │
    │  │ 17+ Tools     │  │       │  │ Browser       │  │
    │  │ Output Opt    │  │       │  │ Automation    │  │
    │  └───────────────┘  │       │  └───────────────┘  │
    └─────────────────────┘       └─────────────────────┘
              │
              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                     Tool Layer                              │
    │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │
    │  │  gogo  │ │  fscan  │ │  httpx  │ │ nuclei  │ │ Sharp  │  │
    │  └────────┘ └────────┘ └────────┘ └────────┘ │Hound.exe│  │
    │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ └────────┘  │
    │  │ nxc    │ │ chisel  │ │impacket │ │responder│            │
    │  └────────┘ └────────┘ └────────┘ └────────┘               │
    └─────────────────────────────────────────────────────────────┘
```

---

## 🎯 AD Attack Flow

```
     ┌─────────────────────────────────────────────────────────────────┐
     │                      Attack Flow                                 │
     └─────────────────────────────────────────────────────────────────┘

  ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
  │    Recon      │ ───► │   Collection  │ ───► │   Analysis    │
  └───────────────┘      └───────────────┘      └───────┬───────┘
         │                                               │
         ▼                                               ▼
  ┌───────────────┐                            ┌───────────────┐
  │ gogo/fscan    │                            │ BloodHound GUI│
  │ kerbrute      │                            │ attack_paths  │
  │ pywerview     │                            │ analysis.py  │
  └───────────────┘                            └───────────────┘
                                                        │
  ┌───────────────┐      ┌───────────────┐            │
  │    Attack     │ ◄─── │    Lateral    │ ◄─────────┘
  └───────────────┘      └───────────────┘
         │                       │
         ▼                       ▼
  ┌───────────────┐      ┌───────────────┐
  │ Kerberoast    │      │ nxc smb       │
  │ AS-REP Roast  │      │ wmiexec       │
  │ secretsdump   │      │ psexec        │
  │ ntlmrelayx    │      │ getST         │
  └───────────────┘      └───────────────┘
```

---

## 📦 MCP Tools

| # | Tool | Function | Command |
|---|------|----------|---------|
| 1 | `invoke_gogo` | Fast asset probe | `gogo -t 100 -iL hosts.txt` |
| 2 | `invoke_fscan` | Network scanner | `fscan -hf hosts.txt` |
| 3 | `invoke_httpx` | Web fingerprinting | `httpx -l urls.txt -title` |
| 4 | `invoke_nuclei` | POC scanner | `nuclei -l urls.txt -t vulnerabilities/` |
| 5 | `invoke_ffuf` | Directory fuzzing | `ffuf -w wordlist.txt -u URL/FUZZ` |
| 6 | `invoke_nxc` | Lateral movement | `nxc smb 192.168.1.0/24 -u user -p pass` |
| 7 | `invoke_kerbrute` | Kerberos enum | `kerbrute userenum -d domain users.txt` |
| 8 | `invoke_bloodhound_analysis` | BloodHound analysis | Parse JSON to attack report |
| 9 | `invoke_powerview` | Domain enum | `pywerview get-domain-user` |
| 10 | `invoke_ldapdomaindump` | LDAP dump | `ldapdomaindump ldap://dc` |
| 11 | `invoke_responder` | LLMNR spoofing | `responder -I eth0` |
| 12 | `invoke_proxy_setup` | Proxy setup | chisel/nc/powershell |
| 13 | `invoke_playwright` | Browser automation | screenshot/form/scraping |
| 14 | `invoke_wmiexec` | WMI execution | impacket-wmiexec |
| 15 | `invoke_psexec` | PSEXEC | impacket-psexec |
| 16 | `invoke_secretsdump` | LSASS Dump | impacket-secretsdump |
| 17 | `invoke_ntlmrelayx` | NTLM Relay | impacket-ntlmrelayx |

---

## ⚡ Token Optimization

| Optimization | Description | Savings |
|-------------|-------------|---------|
| ANSI Removal | Strip terminal colors | ~15% |
| Whitespace | Merge blank lines | ~10% |
| Truncation | Max 8000 chars | ~50% |
| Progress Filter | Remove progress bars | ~20% |
| **Total** | | **~80%** |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [SKILL.md](./.github/skills/redteam/SKILL.md) | Complete tool docs for AI agents |
| [redteam-server/README.md](./redteam-server/README.md) | Server deployment guide |

---

## 🤝 Contributing

Issues and Pull Requests welcome!

[![Stars](https://img.shields.io/github/stars/ktol1/RedTeam-Agent?style=social)](https://github.com/ktol1/RedTeam-Agent)
[![Forks](https://img.shields.io/github/forks/ktol1/RedTeam-Agent?style=social)](https://github.com/ktol1/RedTeam-Agent)

---

<div align="center">

**MIT License** · Copyright © 2024-2026 **ktol1**

**If you find this useful, give it a ⭐ Star!**

</div>
