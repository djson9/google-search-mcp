#!/usr/bin/env python3
"""
FastMCP server that provides Google search functionality using Playwright MCP via MCP Manager.
"""

import asyncio
import re
from fastmcp import FastMCP
from mcp import ClientSession
from mcp.client.sse import sse_client

# Create the MCP server
mcp = FastMCP("google-ai-search")

# MCP Manager SSE endpoint
MCP_MANAGER_URL = "http://127.0.0.1:8765/sse"


@mcp.tool()
async def search_google_ai(query: str) -> str:
    """
    Search Google using AI Mode via Playwright MCP and return the AI-generated response.

    Args:
        query: The search query to ask Google AI

    Returns:
        The AI response from Google search
    """
    try:
        # Connect to the MCP manager via SSE
        async with sse_client(MCP_MANAGER_URL) as transport:
            async with ClientSession(*transport) as session:
                # Initialize the session
                await session.initialize()
                
                # Navigate to Google AI search mode using the playwright MCP through the manager
                result = await session.call_tool(
                    "call_tool",
                    arguments={
                        "tool_name": "playwright__browser_navigate",
                        "arguments": {"url": "https://www.google.com/search?udm=50"}
                    }
                )
                
                # Wait for page to load
                await session.call_tool(
                    "call_tool",
                    arguments={
                        "tool_name": "playwright__browser_wait_for",
                        "arguments": {"time": 2}
                    }
                )
                
                # Take a snapshot to find the search input
                snapshot_result = await session.call_tool(
                    "call_tool",
                    arguments={
                        "tool_name": "playwright__browser_snapshot",
                        "arguments": {}
                    }
                )
                
                # Parse the snapshot to find the textbox ref
                snapshot_text = ""
                if hasattr(snapshot_result, "content") and snapshot_result.content:
                    for content_item in snapshot_result.content:
                        if hasattr(content_item, "text"):
                            snapshot_text = content_item.text
                            break
                
                # Find the textbox ref - search for combobox with "Search" in AI mode
                ref_match = re.search(r'combobox "Search".*?\[ref=(e\d+)\]', snapshot_text)
                if not ref_match:
                    # Fallback to textbox pattern
                    ref_match = re.search(r"textbox.*?\[ref=(e\d+)\]", snapshot_text)
                if not ref_match:
                    return f"Could not find search input on the page. Snapshot:\n{snapshot_text[:500]}..."
                
                search_ref = ref_match.group(1)
                
                # Type the search query and submit
                await session.call_tool(
                    "call_tool",
                    arguments={
                        "tool_name": "playwright__browser_type",
                        "arguments": {
                            "element": "search box",
                            "ref": search_ref,
                            "text": query,
                            "submit": True
                        }
                    }
                )
                
                # Wait for results to load - give more time for AI response
                await session.call_tool(
                    "call_tool",
                    arguments={
                        "tool_name": "playwright__browser_wait_for",
                        "arguments": {"time": 15}
                    }
                )
                
                # Take a snapshot of the results page
                final_snapshot = await session.call_tool(
                    "call_tool",
                    arguments={
                        "tool_name": "playwright__browser_snapshot",
                        "arguments": {}
                    }
                )
                
                # Extract the snapshot text
                snapshot_text = ""
                if hasattr(final_snapshot, "content") and final_snapshot.content:
                    for content_item in final_snapshot.content:
                        if hasattr(content_item, "text"):
                            snapshot_text = content_item.text
                            break
                
                return f"Google AI Search Results for '{query}':\n\n{snapshot_text}"
        
    except Exception as e:
        return f"Error performing Google search: {str(e)}"


if __name__ == "__main__":
    # Run the server
    mcp.run()