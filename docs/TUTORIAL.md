# Tutorial: Write Your First REIXS Spec

You're about to write a complete `.reixs.md` file from scratch. By the end of this tutorial, you'll have a validated, compilable spec for a **property valuation summary** task — and you'll understand every section well enough to write specs for your own tasks.

We're deliberately using a different domain than the built-in lease abstraction template. If we used the same domain, you'd be tempted to copy and tweak. Writing a spec for a new domain forces you to think through each section yourself, which is how you actually learn the format.

**What you'll build:** A REIXS spec that tells an AI agent how to extract key valuation metrics from a residential appraisal report (British Columbia jurisdiction) and produce a structured summary with source page references.

## Prerequisites

You need Python 3.10+ and git. That's it.

```bash
git clone https://github.com/reggiechan74/reixs.git
cd reixs
pip install -e ".[dev]"
reixs --version
```

You should see a version number (e.g., `0.1.0`). If `reixs --version` fails, check that the `pip install` completed without errors and that the `reixs` entry point is on your `PATH`.

Now create a working file:

```bash
touch my_spec.reixs.md
```

We'll build this file section by section. After each step, you'll run `reixs validate my_spec.reixs.md` to see what the validator thinks. Expect errors early on — that's the point. The validator gives you actionable feedback, and watching the error count drop as you add sections is the fastest way to internalize the format.

## Step 1: Create the File — Meta Section

Open `my_spec.reixs.md` in your editor and add:

```markdown
# REIXS: Property Valuation Summary — British Columbia

## Meta

- Spec ID: REIXS-PV-BC-001
- Version: 0.1.0
- Task Type: Property Valuation
- Tier: micro
- Author: Your Name
- Date: 2026-03-01
```

Let's unpack what each field does:

- **Spec ID** — A unique identifier for this spec. The convention is `REIXS-TYPE-JURISDICTION-SEQ` (so `PV` for Property Valuation, `BC` for British Columbia, `001` for the first version), but any non-empty string works.
- **Version** — Semantic versioning (`X.Y.Z`). We're starting at `0.1.0` because this is a draft.
- **Task Type** — What kind of real estate task this is. `Property Valuation` isn't in the built-in registry (only `Lease Abstraction` is, as of v0.1.0), so you'll see a warning — that's expected and harmless.
- **Tier** — One of `micro`, `standard`, or `complex`. We're using `micro` because this is a simple, self-contained task. The tier controls how strict the OFD section validation is: `micro` only requires 5 mandatory OFD sub-sections, while `standard` and `complex` require all 10. Start small.
- **Author** — Your name. No validation beyond "not empty."
- **Date** — ISO 8601 format (`YYYY-MM-DD`).

Now run the validator:

```bash
reixs validate my_spec.reixs.md
```

You'll see errors about missing sections — something like "missing required section: objective", "missing required section: domain_context", and so on for all 9 sections we haven't written yet. That's exactly right. A REIXS spec has 10 mandatory sections, and we've only written one. The validator is telling you what to do next.

## Step 2: Objective

Add this after the Meta section:

```markdown
## Objective

Extract key valuation metrics from a residential appraisal report (BC jurisdiction)
and produce a structured summary with source page references.
```

The Objective section is the simplest one in the spec. It's a free-text paragraph — no bullet lists, no key-value pairs, no special syntax. The only rule is that it can't be empty. Write one or two sentences that describe what the task accomplishes.

Think of it as the "elevator pitch" for the spec. If someone reads only this section, they should understand the task at a high level.

Run `reixs validate my_spec.reixs.md` again. You should see one fewer error now — the "missing required section: objective" message is gone.

## Step 3: Domain Context

Add this next:

```markdown
## Domain Context

- Jurisdiction: British Columbia, Canada
- Currency: CAD
- DDD Reference: re-ddd:property_valuation_bc@0.1.0
```

This section uses the `Key: Value` bullet syntax that you already saw in Meta. Three things to note:

- **Jurisdiction** is required. It's free text — the validator accepts any non-empty string, though it knows about some jurisdictions (like `Ontario, Canada`) for cross-field checks. `British Columbia, Canada` isn't in the known registry, but that's fine. The registry is advisory, not restrictive.

- **Currency** is optional but good practice. If you were writing a spec for Ontario and omitted the currency, the validator would emit a cross-field warning reminding you. For BC, no such warning exists, but declaring the currency explicitly is clearer.

- **DDD Reference** is required and must follow the format `re-ddd:<name>@X.Y.Z`. That regex is enforced — if you write something like `property_valuation_bc` without the `re-ddd:` prefix and version suffix, the validator will reject it. Our reference `re-ddd:property_valuation_bc@0.1.0` has valid format, but it's not in the built-in registry (which only knows about `re-ddd:lease_core_terms_ontario@0.1.0`). You'll get a warning about that — a warning, not an error. The validator is saying "I don't recognize this DDD reference, make sure it's correct" rather than "this is invalid."

Run the validator again. The missing-section errors for `domain_context` should be gone, possibly replaced by a warning about the unrecognized DDD reference.

## Step 4: Inputs

Add this:

```markdown
## Inputs

- Source document: PDF appraisal report
- Document type: Residential property appraisal (Form 1004 or equivalent)
- Expected length: 10-50 pages
```

The Inputs section is the most free-form section in a REIXS spec. There are no required fields — the content is entirely domain-specific. You define whatever inputs are relevant for your task, and the validator won't complain about missing fields.

Each bullet follows the same `Key: Value` syntax. The parser normalizes the key to `snake_case` (so `Source document` becomes `source_document`) and stores the value as a string. If you write a bullet without a colon (like `- The original scanned PDF`), it gets stored as a plain list item instead of a key-value pair. Both forms are valid.

This section tells downstream agents what they'll receive at runtime. Be specific enough that an agent knows what format to expect, but don't over-specify — details about how to process the input belong in the OFD and Behavior Spec sections.

Run `reixs validate my_spec.reixs.md` once more. You've now written 4 of 10 sections. The validator should report 6 missing sections remaining.

---

**Next up:** The OFD section — the heart of the spec — followed by Constraints, Output Contract, Evaluation, Behavior Spec, and Validation Checklist. That's covered in the next part of this tutorial.
