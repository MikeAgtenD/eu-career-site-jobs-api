# EU Career-Site Jobs API: Greenhouse, Lever, Personio, Recruitee, Teamtailor, Workable, SmartRecruiters, Ashby

Get job postings straight from company career sites as clean JSON. You give a list of companies (a careers page URL,
a domain, an ATS board URL or an `ats:slug`), and the [EU Career-Site Jobs](https://apify.com/polderbyte/eu-career-site-jobs)
Actor on Apify detects the applicant tracking system (ATS) and returns every open role from the company's public job
feed, one row per job.

This repository contains example code and documentation for calling that Actor from JavaScript, Python, `curl` or an
AI agent. The Actor itself runs on the Apify platform.

- Store page: https://apify.com/polderbyte/eu-career-site-jobs
- Actor ID for the API: `polderbyte/eu-career-site-jobs` (in URLs: `polderbyte~eu-career-site-jobs`)

## Who it's for

- **Job boards and niche job sites** that want fresh roles from many employers, with apply links that go to the employer.
- **Recruiters and staffing agencies** that watch target companies and want only the new roles each day (diff mode).
- **Labour-market and salary research**: who hires what, where, remote or not, and the salary range when it is published.
- **Sales teams** that use hiring as a buying signal and push new roles at their accounts into a CRM.
- **AI agents and RAG pipelines** that need job descriptions as plain text.

## Supported ATS

| ATS | You can give |
| --- | --- |
| Greenhouse (also EU-hosted boards) | `greenhouse:adyen`, `job-boards.greenhouse.io/<slug>`, a careers page with a Greenhouse embed |
| Lever (US and EU instance) | `lever:spotify`, `lever-eu:<slug>`, `jobs.lever.co/<slug>`, `jobs.eu.lever.co/<slug>` |
| Recruitee | `recruitee:bunq`, `<slug>.recruitee.com`, or a custom careers domain such as `careers.teamleader.eu` |
| Personio | `personio:tado`, `<slug>.jobs.personio.de` or `.com` |
| Teamtailor | `teamtailor:lunar`, `<slug>.teamtailor.com`, or a custom careers domain |
| Workable | `workable:huggingface`, `apply.workable.com/<slug>` |
| SmartRecruiters | `smartrecruiters:BoschGroup`, `careers.smartrecruiters.com/<Identifier>` |
| Ashby | `ashby:linear`, `jobs.ashbyhq.com/<slug>` |

Only have a domain? Give `teamleader.eu` or `adyen.com`: the Actor reads the homepage and careers page (respecting
robots.txt), looks for ATS embeds and links, and as a last resort checks each ATS for a board named after the company.
Workday, SuccessFactors, Taleo, iCIMS, SAP and home-made careers sites are not supported.

## Sample output

A real run on 24 November 2026 with this input:

```json
{ "companies": ["greenhouse:adyen"], "maxItems": 2, "descriptionMaxChars": 200 }
```

returned 2 rows. The first one, unchanged:

```json
{
  "company": "Adyen",
  "ats": "greenhouse",
  "atsSlug": "adyen",
  "jobId": "8414492",
  "title": "Senior AI Engineer (Forward Deployed Engineering)",
  "department": "Infrastructure",
  "location": "Amsterdam",
  "country": "NL",
  "remote": null,
  "workplaceType": null,
  "employmentType": null,
  "postedAt": "2026-11-24T17:12:42Z",
  "updatedAt": "2026-11-24T17:12:42Z",
  "applyUrl": "https://job-boards.greenhouse.io/adyen/jobs/8414492",
  "jobUrl": "https://job-boards.greenhouse.io/adyen/jobs/8414492",
  "descriptionText": "This is Adyen\n\nAdyen provides payments, data, and financial products in a single solution for customers like Meta, Uber, H&M, and Microsoft - making us the financial technology platform of choice.…",
  "salaryMin": null,
  "salaryMax": null,
  "salaryCurrency": null,
  "salaryPeriod": null,
  "salaryText": null,
  "fetchedAt": "2026-11-24T17:58:41Z"
}
```

Fields are `null` when the ATS or the employer does not publish them; the Actor does not guess. Greenhouse and
Teamtailor feeds have no salary; salary appears for Personio, Recruitee, Lever and Ashby jobs when the employer
publishes it.

## Quick start

You need an Apify account and an API token (Apify Console > Settings > API & Integrations). Put the token in an
environment variable, never in your code:

```bash
export APIFY_TOKEN=your_token        # PowerShell: $env:APIFY_TOKEN = "your_token"
```

### JavaScript / Node.js

```bash
npm install apify-client
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('polderbyte/eu-career-site-jobs').call({
    companies: ['greenhouse:adyen', 'personio:tado', 'teamleader.eu'],
    keywords: ['engineer'],
    maxItems: 50,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const job of items) console.log(job.company, '|', job.title, '|', job.applyUrl);
```

### Python

```bash
pip install apify-client
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("polderbyte/eu-career-site-jobs").call(
    run_input={
        "companies": ["greenhouse:adyen", "personio:tado", "teamleader.eu"],
        "keywords": ["engineer"],
        "maxItems": 50,
    }
)

for job in client.dataset(run.default_dataset_id).iterate_items():
    print(job["company"], "|", job["title"], "|", job["applyUrl"])
```

This uses `apify-client` 3.x for Python, where `call()` returns a `Run` object. With the older 1.x/2.x client, use
`run["defaultDatasetId"]`.

### curl

`run-sync-get-dataset-items` starts the run, waits for it to finish and returns the rows in one HTTP call:

```bash
curl -X POST "https://api.apify.com/v2/acts/polderbyte~eu-career-site-jobs/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companies": ["greenhouse:adyen"], "maxItems": 2, "descriptionMaxChars": 200}'
```

The synchronous endpoint waits up to 300 seconds. For large runs, start the run asynchronously (`POST /v2/acts/polderbyte~eu-career-site-jobs/runs`)
and read the dataset when it has finished, or add a webhook.

## Examples in this repo

| File | What it does |
| --- | --- |
| [`examples/node/get-jobs.mjs`](examples/node/get-jobs.mjs) | Runs the Actor for the companies you pass, prints one line per job and saves `output/jobs.json` |
| [`examples/python/get_jobs.py`](examples/python/get_jobs.py) | The same in Python |

```bash
cd examples/node && npm install && node get-jobs.mjs personio:tado lever:spotify
cd examples/python && pip install -r requirements.txt && python get_jobs.py personio:tado lever:spotify
```

Both read `APIFY_TOKEN` from the environment, keep runs small (`maxItems: 5`) and set a spending limit of $0.10 per run.

## Input

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `companies` | array of strings | 4 sample companies | One company per entry: careers page URL, domain, ATS board URL or `ats:slug` (`greenhouse`, `lever`, `lever-eu`, `recruitee`, `personio`, `teamtailor`, `workable`, `smartrecruiters`, `ashby`). Via the API you can also pass objects like `{"ats": "greenhouse", "slug": "adyen", "name": "Adyen"}`. |
| `keywords` | array | – | Only jobs whose title or department contains one of these words (case-insensitive). |
| `keywordsInDescription` | boolean | `false` | Also match `keywords` in the description. |
| `excludeKeywords` | array | – | Drop jobs whose title contains one of these words. |
| `countries` | array | – | ISO codes (`BE`, `NL`, `DE`, ...) or the groups `EU`, `EEA`, `EUROPE`, `BENELUX`, `DACH`, `NORDICS`. Jobs without a recognisable country are left out when set. |
| `locations` | array | – | Location text such as `Amsterdam`, `Gent`, `München`. |
| `remote` | string | `any` | `any`, `remote`, `remote-or-hybrid`, `hybrid` or `onsite`. |
| `departments` | array | – | Only jobs whose department contains one of these words. |
| `postedSince` | string | – | A date (`YYYY-MM-DD`) or an age such as `7 days`, `24 hours`, `2 weeks`, `1 month`. |
| `onlyNewSinceLastRun` | boolean | `false` | Diff mode: output only new, changed and (optionally) removed jobs since the previous run. |
| `includeRemovedJobs` | boolean | `true` | Diff mode: also output a `removed` row for jobs that left the feed. |
| `stateKey` | string | derived | Diff mode: name of the remembered state; runs with the same name share it. |
| `includeDescription` | boolean | `true` | Add `descriptionText` (plain text; e-mail addresses, phone numbers and named contacts removed). |
| `descriptionMaxChars` | integer | `0` | Cut `descriptionText` at this length. `0` = no limit. |
| `maxJobsPerCompany` | integer | `0` | Stop after this many jobs per company, newest first. `0` = no limit. |
| `maxItems` | integer | `1000` | Stop the run after this many job rows in total. |

## Output fields

| Field | Meaning |
| --- | --- |
| `company`, `ats`, `atsSlug`, `jobId` | Who, which ATS, the board id and the ATS's own job id (`ats` + `atsSlug` + `jobId` is unique) |
| `title`, `department`, `location` | As published by the employer |
| `country` | ISO 3166-1 code of the (first) location |
| `remote`, `workplaceType` | `remote` is `true` for fully remote jobs; `workplaceType` is `remote`, `hybrid`, `onsite` or `null` |
| `employmentType` | `full-time`, `part-time`, `internship`, `working-student`, `apprenticeship`, `temporary`, `contract`, `freelance` or `other` |
| `postedAt`, `updatedAt`, `fetchedAt` | ISO 8601 timestamps in UTC |
| `applyUrl`, `jobUrl` | The application form and the posting page at the employer |
| `descriptionText` | The job ad as plain text |
| `salaryMin`, `salaryMax`, `salaryCurrency`, `salaryPeriod`, `salaryText` | Only when the employer publishes pay |
| `changeType` | Diff mode only: `new`, `changed` or `removed` |

The run's key-value store also has a `COMPANIES` record that says, for every input, which ATS and slug were found (or
why nothing was found). Reuse those `ats:slug` values next time to skip detection.

## Pricing

Pay per event: no subscription, no monthly fee. Prices on 24 November 2026:

| Event | Price | When it's charged |
| --- | --- | --- |
| Job | $0.002 | One job row in the output (in diff mode: one new job) |
| Job changed | $0.001 | Diff mode: one job whose content changed or that was removed |
| Company resolved | $0.003 | The Actor had to detect a company's ATS from a careers page or domain |

Example: 100 jobs from companies given as `ats:slug` cost 100 × $0.002 = $0.20. Prices can change; the
[Store page](https://apify.com/polderbyte/eu-career-site-jobs) shows the current ones. To pay less, give `ats:slug`
(no detection), use filters and `maxItems`, and use diff mode for scheduled runs.

## Use it from an AI agent (Apify MCP server)

The [Apify MCP server](https://docs.apify.com/mcp) lets AI assistants such as Claude, Cursor or
VS Code run Apify Actors. To expose only this Actor as a tool, add it with the `tools` parameter:

```json
{
  "mcpServers": {
    "eu-career-site-jobs": {
      "url": "https://mcp.apify.com?tools=polderbyte/eu-career-site-jobs",
      "headers": {
        "Authorization": "Bearer <APIFY_TOKEN>"
      }
    }
  }
}
```

Leave out `headers` if your client supports OAuth: it then opens a browser to sign in to Apify. The Actor shows up as
the tool `polderbyte--eu-career-site-jobs`. With Claude Code:

```bash
claude mcp add --transport http eu-career-site-jobs "https://mcp.apify.com?tools=polderbyte/eu-career-site-jobs" \
  --header "Authorization: Bearer $APIFY_TOKEN"
```

For clients that only support local servers, run `npx -y @apify/actors-mcp-server --tools polderbyte/eu-career-site-jobs`
with `APIFY_TOKEN` set in its environment. Then ask, for example: *"List the open engineering jobs at Adyen and tado
in the Netherlands and Germany, with apply links."*

## FAQ

**A company is not found. What now?** Open the `COMPANIES` record in the run's key-value store: it says why (no
supported ATS, page blocked by robots.txt, unreachable). If you know the ATS, give `ats:slug`; the slug is in the URL
of the company's job board, for example `jobs.lever.co/<slug>`.

**How fresh is the data?** Every run reads the employers' job feeds at that moment.

**How does diff mode work?** With `onlyNewSinceLastRun`, the Actor stores a fingerprint of each job per company in the
named key-value store `eu-career-site-jobs-state`, under `stateKey`. The next run with the same `stateKey` outputs only
new jobs, changed jobs and (with `includeRemovedJobs`) jobs that disappeared. The first run outputs everything as new.

**Does it scrape LinkedIn or Indeed?** No. It reads only the public job-board feeds that companies publish for their
own careers sites. It needs no login and runs no browser.

**Is there personal data in the output?** Recruiter and hiring-manager fields of the ATS are not copied, and e-mail
addresses, phone numbers and named contact persons are removed from descriptions. Job ads remain the employers'
content: link to the `applyUrl` and respect their terms when you republish.

**Is this an official Apify repository?** No. It is example code from the Actor's developer. The Actor is not
affiliated with any of the ATS vendors named here; their names are trademarks of their owners.

## Links

- Actor on Apify Store: https://apify.com/polderbyte/eu-career-site-jobs
- Apify API, run synchronously and get dataset items: https://docs.apify.com/api/v2/actor-run-sync-get-dataset-items-post
- Apify JavaScript client: https://docs.apify.com/api/client/js/docs
- Apify Python client: https://docs.apify.com/api/client/python/docs
- Apify MCP server: https://docs.apify.com/mcp

## License

The example code in this repository is released under the [MIT License](LICENSE). Use of the Actor on Apify is billed
by Apify under its terms.
