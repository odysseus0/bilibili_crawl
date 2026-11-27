# bilibili_crawl

A 2021 crawler for a research study on Bilibili's recommender, built with
[feapder](https://github.com/Boris-code/feapder) (Redis queue, MongoDB store).

- `spiders/account.py`: breadth-first crawl of the account following graph
  from a seed account, storing account info and followings.
- `spiders/video.py`: breadth-first crawl of the related-video graph from a
  seed video, storing video info and related-video payloads.

It is kept as a record and is not maintained. It stored no recommendation
edges (the source video and rank were never recorded), and the 2021 endpoints
and rate limits have since changed. The research question it served was later
answered with public data: Lu, Liu and Zhou, "Recommending the state: How
social media algorithms curate state-created content in China," *Journal of
Communication*, 2026 ([doi:10.1093/joc/jqag010](https://doi.org/10.1093/joc/jqag010)).
