import asyncio
from playwright.async_api import async_playwright
import os
import json
from datetime import datetime

# Whitelist
WHITELISTED_DOMAINS = ["sbimf.com", "sebi.gov.in", "amfiindia.com", "indmoney.com"]

# Target Funds Data
FUNDS_DATA = [
    # Official SBI MF Links
    {
        "name": "SBI Large Cap Fund (Official)",
        "url": "https://www.sbimf.com/sbimf-scheme-details/sbi-large-cap-fund-(formerly-known-as-sbi-bluechip-fund)-43"
    },
    {
        "name": "SBI Flexicap Fund (Official)",
        "url": "https://www.sbimf.com/sbimf-scheme-details/SBI-Flexicap-Fund-39"
    },
    {
        "name": "SBI ELSS Tax Saver Fund (Official)",
        "url": "https://www.sbimf.com/sbimf-scheme-details/SBI-ELSS-Tax-Saver-Fund-(formerly-known-as-SBI-Long-Term-Equity-Fund)-3"
    },
    {
        "name": "SBI Small Cap Fund (Official)",
        "url": "https://www.sbimf.com/sbimf-scheme-details/SBI-Small-Cap-Fund-329"
    },
    {
        "name": "SBI Midcap Fund (Official)",
        "url": "https://www.sbimf.com/sbimf-scheme-details/SBI-Midcap-Fund-34"
    },
    # INDMoney Supplemental Links
    {
        "name": "SBI Bluechip Fund (INDMoney)",
        "url": "https://www.indmoney.com/mutual-funds/sbi-bluechip-fund-direct-growth-3046"
    },
    {
        "name": "SBI Flexicap Fund (INDMoney)",
        "url": "https://www.indmoney.com/mutual-funds/sbi-flexicap-fund-direct-growth-3249"
    },
    {
        "name": "SBI Long Term Equity Fund (INDMoney)",
        "url": "https://www.indmoney.com/mutual-funds/sbi-long-term-equity-fund-direct-growth-2754"
    },
    {
        "name": "SBI Small Cap Fund (INDMoney)",
        "url": "https://www.indmoney.com/mutual-funds/sbi-small-cap-fund-direct-plan-growth-3603"
    },
    {
        "name": "SBI Midcap Fund (INDMoney)",
        "url": "https://www.indmoney.com/mutual-funds/sbi-midcap-fund-direct-growth-3129"
    }
]

async def scrape_page(url, filename, data_dir="phase1/data/raw"):
    if not any(domain in url for domain in WHITELISTED_DOMAINS):
        print(f"ERROR: Domain not allowed: {url}")
        return False

    os.makedirs(data_dir, exist_ok=True)
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            
            print(f"Scraping {url}...")
            # We use a longer timeout and wait_until="load" because "networkidle" can be flaky on heavy sites
            await page.goto(url, wait_until="load", timeout=90000)
            await page.wait_for_timeout(5000) # Wait for JS content to render
            
            # Content extraction
            content = await page.evaluate("() => document.body.innerText")
            
            if "404" in content or "Oops!" in content:
                print(f"WARNING: Page might be a 404: {url}")

            filepath = os.path.join(data_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Source URL: {url}\n")
                f.write(f"Scraped Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n")
                f.write(content)
            
            await browser.close()
            print(f"Successfully saved to {filepath}")
            return True
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return False

async def main():
    results = []
    for fund in FUNDS_DATA:
        filename = fund["name"].lower().replace(" ", "_") + ".txt"
        success = await scrape_page(fund["url"], filename)
        results.append({"fund": fund["name"], "url": fund["url"], "success": success})
    
    with open("phase1/data/raw/manifest.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("\nPhase 1 Scraping Complete.")

if __name__ == "__main__":
    asyncio.run(main())
