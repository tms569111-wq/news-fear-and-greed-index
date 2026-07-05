INSERT INTO assets (id, code, name, market_type, category, search_keyword, active)
VALUES
(1, '005930', '삼성전자', 'KOSPI', 'LARGE_CAP', '삼성전자', TRUE),
(2, 'BTC', '비트코인', 'CRYPTO', 'CRYPTO', '비트코인', TRUE),
(3, 'KOSPI', '코스피', 'INDEX', 'INDEX', '코스피', TRUE);

INSERT INTO daily_news_index
(asset_id, target_date, article_count, positive_article_count, negative_article_count, neutral_article_count,
 avg_sentiment_score, fear_greed_score, index_label, buy_signal, sell_signal)
VALUES
(1, '2023-12-01', 100, 63, 25, 12, 0.632000, 63.20, 'GREED', FALSE, FALSE),
(1, '2023-12-02', 100, 48, 39, 13, 0.512000, 51.20, 'NEUTRAL', FALSE, FALSE),
(2, '2023-12-01', 100, 42, 47, 11, 0.421000, 42.10, 'FEAR', TRUE, FALSE),
(3, '2023-12-01', 100, 55, 33, 12, 0.552000, 55.20, 'GREED', FALSE, FALSE);

INSERT INTO news_articles
(asset_id, title, press, url, published_at, summary, matched_sentence,
 positive_count, negative_count, sentiment_score, sentiment_label)
VALUES
(1, '삼성전자 반도체 업황 회복 기대', '샘플경제', 'https://example.com/samsung-1',
 '2023-12-01 09:00:00', '반도체 업황 회복 기대가 커지고 있다는 내용의 샘플 기사입니다.',
 '삼성전자는 반도체 업황 회복 기대에 따라 투자 심리가 개선되고 있다.',
 7, 2, 0.720000, 'POSITIVE'),
(2, '비트코인 변동성 확대', '샘플코인', 'https://example.com/btc-1',
 '2023-12-01 11:00:00', '비트코인 가격 변동성을 다루는 샘플 기사입니다.',
 '비트코인은 높은 변동성으로 투자자들의 경계감이 커지고 있다.',
 3, 6, 0.410000, 'NEGATIVE');
