# How to run it with an AI assistant

Pick the one you already use. The idea is the same: the assistant reads your policy text and the checks, reports FOUND, NOT FOUND or UNCLEAR with the exact line, and helps you write to your broker. It must not tell you whether you are covered.

## Privacy first

Your policy has your business name, addresses, policy numbers and sometimes claim history. Whatever you paste or upload goes to the company that runs the assistant. Remove personal data first, or use a tool whose data terms you trust. The scanner in `tools/` runs only on your computer and sends nothing anywhere, so it is the safest first pass.

## Claude Code

1. Download this folder (the zip from the GitHub page, or `git clone`) and open a terminal in it.
2. Start Claude Code in that folder. It reads `CLAUDE.md` and the skill in `.claude/skills/exclusion-hunt/` by itself.
3. Say: hunt for AI exclusions in my policy and tell me what to ask my broker first. Give it the path to your policy text or PDF.

## Codex

1. Open this folder in Codex. It reads `AGENTS.md`.
2. Paste the prompt from `prompts/01-QUICK-START.md`.

## ChatGPT or another chat assistant

1. Open `prompts/01-QUICK-START.md` and paste the prompt.
2. Paste the text of `checks/00-INDEX.md`, then work in batches of about 5 checks: paste those check files and your policy text.
3. Long policies may need to be split by coverage part. Say which part you are pasting.

## Getting policy text

- If the PDF has selectable text, copy and paste it into a `.txt` file. Keep the page breaks if you can.
- On a Mac or Linux with `pdftotext` installed (part of the poppler tools): `pdftotext -layout policy.pdf policy.txt`.
- A scanned PDF (a picture of paper) needs OCR (text recognition) first. OCR makes mistakes, especially in form numbers, so treat every result as UNCLEAR until you read the page yourself.

## The scanner

```text
python3 tools/scan_policy.py policy.txt
python3 tools/scan_policy.py policy.txt --csv hits.csv
python3 tools/validate_checks.py
python3 -I -m unittest discover -s tests
```

- `scan_policy.py` lists specific words, common wording and search aid words with line numbers and page numbers. It reads the words from the check files.
- `validate_checks.py` confirms the kit holds exactly 28 well formed checks.
- The tests run offline, on a made up policy in `tests/fixtures/`.

## What a good session looks like

1. The assistant asks for your AI list and your policy text.
2. It reports each check with a quoted line or says NOT FOUND or UNCLEAR.
3. It gives you five questions for your broker, never a verdict.
4. You send the questions by email and keep the written answers.
