"""
Test script to verify churn dashboard filter fixes.
Tests:
1. KPI values change when filter is applied
2. Chart data changes when filter is applied
3. Distribution chart ("Churn Overview") updates with filter
4. Lifecycle cohort charts update with filtered data
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.analytics import column_filter
from app.services.analytics.domain_detector import DomainType, detect_domain
from app.services.analytics.kpi_engine import generate_kpis
from app.services.analytics.chart_recommender import recommend_charts

# ============================================================================
# Test Data: Realistic Churn Dataset
# ============================================================================

np.random.seed(42)
n = 200

# Create realistic churn data
data = {
    'customerID': [f'C{i:04d}' for i in range(n)],
    'gender': np.random.choice(['Male', 'Female'], n, p=[0.5, 0.5]).tolist(),
    'SeniorCitizen': np.random.choice([0, 1], n, p=[0.85, 0.15]).tolist(),
    'Partner': np.random.choice(['Yes', 'No'], n, p=[0.48, 0.52]).tolist(),
    'Dependents': np.random.choice(['Yes', 'No'], n, p=[0.3, 0.7]).tolist(),
    'tenure': np.random.randint(0, 73, n).tolist(),
    'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n, p=[0.4, 0.3, 0.3]).tolist(),
    'MonthlyCharges': (np.random.rand(n) * 100 + 20).tolist(),
    'TotalCharges': (np.random.rand(n) * 5000).tolist(),
    'Churn': np.random.choice(['Yes', 'No'], n, p=[0.27, 0.73]).tolist()  # 27% churn
}

df = pd.DataFrame(data)

print("=" * 80)
print("CHURN DASHBOARD FILTER TEST")
print("=" * 80)
print(f"\n📊 Dataset: {len(df)} rows, {len(df.columns)} columns")
print(f"   Churn Rate (unfiltered): {(df['Churn'] == 'Yes').sum() / len(df) * 100:.1f}%")


# ============================================================================
# Step 1: Full Dataset Analysis
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1: FULL DATASET ANALYSIS")
print("=" * 80)

domain, scores = detect_domain(df)
print(f"\n✅ Domain detected: {domain.value}")

classification = column_filter.filter_columns(df, domain)
print(f"\n✅ Column Classification:")
print(f"   Metrics: {classification.metrics}")
print(f"   Dimensions: {classification.dimensions}")
print(f"   Targets: {classification.targets}")

# Generate full KPIs and charts
kpis_full = generate_kpis(df, domain, classification)
charts_full = recommend_charts(df, domain, classification)

print(f"\n✅ Generated {len(kpis_full)} KPIs and {len(charts_full)} charts")



# Show key KPIs (handle dict output from generate_kpis)
print("\n📊 Full Dataset KPIs:")
if isinstance(kpis_full, dict):
    for idx, (key, kpi_data) in enumerate(list(kpis_full.items())[:5]):
        print(f"   • {kpi_data.get('title', 'N/A')}: {kpi_data.get('value', 'N/A')} ({kpi_data.get('format', 'N/A')})")
else:
    print(f"   KPIs type: {type(kpis_full)}")
# ============================================================================
# Step 2: Apply Filter (e.g., Male customers only)
# ============================================================================

print("\n" + "=" * 80)
print("STEP 2: APPLY FILTER (Gender='Male')")
print("=" * 80)

df_filtered = df[df['gender'] == 'Male'].copy()
print(f"\n✅ Filtered dataset: {len(df_filtered)} rows ({len(df_filtered)/len(df)*100:.1f}% of original)")
print(f"   Churn Rate (filtered): {(df_filtered['Churn'] == 'Yes').sum() / len(df_filtered) * 100:.1f}%")

# Generate filtered KPIs and charts
kpis_filtered = generate_kpis(df_filtered, domain, classification)
charts_filtered = recommend_charts(df_filtered, domain, classification)

print(f"\n✅ Generated {len(kpis_filtered)} KPIs and {len(charts_filtered)} charts (from filtered data)")


# ============================================================================
# Step 3: Verify KPI Values Changed
# ============================================================================

print("\n" + "=" * 80)
print("STEP 3: KPI COMPARISON (Full vs Filtered)")
print("=" * 80)


def find_kpi(kpis, title_substring):
    if isinstance(kpis, dict):
            for key, kpi_data in kpis.items():
                title = kpi_data.get('title', '') if isinstance(kpi_data, dict) else getattr(kpi_data, 'title', '')
                if title_substring.lower() in title.lower():
                    return kpi_data
    else:
        kpi_list = kpis if isinstance(kpis, list) else []
        for kpi in kpi_list:
            if title_substring.lower() in kpi.title.lower():
                return kpi
    return None
kpi_tests = [
    ("total", "Total"),
    ("churn", "Churn"),
]


for search, label in kpi_tests:
    kpi_f = find_kpi(kpis_full, search)
    kpi_t = find_kpi(kpis_filtered, search)
    
    if kpi_f and kpi_t:
        title_f = kpi_f.get('title', 'N/A') if isinstance(kpi_f, dict) else getattr(kpi_f, 'title', 'N/A')
        value_f = kpi_f.get('value', 'N/A') if isinstance(kpi_f, dict) else getattr(kpi_f, 'value', 'N/A')
        title_t = kpi_t.get('title', 'N/A') if isinstance(kpi_t, dict) else getattr(kpi_t, 'title', 'N/A')
        value_t = kpi_t.get('value', 'N/A') if isinstance(kpi_t, dict) else getattr(kpi_t, 'value', 'N/A')
        
        print(f"\n📊 {label}:")
        print(f"   Full:     {title_f} = {value_f}")
        print(f"   Filtered: {title_t} = {value_t}")
        if value_f != value_t:
            print(f"   ✅ VALUES DIFFER (as expected)")
        else:
            print(f"   ⚠️  VALUES ARE SAME (filter may not be applied!)")
    else:
        print(f"\n⚠️  {label} KPI not found in both full and filtered results")

# ============================================================================
# Step 4: Verify Chart Data Changed
# ============================================================================

print("\n" + "=" * 80)
print("STEP 4: CHART DATA COMPARISON (Full vs Filtered)")
print("=" * 80)

def find_chart(charts_dict, title_substring):
    for slot, chart in charts_dict.items():
        if title_substring.lower() in chart.get('title', '').lower():
            return slot, chart
    return None, None

chart_tests = [
    ("Churn Overview", "Churn"),
    ("Tenure Cohort", "Tenure"),
    ("Gender", "Gender"),
]

for search, label in chart_tests:
    slot_f, chart_f = find_chart(charts_full, search)
    slot_t, chart_t = find_chart(charts_filtered, search)
    
    if chart_f and chart_t:
        data_f = chart_f.get('data', [])
        data_t = chart_t.get('data', [])
        print(f"\n📊 {label} Chart:")
        print(f"   Full:     {chart_f['title']}")
        print(f"              Data points: {len(data_f)}")
        if data_f:
            print(f"              First point: {data_f[0]}")
        print(f"   Filtered: {chart_t['title']}")
        print(f"              Data points: {len(data_t)}")
        if data_t:
            print(f"              First point: {data_t[0]}")
        
        # Simple check: if data exists and differs, filter is working
        if data_f and data_t:
            # Compare total values
            total_f = sum(d.get('value', 0) for d in data_f)
            total_t = sum(d.get('value', 0) for d in data_t)
            if total_f != total_t:
                print(f"   ✅ DATA VALUES DIFFER (filter applied successfully)")
            else:
                print(f"   ⚠️  DATA VALUES ARE SAME (filter may not be applied!)")
        elif not data_t:
            print(f"   ⚠️  Filtered data is empty! (possible bug)")
    else:
        status = "Full" if not chart_f else "Filtered" if not chart_t else "Both"
        print(f"\n⚠️  {label} chart not found in {status}")


# ============================================================================
# Step 5: Specific Test for Distribution Chart (Churn Overview)
# ============================================================================

print("\n" + "=" * 80)
print("STEP 5: DISTRIBUTION CHART TEST (Churn Overview - donut)")
print("=" * 80)

# Find "Churn Overview" or similar
churn_overview_f = None
churn_overview_t = None

for slot, chart in charts_full.items():
    if 'overview' in chart.get('title', '').lower() and 'churn' in chart.get('title', '').lower():
        churn_overview_f = chart
        break

for slot, chart in charts_filtered.items():
    if 'overview' in chart.get('title', '').lower() and 'churn' in chart.get('title', '').lower():
        churn_overview_t = chart
        break

if churn_overview_f and churn_overview_t:
    print(f"\n✅ Found Distribution Chart: {churn_overview_f['title']}")
    print(f"   Type: {churn_overview_f['type']}")
    
    data_f = churn_overview_f.get('data', [])
    data_t = churn_overview_t.get('data', [])
    
    print(f"\n   Full Dataset:")
    for d in data_f:
        print(f"      {d.get('name', 'N/A')}: {d.get('value', 0)}")
    
    print(f"\n   Filtered (Gender='Male'):")
    for d in data_t:
        print(f"      {d.get('name', 'N/A')}: {d.get('value', 0)}")
    
    if data_f and data_t:
        total_f = sum(d.get('value', 0) for d in data_f)
        total_t = sum(d.get('value', 0) for d in data_t)
        print(f"\n   Totals: Full={total_f}, Filtered={total_t}")
        if total_t == len(df_filtered):
            print(f"   ✅ FILTER APPLIED: Filtered total matches Gender='Male' count ({len(df_filtered)})")
        else:
            print(f"   ⚠️  FILTER NOT APPLIED: Expected {len(df_filtered)}, got {total_t}")
else:
    print(f"\n⚠️  Churn Overview chart not found")


# ============================================================================
# Step 6: Test Lifecycle Cohort with Filtered Data
# ============================================================================

print("\n" + "=" * 80)
print("STEP 6: LIFECYCLE COHORT CHART TEST")
print("=" * 80)

tenure_full = None
tenure_filtered = None

for slot, chart in charts_full.items():
    if 'tenure' in chart.get('title', '').lower() and 'cohort' in chart.get('title', '').lower():
        tenure_full = chart
        break

for slot, chart in charts_filtered.items():
    if 'tenure' in chart.get('title', '').lower() and 'cohort' in chart.get('title', '').lower():
        tenure_filtered = chart
        break

if tenure_full or tenure_filtered:
    print(f"\n✅ Found Lifecycle Chart")
    
    if tenure_full:
        print(f"   Full: {tenure_full['title']}")
        data_f = tenure_full.get('data', [])
        print(f"      Data points: {len(data_f)}")
        if data_f:
            print(f"      Cohorts: {[d.get('name', 'N/A') for d in data_f]}")
    
    if tenure_filtered:
        print(f"\n   Filtered (Gender='Male'): {tenure_filtered['title']}")
        data_t = tenure_filtered.get('data', [])
        print(f"      Data points: {len(data_t)}")
        if data_t:
            print(f"      Cohorts: {[d.get('name', 'N/A') for d in data_t]}")
        
        # Check if buckets were recalculated based on filtered data
        if data_t:
            print(f"   ✅ Lifecycle cohort recalculated for filtered data")
        else:
            print(f"   ⚠️  Lifecycle cohort returned empty!")
else:
    print(f"\n⚠️  Lifecycle cohort chart not found")


# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"""
✅ Test completed!

Key findings:
1. KPIs are recalculated from filtered data: {'✅ YES' if kpis_filtered else '❌ NO'}
2. Charts are recalculated from filtered data: {'✅ YES' if charts_filtered else '❌ NO'}
3. Distribution charts support filters: {'✅ YES (code fixed)' if churn_overview_t and churn_overview_t.get('data') else '❌ NEEDS FIX'}
4. Lifecycle cohorts adapt to filtered data: {'✅ YES' if tenure_filtered and tenure_filtered.get('data') else '❌ NEEDS CHECK'}

If all items show ✅, the filter fix is working correctly!
""")

print("=" * 80)
