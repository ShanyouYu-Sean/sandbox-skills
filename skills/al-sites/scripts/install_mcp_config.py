#!/usr/bin/env python3
"""Install the AL Sites MCP config into Codex config.toml."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path


SERVER_NAME = "k8s_e2b_sites"
MCP_URL = "https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/mcp"
HEALTH_URL = "https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/healthz"
READY_PROMPT = (
    "AL Sites MCP has been installed and SSO login has completed. "
    "Check whether the k8s_e2b_sites MCP tools are available in this new session. "
    "Do not create or deploy a site unless I ask."
)

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


def verify_health() -> None:
    with urllib.request.urlopen(HEALTH_URL, timeout=15) as response:
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"health check failed with HTTP {response.status}")
    print(f"Health check passed: {HEALTH_URL}")


def open_ready_session() -> bool:
    query = urllib.parse.urlencode({"prompt": READY_PROMPT})
    url = f"codex://threads/new?{query}"
    if sys.platform == "darwin":
        opener = shutil.which("open")
        cmd = [opener, url] if opener else None
    elif os.name == "nt":
        os.startfile(url)  # type: ignore[attr-defined]
        return True
    else:
        opener = shutil.which("xdg-open")
        cmd = [opener, url] if opener else None
    if not cmd:
        print("Could not find a system URL opener. Open one new Codex session to discover the MCP tools.")
        return False
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        print("Opened a new Codex session to discover the MCP tools.")
        return True
    print("Could not open a new Codex session automatically. Open one new Codex session to discover the MCP tools.")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=default_config_path())
    parser.add_argument(
        "--login",
        dest="login",
        action="store_true",
        default=True,
        help="run `codex mcp login k8s_e2b_sites` after writing config (default)",
    )
    parser.add_argument(
        "--no-login",
        dest="login",
        action="store_false",
        help="only write config; do not start the Codex MCP OAuth login flow",
    )
    parser.add_argument(
        "--health-check",
        dest="health_check",
        action="store_true",
        default=True,
        help="verify the remote Sites MCP health endpoint after config (default)",
    )
    parser.add_argument(
        "--no-health-check",
        dest="health_check",
        action="store_false",
        help="skip the remote Sites MCP health check",
    )
    parser.add_argument(
        "--open-ready-session",
        dest="open_ready_session",
        action="store_true",
        default=True,
        help="open a new Codex session after login so MCP tools are discovered (default)",
    )
    parser.add_argument(
        "--no-open-ready-session",
        dest="open_ready_session",
        action="store_false",
        help="do not open a new Codex session after login",
    )
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
        print(f"Skipped OAuth login. To login later, run: codex mcp login {SERVER_NAME}")
    if args.health_check:
        verify_health()
    if args.login and args.open_ready_session:
        open_ready_session()
    else:
        print("Open one new Codex session after login so the MCP tools are discovered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
