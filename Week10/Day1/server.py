from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b

@mcp.resource("greeting://{name}")
def greet(name: str) -> str:
    """Return a greeting for the given name."""
    # TODO: return "Hello, {name}!"
    return f"Hello, {name}"

if __name__ == "__main__":
    # TODO: start the server loop over STDIO
    mcp.run(transport='stdio')
