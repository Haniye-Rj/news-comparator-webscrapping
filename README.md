# news-comparator-webscrapping
How science can be a weapon against oppression and propaganda?


---

# Narrative War: Media Bias & Geographical Displacement Analysis

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Selenium](https://img.shields.io/badge/Library-Selenium-green)
![Scrapy](https://img.shields.io/badge/Library-Scrapy-orange)
![Pandas](https://img.shields.io/badge/Data-Pandas-blue)

##  Project Overview
Abstract

This research examines the divergence in news framing between state-controlled media (IRNA, PressTV) and independent media (Iran International, CNN).By utilizing an automated multi-engine web scraping pipeline comprising Selenium, Scrapy, BeautifulSoup, and Requests, the study identifies systematic thematic imbalances in how events are contextualized.A critical observation is that this report is dynamic ; because the analysis is run over multiple days, the results reflect a changing landscape of headlines, though the underlying narrative patterns remain consistent.

### The Core Thesis
The analysis reveals that while State media frequently covers topics like "Uprisings" or "Rights," it strategically shifts the **Geography of Attention** to foreign nations (e.g., UK, France, Australia) to critique Western systems, while maintaining a total domestic blackout on similar issues within Iran (e.g., Mashhad protests).

---

## Key Features

* **Tri-Engine Scraper:** * **Selenium:** Handles JavaScript-heavy sites like PressTV.
    * **Scrapy:** High-performance extraction for CNN World news.
    * **Requests:** Lightweight fetching for IRNA (Islamic Republic News Agency).
* **Regex-Based Narrative Engine:** Categorizes headlines into seven distinct themes: *Uprising/Protest, Security/IRGC, Terrorist/Agent, Freedom/Rights, Execution/Hanged, Riot/Unrest,* and *General News.*
* **Statistical Analysis:** Processes raw HTML into structured DataFrames to calculate "Narrative Share" and geographical focus.
* **Visualization Suite:** Generates Heatmaps and Bar Charts to visualize the "Mirror Realities" created by different news sources.

---

## Visualizing the Data

### 1. Narrative Density Heatmap
The heatmap illustrates the "Censorship Vacuum." You will notice high density for "Protests" in State media—but a deep dive into the data reveals these are exclusively "Out of Iran" topics. Conversely, categories like **Execution/Hanged** show zero density in State media while being prominent in Independent reporting.

<img width="1200" height="600" alt="Heatmap" src="https://github.com/user-attachments/assets/c0237974-f816-470d-8c74-9a32b097adf7" />

### 2. Geographical Displacement (The Bar Charts)
The charts prove that State media uses **"General News" (74% share)** as a statistical noise floor to drown out sensitive domestic topics. It also highlights the "Protest Paradox": State media covers foreign protests to project moral superiority while ignoring domestic crackdowns.

<img width="1200" height="700" alt="Bar" src="https://github.com/user-attachments/assets/c0207034-e75f-4b69-86b8-11ff074feb44" />

---
### 3. Media Narrative Distribution: Percentage Share (%) based on final_media_analysis.csv

| Narrative Theme | Independent Share | State Share |
| :--- | :--- | :--- |
| **Execution/Hanged** | 2.5% | 1.0% |
| **Freedom/Rights** | 3.7% | 3.6% |
| **Security/IRGC** | 17.3% | 7.1% |
| **Uprising/Protest** | 3.7% | 3.0% |
| **Terrorist/Agent** | 1.2% | 0.0% |
| **Riot/Unrest** | 1.2% | 1.0% |
| **General News** | 70.4% | 84.3% |

***

### **Interpretation of Updated Data**
**The State "General News" Strategy:** State media continues to utilize a significantly higher proportion of **General News (84.3%)** compared to Independent media (70.4%).This maintains the "Information Flooding" pattern, which dilutes the visibility of specialized geopolitical or domestic crisis reporting.
**Narrative Divergence in Security:** Independent media maintains a higher intensity in **Security/IRGC** reporting (17.3% share) compared to State media (7.1%), likely focusing on internal accountability and foreign sanctions.
**Domestic Blackouts:** While the percentages have shifted slightly, State media continues to show the lowest reporting density in themes of **Execution** and **Terrorism/Agents**, themes that are consistently addressed by Independent outlets.

Note: As headlines change daily, these percentages are subject to minor variations with each new analysis run.
## Installation & Usage

### Prerequisites
* Python 3.8+
* Chrome Browser (for Selenium)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/narrative-war.git
   cd narrative-war
   ```
2. Install dependencies:
   ```bash
   pip install pandas matplotlib seaborn selenium beautifulsoup4 scrapy webdriver-manager
   ```

### Running the Pipeline
Simply run the main script to trigger the full collection and analysis cycle:
```bash
python analysis.py
```
This will:
1. Scrape live data from IRNA, PressTV, and CNN.
2. Save local HTML copies in `/saved_pages`.
3. Process and clean the data.
4. Generate the `final_media_analysis.csv` and all visualizations.

---

## Project Structure
* `analysis.py`: The entry point that orchestrates the scraping and analysis.
* `scraper_hub.py`: Contains the Scrapy Spiders and Requests logic.
* `/saved_pages`: Local storage for raw scraped content (Offline-first approach).

---

## Conclusion of Findings
This project provides quantitative proof of **Selective Reality**. State media functions as a "periscope"—focusing intently on the flaws of external rivals while remaining statistically blind to the internal domestic crises. By exporting the "Right to Protest" narrative to Western cities, State media utilizes international news as a domestic blindfold.


