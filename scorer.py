import os
from google import genai
from dotenv import load_dotenv
import json
import math
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from typing import List, Dict
import asyncio
import random
from abc import ABC, abstractmethod
from collections import deque

load_dotenv()

PERSONAS = {
    "founder": {
        "role": "Startup Founder / CEO",
        "focus": "Competitor moves, product launches, and fundraising trends.",
        "impact_def": "Does this affect my startup's runway, competitive advantage, or ability to raise capital?"
    },
    "tech_leader": {
        "role": "Product & Tech Leader",
        "focus": "New AI tools, tech stack updates, and user behavior trends.",
        "impact_def": "Does this shift the technological paradigm, require a tech stack update, or reveal massive software bugs?"
    },
    "investor": {
        "role": "Investor & Trader",
        "focus": "Market volatility, price action, and M&A.",
        "impact_def": "Will this directly move stock/crypto prices, change company valuations, or trigger M&A activity?"
    },
    "marketer": {
        "role": "Marketing & Content Creator",
        "focus": "Viral trends, PR, and public sentiment.",
        "impact_def": "Is this a highly viral topic? Does it shift brand perception or create a new cultural narrative?"
    },
    "sales": {
        "role": "Sales & Business Growth",
        "focus": "Industry pain points, hiring trends, and pricing changes.",
        "impact_def": "Does this reveal a massive pain point I can sell a solution for, or show a company is expanding its budget?"
    },
    "analyst": {
        "role": "Industry Analyst",
        "focus": "Deep market research, tech policy, and economics.",
        "impact_def": "Does this provide hard data on macro trends, regulatory shifts, or long-term economic forecasts?"
    }
}

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

    def score_headlines(self, persona, items):
        """
        Scores a list of items for a given persona.
        Each item must have a 'text' field (headline + snippet) and 'original_headline'.
        Returns a list of dictionaries with scoring details and preserved metadata.
        """
        if not self.client:
            return self._mock_scoring(persona, items)
        
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
        You are an elite Market Intelligence AI strictly advising a {persona['role']}. Evaluate the following signal based strictly on their focus: {persona['focus']}. When scoring 'Impact' from 0-100, use this definition: {persona['impact_def']}. Ignore metrics that do not matter to this specific persona.
        
        Analyze the following headlines and return a JSON array of objects.
        
        Headlines:
        {json.dumps(headlines_for_prompt)}

        For EACH headline, provide:
        1. "signal": A concise, punchy summary of the headline suitable for a dashboard card.
        2. "sentiment": "positive", "neutral", or "negative".
        3. "utility_score": 0-100 (Can this be turned into a product?)
        4. "novelty_score": 0-100 (Is this new?)
        5. "impact_score": 0-100 ({persona['impact_def']})
        6. "score": Calculate weighted score: (utility_score * 0.4) + (novelty_score * 0.3) + (impact_score * 0.3). Round to an integer.
        7. "relevant": boolean (true if score > 60, else false).
        8. "brief": A short 3-sentence briefing for a {persona['role']} about why this matters.

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
            mock_results = self._mock_scoring(persona, valid_items)
            for idx, res in enumerate(mock_results):
                 final_results[valid_indices[idx]] = res
            return final_results

    def _mock_scoring(self, persona, items):
        """Fallback if API fails"""
        results = []
        import random
        for item in items:
            score = round(random.uniform(40, 90))
            mock_item = item.copy()
            mock_item.update({
                "signal": item.get('original_headline'), 
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "score": score,
                "relevant": score > 60,
                "brief": f"API Unavailable. Mock data for {persona['role']}.",
                "utility_score": 50,
                "novelty_score": 50,
                "impact_score": 50
            })
            results.append(mock_item)
        return results

class ScoringStrategy(ABC):
    @abstractmethod
    async def calculate_score(self, text: str) -> float:
        pass

class UtilityScorer(ScoringStrategy):
    def __init__(self):
        self.utility_keywords = {
            "build", "tool", "framework", "guide", "tutorial", "how-to", 
            "open-source", "launch", "release", "api", "sdk", "library", 
            "platform", "solution", "github", "documentation", "integrate"
        }
        
    async def calculate_score(self, text: str) -> float:
        # Simulate async I/O or model call
        await asyncio.sleep(0.01)
        tokens = nltk.word_tokenize(text.lower())
        if not tokens:
            return 0.0
        
        count = sum(1 for token in tokens if token in self.utility_keywords)
        return min(count / 5.0, 1.0)

class ImpactScorer(ScoringStrategy):
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.impact_keywords = {
            "million", "billion", "growth", "revenue", "acquired", "critical", 
            "major", "dominant", "funding", "market", "scale", "investment",
            "valuation", "surge", "plummet", "record", "trillion"
        }
        
    async def calculate_score(self, text: str) -> float:
        await asyncio.sleep(0.01)
        if not text.strip():
            return 0.0
            
        sentiment_scores = self.sia.polarity_scores(text)
        sentiment_magnitude = abs(sentiment_scores['compound'])
        
        tokens = nltk.word_tokenize(text.lower())
        keyword_count = sum(1 for token in tokens if token in self.impact_keywords)
        keyword_score = min(keyword_count / 5.0, 1.0)
        
        score = (sentiment_magnitude * 0.6) + (keyword_score * 0.4)
        return min(score, 1.0)

class NoveltyScorer(ScoringStrategy):
    def __init__(self, window_size: int = 100):
        self.rolling_window = deque(maxlen=window_size)
    
    def _get_embedding(self, text: str) -> List[float]:
        """Mock function to generate vector embeddings."""
        # Generates a random 5-dimensional vector
        return [random.random() for _ in range(5)]
        
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculates cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = math.sqrt(sum(a * a for a in vec1))
        mag2 = math.sqrt(sum(b * b for b in vec2))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)

    async def calculate_score(self, text: str) -> float:
        await asyncio.sleep(0.01)
        if not text.strip():
            return 0.0
            
        new_embedding = self._get_embedding(text)
        
        if not self.rolling_window:
            self.rolling_window.append(new_embedding)
            return 1.0
            
        # Find maximum similarity with existing articles in the window
        max_similarity = 0.0
        for existing_emb in list(self.rolling_window):
            sim = self._cosine_similarity(new_embedding, existing_emb)
            if sim > max_similarity:
                max_similarity = sim
                
        self.rolling_window.append(new_embedding)
        
        # Novelty is inversely proportional to similarity
        novelty = 1.0 - max_similarity
        return max(0.0, min(novelty, 1.0))

class InsightScorer:
    """
    Evaluates market articles based on Utility, Impact, and Novelty using async strategies.
    """
    def __init__(self, data: List[Dict[str, str]]):
        self.data = data
        self._ensure_nltk_resources()
        
        self.utility_scorer = UtilityScorer()
        self.impact_scorer = ImpactScorer()
        self.novelty_scorer = NoveltyScorer(window_size=100)
        
        self.weights = {
            "utility": 0.30,
            "impact": 0.40,
            "novelty": 0.30
        }

    def _ensure_nltk_resources(self):
        resources = ['punkt', 'punkt_tab', 'vader_lexicon']
        for resource in resources:
            try:
                if resource in ('punkt', 'punkt_tab'):
                    nltk.data.find(f'tokenizers/{resource}')
                else:
                    nltk.data.find(f'sentiment/{resource}')
            except LookupError:
                nltk.download(resource, quiet=True)

    async def _score_single_article(self, item: Dict) -> Dict:
        text_to_analyze = f"{item.get('title', '')} {item.get('content', '')}"
        
        utility_task = self.utility_scorer.calculate_score(text_to_analyze)
        impact_task = self.impact_scorer.calculate_score(text_to_analyze)
        novelty_task = self.novelty_scorer.calculate_score(text_to_analyze)
        
        utility_score, impact_score, novelty_score = await asyncio.gather(
            utility_task, impact_task, novelty_task
        )
        
        total_score = (
            (utility_score * self.weights["utility"]) +
            (impact_score * self.weights["impact"]) +
            (novelty_score * self.weights["novelty"])
        )
        
        scored_item = item.copy()
        scored_item["scores"] = {
            "utility": round(utility_score, 4),
            "impact": round(impact_score, 4),
            "novelty": round(novelty_score, 4),
            "total": round(total_score, 4)
        }
        return scored_item

    async def score_and_filter(self) -> List[Dict]:
        """
        Scores all articles concurrently and returns the top 5% based on the weighted total score.
        """
        if not self.data:
            return []

        # Execute all item scorings concurrently
        tasks = [self._score_single_article(item) for item in self.data]
        scored_data = await asyncio.gather(*tasks)
            
        # Sort descending by total score
        scored_data.sort(key=lambda x: x["scores"]["total"], reverse=True)
        
        # Calculate top 5% index
        top_5_percent_count = max(1, math.ceil(len(scored_data) * 0.05))
        
        return scored_data[:top_5_percent_count]
