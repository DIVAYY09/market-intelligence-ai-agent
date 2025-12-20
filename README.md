# Market Intelligence Agent: Product Documentation & Case Study

**Version 1.0** | **Date:** December 2025

## 1. Product Vision & Idea
**"High-Signal Intelligence for the AI Era."**

The **Market Intelligence Agent** is an autonomous AI system designed to solve the "noise" problem for Product Managers and Designers in fast-moving sectors (Fintech, AI, Healthcare). Instead of manually scouring news sites and social feeds, the Agent autonomously crawls, filters, and scores hundreds of data points daily.

It doesn't just aggregate news; it acts as a **Senior Analyst**, using LLMs to evaluate every headline against a strict rubric: *Is this novel? Is it utilitarian? Does it have market impact?* Only the top 10% of "High Signal" items make it to the dashboard.

## 2. System Architecture

The system follows a linear extraction-scoring-presentation pipeline designed for resilience and accuracy.

### **Low-Level: Data Extraction Layer**
*   **Broad Signal Detection (Serper/Google News)**: We utilize the `google.serper.dev` API to cast a wide net across high-authority financial news and social signals (LinkedIn/X context). This ensures we don't miss breaking headlines.
*   **Deep Content Extraction (Playwright)**: For specific, heavy-JS financial portals (like Economic Times or Mint), we deploy a headless Playwright browser to navigate, render the full DOM, and extract nuanced article text that APIs often miss.

### **Mid-Level: The Intelligence Engine (Backend)**
*   **Relevance Scoring (`scorer.py`)**:
    *   **Pre-Filter (Logic Layer)**: To save costs and latency, raw data first passes through a keyword density filter (checking for sector tokens like "crypto", "telemedicine", "LLM").
    *   **AI Analysis (Gemini 2.5 Flash-Lite)**: Candidates surviving the filter are sent to Google's specialized **Gemini 2.5 Flash-Lite** model. The model acts as a critic, returning a strict JSON object with scores for **Utility**, **Novelty**, and **Impact** (0-10 scale).

### **High-Level: The Experience (Frontend)**
*   **Framework**: React + Vite + Tailwind CSS.
*   **Design System**: "Glassmorphism" UI (translucent backdrops, subtle gradients) heavily inspired by Linear and Apple.
*   **Data Flow**: Processed signals are stored in a static JSON structure (`social_signals.json`), ensuring the frontend is blazing fast and decoupled from the scraping latency.

## 3. Problem-Solving Log

Building an autonomous agent comes with significant reliability challenges. Here is how we solved them:

### **Challenge A: The "Legacy SDK" Trap**
*   **Problem**: We started with the older `google-generativeai` library, which lacked support for the newer Gemini 1.5/2.0 schema features.
*   **Solution**: Migrated the entire codebase to the 2025 `google-genai` SDK. This unlocked structured JSON output modes, making our parsing logic 100% robust against "hallucinated formats."

### **Challenge B: The "429-Exhausted" Loop**
*   **Problem**: Scoring 100+ headlines simultaneously triggered Google's API rate limits immediately.
*   **Solution**: We implemented a "Smart Filter" & "Model Swapping" strategy.
    1.  **Logic Filter**: A valid headline must contain at least 3 sector keywords. This reduced API calls by 40% (cutting out noise).
    2.  **Flash-Lite**: Switched to `gemini-2.5-flash-lite`, which offers significantly higher throughput than the Pro variants while maintaining sufficient reasoning capability for scoring.

### **Challenge C: Taming Dynamic DOMs**
*   **Problem**: Financial sites like ET and Mint often loaded content lazily, causing our scrapers to return empty strings.
*   **Solution**: Implemented DOM-based waiting logic in Playwright. Instead of fixed sleeps, we wait for specific CSS selectors (e.g., `div.article-body`) to attach to the tree before extracting.

## 4. Product Functionality

1.  **Autonomous Sector Crawling**: The agent accepts a list of sectors (e.g., "Fintech", "EdTech") and autonomously builds a research plan, executing search queries against multiple sources.
2.  **Product Idea Generation**: The "Utility Score" specifically looks for "buildable" insights. If a headline implies a gap in the market, it gets a high score, effectively suggesting potential startup/feature ideas.
3.  **Synthesis**: It generates a 3-sentence "Executive Brief" for every high-signal item, saving the PM from reading the full article.

## 5. Output & Usage

### **The "Signal Glow" UI**
We distinguish signal from noise visually.
*   **Standard Cards**: Glass background, subtle borders.
*   **High Signal Cards**: If a score > 7.5:
    *   **Visuals**: The card glows with an Amber gradient border.
    *   **Badge**: A "High Signal" badge appears with a pulsing ping animation.
    *   **Shadow**: A dynamic amber light is cast behind the card logic.

### **Feature: "Generate PM Brief"**
Clicking the **"Generate Brief"** button opens a focused modal containing:
*   **Executive Summary**: A concise synthesis of *why* this matters.
*   **Metrics Grid**: A visualized breakdown of the Utility, Novelty, and Impact scores.
*   **Action**: A seamless "Save to Notion" integration point for workflow continuity.

---
*Built with ❤️ by the Market Intelligence Team.*
