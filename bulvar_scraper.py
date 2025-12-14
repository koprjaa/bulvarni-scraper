#!/usr/bin/env python3
"""
Project: bulvarni-scraper
File: bulvar_scraper.py
Description: Scraper that extracts titles from various RSS feeds and saves them to a text file.
Author: Jan Alexandr Kopřiva jan.alexandr.kopriva@gmail.com
License: MIT
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import chardet
import os
import glob
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text

# Initialize Rich Console
console = Console()

ASCII_ART = r"""
▛▀▖   ▜                               
▙▄▘▌ ▌▐▌ ▌▝▀▖▙▀▖ ▞▀▘▞▀▖▙▀▖▝▀▖▛▀▖▞▀▖▙▀▖
▌ ▌▌ ▌▐▐▐ ▞▀▌▌   ▝▀▖▌ ▖▌  ▞▀▌▙▄▘▛▀ ▌  
▀▀ ▝▀▘ ▘▘ ▝▀▘▘   ▀▀ ▝▀ ▘  ▝▀▘▌  ▝▀▘▘         
"""

def print_art():
    """Print embedded ASCII art."""
    console.print("\n")
    console.print(Text(ASCII_ART, style="bold white"))
    console.print("\n")

def fetch_rss_feed(url):
    """Fetch RSS feed from the given URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        raw_content = response.content
        detected = chardet.detect(raw_content)
        encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
        
        try:
            content = raw_content.decode(encoding)
        except UnicodeDecodeError:
            content = raw_content.decode('utf-8', errors='ignore')
        
        return content
    except requests.RequestException:
        # Suppress error print here to let the UI handle it
        return None

def clean_title(title):
    """Clean and filter title text."""
    if not title:
        return ""
    
    title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)
    title = re.sub(r'\s+', ' ', title.strip())
    
    # Skip likely navigation items or empty content
    if len(title) < 20:
        return ""
    
    if title.isupper() and len(title) < 50:
        return ""
    
    navigation_patterns = [
        r'^[A-Z][a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+$',
    ]
    
    for pattern in navigation_patterns:
        if re.match(pattern, title):
            return ""
    
    problematic_patterns = [
        r'^[A-Z\s]+$',
        r'^[A-Z][a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+\s+[a-z]+$',
    ]
    
    for pattern in problematic_patterns:
        if re.match(pattern, title):
            return ""
    
    return title

def extract_titles(xml_content):
    """Extract titles from RSS XML content."""
    try:
        root = ET.fromstring(xml_content)
        titles = []
        
        items = root.findall('.//item')
        if not items:
            items = root.findall('.//entry')  # Atom support
        
        for item in items:
            title_elem = item.find('title')
            if title_elem is not None and title_elem.text:
                clean_title_text = clean_title(title_elem.text)
                if clean_title_text:
                    titles.append(clean_title_text)
        
        return titles
        
    except ET.ParseError:
        return []

def main():
    """Main function to scrape all feeds and save titles to one file."""
    print_art()
    
    feeds = {
        'super_cz': 'https://www.super.cz/rss',
        'blesk_cz': 'https://www.blesk.cz/rss',
        'extra_cz': 'https://www.extra.cz/rss.xml',
        'ahaonline_cz': 'https://www.ahaonline.cz/rss',
        'novinky_cz': 'https://www.novinky.cz/rss',
        'idnes_cz': 'https://servis.idnes.cz/rss.aspx',
        'prozeny_cz': 'https://www.prozeny.cz/rss',
        'zive_cz': 'https://www.zive.cz/rss',
        'doupe_cz': 'https://doupe.zive.cz/rss',
        'zive_sk_najnovsie': 'https://zive.aktuality.sk/rss/najnovsie/',
        'zive_sk_mobilmania': 'https://zive.aktuality.sk/rss/mobilmania/',
        'lupa_cz': 'https://www.lupa.cz/rss/clanky-samostatne/',
        'root_cz': 'https://www.root.cz/rss/clanky/',
        'reflex_cz': 'https://www.reflex.cz/rss',
        'respekt_cz': 'https://www.respekt.cz/api/rss',
        'ceskenoviny_cz': 'https://www.ceskenoviny.cz/sluzby/rss/zpravy.php',
        'irozhlas_cz': 'https://www.irozhlas.cz/rss/irozhlas',
        'ct24_cz': 'https://ct24.ceskatelevize.cz/rss/tema/vyber-redakce-84313'
    }
    
    all_titles = []
    
    console.print("[bold white]Starting scraper...[/bold white]")
    
    with Progress(
        SpinnerColumn(style="bold white"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, style="white", complete_style="bold white", finished_style="bold white"),
        TaskProgressColumn(style="bold white"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[bold white]Scraping feeds...", total=len(feeds))
        
        for feed_name, url in feeds.items():
            progress.update(task, description=f"[white]Scraping {feed_name}...")
            
            xml_content = fetch_rss_feed(url)
            if xml_content:
                titles = extract_titles(xml_content)
                all_titles.extend(titles)
                # We can print individual successes if we want, but it might clutter the progress bar area
                # console.print(f"[green]✓ {feed_name}: {len(titles)} titles[/green]") 
            else:
                console.print(f"[bold white]✗ Failed to fetch {feed_name}[/bold white]")
            
            progress.advance(task)
            
    console.print(f"[bold white]Scraping finished![/bold white] Found [bold white]{len(all_titles)}[/bold white] titles total.")

    if all_titles:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "scraped_output")
        os.makedirs(output_dir, exist_ok=True)
        
        for old_file_path in glob.glob(os.path.join(output_dir, "titles_*.txt")):
            try:
                os.remove(old_file_path)
            except OSError:
                pass

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"titles_{timestamp}.txt"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for title in all_titles:
                    f.write(f"{title}\n")
            
            console.print(Panel(f"Saved {len(all_titles)} titles to:\n[bold white]{filepath}[/bold white]", title="Success", border_style="white"))
            
        except IOError as e:
            console.print(f"[bold white]Error saving file:[/bold white] {e}")
    else:
        console.print("[bold white]No titles found.[/bold white]")

if __name__ == "__main__":
    main() 