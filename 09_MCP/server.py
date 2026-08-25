
#%% packages
from mcp.server import MCPServer
import os


#%% Create an MCP server
mcp = MCPServer(name="LocalMcpServer")

# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Add two numbers"""
#     return a + b


#%% Add an addition tool
@mcp.tool()
def list_files(folder_path: str) -> list[str]:
    """List files in a folder"""
    return os.listdir(folder_path)

@mcp.tool()
def write_markdown_file(file_path: str, content: str) -> str:
    """Write a markdown file
    Args:
        file_path: path to the file
        content: content to write to the file
    Returns:
        success message
    """
    with open(file_path, 'w') as file:
        file.write(content)
    return f"File {file_path} written successfully"

if __name__ == "__main__":
    mcp.run()

#%% install in Claude desktop
# mcp install server.py



