package com.example.newsfeargreed.domain.article;

import com.example.newsfeargreed.domain.asset.Asset;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import org.hibernate.annotations.CreationTimestamp;

@Entity
@Table(name = "news_articles")
public class NewsArticle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "asset_id", nullable = false)
    private Asset asset;

    @Column(nullable = false, length = 500)
    private String title;

    @Column(length = 100)
    private String press;

    @Column(length = 1000)
    private String url;

    @Column(name = "published_at")
    private LocalDateTime publishedAt;

    @CreationTimestamp
    @Column(name = "crawled_at", updatable = false)
    private LocalDateTime crawledAt;

    @Column(columnDefinition = "TEXT")
    private String summary;

    @Column(name = "matched_sentence", columnDefinition = "TEXT")
    private String matchedSentence;

    @Column(name = "positive_count")
    private Integer positiveCount = 0;

    @Column(name = "negative_count")
    private Integer negativeCount = 0;

    @Column(name = "sentiment_score", precision = 7, scale = 6)
    private BigDecimal sentimentScore;

    @Column(name = "sentiment_label", length = 20)
    private String sentimentLabel;

    protected NewsArticle() {
    }

    public Long getId() {
        return id;
    }

    public Asset getAsset() {
        return asset;
    }

    public String getTitle() {
        return title;
    }

    public String getPress() {
        return press;
    }

    public String getUrl() {
        return url;
    }

    public LocalDateTime getPublishedAt() {
        return publishedAt;
    }

    public LocalDateTime getCrawledAt() {
        return crawledAt;
    }

    public String getSummary() {
        return summary;
    }

    public String getMatchedSentence() {
        return matchedSentence;
    }

    public Integer getPositiveCount() {
        return positiveCount;
    }

    public Integer getNegativeCount() {
        return negativeCount;
    }

    public BigDecimal getSentimentScore() {
        return sentimentScore;
    }

    public String getSentimentLabel() {
        return sentimentLabel;
    }
}
