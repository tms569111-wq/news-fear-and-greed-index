import unittest
from datetime import date

from run_daily_pipeline import Asset, ArticleResult, build_daily_row, clean_text, score_sentiment


class PipelineTest(unittest.TestCase):
    def test_clean_text_removes_naver_highlight_tag(self):
        self.assertEqual("삼성전자 상승", clean_text("<b>삼성전자</b> &amp; 상승").replace(" & ", " "))

    def test_score_sentiment(self):
        result = score_sentiment("실적 개선과 성장, 우려", ("개선", "성장"), ("우려",))
        self.assertEqual((2, 1, 0.666667, "POSITIVE"), result)

    def test_daily_row(self):
        asset = Asset("005930", "삼성전자", "KOSPI", "LARGE_CAP", "삼성전자", True)
        articles = [
            ArticleResult("005930", "a", "", "u1", "2026-07-10T09:00:00", "", "", 2, 0, 1.0, "POSITIVE"),
            ArticleResult("005930", "b", "", "u2", "2026-07-10T10:00:00", "", "", 0, 2, 0.0, "NEGATIVE"),
        ]
        row = build_daily_row(asset, date(2026, 7, 10), articles)
        self.assertEqual(50.0, row["fear_greed_score"])
        self.assertEqual("NEUTRAL", row["index_label"])


if __name__ == "__main__":
    unittest.main()
