# refresh_cookie.py
import requests
import re
import json
from datetime import datetime

# --- Configuration (Must match successful authentication headers) ---
AUTH_URL = "https://toffeelive.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": AUTH_URL,
    "Origin": "https://toffeelive.com",
    "Accept": "*/*",
}
CHANNEL_FILE = "channels_with_cookies.json"
# -----------------------------------------------------------------

def get_fresh_cookie():
    """Fetches a new Edge-Cache-Cookie by hitting the ToffeeLive main page."""
    print("Attempting to fetch a fresh cookie...")
    try:
        # Use HEAD request as it is faster and only needs headers
        response = requests.head(AUTH_URL, headers=HEADERS, allow_redirects=True, timeout=10)
        cookie_header = response.headers.get("Set-Cookie")

        if not cookie_header:
            print(f"ERROR: No 'Set-Cookie' header received (Status: {response.status_code}).")
            return None

        # Extract the Edge-Cache-Cookie using regex
        match = re.search(r'(Edge-Cache-Cookie=[^;]+)', cookie_header)
        
        if match:
            new_cookie = match.group(0)
            print(f"✅ Success! New cookie fetched.")
            return new_cookie
        else:
            print("❌ Error: 'Edge-Cache-Cookie' not found in Set-Cookie header.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred during cookie fetch: {e}")
        return None

def update_json_file(new_cookie):
    """Reads the JSON file, replaces all cookie values, and saves the file."""
    try:
        with open(CHANNEL_FILE, "r") as f:
            channels = json.load(f)
    except FileNotFoundError:
        print(f"Error: {CHANNEL_FILE} not found.")
        return False
    except json.JSONDecodeError:
        print(f"Error: Could not parse {CHANNEL_FILE}. Ensure it is valid JSON.")
        return False

    updates_made = 0
    for channel in channels:
        # Check if the channel object has a 'cookie' key
        if "cookie" in channel:
            # Only update if the cookie has changed
            if channel["cookie"] != new_cookie:
                channel["cookie"] = new_cookie
                updates_made += 1

    if updates_made > 0:
        print(f"Total of {updates_made} channel cookies updated.")
        # Save the updated list, formatted nicely
        with open(CHANNEL_FILE, "w") as f:
            json.dump(channels, f, indent=2)
        return True
    else:
        print("No updates needed. Cookie value is the same.")
        return False

if __name__ == "__main__":
    cookie = get_fresh_cookie()
    
    if cookie:
        # Check expiration date for logging
        expiry_match = re.search(r'Expires=(\d+)', cookie)
        if expiry_match:
            timestamp = int(expiry_match.group(1))
            expiry_date = datetime.fromtimestamp(timestamp)
            print(f"   New Expiry: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
        update_json_file(cookie)
    else:
        print("Aborting file update due to cookie retrieval failure.")

