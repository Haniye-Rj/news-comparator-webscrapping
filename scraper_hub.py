import os
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import re


# ==========================================
# 1. SCRAPY COMPONENT: CNN Spider
# ==========================================

class CNNSpider(scrapy.Spider):
    name = "cnn_spider"
    # Switching to a more stable live URL
    start_urls = ["https://www.cnn.com/world/middle-east"]

    def parse(self, response):
        # Your keyword dictionary (Fixed Syntax)
        iran_keywords = {
            "locations": ["Tehran", "Strait of Hormuz", "Persian Gulf", "Isfahan"],
            "figures": ["Khamenei", "Ayatollah", "Pahlavi"],
            "strategic": ["Nuclear", "Sanctions", "Proxy"],
            "conflict": ["Oil Export", "Energy Security", "Blockade", "Maritime"]
        }

        # Flatten list
        flat_list = [item for sublist in iran_keywords.values() for item in sublist]
        pattern_string = r'\b(' + '|'.join(set(flat_list)) + r')\b'
        iran_pattern = re.compile(pattern_string, re.IGNORECASE)

        # CNN headlines on the Middle East page often use 'container__headline-text'
        # but we add 'container__link' as a backup
        raw_headlines = response.css('.container__headline-text::text, a.container__link span::text').getall()
        
        filtered_headlines = [h.strip() for h in raw_headlines if iran_pattern.search(h)]
        
        # Deduplicate
        filtered_headlines = list(set(filtered_headlines))
        
        html_content = "<html><body>"
        for h in filtered_headlines:
            html_content += f"<a>{h}</a><br>"
        html_content += "</body></html>"
        
        os.makedirs("saved_pages", exist_ok=True)
        with open("saved_pages/cnn.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"\n--- Scrapy: Success! Found {len(filtered_headlines)} Iran articles on CNN ---")

# ==========================================
# 2. REQUESTS COMPONENT: IRNA
# ==========================================
def fetch_irna_with_requests():
    print("--- Requests: Fetching IRNA ---")
    url = "https://www.irna.ir/en"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            os.makedirs("saved_pages", exist_ok=True)
            with open("saved_pages/irna.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Successfully saved IRNA via Requests.")
    except Exception as e:
        print(f"Requests failed: {e}")

# ==========================================
# 3. RUNNER
# ==========================================
if __name__ == "__main__":
    # 1. Run Requests function
    fetch_irna_with_requests()

    # 2. Configure Scrapy
    process = CrawlerProcess(settings={
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "LOG_LEVEL": "INFO",  
    })

    # 3. Schedule the spider and START
    process.crawl(CNNSpider)
    process.start()  # <--- CRITICAL: The script will wait here until Scrapy finishes