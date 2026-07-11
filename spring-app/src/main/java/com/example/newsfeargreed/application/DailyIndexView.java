package com.example.newsfeargreed.application;

import java.math.BigDecimal;
import java.time.LocalDate;

public record DailyIndexView(
        LocalDate targetDate,
        BigDecimal fearGreedScore,
        String indexLabel,
        Integer articleCount,
        Integer positiveArticleCount,
        Integer negativeArticleCount,
        Integer neutralArticleCount
) {
}
