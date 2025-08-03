.PHONY: install server client test clean

install:
	pip install -r requirements.txt

server:
	python wikipedia_mcp.py

client:
	python simple_client.py