import os
import json
import asyncio
from playwright.async_api import async_playwright

# --- Configuration (Channel Data and Cookies) ---

# The long-lived cookie value for the standard channels (used as a fallback)
# Note: This is JUST the value part, excluding "Edge-Cache-Cookie="
FALLBACK_COOKIE_VALUE = "URLPrefix=aHR0cHM6Ly9ibGRjbXByb2QtY2RuLnRvZmZlZWxpdmUuY29t:Expires=1765466887:KeyName=prod_linear:Signature=3jtv43bnVzhiEaGYYgWRJKQEnO64dPPqLNKkCEwBvPae749Wit2jSGkEaosqZsTXlor5CSnnCDgAO6VeW3NKDQ"
# The long-lived cookie value for the live event channels (mprod-cdn)
FALLBACK_EVENT_COOKIE_VALUE = "URLPrefix=aHR0cHM6Ly9tcHJvZC1jZG4udG9mZmVlbGl2ZS5jb20:Expires=1765344488:KeyName=prod_live_events:Signature=l2ONZZt0pW1y_4Ri3mNH-X1UCdOr7oFUqkwX4u2bhS6FaYQhP4fwqy7VojcHVhxkbnnqWu1T0UAru06_PTaxBA"
# The core domain prefix for standard channels that need cookie replacement
MAIN_DOMAIN_PREFIX = "https://bldcmprod-cdn.toffeelive.com"


# Channel data in the user-specified JSON format (from your uploaded file)
CHANNELS_JSON = [
  {
    "name": "TOFFEE Sports VIP",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sports_highlights/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/19779/logo/240x240/mobile_logo_975410001725875598.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "TOFFEE Movies VIP",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/toffee_movie/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/2708/logo/240x240/mobile_logo_724353001725875591.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "TOFFEE Dramas VIP",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/toffee_drama/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/44878/logo/240x240/mobile_logo_764950001725875605.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "CNN VIP",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/cnn/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/333/logo/240x240/mobile_logo_146607001735536058.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Somoy TV",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/somoy_tv/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com//Xi_Ga5oBNnOkwJLWkhKP/posters/ef2899d5-1ae0-4fee-aee5-45f9b0b3ba80.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Jamuna TV",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/jamuna_tv/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/PiL635oBEef-9-uV2uCe/posters/36f380e0-6c71-4b27-a73b-2afb3ce7e982.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "ATN News",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/atn_news/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/NCLx35oBEef-9-uVh-Dg/posters/af9773c7-7971-41a2-9b78-121fcb240c48.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "ATN Bangla",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/atn_bangla/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/MCLv35oBEef-9-uVH-D2/posters/0d1e571c-ebb2-4277-9814-760a4f1603a6.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Channel i",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/channel_i/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/qnv835oBcqxnFHJBuQcB/posters/348dfac3-c1e0-485d-a72b-3d282c9e2c73.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Ekhon TV",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/ekhon_tv/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/o3v235oBcqxnFHJBkAdC/posters/159af631-796d-4342-a2a7-c272f32bcd32.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Ekattor TV",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/ekattor_tv/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com//PS_La5oBNnOkwJLWLRN_/posters/e8c444fd-ee3b-4bf3-bb0a-f969bc295f82.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Euro Sport HD",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/euro_sports_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/4388/logo/240x240/mobile_logo_422191001674119624.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "ICC Test Championship Highlights",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/icc_wtc_final/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/f_webp,w_400,q_100/PnZefJcBcqxnFHJBoxca/posters/955ae898-8336-4936-8d78-c6b8866e35f7.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "SONY SPORTS TEN 1 HD",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_1_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/603/logo/240x240/mobile_logo_237244001666780563.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "SONY SPORTS TEN 2 HD",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_2_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/604/logo/240x240/mobile_logo_093449001666780976.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "SONY SPORTS TEN 5 HD",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_5_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/606/logo/240x240/mobile_logo_689539001672145843.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "SONY TEN Cricket",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/ten_cricket/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/301891/logo/240x240/mobile_logo_578686001735197654.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  # Live Event channels (mprod-cdn.toffeelive.com) have a separate, event-specific cookie.
  # We will rely on the hardcoded event cookie for these.
  {
    "name": "EPL channel 1",
    "link": "https://mprod-cdn.toffeelive.com/live/match-1/index.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_256,q_75,f_webp/JS1AqZgBNnOkwJLWlwg-/posters/08617b27-2af1-4035-bcc3-d054ce42ca4b.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "EPL channel 2",
    "link": "https://mprod-cdn.toffeelive.com/live/match-2/index.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_256,q_75,f_webp/Mi1QqZgBNnOkwJLWxggo/posters/3e9d4d0a-a346-4b39-92b5-13e9238ad240.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "EPL channel 3",
    "link": "https://mprod-cdn.toffeelive.com/live/match-3/index.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_256,q_75,f_webp/Pi1TqZgBNnOkwJLWVggf/posters/d0bb78b5-4690-4c12-9c7b-e785eb8d7336.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "EPL channel 4",
    "link": "https://mprod-cdn.toffeelive.com/live/match-4/index.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_256,q_75,f_webp/OyEz-ZgBEef-9-uVnhcx/posters/f2143475-cf44-441a-b55d-58b2b5569aa5.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "EPL channel 5",
    "link": "https://mprod-cdn.toffeelive.com/live/match-5/index.m3u8",
    "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJluFppSx7qkGdkjkiIQ5QyxlqJ9zeWszpJUQibhrbSw&s=10",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "EPL channel 6",
    "link": "https://mprod-cdn.toffeelive.com/live/match-6/index.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/6y_b4poBNnOkwJLWmn7X/posters/c1440521-da52-4cf7-b137-dd38d1de083a.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "BFL Live 1",
    "link": "https://mprod-cdn.toffeelive.com/live/match-11/index.m3u8",
    "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRl6-ZPZ6UT3YhXilJF9fxtHzCqIt6mD71Dmg2_D-ZUsg&s=10",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "BFL Live 2",
    "link": "https://mprod-cdn.toffeelive.com/live/match-12/index.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com//MXnGgJkBcqxnFHJBILyR/posters/035a24dd-4d88-4fc2-99a1-275a5bc97bf5.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "BFL Live 3",
    "link": "https://mprod-cdn.toffeelive.com/live/match-13/index.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com//LnlKhJkBcqxnFHJBU8GM/posters/74e6a7bb-f850-4ec5-991f-7a882b04db37.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "BFL Live 4",
    "link": "https://mprod-cdn.toffeelive.com/live/match-18/index.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com//Ey9jtJoBNnOkwJLWw06R/posters/4e83252b-223d-42a6-a56b-8598aa17e2e8.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "BAN vs IRE",
    "link": "https://mprod-cdn.toffeelive.com/live/match-asiacup/master_1300.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/ty_tbJoBNnOkwJLWsRZG/posters/5e49e175-0e7c-4af4-be13-6711e59d448d.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "IND vs SA",
    "link": "https://mprod-cdn.toffeelive.com/live/match-asiacup-2/master_1300.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/TSK2e5oBEef-9-uVH5vw/posters/5cc6444f-88c9-4a08-a934-39588cec6040.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_EVENT_COOKIE_VALUE
  },
  {
    "name": "Cartoon Network HD",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/cartoon_network_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/26942/logo/240x240/mobile_logo_443429001678950505.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Cartoon Network",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/cartoon_network_sd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/27232/logo/240x240/mobile_logo_320294001679201065.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Pogo",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/pogo_sd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/27159/logo/240x240/mobile_logo_740957001679201029.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Discovery Kids",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovery_kids/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/611/logo/240x240/mobile_logo_430542001673177743.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "SONY YAY VIP",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonyyay/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/612/logo/240x240/mobile_logo_091186001666784752.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Zee Bangla VIP",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_bangla/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/340/logo/240x240/mobile_logo_094417001655891123.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Zee Anmol",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_anmol/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/f_webp,w_400,q_100/7x0Jd5YBEef-9-uVv_Gy/posters/f630a176-73cc-48d7-94cf-69ba0d201b36.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Zing",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zing_sd/playlist.m3u8",
    "logo": "https://assets-prod.services.toffeelive.com/f_webp,w_400,q_100/DK8dd5YBrjBfS2_Ru22e/posters/a89a1e2e-677c-4a8a-9a66-dff5e0b921c8.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Hum TV",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_tv/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/303937/logo/240x240/mobile_logo_880134001738072763.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Hum Masala",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_masala/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/303947/logo/240x240/mobile_logo_203789001738235600.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Hum Sitarey",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/hum_sitaray/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/303948/logo/240x240/mobile_logo_350939001738236112.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "SONY BBC EARTH HD VIP",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonybbc_earth_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/670/logo/240x240/mobile_logo_892290001738663264.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Discovery HD",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovery_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/18093/logo/240x240/mobile_logo_868363001673181438.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "Investigation Discovery HD",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/discovary_investigation_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/18094/logo/240x240/mobile_logo_154805001673178308.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
  {
    "name": "&TV HD",
    "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/and_tv_hd/playlist.m3u8",
    "logo": "https://images.toffeelive.com/images/program/801/logo/240x240/mobile_logo_774900001655894178.png",
    "cookie": "Edge-Cache-Cookie=" + FALLBACK_COOKIE_VALUE
  },
]


async def get_fresh_cookie(proxy_server: str) -> str | None:
    """Attempts to launch Playwright and fetch a new Edge-Cache-Cookie value."""
    print(f"Using proxy: {'***' if proxy_server else 'None'}")
    # The URL to visit to trigger the cookie set
    TARGET_URL = 'https://toffeelive.com/'

    launch_options = {
        'headless': True, 
        'args': [
            '--no-sandbox', 
            '--disable-setuid-sandbox'
        ]
    }
    
    # Configure proxy if available
    if proxy_server:
        # Playwright accepts the full URL string including the socks5:// or http:// scheme
        launch_options['proxy'] = {'server': proxy_server} 
        print(f"Attempting connection via proxy: {proxy_server.split('//')[-1].split('@')[-1]}")

    try:
        async with async_playwright() as playwright:
            print("🚀 Starting Playwright browser simulation to get fresh cookie...")

            # Launch browser with options
            browser = await playwright.chromium.launch(**launch_options)
            
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to the page, waiting for network to be idle
            print(f"Navigating to \"{TARGET_URL}\", waiting until \"networkidle\"")
            await page.goto(TARGET_URL, wait_until='networkidle', timeout=30000) # Increased timeout
            
            # Extract the cookie for the specific CDN domain
            cookies = await context.cookies()
            fresh_cookie_value = None
            for cookie in cookies:
                # The primary CDN cookie is usually set for the main bldcmprod domain
                if cookie['name'] == 'Edge-Cache-Cookie' and MAIN_DOMAIN_PREFIX in cookie['domain']:
                    fresh_cookie_value = cookie['value']
                    break
            
            await browser.close()

            if fresh_cookie_value:
                print("✅ Successfully retrieved fresh cookie.")
                return fresh_cookie_value
            else:
                print("❌ Edge-Cache-Cookie not found after navigation.")
                return None
            
    except Exception as e:
        print(f"❌ Playwright attempt failed. Error: {type(e).__name__}: {e}")
        return None

def generate_json_playlist(channel_data, final_cookie_value: str, final_event_cookie_value: str):
    """Generates the JSON playlist by updating all cookies with the fresh/fallback value."""
    # We clone the data to avoid modifying the global constant
    updated_channels = json.loads(json.dumps(channel_data))
    
    # Ensure the cookie value starts with the "Edge-Cache-Cookie=" prefix for the JSON file
    # We strip it and then add the new value back.
    
    # Re-insert the "Edge-Cache-Cookie=" prefix for the channel objects
    main_cookie_string = f"Edge-Cache-Cookie={final_cookie_value}"
    event_cookie_string = f"Edge-Cache-Cookie={final_event_cookie_value}"


    for channel in updated_channels:
        # Check if the channel is a Live Event channel (identified by 'mprod-cdn' in the link)
        if 'mprod-cdn.toffeelive.com' in channel['link']:
            # Use the hardcoded event cookie
            channel['cookie'] = event_cookie_string
        else:
            # Use the newly fetched (or fallback) main cookie
            channel['cookie'] = main_cookie_string

    # Write the JSON array to the playlist file.
    with open('playlist.m3u', 'w', encoding='utf-8') as f:
        # The user's file was pretty-printed, so we will use indent=2
        json.dump(updated_channels, f, indent=2)

    print("✅ Successfully generated JSON playlist.m3u")


async def main():
    proxy_url = os.environ.get('PROXY_URL')
    
    # 1. Attempt to get a fresh standard cookie
    fresh_cookie_value = await get_fresh_cookie(proxy_url)

    # 2. Determine which cookie value to use for the main channels
    if fresh_cookie_value:
        final_cookie_value = fresh_cookie_value
    else:
        # If fetch fails (due to proxy or geo-block), use the long-lived fallback
        print("Fallback: Using hardcoded long-lived cookie for main channels.")
        final_cookie_value = FALLBACK_COOKIE_VALUE
    
    # 3. Use the hardcoded event cookie for live events, as they have a different signature
    final_event_cookie_value = FALLBACK_EVENT_COOKIE_VALUE
    
    # 4. Generate the JSON playlist with the current cookie
    generate_json_playlist(CHANNELS_JSON, final_cookie_value, final_event_cookie_value)

if __name__ == "__main__":
    asyncio.run(main())
