import json
import os
import asyncio
from playwright.async_api import async_playwright

# You must replace this with a current, long-lived cookie. 
# The script will use this if the attempt to get a new cookie fails.
FALLBACK_COOKIE = "URLPrefix=aHR0cHM6Ly9ibGRjbXByb2QtY2RuLnRvZmZlZWxpdmUuY29t:Expires=1765466887:KeyName=prod_linear:Signature=3jtv43bnVzhiEaGYYgWRJKQEnO64dPPqLNKkCEwBvPae749Wit2jSGkEaosqZsTXlor5CSnnCDgAO6VeW3NKDQ"

# --- Main Logic ---

async def get_fresh_cookie(proxy_server=None):
    """
    Attempts to get a fresh Edge-Cache-Cookie by simulating a web browser visit.
    
    NOTE: This will likely require a regional proxy to succeed.
    """
    
    print("🚀 Starting Playwright browser simulation to get fresh cookie...")
    
    # Configure Playwright launch options
    launch_options = {}
    if proxy_server:
        launch_options['proxy'] = {'server': proxy_server}
        print(f"   Using proxy: {proxy_server}")

    new_cookie = None
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(**launch_options)
            page = await browser.new_page()

            # Listen for the specific network response that contains the cookie
            async def handle_response(response):
                nonlocal new_cookie
                
                # Check for the key network endpoint (this might need adjusting)
                if "cdn.toffeelive.com" in response.url:
                    set_cookie_header = response.request.headers.get("cookie")
                    if set_cookie_header and "Edge-Cache-Cookie" in set_cookie_header:
                        # Find the actual Edge-Cache-Cookie value
                        for item in set_cookie_header.split(';'):
                            if 'Edge-Cache-Cookie' in item:
                                new_cookie = item.strip().split('=')[1]
                                print(f"✅ Found fresh cookie via network intercept.")
                                # Once found, we can stop the navigation
                                await browser.close()
                                return

            page.on("request", handle_response)

            # Navigate to a simple page that triggers the cookie logic
            await page.goto("https://toffeelive.com/", wait_until="networkidle")
            
            # Wait a few seconds to ensure all scripts run before giving up
            await asyncio.sleep(5) 

            await browser.close()

    except Exception as e:
        print(f"❌ Playwright attempt failed. Error: {e}")
        pass
        
    return new_cookie

def generate_m3u(current_cookie):
    """Generates the M3U file using the provided cookie."""
    
    try:
        # 1. Load the channel data from the JSON file
        with open('channels_with_cookies.json', 'r', encoding='utf-8') as f:
            channels = json.load(f)

        m3u_content = "#EXTM3U\n"
        
        # 2. Build the M3U playlist content
        for channel in channels:
            m3u_content += f"#EXTINF:-1 tvg-name=\"{channel['name']}\" tvg-logo=\"{channel['logo']}\" group-title=\"TOFFEE\",{channel['name']}\n"
            # Insert the current cookie into the header line
            m3u_content += f"#EXT-HTTP-HEADER:Cookie: Edge-Cache-Cookie={current_cookie}\n"
            m3u_content += f"{channel['link']}\n"

        # 3. Write the M3U file
        with open('playlist.m3u', 'w', encoding='utf-8') as f:
            f.write(m3u_content)

        print("✅ Successfully generated playlist.m3u.")

    except FileNotFoundError:
        print("❌ Fatal Error: 'channels_with_cookies.json' not found. Aborting.")
        # Exit with error code 1 so the job fails visibly
        exit(1)
    except Exception as e:
        print(f"❌ Error during M3U generation: {e}")
        exit(1)

async def main():
    # Attempt to use a proxy defined in GitHub Secrets (optional but highly recommended)
    proxy_url = os.environ.get('PROXY_URL')
    
    # 1. Try to get a new cookie using the browser simulation (with proxy if available)
    new_cookie = await get_fresh_cookie(proxy_url)

    if new_cookie:
        print("✅ Using newly fetched cookie.")
        final_cookie = new_cookie
    else:
        print("❌ Failed to retrieve fresh cookie.")
        print("Fallback: Using hardcoded long-lived cookie.")
        final_cookie = FALLBACK_COOKIE

    # 2. Generate the M3U file with the best available cookie
    generate_m3u(final_cookie)

if __name__ == "__main__":
    # Note: asyncio is required for Playwright's async functions
    asyncio.run(main())
