from pathlib import Path

def ensure_utf8_file(path: str):
    p = Path(path)
    raw = p.read_bytes()
    try:
        raw.decode("utf-8")
        return
    except UnicodeDecodeError:
        pass
    text = raw.decode("cp1252", errors="strict")
    p.write_text(text, encoding="utf-8", newline="\n")
