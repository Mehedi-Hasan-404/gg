# automation.py (Updated with Exhaustive URL List)
import requests
import re
import json
from datetime import datetime
import sys

# --- Configuration ---
# LIST OF ALL UNIQUE LINKS from channels_with_cookies.json + the main site, 
# listed serially to maximize cookie retrieval chance.
AUTH_URLS = [
    "https://toffeelive.com/", 
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sports_highlights/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/toffee_movie/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/toffee_drama/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/cnn/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/somoy_tv/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/jamuna_tv/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/atn_news/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/atn_bangla/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/channel_i/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/ekhon_tv/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/ekattor_tv/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/euro_sports_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/icc_wtc_final/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_1_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_2_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_5_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/ten_cricket/playlist.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-1/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-2/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-3/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-4/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-5/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-6/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-11/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-12/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-13/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-18/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-asiacup/index.m3u8",
    "https://mprod-cdn.toffeelive.com/live/match-asiacup-2/index.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/cartoon_network_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/cartoon_network_sd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/pogo_sd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovery_kids/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonyyay/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_bangla/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_anmol/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zing_sd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_tv/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_masala/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_sitaray/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonyaath/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonyentertainmnt_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_entertainment/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/b4u_music/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonysab_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_tv_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_max_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_bangla_cinema/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_bollywood/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_action/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_max/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonypix_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_cafe_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/b4u_movies/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonymax_2/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_cinema_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/tlc_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/tlc_sd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/animal_planet_sd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/animal_planet_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonybbc_earth_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovery_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovery_sd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovery_science/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovery_turbo/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovary_investigation_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/and_tv_hd/playlist.m3u8",
    "https://bldcmprod-cdn.toffeelive.com/cdn/live/andpicture_hd/playlist.m3u8"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://toffeelive.com/", 
    "Origin": "https://toffeelive.com",
    "Accept": "*/*",
}
CHANNEL_INPUT_FILE = "channels_with_cookies.json" 
M3U_OUTPUT_FILE = "playlist.m3u"
# ---------------------

def get_fresh_cookie():
    """Attempts to fetch a new Edge-Cache-Cookie from a list of URLs."""
    for url in AUTH_URLS:
        print(f"Attempting to fetch cookie from: {url}...")
        try:
            # Use GET request for full page/stream load simulation
            response = requests.get(url, headers=HEADERS, allow_redirects=True, timeout=15)
            
            # 1. Check Set-Cookie header
            cookie_header = response.headers.get("Set-Cookie")
            if cookie_header:
                match = re.search(r'(Edge-Cache-Cookie=[^;]+)', cookie_header)
                if match:
                    print(f"✅ Success! New cookie fetched from {url}.")
                    return match.group(0)

            print(f"   -> Cookie not found in headers from {url}.")

        except requests.exceptions.RequestException as e:
            print(f"   -> Network error occurred accessing {url}: {e}")
            
    print("❌ FAILED to retrieve Edge-Cache-Cookie from all attempts.")
    return None

def generate_m3u(new_cookie):
    """Generates the M3U playlist file with the fresh cookie embedded."""
    try:
        with open(CHANNEL_INPUT_FILE, "r") as f:
            channels = json.load(f)
    except Exception as e:
        print(f"Error loading or parsing {CHANNEL_INPUT_FILE}: {e}")
        return False

    m3u_content = "#EXTM3U\n"
    
    for channel in channels:
        name = channel.get("name", "Unknown Channel")
        link = channel.get("link", "")
        logo = channel.get("logo", "")
        
        if not link:
            continue
            
        m3u_content += f"#EXTINF:-1 tvg-name=\"{name}\" tvg-logo=\"{logo}\" group-title=\"TOFFEE\",{name}\n"
        
        # Embed the cookie as a header for the player to use
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
        # Fallback: If cookie retrieval fails, use the old cookie from the JSON file
        print("Falling back to old cookie to avoid service interruption...")
        try:
             with open(CHANNEL_INPUT_FILE, "r") as f:
                 channels = json.load(f)
             # Get the cookie from the first channel in the JSON
             fallback_cookie = channels[0].get("cookie", "Edge-Cache-Cookie=FALLBACK_FAILED")
             if fallback_cookie != "Edge-Cache-Cookie=FALLBACK_FAILED":
                 generate_m3u(fallback_cookie)
             else:
                 print("Error: Fallback cookie not found. Aborting M3U generation.")
                 sys.exit(1)
        except Exception as e:
             print(f"Fallback failed. Aborting M3U generation. Error: {e}")
             sys.exit(1)

