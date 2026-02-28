import os
import urllib.request
import json
import zipfile
import shutil

TOOLS_DIR = r"d:\mcp\redteam-tools"

# 需下载的 Go 语言编写的核心工具列表与仓库
TOOLS_LIST = {
    "fscan": "shadow1ng/fscan",
    "gogo": "chainreactors/gogo",
    "httpx": "projectdiscovery/httpx",
    "nuclei": "projectdiscovery/nuclei",
    "ffuf": "ffuf/ffuf",
    "dnsx": "projectdiscovery/dnsx",
    "kerbrute": "ropnop/kerbrute",
    "nxc": "Pennyw0rth/NetExec"
}

def download_and_extract_latest(repo, tool_name):
    print(f"\n[*] 正在准备安装 {tool_name} (来自 {repo})...")
    
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(api_url)
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"[!] 无法拉取 {repo} 的最新发布数据: {e}")
        return

    # 寻找匹配的资源
    target_url = None
    is_zip = False
    
    for asset in data.get('assets', []):
        name = asset['name'].lower()
        # 跳过非 64位 x86 架构
        if "arm" in name or "386" in name or "x86" in name.replace("x86_64", ""):
            continue
            
        if "windows" in name or "64.exe" in name or name.endswith(".exe"):
            if name.endswith(".zip"):
                target_url = asset['browser_download_url']
                is_zip = True
                break
            elif name.endswith(".exe"):
                # 如果有直接的 exe，我们优先拿 zip，如果没有 zip 就拿 exe
                target_url = asset['browser_download_url']
                is_zip = False
                
    if not target_url:
        print(f"[!] 没有找到适用于 Windows 64位的发布文件，跳过。")
        return

    temp_path = os.path.join(TOOLS_DIR, f"{tool_name}_temp" + (".zip" if is_zip else ".exe"))
    
    print(f"[-] 正在从 Github 拉取文件: {target_url}")
    try:
        # 添加 User-Agent 防止被 API 或 CDN 拦截
        req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(temp_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        print(f"[!] 下载失败: {e}")
        return

    # 解压并提取 exe
    if is_zip:
        print(f"[-] 正在解压至 {TOOLS_DIR}")
        try:
            with zipfile.ZipFile(temp_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if member.endswith(".exe"):
                        source = zip_ref.open(member)
                        target = open(os.path.join(TOOLS_DIR, f"{tool_name}.exe"), "wb")
                        with source, target:
                            shutil.copyfileobj(source, target)
            os.remove(temp_path)
            print(f"[+] {tool_name} 安装成功！")
        except Exception as e:
            print(f"[!] 解压发生错误: {e}")
    else:
        # 直接重命名为标准的 tool_name.exe
        target_exe = os.path.join(TOOLS_DIR, f"{tool_name}.exe")
        os.replace(temp_path, target_exe)
        print(f"[+] {tool_name} 安装成功！可执行文件已就位。")

# 需通过 pip 安装的 Python 工具包
PYTHON_PACKAGES = [
    "impacket",           # wmiexec / psexec / secretsdump / GetNPUsers / GetUserSPNs / getST / ntlmrelayx
    "bloodhound",         # bloodhound-python：AD 权限图谱收集
    "netexec",            # nxc：内网横向渗透控制台（pip 版，补充 exe 版）
    "playwright",         # Playwright 无头浏览器：动态页面信息读取
]

def install_python_packages():
    import subprocess
    import sys
    print("\n" + "="*50)
    print("安装 Python 渗透工具包 (impacket / bloodhound / netexec)")
    print("="*50)
    for pkg in PYTHON_PACKAGES:
        print(f"\n[*] 正在安装 Python 包: {pkg} ...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--upgrade", "-q"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"[+] {pkg} 安装/升级成功")
        else:
            print(f"[!] {pkg} 安装失败:\n{result.stderr.strip()}")

    # 验证 impacket 入口点可用
    print("\n[*] 验证 impacket 入口点...")
    result = subprocess.run(
        ["impacket-wmiexec", "--help"],
        capture_output=True, text=True
    )
    if result.returncode == 0 or "usage" in (result.stdout + result.stderr).lower():
        print("[+] impacket 入口点 (impacket-wmiexec) 可用")
    else:
        print("[~] impacket 入口点不在 PATH，将使用 python -m impacket.examples.* 调用")

    # 安装 Playwright 浏览器引擎
    print("\n[*] 安装 Playwright Chromium 浏览器引擎...")
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("[+] Playwright Chromium 浏览器引擎安装成功")
    else:
        print(f"[!] Playwright 浏览器安装失败:\n{result.stderr.strip()}")


if __name__ == "__main__":
    if not os.path.exists(TOOLS_DIR):
        print(f"[*] 创建工具统一存放目录: {TOOLS_DIR}")
        os.makedirs(TOOLS_DIR)
        
    print("="*50)
    print("RedTeam-MCP 依赖工具自动化部署脚本")
    print("="*50)
    
    for tool_name, repo in TOOLS_LIST.items():
        download_and_extract_latest(repo, tool_name)

    install_python_packages()

    print("\n" + "="*50)
    print("[+] 所有工具安装完成，与 SKILL.md 配置已对齐")
    print("    二进制工具目录:", TOOLS_DIR)
    print("    Python 工具通过 impacket-* / nxc / bloodhound-python 命令调用")
    print("="*50)
        
    print("\n" + "="*50)
    print("[完成] 所有核心二进制引擎已处理完毕！")
    print(f"[*] 提示：记得将 {TOOLS_DIR} 添加到 Windows 的系统 PATH 环境变量中哦！")
    print("="*50)