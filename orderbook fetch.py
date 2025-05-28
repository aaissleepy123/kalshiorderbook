from typing import Dict, Any, Optional
from requests.models import PreparedRequest
import requests
import datetime
from main import sign_pss_text, private_key  # Assuming private_key is loaded in main

def get_headers(method: str, path: str, private_key) -> Dict[str, str]:
    """
    Generate authenticated headers for Kalshi API requests.

    Args:
        method (str): HTTP method (e.g., "GET").
        path (str): API path (e.g., "/trade-api/v2/markets/XYZ/orderbook").
        private_key: RSA private key object.

    Returns:
        Dict[str, str]: Headers for the request.
    """
    timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
    msg_string = timestamp + method + path
    sig = sign_pss_text(private_key, msg_string)
    headers = {
        'KALSHI-ACCESS-KEY': 'a952bafb-12dd-4955-9e7c-3895265e812d',
        'KALSHI-ACCESS-SIGNATURE': sig,
        'KALSHI-ACCESS-TIMESTAMP': timestamp
    }
    return headers



def fetch_orderbook_data(ticker: str, depth: Optional[int] = None) -> Dict[str, Any]:
    """
    Fetches orderbook data for a given Kalshi market ticker.

    Args:
        ticker (str): The market ticker (e.g., "WTH-NYC-25MAY27").
        depth (int, optional): Depth of the orderbook to retrieve.

    Returns:
        Dict[str, Any]: JSON response from Kalshi's orderbook API.
    """
    base_url = "https://api.elections.kalshi.com"
    path = f"/trade-api/v2/markets?series_ticker={ticker}/orderbook"

    # Prepare full URL with optional query parameters
    params = {}
    if depth is not None:
        params["depth"] = depth

    req = PreparedRequest()
    req.prepare_url(base_url + path, params)
    url = req.url

    # Generate signed headers
    headers = get_headers(method="GET", path=path, private_key=private_key)

    # Make the request
    response = requests.get(url, headers=headers)
    return response.json()


# Example usage
data = fetch_orderbook_data("KXHIGHNY", 10)
print(data)
