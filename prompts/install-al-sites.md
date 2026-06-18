# Install AL Sites Skill

Use this prompt with Codex or another local-shell agent that can install a skill from a GitHub repository.

Short version:

```text
帮我安装这个 skills https://github.com/ShanyouYu-Sean/sandbox-skills
```

Full version:

```text
Install the skills from this GitHub repository and finish AL Sites bootstrap in this same session:

https://github.com/ShanyouYu-Sean/sandbox-skills

Do not ask me which skill path to use. This repository's default skill is `skills/al-sites`.

Clone or download the repository, then run `./install.sh` from the repository root. The script installs `skills/al-sites` into my local Codex skill directory, writes the `k8s_e2b_sites` MCP config, runs `codex mcp login k8s_e2b_sites` for Bytedance SSO, verifies the health endpoint, and opens a new Codex session so MCP tools can be discovered.

Do not write or print API keys, bearer tokens, OAuth codes, or cookies. Do not ask me to run another manual login command. If opening the new Codex session fails, tell me to open one new Codex session manually.
```
