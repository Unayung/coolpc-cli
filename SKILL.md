---
name: coolpc
description: Use when the user asks about 原價屋 / coolpc prices, PC part prices in Taiwan, 組電腦 / 估價單 / 預算搭配 / 零件推薦, or wants a build quoted from coolpc.com.tw. Read-only; no login, no ordering.
---

# coolpc — 原價屋 price list from a shell

`~/Projects/coolpc-cli/coolpc`. Stdlib Python, one public page (evaluate.php), cached 30 min.

```
coolpc categories --json
coolpc search <words...> [-c CATEGORY] [-g GROUP] [--min N] [--max N]
              [--sort price|price-desc|page] [--limit N|0] [--bundle] --json
coolpc quote <id> <id> ... --json        # items + total + coins
```

- Words are AND-matched against the name, case-insensitive. `-c` is a substring of the
  category (`SSD`, `CPU`, `主機板`, `記憶體`, `顯示卡`, `電源`, `機殼`, `散熱`, `水冷`, `螢幕`).
  `-g` filters the sub-group inside a category (e.g. `AM5`, `1851`, `DDR5`).
- Results are cheapest first. `price` is what the part costs. `coins` is a 酷幣 rebate,
  **never subtract it**. `was` is the price before a drop (worth mentioning).
- 搭機價 / 任搭 prices are hidden by default because they need a whole build. If the user is
  buying a whole build from coolpc, rerun with `--bundle` and say which prices need it.
- Ids like `n4-31` are only stable for the day. Always quote names, not just ids.
- Exit `4` = coolpc unreachable; `--refresh` forces a new download.

## Helping with a build (from coolpc-skill)

1. Ask what is missing: total budget, main use (文書 / 遊戲 + resolution / 剪輯 / 3D / AI /
   開發), parts to reuse, preferences (ITX/ATX, quiet, RGB, brand).
2. Starting split for a gaming build, adjust to the use:

   | 預算 | CPU | 顯示卡 | 主機板 | 記憶體 | SSD | 電源 | 機殼 | 散熱 |
   |---|---|---|---|---|---|---|---|---|
   | 3 萬 | 20% | 35% | 12% | 10% | 8% | 8% | 5% | 5% |
   | 5 萬 | 18% | 38% | 12% | 8% | 7% | 8% | 5% | 4% |
   | 10 萬 | 20% | 40% | 12% | 8% | 8% | 7% | 3% | 3% |

3. Pick parts with `search`, then **check compatibility before presenting**: CPU socket ↔ board
   (LGA1700 / LGA1851 / AM4 / AM5), DDR4 vs DDR5 ↔ board, PSU watts ≥ CPU + GPU TDP + 20%,
   case ↔ board size (ATX / mATX / ITX), M.2 generation ↔ board slot.
4. `coolpc quote <ids>` for the total, then a table: 零件 / 型號 / 售價, a 合計 row, a few lines
   on why these parts, and one cheaper and one faster alternative.
5. The quote has no shareable link: give the list and https://coolpc.com.tw/evaluate.php, and
   tell them to pick the items there, then 列印估價單 or screenshot it for the store.

【現貨】 in a name means in stock, 【訂】 means ordered in.
