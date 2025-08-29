# summarize_to_markdown.py
import json, datetime
from collections import OrderedDict, defaultdict
from typing import Dict, Any, List

PRIO_ORDER = {"high": 0, "alta": 0, "medium": 1, "média": 1, "low": 2, "baixa": 2}

def _iter_docs(jsonl_path: str):
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)

def _clean(s: str) -> str:
    return " ".join((s or "").strip().split())

def _to_date(s: str) -> str:
    if not s:
        return ""
    
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.datetime.strptime(s.strip(), fmt).date().isoformat()
        except Exception:
            pass
    return s.strip()

def generate_markdown_from_jsonl(jsonl_path: str, md_path: str = "resumebuddy.md"):
    section_order: List[str] = []
    sections: Dict[str, Dict[str, Any]] = OrderedDict()  # title -> {"ideas": [], "quotes": []}
    concepts: Dict[str, str] = OrderedDict()
    entities_by_type: Dict[str, List[str]] = defaultdict(list)
    numbers: List[Dict[str, str]] = []
    todos: List[Dict[str, str]] = []

    current_section = "Notas"
    section_order.append(current_section)
    sections[current_section] = {"ideas": [], "quotes": []}

    for doc in _iter_docs(jsonl_path):
        extractions = doc.get("extractions") or doc.get("annotations") or []
        for ex in extractions:
            cls = ex.get("extraction_class") or ex.get("class") or ""
            text = _clean(ex.get("extraction_text") or ex.get("text") or "")
            attrs = ex.get("attributes") or {}

            if not cls or not text:
                continue

            # Sections
            if cls == "section_title":
                current_section = text
                if current_section not in sections:
                    section_order.append(current_section)
                    sections[current_section] = {"ideas": [], "quotes": []}

            # Bullets
            elif cls == "idea":
                sec = _clean(attrs.get("section", "")) or current_section
                if sec not in sections:
                    section_order.append(sec)
                    sections[sec] = {"ideas": [], "quotes": []}
                sections[sec]["ideas"].append({
                    "text": text,
                    "importance": (attrs.get("importance") or "").lower()
                })

            # Concepts
            elif cls == "concept":
                definition = _clean(attrs.get("definition", ""))
                if text not in concepts or (definition and not concepts[text]):
                    concepts[text] = definition

            # Entities
            elif cls == "entity":
                etype = (attrs.get("type") or "Topic").title()
                if text not in entities_by_type[etype]:
                    entities_by_type[etype].append(text)

            # Numbers
            elif cls == "number":
                numbers.append({
                    "metric": _clean(attrs.get("metric") or "valor"),
                    "value": text,
                    "unit": _clean(attrs.get("unit") or ""),
                    "context": _clean(attrs.get("context") or "")
                })

            # todo
            elif cls == "todo":
                todos.append({
                    "text": text,
                    "due": _to_date(attrs.get("due_date")), # pyright: ignore[reportArgumentType]
                    "priority": (attrs.get("priority") or "").lower()
                })

            # Citations
            elif cls == "quote":
                sec = current_section
                if sec not in sections:
                    section_order.append(sec)
                    sections[sec] = {"ideas": [], "quotes": []}
                spk = _clean(attrs.get("speaker") or "")
                quote_line = f"“{text}”" + (f" — {spk}" if spk else "")
                sections[sec]["quotes"].append(quote_line)

    # TL;DR 
    all_ideas = []
    for s in section_order:
        for it in sections[s]["ideas"]:
            all_ideas.append(it)
    def _score(idea):
        imp = idea.get("importance", "")
        return {"high": 0, "medium": 1, "low": 2}.get(imp, 3)
    tldr = [f"- {i['text']}" for i in sorted(all_ideas, key=_score)[:5]]

    def _prio_key(t):
        return (PRIO_ORDER.get(t["priority"], 9), t["due"] or "9999-12-31", t["text"])
    todos_sorted = sorted(todos, key=_prio_key)

    # Render Markdown
    lines = []
    lines.append("# ResumeBuddy — Resumo Estruturado\n")
    if tldr:
        lines.append("## TL;DR (até 5 pontos)")
        lines.extend(tldr)
        lines.append("")

    for s in section_order:
        has_content = sections[s]["ideas"] or sections[s]["quotes"]
        if not has_content:
            continue
        lines.append(f"## {s}")
        for it in sections[s]["ideas"]:
            lines.append(f"- {it['text']}")
        if sections[s]["quotes"]:
            lines.append("\n> **Citações**")
            for q in sections[s]["quotes"]:
                lines.append(f"> {q}")
        lines.append("")

    if concepts:
        lines.append("## Conceitos")
        for term, defi in concepts.items():
            if defi:
                lines.append(f"- **{term}** — {defi}")
            else:
                lines.append(f"- **{term}**")
        lines.append("")

    if entities_by_type:
        lines.append("## Entidades")
        for etype, vals in entities_by_type.items():
            vals_sorted = sorted(set(vals), key=str.lower)
            lines.append(f"- **{etype}**: " + ", ".join(vals_sorted))
        lines.append("")

    if numbers:
        lines.append("## Números / Métricas")
        lines.append("| Métrica | Valor | Unidade | Contexto |")
        lines.append("|---|---|---|---|")
        for n in numbers:
            lines.append(f"| {n['metric']} | {n['value']} | {n['unit']} | {n['context']} |")
        lines.append("")

    if todos_sorted:
        lines.append("## Tarefas (To-Do)")
        for t in todos_sorted:
            pr = t['priority'] or "-"
            due = t['due'] or "-"
            lines.append(f"- [{pr}] {t['text']} — **due:** {due}")
        lines.append("")

    lines.append(f"_Gerado em {datetime.datetime.now().isoformat(timespec='seconds')}_\n")

    with open(md_path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))

    return md_path
