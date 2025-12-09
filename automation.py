# automation.py (FIXED COOKIE FETCH LOGIC)
import requests
import re
import json
from datetime import datetime

# --- Configuration ---
# TRYING THE STREAM ORIGIN DOMAIN, as it might be required for the cookie to be set
AUTH_URL = "https://mprod-cdn.toffeelive.com/live/match-asiacup/master_1300.m3u8" 
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # The referer MUST be the official website
    "Referer": "https://toffeelive.com/", 
    "Origin": "https://toffeelive.com",
    "Accept": "*/*",
}
CHANNEL_INPUT_FILE = "channels_with_cookies.json" 
M3U_OUTPUT_FILE = "playlist.m3u"
# ---------------------

def get_fresh_cookie():
    """Fetches a new Edge-Cache-Cookie."""
    print(f"Attempting to fetch a fresh cookie from: {AUTH_URL}...")
    try:
        # Use GET request for stream link, as HEAD might not trigger the necessary process
        response = requests.get(AUTH_URL, headers=HEADERS, allow_redirects=True, timeout=10)

        # 1. Check Set-Cookie header (most common method)
        cookie_header = response.headers.get("Set-Cookie")
        if cookie_header:
            match = re.search(r'(Edge-Cache-Cookie=[^;]+)', cookie_header)
            if match:
                print("✅ Success! New cookie fetched from Set-Cookie header.")
                return match.group(0)

        # 2. Check the response body (if the server returns a temporary page with an embedded cookie)
        # This is a fallback and usually not necessary, but good to check.
        if "Edge-Cache-Cookie" in response.text:
            print("⚠️ Warning: Cookie found in response body. This method is unreliable.")

        print(f"❌ Error: 'Edge-Cache-Cookie' not found in Set-Cookie header after checking {AUTH_URL}.")
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
        name = channel.get("name", "Unknown Channel")
        link = channel.get("link", "")
        logo = channel.get("logo", "")
        
        if not link:
            continue
            
        m3u_content += f"#EXTINF:-1 tvg-name=\"{name}\" tvg-logo=\"{logo}\" group-title=\"TOFFEE\",{name}\n"
        # CRITICAL: Embed the cookie as a header for the player to use
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
        # If cookie retrieval fails, we still try to generate the playlist
        # using the OLD cookie value from the JSON file, as a last resort.
        print("Attempting M3U generation with old cookie as fallback...")
        try:
             with open(CHANNEL_INPUT_FILE, "r") as f:
                 channels = json.load(f)
             if channels and "cookie" in channels[0]:
                 fallback_cookie = channels[0]["cookie"]
                 generate_m3u(fallback_cookie)
        except Exception:
             print("Fallback failed. Aborting M3U generation.")

