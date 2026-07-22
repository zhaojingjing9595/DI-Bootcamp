import asyncio
import json
import os
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from openai import OpenAI


# Step 0: setup
SERVER_URL = "http://127.0.0.1:8000/mcp/"
MODEL = "qwen2.5:3b"

llm = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")

QUESTION = "read my notes file, and summarize it, and another question is : What is the current weather in New York?"

# helper to convert the json
def convert_tool(mcp_tool):
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.inputSchema
        }
    }
    

async def main():
    # connect to server
    async with streamable_http_client(SERVER_URL) as (reader, writer, _):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            
            
            #  Step 1: Discover Tools, resources, etc..
            print("Discovering Tools: ")
            tools = await session.list_tools()
            for t in tools.tools:
                print(f"   tool name: {t.name} \n   tool desc: {t.description} \n ")
            
            # Step 2: Discover Resources
            print("Discovering Resources: ")
            resources = await session.list_resources()
            for r in resources.resources:
                print(f"   resource: {r.name} - {r.uri}")
            
            #step 3: Discover Prompts
            print("Discovering Prompts")
            prompts = await session.list_prompts()
            for p in prompts.prompts:
                print(f"   prompt name: {p.name}")
                print(f"   prompt desc: {p.description}")
                for arg in (p.arguments or []):
                    print(f"    needs arg: {arg.name}")
                    
            # Push a resource
            data = await session.read_resource("notes://today")
            notes = data.contents[0].text
            print(notes)
                
            # messages = [
            #     {
            #         "role": "system",
            #         "content": f"Here is today's note: {notes}"
            #     }, 
            #     {   
            #         "role": "user",
            #         "content": "Base on the note, what should I focus on?"
            #     }
                
            # ]
            print(f"Question: {QUESTION}")
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant. And here is today's note: " + notes + "When a tool can answer, call it.When a tool result is given to you, treat it as true, current data and answer directly using it. Never say you lack real-time access."},
                    # {
                    #     "role": "system", 
                    #     "content": "You are a helpful assistant. When a tool can answer, call it. When a tool result is given to you, treat it as true, current data and answer directly using it. Never say you lack real-time access."},   # B
                {
                    "role": "user", 
                    "content": QUESTION},
            ]
            print("LLM thinking" + 6*".")
            answer = llm.chat.completions.create(
                model=MODEL,
                tools=[convert_tool(t) for t in tools.tools],
                messages=messages,
                tool_choice="auto")
            reply = answer.choices[0].message
            print(f"LLM response: \n {reply}")
            if reply.content:
                print(f" content: {reply.content}")
                
                # messages.append([
                #     {
                #         "role": "system", 
                #         "content": "You are a helpful assistant. When a tool can answer, call it. When a tool result is given to you, treat it as true, current data and answer directly using it. Never say you lack real-time access."},
                #     {
                #         "role": "user", 
                #         "content": QUESTION},
                # ])
                # reply2 = llm.chat.completions.create(model=MODEL, messages=messages)

                # if reply2.content:
                #     print(f"reply2 content: {reply.content}")
                # elif len(reply2.tool_calls) > 0:
                #     chosen = reply2.tool_calls[0]
                #     tool_name = chosen.function.name
                #     tool_arg = json.loads(chosen.function.arguments)
                #     print(f"2nd response content: {reply2.content}")
                #     print(f"chosen tool_name: {tool_name}, tool_arg: {tool_arg}")
                #     result = await session.call_tool(tool_name, arguments=tool_arg)
                #     tool_output = result.content[0].text
                #     print(f"tool_output: {tool_output}")

            tool_results = []
            if len(reply.tool_calls) > 0:
                print(f"found {len(reply.tool_calls)}")
                for t in reply.tool_calls:
                    tool_name = t.function.name
                    tool_arg = json.loads(t.function.arguments)
                    print(f"need tools")
                    print(f" tool_name: {tool_name}, tool_arg: {tool_arg}")
                    result = await session.call_tool(tool_name, arguments=tool_arg)
                    tool_output = result.content[0].text
                    print(f"tool_output: {tool_output}")
                    tool_results.append((t.id, tool_output))

            print("##### Synthesis ####")
            messages.append(reply)
            for tool_call_id, tool_output in tool_results:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": tool_output
                })

            final = llm.chat.completions.create(model=MODEL, messages=messages)
            print(f"final content: {final.choices[0].message.content}")

if __name__ == "__main__":
    asyncio.run(main())