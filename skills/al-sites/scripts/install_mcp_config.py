#!/usr/bin/env python3
"""Install the AL Sites MCP config into Codex config.toml."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path


SERVER_NAME = "k8s_e2b_sites"
MCP_URL = "https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/mcp"

BLOCK = f"""[mcp_servers.{SERVER_NAME}]
enabled = true
url = "{MCP_URL}"
startup_timeout_sec = 20
tool_timeout_sec = 300
default_tools_approval_mode = "approve"
"""


def default_config_path() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "config.toml"
    return Path.home() / ".codex" / "config.toml"


def install_config(path: Path) -> bool:
    path = path.expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    pattern = re.compile(rf"(?ms)^\[mcp_servers\.{re.escape(SERVER_NAME)}\]\n.*?(?=^\[|\Z)")
    if pattern.search(original):
        updated = pattern.sub(BLOCK.rstrip() + "\n\n", original).rstrip() + "\n"
    else:
        prefix = original.rstrip()
        updated = (prefix + "\n\n" if prefix else "") + BLOCK
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=default_config_path())
    parser.add_argument("--login", action="store_true", help="run `codex mcp login k8s_e2b_sites` after writing config")
    args = parser.parse_args()

    changed = install_config(args.config)
    status = "updated" if changed else "already configured"
    print(f"{args.config}: {status}")
    if args.login:
        codex = shutil.which("codex")
        if not codex:
            print("Codex CLI not found on PATH. Run `codex mcp login k8s_e2b_sites` once Codex CLI is available.")
            return 2
        subprocess.run([codex, "mcp", "login", SERVER_NAME], check=True)
        print(f"OAuth login completed for MCP server `{SERVER_NAME}`.")
    else:
        print(f"To login now, run: codex mcp login {SERVER_NAME}")
    print("Restart Codex or open a new session if this session does not show the MCP tools.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
