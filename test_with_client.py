#!/usr/bin/env python3
"""
Test the Google search using MCP client to call Playwright.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def search_google_with_playwright(query: str):
    """Use MCP client to control Playwright and search Google."""
    
    server_params = StdioServerParameters(
        command="/Users/davidson/workspace/agent-task-mcp/agent-playwright-mcp/run_playwright_proxy.sh"
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print(f"Searching Google for: {query}")
            print("-" * 50)
            
            # Navigate to Google AI search mode
            print("Navigating to Google AI search mode...")
            nav_result = await session.call_tool(
                "browser_navigate",
                arguments={"url": "https://www.google.com/search?udm=50"}
            )
            print(f"Navigation result: {nav_result}")
            
            # Wait a bit
            await session.call_tool(
                "browser_wait_for",
                arguments={"time": 2}
            )
            
            # Take a snapshot
            print("\nTaking snapshot...")
            snapshot = await session.call_tool(
                "browser_snapshot",
                arguments={}
            )
            
            # Parse the snapshot response
            snapshot_text = ""
            if hasattr(snapshot, 'content') and snapshot.content:
                for content_item in snapshot.content:
                    if hasattr(content_item, 'text'):
                        snapshot_text = content_item.text
                        break
            
            print(f"Snapshot text preview: {snapshot_text[:200]}...")
            
            # Look for search input - in AI mode it's a textbox
            import re
            ref_match = re.search(r'textbox.*?\[ref=(e\d+)\]', snapshot_text)
            if ref_match:
                search_ref = ref_match.group(1)
                print(f"\nFound search input with ref: {search_ref}")
                
                # Type the search query
                print(f"\nTyping search query: {query}")
                type_result = await session.call_tool(
                    "browser_type",
                    arguments={
                        "element": "search box",
                        "ref": search_ref,
                        "text": query,
                        "submit": True
                    }
                )
                print(f"Type result: {type_result}")
                
                # Wait for results
                await session.call_tool(
                    "browser_wait_for",
                    arguments={"time": 3}
                )
                
                # Take final snapshot
                final_snapshot = await session.call_tool(
                    "browser_snapshot", 
                    arguments={}
                )
                
                return "Search completed successfully"
            else:
                return "Could not find search input"

if __name__ == "__main__":
    result = asyncio.run(search_google_with_playwright("Python binary search tree"))
    print(f"\nFinal result: {result}")