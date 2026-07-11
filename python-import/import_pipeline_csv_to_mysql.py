"""python-pipeline 결과 CSV를 MySQL에 적재한다."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def as_bool(value: str | bool | None) -> bool:
    return str(value or "false").lower() in {"true", "1", "yes"}


def as_nullable(value: str | None):
    return value if value not in (None, "") else None


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "news_fear_greed"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def upsert_asset(cursor, row: dict) -> None:
    cursor.execute(
        """
        INSERT INTO assets (code, name, market_type, category, search_keyword, active)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            market_type = VALUES(market_type),
            category = VALUES(category),
            search_keyword = VALUES(search_keyword),
            active = VALUES(active)
        """,
        (
            row["code"],
            row["name"],
            row["market_type"],
            as_nullable(row.get("category")),
            row["search_keyword"],
            as_bool(row.get("active", "true")),
        ),
    )


def get_asset_id(cursor, code: str) -> int:
    cursor.execute("SELECT id FROM assets WHERE code = %s", (code,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"assets에 없는 종목 코드입니다: {code}")
    return result["id"]


def upsert_daily_index(cursor, row: dict) -> None:
    asset_id = get_asset_id(cursor, row["asset_code"])
    cursor.execute(
        """
        INSERT INTO daily_news_index
        (asset_id, target_date, article_count, positive_article_count,
         negative_article_count, neutral_article_count, avg_sentiment_score,
         fear_greed_score, index_label, buy_signal, sell_signal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            article_count = VALUES(article_count),
            positive_article_count = VALUES(positive_article_count),
            negative_article_count = VALUES(negative_article_count),
            neutral_article_count = VALUES(neutral_article_count),
            avg_sentiment_score = VALUES(avg_sentiment_score),
            fear_greed_score = VALUES(fear_greed_score),
            index_label = VALUES(index_label),
            buy_signal = VALUES(buy_signal),
            sell_signal = VALUES(sell_signal)
        """,
        (
            asset_id,
            row["target_date"],
            int(row["article_count"]),
            int(row["positive_article_count"]),
            int(row["negative_article_count"]),
            int(row["neutral_article_count"]),
            float(row["avg_sentiment_score"]),
            float(row["fear_greed_score"]),
            row["index_label"],
            as_bool(row.get("buy_signal")),
            as_bool(row.get("sell_signal")),
        ),
    )


def upsert_article(cursor, row: dict) -> None:
    asset_id = get_asset_id(cursor, row["asset_code"])
    url = as_nullable(row.get("url"))
    if url:
        cursor.execute(
            "SELECT id FROM news_articles WHERE asset_id = %s AND url = %s LIMIT 1",
            (asset_id, url),
        )
    else:
        cursor.execute(
            "SELECT id FROM news_articles WHERE asset_id = %s AND title = %s "
            "AND published_at = %s LIMIT 1",
            (asset_id, row["title"], row["published_at"]),
        )
    existing = cursor.fetchone()
    values = (
        row["title"],
        as_nullable(row.get("press")),
        url,
        as_nullable(row.get("published_at")),
        as_nullable(row.get("summary")),
        as_nullable(row.get("matched_sentence")),
        int(row.get("positive_count") or 0),
        int(row.get("negative_count") or 0),
        float(row.get("sentiment_score") or 0.5),
        row.get("sentiment_label") or "NEUTRAL",
    )
    if existing:
        cursor.execute(
            """
            UPDATE news_articles
            SET title=%s, press=%s, url=%s, published_at=%s, summary=%s,
                matched_sentence=%s, positive_count=%s, negative_count=%s,
                sentiment_score=%s, sentiment_label=%s
            WHERE id=%s
            """,
            values + (existing["id"],),
        )
    else:
        cursor.execute(
            """
            INSERT INTO news_articles
            (asset_id, title, press, url, published_at, summary, matched_sentence,
             positive_count, negative_count, sentiment_score, sentiment_label)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (asset_id,) + values,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="파이프라인 CSV를 MySQL에 적재")
    parser.add_argument(
        "--pipeline-dir",
        type=Path,
        default=PROJECT_DIR / "python-pipeline",
        help="python-pipeline 폴더 경로",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv(BASE_DIR / ".env")
    args = parse_args()
    pipeline_dir = args.pipeline_dir.resolve()
    assets = read_csv(pipeline_dir / "config" / "assets.csv")
    daily_rows = read_csv(pipeline_dir / "output" / "daily_news_index.csv")
    article_path = pipeline_dir / "output" / "news_articles.csv"
    article_rows = read_csv(article_path) if article_path.exists() else []

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            for row in assets:
                upsert_asset(cursor, row)
            for row in daily_rows:
                upsert_daily_index(cursor, row)
            for row in article_rows:
                upsert_article(cursor, row)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    print(f"MySQL 적재 완료: 지수 {len(daily_rows)}건, 기사 {len(article_rows)}건")


if __name__ == "__main__":
    main()
