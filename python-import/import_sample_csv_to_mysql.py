"""
샘플 CSV를 MySQL에 넣는 starter script입니다.
실제 기존 UGRP Excel 구조에 맞게 컬럼명은 나중에 수정하세요.
"""

import os
import pandas as pd
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "news_fear_greed"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def upsert_asset(cursor, row):
    sql = """
    INSERT INTO assets (code, name, market_type, category, search_keyword, active)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        market_type = VALUES(market_type),
        category = VALUES(category),
        search_keyword = VALUES(search_keyword),
        active = VALUES(active)
    """
    cursor.execute(sql, (
        row["code"], row["name"], row["market_type"], row["category"],
        row["search_keyword"], str(row.get("active", "true")).lower() == "true"
    ))


def get_asset_id(cursor, asset_code):
    cursor.execute("SELECT id FROM assets WHERE code = %s", (asset_code,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"asset code not found: {asset_code}")
    return result["id"]


def insert_daily_index(cursor, row):
    asset_id = get_asset_id(cursor, row["asset_code"])
    sql = """
    INSERT INTO daily_news_index
    (asset_id, target_date, article_count, positive_article_count, negative_article_count,
     neutral_article_count, avg_sentiment_score, fear_greed_score, index_label, buy_signal, sell_signal)
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
    """
    cursor.execute(sql, (
        asset_id,
        row["target_date"],
        int(row["article_count"]),
        int(row["positive_article_count"]),
        int(row["negative_article_count"]),
        int(row["neutral_article_count"]),
        float(row["avg_sentiment_score"]),
        float(row["fear_greed_score"]),
        row["index_label"],
        str(row.get("buy_signal", "false")).lower() == "true",
        str(row.get("sell_signal", "false")).lower() == "true",
    ))


def main():
    assets = pd.read_csv("../data/sample/sample_assets.csv")
    daily = pd.read_csv("../data/sample/sample_daily_news_index.csv")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for _, row in assets.iterrows():
                upsert_asset(cursor, row)
            for _, row in daily.iterrows():
                insert_daily_index(cursor, row)
        conn.commit()
        print("Sample CSV import completed.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
