# Install AL Sites Skill

Use this prompt with Codex or another local-shell agent that can install a skill from a GitHub repository.

Short version:

```text
从 git@github.com:ShanyouYu-Sean/sandbox-skills.git 安装 al-sites，并完成 MCP 配置和 SSO 授权
```

Full version:

```text
Install the AL Sites skill from this GitHub repository and finish bootstrap in this same session:

git@github.com:ShanyouYu-Sean/sandbox-skills.git

Use the skill in `skills/al-sites`. After installing it into my local Codex skill directory, do not wait for a new session to activate the skill. Directly run the installed script:

python3 "${CODEX_HOME:-$HOME/.codex}/skills/al-sites/scripts/install_mcp_config.py"

That script must configure the remote AL Sites MCP and run `codex mcp login k8s_e2b_sites` for Bytedance SSO. Then verify:

curl -sS https://sd8lskvf5a7a8tsp61g1g.apigateway-cn-beijing.volceapi.com/healthz

Do not write or print API keys or bearer tokens. After successful login and health check, tell me to open one new Codex session to use `k8s_e2b_sites` MCP tools; do not ask me to run another manual login command.
```
