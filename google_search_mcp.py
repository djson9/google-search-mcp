#!/usr/bin/env python3
"""
FastMCP server that provides Google search functionality using Playwright and Wikipedia search.
"""

import asyncio
import httpx
from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("google-ai-search")

@mcp.tool()
async def search_wikipedia(query: str, limit: int = 5) -> str:
    """
    Search Wikipedia for articles matching the query.
    
    Args:
        query: Search term to look for
        limit: Maximum number of results to return (default: 5)
    
    Returns:
        A formatted string with search results
    """
    # Wikipedia API endpoint
    url = "https://en.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": limit
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()
        
        if "query" not in data or "search" not in data["query"]:
            return f"No results found for '{query}'"
        
        results = data["query"]["search"]
        
        if not results:
            return f"No results found for '{query}'"
        
        # Format the results
        output = f"Wikipedia search results for '{query}':\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "Unknown")
            snippet = result.get("snippet", "No description available")
            # Remove HTML tags from snippet
            snippet = snippet.replace("<span class='searchmatch'>", "").replace("</span>", "")
            
            output += f"{i}. **{title}**\n"
            output += f"   {snippet}...\n"
            output += f"   URL: https://en.wikipedia.org/wiki/{title.replace(' ', '_')}\n\n"
        
        return output.strip()

@mcp.tool()
async def debug() -> str:
    """
    Debug tool that navigates to the Google AI search page and returns a snapshot.

    Returns:
        A snapshot of the Google AI search page
    """
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    try:
        # Connect to the Playwright MCP server
        server_params = StdioServerParameters(
            command="npx",
            args=["@playwright/mcp@latest"]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()

                # Navigate to Google AI search mode
                await session.call_tool(
                    "browser_navigate",
                    arguments={"url": "https://www.google.com/search?udm=50"}
                )

                # Wait for page to load
                await session.call_tool(
                    "browser_wait_for",
                    arguments={"time": 3}
                )

                # Take a snapshot of the page
                snapshot_result = await session.call_tool(
                    "browser_snapshot",
                    arguments={}
                )

                # Extract the snapshot text
                snapshot_text = ""
                if hasattr(snapshot_result, 'content') and snapshot_result.content:
                    for content_item in snapshot_result.content:
                        if hasattr(content_item, 'text'):
                            snapshot_text = content_item.text
                            break

                # Keep the browser open for debugging
                await session.call_tool(
                    "browser_wait_for",
                    arguments={"time": 30}  # Wait 30 seconds before closing
                )

                return f"Debug: Google AI Search Page Navigation Complete\n\nPage Snapshot:\n{snapshot_text}"

    except Exception as e:
        return f"Debug error: {str(e)}"

@mcp.tool()
async def search_google_ai(query: str) -> str:
    """
    Search Google using AI Mode via Playwright MCP and return the AI-generated response.

    Args:
        query: The search query to ask Google AI

    Returns:
        The AI response from Google search
    """
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    import re
    
    try:
        # Connect to the Playwright MCP server
        server_params = StdioServerParameters(
            command="npx",
            args=["@playwright/mcp@latest"]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                # Navigate to Google AI search mode
                await session.call_tool(
                    "browser_navigate",
                    arguments={"url": "https://www.google.com/search?udm=50"}
                )
                
                # Wait for page to load
                await session.call_tool(
                    "browser_wait_for",
                    arguments={"time": 2}
                )
                
                # Take a snapshot to find the search input
                snapshot_result = await session.call_tool(
                    "browser_snapshot",
                    arguments={}
                )
                
                # Parse the snapshot to find the textbox ref
                snapshot_text = ""
                if hasattr(snapshot_result, 'content') and snapshot_result.content:
                    for content_item in snapshot_result.content:
                        if hasattr(content_item, 'text'):
                            snapshot_text = content_item.text
                            break
                
                # Find the textbox ref
                ref_match = re.search(r'textbox.*?\[ref=(e\d+)\]', snapshot_text)
                if not ref_match:
                    return "Could not find search input on the page"
                
                search_ref = ref_match.group(1)
                
                # Type the search query and submit
                await session.call_tool(
                    "browser_type",
                    arguments={
                        "element": "search box",
                        "ref": search_ref,
                        "text": query,
                        "submit": True
                    }
                )
                
                # Wait for results to load - give more time for AI response
                await session.call_tool(
                    "browser_wait_for",
                    arguments={"time": 15}
                )
                
                # Take a snapshot of the results page
                final_snapshot = await session.call_tool(
                    "browser_snapshot",
                    arguments={}
                )
                
                # Extract the snapshot text
                snapshot_text = ""
                if hasattr(final_snapshot, 'content') and final_snapshot.content:
                    for content_item in final_snapshot.content:
                        if hasattr(content_item, 'text'):
                            snapshot_text = content_item.text
                            break
                
                return f"Google AI Search Results for '{query}':\n\n{snapshot_text}"
                
    except Exception as e:
        return f"Error performing Google search: {str(e)}"

if __name__ == "__main__":
    # Run the server
    asyncio.run(mcp.run())