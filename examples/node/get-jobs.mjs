// Fetch job postings from company career sites with the Apify Actor
// polderbyte/eu-career-site-jobs.
//
// Usage:
//   export APIFY_TOKEN=...            (PowerShell: $env:APIFY_TOKEN = "...")
//   npm install
//   node get-jobs.mjs                                  # default: greenhouse:adyen
//   node get-jobs.mjs personio:tado lever:spotify teamleader.eu
//
// Each argument is one company: an 'ats:slug', an ATS board URL, a careers page URL or a domain.

import { mkdir, writeFile } from 'node:fs/promises';
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set the APIFY_TOKEN environment variable (Apify Console > Settings > API & Integrations).');
    process.exit(1);
}

const companies = process.argv.slice(2);
const input = {
    companies: companies.length > 0 ? companies : ['greenhouse:adyen'],
    maxItems: 5, // keeps the run small and cheap; raise it for real use
    descriptionMaxChars: 300,
    // Optional filters, see the README for all fields:
    // keywords: ['engineer'],
    // countries: ['BENELUX'],
    // remote: 'remote-or-hybrid',
    // postedSince: '14 days',
};

const client = new ApifyClient({ token });

// call() starts the run and waits for it to finish.
// maxTotalChargeUsd caps what this run can cost you.
const run = await client.actor('polderbyte/eu-career-site-jobs').call(input, {
    maxTotalChargeUsd: 0.1,
    log: null, // remove this line to stream the Actor's log to your terminal
});

if (run.status !== 'SUCCEEDED') {
    console.error(`Run ${run.id} ended with status ${run.status}.`);
    process.exit(1);
}

const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const job of items) {
    const where = [job.location, job.country].filter(Boolean).join(', ');
    console.log(`${job.company} | ${job.title} | ${where || '-'} | posted ${job.postedAt ?? '-'}`);
    console.log(`  apply: ${job.applyUrl}`);
}

await mkdir('output', { recursive: true });
await writeFile('output/jobs.json', JSON.stringify(items, null, 2));
console.log(`\n${items.length} job(s) saved to output/jobs.json (run ${run.id}).`);
