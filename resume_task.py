#Prompt + example for LLM 
import langextract as lx
import textwrap

# ======================================================================
# 1) Prompt
# ======================================================================
prompt = textwrap.dedent("""\
You are extracting a structured scaffold for study/summary,
articles or books. Perform ONLY EXTRACTIVE annotation (use exact spans).

CLASSES to extract (use these exact class names):
- section_title: a heading or phrase that functions like a section/subject.
  attributes: {"level": "h1|h2|h3", "hint": "<short label>"}
- idea: a key idea/sentence worth summarizing later.
  attributes: {"importance": "high|medium|low", "section": "<nearest section_title>"}
- concept: a term/phrase being defined or explained.
  attributes: {"definition": "<short definition from text if present>"}
- entity: a proper noun or date/topic tag.
  attributes: {"type": "Person|Org|Place|Date|Topic|Doc"}
- number: a numeric fact.
  attributes: {"metric": "<what is measured>", "unit": "<unit>", "context": "<short context>"}
- quote: a notable quote.
  attributes: {"speaker": "<who said>", "purpose": "<why relevant>"}
- todo: an actionable instruction in notes.
  attributes: {"priority": "high|medium|low", "due_date": "<if any>"}

RULES:
- Use exact text for extraction_text; DO NOT paraphrase; avoid overlapping spans.
- Prefer concise spans that best represent the item.
- Attach meaningful attributes; leave missing ones out.
- If page/timecodes exist in the text, keep them inside attributes as seen.
""")

# =============================================================================
# 2) Few-shot examples
# =============================================================================

examples = [
    lx.data.ExampleData(
        text=(
            "=== Cloud Security – Key Notes ===\n"
            "Rotate keys every 90 days (per NIST SP 800-57). "
            "Action: Migrate secrets to Vault by 10/30. "
            "Zero trust reduces lateral movement.\n"
            "Tip: enable MFA for admins."
        ),
        extractions=[
            # SECTION
            lx.data.Extraction(
                extraction_class="section_title",
                extraction_text="Cloud Security – Key Notes",
                attributes={"level": "h1", "hint": "security"}
            ),
            # IDEA
            lx.data.Extraction(
                extraction_class="idea",
                extraction_text="Zero trust reduces lateral movement",
                attributes={"importance": "high", "section": "Cloud Security – Key Notes"}
            ),
            # CONCEPT
            lx.data.Extraction(
                extraction_class="concept",
                extraction_text="Rotate keys",
                attributes={"definition": "change cryptographic keys on a schedule"}
            ),
            # ENTITY (document reference)
            lx.data.Extraction(
                extraction_class="entity",
                extraction_text="NIST SP 800-57",
                attributes={"type": "Doc"}
            ),
            # NUMBER
            lx.data.Extraction(
                extraction_class="number",
                extraction_text="90 days",
                attributes={"metric": "key rotation period", "unit": "days", "context": "policy cadence"}
            ),
            #
            lx.data.Extraction(
                extraction_class="todo",
                extraction_text="Migrate secrets to Vault",
                attributes={"priority": "high", "due_date": "10/30"}
            ),
            # QUOTE
            lx.data.Extraction(
                extraction_class="quote",
                extraction_text="enable MFA for admins",
                attributes={"speaker": "Tip", "purpose": "hardening"}
            ),
        ],
    ),

    lx.data.ExampleData(
        text=(
            "Chapter: Data Ethics\n"
            "Principle: transparency builds trust. GDPR requires explicit consent. "
            "Next: draft consent banner before 2025-09-01."
        ),
        extractions=[
            lx.data.Extraction(
                extraction_class="section_title",
                extraction_text="Data Ethics",
                attributes={"level": "h1", "hint": "ethics"}
            ),
            lx.data.Extraction(
                extraction_class="idea",
                extraction_text="transparency builds trust",
                attributes={"importance": "medium", "section": "Data Ethics"}
            ),
            lx.data.Extraction(
                extraction_class="entity",
                extraction_text="GDPR",
                attributes={"type": "Doc"}
            ),
            lx.data.Extraction(
                extraction_class="todo",
                extraction_text="draft consent banner",
                attributes={"priority": "medium", "due_date": "2025-09-01"}
            ),
        ],
    ),
]
