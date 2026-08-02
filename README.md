# czech-tabloid-scraper

Reads 18 Czech news, tabloid, and tech RSS feeds and writes about 2,400 headlines to one UTF-8 text file. A full run takes about 14 seconds.

![python](https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![license](https://img.shields.io/badge/license-MIT-A31F34?style=flat-square)
![status](https://img.shields.io/badge/status-active-22863A?style=flat-square)

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

`feedparser` alone does not handle these feeds well. Four points explain the difference.

- **Encoding.** Older Czech feeds still serve `windows-1250` or broken byte sequences. The script detects the encoding per feed with `chardet` and falls back to `errors='replace'`. It never fails on bad bytes.
- **RSS and Atom.** Both `<item>` and `<entry>` structures have explicit handling.
- **Navigation filter.** Regular expressions remove single word menu items, all caps breadcrumbs, and any string shorter than 20 characters. The output holds headlines, not page furniture.
- **CDATA.** The script strips `<![CDATA[...]]>` wrappers.

The script fetches the feeds one after another. Concurrency would add rate limit risk and save little, because a full run already takes about 14 seconds.

## Sources

| Tabloid | Tech | News |
|---|---|---|
| Super.cz, Blesk, Aha, Extra.cz, Showbiz.sk | Živě.cz, Lupa, Cnews, Svět Androida, Technet | Novinky, iDnes, ČT24, iRozhlas, Seznam Zprávy, Lidovky, E15, Forum24, Živé.sk |

The 18 feeds live in the `RSS_FEEDS` dict at the top of `bulvar_scraper.py`. Edit that dict to add or remove a source.

## Limits

- Each run writes a fresh snapshot. The script keeps no state between runs. For an incremental view, pipe the output through `sort | uniq` or add a small SQLite layer.
- The script skips a dead feed without a message and continues.
- No tests.

## License

[MIT](LICENSE)
