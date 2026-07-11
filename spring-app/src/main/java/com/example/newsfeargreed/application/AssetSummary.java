package com.example.newsfeargreed.application;

import java.math.BigDecimal;
import java.time.LocalDate;

/** 메인 화면에서 종목 한 줄을 표시하기 위한 조회 결과입니다. */
public record AssetSummary(
        Long id,
        String code,
        String name,
        String marketType,
        LocalDate latestDate,
        BigDecimal latestScore,
        String latestLabel
) {
}
