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


async def main():
    # AsyncExitStack lets us open (and later close) server connections cleanly.
    async with AsyncExitStack() as stack:
        # Open the connection to your Day 1 server.
        r, w, _ = await stack.enter_async_context(streamable_http_client(LOCAL_URL))
        session = await stack.enter_async_context(ClientSession(r, w))
        await session.initialize()

        # =====================================================================
        # >>> YOUR CODE GOES HERE  —  paste each STAGE from the guide below  <<<
        # =====================================================================
        console.print("[dim]Skeleton is connected. Now add Stage 4 from the guide.[/dim]")
        
        # remember which server owns each tool
        owner = {}          # tool name -> the session that runs it
        all_tools = []      # every tool, in the model's format

        for t in (await session.list_tools()).tools:
            owner[t.name] = session
            all_tools.append(to_openai_tool(t))
            
        # connect Neon (only if a key is set)
        neon_pid, schema_hint = "", ""
        NEON_KEY = os.environ.get("NEON_API_KEY", "")
        if NEON_KEY:
            neon_http_client = httpx.AsyncClient(headers={"Authorization": f"Bearer {NEON_KEY}"})
            r2, w2, _ = await stack.enter_async_context(
                streamable_http_client("https://mcp.neon.tech/mcp",
                                        http_client=neon_http_client))
            neon = await stack.enter_async_context(ClientSession(r2, w2))
            await neon.initialize()
            for t in (await neon.list_tools()).tools:
                if t.name == "run_sql":                 # just this one, to keep it focused
                    owner[t.name] = neon
                    all_tools.append(to_openai_tool(t))

            # find the project id
            for tn in ("list_projects", "list_shared_projects"):
                try:
                    d = extract(await neon.call_tool(tn, arguments={}))
                    projs = d.get("projects", d) if isinstance(d, dict) else d
                    if isinstance(projs, list) and projs:
                        neon_pid = projs[0].get("id", ""); break
                except Exception:
                    pass
            console.print(f"[cyan]Neon project:[/cyan] {neon_pid or '(not found — paste it manually)'}")
            neon_pid = "dark-tooth-58181708"
            # read the table + column names, so the AI uses REAL column names
            if neon_pid:
                d = extract(await neon.call_tool("run_sql", arguments={
                    "projectId": neon_pid, "databaseName": "neondb",
                    "sql": "SELECT table_name, column_name FROM information_schema.columns "
                           "WHERE table_schema='public' ORDER BY table_name, ordinal_position"}))
                rows = d.get("rows", d) if isinstance(d, dict) else d
                cols = {}
                for row in rows:
                    if isinstance(row, dict) and "table_name" in row:
                        cols.setdefault(row["table_name"], []).append(row.get("column_name", ""))
                def quoted(name):
                    # Postgres lowercases unquoted identifiers, so any table/column
                    # with uppercase letters must be double-quoted EXACTLY in SQL.
                    return f'"{name}"' if name != name.lower() else name

                schema_hint = (
                    " Database tables: " + "; ".join(
                        f"{quoted(t)}({', '.join(quoted(c) for c in cs)})" for t, cs in cols.items())
                    + " IMPORTANT: any identifier shown above in double quotes contains "
                      "uppercase letters and MUST be wrapped in double quotes exactly as "
                      "shown in every SQL query, or Postgres will fail to find it."
                )
                console.print(Panel(schema_hint.strip(), title="🗂️  Schema", border_style="cyan"))

        #######################################################################
        # STAGE 4 — ask the server for its tools
        # tools = (await session.list_tools()).tools
        console.print(Panel(
            "\n".join(f"• {t['function']['name']}" for t in all_tools),
            title="🛠️  Available tools", border_style="blue"))

        #######################################################################
        # STAGE 5 — ask the AI which tool to use
        # openai_tools = [to_openai_tool(t) for t in tools]

        messages = [
            {
                "role": "system", 
                "content": "You are a helpful assistant. When a tool result is given, use it and answer directly. For run_sql, the projectId and databaseName are provided for you." + schema_hint},
        ]

        console.print("[bold green]Chat ready![/bold green] [dim](type 'quit' to exit)[/dim]\n")
        while True:
            user = console.input("[bold cyan]You:[/bold cyan] ").strip()
            if user.lower() in ("quit", "exit"):
                break

            messages.append({
                "role": "user",
                "content": user
            })

            # inner AGENT loop: keep calling tools until the AI is done (max 5 rounds)
            for _ in range(5):
                console.rule(f"[dim]round {_+1}[/dim]", style="dim")
                resp = llm.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    tools=all_tools,
                    tool_choice="auto")
                msg = resp.choices[0].message

                ######################################################################
                # llm response option 1: no tool call needed, just return answers
                if not msg.tool_calls:
                    messages.append({
                        "role": "assistant",
                        "content": msg.content})
                    console.print(Panel(Markdown(msg.content or ""),
                                         title="🤖 Assistant", border_style="green"))
                    break

                ######################################################################
                # llm response option 2: ask for some tools
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

                # EXECUTE each tool the AI asked for, and save the result
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    if tc.function.name == "run_sql":    # the APP supplies these, not the AI
                        args["projectId"] = neon_pid
                        args["databaseName"] = "neondb"
                    the_session = owner.get(tc.function.name, session)   # <-- ROUTE it
                    console.print(Panel(
                        json.dumps(args, indent=2),
                        title=f"🔧 calling {tc.function.name}", border_style="yellow"))

                    result = await the_session.call_tool(tc.function.name, arguments=args)
                    console.print(Panel(
                        result_text(result),
                        title="📦 tool result", border_style="magenta"))
                    # save tool calling results to the context
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": result_text(result)
                        })

        # SYNTHESIZE — ask the AI again, now that it has the real data
        final = llm.chat.completions.create(model=MODEL, messages=messages)
        console.print(Panel(Markdown(final.choices[0].message.content or ""),
                             title="✅ Answer", border_style="green"))


asyncio.run(main())
