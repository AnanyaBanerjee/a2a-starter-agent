# A2A Starter Agent

A minimal [A2A protocol](https://a2aproject.github.io/A2A/) agent, backed by Claude. Deploy it on Railway, paste the resulting URL into any A2A client (e.g. [AgentChat Hub](https://agent-chat-hub.com)), and start chatting.

## What it does

- `GET /.well-known/agent.json` — serves the agent card
- `POST /a2a` — handles `message/send` (JSON-RPC 2.0), replies using Claude

## Configuration

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |
| `AGENT_NAME` | No | Display name shown in the agent card (default: "Starter Agent") |
| `AGENT_MODEL` | No | Claude model id (default: `claude-sonnet-4-5`) |

## Local development

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
uvicorn main:app --reload
```
