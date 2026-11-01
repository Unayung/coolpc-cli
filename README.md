# coolpc-cli

原價屋 ([coolpc.com.tw](https://coolpc.com.tw/evaluate.php)) price list from the shell.
Read-only, no login, zero dependencies (Python 3.8+ stdlib, one file).

It reads the public 估價單 page, which lists every product coolpc sells with today's
price, and lets you search it, list a category, or total up a quote.

```
coolpc categories                              # 30 categories and item counts
coolpc search 2TB Gen4 -c SSD                  # every word must match the name
coolpc search -c CPU --max 8000 --limit 0      # a whole category under a price
coolpc search 4090 -c 顯示卡 --sort price-desc
coolpc search 8400F --bundle                   # also show 搭機價 / 任搭 prices
coolpc quote n4-31 n7-118 n12-40               # items + 合計 + 酷幣
```

`--json` gives `{"ok":true,"data":…}` or `{"ok":false,"error":{"message","code"}}`, before or
after the subcommand. Exit codes: `0` ok, `1` error, `2` usage, `4` network.

```console
$ coolpc search 2TB Gen4 -c SSD --limit 3
20 items (showing 3)
n7-118               7,999          ｛致態 ZhiTai Ti600 2TB｝/Gen4/PCIe 4.0/讀7000/寫6000/QLC【五年保】~…
n7-130     12,490↘   7,999          MSI 微星｛M480PRO 2TB｝/Gen4/讀7400/寫7000/3D TLC顆粒/DRAM快取【五年…
n7-145               8,190          美光 Micron｛E100 2TB｝/Gen4 PCIe 4.0/讀5000/寫4500/QLC【五年保】
```

Each item: `id`, `category`, `group` (the sub-heading inside a category, e.g. `AMD AM5`),
`name`, `price`, `was` (price before a drop, else null), `coins`, `bundle`, `tags`.

## Things that are not what they look like (verified 2026-11-01)

- **`coins` is not a discount.** `$4950 ◆ ★ ↓酷幣200↓` costs 4,950 and gives back 200 酷幣
  for a later order. The page keeps it in a JS array `dN` next to the price array `cN`, which
  makes it look like a discount; subtracting it understates the price.
- **A price drop is written `$43990↘$33990`.** `price` is the second number (it matches `cN`),
  `was` the first.
- **搭機價 and 【任搭主機板】 prices only apply to a whole build** (or with a board), so `search`
  hides them unless `--bundle`. The same part is usually also listed at its standalone price.
- **The page is Big5 with HKSCS-ish extras.** Strict `big5` mangles ~80 characters; `cp950`
  decodes it cleanly.
- **Names contain commas.** The price is after the *last* `, $`.
- **Ids (`n4-31`) are positions on today's page** (category box 4, option 31). coolpc edits the
  page during the day, so an id can later point at something else; `quote` prints each name
  back so a shift is visible.
- **The quote has no shareable URL.** evaluate.php keeps the selection in the page only, so
  `quote` gives the list and total and the link to pick them by hand.

The page is cached for 30 minutes in `~/.cache/coolpc/catalog.json` (`XDG_CACHE_HOME` moves
it); `--refresh` re-downloads. One fetch is ~1 MB, so be gentle.

## Not included

The interactive picker and the Playwright form-filler from
[coolpc-skill](https://github.com/PttCodingMan/coolpc-skill), which this CLI is based on. They
need a terminal prompt and a browser; `search` + `quote` cover the same ground for an agent.

## Files

- `coolpc` — the CLI.
- `SKILL.md` — the agent-facing brief, including the build-advice flow from coolpc-skill.
- `test_coolpc.py` — offline self-check: `python3 test_coolpc.py`.
