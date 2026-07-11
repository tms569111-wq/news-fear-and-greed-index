package com.example.newsfeargreed.web.api;

import com.example.newsfeargreed.application.ArticleView;
import com.example.newsfeargreed.application.AssetQueryService;
import com.example.newsfeargreed.application.AssetSummary;
import com.example.newsfeargreed.application.DailyIndexView;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/assets")
public class AssetApiController {

    private final AssetQueryService assetQueryService;

    public AssetApiController(AssetQueryService assetQueryService) {
        this.assetQueryService = assetQueryService;
    }

    @GetMapping
    public List<AssetSummary> assets() {
        return assetQueryService.findAssetSummaries();
    }

    @GetMapping("/{id}/index")
    public List<DailyIndexView> indices(@PathVariable("id") Long id) {
        return assetQueryService.findIndices(id);
    }

    @GetMapping("/{id}/articles")
    public List<ArticleView> articles(@PathVariable("id") Long id) {
        return assetQueryService.findArticles(id);
    }
}
