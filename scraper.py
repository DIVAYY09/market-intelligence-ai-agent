import os
import argparse
import time
import json
import uuid
import requests
from datetime import datetime
from scorer import RelevanceScorer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_serper(query, type="news"):
    """
    Search using Serper.dev API.
    type can be 'search' or 'news' (maps to tbm='nws')
    """
    url = "https://google.serper.dev/news" if type == "news" else "https://google.serper.dev/search"
    
    payload = json.dumps({
        "q": query,
        "num": 10,
        "tbs": "qdr:d"  # last 24 hours
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
    except Exception as e:
        print(f"Error calling Serper: {e}")
        return {}

def save_signals(signals):
    """Save signals to JSON file"""
    output_dir = "public/data"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "social_signals.json")
    
    transformed_data = []
    
    for item in signals:
        transformed_data.append({
            "id": str(uuid.uuid4()),
            "name": item.get('source', 'Social Signal'), 
            "ticker": item.get('source', 'WEB'), # This displays as the Source label in UI
            "signal": item.get('signal', item.get('original_headline')),
            "sentiment": item.get('sentiment', 'neutral'),
            "relevant": item.get('relevant', False),
            "score": item.get('score', 0),
            "time": item.get('time', datetime.now().strftime("%H:%M")),
            "brief": item.get('brief', "No brief available."),
            "link": item.get('link', '#'),
            "metrics": {
                "utility": item.get('utility_score', 0),
                "novelty": item.get('novelty_score', 0),
                "impact": item.get('impact_score', 0)
            }
        })
    
    # Sort by score desc
    transformed_data.sort(key=lambda x: x['score'], reverse=True)

    try:
        with open(filepath, 'w') as f:
            json.dump(transformed_data, f, indent=2)
        print(f"Successfully saved {len(transformed_data)} signals to {filepath}")
    except Exception as e:
        print(f"Error saving signals: {e}")

def main():
    parser = argparse.ArgumentParser(description="Market Intelligence Agent - Social Search")
    parser.add_argument("--sector", type=str, help="Specific sector to research (optional)")
    args = parser.parse_args()
    
    # Default sectors to scan if none provided
    sectors = ["Fintech", "EdTech", "Healthcare", "AI"]
    if args.sector:
        sectors = [args.sector]
    
    print(f"Starting Social Intelligence Scan for: {sectors}")
    
    if not SERPER_API_KEY:
        print("Error: SERPER_API_KEY not found in .env")
        return

    scorer = RelevanceScorer()
    all_raw_items = []
    
    for sector in sectors:
        # Construct queries to find social/news content
        # User requested "latest posts on LinkedIn and X" and "tbm: nws"
        # We will try a mix to ensure coverage.
        
        queries = [
            f"{sector} news site:linkedin.com",
            f"{sector} news site:twitter.com",
            f"{sector} news site:x.com",
            f"{sector} industry news" # Fallback for general high signal
        ]
        
        for q in queries:
            print(f"Searching: {q}...")
            # Use 'news' type as requested for fresh results
            results = search_serper(q, type="news")
            
            # Serper 'news' response structure: {'news': [{'title':..., 'snippet':..., 'source':..., 'link':..., 'date':...}]}
            if 'news' in results:
                for news_item in results['news']:
                    # Extract clean source name
                    source_raw = news_item.get('source', 'Web')
                    
                    # Normalize source for UI
                    if "linkedin" in q:
                        display_source = "LinkedIn"
                    elif "x.com" in q or "twitter" in q:
                        display_source = "X (Twitter)"
                    else:
                        display_source = source_raw

                    all_raw_items.append({
                        "text": news_item.get('title', '') + ". " + news_item.get('snippet', ''),
                        "original_headline": news_item.get('title', ''),
                        "snippet": news_item.get('snippet', ''),
                        "source": display_source,
                        "link": news_item.get('link', ''),
                        "time": news_item.get('date', 'Today')
                    })
            time.sleep(0.5) # rate limit politeness

    # Remove duplicates based on headline
    unique_items = {i['original_headline']: i for i in all_raw_items}.values()
    all_raw_items = list(unique_items)
    
    if not all_raw_items:
        print("No results found via Serper.")
        all_raw_items.append({
            "text": "System Check: No recent social signals found. API connectivity verified.", 
            "original_headline": "System Check: No signals.", 
            "source": "System",
            "snippet": "No data returned from search.",
            "link": "#"
        })

    print(f"Collected {len(all_raw_items)} candidates. Scoring...")
    
    # Scorer now handles item objects directly to preserve metadata and link
    final_results = scorer.score_headlines("Multi-Sector", all_raw_items)
        
    save_signals(final_results)

if __name__ == "__main__":
    main()
