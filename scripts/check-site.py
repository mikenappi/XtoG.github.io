"""Check the built reading paths, local resources and fragment destinations."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path("dist")
BASE = "/XtoG.github.io/"
ORIGIN = "https://mikenappi.github.io"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        for key in ("href", "src"):
            if values.get(key):
                self.links.append(values[key])


pages = {path: Page(path) for path in ROOT.rglob("*.html")}
if len(pages) < 10 or ROOT / "pagefind/pagefind.js" not in set(ROOT.rglob("pagefind.js")):
    raise SystemExit("Expected all reading pages and the Pagefind search index")

failures = []
for path, page in pages.items():
    url = ORIGIN + BASE + path.relative_to(ROOT).as_posix()
    for link in page.links:
        target = urlsplit(urljoin(url, link))
        if target.netloc != "mikenappi.github.io" or target.scheme != "https":
            continue
        if not target.path.startswith(BASE):
            failures.append(f"{path}: outside project path: {link}")
            continue
        dest = ROOT / unquote(target.path[len(BASE):])
        if dest.is_dir():
            dest = dest / "index.html"
        if not dest.exists():
            failures.append(f"{path}: missing destination: {link}")
        elif target.fragment and dest in pages and unquote(target.fragment) not in pages[dest].ids:
            failures.append(f"{path}: missing anchor: {link}")

if failures:
    raise SystemExit("\n".join(failures))
print(f"Verified internal links, anchors and resources across {len(pages)} HTML pages")
