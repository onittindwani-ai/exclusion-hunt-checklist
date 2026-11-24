# The Exclusion Hunt Checklist

A free kit by Onit Tindwani (Sendora) with 28 checks for finding AI related wording in your US business insurance policies, and a plain list of what to ask your broker. You use it with an AI assistant such as Claude Code, Codex or ChatGPT. You do not need to know anything about AI or insurance to start.

Business insurance policies are now being changed to add wording about AI. Some standard general liability add on pages (endorsements) that let an insurer refuse claims connected to generative AI (AI that writes or makes things) became available in January 2026, and each insurer decides whether to use them. This kit helps you find out whether your own policies have wording like that, and what to ask.

**This is not insurance or legal advice.** It never tells you what you are covered for. Policies and rules differ by state and by insurer. Always ask your broker, in writing.

## What you get

- **28 numbered checks** in `checks/`. Each one has the exact words or form numbers to look for, where they hide in a policy, why they matter, the source with the date it was read, what you do, the question to ask your broker and a paste in prompt. Checks 1 to 3 are the three steps from the Reel. The other 25 are the rest of the hunt.
- **Prompts** in `prompts/`: a quick start, a full policy hunt, a broker email draft, a written request to the insurer and a report.
- **Templates** in `templates/`: an exclusion register, a broker question list, a renewal change log and an AI use map. They have made up sample rows labelled SAMPLE.
- **Tools** in `tools/` (Python standard library only): a validator that confirms the 28 checks, and a scanner that finds the exact words in a plain text policy with line and page numbers, on your own computer.
- **A Claude Code skill** in `.claude/skills/exclusion-hunt/`, plus `AGENTS.md` and `CLAUDE.md` for other assistants.
- **Docs** in `docs/`: start here, how to run it, honest limits, every source with the date read, a glossary and how to ask in writing.

## The easiest first step

Give your AI assistant this repo link and your policy PDF and say: **hunt for AI exclusions and tell me what to ask my broker first.**

Or paste the prompt in `prompts/01-QUICK-START.md`.

## Privacy warning

Your policy has your business name, addresses, policy numbers and sometimes claim history. Whatever you paste or upload goes to the company that runs the assistant. Remove personal data first, or use a tool whose data terms you trust. The scanner in `tools/` runs only on your computer and sends nothing anywhere.

## The 28 checks at a glance

| Checks | What they cover |
| --- | --- |
| 1 to 3 | The Reel steps: ask your broker in writing, write down where you use AI, keep proof a person checks AI output |
| 4 to 7 | The ISO general liability forms CG 40 47, CG 40 48, CG 35 08, and an insurer's own AI wording |
| 8 to 9 | How far an exclusion reaches: the definition of AI and words like arising out of |
| 10 to 16 | Management, employment and professional policies: absolute exclusions, hiring, AI washing, AI mistakes, professional services, affirmative endorsements, sublimits |
| 17 to 21 | Cyber, crime and property: AI attacks, deepfakes, social engineering, property cyber incident exclusions |
| 22 to 25 | Contracts, whose AI is reached, application questions, the renewal forms list |
| 26 to 28 | Claims made timing, state filings and silent AI |

The full list with links is in `checks/00-INDEX.md`.

## What it cannot do

- It cannot tell you what you are covered for, or promise a claim will be paid or refused.
- It is not legal advice. It is not a substitute for your broker or a lawyer.
- It cannot read a scanned PDF reliably. A match in the scanner is a place to read, and no match is not proof the wording is absent.
- It covers the United States only, and only the policy types listed above. It has no workers' compensation check because none of the sources read gave AI wording for it.
- Its sources were read on 2026-11-24 and wording changes. See `docs/02-HONEST-LIMITS.md` and `docs/03-SOURCES.md`.

## Run the tools

```text
python3 tools/validate_checks.py
python3 tools/scan_policy.py policy.txt
python3 -I -m unittest discover -s tests
```

Python 3.9 or newer. No packages to install. The tests run offline.

## License

MIT. Copyright (c) 2026 Onit Tindwani. ISO forms are copyrighted by Insurance Services Office; this kit quotes only form numbers and short phrases.

Version 1.0.0 (2026-11-24). Repository: https://github.com/onittindwani-ai/exclusion-hunt-checklist
