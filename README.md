# Bulvár Scraper

![Python](https://img.shields.io/badge/python-3-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 1. Overview
This tool aggregates headlines from major Czech tabloid and news RSS feeds into a unified text format. It is designed to create clean datasets for natural language processing or sentiment analysis by stripping away navigation elements and non-article content.

## 2. Motivation
RSS feeds often contain noise, inconsistent encoding, and non-news items like navigation links. This project solves the problem of normalizing this data into a single, clean stream of text for downstream analysis, eliminating the need to manually parse multiple heterogeneous sources.

## 3. What This Project Does
1.  **Fetcher**: Downloads XML content from a predefined list of 18+ Czech news sources.
2.  **Cleaner**: detecting encoding via `chardet` and applies regex filters to remove common RSS noise (e.g., "Overview", "Navigation", upper-case formatting).
3.  **Aggregator**: Consolidates valid headlines into a timestamped text file.

## 4. Architecture
The application follows a linear ETL (Extract, Transform, Load) pipeline pattern:
-   **Extract**: `fetch_rss_feed()` retrieves raw bytes from endpoints.
-   **Transform**: `clean_title()` and `extract_titles()` normalize encoding and filter strings.
-   **Load**: `main()` writes the final dataset to the local file system.

## 5. Tech Stack
-   **Language**: Python 3
-   **Networking**: `requests` for HTTP I/O.
-   **Encoding**: `chardet` for robust character encoding detection.
-   **UI**: `rich` for terminal feedback and progress tracking.

## 6. Data Sources
The scraper targets major Czech platforms including:
-   Super.cz, Blesk, Extra.cz, Ahaonline
-   Novinky, iDnes, Aktuálně
-   Tech news (Živě, Root, Lupa)

## 7. Key Design Decisions
-   **Robust Encoding Detection**: Many legacy RSS feeds declare incorrect encodings. `chardet` is used on raw bytes to prevent mojibake before decoding.
-   **Regex Filtering**: Heuristic patterns (`navigation_patterns`) are used to discard non-content titles (e.g., one-word section headers) that pollute text analysis datasets.
-   **Terminal UI**: `rich` was implemented to provide immediate visual feedback during network-bound operations, distinguishing this from a silent cron script.

## 8. Limitations
-   **Synchronous Execution**: Network requests are blocking, which limits meaningful concurrency and total throughput.
-   **Hardcoded Configuration**: Feed URLs are defined in source, requiring code changes for updates.
-   **No Database**: Data is persisted only to flat files, making historical querying difficult.

## 9. How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Execute scraper
python3 bulvar_scraper.py
```

## 10. Example Usage
Output is saved to `scraped_output/`:
```text
titles_20251214_113000.txt
```
Content sample:
```text
Karel Gott opět ve studiu
Ceny energií klesají pod vládní strop
Nový iPhone má USB-C
...
```

## 11. Future Improvements
-   Implement `asyncio` and `aiohttp` for parallel fetching.
-   Externalize configuration to `config.yaml`.
-   Add SQLite integration for historical data tracking.

## 12. Author
Jan Alexandr Kopřiva  
jan.alexandr.kopriva@gmail.com

## 13. License
MIT