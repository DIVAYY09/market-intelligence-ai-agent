import os
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

class RelevanceScorer:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print("WARNING: GOOGLE_API_KEY not found. Scoring will be mocked/disabled.")
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Error configuring Gemini Client: {e}")
                self.client = None

    SECTOR_KEYWORDS = {
        "Fintech": ["payment", "bank", "crypto", "blockchain", "wallet", "transaction", "stock", "market", "sec", "regulation", "stripe", "visa", "upi", "lending", "finance", "money", "currency", "defi", "nft"],
        "EdTech": ["student", "learning", "course", "university", "skill", "degree", "campus", "online", "class", "tutor", "education", "school", "certificate", "training", "edtech"],
        "Healthcare": ["patient", "doctor", "drug", "vaccine", "hospital", "medicine", "care", "surgery", "biotech", "pharma", "health", "clinical", "therapy", "medical", "disease"],
        "AI": ["ai", "llm", "model", "generative", "inference", "nvidia", "gpu", "transformer", "neural", "bot", "agent", "automation", "intelligence", "gpt", "gemini", "openai", "machine learning"]
    }
    
    # Flatten keywords for general search or check specific sector? 
    # User said "keywords from my target sectors", implying checking all or relevant ones. 
    # To be safe and broad, we'll check against the set of ALL sector keywords.
    ALL_KEYWORDS = set()
    for k_list in SECTOR_KEYWORDS.values():
        for k in k_list:
            ALL_KEYWORDS.add(k.lower())

    def score_headlines(self, sector, items):
        """
        Scores a list of items for a given sector.
        Each item must have a 'text' field (headline + snippet) and 'original_headline'.
        Returns a list of dictionaries with scoring details and preserved metadata.
        """
        if not self.client:
            return self._mock_scoring(sector, items)
        
        if not items:
            return []

        # Filter headlines based on keywords
        valid_items = []
        valid_indices = []
        final_results = [None] * len(items)

        for i, item in enumerate(items):
            count = 0
            # Use 'text' (headline + snippet) for keyword search for better recall
            text_lower = item.get('text', '').lower()
            for kw in self.ALL_KEYWORDS:
                if kw in text_lower: 
                    count += 1
            
            # User requirement: At least 3 keywords
            if count >= 3:
                valid_items.append(item)
                valid_indices.append(i)
            else:
                # Create a skipped entry but preserve original data
                skipped_item = item.copy()
                skipped_item.update({
                    "signal": item.get('original_headline'),
                    "sentiment": "neutral",
                    "score": 0,
                    "relevant": False,
                    "brief": "Filtered: Low keyword density (quota saving).",
                    "utility_score": 0,
                    "novelty_score": 0,
                    "impact_score": 0
                })
                final_results[i] = skipped_item

        if not valid_items:
            print("No headlines met the keyword criteria (>=3 keywords). Skipping API call.")
            return [res for res in final_results if res is not None]

        print(f"Scoring {len(valid_items)}/{len(items)} headlines via API...")
        
        # Prepare valid headlines for the prompt
        headlines_for_prompt = [item.get('text', '') for item in valid_items]

        prompt = f"""
        You are a Market Intelligence Analyst for the {sector} sector.
        Analyze the following headlines and return a JSON array of objects.
        
        Headlines:
        {json.dumps(headlines_for_prompt)}

        For EACH headline, provide:
        1. "signal": A concise, punchy summary of the headline suitable for a dashboard card.
        2. "sentiment": "positive", "neutral", or "negative".
        3. "utility_score": 0-10 (Can this be turned into a product?)
        4. "novelty_score": 0-10 (Is this new?)
        5. "impact_score": 0-10 (Does this change the market?)
        6. "score": Calculate weighted score: (utility_score * 0.4) + (novelty_score * 0.3) + (impact_score * 0.3). Round to 1 decimal.
        7. "relevant": boolean (true if score > 7.5, else false).
        8. "brief": A short 3-sentence briefing for a Product Manager about why this matters.

        Return ONLY valid JSON.
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt
            )
            # clean up code blocks if present
            text = response.text.replace("```json", "").replace("```", "").strip()
            api_results = json.loads(text)
            
            # Map API results back to final_results
            for idx, api_res in enumerate(api_results):
                if idx < len(valid_indices):
                    # Merge API result into the original item
                    original_item = valid_items[idx] 
                    merged_item = original_item.copy()
                    merged_item.update(api_res)
                    
                    # Ensure original headline is preserved if API didn't return it or changed it
                    if "original_headline" not in merged_item:
                         merged_item["original_headline"] = original_item.get("original_headline")

                    # Sanity check on signal length
                    if len(merged_item.get('signal', '')) > 200:
                        merged_item['signal'] = merged_item.get('original_headline')

                    final_results[valid_indices[idx]] = merged_item
                else:
                    print(f"Warning: API returned more results than expected.")

            # Fill any remaining Nones
            for i in range(len(final_results)):
                if final_results[i] is None:
                     # Fallback for API failure on specific item
                     fallback_item = items[i].copy()
                     fallback_item.update({
                        "signal": items[i].get('original_headline'),
                        "sentiment": "neutral",
                        "score": 0,
                        "relevant": False,
                        "brief": "Error: Scoring skipped or API mismatch.",
                        "utility_score": 0,
                        "novelty_score": 0,
                        "impact_score": 0
                     })
                     final_results[i] = fallback_item
            
            return final_results

        except Exception as e:
            print(f"Error during scoring: {e}")
            # If API fails, fall back to mock for the VALID headlines
            mock_results = self._mock_scoring(sector, valid_items)
            for idx, res in enumerate(mock_results):
                 final_results[valid_indices[idx]] = res
            return final_results

    def _mock_scoring(self, sector, items):
        """Fallback if API fails"""
        results = []
        import random
        for item in items:
            score = round(random.uniform(4, 9), 1)
            mock_item = item.copy()
            mock_item.update({
                "signal": item.get('original_headline'), 
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "score": score,
                "relevant": score > 7.5,
                "brief": "API Unavailable. Mock data.",
                "utility_score": 5,
                "novelty_score": 5,
                "impact_score": 5
            })
            results.append(mock_item)
        return results
