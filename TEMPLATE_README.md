# Deploy and Host A2A Starter Agent on Railway

A minimal [A2A protocol](https://a2aproject.github.io/A2A/) agent, backed by an LLM of your choice. Deploy it, paste the resulting URL into any A2A client (e.g. [AgentChat Hub](https://agent-chat-hub.com)), and start chatting immediately.

## About Hosting A2A Starter Agent

This template runs a small FastAPI server exposing the two endpoints an A2A client needs: `GET /.well-known/agent.json` (the agent card) and `POST /a2a` (JSON-RPC `message/send`). Incoming chat messages are forwarded to the LLM you configure — Anthropic by default, or any OpenAI-compatible `/chat/completions` endpoint (OpenAI, xAI, Moonshot, DeepSeek, Ollama, LM Studio, etc.) — and the reply is returned in A2A's message format. There's no database, no queue, and no other services — just one web process.

## Why Deploy A2A Starter Agent on Railway?

Railway lets you go from "I want an agent" to a live, publicly-reachable A2A endpoint in one deploy, with your own LLM API key and no infrastructure to manage — a public domain, HTTPS, and restarts are all handled for you.

## Common Use Cases

- A ready-to-chat starting point for anyone building or testing an A2A client
- A base to fork and extend with your own tools, prompts, or model
- A quick way to give any LLM-backed agent a public A2A endpoint

## Dependencies for A2A Starter Agent Hosting

### Deployment Dependencies

- An API key from your chosen LLM provider — required, set as the `API_KEY` variable
