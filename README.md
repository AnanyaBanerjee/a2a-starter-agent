# A2A Starter Agent

A minimal [A2A protocol](https://a2aproject.github.io/A2A/) agent, backed by an LLM of your choice. Deploy it on Railway, paste the resulting URL into any A2A client (e.g. [AgentChat Hub](https://agent-chat-hub.com)), and start chatting.

## What it does

- `GET /.well-known/agent.json` — serves the agent card
- `POST /a2a` — handles `message/send` (JSON-RPC 2.0), replies using the LLM you configure

## Choosing a provider

| Provider | `LLM_PROVIDER` | `BASE_URL` | `MODEL` (example) |
|---|---|---|---|
| Anthropic (Claude) | `anthropic` | *(leave blank)* | `claude-sonnet-4-5` |
| OpenAI | `custom` | `https://api.openai.com/v1` | `gpt-4o` |
| xAI (Grok) | `custom` | `https://api.x.ai/v1` | `grok-4` |
| Moonshot (Kimi) | `custom` | `https://api.moonshot.ai/v1` | `kimi-k2` |
| DeepSeek | `custom` | `https://api.deepseek.com/v1` | `deepseek-chat` |
| Ollama / LM Studio | `custom` | your server's URL + `/v1` | whatever model you have pulled |

## Configuration

| Variable | Required | Description |
|---|---|---|
| `LLM_PROVIDER` | No | `anthropic` (default) or `custom` — see table above |
| `API_KEY` | Yes (except unauthenticated local servers) | Your LLM provider's API key |
| `MODEL` | No | Model id (default: `claude-sonnet-4-5` for Anthropic, `gpt-4o` otherwise) |
| `BASE_URL` | Only if `LLM_PROVIDER=custom` | Base URL of any OpenAI-compatible `/chat/completions` endpoint |
| `AGENT_NAME` | No | Display name shown in the agent card (default: "Starter Agent") |

## Local development

```bash
pip install -r requirements.txt
export API_KEY=sk-...
uvicorn main:app --reload
```
