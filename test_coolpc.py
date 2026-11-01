#!/usr/bin/env python3
"""Self-check for coolpc. No network: a trimmed copy of evaluate.php's real
structure covers the parsing rules that would silently misprice things.

    python3 test_coolpc.py
"""
import importlib.util
import pathlib
from importlib.machinery import SourceFileLoader

_p = pathlib.Path(__file__).with_name("coolpc")
_spec = importlib.util.spec_from_file_location(
    "coolpc", _p, loader=SourceFileLoader("coolpc", str(_p)))
cp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cp)

PAGE = """
<TD class=t>處理器 CPU</TD><TD>
<SELECT onchange="cnt(4)" name=n4 class=s>
<OPTION value=0 selected class=bf>共有商品 3 樣
<OPTGROUP LABEL='AMD AM5'>
<OPTION value=1>｛AMD R5 8400F盒｝【6核/12緒】4.2G(↑4.7G)65W, $4950 ◆ ★ ↓酷幣200↓
<OPTION disabled style='x' value=2>&#x21AA; 買就送, 贈品一份
<OPTION value=3>｛AMD R5 8400F盒｝【任搭主機板】, $4450 ◆ ★
<OPTGROUP LABEL='Intel 1851'>
<OPTION value=4>｛Intel U5 225, 盒裝｝10核, $43990↘$33990 ◆ ★
</SELECT>
<script>c4=[0,4950,0,4450,33990];d4=[0,200,0,0,0];</script>
"""


def _items():
    return {it["id"]: it for it in cp.parse(PAGE)}


def test_coins_are_not_subtracted_from_the_price():
    # d4 is a 酷幣 rebate. The skill's scraper subtracted it and reported
    # 4750 for a part that costs 4950.
    it = _items()["n4-1"]
    assert it["price"] == 4950 and it["coins"] == 200, it


def test_name_keeps_commas_and_price_drop_is_read():
    # The price is after the LAST ", $"; splitting on the first comma
    # truncated this name to "｛Intel U5 225".
    it = _items()["n4-4"]
    assert it["name"] == "｛Intel U5 225, 盒裝｝10核", it["name"]
    assert it["price"] == 33990 and it["was"] == 43990


def test_disabled_notes_and_header_are_skipped():
    ids = set(_items())
    assert ids == {"n4-1", "n4-3", "n4-4"}, ids


def test_category_and_group_come_through():
    its = _items()
    assert its["n4-1"]["category"] == "處理器 CPU"
    assert its["n4-1"]["group"] == "AMD AM5" and its["n4-4"]["group"] == "Intel 1851"


def test_bundle_prices_hidden_unless_asked():
    items = cp.parse(PAGE)
    assert [i["id"] for i in cp.search(items, ["8400F"])] == ["n4-1"]
    both = cp.search(items, ["8400F"], bundle=True)
    assert [i["id"] for i in both] == ["n4-3", "n4-1"], "price order, cheapest first"


def test_search_needs_every_word_and_respects_filters():
    items = cp.parse(PAGE)
    assert cp.search(items, ["amd", "65w"]) and not cp.search(items, ["amd", "intel"])
    assert [i["id"] for i in cp.search(items, hi=5000)] == ["n4-1"]
    assert [i["id"] for i in cp.search(items, group="intel")] == ["n4-4"]
    assert not cp.search(items, category="顯示卡")


def test_cjk_columns_line_up():
    assert cp._w("顯示卡a") == 7
    assert cp._w(cp._cut("顯示卡顯示卡", 7)) == 7, "truncated cell must keep its width"
    assert cp._cut("ab", 4) == "ab  "


def test_json_flag_works_before_or_after_the_subcommand():
    for argv in (["--json", "categories"], ["categories", "--json"]):
        a = cp.build_parser().parse_args(argv)
        assert getattr(a, "json", False) is True, argv


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok  " + fn.__name__)
    print("\n{} checks passed".format(len(fns)))
