from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DemoServer")

#To-Do: Add decorator to register add as a tool
@mcp.tool()
def add(a: int, b: int) -> int:
    "Add two numbers."
    return a + b

# TODO (optional exercise): add multiply(a, b) here if you want an extra tool
@mcp.tool()
def multiply(a: float, b: float) -> float:
    "Multiple two numbers"
    return a * b



#To-Do: Add decorator to register greet as a tool
@mcp.tool()
def greet(name: str) -> str:
    "Return a greeting string."
    return f"Hey, {name}!"

if __name__ == "__main__":
    mcp.run()
