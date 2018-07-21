import opengraph
import requests
from bs4 import BeautifulSoup
from little_boxes.urlutils import check_url
from little_boxes.urlutils import is_url_valid


def links_from_note(note):
    tags_href = set()
    for t in note.get("tag", []):
        h = t.get("href")
        if h:
            # TODO(tsileo): fetch the URL for Actor profile, type=mention
            tags_href.add(h)

    links = set()
    soup = BeautifulSoup(note["content"])
    for link in soup.find_all("a"):
        h = link.get("href")
        if h.startswith("http") and h not in tags_href and is_url_valid(h):
            links.add(h)

    return links


def fetch_og_metadata(user_agent, links):
    htmls = []
    for l in links:
        check_url(l)
        r = requests.get(l, headers={"User-Agent": user_agent}, timeout=15)
        r.raise_for_status()
        htmls.append(r.text)
    return [dict(opengraph.OpenGraph(html=html)) for html in htmls]
