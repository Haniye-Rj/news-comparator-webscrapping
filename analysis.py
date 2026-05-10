import os
import re
import time
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from collections import Counter
import seaborn as sns

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as sel_exceptions
from scraper_hub import fetch_irna_with_requests, CNNSpider
# ==========================================
# 1. CONFIGURATION & MAPPING
# ==========================================
narrative_map = {
    # Added: 'anti-government', 'crackdown', 'unrest', 'mobilization'
    'Uprising/Protest': r'\b(uprising|protest|demonstration|strike|clash|activism|anti-government|crackdown|mobilization|movement|rally|dissent|unrest)\b',
    
    # Added: 'looting', 'violence', 'clashes', 'vandalism' (often used by state media to delegitimize protests)
    'Riot/Unrest': r'\b(riot|thug|unrest|chaos|vandal|sabotage|instability|looting|violence|clashes|anarchy|disruption)\b',
    
    # Added: 'extremist', 'radical', 'espionage', 'covert', 'proxy'
    'Terrorist/Agent': r'\b(terrorist|militant|spy|agent|traitor|separatist|hired|espionage|extremist|radical|covert|proxy|saboteur|insurgent)\b',
    
    # Added: 'activist', 'defender', 'amnesty', 'sanctions', 'moratorium'
    'Freedom/Rights': r'\b(freedom|rights|liberty|nobel|justice|laureate|hospitalized|activist|defender|amnesty|sanctions|moratorium|democracy|civic)\b',
    
    # Added: 'pasdaran', 'basij', 'detain', 'patrol', 'intelligence'
    'Security/IRGC': r'\b(security|order|force|guard|irgc|pasdaran|basij|sepah|police|arrest|warn|blockade|ouster|detain|patrol|intelligence|custody)\b',
    
    # Added: 'sentence', 'verdict', 'tribunal', 'convicted'
    'Execution/Hanged': r'\b(hanged|executed|punished|death penalty|judiciary|execution|sentence|verdict|tribunal|convicted|gallows)\b'
}

# Mapping for both Online and Offline modes
source_groups = {
    "irna.html": "State",
    "presstv.html": "State",
    "iranintl.html": "Independent",
    "cnn.html": "Independent"  
}

# ==========================================
# 2. ONLINE SCRAPER (Selenium)
# ==========================================
def run_online_scraper():
    """Scrapes live sites and SAVES them as HTML files for the offline analyzer."""
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    if not os.path.exists("saved_pages"):
        os.makedirs("saved_pages")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(45)
    
    urls = [
        ("https://www.irna.ir/en", "irna.html"),
        ("https://www.presstv.ir/", "presstv.html"),
        ("https://www.iranintl.com/en", "iranintl.html")
    ]

    try:
        for url, filename in urls:
            try:
                print(f"Downloading live content from {url}...")
                driver.get(url)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                time.sleep(5) # Allow JS to load
                
                # Save as local HTML file
                with open(f"saved_pages/{filename}", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
            except Exception as e:
                print(f"Error downloading {url}: {e}")
    finally:
        driver.quit()

# ==========================================
# 3. OFFLINE EXTRACTION (BeautifulSoup)
# ==========================================
def extract_headlines_offline():
    """Reads the saved HTML files and extracts titles into a DataFrame."""
    all_data = []
    folder = "saved_pages"
    
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' not found. Run Scraper first!")
        return pd.DataFrame()

    for filename, group in source_groups.items():
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):
            continue
            
        print(f"Parsing local file: {filename} ({group})...")
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            elements = soup.find_all(['h1', 'h2', 'h3', 'a'])
            
            for el in elements:
                text = el.get_text().strip()
                if len(text) > 30 and "cookie" not in text.lower():
                    all_data.append({
                        'Source': filename.replace(".html", "").upper(),
                        'Group': group,
                        'Title': text
                    })
    
    return pd.DataFrame(all_data).drop_duplicates(subset=['Title'])

# ==========================================
# 4. ANALYSIS & VISUALIZATION LOGIC
# ==========================================
def apply_narrative_mapping(df):
    def tag_text(text):
        text = str(text).lower()
        tags = [cat for cat, pat in narrative_map.items() if re.search(pat, text)]
        return ", ".join(tags) if tags else "General News"

    df['Detected_Narratives'] = df['Title'].apply(tag_text)
    return df

def generate_visuals(df):
    plot_df = df.copy()
    plot_df['Detected_Narratives'] = plot_df['Detected_Narratives'].str.split(', ')
    exploded = plot_df.explode('Detected_Narratives')
    exploded = exploded[exploded['Detected_Narratives'] != "General News"]
    
    if exploded.empty:
        print("No specific narratives found to plot.")
        return

    pivot_table = exploded.groupby(['Group', 'Detected_Narratives']).size().unstack(level=0, fill_value=0)
    
    pivot_table.plot(kind='barh', figsize=(12, 7), color=['#3498db', '#e74c3c'])
    plt.title("Narrative War: State vs Independent Media Focus", fontsize=14)
    plt.xlabel("Number of Headlines", fontsize=12)
    plt.ylabel("Thematic Category", fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# ==========================================
# 1. DATA PREPARATION
# ==========================================

# Step 1: Extract headlines from the HTML files saved by scrapers
df_raw = extract_headlines_offline()

if df_raw.empty:
    print("Error: No data found. Please run the scrapers first!")
else:
    # Step 2: Apply the narrative mapping (Regex logic)
    analyzed_df = apply_narrative_mapping(df_raw)

    # Step 3: Create a copy for statistical analysis
    # filter out 'General News' to focus on the 'Narrative War'
    stats_df = analyzed_df.copy()
    stats_df = stats_df[stats_df['Detected_Narratives'] != "General News"]

    # Step 4: Create an 'exploded' dataframe
    # This handles headlines with multiple tags (e.g., "Protest, Rights") 
    # so each tag gets its own row for accurate counting.
    stats_exploded = stats_df.copy()
    stats_exploded['Detected_Narratives'] = stats_exploded['Detected_Narratives'].str.split(', ')
    exploded = stats_exploded.explode('Detected_Narratives')

    # ==========================================
    # 2. STATISTICAL SUMMARY
    # ==========================================

    print("\n" + "="*30)
    print("      STATISTICAL SUMMARY")
    print("="*30)

    # Calculate Narrative Share as a Percentage per Group
    summary_pct = (
        exploded.groupby('Group')['Detected_Narratives']
        .value_counts(normalize=True)
        .unstack(fill_value=0) * 100
    )

    print("\n--- Narrative Share by Media Group (%) ---")
    print(summary_pct.round(2))

    # Calculate Average Headline Length (Metric for editorial style)
    stats_df['Headline_Length'] = stats_df['Title'].str.len()
    avg_len = stats_df.groupby('Group')['Headline_Length'].mean()

    print("\n--- Avg Headline Length (Characters) ---")
    print(avg_len.round(1))

    # ==========================================
    # 3. VISUALIZATIONS
    # ==========================================

    # Visualization A: The Heatmap 
    pivot_heatmap = exploded.groupby(['Source', 'Detected_Narratives']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_heatmap, annot=True, cmap="YlGnBu", fmt='g')
    plt.title("Heatmap: Narrative Frequency by News Source", fontsize=14)
    plt.xlabel("Narrative Category")
    plt.ylabel("Specific News Source")
    plt.tight_layout()
    plt.show()

    # Visualization B: The Bar Chart 
    generate_visuals(analyzed_df)

    # ==========================================
    # 4. FINAL EXPORT
    # ==========================================
    analyzed_df.to_csv("final_narrative_analysis_report.csv", index=False)
    summary_pct.to_csv("narrative_stats_summary.csv")
    print("\nSUCCESS: All charts generated and CSVs saved.")

# ==========================================
# 5. MAIN EXECUTION
# ==========================================
if __name__ == "__main__":

    # 1. DATA COLLECTION PHASE
    # Use Requests for IRNA
    fetch_irna_with_requests() 
    
    # Use Scrapy for CNN
    # Note: Scrapy needs to run in a process to handle the reactor
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        "USER_AGENT": "Mozilla/5.0",
        "LOG_LEVEL": "ERROR", 
    })
    process.crawl(CNNSpider)
    process.start() 

    # Selenium for PressTV/Live Content
    run_online_scraper()

    print("\n" + "="*40)
    print("COLLECTION COMPLETE. STARTING TRANSFORMATION...")
    print("="*40 + "\n")

    # 2. EXTRACTION PHASE (BeautifulSoup)
    df_raw = extract_headlines_offline()
    
    if not df_raw.empty:
        # 3. ANALYSIS PHASE (Regex & Pandas)
        analyzed_df = apply_narrative_mapping(df_raw)

        # 4. VISUALIZATION PHASE (Matplotlib & Seaborn)
        print("Generating Analysis Visuals...")
        generate_visuals(analyzed_df)

        # 5. FINAL OUTPUT (The project requirement)
        analyzed_df.to_csv("final_media_analysis.csv", index=False)
        
        print("\n" + "!"*30)
        print("SUCCESS: FINAL DATAFRAME CREATED")
        print(f"Total Rows: {len(analyzed_df)}")
        print("!"*30)
        
        # Display the head of the dataframe to prove it's structured
        print("\n--- DATAFRAME PREVIEW ---")
        print(analyzed_df.head(10))
    else:
        print("CRITICAL ERROR: No data was collected in the scraped_pages folder.")