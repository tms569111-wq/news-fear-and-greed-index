package com.example.newsfeargreed.application;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record ArticleView(
        String title,
        String press,
        String url,
        LocalDateTime publishedAt,
        String summary,
        BigDecimal sentimentScore,
        String sentimentLabel
) {
}
