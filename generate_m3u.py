# generate_m3u.py
import json

# Replace 'hh' with the name of your deployed Worker if it's different
WORKER_DOMAIN = "hh.workers.dev" 
BASE_URL = "https://mprod-cdn.toffeelive.com"

# The Worker's URL for proxying needs the TARGET_ORIGIN's full path
# Example: https://hh.workers.dev/cdn/live/sports_highlights/playlist.m3u8

def generate_playlist():
    try:
        with open("channels.json", "r") as f:
            channels = json.load(f)
    except FileNotFoundError:
        print("channels.json not found.")
        return

    m3u_content = "#EXTM3U\n"
    
    for channel in channels:
        # 1. Generate the fully proxied URL
        proxied_link = f"https://{WORKER_DOMAIN}{channel['path']}"
        
        # 2. Add M3U tags (name, logo)
        m3u_content += f"#EXTINF:-1 tvg-id=\"{channel['name']}\" tvg-name=\"{channel['name']}\" tvg-logo=\"{channel['logo']}\" group-title=\"TOFFEE\",{channel['name']}\n"
        
        # 3. Add the proxied stream link
        m3u_content += f"{proxied_link}\n"

    try:
        with open("playlist.m3u", "w") as f:
            f.write(m3u_content)
        print("✅ Successfully generated playlist.m3u")
    except Exception as e:
        print(f"Error writing M3U file: {e}")

if __name__ == "__main__":
    generate_playlist()
