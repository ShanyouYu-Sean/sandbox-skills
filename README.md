# Sandbox Skills

Public Codex skills for AL sandbox workflows.

## AL Sites

Ask Codex:

```text
帮我安装这个 skills https://github.com/ShanyouYu-Sean/sandbox-skills
```

The intended installer flow is:

1. Clone or download this repository.
2. Run `./install.sh` from the repository root.
3. Complete the browser-based Bytedance SSO flow opened by `codex mcp login`.
4. Use the new Codex session opened by the installer to let `k8s_e2b_sites` MCP tools load.

`install.sh` installs `skills/al-sites`, writes the Codex MCP config, runs MCP OAuth login, verifies the health endpoint, and opens a new Codex session for MCP discovery. No token copy/export step is required.
