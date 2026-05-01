# Sales Manager Prompt Library

> Copy-paste ready prompts for Sales Managers and Revenue Leaders.
> Replace `[bracketed text]` with your specifics.

---

## Pipeline Management

### Weekly Pipeline Review (/pipeline-review)
```
/pipeline-review Analyze [full team / AE Name]'s [Q2] pipeline.

Flag the following and prioritize by urgency:

1. STALLED DEALS: stuck in same stage for >21 days
2. DARK DEALS: no CRM activity or email in >10 days
3. MEDDIC GAPS: missing required qualification fields (Economic Buyer, Decision Process, or Pain)
4. SLIPPED CLOSE DATES: close date moved back more than once
5. SINGLE-THREADED: only one contact engaged at the account
6. RISKY CLOSE DATES: close date within 30 days but deal health is Yellow or Red

For each flagged deal: deal name, AE, current stage, specific issue, recommended next action.

Sort by: revenue at risk (largest first).
Post to #pipeline-review Slack channel with @here tag.
```

### Deal Risk Assessment
```
Assess the risk of [Deal Name] at [Company].

Deal data:
- AE: [name]
- Stage: [stage]
- Value: $[amount]
- Close date: [date]
- Days in current stage: [N]
- MEDDIC completeness: [paste known fields]
- Last activity: [date and description]
- Competitor(s): [names]
- Champion: [name/title or unknown]
- Economic buyer engaged: Y/N

Assess:
1. Probability of closing by stated date (High/Medium/Low) + rationale
2. Top 2 risks to closing this deal
3. What must happen in the next 14 days to keep it on track
4. Is the deal size realistic given what we know?
5. Coaching recommendation for the AE on this deal
```

### End-of-Quarter Push Planning
```
It's [date], [N] weeks before end of [Q].

My team's current position:
- Quota: $[amount]
- Closed to date: $[amount]  
- Gap: $[amount]
- Commit pipeline: [paste deal list with values and stages]
- Upside pipeline: [paste deal list]

Generate a Q-end push plan:
1. Deals most likely to close this quarter (rank by probability × value)
2. Deals worth accelerating with special effort or executive engagement
3. Deals to deprioritize until next quarter
4. Specific actions for each "closable" deal this week
5. Deals where I should get involved as a manager (executive sponsor, competitive intel, pricing authority)

Output: prioritized action list by deal, with owner and timeline.
```

### Pipeline Health Report (Monthly)
```
Generate a monthly pipeline health report for [Month/Quarter].

Data: [paste pipeline summary or describe current state]

Report sections:
1. Pipeline coverage: total pipeline vs. quota (target: 3x coverage minimum)
2. Stage distribution: deals by stage (are we front-loaded or back-loaded?)
3. Deal velocity: average days per stage vs. our target
4. Win/loss summary this month: # won, # lost, common reasons for each
5. New pipeline added this month vs. target
6. Deals lost to inactivity (went dark, no close)
7. Forecast accuracy: last month's commit vs. actual

Identify: top 3 pipeline health concerns and recommended corrective actions.
```

---

## Forecasting

### Quarterly Forecast (/forecast)
```
/forecast Generate [Q2] forecast for my team.

Team pipeline: [paste deal list: Company / AE / Stage / Value / Close Date / AE Confidence %]
Team quota: $[total amount]
Closed to date: $[amount]

Weighting:
- Closed Won: 100%
- Commit: 90%
- Best Case: 50%
- Pipeline: 20%
- Upside: 10%

Output:
1. Weighted forecast total
2. Best Case / Most Likely / Worst Case scenarios
3. Gap to quota in each scenario
4. Deals where AI confidence differs significantly from AE-stated confidence (flag these)
5. Top 3 deals to watch that could swing the forecast significantly
6. Recommended actions to close the gap (if gap exists)

Post to #sales-forecast with a 2-paragraph executive narrative.
```

### Deal-Level Probability Audit
```
Review AE-stated close probabilities for my team's pipeline and flag outliers.

Pipeline: [paste or describe]

For each deal, evaluate whether the AE's probability is:
- Realistic (supported by MEDDIC data, stage, and activity)
- Optimistic (higher than warranted — explain why)
- Pessimistic (lower than warranted — explain why)

Flag any deal where:
- AE has 80%+ confidence but Economic Buyer is not identified
- AE has 70%+ confidence but no champion confirmed
- AE has 60%+ confidence but close date is beyond 90 days with no contract in review
- AE has 50%+ confidence but deal has been in current stage for >30 days

Coaching recommendation for each flagged deal.
```

### Board / Leadership Forecast Narrative
```
Write a 2-paragraph forecast narrative for our [Q2] board / leadership review.

Data:
- Quota: $[amount]
- Current forecast (weighted): $[amount]
- Closed to date: $[amount]
- Key deals in forecast: [list top 3-5 with status]
- Key risks: [list]
- Key upside: [list]

Paragraph 1: current state and confidence in forecast (factual, no spin)
Paragraph 2: risks and what we're doing to mitigate them, + upside opportunities

Tone: direct, data-driven, honest. No fluff. Suitable for a CEO or board member.
Length: 150-200 words total.
```

---

## Coaching & Team Development

### Call Coaching Review
```
Review this call transcript and provide coaching feedback for [AE Name].

Transcript: [attach or paste]
Call type: [discovery / demo / negotiation / close attempt]
Account: [Company]
Deal stage: [stage]

Score the call (1–5 each):
1. Opening: did they establish credibility and set a clear agenda?
2. Discovery depth: did they uncover economic impact and decision process?
3. Listening: did they ask follow-up questions or just stick to a script?
4. Competitive positioning: did they differentiate effectively if competition mentioned?
5. MEDDIC advancement: which new qualification fields were confirmed?
6. Objection handling: how did they respond to pushback?
7. Close / next step quality: was the next step specific, committed, and calendar-booked?

Provide:
- 3 specific coaching points with timestamps from the transcript
- 1 thing they did well (be specific)
- 1 drill or exercise to improve their weakest area

Keep feedback constructive and example-based (not generic advice).
```

### Win/Loss Analysis
```
Analyze our win/loss data for [Q] [year].

Won deals summary: [paste or describe — company, size, industry, key reasons won]
Lost deals summary: [paste or describe — company, size, industry, key reasons lost]

Analyze:
1. Win patterns: what do our won deals have in common? (industry, size, use case, champion profile)
2. Loss patterns: where do we consistently lose? (competitor, pricing, timing, use case)
3. Win/loss by competitor: where do we win vs. [Competitor 1], [Competitor 2]?
4. Deals we shouldn't have pursued (time wasted on poor-fit deals)
5. Deals we lost that were winnable (what could have changed the outcome?)

Recommendations:
- 2 changes to ICP definition based on win patterns
- 2 competitive talk track improvements based on loss patterns
- 1 process change to improve qualification and avoid wasted pipeline
```

### New Hire Ramp Plan Assessment
```
[AE Name] is [N] weeks into their ramp.

Their activity to date:
- Calls completed: [N]
- Deals created: [N with values]
- Pipeline value: $[amount]
- Deals in active stages: [list]
- Skills demonstrated: [list what you've observed]
- Areas of concern: [list what you've noticed]

Assess:
1. Are they on track for their ramp milestone at [N] months? (Yes / At Risk / No)
2. Where specifically are they struggling (top of funnel / qualification / demo / close)?
3. Top 3 coaching priorities for the next 30 days
4. Resources or training to assign
5. Deals where I should shadow or co-sell to accelerate their learning

Output: a 30-day coaching plan with specific weekly actions.
```

---

## Competitive Intelligence

### Competitor Battle Card Request
```
Generate an updated battle card for [Competitor Name].

Focus areas:
1. How they position against us (their messaging, not ours)
2. Where they genuinely beat us (be honest — AEs need to know)
3. Where we beat them (with proof points, not just claims)
4. Deal-stage-specific talk tracks:
   - Discovery: questions to ask that surface [Competitor] weaknesses
   - Demo: features to emphasize when [Competitor] is in evaluation
   - Proposal: how to frame our pricing vs. their pricing
   - Close: objections they'll plant and how to address each
5. Red flags: situations where we should NOT compete with them (deals we'll lose)
6. Recent changes: new features, pricing changes, acquisitions, customer wins/losses

Source: recent transcripts, win/loss data, public intel (their website, G2, press releases).
Last updated: [today's date]. Flag anything older than 90 days as "Needs Verification."
```

### Market Intelligence Briefing
```
Generate a competitive market intelligence briefing for the [your sector] market.

Focus period: last 90 days.

Cover:
1. Major moves by [Competitor 1]: product releases, pricing changes, customer wins, personnel
2. Major moves by [Competitor 2]: same
3. Emerging competitors or new entrants in our space
4. Customer sentiment trends (G2, Gartner, Reddit, LinkedIn)
5. Analyst coverage: any new reports or ratings that affect how buyers evaluate the market
6. Implications for our team: what should AEs know before their next competitive deal?

Output: 1-page briefing suitable for distribution to the full presales team in Slack.
Length: 500 words max. Bullet points preferred. No fluff.
```
