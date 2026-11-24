# The World in One Day — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/povtalks-ai/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/povtalks-ai/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image summing up the world news of Tuesday 24 November 2026, drawn as a
newspaper front page: COP31 collapses in Antalya with no climate deal, Jensen
Huang returns to Nvidia and shares jump 31%, Russian ships are hit off Libya
and Finland, 24 people die in a candy factory fire in Indonesia, Israeli
strikes hit Gaza, and in sport Alcaraz wins a first ATP Finals title while
the world chess title match opens in Geneva.

Built for the [make.fun "Sum up 24 November's world news in one image"
bounty](https://make.fun/bounty/news-image-20261124), $100 in USDC.

## The image

`entry.png` (1024×1024, drawn with Pillow by `tools/render.py` from the
day's researched headlines) carries the date in its masthead and one short,
labelled panel per story, across climate, markets, war, disaster, the Middle
East and sport. Nothing in it is invented: every headline is a story
reported on 24 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`, so both runs write the same bytes. To redraw the image,
run `python3 tools/render.py` (Pillow, no network, deterministic).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
