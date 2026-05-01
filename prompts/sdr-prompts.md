# SDR Prompt Library

> Copy-paste ready prompts for Sales Development Representatives.
> Replace `[bracketed text]` with your specifics.

---

## Account Research

### Full Account Research Brief
```
Run account-research on [Company Name] ([company.com]).

I need:
- Funding history (all rounds, total raised, lead investors, latest valuation)
- Tech stack (cloud infrastructure, DevOps tools, data platforms, languages)
- Headcount trend over last 12 months — which teams growing or shrinking?
- Recent leadership changes in Engineering, IT, or Operations
- Any public mentions of cost, efficiency, or platform challenges
- Upcoming events: earnings calls, product launches, conferences
- 3 personalized pain point hypotheses for a [your service type] pitch

Output: one-page brief to the [Company] Notion deal room.
Flag any data points older than 90 days as "Needs Verification."
Confidence rating: High / Medium / Low per section.
```

### Quick Trigger Research (Pre-Outreach)
```
Quick account-research for [Company] before I reach out.

Focus only on:
1. Most recent funding or news event (1-2 lines)
2. Their current cloud or infrastructure setup (1-2 lines)
3. One specific pain signal I can reference in a cold email
4. Best title to target for [our service] (SDR guidance)

Keep output to one paragraph. Speed matters more than depth here.
```

### Tech Stack Identification
```
Identify the tech stack at [Company] ([company.com]).

Focus on:
- Cloud provider(s) in use (AWS / GCP / Azure / multi-cloud)
- Container orchestration (Kubernetes, ECS, EKS, GKE, etc.)
- CI/CD toolchain (Jenkins, GitHub Actions, CircleCI, etc.)
- Monitoring and observability tools
- Data platform (Snowflake, Databricks, BigQuery, etc.)
- Any tools that compete with or complement [our product/service]

Source: BuiltWith, LinkedIn job postings, GitHub public repos, blog posts.
Flag any uncertainty.
```

---

## Cold Outreach

### Email — First Touch (Pain-Led)
```
Draft a cold email first touch to [First Name], [Title] at [Company].

Context from research brief:
- Company trigger: [funding round / leadership hire / product launch / news]
- Their likely pain: [specific challenge based on research]
- Our relevant differentiator: [specific value prop, not generic]

Requirements:
- Tone: peer-to-peer, not salesy
- Length: 100–120 words max
- No buzzwords (no "synergy", "leverage", "best-in-class", "cutting-edge")
- One clear, low-friction call to action (not "let's hop on a call")
- 3 subject line options (A/B/C variants)
- P.S. line that adds credibility (case study, stat, or mutual connection)
```

### Email — First Touch (Insight-Led)
```
Draft a cold email to [First Name], [Title] at [Company].

Open with an insight about their industry, not about us.
The insight: [paste relevant industry trend, stat, or news]

Then bridge to: why this matters specifically for [Company] based on their situation.
Then: what we do about it (one sentence, specific).
CTA: one specific question or a soft request for a 15-min call.

Max 110 words. Subject line should reference the insight, not our company name.
```

### LinkedIn Connection Request
```
Write a LinkedIn connection request from me ([Your Name]) to [Name], [Title] at [Company].

Context: [reference their recent post / shared connection / mutual event / company news]
Goal: get accepted + start a conversation

Requirements:
- Max 280 characters (LinkedIn limit)
- Reference something specific (not generic "saw your profile")
- No pitch in the connection request itself
- Conversational tone
```

### LinkedIn Follow-Up (After Connection Accepted)
```
Draft a LinkedIn follow-up message to [Name] at [Company] who just accepted my connection.

Context:
- We connected because: [reason]
- Their role: [title and likely responsibilities]
- Our value: [specific to their role]

Goal: start a genuine conversation, not pitch immediately.
Max 400 characters.
Offer something of value (insight, resource, question) before asking for time.
```

### 4-Touch Email Sequence
```
Draft a 4-touch outreach sequence for [Title] at [Company].

Persona: [describe: technically fluent / business-focused / skeptical / growth-oriented]
Key insight from research: [paste 2-3 sentences from research brief]
Our value prop for this persona: [specific]

Sequence:
- Touch 1: Email — lead with their pain, not our product (120 words)
- Touch 2: Email follow-up — add new value, don't just follow up (80 words)
- Touch 3: LinkedIn message (280 chars max)
- Touch 4: Breakup email — permission to say no (60 words)

Tone consistent across all 4. No "just checking in." No "circling back."
```

---

## Follow-Up & Sequence Management

### Follow-Up After No Response (Email)
```
[Prospect] hasn't responded to my email sent [X days] ago.

Draft a follow-up email that:
1. Doesn't reference "following up" or "checking in"
2. Adds a new piece of value (use this: [insight / case study / news])
3. Changes the angle slightly from the first email
4. Has a different, compelling subject line

Max 80 words. Soft CTA (question or observation, not hard ask for meeting).
```

### Re-Engagement After Long Silence
```
[Name] at [Company] went silent after [last interaction — e.g., "attending our webinar" / "downloading our content"].
Last contact: [X] days ago.

Draft a re-engagement email that:
1. Acknowledges time has passed without making it awkward
2. References a new trigger event at their company: [event]
3. Offers something new (not what we offered before)
4. Makes it easy to say "not interested" (gives them an out)

Max 90 words. Subject line should feel like it's from a peer, not a vendor.
```

### Meeting Confirmation
```
[Name] just agreed to a 30-minute call on [date/time].

Draft a meeting confirmation email that:
1. Confirms logistics (date, time, timezone, video link)
2. Sets a brief agenda (2-3 bullets, not too formal)
3. Builds anticipation / credibility without overselling
4. Asks one pre-call question to gather context

Keep it warm and professional. Under 100 words plus agenda bullets.
```

---

## Qualification & Research Support

### ICP Scoring Research
```
Score [Company] against our ICP criteria:

ICP criteria:
- Industry: [target industries]
- Headcount: [range]
- Annual revenue: [range]
- Tech stack signals: [required tools/platforms]
- Growth signals: [hiring growth, funding, expansion]
- Pain signals: [specific challenges we solve]

For each criterion: score 1–3 (1=poor fit, 2=acceptable, 3=strong fit).
Total score out of [max].
Recommendation: Pursue / Deprioritize / Monitor.
Top 2 reasons to pursue or not pursue.
```

### Competitive Overlap Check
```
Check if [Company] is likely already using or evaluating [Competitor Name].

Look for:
- LinkedIn job postings that mention [Competitor] tools
- Tech stack data (BuiltWith, Stackshare)
- Case studies or press releases mentioning [Competitor]
- Review sites (G2, Capterra) for [Company] employee reviews mentioning [Competitor]

Output: likelihood they're using [Competitor] (High/Medium/Low) + evidence.
If using competitor: suggest how to position our differentiation.
```
