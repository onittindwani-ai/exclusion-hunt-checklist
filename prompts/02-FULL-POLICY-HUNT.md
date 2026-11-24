# Full policy hunt prompt

Use this after the quick start, once you have the policy as text. Paste the policy text (or attach it) after the prompt.

Tip: run the scanner first (`python3 tools/scan_policy.py policy.txt`). It shows where the exact words appear, with line numbers, on your own computer. Then paste its result with the policy so the assistant starts from real hits.

```text
Run all 28 checks from the folder `checks/` on the policy text below, one policy at a time. Name the policy and the carrier at the top.

For each check give one row: check number, short title, FOUND / NOT FOUND / UNCLEAR, the exact line copied from the text, the page, the form or section name, and one plain sentence on what the wording says (not what it means for my cover).

Rules:
- This is not insurance or legal advice. Never say I am covered or not covered. Never say a policy is safe.
- NOT FOUND only means you did not see the words in this text. Say that, because scanned text can be wrong.
- Checks 2 and 3 are about my own records, and check 27 is done on a state website, so mark them "needs me" and say what I must do.
- If a check does not apply to this type of policy, say "does not apply to this policy type".
- Use the words listed in each check file under "Exact words to look for". Do not invent other form numbers.
- After the table, list the checks marked FOUND first, then UNCLEAR, then NOT FOUND.
- Finish with: the 5 most important broker questions, taken from the "Ask your broker or carrier" part of the checks that matter most.

My list of where I use AI (if I have one): [paste it here]

Policy text:
[paste here]
```
