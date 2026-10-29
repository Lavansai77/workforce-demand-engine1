import os
import pandas as pd

DATA_DIR = "data"

def run_validation():
    print("🔍 Starting Automated Data Validation Suite...\n")
    
    # Load Datasets
    try:
        df_roles = pd.read_csv(os.path.join(DATA_DIR, "roles.csv"))
        df_skills = pd.read_csv(os.path.join(DATA_DIR, "skills.csv"))
        df_employees = pd.read_csv(os.path.join(DATA_DIR, "employees.csv"))
        df_emp_skills = pd.read_csv(os.path.join(DATA_DIR, "employee_skills.csv"))
        df_projects = pd.read_csv(os.path.join(DATA_DIR, "projects.csv"))
        df_demand = pd.read_csv(os.path.join(DATA_DIR, "demand_plans.csv"))
        df_availability = pd.read_csv(os.path.join(DATA_DIR, "availability.csv"))
    except FileNotFoundError as e:
        print(f"❌ Error: Missing generated data file. Please run generator.py first. ({e})")
        return

    validation_passed = True

    # --- Check 1: Primary Key Uniqueness ---
    print("Checking Primary Key Uniqueness...")
    checks = [
        (df_roles, "role_id", "Roles"),
        (df_skills, "skill_id", "Skills"),
        (df_employees, "employee_id", "Employees"),
        (df_projects, "project_id", "Projects"),
        (df_demand, "demand_id", "DemandPlans")
    ]
    
    for df, pk, name in checks:
        duplicates = df[df.duplicated(subset=[pk])]
        if len(duplicates) > 0:
            print(f"  ❌ FAILED: Duplicate primary keys found in {name}: {len(duplicates)} rows.")
            validation_passed = False
        else:
            print(f"  ✅ PASSED: {name} primary key ({pk}) is unique.")

    # --- Check 2: Foreign Key Integrity ---
    print("\nChecking Foreign Key Integrity...")
    
    # Employees -> Roles
    invalid_roles = df_employees[~df_employees["role_id"].isin(df_roles["role_id"])]
    if len(invalid_roles) > 0:
        print(f"  ❌ FAILED: Employees reference non-existent role IDs: {len(invalid_roles)} rows.")
        validation_passed = False
    else:
        print("  ✅ PASSED: Employee foreign keys (role_id) are valid.")

    # Demand Plans -> Projects
    invalid_proj = df_demand[~df_demand["project_id"].isin(df_projects["project_id"])]
    if len(invalid_proj) > 0:
        print(f"  ❌ FAILED: Demand plans reference non-existent project IDs: {len(invalid_proj)} rows.")
        validation_passed = False
    else:
        print("  ✅ PASSED: DemandPlan foreign keys (project_id) are valid.")

    # --- Check 3: Date Ordering Logic ---
    print("\nChecking Date Ordering Logic...")
    df_projects["start_date"] = pd.to_datetime(df_projects["start_date"])
    df_projects["end_date"] = pd.to_datetime(df_projects["end_date"])
    invalid_dates = df_projects[df_projects["end_date"] < df_projects["start_date"]]
    
    if len(invalid_dates) > 0:
        print(f"  ❌ FAILED: Projects found where end_date is before start_date: {len(invalid_dates)} rows.")
        validation_passed = False
    else:
        print("  ✅ PASSED: All project start and end dates are chronologically sound.")

    # --- Check 4: Capacity Reconciliation ---
    print("\nChecking Capacity Reconciliation (Net Available = Total - Leave)...")
    df_availability["calculated_net"] = df_availability["total_capacity_hours"] - df_availability["leave_hours"]
    # Ensure non-negative
    df_availability["calculated_net"] = df_availability["calculated_net"].apply(lambda x: max(0.0, x))
    
    discrepancies = df_availability[df_availability["net_available_hours"] != df_availability["calculated_net"]]
    if len(discrepancies) > 0:
        print(f"  ❌ FAILED: Capacity reconciliation mismatch found: {len(discrepancies)} rows.")
        validation_passed = False
    else:
        print("  ✅ PASSED: Availability capacity reconciles correctly across all records.")

    # --- Final Summary ---
    print("\n" + "="*50)
    if validation_passed:
        print("🎉 ALL VALIDATION CHECKS PASSED SUCCESSFULLY!")
    else:
        print("⚠️ Validation completed with errors. Review output logs above.")
    print("="*50)

if __name__ == "__main__":
    run_validation()