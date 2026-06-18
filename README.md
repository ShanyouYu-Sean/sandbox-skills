# Sandbox Skills

Public Codex skills for AL sandbox workflows.

## AL Sites

Install the AL Sites skill from `skills/al-sites`.

```text
从 git@github.com:ShanyouYu-Sean/sandbox-skills.git 安装 al-sites，并完成 MCP 配置和 SSO 授权
```

The install prompt should install `skills/al-sites`, then immediately run the installed `scripts/install_mcp_config.py` in the same session. The script configures the remote AL Sites MCP endpoint and starts Codex's native MCP OAuth flow with Bytedance SSO. No token copy/export step is required. After login, open one new Codex session to use the `k8s_e2b_sites` MCP tools.
