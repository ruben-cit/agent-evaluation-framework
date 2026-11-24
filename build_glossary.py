"""Regenerate the Glossary section of index.html from CONTEXT.md."""

import html
import re
from pathlib import Path

START = "<!-- glossary:start -->"
END = "<!-- glossary:end -->"


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def render(context):
    language = context.split("## Language", 1)[1]
    out = ['<section id="glossary"><h2>Glossary</h2>']
    open_list = False
    lines = language.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        group = re.fullmatch(r"### (.+)", line)
        term = re.fullmatch(r"\*\*(.+)\*\*:", line)
        if group:
            if open_list:
                out.append("</dl>")
            out.append(f"<h3>{inline(group[1])}</h3>")
            out.append('<dl class="glossary">')
            open_list = True
        elif term:
            body = []
            i += 1
            while i < len(lines) and lines[i].strip():
                if not lines[i].startswith("_Avoid_:"):
                    body.append(lines[i].strip())
                i += 1
            out.append(
                f"  <div><dt>{inline(term[1])}</dt> "
                f"<dd>{inline(' '.join(body))}</dd></div>"
            )
            continue
        i += 1
    if open_list:
        out.append("</dl>")
    out.append("</section>")
    return "\n".join(out)


def splice(page, fragment):
    if START not in page or END not in page:
        raise ValueError("glossary markers not found")
    before = page.split(START, 1)[0]
    after = page.split(END, 1)[1]
    return f"{before}{START}\n{fragment}\n{END}{after}"


if __name__ == "__main__":
    root = Path(__file__).parent
    page = root / "index.html"
    fragment = render((root / "CONTEXT.md").read_text())
    page.write_text(splice(page.read_text(), fragment))
