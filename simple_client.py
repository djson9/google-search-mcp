#!/usr/bin/env python3
"""
Simple client to test the Wikipedia MCP server using subprocess.
"""

import asyncio
import json
from fastmcp import FastMCP

async def test_with_fastmcp_client():
    """Test the Wikipedia server using FastMCP's testing capabilities."""
    
    # Import the server
    from wikipedia_mcp import mcp as server
    
    # Get a test client
    async with server.test_client() as client:
        print("Testing Wikipedia MCP Server")
        print("=" * 50)
        
        # Test searches
        test_queries = [
            ("Python programming language", 3),
            ("Machine learning", 4),
            ("FastMCP", 2)
        ]
        
        for query, limit in test_queries:
            print(f"\nSearching for: '{query}' (limit: {limit})")
            print("-" * 40)
            
            # Call the tool
            result = await client.call_tool(
                "search_wikipedia",
                query=query,
                limit=limit
            )
            
            print(result)
            print()

if __name__ == "__main__":
    asyncio.run(test_with_fastmcp_client())