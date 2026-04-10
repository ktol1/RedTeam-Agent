import os
import re

def process_file(path, func):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = func(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def fix_readme(content):
    content = content.replace('RedTeam-MCP', 'RedTeam-Agent')
    content = content.replace('[![MCP](https://img.shields.io/badge/MCP-Protocol-green?style=for-the-badge)](https://modelcontextprotocol.io/)', '[![Skill](https://img.shields.io/badge/Workflow-Skill--First-brightgreen?style=for-the-badge)](./.github/skills/redteam/SKILL.md)')
    content = content.replace('AI calls penetration tools directly via MCP', 'AI calls penetration tools directly via Skill + terminal')
    content = content.replace('通过 MCP 协议，AI 直接调用渗透工具', '通过 Skill + 终端，AI 直接调用渗透工具')
    content = content.replace('基于 **Model Context Protocol (MCP)**', '采用 **Skill-first 终端工作流**')
    content = content.replace('通过 MCP 协议，AI Agent', 'AI 读取项目 Skill 后，会自动识别工具并')
    content = content.replace('based on **Model Context Protocol (MCP)**. Through MCP, AI Agents can autonomously perform', 'now uses a **Skill-first terminal workflow**. AI reads the project skill, discovers tools, and executes commands directly in terminal to complete')
    return content

def fix_skill(content):
    content = content.replace('RedTeam-MCP', 'RedTeam-Agent')
    content = re.sub(r'description: RedTeam penetration testing agent skill.*', 'description: RedTeam physical terminal execution skill. ONLY run using run_in_terminal, NOT MCP. Use for network scan, lateral movement, etc.', content)
    content = re.sub(r'invoke_responder\(.*?\)', 'invoke_responder is NOT supported, manually run responder with nohup or Start-Job.', content)
    content = content.replace('MCP 工具', '终端工具')
    content = re.sub(r'invoke_misc\(.*?\)', 'run python -m impacket.examples...', content)
    content = content.replace('invoke_ntlmrelayx MCP Tool', '终端后台运行')
    content = content.replace('上传后执行的命令', '上传文件使用 scp 或终端 base64 echo 方式，再远程执行')
    content = content.replace('invoke_', 'impacket-')
    content = content.replace('调用 server.py', '调用终端二进制文')
    return content

def fix_general(content):
    content = content.replace('RedTeam-MCP', 'RedTeam-Agent')
    return content

process_file('README.md', fix_readme)
process_file('README_zh.md', fix_readme)
process_file('.github/skills/redteam/SKILL.md', fix_skill)
process_file('redteam-server/install_tools.py', fix_general)
process_file('redteam-server/install_tools_linux.py', fix_general)
