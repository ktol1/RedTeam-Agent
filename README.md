<div align="center">

<img src="assets/banner.svg" alt="RedTeam-MCP Banner" width="800"/>

# 🔴 RedTeam-MCP

### AI-Powered Autonomous Red Team Framework via Model Context Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-Compatible-brightgreen.svg)](https://modelcontextprotocol.io)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg)](/)
[![Tools](https://img.shields.io/badge/Integrated_Tools-15+-orange.svg)](/)
[![Stars](https://img.shields.io/github/stars/ktol1/RedTeam-MCP?style=social)](https://github.com/ktol1/RedTeam-MCP)

**让 AI 像真正的渗透测试专家一样，自主规划攻击路径、调用安全工具、横向移动、域内提权。**

[English](#overview) · [快速开始](#-quick-start) · [工具列表](#-integrated-tools) · [架构](#-architecture) · [演示](#-demo)

</div>

---

## 📖 Overview

**RedTeam-MCP** 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 的红队自动化框架，将 **15+ 款主流渗透测试工具** 封装为 AI 可调用的标准化接口。

通过它，Claude / GPT / 任何 MCP 兼容 LLM 能够：

- 🔍 **自主发现资产** — 扫描网段、识别操作系统、枚举端口与服务
- 🌐 **Web 指纹识别** — 探测技术栈、中间件、CMS 版本
- 💥 **漏洞精准验证** — 基于模板的 CVE/RCE/SQLi 检测
- 🏰 **Active Directory 攻击** — Kerberoasting / AS-REP Roasting / DCSync / 委派攻击
- 🔀 **横向移动** — Pass-the-Hash / WMI 执行 / SMB 中继
- 📊 **自动化报告** — AI 汇总所有发现并生成攻击链分析

> **⚠️ Disclaimer**: This tool is for authorized security testing and educational purposes only. Always obtain proper authorization before testing.

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🤖 AI-Native Design
- 所有工具以 MCP Tool 协议暴露，AI 可直接调用
- 内置超时保护、输出截断、错误恢复
- 非交互式执行，无密码提示阻塞风险

</td>
<td width="50%">

### ⚡ Zero-Config Setup
- 一键安装脚本：二进制工具 + Python 包全自动
- 无需 Nmap/Npcap 驱动依赖
- Windows 原生支持，开箱即用

</td>
</tr>
<tr>
<td width="50%">

### 🔧 15+ Integrated Tools
- Go 高性能引擎：gogo / fscan / httpx / nuclei / ffuf / dnsx / kerbrute
- Python 域渗透：Impacket 全套 / NetExec (nxc) / BloodHound
- 内置原生端口扫描器替代 Nmap

</td>
<td width="50%">

### 🧠 Agent Skill System
- 附带 `.github/skills/redteam/SKILL.md` 知识库
- 指导 AI 正确使用每个工具的参数和最佳实践
- 渐进式探测工作流：发现 → 指纹 → 漏洞验证

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11** (x64)
- **Python 3.10+**
- Internet connection (for tool download)

### Step 1: Clone & Install

```bash
git clone https://github.com/ktol1/RedTeam-MCP.git
cd RedTeam-MCP

# Create virtual environment
cd redteam-server
python -m venv venv
venv\Scripts\activate.bat

# Install Python dependencies
pip install -r requirements.txt

# One-click download all binary tools + Python packages
python install_tools.py
```

### Step 2: Add `redteam-tools` to PATH

Add `D:\mcp\redteam-tools` (or your actual path) to the system `PATH` environment variable.

### Step 3: Connect to AI Client

<details>
<summary><b>VS Code (Cline / Roo Code)</b></summary>

Add to your MCP Server configuration:
```json
{
  "mcpServers": {
    "RedTeam": {
      "command": "path/to/venv/Scripts/python.exe",
      "args": ["path/to/redteam-server/server.py"]
    }
  }
}
```
</details>

<details>
<summary><b>Claude Desktop</b></summary>

Edit `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "RedTeam": {
      "command": "path/to/venv/Scripts/python.exe",
      "args": ["path/to/redteam-server/server.py"]
    }
  }
}
```
</details>

<details>
<summary><b>Cursor IDE</b></summary>

Settings → Features → MCP Servers → Add:
- **Type**: `command`
- **Name**: `RedTeam`
- **Command**: `path/to/venv/Scripts/python.exe path/to/redteam-server/server.py`
</details>

### Step 4: Test

```bash
# Start MCP Inspector for debugging
mcp dev server.py
```

Then tell your AI: *"Scan the 192.168.1.0/24 network for live Windows hosts and identify open services."*

---

## 🔧 Integrated Tools

| Category | Tool | Description |
|----------|------|-------------|
| 🔍 Asset Discovery | **[gogo](https://github.com/chainreactors/gogo)** | Ultra-fast port scanning & protocol fingerprinting |
| 🔍 Asset Discovery | **[fscan](https://github.com/shadow1ng/fscan)** | All-in-one intranet scanner (ports, vuln, brute-force) |
| 🌐 Web Recon | **[httpx](https://github.com/projectdiscovery/httpx)** | HTTP probing, tech detection, title extraction |
| 💥 Vuln Scanning | **[nuclei](https://github.com/projectdiscovery/nuclei)** | Template-based vulnerability scanner (CVE/RCE/SQLi) |
| 📂 Fuzzing | **[ffuf](https://github.com/ffuf/ffuf)** | Web directory & VHost brute-forcer |
| 🌍 DNS | **[dnsx](https://github.com/projectdiscovery/dnsx)** | DNS resolution & subdomain enumeration |
| 🔑 Kerberos | **[kerbrute](https://github.com/ropnop/kerbrute)** | Kerberos user enumeration & password spraying |
| 🏰 AD Attack | **[Impacket](https://github.com/fortra/impacket)** | wmiexec / psexec / secretsdump / getST / ntlmrelayx |
| 🔀 Lateral Movement | **[NetExec (nxc)](https://github.com/Pennyw0rth/NetExec)** | Multi-protocol pentest framework (SMB/WinRM/LDAP...) |
| 🗺️ AD Mapping | **[BloodHound.py](https://github.com/dirkjanm/BloodHound.py)** | Active Directory privilege path collection |
| 📡 Port Scan | **Built-in** | Native async Python port scanner (no Npcap needed) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   AI Agent (LLM)                        │
│            Claude / GPT / Any MCP Client                │
└──────────────────────┬──────────────────────────────────┘
                       │ MCP Protocol (stdio)
                       ▼
┌─────────────────────────────────────────────────────────┐
│               redteam-server/server.py                  │
│                  FastMCP Server                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │invoke_   │ │invoke_   │ │invoke_   │ │invoke_    │  │
│  │gogo()    │ │fscan()   │ │nuclei()  │ │dcsync()   │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └─────┬─────┘  │
│       │  async subprocess + timeout protection  │       │
└───────┼─────────────┼───────────┼───────────────┼───────┘
        ▼             ▼           ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                  redteam-tools/                          │
│   gogo.exe  fscan.exe  httpx.exe  nuclei.exe  ffuf.exe  │
│   dnsx.exe  kerbrute.exe  nxc.exe                       │
│   + impacket-* (Python entry points)                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Demo

### Example: Autonomous Network Penetration

```
User: "Scan 10.10.26.0/24, find all Windows hosts, check for vulnerabilities."

AI Agent Execution Plan:
  1. gogo -i 10.10.26.0/24 -p win -v -q     → Found 4 Windows hosts
  2. httpx → Web services on :80, :8080       → Identified IIS, Tomcat
  3. nuclei -as -s critical,high              → CVE-2024-XXXX confirmed
  4. nxc smb ... --shares                     → Writable share found
  5. Report: Complete attack chain documented
```

### Example: Active Directory Attack Chain

```
User: "We have credentials user:pass for corp.local. Find a path to Domain Admin."

AI Agent:
  1. bloodhound-python -c All                → Collected AD graph
  2. kerbrute userenum                        → 47 valid users discovered
  3. GetUserSPNs.py (Kerberoast)             → 3 SPN hashes captured  
  4. Cracked svc_backup hash → DA privileges via backup operator
  5. secretsdump.py -just-dc                  → Full domain hash dump
```

---

## 📁 Project Structure

```
RedTeam-MCP/
├── 📄 README.md                    # This file
├── 📄 LICENSE                      # MIT License
├── 📂 .github/
│   └── 📂 skills/redteam/
│       └── 📄 SKILL.md            # AI Agent knowledge base (tool usage guide)
├── 📂 redteam-server/
│   ├── 📄 server.py               # MCP Server (all tool wrappers)
│   ├── 📄 install_tools.py        # One-click tool installer
│   ├── 📄 requirements.txt        # Python dependencies
│   └── 📄 README.md               # Server-specific docs
├── 📂 redteam-tools/              # Binary tools directory (auto-populated)
│   ├── gogo.exe
│   ├── fscan.exe
│   ├── httpx.exe
│   ├── nuclei.exe
│   ├── ffuf.exe
│   ├── dnsx.exe
│   ├── kerbrute.exe
│   └── nxc.exe
└── 📂 assets/
    └── banner.svg                  # Project banner image
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Built with ❤️ for the Security Community**

*RedTeam-MCP — Where AI Meets Offensive Security*

</div>
