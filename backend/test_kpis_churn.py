import pandas as pd
import numpy as np
import json
import traceback
import sys
from app.services.analytics import column_filter
from app.services.analytics.kpi_engine import generate_kpis
from app.services.analytics.domain_detector import DomainType

# Generate more realistic telco churn data
np.random.seed(42)
data = {
    'customerID': [f'C{i}' for i in range(100)],
    'tenure': np.random.randint(1, 72, 100).tolist(),
    'MonthlyCharges': (np.random.rand(100) * 100).tolist(),
    'TotalCharges': (np.random.rand(100) * 5000).tolist(),
    'Churn': np.random.choice(['Yes', 'No'], 100, p=[0.2, 0.8]).tolist(),
    'Support_Tickets': np.random.randint(0, 5, 100).tolist()
}
df = pd.DataFrame(data)

try:
    # 1. Classify columns
    c = column_filter.filter_columns(df, DomainType.CHURN)
    print("Classified Columns:")
    print(f"  Metrics: {c.metrics}")
    print(f"  Dimensions: {c.dimensions}")
    print(f"  Targets: {c.targets}")

    # 2. Generate KPIs
    kpis = generate_kpis(df, DomainType.CHURN, c)

    print("\nGenerated KPIs:")
    for k, v in kpis.items():
        print(f"  - {v['title']}: {v['value']} ({v['format']}) - {v['reason']}")

    # Save to file for inspection
    with open("test_kpis_churn_result.json", "w") as f:
        json.dump(kpis, f, indent=2)
    
    # Check if ARPU, LTV, and Support Tickets are present
    titles = [v['title'] for v in kpis.values()]
    has_arpu = any("ARPU" in t for t in titles)
    has_ltv = any("LTV" in t for t in titles)
    has_tickets = any("Tickets" in t or "Support" in t for t in titles)

    print("\nVerification:")
    print(f"  Has ARPU: {has_arpu}")
    print(f"  Has LTV: {has_ltv}")
    print(f"  Has Support Tickets: {has_tickets}")

    if has_arpu and has_ltv and has_tickets:
        print("\nAll target KPIs generated successfully!")
    else:
        print("\nSome metrics are missing. Check column finding logic.")

except Exception as e:
    traceback.print_exc()
