#!/usr/bin/env python3
"""Fetch all post IDs from a public Telegram channel and regenerate telegram.md."""

import re
import sys
import requests
from pathlib import Path

CHANNEL = "china_wholesale_b2b"
BASE_URL = f"https://t.me/s/{CHANNEL}"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TelegramBot/1.0)"}
OUT_FILE = Path(__file__).parent.parent / "telegram.md"


def fetch_all_ids() -> list[int]:
    ids: set[int] = set()
    url = BASE_URL

    while True:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        found = {int(x) for x in re.findall(rf"/{re.escape(CHANNEL)}/(\d+)", resp.text)}
        new = found - ids

        if not new:
            break

        ids |= new
        oldest = min(new)

        if oldest <= 1:
            break

        url = f"{BASE_URL}?before={oldest}"

    return sorted(ids, reverse=True)


def render_post(n: int) -> str:
    return (
        f'<div class="tg-post">\n'
        f'<script async src="https://telegram.org/js/telegram-widget.js?22"'
        f' data-telegram-post="{CHANNEL}/{n}"'
        f' data-width="100%"'
        f' data-userpic="false"'
        f' data-color="229ED9"'
        f' data-dark-color="229ED9"></script>\n'
        f"</div>"
    )


def generate(ids: list[int]) -> str:
    posts_html = "\n\n".join(render_post(n) for n in ids)
    count = len(ids)

    return f"""\
---
title: "China Wholesale B2B — Telegram Channel"
description: "Join our Telegram channel for daily China sourcing tips, supplier insights, and wholesale market updates."
---

<style>
.tg-hero {{
  background: linear-gradient(135deg, #229ED9 0%, #1a7fad 100%);
  border-radius: 12px;
  padding: 2rem 1.5rem;
  color: #fff;
  text-align: center;
  margin-bottom: 2rem;
}}
.tg-hero .tg-icon {{ font-size: 3rem; margin-bottom: 0.75rem; }}
.tg-hero h1 {{
  margin: 0 0 0.5rem;
  font-size: 1.6rem;
  color: #fff;
  border: none;
}}
.tg-hero p {{ margin: 0 0 1.25rem; opacity: 0.92; font-size: 1rem; }}
.tg-join-btn {{
  display: inline-block;
  background: #fff;
  color: #229ED9 !important;
  font-weight: 700;
  padding: 0.65rem 1.75rem;
  border-radius: 99px;
  text-decoration: none !important;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}}
.tg-join-btn:hover {{
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(0,0,0,0.2);
  text-decoration: none !important;
}}
.tg-stats {{
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1.25rem;
  font-size: 0.85rem;
  opacity: 0.85;
}}
.tg-feed-label {{
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 1rem;
  font-weight: 600;
}}
.tg-post {{ margin-bottom: 1rem; }}
.tg-footer-cta {{
  text-align: center;
  padding: 1.5rem;
  border: 1px solid var(--border);
  border-radius: 10px;
  margin-top: 1rem;
}}
.tg-footer-cta p {{ margin: 0 0 1rem; color: var(--muted); }}
</style>

<div class="tg-hero">
  <div class="tg-icon">📢</div>
  <h1>China Wholesale B2B</h1>
  <p>Daily supplier tips, factory insights &amp; wholesale market updates — straight from China.</p>
  <a class="tg-join-btn" href="https://t.me/{CHANNEL}" target="_blank" rel="noopener">
    Join Channel →
  </a>
  <div class="tg-stats">
    <span>📦 Sourcing Tips</span>
    <span>🏭 Factory Insights</span>
    <span>💰 Price Alerts</span>
  </div>
</div>

<div class="tg-feed-label">All Posts ({count} total)</div>

{posts_html}

<div class="tg-footer-cta">
  <p>Want more? All new posts appear on the channel first.</p>
  <a class="tg-join-btn" href="https://t.me/{CHANNEL}" target="_blank" rel="noopener">
    📢 Open in Telegram
  </a>
</div>
"""


def main() -> None:
    print(f"Fetching posts from @{CHANNEL}...")
    ids = fetch_all_ids()

    if not ids:
        print("No posts found — keeping existing file.", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(ids)} posts: {ids[:5]}{'...' if len(ids) > 5 else ''}")
    OUT_FILE.write_text(generate(ids), encoding="utf-8")
    print(f"Written → {OUT_FILE}")


if __name__ == "__main__":
    main()
