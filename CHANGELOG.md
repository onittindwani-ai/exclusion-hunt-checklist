# Changelog

## 1.0.0 (2026-11-24)

First release.

- 28 numbered checks for hunting AI wording in US business insurance policies. Checks 1 to 3 are the three steps from the Reel. Each check has the exact words to look for, where the wording hides in a policy, why it matters, its sources with the date each was read, what a layperson does, a question for the broker or insurer and a paste in prompt.
- Coverage of the ISO generative AI endorsements CG 40 47, CG 40 48 and CG 35 08, insurer written equivalents, definitions of AI, the reach of "arising out of", absolute exclusions on management and professional policies, employment practices, AI washing, sublimits, affirmative AI endorsements, cyber, crime, commercial property, contracts and vendors, applications, renewals, claims made timing, state filings and silent AI.
- Prompts for a quick start, a full policy hunt, a broker email, a written request to the insurer and a report. No prompt gives a coverage verdict.
- Templates: exclusion register, broker question list, renewal change log and AI use map, each with made up sample rows labelled SAMPLE.
- Tools using only the Python standard library: a validator that confirms the 28 checks and their sources, and a scanner that finds the exact words in a plain text policy with line and page numbers.
- A Claude Code skill, `AGENTS.md` and `CLAUDE.md`.
- Offline tests with a made up policy.

Known limits at this release: sources were read on 2026-11-24 and only two were read as full text (see `docs/03-SOURCES.md`); the base general liability form was not read directly; the kit has been tested on made up text only, not on real policies; it is not insurance or legal advice.
