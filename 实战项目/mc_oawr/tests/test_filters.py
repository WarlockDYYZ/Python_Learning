"""D2/D6: 筛选模块单元测试

测试用例覆盖：
- 正常日期范围筛选
- 单渠道筛选
- 无交集筛选（应报错）
- 空结果处理
- 日期边界测试
"""
import sys
import os
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.filters import filter_df, filter_by_date, filter_by_channel
from src.clean import clean_sales_data
from src.generate_data import generate_sales_data


@pytest.fixture
def sample_df():
    """生成测试用数据"""
    df = generate_sales_data(n_days=30, seed=42)
    df = clean_sales_data(df)
    return df


class TestFilterByDate:
    def test_full_range(self, sample_df):
        result = filter_by_date(sample_df, start_date="2025-09-01", end_date="2025-09-30")
        assert len(result) > 0
        assert result["date"].min() >= pd.Timestamp("2025-09-01")
        assert result["date"].max() <= pd.Timestamp("2025-09-30")

    def test_single_day(self, sample_df):
        result = filter_by_date(sample_df, start_date="2025-09-15", end_date="2025-09-15")
        assert len(result) > 0
        assert all(result["date"] == pd.Timestamp("2025-09-15"))

    def test_no_overlap(self, sample_df):
        result = filter_by_date(sample_df, start_date="2020-01-01", end_date="2020-01-31")
        assert len(result) == 0


class TestFilterByChannel:
    def test_single_channel(self, sample_df):
        result = filter_by_channel(sample_df, channels=["抖音"])
        assert len(result) > 0
        assert all(result["channel"] == "抖音")

    def test_multiple_channels(self, sample_df):
        result = filter_by_channel(sample_df, channels=["抖音", "淘宝"])
        assert len(result) > 0
        assert set(result["channel"].unique()).issubset({"抖音", "淘宝"})

    def test_nonexistent_channel(self, sample_df):
        with pytest.raises(ValueError):
            filter_by_channel(sample_df, channels=[" nonexistent_channel "])

    def test_none_channels(self, sample_df):
        result = filter_by_channel(sample_df, channels=None)
        assert len(result) == len(sample_df)


class TestFilterDF:
    def test_combined_filter(self, sample_df):
        result = filter_df(sample_df, start_date="2025-09-01", end_date="2025-09-15", channels=["抖音"])
        assert len(result) > 0
        assert all(result["date"] >= pd.Timestamp("2025-09-01"))
        assert all(result["channel"] == "抖音")

    def test_empty_result_raises(self, sample_df):
        with pytest.raises(AssertionError):
            filter_df(sample_df, start_date="2020-01-01", end_date="2020-01-31")

    def test_duplicate_removal(self, sample_df):
        # 手动添加重复行
        df_with_dups = pd.concat([sample_df, sample_df.head(5)], ignore_index=True)
        result = filter_df(df_with_dups)
        assert result.duplicated().sum() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])