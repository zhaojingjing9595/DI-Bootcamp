from mcp.server.fastmcp import FastMCP
notes = []
mcp = FastMCP() ## TODO: consruct FastMCP server instance

## TODO: Add decorator to register list_notes as a tool
@mcp.tool()
def add_note(text: str) -> str:
    'Add a note to the in-memory list.'
    notes.append(text)
    return f"Saved note #{len(notes)}: {text}"

## TODO: Add decorator to register list_notes as a tool
@mcp.tool()
def list_notes() -> str:
    'List saved notes.'
    if not notes:
        return "No notes yet"
    return "".join(f"{i+1}. {n}" for i, n in enumerate(notes))

if __name__ == "__main__":
    mcp.run()