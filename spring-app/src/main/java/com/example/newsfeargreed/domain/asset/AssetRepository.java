package com.example.newsfeargreed.domain.asset;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AssetRepository extends JpaRepository<Asset, Long> {

    Optional<Asset> findByCode(String code);

    List<Asset> findByActiveTrueOrderByNameAsc();
}
