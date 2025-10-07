.PHONY: install server client test clean

install:
	pip install -r requirements.txt

client:
	python simple_client.py