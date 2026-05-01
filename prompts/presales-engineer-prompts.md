# Presales Engineer Prompt Library

> Copy-paste ready prompts for Solutions Engineers / Presales Engineers.
> Replace `[bracketed text]` with your specifics.

---

## Technical Discovery

### Full Technical Discovery Brief
```
Generate a technical discovery brief for [Company] — pre-call research.

What I know about their environment:
- Current stack: [paste from research brief or CRM]
- Project scope: [migration / new build / modernization / integration]
- Team size: [engineering headcount if known]
- Timeline: [customer's stated timeline]

Technical questions I need answered in this call:

Architecture & Design:
- Current architecture: monolith / microservices / serverless / hybrid?
- Data volumes and throughput requirements?
- Any hard architectural constraints or non-negotiables?

Infrastructure & Operations:
- Current cloud setup (on-prem / cloud provider / hybrid)?
- Container/orchestration maturity?
- CI/CD pipeline and deployment frequency?

Security & Compliance:
- Compliance requirements: SOC2 / HIPAA / PCI / ISO27001 / FedRAMP?
- Data residency requirements?
- Identity and access management setup?

Team & Skills:
- Platform/infra team size and current capacity?
- Key skill gaps they're trying to address?
- Appetite for managed services vs. self-managed?

Integration:
- Key systems that need to integrate with the new solution?
- API strategy: REST / gRPC / event-driven?
- Any legacy systems that cannot be replaced?

Output: structured technical brief in [Company] Notion deal room — "Calls" tab.
```

### Technical Risk Assessment
```
Assess technical risks for the [Company] [project type] deal.

Deal scope: [description]
Their environment: [paste tech stack summary]
Our proposed solution: [description]

Identify:
1. Top 3 technical risks (likelihood × impact for each)
2. Migration / implementation risks specific to their stack
3. Integration complexity hotspots
4. Skills gaps that could slow delivery
5. Security or compliance risks not yet addressed

For each risk: likelihood (High/Med/Low), impact (High/Med/Low), mitigation approach.

Also: what questions must I ask in the next technical call to validate or dismiss each risk?
```

### Competitor Technical Comparison
```
Create a technical comparison of our solution vs. [Competitor] for [Company]'s use case.

Use case: [specific: e.g., "Kubernetes migration from VMware for a fintech with SOC2 requirements"]

Compare on:
1. Architecture approach (how each solution works)
2. Scalability and performance characteristics
3. Security and compliance capabilities
4. Integration ecosystem
5. Operational complexity (day-2 operations)
6. Migration path from their current state
7. Total cost of ownership (implementation + ongoing)

Format: side-by-side comparison table + 1-paragraph narrative on why we win for their specific use case.
Keep all claims factual and defensible (cite docs/benchmarks where possible).
```

---

## Technical Assets

### Technical One-Pager (create-an-asset)
```
Create a technical one-pager for [Company].

Audience: [Their Platform Engineering Lead / VP Engineering / CTO]
Tone: peer-to-peer, architectural, credible — not marketing-speak

Their situation: [2-3 sentences from discovery call]
Their goal: [specific outcome they want]
Our proposed approach: [your solution overview]

Document structure:
1. Current State: what they're dealing with (their pain, in their technical language)
2. Our Approach: how we solve it (architecture overview, key components)
3. Implementation Phases: 3-4 phases with milestones and durations
4. Risk Mitigations: top 3 risks and how we address each
5. Our Toolchain: technology stack we bring and why it fits their environment
6. What Success Looks Like at 90 Days: specific, measurable outcomes

Length: 1 page (A4), suitable for printing and leaving behind.
Use their technical terminology. No vendor jargon.
```

### Architecture Overview Document
```
Create an architecture overview document for [Company]'s proposed [solution name].

Context:
- Their current architecture: [description]
- Target architecture: [description]
- Key constraints: [list: budget, timeline, compliance, team skills]
- Scale requirements: [users, transactions, data volume]

Document sections:
1. Architecture Diagram Description (describe components and data flows in text — I'll convert to diagram)
2. Component Breakdown: each major component, purpose, technology choice, and rationale
3. Data Flow: how data moves through the system
4. Security Architecture: authentication, authorization, encryption, network topology
5. Scalability: how the architecture scales (horizontal/vertical, auto-scaling triggers)
6. Disaster Recovery: RPO/RTO targets and how they're met
7. Monitoring & Observability: what we'll instrument and how

Technical depth: suitable for review by a senior engineer or architect.
```

### POC / Pilot Plan
```
Create a Proof of Concept plan for [Company].

Business goal of POC: [what success means to the buyer]
Technical goal of POC: [specific hypothesis to test]
Timeline: [duration, e.g., "3 weeks"]
Resources required: [from us / from them]

POC Plan structure:
1. Success Criteria: specific, measurable, agreed upfront (not vague)
2. Scope: what's in the POC (narrow) and what's explicitly out of scope
3. Technical Setup: environment, data, integrations required
4. Week-by-week milestones: what gets built/tested each week
5. Evaluation Criteria: how we'll measure success (performance, functionality, ease of use)
6. Go/No-Go Decision Framework: what outcome moves to commercial engagement

Tone: collaborative and practical. This is a joint plan, not a sales pitch.
Format: suitable for sharing with their engineering lead for sign-off.
```

### Demo Script
```
Create a demo script for [Company] — [demo type: discovery demo / technical deep-dive / executive demo].

Audience: [titles attending]
Duration: [30 / 45 / 60] minutes
Key pain points to address: [list from discovery]
Their tech stack context: [relevant details to reference]
Competitor they mentioned: [name or none]

Script structure:
1. Opening hook: reference their specific situation (30 seconds, not generic)
2. Agenda framing: set expectations (30 seconds)
3. Demo flow: [3-4 scenarios that map to their stated pains]
   - Scenario 1: [pain] → show [feature/capability] → connect to their outcome
   - Scenario 2: [pain] → show [feature/capability] → connect to their outcome
   - Scenario 3: [pain] → show [feature/capability] → connect to their outcome
4. Objection handling pauses: where to stop and ask for reactions
5. Closing: summarize what they saw, proposed next step, open for Q&A

Include: transition phrases between sections and suggested discovery questions to weave in.
```

---

## Post-Call & Proposal Support

### Technical Call Summary
```
/call-summary [Company] technical call — [date]
Transcript: [attach or paste]

Extract for technical review:
1. Technical requirements confirmed (vs. what we assumed)
2. Technical requirements changed or newly discovered
3. Architecture decisions made or proposed
4. Open technical questions that need answers before proposal
5. Technical objections raised and how we responded
6. Integration dependencies confirmed
7. Security/compliance requirements confirmed
8. Technical next steps with owners and dates
9. Risks identified during the call
10. Recommendation: ready for proposal Y/N? If not, what's needed?

Post to [Company] Notion deal room — "Calls" tab.
Flag any "blockers to proposal" in red.
```

### Technical Requirement Validation
```
Review our proposed solution against [Company]'s requirements.

Their requirements (from discovery):
[paste or summarize their stated technical requirements]

Our proposed solution: [description]

For each requirement:
- Does our solution meet it? (Yes / Partially / No / Unknown)
- If Partially or No: what's the gap and how do we address it?
- If Unknown: what do we need to verify?

Output: requirements traceability matrix.
Flag any gaps that could affect the proposal or create delivery risk.
Recommend: proceed with proposal / need another technical call first.
```

### Implementation Effort Estimate
```
Provide a rough implementation effort estimate for [Company]'s [project].

Scope summary: [paste from discovery or proposal]
Their environment: [key technical context]
Constraints: [timeline, budget signal, team involvement]

Estimate by phase:
- Phase 1: [description] — [weeks] — [# of engineers]
- Phase 2: [description] — [weeks] — [# of engineers]
- Phase 3: [description] — [weeks] — [# of engineers]

For each phase:
- Key deliverables
- Assumptions (what must be true for this estimate to hold)
- Risk factors that could extend timeline
- Customer involvement required

Disclaimer: this is a rough order of magnitude estimate. Final sizing requires [prerequisites].
```

### RFP / RFI Response Section
```
Draft a response to this RFP section for [Company]:

RFP question: "[paste exact question]"

Context about their environment: [paste relevant details]
Word limit: [if specified]
Evaluation criteria they mentioned: [if known]

Response requirements:
- Be specific to their environment and stated requirements
- Use concrete examples from similar implementations (anonymized if needed)
- Quantify where possible (performance metrics, implementation timelines, team sizes)
- Avoid generic marketing language
- Address any implicit concerns behind the question

Draft: [N] words. Confident, technically credible tone.
```
