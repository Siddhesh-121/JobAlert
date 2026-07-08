"""
MAIN ORCHESTRATOR
━━━━━━━━━━━━━━━━
Run this directly:  python main.py
Or let GitHub Actions run it on a schedule.

Flow:
  scrapers → filter → dedup → notify → save state
"""

import sys

from dotenv import load_dotenv
load_dotenv()

from scrapers import scrape_linkedin
# from scrapers import scrape_indeed      # uncomment when ready
# from scrapers import scrape_irishjobs   # uncomment when ready
# from scrapers import scrape_glassdoor   # uncomment when ready

from filter   import filter_jobs
from dedup    import load_seen, save_seen, filter_new
from notifier import send_alert, send_summary

def run():
    print("=" * 50)
    print("🔍 Job Alert Bot starting...")
    print("=" * 50)

    # ── 1. SCRAPE ─────────────────────────────────────────────────────────────
    all_jobs = []

    print("\n[1/4] Scraping sources...")

    # LinkedIn (active)
    linkedin_jobs = scrape_linkedin()
    print(f"  LinkedIn → {len(linkedin_jobs)} jobs found")
    all_jobs.extend(linkedin_jobs)

    # Add more sources here as you enable them:
    # indeed_jobs = scrape_indeed()
    # print(f"  Indeed → {len(indeed_jobs)} jobs found")
    # all_jobs.extend(indeed_jobs)

    # irishjobs_jobs = scrape_irishjobs()
    # print(f"  IrishJobs → {len(irishjobs_jobs)} jobs found")
    # all_jobs.extend(irishjobs_jobs)

    print(f"  Total scraped: {len(all_jobs)}")

    # ── 2. FILTER ─────────────────────────────────────────────────────────────
    print("\n[2/4] Filtering for SDE roles...")
    relevant = filter_jobs(all_jobs)
    print(f"  Relevant matches: {len(relevant)}")

    # ── 3. DEDUP ──────────────────────────────────────────────────────────────
    print("\n[3/4] Checking for new jobs (dedup)...")
    seen       = load_seen()
    new_jobs, seen = filter_new(relevant, seen)
    print(f"  New (unseen) jobs: {len(new_jobs)}")

    # ── 4. NOTIFY + SAVE ──────────────────────────────────────────────────────
    print("\n[4/4] Sending notifications...")
    if new_jobs:
        send_alert(new_jobs)
        for job in new_jobs:
            print(f"  ✅ {job['title']} @ {job['company']} ({job['source']})")
    else:
        print("  No new jobs — nothing to send.")

    send_summary(len(all_jobs), len(new_jobs))
    save_seen(seen)

    print("\n✅ Done.")
    return len(new_jobs)


if __name__ == "__main__":
    count = run()
    sys.exit(0)
