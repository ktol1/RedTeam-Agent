# Repository Instructions

This repository uses Skill-first terminal workflows.

## Preferred execution model

- Do not use MCP tool wrappers from `redteam-server/server.py`.
- Prefer direct terminal execution of binaries in `d:\mcp\redteam-tools`.
- Load and follow the `redteam` skill before launching red-team commands.

## Tool location

- Primary directory: `d:\mcp\redteam-tools`
- Use absolute paths when command resolution fails.

## Output discipline

- For long scan output, write results to files first.
- Summarize high-signal findings only: hosts, ports, services, vulnerabilities, creds.

## Safety and reliability

- Use non-interactive command forms.
- If arguments are uncertain, read local help files in `d:\mcp\redteam-tools\*_help.txt` before retrying.
