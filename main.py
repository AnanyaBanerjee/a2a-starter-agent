"""Minimal A2A-protocol agent: proxies chat to an LLM you configure.

Implements just enough of the A2A spec (agent card + message/send) to work as
a one-click Railway-deployable starter agent for AgentChat Hub or any other
A2A client. No streaming, no task persistence, no extra services.

Supports Anthropic natively and any OpenAI-compatible chat-completions
endpoint (OpenAI, xAI, Moonshot, DeepSeek, Ollama, LM Studio, etc.) via
LLM_PROVIDER=custom + BASE_URL.
"""

import os
import uuid

import anthropic
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

AGENT_NAME = os.environ.get("AGENT_NAME", "Starter Agent")
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "anthropic")  # 'anthropic' | 'custom'
API_KEY = os.environ.get("API_KEY", "")
MODEL = os.environ.get("MODEL", "claude-sonnet-4-5" if LLM_PROVIDER == "anthropic" else "gpt-4o")
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")

anthropic_client = anthropic.Anthropic(api_key=API_KEY) if LLM_PROVIDER == "anthropic" else None


def _public_url(request: Request) -> str:
    # Railway terminates TLS in front of the app, so trust the forwarded proto/host.
    proto = request.headers.get("x-forwarded-proto", "https")
    host = request.headers.get("x-forwarded-host", request.headers.get("host", ""))
    return f"{proto}://{host}"


@app.get("/.well-known/agent.json")
def agent_card(request: Request):
    return {
        "name": AGENT_NAME,
        "description": "A minimal agent speaking the A2A protocol, backed by an LLM of your choice.",
        "url": _public_url(request),
        "version": "1.0.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "skills": [
            {
                "id": "chat",
                "name": "Chat",
                "description": "General-purpose conversation.",
                "examples": ["What can you help me with?"],
            }
        ],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
    }


def _extract_text(parts: list[dict]) -> str:
    return "\n".join(p.get("text", "") for p in parts if p.get("type") == "text").strip()


def _reply_anthropic(user_text: str) -> str:
    reply = anthropic_client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": user_text}],
    )
    return "".join(block.text for block in reply.content if block.type == "text")


def _reply_custom(user_text: str) -> str:
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    resp = httpx.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json={"model": MODEL, "messages": [{"role": "user", "content": user_text}]},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


@app.post("/a2a")
async def a2a(request: Request):
    body = await request.json()
    rpc_id = body.get("id")
    method = body.get("method")

    if method not in ("message/send", "message/stream"):
        return JSONResponse(
            {"jsonrpc": "2.0", "id": rpc_id, "error": {"code": -32601, "message": "Method not found"}},
            status_code=400,
        )

    user_text = _extract_text(body["params"]["message"].get("parts", []))
    reply_text = _reply_anthropic(user_text) if LLM_PROVIDER == "anthropic" else _reply_custom(user_text)

    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "result": {
            "status": {
                "state": "completed",
                "message": {
                    "role": "agent",
                    "messageId": str(uuid.uuid4()),
                    "parts": [{"type": "text", "text": reply_text}],
                },
            },
            "artifacts": [],
        },
    }
