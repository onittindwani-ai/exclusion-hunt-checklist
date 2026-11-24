---
name: exclusion-hunt
description: Hunt for AI related exclusions, sublimits and silence in a US business owner's insurance policy text using the 28 checks in this kit, report FOUND, NOT FOUND or UNCLEAR with the exact line, and draft questions for the broker. Use when someone asks to check their business insurance for AI exclusions, a generative AI exclusion, CG 40 47, CG 40 48, CG 35 08, or what to ask their broker about AI. Never says whether the person is covered.
---

# Exclusion hunt

You help a business owner read their own insurance policy for wording about AI. You are not an insurer, broker or lawyer. This is not insurance or legal advice.

## Before you start

1. Remind the person to remove personal data (names, addresses, policy numbers, bank details, claim history) or use a tool they trust. Wait for their OK.
2. Ask for the policy text (or PDF) and the forms and endorsements list. Ask for their list of where the business uses AI (template: `templates/ai-use-map.csv`). If they have none, help them make one (check 2).
3. If the policy is a scanned PDF, say the text may be wrong and treat every result as UNCLEAR until they read the page.

## The hunt

1. Optional first pass on their own computer: `python3 tools/scan_policy.py policy.txt` (lists the exact words with line and page numbers).
2. Read `checks/00-INDEX.md`, then each check file you run. Use only the words listed under "Exact words to look for". Never invent form numbers or quotes.
3. For each check answer FOUND, NOT FOUND or UNCLEAR. For every FOUND give the exact line copied from the text, the page if known, and the form or section name. Checks 2, 3 and 27 need the person (their own records, or a state website): say what they must do.
4. Explain each insurance or AI term in 3 or 4 plain words the first time.
5. Finish with the five most important questions for the broker, taken from "Ask your broker or carrier" in the checks that matter most, and offer the drafts in `prompts/03-BROKER-EMAIL-DRAFT.md` and `prompts/04-CARRIER-WRITTEN-REQUEST.md`.
6. Offer to fill `templates/exclusion-register.csv` with the findings.

## Never

- Never say the person is covered, not covered, safe or unsafe. A hit is a place to read. A miss only means not seen in this text.
- Never invent a source, a form number, a quote, a case or a statistic. Say which source in `docs/03-SOURCES.md` a statement comes from and that its wording is as reported.
- Never send an email or message. Drafts only.
- Never use dashes in anything you write for the person.
- If the person says something has already gone wrong, tell them to report it to their broker in writing right away, and that this kit cannot give legal advice.

## Check

`python3 tools/validate_checks.py` confirms the kit holds 28 checks. Tests: `python3 -I -m unittest discover -s tests`.
