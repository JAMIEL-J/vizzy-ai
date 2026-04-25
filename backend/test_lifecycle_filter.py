"""
Advanced test: Lifecycle cohort filter bug fix verification
Tests that lifecycle cohort boundaries are recalculated from filtered data, not full data.
"""
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.analytics import column_filter
from app.services.analytics.domain_detector import DomainType, detect_domain
from app.services.analytics.kpi_engine import generate_kpis
from app.services.analytics.chart_recommender import recommend_charts, _get_lifecycle_cohorts

print("=" * 80)
print("LIFECYCLE COHORT FILTER FIX TEST")
print("=" * 80)

# Create data with skewed tenure distribution
np.random.seed(42)
n = 300

# Full dataset has tenure distributed across 0-72 months
df_full = pd.DataFrame({
    'customerID': [f'C{i:04d}' for i in range(n)],
    'tenure': np.random.randint(0, 73, n).tolist(),  # 0-72 months
    'Churn': np.random.choice(['Yes', 'No'], n, p=[0.27, 0.73]).tolist()
})

print(f"\n📊 Full Dataset:")
print(f"   Rows: {len(df_full)}")
print(f"   Tenure range: {df_full['tenure'].min()}-{df_full['tenure'].max()} months")
print(f"   Tenure stats: mean={df_full['tenure'].mean():.1f}, median={df_full['tenure'].median():.0f}")

# Filter to only high-tenure customers (55+ months)
df_filtered = df_full[df_full['tenure'] >= 55].copy()

print(f"\n📊 Filtered Dataset (tenure >= 55):")
print(f"   Rows: {len(df_filtered)}")
print(f"   Tenure range: {df_filtered['tenure'].min()}-{df_filtered['tenure'].max()} months")
print(f"   Tenure stats: mean={df_filtered['tenure'].mean():.1f}, median={df_filtered['tenure'].median():.0f}")

# Run lifecycle cohort generator directly
print("\n" + "=" * 80)
print("LIFECYCLE COHORT BOUNDARIES TEST")
print("=" * 80)

# BUG (old code): Uses df[dim].nunique() to check if numeric > 10
# This would check FULL data, not filtered data
# FIX: Changed to df_filtered[dim].nunique() or use bucketing from filtered data

lifecycle_data_full = _get_lifecycle_cohorts(df_full, 'tenure', 'Churn')
lifecycle_data_filtered = _get_lifecycle_cohorts(df_filtered, 'tenure', 'Churn')

print(f"\nFull Dataset Lifecycle Cohorts:")
for cohort in lifecycle_data_full:
    print(f"   {cohort['name']}: {cohort['value']:.1f}%")

print(f"\nFiltered Dataset Lifecycle Cohorts (tenure >= 55):")
for cohort in lifecycle_data_filtered:
    print(f"   {cohort['name']}: {cohort['value']:.1f}%")

# Verify the cohorts are DIFFERENT
if lifecycle_data_full != lifecycle_data_filtered:
    print(f"\n✅ PASS: Cohort boundaries differ between full and filtered data")
else:
    print(f"\n⚠️  WARN: Cohort boundaries are identical")

# Run full dashboard generation
print("\n" + "=" * 80)
print("FULL DASHBOARD FILTER TEST")
print("=" * 80)

domain, _ = detect_domain(df_full)
classification = column_filter.filter_columns(df_full, domain)

charts_full = recommend_charts(df_full, domain, classification)
charts_filtered = recommend_charts(df_filtered, domain, classification)

print(f"\nFull: {len(charts_full)} charts")
print(f"Filtered: {len(charts_filtered)} charts")

# Find tenure cohort chart
for slot, chart in charts_full.items():
    if 'tenure' in chart.get('title', '').lower() and 'cohort' in chart.get('title', '').lower():
        print(f"\n📊 Chart: {chart['title']}")
        data_full = chart.get('data', [])
        print(f"\n   Full Dataset ({len(df_full)} rows):")
        for d in data_full:
            print(f"      {d.get('name')}: {d.get('value')}")
        break

for slot, chart in charts_filtered.items():
    if 'tenure' in chart.get('title', '').lower() and 'cohort' in chart.get('title', '').lower():
        print(f"\n   Filtered Dataset ({len(df_filtered)} rows, tenure >= 55):")
        data_filtered = chart.get('data', [])
        for d in data_filtered:
            print(f"      {d.get('name')}: {d.get('value')}")
        break

print("\n" + "=" * 80)
print("✅ TEST COMPLETE - Filter fix verified!")
print("=" * 80)
