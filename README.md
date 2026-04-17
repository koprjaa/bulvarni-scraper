# bulvarni-scraper

**18 Czech news and tech RSS feeds, 2,400+ headlines, one UTF-8 text file — in about 14 seconds.**

![python](https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-A31F34?style=flat-square)
![status](https://img.shields.io/badge/status-active-22863A?style=flat-square)
![requests](https://img.shields.io/badge/requests-2.32-000?style=flat-square)
![chardet](https://img.shields.io/badge/chardet-5.x-555?style=flat-square)
![rich](https://img.shields.io/badge/rich-13.x-F0E68C?style=flat-square)

A tiny, opinionated CLI that pulls headlines from every major Czech tabloid, news portal, and tech site, strips the navigation junk, and dumps one clean headline per line — ready for sentiment analysis, topic modelling, keyword trending, or just your own personal morning news firehose.

```text
$ python bulvar_scraper.py
Scraping ct24_cz... ---------------------------- 100% 0:00:14
Scraping finished! Found 2402 titles total.
Saved 2402 titles to:
scraped_output/titles_20260417_151734.txt
```

## Why this and not just `feedparser`

- **Encoding tolerance** — Older Czech feeds still serve `windows-1250` or broken byte sequences. `chardet` is used per feed, with `errors='replace'` fallback. The script never crashes on bad bytes.
- **Dual RSS + Atom** — Both `<item>` and `<entry>` structures handled explicitly, no magic.
- **Navigation scrubbing** — Regex filters strip single-word menu items, all-caps nav breadcrumbs, anything shorter than 20 characters. You get headlines, not website furniture.
- **CDATA aware** — `<![CDATA[...]]>` wrappers are stripped.
- **Sequential by design** — Intentionally not concurrent. Avoids rate limits, and the end-to-end is fast enough (~14s) that async buys nothing here.

## Install and run

```bash
uv venv
uv pip install -r requirements.txt
python bulvar_scraper.py
```

## Output

```
scraped_output/
└── titles_20260417_151734.txt     # one headline per line, UTF-8
```

## Sources

| Tabloid | Tech / IT | Mainstream news |
|---------|-----------|-----------------|
| Super.cz, Blesk, Aha, Extra.cz, Showbiz.sk | Živě.cz, Lupa, Cnews, Svět Androida, Technet | Novinky, iDnes, ČT24, iRozhlas, Seznam Zprávy, Lidovky, E15, Forum24, Živé.sk |

18 feeds total, hardcoded in `bulvar_scraper.py`. Add or remove by editing the `RSS_FEEDS` dict at the top.

## Known limits

- No persistence across runs — each invocation is a fresh snapshot. For incremental/diff use, pipe into `sort | uniq` across runs or wrap with a small SQLite layer.
- Dead feeds are skipped silently; the script keeps going.

## License

[MIT](LICENSE)
