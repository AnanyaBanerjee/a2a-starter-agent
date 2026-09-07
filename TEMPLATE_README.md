# Deploy and Host A2A Starter Agent on Railway

A minimal [A2A protocol](https://a2aproject.github.io/A2A/) agent, backed by an LLM of your choice. Deploy it, paste the resulting URL into any A2A client (e.g. [AgentChat Hub](https://agent-chat-hub.com)), and start chatting immediately.

## Before You Deploy: Choose Your LLM Provider

Set these variables on the deploy screen based on the provider you want:

| Provider | `LLM_PROVIDER` | `BASE_URL` | `MODEL` (example) | Get an API key |
|---|---|---|---|---|
| Anthropic (Claude) | `anthropic` | *(leave blank)* | `claude-sonnet-4-5` | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| OpenAI | `custom` | `https://api.openai.com/v1` | `gpt-4o` | [platform.openai.com](https://platform.openai.com/api-keys) |
| xAI (Grok) | `custom` | `https://api.x.ai/v1` | `grok-4` | [console.x.ai](https://console.x.ai) |
| Moonshot (Kimi) | `custom` | `https://api.moonshot.ai/v1` | `kimi-k2` | [platform.moonshot.ai](https://platform.moonshot.ai/console/api-keys) |
| DeepSeek | `custom` | `https://api.deepseek.com/v1` | `deepseek-chat` | [platform.deepseek.com](https://platform.deepseek.com/api_keys) |
| Ollama / LM Studio (self-hosted) | `custom` | your server's URL, e.g. `http://your-host:11434/v1` | whatever model you have pulled | none needed — leave `API_KEY` blank |
| Any other OpenAI-compatible API | `custom` | that provider's base URL | that provider's model id | that provider's dashboard |

`API_KEY` is always required except for an unauthenticated local server. Everything else has a sensible default and can be left as-is.

## About Hosting A2A Starter Agent

This template runs a small FastAPI server exposing the two endpoints an A2A client needs: `GET /.well-known/agent.json` (the agent card) and `POST /a2a` (JSON-RPC `message/send`). Incoming chat messages are forwarded to the LLM you configure above, and the reply is returned in A2A's message format. There's no database, no queue, and no other services — just one web process.

## Why Deploy A2A Starter Agent on Railway?

Railway lets you go from "I want an agent" to a live, publicly-reachable A2A endpoint in one deploy, with your own LLM API key and no infrastructure to manage — a public domain, HTTPS, and restarts are all handled for you.

## Common Use Cases

- A ready-to-chat starting point for anyone building or testing an A2A client
- A base to fork and extend with your own tools, prompts, or model
- A quick way to give any LLM-backed agent a public A2A endpoint

## Dependencies for A2A Starter Agent Hosting

### Deployment Dependencies

- An API key from your chosen LLM provider (see the table above) — required, set as the `API_KEY` variable
