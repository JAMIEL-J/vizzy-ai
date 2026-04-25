import pandas as pd
from app.services.analytics.chart_recommender import _get_churn_count_by_segment
import warnings

warnings.filterwarnings('ignore')

csv_path = r'D:\Vizzy Redesign\Vizzy Redesign\backend\tests\datasets\churn.csv'
print(f"Using {csv_path}")

try:
    df = pd.read_csv(csv_path)
    churn_col = next((c for c in df.columns if 'churn' in c.lower() or 'exited' in c.lower() or 'attrition' in c.lower()), None)
    gender_col = next((c for c in df.columns if 'gender' in c.lower()), None)
    contract_col = next((c for c in df.columns if 'contract' in c.lower() or 'type' in c.lower()), None)
    
    print(f"Columns - Churn: {churn_col}, Gender: {gender_col}, Contract: {contract_col}")
    
    if churn_col and gender_col:
        res1 = _get_churn_count_by_segment(df, churn_col, gender_col)
        print("Unfiltered Churn Count by gender:", res1)
        print("Original total count by gender:", df.groupby(gender_col).size().to_dict())

    if churn_col and gender_col and contract_col:
        m2m_value = next((v for v in df[contract_col].unique() if 'month' in str(v).lower()), None)
        if m2m_value:
            print(f"Month-to-month value is '{m2m_value}'")
            df_filtered = df[df[contract_col] == m2m_value]
            res2 = _get_churn_count_by_segment(df_filtered, churn_col, gender_col)
            print("Filtered Churn Count by gender (Month-to-month):", res2)
            res_total = df_filtered.groupby(gender_col).size().to_dict()
            print("Total counts in filtered df:\n", res_total)
            
            # Show a sample of the filtered dataframe's churn column
            print("Sample of target column values in filtered df:")
            print(df_filtered[[gender_col, churn_col]].head(10))
            
except Exception as e:
    import traceback
    traceback.print_exc()
