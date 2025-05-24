import os
import requests
from fastmcp import FastMCP
import json # For better error display if needed

# --- Configuration ---
API_BASE_URL_DEFAULT = os.getenv("FINANCE_API_BASE_URL", "https://stock.indianapi.in")
API_BASE_URL = API_BASE_URL_DEFAULT
API_KEY_ENV_VAR = "INDIANAPI_KEY"

# Support both INDIANAPI_KEY and FINANCE_API_KEY for compatibility with Claude Desktop config
api_key = os.getenv("INDIANAPI_KEY") or os.getenv("FINANCE_API_KEY")
if api_key:
    os.environ[API_KEY_ENV_VAR] = api_key

mcp = FastMCP("indian-stocks-mcp")

def _make_api_request(endpoint: str, params: dict = None):
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        print(f"ERROR: API key environment variable '{API_KEY_ENV_VAR}' not set.")
        return {
            "status": "error",
            "error_type": "ConfigurationError",
            "message": f"API key '{API_KEY_ENV_VAR}' is not configured in the environment.",
        }
    headers = {
        "X-Api-Key": api_key,
        "Accept": "application/json"
    }
    url = f"{API_BASE_URL}{endpoint}"
    try:
        print(f"MCP Server: Making request to {url} with params: {params}")
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        try:
            data = response.json()
            return {"status": "success", "response": data}
        except json.JSONDecodeError:
            print(f"MCP Server: Non-JSON response from {url}. Status: {response.status_code}. Content: {response.text[:200]}...")
            return {
                "status": "error",
                "error_type": "InvalidResponseFormat",
                "message": "API returned a non-JSON response.",
                "details": response.text[:500]
            }
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err}"
        try:
            error_details = response.json()
        except json.JSONDecodeError:
            error_details = response.text[:500]
        print(f"MCP Server: {error_message} - Details: {error_details}")
        return {
            "status": "error",
            "error_type": "HttpError",
            "message": str(http_err),
            "details": error_details
        }
    except requests.exceptions.RequestException as req_err:
        print(f"MCP Server: Request error occurred: {req_err}")
        return {
            "status": "error",
            "error_type": "RequestError",
            "message": str(req_err)
        }
    except Exception as e:
        print(f"MCP Server: An unexpected error occurred: {e}")
        return {
            "status": "error",
            "error_type": "ServerError",
            "message": f"An unexpected server error occurred: {str(e)}"
        }

# --- Tool Registration (no decorator, use add_tool) ---
def get_ipo_data():
    return _make_api_request("/ipo")
mcp.add_tool(get_ipo_data, description="Fetches Initial Public Offering (IPO) data from stock.indianapi.in.")

def get_news_data(query: str = None, symbol: str = None):
    params = {}
    if query:
        params['q'] = query
    if symbol:
        params['symbol'] = symbol
    return _make_api_request("/news", params=params or None)
mcp.add_tool(get_news_data, description="Fetches latest news data from stock.indianapi.in. Optionally filter by query or symbol.")

def get_stock_details(name: str):
    return _make_api_request("/stock", params={"name": name})
mcp.add_tool(get_stock_details, description="Fetches details for a specific stock from stock.indianapi.in. Uses correct parameter name: name.")

def get_trending_stocks():
    return _make_api_request("/trending")
mcp.add_tool(get_trending_stocks, description="Fetches currently trending stocks from stock.indianapi.in.")

def get_financial_statement(stock_name: str, 
                            stats: str, statement_type: str = "income", period: str = "annual"):
    params = {"stock_name": stock_name, "stats": stats, "type": statement_type, "period": period}
    return _make_api_request("/statement", params=params)
mcp.add_tool(get_financial_statement, description="Fetches financial statements for a specific stock from stock.indianapi.in. Includes required parameters: stock_name and stats.")

def get_commodities_data(commodity_name: str = None):
    params = {}
    if commodity_name:
        params['name'] = commodity_name
    return _make_api_request("/commodities", params=params or None)
mcp.add_tool(get_commodities_data, description="Fetches current data for various commodities from stock.indianapi.in.")

def get_mutual_funds_data(category: str = None):
    params = {}
    if category:
        params['category'] = category
    return _make_api_request("/mutual_funds", params=params or None)
mcp.add_tool(get_mutual_funds_data, description="Fetches data on mutual funds from stock.indianapi.in.")

def get_price_shockers_data():
    return _make_api_request("/price_shockers")
mcp.add_tool(get_price_shockers_data, description="Fetches data on stocks with significant price changes from stock.indianapi.in.")

def get_bse_most_active_stocks():
    return _make_api_request("/BSE_most_active")
mcp.add_tool(get_bse_most_active_stocks, description="Fetches the most active stocks on the BSE from stock.indianapi.in.")

def get_nse_most_active_stocks():
    return _make_api_request("/NSE_most_active")
mcp.add_tool(get_nse_most_active_stocks, description="Fetches the most active stocks on the NSE from stock.indianapi.in.")

def get_historical_stock_data(symbol: str, from_date: str, to_date: str, interval: str = "1d"):
    params = {
        "symbol": symbol,
        "from": from_date,
        "to": to_date,
        "interval": interval
    }
    return _make_api_request("/historical_data", params=params)
mcp.add_tool(get_historical_stock_data, description="Fetches historical price data for a stock from stock.indianapi.in.")

def search_by_industry(industry_query: str):
    return _make_api_request("/industry_search", params={"query": industry_query})
mcp.add_tool(search_by_industry, description="Searches for companies or stocks within a specific industry from stock.indianapi.in.")

def get_stock_forecasts(symbol: str):
    return _make_api_request("/stock_forecasts", params={"symbol": symbol})
mcp.add_tool(get_stock_forecasts, description="Fetches analyst stock forecasts or price targets for a specific stock from stock.indianapi.in.")

def get_historical_stats(stock_name: str, stats: str = "volatility"):
    params = {"stock_name": stock_name, "stats": stats}
    return _make_api_request("/historical_stats", params=params)
mcp.add_tool(get_historical_stats, description="Fetches historical statistical data for a stock from stock.indianapi.in. Uses correct parameter names: stock_name and stats.")

def get_corporate_actions(symbol: str, action_type: str = None):
    params = {"symbol": symbol}
    if action_type:
        params["type"] = action_type
    return _make_api_request("/corporate_actions", params=params)
mcp.add_tool(get_corporate_actions, description="Fetches corporate actions data for a stock from stock.indianapi.in.")

def search_mutual_funds(query: str, category: str = None):
    params = {"q": query}
    if category:
        params["category"] = category
    return _make_api_request("/mutual_fund_search", params=params)
mcp.add_tool(search_mutual_funds, description="Searches for mutual funds based on a query from stock.indianapi.in.")

def get_stock_target_price(symbol: str):
    return _make_api_request("/stock_target_price", params={"symbol": symbol})
mcp.add_tool(get_stock_target_price, description="Fetches the target price for a specific stock from stock.indianapi.in.")

def get_mutual_fund_details(scheme_code: str):
    return _make_api_request("/mutual_funds_details", params={"scheme_code": scheme_code})
mcp.add_tool(get_mutual_fund_details, description="Fetches detailed information for a specific mutual fund from stock.indianapi.in.")

def get_recent_announcements(symbol: str = None):
    params = {}
    if symbol:
        params["symbol"] = symbol
    return _make_api_request("/recent_announcements", params=params or None)
mcp.add_tool(get_recent_announcements, description="Fetches recent announcements for a stock or the market from stock.indianapi.in.")

def fetch_52_week_high_low_data(range_type: str = "high", exchange: str = None):
    params = {"type": range_type}
    if exchange:
        params["exchange"] = exchange
    return _make_api_request("/fetch_52_week_high_low_data", params=params)
mcp.add_tool(fetch_52_week_high_low_data, description="Fetches stocks near their 52-week high or low from stock.indianapi.in.")

if __name__ == "__main__":
    if not os.getenv(API_KEY_ENV_VAR):
        print(f"CRITICAL WARNING: Environment variable '{API_KEY_ENV_VAR}' for the API key is NOT SET.")
        print("The server will run, but ALL API calls will fail with authentication errors.")
        print(f"Please set it: export {API_KEY_ENV_VAR}=\"YOUR_API_KEY_HERE\"")
    if API_BASE_URL == "https://api.examplefinance.com/v1" and API_BASE_URL_DEFAULT != API_BASE_URL :
        print(f"WARNING: API_BASE_URL is set to a generic placeholder '{API_BASE_URL}'.")
        print(f"The script will attempt to use '{API_BASE_URL_DEFAULT}' from your example snippet.")
        print(f"If this is incorrect, please set the 'FINANCE_API_BASE_URL' environment variable.")
    print(f"Finance MCP server starting. Using API base URL: {API_BASE_URL}")
    print(f"Ensure '{API_KEY_ENV_VAR}' environment variable is set with your key for stock.indianapi.in.")
    mcp.run()
    print("Finance MCP server stopped.")