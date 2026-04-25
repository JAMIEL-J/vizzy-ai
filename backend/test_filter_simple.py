"""
Simple test to verify churn dashboard filter fix.
"""
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.analytics import column_filter
from app.services.analytics.domain_detector import DomainType, detect_domain
from app.services.analytics.kpi_engine import generate_kpis
from app.services.analytics.chart_recommender import recommend_charts

# Create test data
np.random.seed(42)
n = 200
df = pd.DataFrame({
    'customerID': [f'C{i:04d}' for i in range(n)],
    'gender': np.random.choice(['Male', 'Female'], n, p=[0.5, 0.5]).tolist(),
    'tenure': np.random.randint(0, 73, n).tolist(),
    'MonthlyCharges': (np.random.rand(n) * 100 + 20).tolist(),
    'Churn': np.random.choice(['Yes', 'No'], n, p=[0.27, 0.73]).tolist()
})

print("=" * 80)
print("CHURN DASHBOARD FILTER FIX TEST")
print("=" * 80)
print(f"\n📊 Dataset: {len(df)} rows")
print(f"   Full Churn: {(df['Churn'] == 'Yes').sum()} / {len(df)}")

# Full data
domain, _ = detect_domain(df)
classification = column_filter.filter_columns(df, domain)
kpis_full = generate_kpis(df, domain, classification)
charts_full = recommend_charts(df, domain, classification)

print(f"\n✅ Full: {len(kpis_full)} KPIs, {len(charts_full)} charts")

# Filter: Gender='Male'
df_male = df[df['gender'] == 'Male'].copy()
kpis_male = generate_kpis(df_male, domain, classification)
charts_male = recommend_charts(df_male, domain, classification)

male_churn = (df_male['Churn'] == 'Yes').sum()
print(f"\n📊 Filtered (Gender='Male'): {len(df_male)} rows")
print(f"   Filtered Churn: {male_churn} / {len(df_male)}")
print(f"✅ Filtered: {len(kpis_male)} KPIs, {len(charts_male)} charts")

# Test 1: KPI values should change
print("\n" + "=" * 80)
print("TEST 1: KPI VALUES CHANGE", "when filter applied")
print("=" * 80)

total_full = kpis_full['kpi_0']['value']
total_male = kpis_male['kpi_0']['value']

print(f"\nTotal Customers:")
print(f"   Full:     {total_full}")
print(f"   Filtered: {total_male}")
if total_male < total_full:
    print(f"   ✅ PASS: Filter reduced total customers")
else:
    print(f"   ❌ FAIL: Filter did not apply properly")

# Test 2: Chart data changes
print("\n" + "=" * 80)
print("TEST 2: CHART DATA CHANGES when filter applied")
print("=" * 80)

# Find "Churn Overview" (distribution chart)
churn_chart_full = None
churn_chart_male = None

for slot, chart in charts_full.items():
    if 'overview' in chart.get('title', '').lower() and 'churn' in chart.get('title', '').lower():
        churn_chart_full = chart
        break

for slot, chart in charts_male.items():
    if 'overview' in chart.get('title', '').lower() and 'churn' in chart.get('title', '').lower():
        churn_chart_male = chart
        break

if churn_chart_full and churn_chart_male:
    data_full = churn_chart_full.get('data', [])
    data_male = churn_chart_male.get('data', [])
    
    print(f"\nChart: {churn_chart_full['title']}")
    print(f"Type: {churn_chart_full['type']}")
    
    if data_full:
        total_f = sum(d.get('value', 0) for d in data_full)
        print(f"\n   Full: Total={total_f} from {len(data_full)} data points")
        for d in data_full:
            print(f"      {d.get('name')}: {d.get('value')}")
    
    if data_male:
        total_m = sum(d.get('value', 0) for d in data_male)
        print(f"\n   Filtered: Total={total_m} from {len(data_male)} data points")
        for d in data_male:
            print(f"      {d.get('name')}: {d.get('value')}")
        
        # Check: filtered total should equal len(df_male)
        if total_m == len(df_male):
            print(f"\n   ✅ PASS: Chart data matches filtered dataset size ({len(df_male)} rows)")
        else:
            print(f"\n   ❌ FAIL: Chart total {total_m} != expected {len(df_male)}")
    else:
        print(f"\n   ❌ FAIL: Filtered chart data is empty!")
else:
    print(f"⚠️  Could not find Churn Overview chart")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
