package com.example.newsfeargreed.domain.index;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DailyNewsIndexRepository extends JpaRepository<DailyNewsIndex, Long> {

    List<DailyNewsIndex> findByAssetIdOrderByTargetDateAsc(Long assetId);

    Optional<DailyNewsIndex> findFirstByAssetIdOrderByTargetDateDesc(Long assetId);
}
