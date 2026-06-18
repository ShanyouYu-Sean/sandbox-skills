# Sandbox Skills Install Guide

When a user asks to install this repository's skills from
`github.com/ShanyouYu-Sean/sandbox-skills`, do not ask which skill path to use.
Install `skills/al-sites` and finish bootstrap in the same session.

Preferred flow:

1. Clone or download this repository.
2. Run `./install.sh` from the repository root.
3. Let the script complete Codex MCP OAuth login through Bytedance SSO.
4. Do not print API keys, bearer tokens, OAuth codes, or cookies.
5. Tell the user that a new Codex session was opened, or that they should open
   one new Codex session if automatic opening failed.

The install script copies `skills/al-sites` into the local Codex skill
directory, writes the `k8s_e2b_sites` MCP config, runs
`codex mcp login k8s_e2b_sites`, verifies the health endpoint, and opens a new
Codex session so MCP tools can be discovered.
