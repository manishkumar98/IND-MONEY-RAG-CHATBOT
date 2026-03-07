import asyncio
from playwright.async_api import async_playwright
import os

WHITELISTED_DOMAINS = ["sbimf.com", "sebi.gov.in", "amfiindia.com"]

async def scrape_fund_page(url):
    if not any(domain in url for domain in WHITELISTED_DOMAINS):
        print(f"Skipping non-whitelisted domain: {url}")
        return None
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        # Wait for content to load
        await page.wait_for_timeout(2000)
        content = await page.content()
        await browser.close()
        return content

def save_to_raw(filename, content):
    os.makedirs("data/raw", exist_ok=True)
    with open(f"data/raw/{filename}", "w") as f:
        f.write(content)

# Example usage skeleton
if __name__ == "__main__":
    # urls = [...]
    # asyncio.run(main(urls))
    pass
