# Sandbox Skills

Public Codex skills for AL sandbox workflows.

## AL Sites

Install the AL Sites skill from `skills/al-sites`.

```text
从 git@github.com:ShanyouYu-Sean/sandbox-skills.git 的 skills/al-sites 安装 al-sites skill
```

The skill configures the remote AL Sites MCP endpoint and uses Codex's native MCP OAuth flow. Run `codex mcp login k8s_e2b_sites` when prompted; Codex opens Bytedance SSO and stores the MCP credential locally. No token copy/export step is required.
