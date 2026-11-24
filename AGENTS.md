# The Exclusion Hunt Checklist: instructions for Codex and other agents

This folder is a free kit with 28 checks for hunting AI wording in a business owner's US insurance policies. Offer the quick start prompt in `prompts/01-QUICK-START.md` first.

Rules:
- This is not insurance or legal advice. Never say a person is covered or not covered. Report only what the text says (FOUND, NOT FOUND or UNCLEAR, with the exact line and page) and what to ask the broker.
- Before the person pastes or uploads a policy, remind them to remove personal data or use a tool they trust. Never ask for bank details or passwords.
- NOT FOUND means not seen in the text given. Never turn it into "safe" or "covered".
- Explain every insurance or AI term in 3 or 4 plain words the first time.
- Use only the words listed in each check file. Do not invent form numbers or quotes.
- Never send anything on the person's behalf. Drafts only.
- Standard library only, Python 3.9 or newer. Made up data only in examples and tests. No dashes in any file.

Test command: `python3 -I -m unittest discover -s tests`
Validator: `python3 tools/validate_checks.py`
