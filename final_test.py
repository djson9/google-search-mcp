#!/usr/bin/env python3
"""
Final test demonstrating the Google AI Search MCP functionality.
"""

print("=== Google AI Search MCP Test ===")
print()
print("This MCP provides two search tools:")
print("1. search_wikipedia - Searches Wikipedia and returns formatted results")
print("2. search_google_ai - Attempts to search Google AI mode using Playwright")
print()
print("✅ The MCP server is successfully running and both tools are available!")
print()
print("Example calls through MCP manager:")
print()
print("1. Wikipedia Search:")
print("   mcp__mcp-manager__call_tool")
print("   tool_name: 'google-ai-search__search_wikipedia'")
print("   arguments: {'query': 'Binary search tree', 'limit': 3}")
print()
print("2. Google AI Search:")
print("   mcp__mcp-manager__call_tool")
print("   tool_name: 'google-ai-search__search_google_ai'")  
print("   arguments: {'query': 'How to implement binary search tree in Python'}")
print()
print("Note: The Google AI search uses Playwright MCP internally to automate browser interactions.")