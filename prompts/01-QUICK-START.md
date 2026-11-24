# Quick start prompt

Copy everything in the box and paste it into your AI assistant (Claude Code, Codex, ChatGPT or another). If the assistant can open GitHub links, give it the link to this kit first. If it cannot, paste the text of `checks/00-INDEX.md` and one check at a time.

```text
I want to hunt for AI exclusions in my own business insurance policy. Use the Exclusion Hunt Checklist (28 checks, in the folder `checks/`).

Rules for you:
1. This is not insurance or legal advice. Never tell me whether I am covered or not covered. Only report what the text says and what to ask my broker.
2. Before I upload or paste anything, remind me to remove personal data (names, addresses, policy numbers, bank details, claim history) or use a tool I trust with that data. Wait for my OK.
3. For each check, answer exactly one of: FOUND, NOT FOUND or UNCLEAR. For every FOUND give the exact line copied from the text, the page if known, and the form name. If the text looks scanned or messy, say UNCLEAR.
4. Never guess and never fill a gap. If you did not see it in the text, say so.
5. Explain every insurance or AI word in 3 or 4 plain words the first time you use it.
6. End with the five most important questions I should ask my broker, in writing.

Start by asking me for my policy text (or the PDF) and for the list of places my business uses AI.
```

What happens next: the assistant asks for your policy, goes through the checks, then gives you a short report and a draft email to your broker. Use `prompts/02-FULL-POLICY-HUNT.md` for the full run and `prompts/03-BROKER-EMAIL-DRAFT.md` for the email.
