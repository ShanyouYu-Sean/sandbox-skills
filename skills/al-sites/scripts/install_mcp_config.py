#!/usr/bin/env python3
"""Install the AL Sites MCP config into Codex config.toml."""

from __future__ import annotations

import argparse
import os
import re
import webbrowser
from pathlib import Path


SERVER_NAME = "k8s_e2b_sites"
MCP_URL = "https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/mcp"
LOGIN_URL = "https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/auth/login?client=codex"

BLOCK = f"""[mcp_servers.{SERVER_NAME}]
enabled = true
url = "{MCP_URL}"
headers = {{ Authorization = "Bearer ${{AL_SITES_MCP_TOKEN}}" }}
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
    parser.add_argument("--no-open-login", action="store_true", help="print the Bytedance SSO login URL without opening it")
    args = parser.parse_args()

    changed = install_config(args.config)
    status = "updated" if changed else "already configured"
    print(f"{args.config}: {status}")
    print("Bytedance SSO login URL:")
    print(LOGIN_URL)
    if not args.no_open_login:
        if webbrowser.open(LOGIN_URL):
            print("Opened the Bytedance SSO login URL in your browser.")
        else:
            print("Could not open a browser automatically; open the URL above manually.")
    print("After login, export AL_SITES_MCP_TOKEN in the environment used by Codex.")
    print("Restart Codex or open a new session so the MCP server is loaded with the token.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
