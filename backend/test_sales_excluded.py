import pandas as pd
import numpy as np
import json
import traceback
import sys
from app.services.analytics import column_filter
from app.services.analytics.kpi_engine import generate_kpis
from app.services.analytics.domain_detector import DomainType

# Generate sales data with a high-cardinality ID column
np.random.seed(42)
n = 100
data = {
    'InvoiceID': [100 + i // 2 for i in range(n)], # 50 unique orders
    'LineItemID': [i for i in range(n)],           # 100 unique items
    'Ref_Type': np.random.choice(['A', 'B'], n).tolist(),
    'Sales': (np.random.rand(n) * 100).tolist()
}
df = pd.DataFrame(data)

try:
    # 1. Classify columns
    c = column_filter.filter_columns(df, DomainType.SALES)
    print("Classified Columns:")
    print(f"  Metrics: {c.metrics}")
    print(f"  Dimensions: {c.dimensions}")
    print(f"  Excluded: {c.excluded}") # InvoiceID and LineItemID should be here

    # 2. Generate KPIs
    kpis = generate_kpis(df, DomainType.SALES, c)

    print("\nGenerated KPIs:")
    for k, v in kpis.items():
        if "Orders" in v['title']:
            print(f"  - {v['title']}: {v['value']} ({v['format']})")
            print(f"    Subtitle: {v.get('subtitle')}")
            print(f"    Reason: {v.get('reason')}")

    # Verification
    total_orders_kpi = next((v for v in kpis.values() if v['title'] == "Total Orders"), None)
    
    if total_orders_kpi:
        val = total_orders_kpi['value']
        subtitle = total_orders_kpi.get('subtitle', '')
        reason = total_orders_kpi.get('reason', '')
        
        print("\nVerification Results:")
        print(f"Primary Value: {val}")
        print(f"Subtitle: {subtitle}")
        print(f"Reason: {reason}")
        
        if val == 50 and "InvoiceID" in reason:
            print("SUCCESS: Identified InvoiceID as order primary despite being excluded/high-cardinality.")
        elif val == 100:
            print("FAILURE: Fell back to record count or picked LineItemID.")
        else:
            print(f"FAILURE: Got unexpected value {val}")

except Exception as e:
    traceback.print_exc()
