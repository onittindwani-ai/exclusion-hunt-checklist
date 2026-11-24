# Check 22: Check your contracts with customers and AI vendors for who carries the risk

- Check number: 22
- Group: Contracts, applications and renewals
- Policy types: General liability (contractual liability), all policies

## Exact words to look for

Wording from the sources (a [common] tag means ordinary wording that proves nothing alone):

- `insured contract` [common]
- `contractual liability` [common]

Search aid words (helpers, not quotes from a form):

- `indemnify`
- `hold harmless`
- `limitation of liability`
- `warranty`

## Where it hides in a policy

Not only in the policy: in the customer contracts you sign and the terms of your AI software. In the policy, contractual liability is an exclusion with an exception for what the policy calls an insured contract.

## Why it matters

A law firm article advises reviewing contracts with customers and AI vendors for gaps in indemnity (who promises to cover whose losses). A person quoted in trade press says vendor contracts and base model terms place liability for AI outputs on the business that uses the tool. A forms reference site says the 04 13 edition of the general liability form excludes contractual liability except for insured contracts. If you promise a customer more than your policy covers, you carry the difference.

## Source

- Source ID: L1
  - Title: The Continued Rise of Generative AI Exclusions in Commercial Insurance Policies: What Policyholders Need to Know
  - URL: https://www.olshanlaw.com/assets/htmldocuments/Legal%20Intelligencer%20-%20The%20Continued%20Rise%20of%20Generative%20AI%20Exclusions%20in%20Commercial%20Insurance%20Policies%20-%20What%20Policyholders%20Need%20to%20Know%20Crawford%205-15-26.pdf
  - Date read: 2026-11-24
  - Evidence: A: text read directly from the document
  - Used here for: Advises reviewing contracts with customers and AI vendors for indemnity gaps.
- Source ID: T7
  - Title: Why your clients probably aren't covered for AI
  - URL: https://www.insurancebusinessmag.com/us/news/professional-liability/why-your-clients-probably-arent-covered-for-ai-597354.aspx
  - Date read: 2026-11-24
  - Evidence: B: page read through a page reader tool, wording is as reported
  - Used here for: Reports a quoted view that vendor and model terms put liability for AI outputs on the user.
- Source ID: T11
  - Title: CG 00 01 Commercial General Liability Coverage Form (form information page)
  - URL: https://insurancexdate.com/insurance-forms/CG/CG-00-01/
  - Date read: 2026-11-24
  - Evidence: B: page read through a page reader tool, wording is as reported
  - Used here for: States the contractual liability exclusion with an insured contract exception in the 04 13 edition.

## What you do

1. List each AI vendor you use and find their terms on who is responsible for output.
2. List customer contracts that promise accuracy, results or indemnity.
3. Ask your broker whether these promises are inside your cover.

## Ask your broker or carrier

> Do the indemnity promises in my customer contracts, and the terms of my AI vendors, fit inside my policies? Which promises might not be covered?

Send it by email so the answer is in writing.

## Paste-in prompt

```text
You are helping me read my own insurance policy text. This is not insurance or legal advice. Never tell me whether I am covered or not covered.

Task: run check 22 only: "Check your contracts with customers and AI vendors for who carries the risk"

Look in the policy text I paste for these words. Ignore capital letters. A line break may split a phrase, and a form number may have different spacing:
  insured contract; contractual liability
Also look for these helper words (they are search aids, not quotes from a form):
  indemnify; hold harmless; limitation of liability; warranty

For every hit give: the exact line copied from the text, the page if the text shows one, and the name of the form or section it sits in.
Then answer with exactly one of: FOUND, NOT FOUND or UNCLEAR. Use UNCLEAR if the text looks scanned, cut off or messy.
Look for the contractual liability exclusion and the insured contract wording.
Never guess. Never fill a gap. If you did not see it in the text, say so.

Finish with: Ask your broker: Do the indemnity promises in my customer contracts, and the terms of my AI vendors, fit inside my policies? Which promises might not be covered?
```

## Pass or needs work

Result: [ ] Pass   [ ] Needs work   [ ] Could not tell

Pass here only means you found the wording or got a clear written answer and understood it. It never means you are covered.

Notes:
