package com.example.newsfeargreed.application;

import java.util.List;

public record AssetDetail(
        Long id,
        String code,
        String name,
        String marketType,
        String category,
        List<DailyIndexView> indices,
        List<ArticleView> articles
) {
}
