import requests
from bs4 import BeautifulSoup
import json
import os
import re

URL = "https://tr.wikipedia.org/wiki/Bir_sonraki_T%C3%BCrkiye_genel_se%C3%A7imleri_i%C3%A7in_yap%C4%B1lan_anketler"
OUTPUT_FILE = "polls.js"

def clean_currency(val):
    if not val or val in ['-', '–', '—']:
        return 0.0
    val = val.replace(',', '.')
    # Remove non-numeric except dot
    val = re.sub(r'[^0-9.]', '', val)
    try:
        return float(val)
    except:
        return 0.0

def parse_table(table):
    data = []
    rows = table.find_all('tr')
    if not rows:
        return []

    # Identify headers
    headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
    
    # Map headers to standard keys
    # Map headers to standard keys
    key_map = {
        'AKP': 'AKP', 'AK PARTİ': 'AKP',
        'CHP': 'CHP',
        'MHP': 'MHP',
        'İYİ': 'IYI', 'İYİ PARTİ': 'IYI',
        'DEM': 'DEM', 'HEDEP': 'DEM', 'YSP': 'DEM',
        'YRP': 'YRP', 'YENİDEN REFAH': 'YRP',
        'ZP': 'ZP', 'ZAFER': 'ZP',
        'TİP': 'TIP', 'TÜRKİYE İŞÇİ PARTİSİ': 'TIP',
        'A': 'A', 'ANAHTAR': 'A'
    }

    # Find indices
    indices = {}
    for idx, h in enumerate(headers):
        # Clean header (remove citations [1])
        h_clean = re.sub(r'\[.*?\]', '', h).upper()
        
        found_key = None
        for k, v in key_map.items():
            if k in h_clean:
                found_key = v
                break
        
        if found_key:
            indices[found_key] = idx
        elif 'TARİH' in h_clean:
            indices['date'] = idx

    if 'date' not in indices:
        return []

    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        if not cells:
            continue
            
        # Check if row has enough cells roughly
        if len(cells) < len(indices):
            continue

        item = {}
        # Get date
        date_idx = indices['date']
        if date_idx < len(cells):
            d_text = cells[date_idx].get_text(strip=True)
            # Remove (n) poll count
            d_text = re.sub(r'\s*\(\d+\)$', '', d_text)
            item['date'] = d_text
            
            # Stop if row is invalid date
            if 'SEÇİMİ' in d_text.upper():
                pass # It's a reference point, keep it?

            has_data = False
            for k, idx in indices.items():
                if k == 'date': continue
                if idx < len(cells):
                    val = clean_currency(cells[idx].get_text(strip=True))
                    item[k] = val
                    if val > 0: has_data = True
            
            if has_data:
                data.append(item)
                
    return data

def main():
    print(f"Fetching {URL}...")
    try:
        # Wikipedia requires User-Agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Locate Monthly Averages and Medians
    # Strategy: Find header h3/h4 with text "Ortalamalar"
    
    means_data = []
    medians_data = []
    
    for header in soup.find_all(['h3', 'h4', 'h2']):
        text = header.get_text(strip=True)
        if 'Ortalamalar' in text:
            # Find next table
            table = header.find_next('table')
            if table:
                print("Found Means Table")
                means_data = parse_table(table)
        
        if 'Ortancalar' in text:
            table = header.find_next('table')
            if table:
                print("Found Medians Table")
                medians_data = parse_table(table)

    output_data = {
        "means": means_data,
        "medians": medians_data
    }
    
    # Write to JS file
    js_content = f"window.poll_history = {json.dumps(output_data, indent=2, ensure_ascii=False)};"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print(f"Successfully wrote {len(means_data)} mean rows and {len(medians_data)} median rows to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
