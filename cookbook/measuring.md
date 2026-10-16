# Measuring whether a map helps (method)

**Status:** method profile — documents *how* to measure, not measured results.  
**Do not** paste invented before/after numbers into this file.

This is an optional cookbook pattern. It is **not** Core MUST and not required for Orientation conformance.

---

## Goal

Check whether a **sparse local map** improves orientation on *your* real work — with an honest A/B, not a slogan.

Related: root README “Experiment before you expand” and [`MOTIVATION.md`](../MOTIVATION.md).

---

## 1. Choose 10–20 real tasks

Pick tasks that already happened or will happen soon:

- Prefer tasks that need **finding the right package/path** (not pure greenfield design).
- Mix easy and hard orientation cases.
- Write each task as a one-line prompt the agent would receive (no solution spoilers).
- Record date, who ran it, harness/model if relevant — in *your* private notes, not necessarily in this repo.

**Do not** invent a fake completed study inside the protocol repository.

---

## 2. Conditions

| Condition | Setup |
|-----------|--------|
| **A — no map** | Hide or rename the map file; agent may use normal repo docs (`AGENTS.md` / wiki / grep). |
| **B — map only** | Provide the map; instruct: read local map first; **do not** preload this upstream AAP repo or the full SPEC. |

Run **A then B** (or counterbalance order across tasks). Same task wording both times when possible.

Keep other variables as stable as you can (same harness, similar model, same time box).

---

## 3. Metrics (log per task)

| Metric | What to count |
|--------|----------------|
| **Turns / steps** | Agent tool rounds until first correct locus *or* until time box |
| **Tokens** | If the harness exposes them (optional) |
| **Wrong-home edits** | Files changed outside the intended package before correction |
| **Time to locus** | Wall time (or turn index) until the agent opens/edits the right area |
| **Outcome** | success / partial / fail (your definition, stated once per study) |

Optional: note whether L2 artifacts or optional profiles were used (they are **out of scope** for a pure “map only” B run).

---

## 4. Results table template

Copy into your private notes or a local scratch file. Leave cells empty until you measure.

| Task id | Order (A→B / B→A) | Turns A | Turns B | Tokens A | Tokens B | Wrong-home A | Wrong-home B | Time-to-locus A | Time-to-locus B | Outcome A | Outcome B | Notes |
|---------|-------------------|---------|---------|----------|----------|--------------|--------------|-----------------|-----------------|-----------|-----------|-------|
| T01 | | | | | | | | | | | | |
| T02 | | | | | | | | | | | | |
| … | | | | | | | | | | | | |

**Hypothesis language only** until rows are filled: e.g. “We *hypothesize* B reduces wrong-home edits on multi-package tasks.”

---

## 5. When the map did not help

Always record failures of the map, not only wins:

- Map too sparse → wrong layout key or missing node  
- Map too dense → ignored or still grepped blindly  
- Stale paths → false confidence  
- Task was not orientation-bound (pure algorithm / external docs)  
- Agent skipped L0 instruction  

If **B** does not improve wrong-home rate or time-to-locus on your set: **shrink the map** before adding profiles (same advice as the root README).

---

## 6. What not to publish here

- Business volumes, customer counts, revenue  
- Real service/product names (use fictional labels in any *public* write-up)  
- Effect claims without the table above and a stated method  

Publishing a sanitized summary later is optional and separate from Core.
