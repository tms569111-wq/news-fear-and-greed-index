-- 2차 고도화용 테이블입니다.
-- 1차 MVP에서는 사용하지 않아도 됩니다.

USE news_fear_greed;

CREATE TABLE daily_prices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    price_date DATE NOT NULL,
    open_price DECIMAL(18,4),
    high_price DECIMAL(18,4),
    low_price DECIMAL(18,4),
    close_price DECIMAL(18,4),
    volume BIGINT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_prices_asset
        FOREIGN KEY (asset_id) REFERENCES assets(id),
    UNIQUE KEY uk_prices_asset_date (asset_id, price_date)
);

CREATE TABLE technical_indicators (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    target_date DATE NOT NULL,
    rsi DECIMAL(7,4),
    macd DECIMAL(12,6),
    macd_signal DECIMAL(12,6),
    macd_histogram DECIMAL(12,6),
    technical_signal VARCHAR(20),
    expected_action VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_indicators_asset
        FOREIGN KEY (asset_id) REFERENCES assets(id),
    UNIQUE KEY uk_indicators_asset_date (asset_id, target_date)
);

CREATE TABLE analysis_runs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    run_type VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finished_at DATETIME,
    target_asset_id BIGINT,
    target_start_date DATE,
    target_end_date DATE,
    processed_article_count INT DEFAULT 0,
    error_message TEXT,
    CONSTRAINT fk_runs_asset
        FOREIGN KEY (target_asset_id) REFERENCES assets(id)
);
