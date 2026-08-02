# czech-tabloid-scraper

Reads 18 Czech news, tabloid, and tech RSS feeds and writes about 2,400 headlines to one UTF-8 text file. A full run takes about 14 seconds.

![python](https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-A31F34?style=flat-square)
![status](https://img.shields.io/badge/status-active-22863A?style=flat-square)
[![ci](https://github.com/koprjaa/czech-tabloid-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/koprjaa/czech-tabloid-scraper/actions/workflows/ci.yml)

The output is one headline per line, ready for sentiment analysis, topic modeling, or keyword trending.

```text
$ python bulvar_scraper.py
Scraping ct24_cz... ---------------------------- 100% 0:00:14
Scraping finished! Found 2402 titles total.
Saved 2402 titles to:
scraped_output/titles_20260417_151734.txt
```

## Install

```bash
uv venv
uv pip install -r requirements.txt
```

## Use

```bash
python bulvar_scraper.py
```

The file lands in `scraped_output/titles_<timestamp>.txt`.

## How it works

`feedparser` alone does not handle these feeds well. Five points explain the difference.

- **Encoding.** Older Czech feeds still serve `windows-1250` or broken byte sequences. The script detects the encoding per feed with `chardet` and falls back to `errors='replace'`. It never fails on bad bytes.
- **RSS and Atom.** RSS puts headlines in `<item>`, Atom in `<entry>`. Atom also namespaces its tags, so the script matches on the local tag name. A plain `.//entry` lookup finds nothing in a real Atom feed.
- **Navigation filter.** One regular expression removes breadcrumbs, which are a capitalized word followed by lowercase words only. A second removes all caps menu labels, and anything shorter than 20 characters goes too. The pattern is ASCII, so a Czech headline with a diacritic never looks like a breadcrumb. That is what keeps real headlines in the output.
- **CDATA.** The script strips `<![CDATA[...]]>` wrappers.
- **Untrusted XML.** The feeds belong to other people, so `defusedxml` parses them. An entity expansion payload is refused and that feed is skipped.

The script fetches the feeds one after another. Concurrency would add rate limit risk and save little, because a full run already takes about 14 seconds.

## Sources

| Tabloid | Tech | News |
|---|---|---|
| Super.cz, Blesk, Aha, Extra.cz, Showbiz.sk | Živě.cz, Lupa, Cnews, Svět Androida, Technet | Novinky, iDnes, ČT24, iRozhlas, Seznam Zprávy, Lidovky, E15, Forum24, Živé.sk |

The 18 feeds live in the `FEEDS` dict at the top of `bulvar_scraper.py`. Edit that dict to add or remove a source.

## Limits

- Each run writes a fresh snapshot and deletes the file from the previous run. The script keeps no state between runs. For an incremental view, pipe the output through `sort | uniq` or add a small SQLite layer.
- A dead feed prints one line and the run continues with the rest.
- The navigation filter drops any headline written without diacritics, because it cannot tell one from a breadcrumb.

## Development

```bash
uv run --extra dev ruff check .
uv run --extra dev pytest -q
```

CI runs both on Python 3.10, 3.11, and 3.12, on Linux and Windows.

## License

[MIT](LICENSE)
