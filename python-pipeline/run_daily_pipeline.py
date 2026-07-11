"""매일 뉴스 수집 결과를 CSV 파일로 만드는 독립 실행 파이프라인.

Spring Boot와 직접 통신하지 않는다. 이 파일을 수동 실행하거나 Windows 작업
스케줄러에서 오전 9시에 실행한 뒤, 생성된 CSV를 MySQL 적재기가 읽는다.
"""

from __future__ import annotations

import argparse
import csv
import html
import os
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

BASE_DIR = Path(__file__).resolve().parent
SEOUL = ZoneInfo("Asia/Seoul")
NAVER_NEWS_URL = "https://openapi.naver.com/v1/search/news.json"
TAG_PATTERN = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class Asset:
    code: str
    name: str
    market_type: str
    category: str
    search_keyword: str
    active: bool


@dataclass(frozen=True)
class ArticleResult:
    asset_code: str
    title: str
    press: str
    url: str
    published_at: str
    summary: str
    matched_sentence: str
    positive_count: int
    negative_count: int
    sentiment_score: float
    sentiment_label: str


def clean_text(value: str | None) -> str:
    """네이버 응답의 HTML 강조 태그와 엔티티를 일반 문자열로 바꾼다."""
    if not value:
        return ""
    without_tags = TAG_PATTERN.sub("", value)
    return re.sub(r"\s+", " ", html.unescape(without_tags)).strip()


def load_assets(path: Path) -> list[Asset]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        rows = csv.DictReader(file)
        return [
            Asset(
                code=row["code"],
                name=row["name"],
                market_type=row["market_type"],
                category=row.get("category", ""),
                search_keyword=row["search_keyword"],
                active=row.get("active", "true").lower() == "true",
            )
            for row in rows
        ]


def load_lexicon(path: Path) -> tuple[str, ...]:
    with path.open(encoding="utf-8") as file:
        return tuple(
            line.strip()
            for line in file
            if line.strip() and not line.lstrip().startswith("#")
        )


def build_session():
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    retry = Retry(
        total=3,
        backoff_factor=0.7,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def fetch_naver_news(
    session,
    keyword: str,
    client_id: str,
    client_secret: str,
    pages: int,
    display: int,
) -> list[dict]:
    """공식 네이버 뉴스 검색 API를 최신순으로 여러 페이지 조회한다."""
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    items: list[dict] = []
    for page in range(pages):
        start = page * display + 1
        if start > 1000:
            break
        response = session.get(
            NAVER_NEWS_URL,
            headers=headers,
            params={
                "query": keyword,
                "display": display,
                "start": start,
                "sort": "date",
            },
            timeout=15,
        )
        response.raise_for_status()
        page_items = response.json().get("items", [])
        items.extend(page_items)
        if len(page_items) < display:
            break
    return items


def parse_published_at(value: str) -> datetime:
    parsed = parsedate_to_datetime(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=SEOUL)
    return parsed.astimezone(SEOUL)


def count_terms(text: str, terms: Iterable[str]) -> int:
    return sum(text.count(term) for term in terms)


def score_sentiment(
    text: str,
    positive_terms: Iterable[str],
    negative_terms: Iterable[str],
) -> tuple[int, int, float, str]:
    """legacy의 긍·부정 단어 집계를 재현 가능한 0~1 점수로 바꾼다."""
    positive_count = count_terms(text, positive_terms)
    negative_count = count_terms(text, negative_terms)
    total = positive_count + negative_count
    score = 0.5 if total == 0 else positive_count / total

    if score > 0.55:
        label = "POSITIVE"
    elif score < 0.45:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"
    return positive_count, negative_count, round(score, 6), label


def to_article_result(
    asset: Asset,
    item: dict,
    positive_terms: Iterable[str],
    negative_terms: Iterable[str],
) -> ArticleResult:
    title = clean_text(item.get("title"))
    summary = clean_text(item.get("description"))
    analysis_text = f"{title} {summary}"
    positive_count, negative_count, score, label = score_sentiment(
        analysis_text, positive_terms, negative_terms
    )
    published_at = parse_published_at(item["pubDate"])
    url = item.get("originallink") or item.get("link") or ""
    source_domain = urlparse(url).netloc.removeprefix("www.")
    return ArticleResult(
        asset_code=asset.code,
        title=title,
        press=source_domain,
        url=url,
        published_at=published_at.replace(tzinfo=None).isoformat(timespec="seconds"),
        summary=summary,
        matched_sentence=summary,
        positive_count=positive_count,
        negative_count=negative_count,
        sentiment_score=score,
        sentiment_label=label,
    )


def label_index(score: float) -> str:
    if score < 25:
        return "EXTREME_FEAR"
    if score < 45:
        return "FEAR"
    if score <= 55:
        return "NEUTRAL"
    if score <= 75:
        return "GREED"
    return "EXTREME_GREED"


def build_daily_row(asset: Asset, target_date: date, articles: list[ArticleResult]) -> dict:
    scores = [article.sentiment_score for article in articles]
    average = sum(scores) / len(scores) if scores else 0.5
    fear_greed_score = round(average * 100, 2)
    positive = sum(article.sentiment_label == "POSITIVE" for article in articles)
    negative = sum(article.sentiment_label == "NEGATIVE" for article in articles)
    neutral = len(articles) - positive - negative
    return {
        "asset_code": asset.code,
        "target_date": target_date.isoformat(),
        "article_count": len(articles),
        "positive_article_count": positive,
        "negative_article_count": negative,
        "neutral_article_count": neutral,
        "avg_sentiment_score": round(average, 6),
        "fear_greed_score": fear_greed_score,
        "index_label": label_index(fear_greed_score),
        "buy_signal": "false",
        "sell_signal": "false",
    }


def read_existing_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_rows(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def merge_daily_rows(path: Path, new_rows: list[dict]) -> None:
    keys = {(row["asset_code"], row["target_date"]) for row in new_rows}
    existing = [
        row
        for row in read_existing_rows(path)
        if (row["asset_code"], row["target_date"]) not in keys
    ]
    merged = existing + new_rows
    merged.sort(key=lambda row: (row["asset_code"], row["target_date"]))
    write_rows(path, merged, list(new_rows[0].keys()))


def merge_article_rows(path: Path, new_rows: list[dict]) -> None:
    if not new_rows:
        return
    existing = read_existing_rows(path)
    by_key = {
        (row["asset_code"], row["url"] or row["title"]): row
        for row in existing
    }
    for row in new_rows:
        by_key[(row["asset_code"], row["url"] or row["title"])] = row
    merged = list(by_key.values())
    merged.sort(key=lambda row: (row["asset_code"], row["published_at"]))
    write_rows(path, merged, list(new_rows[0].keys()))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="뉴스공탐지수 일일 CSV 생성")
    parser.add_argument(
        "--date",
        help="분석 날짜(YYYY-MM-DD). 생략하면 완전히 끝난 전날을 분석합니다.",
    )
    parser.add_argument("--asset-code", help="한 종목만 실행할 때 종목 코드")
    parser.add_argument("--pages", type=int, default=10, help="종목별 조회 페이지 수(최대 10 권장)")
    parser.add_argument("--display", type=int, default=100, help="페이지당 기사 수(최대 100)")
    return parser.parse_args()


def main() -> None:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
    args = parse_args()
    target_date = (
        date.fromisoformat(args.date)
        if args.date
        else datetime.now(SEOUL).date() - timedelta(days=1)
    )
    client_id = os.getenv("NAVER_CLIENT_ID", "").strip()
    client_secret = os.getenv("NAVER_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise SystemExit(
            "NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET이 필요합니다. "
            "python-pipeline/.env.example을 참고하세요."
        )

    assets = [asset for asset in load_assets(BASE_DIR / "config" / "assets.csv") if asset.active]
    if args.asset_code:
        assets = [asset for asset in assets if asset.code == args.asset_code]
        if not assets:
            raise SystemExit(f"활성 종목을 찾을 수 없습니다: {args.asset_code}")

    positive_terms = load_lexicon(BASE_DIR / "lexicons" / "positive.txt")
    negative_terms = load_lexicon(BASE_DIR / "lexicons" / "negative.txt")
    session = build_session()
    all_articles: list[ArticleResult] = []
    daily_rows: list[dict] = []

    for asset in assets:
        raw_items = fetch_naver_news(
            session,
            asset.search_keyword,
            client_id,
            client_secret,
            pages=max(1, args.pages),
            display=min(max(1, args.display), 100),
        )
        article_by_url: dict[str, ArticleResult] = {}
        for item in raw_items:
            try:
                published_at = parse_published_at(item["pubDate"])
            except (KeyError, TypeError, ValueError):
                continue
            if published_at.date() != target_date:
                continue
            article = to_article_result(asset, item, positive_terms, negative_terms)
            article_by_url[article.url or article.title] = article

        articles = list(article_by_url.values())
        all_articles.extend(articles)
        daily_rows.append(build_daily_row(asset, target_date, articles))
        print(f"{asset.name}: {target_date} 기사 {len(articles)}건")

    output_dir = BASE_DIR / "output"
    merge_daily_rows(output_dir / "daily_news_index.csv", daily_rows)
    merge_article_rows(
        output_dir / "news_articles.csv",
        [asdict(article) for article in all_articles],
    )
    print(f"CSV 생성 완료: {output_dir}")


if __name__ == "__main__":
    main()
