# Start here

This kit helps a business owner find out, with an AI assistant, whether their business insurance policies have wording about AI (artificial intelligence) that may limit cover, and what to ask their broker about it. You do not need to know anything about AI or insurance to start. Every term is explained in the glossary (`04-GLOSSARY.md`).

It is not insurance or legal advice. It never tells you what you are covered for. It helps you find the words and ask better questions.

## The 3 steps from the Reel (checks 1 to 3)

1. Ask your broker, in writing, if your policy has a generative AI exclusion, and if your cyber and professional policies cover AI mistakes.
2. Write down everywhere your business uses AI (emails, ads, a chatbot, hiring), so you can analyze the risk. A blank list is in `templates/ai-use-map.csv`.
3. Keep proof that a person checks what the AI sends out.

That is 3 of the 28 checks. The other 25 are in the `checks/` folder.

## What you need

- Your policies. Ask your broker for the full policy and the list of forms and endorsements (the "forms schedule") for each one.
- 30 to 60 minutes for a first pass.
- An AI assistant (Claude Code, Codex, ChatGPT or similar). The easiest start is `prompts/01-QUICK-START.md`.
- Optional: Python 3.9 or newer, to run the scanner on your own computer.

## The easiest first step

Give your AI assistant this repo link and your policy PDF and say: hunt for AI exclusions and tell me what to ask my broker first.

Before you upload a policy, remove personal data (names, addresses, policy numbers, bank details, claim history) or use a tool whose data terms you trust. Your policy goes to the company that runs the assistant.

## The path

1. Collect each policy and its forms schedule.
2. Turn each policy into plain text (see `01-RUN-WITH-AN-AI-ASSISTANT.md`). A scanned PDF may not turn into good text.
3. Optional: run `python3 tools/scan_policy.py policy.txt`. It lists where the exact words appear, with line numbers.
4. Run the checks with your assistant (`prompts/02-FULL-POLICY-HUNT.md`).
5. Send the broker email (`prompts/03-BROKER-EMAIL-DRAFT.md`). Keep the written answers.
6. Record every finding in `templates/exclusion-register.csv`. Do it again at every renewal (`templates/renewal-change-log.csv`).

## How to read a result

- FOUND means the words are in the text you gave. It does not mean what you think it means for you. Ask your broker.
- NOT FOUND means the words were not seen in that text. That is not proof they are absent, and it is not proof you are covered.
- UNCLEAR means the text was messy or the check needs something outside the policy.
- Pass in a check file only means you got a clear written answer. It never means you are covered.

## What is in the folders

- `checks/`: the 28 checks, each with the exact words, where they hide, why they matter, the source and date read, what you do, the question for your broker and a paste in prompt.
- `prompts/`: copy and paste prompts.
- `templates/`: a register, a broker question list, a renewal log and an AI use map, each with made up sample rows.
- `tools/`: a checker that counts and validates the 28 checks, and a scanner for plain text policies. Both use only Python's standard library and send nothing anywhere.
- `docs/`: this page, how to run it, the honest limits, the sources and a glossary.
- `.claude/skills/exclusion-hunt/`: a Claude Code skill that runs the hunt the same way.
