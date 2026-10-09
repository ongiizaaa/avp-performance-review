"""Build AVP Performance Review.

    python3 tools/build.py            -> site/index.html + site/sw.js (Netlify, offline-capable PWA)
    python3 tools/build.py --artifact -> dist/artifact.html (Claude artifact version, libraries from cdnjs)

src/app.html is the single source for the app: markup, styles and script.
src/template-base.xlsx is the cleaned "Performance Review" template the app fills in;
src/template-static.json holds its fixed labels and style ids.
"""
import base64, datetime, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
LIBS = {
    "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js": "lib/xlsx-0.18.5.full.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js": "lib/jszip-3.10.1.min.js",
}

def version():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    return now.strftime("%Y.%m.%d-%H%M")

def app_content(ver):
    s = (SRC / "app.html").read_text(encoding="utf-8")
    b64 = base64.b64encode((SRC / "template-base.xlsx").read_bytes()).decode()
    static = json.dumps(json.loads((SRC / "template-static.json").read_text(encoding="utf-8")), ensure_ascii=False)
    for token in ('"__BASE64__"', "__STATIC__", "__VERSION__"):
        assert token in s, token
    return s.replace('"__BASE64__"', '"' + b64 + '"').replace("__STATIC__", static).replace("__VERSION__", ver)

def build_site(ver):
    s = app_content(ver)
    for cdn, local in LIBS.items():
        assert cdn in s, cdn
        s = s.replace(cdn, local)
    cut = s.index("</style>") + len("</style>")
    head_part, body_part = s[:cut], s[cut:]
    head = (
        '<!doctype html>\n<html lang="th">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#154681">\n<meta name="robots" content="noindex">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" type="image/png" href="icons/favicon-32.png">\n'
        '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n<meta name="apple-mobile-web-app-title" content="Performance Review">\n'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
    )
    sw = ('<script>if ("serviceWorker" in navigator && location.protocol.startsWith("http")) '
          'window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));</script>\n')
    html = head + head_part + "\n</head>\n<body>\n" + body_part.strip() + "\n" + sw + "</body>\n</html>\n"
    (ROOT / "site" / "index.html").write_text(html, encoding="utf-8")
    sw_src = (ROOT / "tools" / "sw.template.js").read_text(encoding="utf-8").replace("__VERSION__", ver)
    (ROOT / "site" / "sw.js").write_text(sw_src, encoding="utf-8")
    print("site/index.html", len(html.encode()), "bytes · version", ver)

def build_artifact(ver):
    out = ROOT / "dist"; out.mkdir(exist_ok=True)
    s = app_content(ver)
    (out / "artifact.html").write_text(s, encoding="utf-8")
    print("dist/artifact.html", len(s.encode()), "bytes · version", ver)

if __name__ == "__main__":
    v = version()
    build_artifact(v) if "--artifact" in sys.argv else build_site(v)
