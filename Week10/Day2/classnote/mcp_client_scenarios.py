"""
mcp_client_scenarios.py — 5 worked examples of client <-> LLM <-> MCP server.

Run the server first, in another terminal:
    python mcp_server.py

Then run this file:
    python mcp_client_scenarios.py

WHAT EACH SCENARIO SHOWS
    1. Direct response      — LLM answers with no tool at all.
    2. One tool              — LLM calls get_weather.
    3. Two+ tools             — LLM calls read_file AND get_weather in one turn.
    4. Resource + tool       — the HOST injects notes://today into context,
                                then the LLM still calls a tool for the rest.
    5. Prompt template       — the USER triggers the "summarize" prompt by
                                name; the server hands back ready-made text
                                that itself asks the LLM to call read_file.

All five reuse the same DECIDE -> EXECUTE -> SYNTHESIZE helper so you can
compare them side by side.
"""

import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from openai import OpenAI

from logger_setup import get_logger

SERVER_URL = "http://127.0.0.1:8000/mcp/"
MODEL = "qwen2.5:3b"

llm = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
log = get_logger(__name__)


def convert_tool(mcp_tool):
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.inputSchema,
        },
    }


def log_messages(messages):
    for m in messages:
        role = m["role"] if isinstance(m, dict) else m.role
        content = m.get("content") if isinstance(m, dict) else m.content
        log.debug("  [%s] %s", role, content)


async def decide_execute_synthesize(session, mcp_tools, messages, label):
    """The shared 4-step loop every scenario below runs through."""
    log.info("=" * 70)
    log.info(label)
    log.info("=" * 70)
    log_messages(messages)

    # ── DECIDE ──────────────────────────────────────────────────────────
    response = llm.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[convert_tool(t) for t in mcp_tools],
        tool_choice="auto",
    )
    reply = response.choices[0].message
    messages.append(reply)

    if not reply.tool_calls:
        log.info("No tool needed. Answer: %s", reply.content)
        return reply.content

    log.info("Model wants %d tool call(s):", len(reply.tool_calls))
    for tc in reply.tool_calls:
        log.info("  %s(%s)", tc.function.name, tc.function.arguments)

    # ── EXECUTE — one call, one result message, per tool call ─────────
    for tc in reply.tool_calls:
        args = json.loads(tc.function.arguments)
        try:
            result = await session.call_tool(tc.function.name, arguments=args)
            output = result.content[0].text
            log.debug("  %s -> %s", tc.function.name, output[:200])
        except Exception:
            log.exception("Tool call failed: %s(%s)", tc.function.name, args)
            output = f"Tool call failed: {tc.function.name}"
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": output,
        })

    # ── SYNTHESIZE ──────────────────────────────────────────────────────
    final = llm.chat.completions.create(model=MODEL, messages=messages)
    log.info("Final answer: %s", final.choices[0].message.content)
    return final.choices[0].message.content


# ── Scenario 1 · direct response, no tool ────────────────────────────────
async def scenario_1(session, mcp_tools):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 12 times 4?"},
    ]
    await decide_execute_synthesize(session, mcp_tools, messages,
                                     "SCENARIO 1 — direct response, no tool")


# ── Scenario 2 · exactly one tool call ───────────────────────────────────
async def scenario_2(session, mcp_tools):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Call a "
         "tool whenever it can answer the question. Treat tool results as "
         "true, current data — never say you lack real-time access."},
        {"role": "user", "content": "What's the weather like in Paris right now?"},
    ]
    await decide_execute_synthesize(session, mcp_tools, messages,
                                     "SCENARIO 2 — one tool (get_weather)")


# ── Scenario 3 · two or more tool calls in one turn ──────────────────────
async def scenario_3(session, mcp_tools):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Call as "
         "many tools as needed to fully answer — you may need more than one."},
        {"role": "user", "content": "Read notes.txt for me, and separately "
         "tell me the current weather in Tokyo."},
    ]
    await decide_execute_synthesize(session, mcp_tools, messages,
                                     "SCENARIO 3 — two+ tools (read_file + get_weather)")


# ── Scenario 4 · resource injected by the HOST, then a tool call ─────────
async def scenario_4(session, mcp_tools):
    # The LLM never "calls" a resource — the host fetches it directly and
    # stuffs it into context, same as you'd paste a file into a chat.
    data = await session.read_resource("notes://today")
    notes = data.contents[0].text

    messages = [
        {"role": "system", "content": f"You are a helpful assistant. Today's "
         f"notes are already loaded for you: {notes} Call a tool for anything "
         f"these notes don't cover."},
        {"role": "user", "content": "Based on today's notes, what should I "
         "focus on? Also, what's the weather in New York?"},
    ]
    await decide_execute_synthesize(session, mcp_tools, messages,
                                     "SCENARIO 4 — resource (notes://today) + tool (get_weather)")


# ── Scenario 5 · user-triggered prompt template, which asks for a tool ───
async def scenario_5(session, mcp_tools):
    # The USER picks "summarize" by name (imagine a menu in a client like
    # Goose). The server returns ready-made instruction text — we drop it
    # straight in as the user's turn, no hand-typing required.
    prompt_result = await session.get_prompt("summarize", arguments={"filename": "notes.txt"})
    templated_user_message = prompt_result.messages[0].content.text

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Call a "
         "tool whenever it can answer the question."},
        {"role": "user", "content": templated_user_message},
    ]
    await decide_execute_synthesize(session, mcp_tools, messages,
                                     "SCENARIO 5 — prompt template ('summarize') -> tool (read_file)")


async def main():
    async with streamable_http_client(SERVER_URL) as (reader, writer, _):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            log.info("Discovered tools: %s", [t.name for t in mcp_tools])

            await scenario_1(session, mcp_tools)
            await scenario_2(session, mcp_tools)
            await scenario_3(session, mcp_tools)
            await scenario_4(session, mcp_tools)
            await scenario_5(session, mcp_tools)


if __name__ == "__main__":
    asyncio.run(main())
