"""Minimal A2A-protocol agent: proxies chat to Claude via the Anthropic API.

Implements just enough of the A2A spec (agent card + message/send) to work as
a one-click Railway-deployable starter agent for AgentChat Hub or any other
A2A client. No streaming, no task persistence, no extra services.
"""

import os
import uuid

import anthropic
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

AGENT_NAME = os.environ.get("AGENT_NAME", "Starter Agent")
AGENT_MODEL = os.environ.get("AGENT_MODEL", "claude-sonnet-4-5")


def _public_url(request: Request) -> str:
    # Railway terminates TLS in front of the app, so trust the forwarded proto/host.
    proto = request.headers.get("x-forwarded-proto", "https")
    host = request.headers.get("x-forwarded-host", request.headers.get("host", ""))
    return f"{proto}://{host}"


@app.get("/.well-known/agent.json")
def agent_card(request: Request):
    return {
        "name": AGENT_NAME,
        "description": "A minimal Claude-backed agent speaking the A2A protocol.",
        "url": _public_url(request),
        "version": "1.0.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "skills": [
            {
                "id": "chat",
                "name": "Chat",
                "description": "General-purpose conversation powered by Claude.",
                "examples": ["What can you help me with?"],
            }
        ],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
    }


def _extract_text(parts: list[dict]) -> str:
    return "\n".join(p.get("text", "") for p in parts if p.get("type") == "text").strip()


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

    reply = client.messages.create(
        model=AGENT_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": user_text}],
    )
    reply_text = "".join(block.text for block in reply.content if block.type == "text")

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
