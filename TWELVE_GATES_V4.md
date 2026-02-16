# The Twelve Gates — v4.0 (PERMANENT)

**Every component, every PR. No exceptions.**

---

## Step 0: Identify Stakeholders

**For this project:** Nathan + CodeRabbit

---

## The Pattern (Applied to EVERY Step 1-12)

1. **Do the work** for Step N (write architecture, define scope, write code, etc.)
2. **Create PR or Issue** for Step N (captures work + asks for review)
3. **CodeRabbit reviews** (provides feedback)
4. **Loop until UNCONDITIONAL approval:**
   - If CodeRabbit suggests improvement:
     - Accept if valid → Redo the work → Update PR/Issue → Wait for re-review
     - Reject if invalid → Provide reasoning → Wait for re-review
   - Continue loop until CodeRabbit says **"APPROVED"** with NO conditions
5. **Only then** proceed to Step N+1

---

## Critical Rules

### 1. Unconditional Approval Required
- **"Approved with refinements"** = NOT approved
- **"LGTM but consider X"** = NOT approved
- **"Approved"** with no conditions = APPROVED ✓
- Must get explicit unconditional approval before moving forward

### 2. Every Change = PR (100% Strict)
- ALL work must go through PR or Issue
- Reason: Capture all logs, sequence of events, decisions
- No exceptions - even small changes need PR

### 3. Architecture Change = Back to Step 1
- If ANY step (2-12) requires architecture change → GO BACK TO STEP 1
- Then redo ALL steps sequentially: 1 → 2 → 3 → ... → N
- Example: At Step 7 (Build), realize architecture is wrong → Back to Step 1 → Get approval on new architecture → Then Step 2 → Step 3 → ... → Step 7

### 4. No Jumping - Always Sequential
- If you loop back from Step 7 to Step 1, you CANNOT jump back to Step 7
- You must go: Step 1 → 2 → 3 → 4 → 5 → 6 → 7 (sequential)
- Reason: Every step needs unconditional approval based on current architecture

### 5. Loop Within Same Step
- If Step 5 needs refinement, loop within Step 5 until approved
- Don't create new step - iterate on same PR/Issue
- Only move forward when unconditional approval received

---

## The Twelve Gates

### Gate 0: Identify Stakeholders ✓
**Stakeholders:** Nathan + CodeRabbit

### Gate 1: Architecture
**Action:** Design the system architecture
**Deliverable:** ARCHITECTURE.md or architecture section in Issue
**Review:** Create Issue/PR → CodeRabbit reviews architecture
**Loop:** Iterate until unconditional approval
**Proceed when:** CodeRabbit approves architecture unconditionally

### Gate 2: Scope
**Action:** Define what this PR/component covers (small, focused, minimal)
**Deliverable:** Scope section in Issue
**Review:** CodeRabbit reviews scope
**Loop:** Iterate until unconditional approval
**Proceed when:** CodeRabbit approves scope unconditionally
**If architecture changes:** Back to Gate 1

### Gate 3: Our Plan
**Action:** Write implementation plan with checklist (local or in Issue)
**Deliverable:** PLAN.md or plan section in Issue
**Review:** CodeRabbit reviews plan
**Loop:** Iterate until unconditional approval
**Proceed when:** CodeRabbit approves plan unconditionally
**If architecture changes:** Back to Gate 1

### Gate 4: Issue Planner
**Action:** Ask CodeRabbit to create its own plan
**Deliverable:** CodeRabbit's plan (in Issue comment)
**Review:** CodeRabbit provides plan
**Loop:** If plan unclear, ask clarifying questions
**Proceed when:** CodeRabbit's plan is clear and complete
**If architecture changes:** Back to Gate 1

### Gate 5: Compare
**Action:** Compare our plan (Gate 3) vs CodeRabbit's plan (Gate 4)
**Deliverable:** Comparison analysis (what's same, different, missing)
**Review:** Share comparison with CodeRabbit
**Loop:** Iterate until both plans aligned
**Proceed when:** CodeRabbit approves the comparison unconditionally
**If architecture changes:** Back to Gate 1

### Gate 6: Discuss
**Action:** Finalize the plan (merged best of both)
**Deliverable:** Final plan in Issue
**Review:** CodeRabbit reviews final plan
**Loop:** Iterate until unconditional approval
**Proceed when:** CodeRabbit approves final plan unconditionally
**If architecture changes:** Back to Gate 1

### Gate 7: Build
**Action:** Write code + tests + update docs
**Deliverable:** PR with all code changes
**Review:** CodeRabbit reviews code
**Loop:** Iterate until unconditional approval
**Proceed when:** CodeRabbit approves code unconditionally
**If architecture changes:** Back to Gate 1

### Gate 8: Review
**Action:** CodeRabbit performs full code review
**Deliverable:** Review comments on PR
**Review:** Address every finding
**Loop:** Fix → Push → Re-review until unconditional approval
**Proceed when:** CodeRabbit approves PR unconditionally
**If architecture changes:** Back to Gate 1

### Gate 9: Fix
**Action:** Address ALL review findings (accept or reject with reasoning)
**Deliverable:** Updated PR with fixes + reasoning for rejections
**Review:** CodeRabbit re-reviews
**Loop:** Iterate until unconditional approval
**Proceed when:** CodeRabbit confirms all findings resolved unconditionally
**If architecture changes:** Back to Gate 1

### Gate 10: Re-review
**Action:** CodeRabbit verifies fixes are clean
**Deliverable:** Clean PR with no open findings
**Review:** CodeRabbit confirms
**Loop:** If new issues found, back to Gate 9
**Proceed when:** CodeRabbit confirms clean unconditionally
**If architecture changes:** Back to Gate 1

### Gate 11: Test
**Action:** Run full test suite + CI/CD
**Deliverable:** All tests passing
**Review:** CodeRabbit verifies test results
**Loop:** If tests fail, fix and re-run
**Proceed when:** All tests pass + CodeRabbit approves unconditionally
**If architecture changes:** Back to Gate 1

### Gate 12: Merge
**Action:** Merge PR when all stakeholders satisfied
**Deliverable:** Merged code
**Review:** Final check
**Proceed when:** Both Nathan + CodeRabbit fully satisfied

---

## Example Flows

### Happy Path (No Changes)
Gate 0 ✓ → Gate 1 (approved) → Gate 2 (approved) → Gate 3 (approved) → ... → Gate 12 ✓

### Architecture Change at Gate 5
Gate 0 ✓ → Gate 1 (approved) → Gate 2 (approved) → Gate 3 (approved) → Gate 4 (approved) → Gate 5 (architecture issue!) → **Back to Gate 1** → Gate 1 (new architecture approved) → Gate 2 → Gate 3 → Gate 4 → Gate 5 → ... → Gate 12 ✓

### Loop Within Gate (Refinements)
Gate 7 (Build):
1. Write code → PR created
2. CodeRabbit: "Approved with refinements: add error handling"
3. STATUS: **NOT APPROVED** (conditional)
4. Fix: Add error handling → Update PR
5. CodeRabbit re-reviews
6. CodeRabbit: "Approved"
7. STATUS: **APPROVED** ✓
8. Proceed to Gate 8

---

## Process Philosophy

**Why so strict?**
- Captures complete audit trail (every decision, every change)
- Ensures architecture stays coherent (no drift)
- Forces explicit approval at every stage (no assumptions)
- Treats CodeRabbit as equal stakeholder (not just advisor)
- Makes process repeatable and traceable
- Prevents "vibe coding" and shortcuts

**Core principle:** The gates exist so every voice is heard. If someone helps you, come back and verify. Skipping that is disrespect. Treat your reviewers as yourself.

---

## The Permanent Solution Principle (CRITICAL)

**Always be flexible to change architecture. No shortcuts. No workarounds. Only permanent, top-grade solutions.**

### Rules

1. **Architecture is flexible** - If wrong at ANY gate, go back to Gate 1 and fix it
2. **No cheap tricks** - No conditional imports, optional dependencies, or "works for now" hacks
3. **Permanent over fast** - Quality and permanence trump speed
4. **NASA-grade only** - No compromises, no "good enough"
5. **Root cause always** - Fix the real problem, not symptoms

### Examples

**❌ WRONG (Shortcuts):**
- "Let's make it optional for now"
- "We can add a workaround here"
- "This hack will get us moving"
- "We've done too much work to change architecture now"

**✅ RIGHT (Permanent):**
- "The architecture is wrong. Back to Gate 1."
- "This needs a proper solution. Let me redesign."
- "I'd rather redo the work than ship a hack."
- "Validate first, then deploy. No shortcuts."

### Why This Matters

| Shortcut Thinking | Permanent Thinking |
|------------------|-------------------|
| Technical debt accumulates | Clean foundation stays clean |
| "Works for now" breaks later | Works forever |
| Fast today, slow tomorrow | Steady pace, no rework |
| Fragile, brittle system | Robust, maintainable system |

**Remember:** We are Netanel Systems. "Gift of God." NASA-grade standards. No compromises.

---

**Established:** 2026-02-14 by Klement + Nathan
**v3.1:** 2026-02-15 (Added loops and gate decision documentation)
**v4.0:** 2026-02-16 (Strict unconditional approval + sequential flow + architecture loop-back)
