"""Fetch job postings from company career sites with the Apify Actor
polderbyte/eu-career-site-jobs.

Usage:
    export APIFY_TOKEN=...            (PowerShell: $env:APIFY_TOKEN = "...")
    pip install -r requirements.txt
    python get_jobs.py                                  # default: greenhouse:adyen
    python get_jobs.py personio:tado lever:spotify teamleader.eu

Each argument is one company: an 'ats:slug', an ATS board URL, a careers page URL or a domain.
"""

import json
import os
import sys
from decimal import Decimal
from pathlib import Path

from apify_client import ApifyClient

sys.stdout.reconfigure(encoding="utf-8")  # so non-ASCII job titles also print on Windows consoles

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable (Apify Console > Settings > API & Integrations).")

companies = sys.argv[1:] or ["greenhouse:adyen"]
run_input = {
    "companies": companies,
    "maxItems": 5,  # keeps the run small and cheap; raise it for real use
    "descriptionMaxChars": 300,
    # Optional filters, see the README for all fields:
    # "keywords": ["engineer"],
    # "countries": ["BENELUX"],
    # "remote": "remote-or-hybrid",
    # "postedSince": "14 days",
}

client = ApifyClient(token)

# call() starts the run and waits for it to finish.
# max_total_charge_usd caps what this run can cost you.
run = client.actor("polderbyte/eu-career-site-jobs").call(
    run_input=run_input,
    max_total_charge_usd=Decimal("0.10"),
    logger=None,  # remove this argument to stream the Actor's log to your terminal
)

if run is None or run.status != "SUCCEEDED":
    sys.exit(f"Run did not succeed: {run.status if run else 'no run returned'}")

items = list(client.dataset(run.default_dataset_id).iterate_items())

for job in items:
    where = ", ".join(part for part in (job.get("location"), job.get("country")) if part)
    print(f"{job['company']} | {job['title']} | {where or '-'} | posted {job.get('postedAt') or '-'}")
    print(f"  apply: {job['applyUrl']}")

Path("output").mkdir(exist_ok=True)
Path("output/jobs.json").write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\n{len(items)} job(s) saved to output/jobs.json (run {run.id}).")
