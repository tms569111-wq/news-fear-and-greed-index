package com.example.newsfeargreed.web.view;

import com.example.newsfeargreed.application.AssetQueryService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
public class AssetViewController {

    private final AssetQueryService assetQueryService;

    public AssetViewController(AssetQueryService assetQueryService) {
        this.assetQueryService = assetQueryService;
    }

    @GetMapping({"/", "/assets"})
    public String assets(Model model) {
        model.addAttribute("assets", assetQueryService.findAssetSummaries());
        return "assets";
    }

    @GetMapping("/assets/{id}")
    public String assetDetail(@PathVariable("id") Long id, Model model) {
        model.addAttribute("asset", assetQueryService.findAssetDetail(id));
        return "asset-detail";
    }
}
