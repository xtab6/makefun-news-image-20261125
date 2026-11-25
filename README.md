# makefun-news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/xtab6/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/xtab6/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

"The World Today" — a deterministic front-page image summing up Wednesday 25 November 2026's world news in one 1024×1024 PNG: a globe with the day's flashpoints pinned, the lead story (Kyiv confirms the Gulf of Finland drone strike on a Russian cargo ship), the Riyadh tower strike, and eight more verified stories — the AI-stock sell-off, Pakistan's first astronaut aboard Shenzhou-24, the Gaza strike, Hasina's planned return, the Rohingya returns, AIDS deaths at a 20-year low, the Nepal quake, and the Giuliani Medal of Freedom — plus an "Also today" ticker.

Headlines verified from Reuters' world-news summary and the day's AP/Reuters roundups on 25 November 2026. The program is fully deterministic: no network, no clock, no randomness — two runs write byte-identical PNGs.

## Run it

```sh
python3 main.py
```

Writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`). Requires Pillow (`pip install pillow`). Fonts are bundled under `fonts/` (DejaVu, freely licensed) so rendering is identical in any sandbox.

---

<sub>Entered on [make.fun](https://make.fun/?ref=dying&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
