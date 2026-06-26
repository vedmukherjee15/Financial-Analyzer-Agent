# Gsheet Agent

`Gsheet Agent` is a Google Sheets-oriented financial analysis assistant built with LangChain, LangGraph, OpenAI chat models, and MCP tools. It can read spreadsheet data, fetch market and finance context from external tools, and answer spreadsheet-focused requests in natural language.

## What It Does

- Reads Google Sheets data through MCP tools
- Uses Yahoo Finance MCP for market and company data
- Uses a live web search tool for supplemental context
- Supports conversational querying from the terminal
- Maintains per-thread conversational state with LangGraph checkpointers

## Current Status

The current implementation is best treated as a read-first analysis agent.

Raw Google Sheets write tools such as `update_cells` and `batch_update_cells` have been disabled in the agent because model-generated ranges were causing repeated Google Sheets API `400` errors. Read operations and analysis workflows are the stable path right now.

## Project Structure

```text
Gsheet Agent/
├── analysis_Agent.py
├── README.md
├── .gitignore
├── scripts/
│   ├── base_tools.py
│   ├── mcp_config.example.json
│   ├── mcp_config.json
│   ├── prompts.py
│   └── utils.py
├── Eternal.md
├── news.md
└── test.md
```

## How It Works

`analysis_Agent.py` is the entrypoint. It:

1. Loads environment variables with `python-dotenv`
2. Loads MCP server configuration from `scripts/mcp_config.json`
3. Connects to the `google-sheets` and `yahoo-finance` MCP servers
4. Registers extra local tools such as weather and web search
5. Builds a LangChain agent with a LangGraph in-memory checkpointer
6. Runs an interactive terminal loop for natural language prompts

## Requirements

- Python `3.12+`
- `uv` recommended for dependency management
- OpenAI API access
- Google Sheets MCP credentials
- Network access for external MCP tools and APIs

## Installation

From the project root:

```bash
uv sync
```

If you prefer `pip`:

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Environment Variables

Create a local `.env` file inside `Gsheet Agent` or set these in your shell:

```env
OPENAI_API_KEY=your_openai_api_key
WEATHER_API_KEY=your_weatherapi_key
```

### 2. MCP Configuration

The agent expects a local file at:

```text
scripts/mcp_config.json
```

Start from the example file:

```bash
cp scripts/mcp_config.example.json scripts/mcp_config.json
```

Then replace the placeholder values with your local Google Sheets and token paths.

## Running the Agent

Run from inside the `Gsheet Agent` directory:

```bash
cd "Gsheet Agent"
uv run python analysis_Agent.py
```

If you are using the existing virtual environment directly:

```bash
python analysis_Agent.py
```

## Example Prompts

- `Show me the latest cash flow data for Apple from the connected sheet`
- `Read the quarterly sheet and summarize the top 5 changes`
- `Compare the balance sheet values in the sheet with recent Yahoo Finance data`
- `Find recent news about Nvidia and summarize it next to the sheet context`

## Key Files

- [analysis_Agent.py](./analysis_Agent.py): interactive CLI entrypoint
- [scripts/base_tools.py](./scripts/base_tools.py): local helper tools such as web search and weather
- [scripts/utils.py](./scripts/utils.py): MCP config loading utilities
- [scripts/prompts.py](./scripts/prompts.py): system prompt for the sheet agent




