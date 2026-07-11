package com.example.newsfeargreed.application;

import com.example.newsfeargreed.domain.article.NewsArticle;
import com.example.newsfeargreed.domain.article.NewsArticleRepository;
import com.example.newsfeargreed.domain.asset.Asset;
import com.example.newsfeargreed.domain.asset.AssetRepository;
import com.example.newsfeargreed.domain.index.DailyNewsIndex;
import com.example.newsfeargreed.domain.index.DailyNewsIndexRepository;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
@Transactional(readOnly = true)
public class AssetQueryService {

    private final AssetRepository assetRepository;
    private final DailyNewsIndexRepository dailyNewsIndexRepository;
    private final NewsArticleRepository newsArticleRepository;

    public AssetQueryService(
            AssetRepository assetRepository,
            DailyNewsIndexRepository dailyNewsIndexRepository,
            NewsArticleRepository newsArticleRepository
    ) {
        this.assetRepository = assetRepository;
        this.dailyNewsIndexRepository = dailyNewsIndexRepository;
        this.newsArticleRepository = newsArticleRepository;
    }

    /** 활성 종목과 각 종목의 가장 최근 지수를 메인 화면용으로 조합합니다. */
    public List<AssetSummary> findAssetSummaries() {
        return assetRepository.findByActiveTrueOrderByNameAsc().stream()
                .map(asset -> dailyNewsIndexRepository
                        .findFirstByAssetIdOrderByTargetDateDesc(asset.getId())
                        .map(index -> toSummary(asset, index))
                        .orElseGet(() -> toEmptySummary(asset)))
                .toList();
    }

    public AssetDetail findAssetDetail(Long assetId) {
        Asset asset = findAsset(assetId);
        List<DailyIndexView> indices = findIndices(assetId);
        List<ArticleView> articles = findArticles(assetId);
        return new AssetDetail(
                asset.getId(),
                asset.getCode(),
                asset.getName(),
                asset.getMarketType(),
                asset.getCategory(),
                indices,
                articles
        );
    }

    public List<DailyIndexView> findIndices(Long assetId) {
        findAsset(assetId);
        return dailyNewsIndexRepository.findByAssetIdOrderByTargetDateAsc(assetId).stream()
                .map(this::toDailyIndexView)
                .toList();
    }

    public List<ArticleView> findArticles(Long assetId) {
        findAsset(assetId);
        return newsArticleRepository.findTop100ByAssetIdOrderByPublishedAtDesc(assetId).stream()
                .map(this::toArticleView)
                .toList();
    }

    private Asset findAsset(Long assetId) {
        return assetRepository.findById(assetId)
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND,
                        "종목을 찾을 수 없습니다: " + assetId
                ));
    }

    private AssetSummary toSummary(Asset asset, DailyNewsIndex index) {
        return new AssetSummary(
                asset.getId(),
                asset.getCode(),
                asset.getName(),
                asset.getMarketType(),
                index.getTargetDate(),
                index.getFearGreedScore(),
                index.getIndexLabel()
        );
    }

    private AssetSummary toEmptySummary(Asset asset) {
        return new AssetSummary(
                asset.getId(),
                asset.getCode(),
                asset.getName(),
                asset.getMarketType(),
                null,
                null,
                "NO_DATA"
        );
    }

    private DailyIndexView toDailyIndexView(DailyNewsIndex index) {
        return new DailyIndexView(
                index.getTargetDate(),
                index.getFearGreedScore(),
                index.getIndexLabel(),
                index.getArticleCount(),
                index.getPositiveArticleCount(),
                index.getNegativeArticleCount(),
                index.getNeutralArticleCount()
        );
    }

    private ArticleView toArticleView(NewsArticle article) {
        return new ArticleView(
                article.getTitle(),
                article.getPress(),
                article.getUrl(),
                article.getPublishedAt(),
                article.getSummary(),
                article.getSentimentScore(),
                article.getSentimentLabel()
        );
    }
}
