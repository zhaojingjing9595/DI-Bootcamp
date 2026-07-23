"""
workshop_agent_START.py — your STARTING POINT for the guided build.

Follow WORKSHOP_Build_the_Agent.md. You will paste ONE stage at a time into the
marked spot below, run it, watch it work, then move to the next stage.

BEFORE YOU START (do this once):
    pip install "mcp[cli]" openai python-dotenv ddgs
    ollama pull qwen2.5:7b
    Terminal 1:  python ../Day1-Build-a-Server/day1_server_full.py   (keep it running!)

    (Optional, for the last stage) make a .env file next to this one:
        NEON_API_KEY=your_key_here
"""
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


import asyncio
import json
import os
from contextlib import AsyncExitStack

from dotenv import load_dotenv
load_dotenv()

from mcp import ClientSession
import httpx
from mcp.client.streamable_http import streamable_http_client
from openai import OpenAI

# ── settings ─────────────────────────────────────────────────────────────────
LOCAL_URL = "http://127.0.0.1:8000/mcp/"   # your Day 1 server
MODEL     = "qwen2.5:3b"                     # a strong tool-caller
NEON_URL  = "https://mcp.neon.tech/mcp"
NEON_DB   = "neondb"
MAX_ROUNDS = 5
llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # connect to local ollama llm model


# ── helpers (already written for you — don't worry about these) ──────────────
def to_openai_tool(t):
    """Turn an MCP tool into the shape the model expects."""
    return {"type": "function", "function": {
        "name": t.name, "description": t.description or "", "parameters": t.inputSchema}}


def extract(result):
    """Get the data out of a tool result. Neon's SQL results come back as
    'structuredContent' (a dict); your local tools come back as text.
    (You'll need this in Stage 8 — leave it as-is.)"""
    data = getattr(result, "structuredContent", None)
    if data:
        return data
    parts = getattr(result, "content", None) or getattr(result, "contents", []) or []
    text = "".join(getattr(p, "text", "") for p in parts).strip()
    try:
        return json.loads(text) if text else text
    except Exception:
        return text


def result_text(result):
    """Always return a readable string for the model — works for text results
    (local tools) AND structuredContent results (Neon's run_sql)."""
    parts = getattr(result, "content", None) or getattr(result, "contents", []) or []
    text = "".join(getattr(p, "text", "") for p in parts)
    return text or json.dumps(extract(result))[:2000]


def quoted(name):
    # Postgres lowercases unquoted identifiers, so any table/column
    # with uppercase letters must be double-quoted EXACTLY in SQL.
    return f'"{name}"' if name != name.lower() else name


# ── connection setup ──────────────────────────────────────────────────────────
async def connect_local_server(stack, owner, all_tools):
    """Open the connection to the Day 1 server and register its tools."""
    r, w, _ = await stack.enter_async_context(streamable_http_client(LOCAL_URL))
    session = await stack.enter_async_context(ClientSession(r, w))
    await session.initialize()

    for t in (await session.list_tools()).tools:
        owner[t.name] = session
        all_tools.append(to_openai_tool(t))

    return session


async def find_neon_project_id(neon):
    """Look up the first available Neon project id."""
    for tool_name in ("list_projects", "list_shared_projects"):
        try:
            d = extract(await neon.call_tool(tool_name, arguments={}))
            projs = d.get("projects", d) if isinstance(d, dict) else d
            if isinstance(projs, list) and projs:
                return projs[0].get("id", "")
        except Exception:
            pass
    return ""


async def fetch_schema_hint(neon, neon_pid):
    """Read the table + column names, so the AI uses REAL column names."""
    d = extract(await neon.call_tool("run_sql", arguments={
        "projectId": neon_pid, "databaseName": NEON_DB,
        "sql": "SELECT table_name, column_name FROM information_schema.columns "
               "WHERE table_schema='public' ORDER BY table_name, ordinal_position"}))
    rows = d.get("rows", d) if isinstance(d, dict) else d

    cols = {}
    for row in rows:
        if isinstance(row, dict) and "table_name" in row:
            cols.setdefault(row["table_name"], []).append(row.get("column_name", ""))

    return (
        " Database tables: " + "; ".join(
            f"{quoted(t)}({', '.join(quoted(c) for c in cs)})" for t, cs in cols.items())
        + " IMPORTANT: any identifier shown above in double quotes contains "
          "uppercase letters and MUST be wrapped in double quotes exactly as "
          "shown in every SQL query, or Postgres will fail to find it."
    )


async def connect_neon(stack, owner, all_tools):
    """Connect to Neon (only if a key is set) and return (neon_pid, schema_hint)."""
    neon_key = os.environ.get("NEON_API_KEY", "")
    if not neon_key:
        return "", ""

    neon_http_client = httpx.AsyncClient(headers={"Authorization": f"Bearer {neon_key}"})
    r2, w2, _ = await stack.enter_async_context(
        streamable_http_client(NEON_URL, http_client=neon_http_client))
    neon = await stack.enter_async_context(ClientSession(r2, w2))
    await neon.initialize()

    for t in (await neon.list_tools()).tools:
        if t.name == "run_sql":                 # just this one, to keep it focused
            owner[t.name] = neon
            all_tools.append(to_openai_tool(t))

    neon_pid = await find_neon_project_id(neon)
    console.print(f"[cyan]Neon project:[/cyan] {neon_pid or '(not found — paste it manually)'}")
    neon_pid = "dark-tooth-58181708"

    schema_hint = ""
    if neon_pid:
        schema_hint = await fetch_schema_hint(neon, neon_pid)
        console.print(Panel(schema_hint.strip(), title="🗂️  Schema", border_style="cyan"))

    return neon_pid, schema_hint


# ── chat / agent loop ─────────────────────────────────────────────────────────
def build_system_message(schema_hint):
    return {
        "role": "system",
        "content": "You are a helpful assistant. When a tool result is given, use it and "
                   "answer directly. For run_sql, the projectId and databaseName are "
                   "provided for you." + schema_hint,
    }


def print_available_tools(all_tools):
    console.print(Panel(
        "\n".join(f"• {t['function']['name']}" for t in all_tools),
        title="🛠️  Available tools", border_style="blue"))


async def execute_tool_calls(msg, messages, owner, session, neon_pid):
    """Run every tool the AI asked for and append each result to messages."""
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        if tc.function.name == "run_sql":    # the APP supplies these, not the AI
            args["projectId"] = neon_pid
            args["databaseName"] = NEON_DB
        the_session = owner.get(tc.function.name, session)   # <-- ROUTE it

        console.print(Panel(
            json.dumps(args, indent=2),
            title=f"🔧 calling {tc.function.name}", border_style="yellow"))

        result = await the_session.call_tool(tc.function.name, arguments=args)
        console.print(Panel(
            result_text(result),
            title="📦 tool result", border_style="magenta"))

        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": result_text(result),
        })


def call_llm(messages, all_tools):
    return llm.chat.completions.create(
        model=MODEL, messages=messages, tools=all_tools, tool_choice="auto")


async def run_agent_rounds(messages, all_tools, owner, session, neon_pid):
    """Keep calling tools until the AI is done answering (max MAX_ROUNDS rounds)."""
    for round_num in range(MAX_ROUNDS):
        console.rule(f"[dim]round {round_num + 1}[/dim]", style="dim")
        resp = call_llm(messages, all_tools)
        msg = resp.choices[0].message

        if not msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content})
            console.print(Panel(Markdown(msg.content or ""),
                                 title="🤖 Assistant", border_style="green"))
            return

        # save the AI's turn (it asked for a tool)
        messages.append({
            "role": "assistant", "content": msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                } for tc in msg.tool_calls],
        })
        console.print(f"[yellow]AI wants to call:[/yellow] {[tc.function.name for tc in msg.tool_calls]}")

        await execute_tool_calls(msg, messages, owner, session, neon_pid)


def print_final_answer(messages):
    """Ask the AI again, now that it has the real data, and print the answer."""
    final = llm.chat.completions.create(model=MODEL, messages=messages)
    console.print(Panel(Markdown(final.choices[0].message.content or ""),
                         title="✅ Answer", border_style="green"))


async def chat_loop(session, all_tools, owner, neon_pid, schema_hint):
    messages = [build_system_message(schema_hint)]
    console.print("[bold green]Chat ready![/bold green] [dim](type 'quit' to exit)[/dim]\n")

    while True:
        user = console.input("[bold cyan]You:[/bold cyan] ").strip()
        if user.lower() in ("quit", "exit"):
            break

        messages.append({"role": "user", "content": user})
        await run_agent_rounds(messages, all_tools, owner, session, neon_pid)

    print_final_answer(messages)


# ── entrypoint ────────────────────────────────────────────────────────────────
async def main():
    # AsyncExitStack lets us open (and later close) server connections cleanly.
    async with AsyncExitStack() as stack:
        owner = {}          # tool name -> the session that runs it
        all_tools = []      # every tool, in the model's format

        session = await connect_local_server(stack, owner, all_tools)
        neon_pid, schema_hint = await connect_neon(stack, owner, all_tools)

        print_available_tools(all_tools)
        await chat_loop(session, all_tools, owner, neon_pid, schema_hint)


asyncio.run(main())
