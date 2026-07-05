package com.example.newsfeargreed.domain.index;

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
import jakarta.persistence.UniqueConstraint;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import org.hibernate.annotations.CreationTimestamp;

@Entity
@Table(
        name = "daily_news_index",
        uniqueConstraints = @UniqueConstraint(
                name = "uk_daily_index_asset_date",
                columnNames = {"asset_id", "target_date"}
        )
)
public class DailyNewsIndex {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "asset_id", nullable = false)
    private Asset asset;

    @Column(name = "target_date", nullable = false)
    private LocalDate targetDate;

    @Column(name = "article_count", nullable = false)
    private Integer articleCount = 0;

    @Column(name = "positive_article_count")
    private Integer positiveArticleCount = 0;

    @Column(name = "negative_article_count")
    private Integer negativeArticleCount = 0;

    @Column(name = "neutral_article_count")
    private Integer neutralArticleCount = 0;

    @Column(name = "avg_sentiment_score", precision = 7, scale = 6)
    private BigDecimal avgSentimentScore;

    @Column(name = "fear_greed_score", precision = 5, scale = 2)
    private BigDecimal fearGreedScore;

    @Column(name = "index_label", length = 20)
    private String indexLabel;

    @Column(name = "buy_signal", nullable = false)
    private Boolean buySignal = false;

    @Column(name = "sell_signal", nullable = false)
    private Boolean sellSignal = false;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    protected DailyNewsIndex() {
    }

    public Long getId() {
        return id;
    }

    public Asset getAsset() {
        return asset;
    }

    public LocalDate getTargetDate() {
        return targetDate;
    }

    public Integer getArticleCount() {
        return articleCount;
    }

    public Integer getPositiveArticleCount() {
        return positiveArticleCount;
    }

    public Integer getNegativeArticleCount() {
        return negativeArticleCount;
    }

    public Integer getNeutralArticleCount() {
        return neutralArticleCount;
    }

    public BigDecimal getAvgSentimentScore() {
        return avgSentimentScore;
    }

    public BigDecimal getFearGreedScore() {
        return fearGreedScore;
    }

    public String getIndexLabel() {
        return indexLabel;
    }

    public Boolean getBuySignal() {
        return buySignal;
    }

    public Boolean getSellSignal() {
        return sellSignal;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}
