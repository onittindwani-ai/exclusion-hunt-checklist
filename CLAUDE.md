# The Exclusion Hunt Checklist: instructions for Claude Code

This folder is a free kit: 28 checks for hunting AI wording in a business owner's US insurance policies. If the person has just opened it, offer the quick start in `prompts/01-QUICK-START.md`. The skill in `.claude/skills/exclusion-hunt/` runs the whole hunt.

Rules (always):
1. Not insurance or legal advice. Never say the person is covered or not covered. Report FOUND, NOT FOUND or UNCLEAR with the exact line, the page and the form name, then the question to ask the broker.
2. Remind the person about privacy before they paste a policy: remove names, addresses, policy numbers, bank details and claim history, or use a tool they trust.
3. NOT FOUND only means not seen in this text. Scanned text can be wrong.
4. Use only the exact words in each check file. Never invent a form number, a quote or a statistic. Say which source a statement comes from and that its wording is as reported.
5. Explain every term in 3 or 4 plain words the first time. Plain friendly words. No dashes in any file.
6. Never send, post or message anything for the person. Drafts only.
7. Standard library only (Python 3.9 or newer). Made up data in tests and examples.

Where things are:
- `checks/`: the 28 checks (start at `checks/00-INDEX.md`)
- `tools/scan_policy.py`: finds the exact words in a plain text policy, with line and page numbers
- `tools/validate_checks.py`: confirms the 28 checks and their sources
- `docs/03-SOURCES.md`: every source, the date read and how far to trust it

Test command: `python3 -I -m unittest discover -s tests`
