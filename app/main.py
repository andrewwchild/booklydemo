import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agent.memory import ConversationMemory
from agent.orchestrator import BooklyAgent

load_dotenv()

app = FastAPI(title="Bookly Customer Support Agent", version="1.0.0")
agent = BooklyAgent()

sessions: dict[str, ConversationMemory] = {}

STATIC_DIR = Path(__file__).parent / "static"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str | None = None


class ToolCallInfo(BaseModel):
    name: str
    arguments: dict
    result: dict


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    mode: str
    tool_calls: list[ToolCallInfo] = []


@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "llm_mode": "mock" if agent.use_mock else "live",
        "model": agent.model if not agent.use_mock else None,
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = ConversationMemory()

    memory = sessions[session_id]
    try:
        result = agent.chat(memory, req.message.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return ChatResponse(
        reply=result["reply"],
        session_id=session_id,
        mode=result["mode"],
        tool_calls=[
            ToolCallInfo(name=tc["name"], arguments=tc["arguments"], result=tc["result"])
            for tc in result.get("tool_calls", [])
        ],
    )


@app.delete("/api/session/{session_id}")
async def reset_session(session_id: str):
    sessions.pop(session_id, None)
    return {"ok": True}


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
