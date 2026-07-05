package com.example.newsfeargreed.domain.article;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NewsArticleRepository extends JpaRepository<NewsArticle, Long> {

    List<NewsArticle> findByAssetIdOrderByPublishedAtDesc(Long assetId);
}
