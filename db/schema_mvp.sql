CREATE DATABASE IF NOT EXISTS news_fear_greed
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE news_fear_greed;

DROP TABLE IF EXISTS daily_news_index;
DROP TABLE IF EXISTS news_articles;
DROP TABLE IF EXISTS assets;

CREATE TABLE assets (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(30) NOT NULL,
    name VARCHAR(100) NOT NULL,
    market_type VARCHAR(30) NOT NULL,
    category VARCHAR(30),
    search_keyword VARCHAR(100) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_assets_code (code)
);

CREATE TABLE news_articles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    title VARCHAR(500) NOT NULL,
    press VARCHAR(100),
    url VARCHAR(1000),
    published_at DATETIME,
    crawled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    summary TEXT,
    matched_sentence TEXT,
    positive_count INT DEFAULT 0,
    negative_count INT DEFAULT 0,
    sentiment_score DECIMAL(7,6),
    sentiment_label VARCHAR(20),
    CONSTRAINT fk_articles_asset
        FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE INDEX idx_articles_asset_published
ON news_articles(asset_id, published_at);

CREATE TABLE daily_news_index (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    target_date DATE NOT NULL,
    article_count INT NOT NULL DEFAULT 0,
    positive_article_count INT DEFAULT 0,
    negative_article_count INT DEFAULT 0,
    neutral_article_count INT DEFAULT 0,
    avg_sentiment_score DECIMAL(7,6),
    fear_greed_score DECIMAL(5,2),
    index_label VARCHAR(20),
    buy_signal BOOLEAN DEFAULT FALSE,
    sell_signal BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_daily_index_asset
        FOREIGN KEY (asset_id) REFERENCES assets(id),
    UNIQUE KEY uk_daily_index_asset_date (asset_id, target_date)
);

CREATE INDEX idx_daily_index_asset_date
ON daily_news_index(asset_id, target_date);
