import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command="mcp", args=["run", "server.py"], env=None)


def extract_content(payload):
    """Best-effort to pull text from MCP responses."""
    if hasattr(payload, "contents"):
        contents = payload.contents
        if contents:
            first = contents[0]
            if hasattr(first, "text"):
                return first.text
            if isinstance(first, dict) and "text" in first:
                return first["text"]
            return str(first)
    if hasattr(payload, "content"):
        content = payload.content
        if content:
            first = content[0]
            if hasattr(first, "text"):
                return first.text
        return content
    return str(payload)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # TODO: list resources and print their URIs
            resources = await session.list_resources()
            for r in resources.resources:
                print(r.uri)
            # TODO: list tools and print their names
            tools = await session.list_tools()
            # TODO: read greeting://hello and print the content
            result = await session.read_resource("greeting://hello")
            print(extract_content(result))

            # TODO: call add with a=1, b=7 and print the result
            result = await session.call_tool("add", {"a": 1, "b": 7})
            print(extract_content(result))

if __name__ == "__main__":
    asyncio.run(run())
