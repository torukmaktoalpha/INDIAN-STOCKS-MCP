# Indian Stocks MCP

This project provides a Model Context Protocol (MCP) server for accessing Indian stock market data. It is designed to be used as a backend data provider for financial analysis, research, and AI-powered applications.

## Features
- Exposes financial data for Indian stocks via a local server (`server.py`).
- Integrates with MCP-compatible tools and workflows.
- Supports trending stocks, financial statements, historical stats, and more.
- Secure API key and base URL configuration via environment variables.

## Usage
1. Ensure you have Python 3 installed.
2. Start the server:
   ```sh
   python3 server.py
   ```
3. The server will connect to the Indian stock data API using the credentials set in your environment or configuration.

## Configuration
- `FINANCE_API_KEY`: Your API key for https://stock.indianapi.in
- `FINANCE_API_BASE_URL`: The base URL for the stock data API (default: https://stock.indianapi.in)

These can be set in your environment or are configured in your VS Code settings for MCP integration.

## Using with Claude Desktop

To use the Indian Stocks MCP server with Claude Desktop, add the following configuration to your Claude Desktop config file (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "finance-data-server": {
      "command": "python3",
      "args": ["/Users/aditya/Desktop/indian-stocks-mcp/server.py"],
      "env": {
        "FINANCE_API_KEY": "<your_finance_api_key>",
        "FINANCE_API_BASE_URL": "https://stock.indianapi.in"
      }
    }
  }
}
```

Replace `<your_finance_api_key>` with your actual API key.

This will enable Claude Desktop to access Indian stock market data through the MCP server you are running locally.

## Integration
This project is intended to be used with MCP-compatible clients, such as VS Code extensions or AI agents that support the Model Context Protocol.

## License
This project is for educational and research purposes. Please check the API provider's terms of use for data licensing and restrictions.
