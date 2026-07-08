"""
SCRAPER BLOCK: LinkedIn
━━━━━━━━━━━━━━━━━━━━━━
To swap this out, replace with indeed.py / irishjobs.py etc.
Each scraper must return a list of dicts with keys:
  - title      (str)
  - company    (str)
  - location   (str)
  - url        (str)
  - source     (str)  e.g. "LinkedIn"
"""

import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Tune these to your search ──────────────────────────────────────────────────
SEARCH_QUERIES = [
    "Software Engineer",
    "AI Software Engineer",
    "Backend Engineer",
    "Full Stack Developer",
    "Node.js Developer",
    "Java Developer",
    "Graduate Software Engineer",
]
LOCATION = "Ireland"
MAX_PAGES = 2          # LinkedIn shows 25 results/page; 2 pages = up to 50
# ──────────────────────────────────────────────────────────────────────────────


def scrape() -> list[dict]:
    """Entry point called by main.py. Returns list of job dicts."""
    jobs = []
    seen_urls = set()

    for query in SEARCH_QUERIES:
        for page in range(MAX_PAGES):
            url = _build_url(query, page)
            batch = _fetch_page(url)
            for job in batch:
                if job["url"] not in seen_urls:
                    seen_urls.add(job["url"])
                    jobs.append(job)
            time.sleep(2)   # polite delay between requests

    return jobs


def _build_url(query: str, page: int) -> str:
    start = page * 25
    q = requests.utils.quote(query)
    loc = requests.utils.quote(LOCATION)
    return (
        f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        f"?keywords={q}&location={loc}&start={start}&f_TPR=r86400"
        # f_TPR=r86400 → posted in last 24 hours; remove to get older listings
    )


def _fetch_page(url: str) -> list[dict]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[LinkedIn] Request failed: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.find_all("li")
    jobs = []

    for card in cards:
        title_tag   = card.find("h3", class_="base-search-card__title")
        company_tag = card.find("h4", class_="base-search-card__subtitle")
        location_tag= card.find("span", class_="job-search-card__location")
        link_tag    = card.find("a", class_="base-card__full-link")

        if not title_tag or not link_tag:
            continue

        jobs.append({
            "title":    title_tag.get_text(strip=True),
            "company":  company_tag.get_text(strip=True) if company_tag else "N/A",
            "location": location_tag.get_text(strip=True) if location_tag else LOCATION,
            "url":      link_tag["href"].split("?")[0],   # strip tracking params
            "source":   "LinkedIn",
        })

    return jobs


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PLACEHOLDER BLOCKS — uncomment and fill in when ready to add more sources
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# from scrapers import indeed       # scrapers/indeed.py
# from scrapers import irishjobs    # scrapers/irishjobs.py
# from scrapers import glassdoor    # scrapers/glassdoor.py
# from scrapers import jobsie       # scrapers/jobsie.py
