# extracting
import langextract as lx
from resume_task import prompt, examples
from key import get_api_key
from ensure_file import ensure_utf8_file
from summarize_to_markdown import generate_markdown_from_jsonl


text = open("meu_arquivo.txt", "r", encoding="utf-8").read()
api_key=get_api_key()
result = lx.extract(
    text_or_documents=text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.0-flash",   # doc recommendation
    api_key=api_key,
    extraction_passes=1,           # better recall in long texts
    max_workers=2,                 # parallel
    max_char_buffer=8000           # small chuncks for better extraction
)

# Save the result to a JSONL file and generate markdown and HTML visualizations
lx.io.save_annotated_documents([result], output_name="resumebuddy.jsonl", output_dir=".") # pyright: ignore[reportArgumentType]
ensure_utf8_file("resumebuddy.jsonl")
md_path = generate_markdown_from_jsonl("resumebuddy.jsonl", "resumebuddy.md")
html = lx.visualize("resumebuddy.jsonl")
with open("resumebuddy_visualization.html", "w", encoding="utf-8") as f:
    f.write(html)
print("OK: resumebuddy.jsonl + resumebuddy_visualization.html are ready.")
