---
name: al-sites
description: Use when installing, configuring, verifying, or using the AL Sites MCP from Codex, including remote Sites MCP setup, smoke-test site creation, static site preview, deployment, and share URL generation.
---

# AL Sites

Use this skill to connect Codex to the AL Sites MCP and then create, preview,
deploy, or share Sites projects.

## Endpoints

MCP endpoint:

```text
https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/mcp
```

Health endpoint:

```text
https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/healthz
```

## Install Or Repair Config

When the user asks to install, configure, or use Sites MCP, run the bundled
installer with OAuth login:

```bash
python3 <skill-dir>/scripts/install_mcp_config.py --login
```

Resolve `<skill-dir>` to the directory containing this `SKILL.md`. The script
updates `~/.codex/config.toml` idempotently with:

```toml
[mcp_servers.k8s_e2b_sites]
enabled = true
url = "https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/mcp"
startup_timeout_sec = 20
tool_timeout_sec = 300
default_tools_approval_mode = "approve"
```

The `--login` flag runs `codex mcp login k8s_e2b_sites`, which uses Codex's
native MCP OAuth flow. The browser redirects through Bytedance SSO and Codex
stores the resulting credential locally. Do not ask the user to copy tokens,
export environment variables, or paste secrets into chat.

After changing MCP config, tell the user to restart Codex or open a new session
only if this session does not show the `k8s_e2b_sites` MCP tools. If MCP loading
fails with an unauthorized error, run `codex mcp login k8s_e2b_sites` again.

## Verify Reachability

Run:

```bash
curl -sS https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/healthz
```

Expect JSON with `ok: true`. If health fails, report the HTTP/network error and
do not continue to a smoke test.

## Use The MCP

If the Sites MCP tools are available in the current session, use them directly.
For a smoke test:

1. Call `site_create` with name `codex-smoke-site`.
2. Call `site_write_files` for `/workspace/index.html` with a minimal HTML page.
3. Call `site_start_dev` for a preview, or `site_deploy` for a share URL.
4. Return the preview or share URL and any required headers.

If the tools are not available, do not fake a tool call. Configure the MCP,
verify `/healthz`, run `codex mcp login k8s_e2b_sites` if auth is missing, and
tell the user to restart or open a new session only if tools still are not
loaded after login.

Never put API keys or bearer tokens in tool arguments, config, logs, or final
output.
