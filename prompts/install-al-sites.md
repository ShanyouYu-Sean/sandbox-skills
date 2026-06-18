# Install AL Sites Skill

Use this prompt with Codex or another local-shell agent that can install a skill from a GitHub repository.

```text
Install the AL Sites skill from this GitHub repository:

git@github.com:ShanyouYu-Sean/sandbox-skills.git

Use the skill in `skills/al-sites`. After installing it, run the bundled installer to configure the remote AL Sites MCP, complete `codex mcp login k8s_e2b_sites`, verify the health endpoint, and tell me whether I need to restart Codex or open a new session before using the MCP tools. Do not write or print API keys or bearer tokens.
```
