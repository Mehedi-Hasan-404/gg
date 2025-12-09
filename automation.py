# automation.py
import requests
import re
import json
from datetime import datetime

# --- Configuration ---
AUTH_URL = "https://toffeelive.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": AUTH_URL,
    "Origin": "https://toffeelive.com",
    "Accept": "*/*",
}
# Input file (contains links and placeholder cookie)
CHANNEL_INPUT_FILE = "channels_with_cookies.json" 
# Output file (the playlist you requested)
M3U_OUTPUT_FILE = "playlist.m3u"
# ---------------------

def get_fresh_cookie():
    """Fetches a new Edge-Cache-Cookie."""
    print("Attempting to fetch a fresh cookie...")
    try:
        response = requests.head(AUTH_URL, headers=HEADERS, allow_redirects=True, timeout=10)
        cookie_header = response.headers.get("Set-Cookie")

        if not cookie_header:
            print(f"ERROR: No 'Set-Cookie' header received (Status: {response.status_code}).")
            return None

        match = re.search(r'(Edge-Cache-Cookie=[^;]+)', cookie_header)
        
        if match:
            new_cookie = match.group(0)
            print("✅ Success! New cookie fetched.")
            return new_cookie
        else:
            print("❌ Error: 'Edge-Cache-Cookie' not found in Set-Cookie header.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred during cookie fetch: {e}")
        return None

def generate_m3u(new_cookie):
    """Generates the M3U playlist file with the fresh cookie embedded."""
    try:
        with open(CHANNEL_INPUT_FILE, "r") as f:
            channels = json.load(f)
    except FileNotFoundError:
        print(f"Error: {CHANNEL_INPUT_FILE} not found. Cannot proceed.")
        return False
    except json.JSONDecodeError:
        print(f"Error: Could not parse {CHANNEL_INPUT_FILE}. Check JSON syntax.")
        return False

    m3u_content = "#EXTM3U\n"
    
    for channel in channels:
        # 1. Prepare M3U tags
        name = channel.get("name", "Unknown Channel")
        link = channel.get("link", "")
        logo = channel.get("logo", "")
        
        if not link:
            continue
            
        # 2. Add EXTINF line with logo and name
        m3u_content += f"#EXTINF:-1 tvg-name=\"{name}\" tvg-logo=\"{logo}\" group-title=\"TOFFEE\",{name}\n"
        
        # 3. Add stream URL with embedded cookie header
        # The player must support this #EXT-HTTP-HEADER structure
        m3u_content += f"#EXT-HTTP-HEADER:Cookie: {new_cookie}\n"
        m3u_content += f"{link}\n"
        
    try:
        with open(M3U_OUTPUT_FILE, "w") as f:
            f.write(m3u_content)
        print(f"✅ Successfully generated {M3U_OUTPUT_FILE}.")
        return True
    except Exception as e:
        print(f"Error writing M3U file: {e}")
        return False

if __name__ == "__main__":
    cookie = get_fresh_cookie()
    
    if cookie:
        generate_m3u(cookie)
    else:
        print("Skipping M3U generation due to cookie retrieval failure.")
