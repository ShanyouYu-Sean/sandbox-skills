# Sandbox Skills

Public Codex skills for AL sandbox workflows.

## AL Sites

Install the AL Sites skill from `skills/al-sites`.

```text
从 git@github.com:ShanyouYu-Sean/sandbox-skills.git 的 skills/al-sites 安装 al-sites skill
```

The skill configures the remote AL Sites MCP endpoint, opens or prints the Bytedance SSO login URL, and verifies the health endpoint. After login, export the returned `AL_SITES_MCP_TOKEN` in the environment used by Codex, then restart Codex or open a new session so the `k8s_e2b_sites` tools are loaded.
