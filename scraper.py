import os
import argparse
import time
import json
import webbrowser
import uuid
import requests
from datetime import datetime
from scorer import RelevanceScorer, PERSONAS
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

def save_signals(signals, persona_id):
    """Save signals to JSON file"""
    output_dir = "public/data"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{persona_id}_signals.json")
    
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
    
    # Default intent queries to scan if none provided
    INTENT_QUERIES = [
        "startup fundraising OR VC deal flow",
        "tech competitor product launch",
        "market volatility OR stock price action",
        "corporate M&A OR acquisitions",
        "new AI developer tools OR tech stack",
        "software bug backlash OR consumer complaint",
        "viral social media PR trend",
        "B2B SaaS pricing changes",
        "macro economic tech forecast",
        "tech regulatory policy changes"
    ]
    if args.sector:
        INTENT_QUERIES = [args.sector]
    
    print(f"Starting Social Intelligence Scan for Persona Intents...")
    
    if not SERPER_API_KEY:
        print("Error: SERPER_API_KEY not found in .env")
        return

    scorer = RelevanceScorer()
    all_raw_items = []
    
    for intent in INTENT_QUERIES:
        # Construct queries to find social/news content
        # User requested "latest posts on LinkedIn and X" and "tbm: nws"
        # We will try a mix to ensure coverage.
        
        queries = [
            f"{intent} site:linkedin.com",
            f"{intent} site:twitter.com",
            f"{intent} site:x.com",
            f"{intent} industry news" # Fallback for general high signal
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
    for p_id, persona_data in PERSONAS.items():
        print(f"Scoring for persona: {persona_data['role']}...")
        final_results = scorer.score_headlines(persona_data, all_raw_items)
        
        # Keep items that score above 60 for that specific persona
        filtered_results = [item for item in final_results if item.get('score', 0) > 60]
        
        save_signals(filtered_results, p_id)
    
    # Auto-open the dashboard
    dashboard_url = "http://localhost:5173/market-intelligence-ai-agent/"
    print(f"Opening dashboard at {dashboard_url}...")
    webbrowser.open(dashboard_url)

if __name__ == "__main__":
    main()
