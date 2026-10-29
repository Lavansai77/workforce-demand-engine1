import os
import pandas as pd

DATA_DIR = "data"
OUTPUT_SQL = os.path.join(DATA_DIR, "seed_dump.sql")

def generate_mysql_inserts(df, table_name):
    if df.empty:
        return f"-- No data for {table_name}\n"
    
    columns = list(df.columns)
    col_str = ", ".join([f"`{c}`" for c in columns])
    
    sql_statements = [f"-- Table structure and data for `{table_name}`\n"]
    
    for _, row in df.iterrows():
        values = []
        for val in row:
            if pd.isna(val):
                values.append("NULL")
            elif isinstance(val, (int, float)):
                values.append(str(val))
            else:
                # Escape single quotes for SQL safety
                escaped_val = str(val).replace("'", "''")
                values.append(f"'{escaped_val}'")
        
        val_str = ", ".join(values)
        sql_statements.append(f"INSERT INTO `{table_name}` ({col_str}) VALUES ({val_str});")
        
    return "\n".join(sql_statements) + "\n\n"

def export_to_mysql():
    print("📦 Exporting datasets to MySQL-compatible SQL seed dump...")
    
    tables = [
        "roles", "skills", "employees", "employee_skills", 
        "projects", "demand_plans", "availability"
    ]
    
    sql_lines = [
        "-- Workforce Demand Forecasting & Capacity Planning Engine",
        "-- MySQL Compatible Seed Dump",
        "-- Generated with Fixed Seed: 20261022\n",
        "SET FOREIGN_KEY_CHECKS = 0;\n"
    ]
    
    for table in tables:
        csv_path = os.path.join(DATA_DIR, f"{table}.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            sql_lines.append(generate_mysql_inserts(df, table))
        else:
            print(f"⚠️ Warning: {csv_path} not found. Skipping.")
            
    sql_lines.append("SET FOREIGN_KEY_CHECKS = 1;\n")
    
    with open(OUTPUT_SQL, "w", encoding="utf-8") as f:
        f.writelines("\n".join(sql_lines))
        
    print(f"✅ MySQL seed dump successfully created at: {OUTPUT_SQL}")

if __name__ == "__main__":
    export_to_mysql()