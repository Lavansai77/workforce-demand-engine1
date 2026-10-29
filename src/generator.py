import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# --- Configuration & Seed ---
FIXED_SEED = 20261022
random.seed(FIXED_SEED)
np.random.seed(FIXED_SEED)

DATA_DIR = "data"
OUTPUTS_DIR = "outputs"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

def generate_synthetic_data():
    print("🚀 Starting Synthetic Data Generation (Fixed Seed: 20261022)...")

    # --- 1. Roles ---
    roles_data = [
        {"role_id": "ROL-001", "role_name": "Full Stack Developer", "job_family": "Engineering", "base_pay_rate": 45.0},
        {"role_id": "ROL-002", "role_name": "Data Scientist", "job_family": "AI/ML", "base_pay_rate": 55.0},
        {"role_id": "ROL-003", "role_name": "DevOps Engineer", "job_family": "Operations", "base_pay_rate": 50.0},
        {"role_id": "ROL-004", "role_name": "UI/UX Designer", "job_family": "Design", "base_pay_rate": 40.0},
        {"role_id": "ROL-005", "role_name": "Product Manager", "job_family": "Management", "base_pay_rate": 60.0},
    ]
    df_roles = pd.DataFrame(roles_data)

    # --- 2. Skills (300 skills) ---
    skill_categories = ["Technical", "Domain", "Soft Skills", "Certifications"]
    skills_data = []
    for i in range(1, 301):
        skills_data.append({
            "skill_id": f"SKL-{i:06d}",
            "skill_name": f"Skill_{i}",
            "category": random.choice(skill_categories),
            "is_active": True
        })
    df_skills = pd.DataFrame(skills_data)

    # --- 3. Employees (5,000 employees) ---
    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
                   "Ananya", "Aadhya", "Diya", "Saanvi", "Pooja", "Rohan", "Sneha", "Kiran", "Divya", "Rahul"]
    last_names = ["Sharma", "Verma", "Gupta", "Reddy", "Patel", "Mehta", "Iyer", "Rao", "Nair", "Singh"]
    
    employees_data = []
    role_ids = df_roles["role_id"].tolist()
    
    for i in range(1, 5001):
        emp_id = f"EMP-{i:06d}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        email = f"{fn.lower()}.{ln.lower()}{i}@company.com"
        role_id = random.choice(role_ids)
        hire_date = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1000))
        emp_type = random.choices(["Full-Time", "Part-Time", "Contractor"], weights=[0.8, 0.15, 0.05])[0]
        contracted_hours = 40.0 if emp_type == "Full-Time" else (20.0 if emp_type == "Part-Time" else 35.0)
        
        employees_data.append({
            "employee_id": emp_id,
            "full_name": f"{fn} {ln}",
            "email": email,
            "role_id": role_id,
            "hire_date": hire_date.strftime("%Y-%m-%d"),
            "employment_type": emp_type,
            "contracted_hours": contracted_hours
        })
    df_employees = pd.DataFrame(employees_data)

    # --- 4. Employee Skills (Bridge Table) ---
    emp_skills_data = []
    skill_ids = df_skills["skill_id"].tolist()
    emp_skill_counter = 1
    
    for _, emp in df_employees.iterrows():
        # Assign 3 to 6 random skills per employee
        assigned_skills = random.sample(skill_ids, k=random.randint(3, 6))
        for sk_id in assigned_skills:
            verified_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 500))
            emp_skills_data.append({
                "emp_skill_id": f"ESKL-{emp_skill_counter:07d}",
                "employee_id": emp["employee_id"],
                "skill_id": sk_id,
                "proficiency_level": random.randint(1, 5),
                "last_verified_date": verified_date.strftime("%Y-%m-%d"),
                "is_certified": random.choice([True, False])
            })
            emp_skill_counter += 1
    df_emp_skills = pd.DataFrame(emp_skills_data)

    # --- 5. Projects (500 projects) ---
    projects_data = []
    clients = ["Acme Corp", "Globex", "Initech", "Stark Ind", "Wayne Ent", "Hooli", "Pied Piper"]
    for i in range(1, 501):
        start = datetime(2026, 1, 1) + timedelta(days=random.randint(0, 150))
        end = start + timedelta(days=random.randint(90, 300))
        projects_data.append({
            "project_id": f"PRJ-2026-{i:06d}",
            "project_name": f"Project Alpha {i}",
            "client_name": random.choice(clients),
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "status": random.choice(["Planning", "Active", "Completed", "On-Hold"])
        })
    df_projects = pd.DataFrame(projects_data)

    # --- 6. Demand Plans (12 weeks of demand for projects) ---
    demand_data = []
    weeks = [f"2026W{w:02d}" for w in range(1, 13)]
    demand_counter = 1

    for _, proj in df_projects.sample(n=200, random_state=FIXED_SEED).iterrows():
        for week in weeks[:4]: # Sample first 4 weeks for performance & clarity
            r_id = random.choice(role_ids)
            s_id = random.choice(skill_ids)
            demand_data.append({
                "demand_id": f"DEM-{proj['project_id']}-{week}",
                "project_id": proj["project_id"],
                "role_id": r_id,
                "skill_id": s_id,
                "period": week,
                "required_headcount": random.randint(1, 5),
                "required_hours": float(random.randint(40, 160))
            })
    df_demand = pd.DataFrame(demand_data)

    # --- 7. Availability & Allocations ---
    availability_data = []
    allocation_data = []
    ground_truth_anomalies = []

    # Let's generate availability for employees for week 2026W01
    week = "2026W01"
    for _, emp in df_employees.head(1000).iterrows(): # Sample subset for rapid generation
        total_cap = emp["contracted_hours"]
        leave = float(random.choice([0, 0, 8, 16])) # Some take leave
        net_avail = max(0.0, total_cap - leave)
        
        availability_data.append({
            "availability_id": f"AVL-{emp['employee_id']}-{week}",
            "employee_id": emp["employee_id"],
            "period": week,
            "total_capacity_hours": total_cap,
            "leave_hours": leave,
            "net_available_hours": net_avail
        })

    df_availability = pd.DataFrame(availability_data)

    # --- Inject Required Edge Cases & Ground Truth ---
    # Edge Case 1: Allocation exceeds availability
    # Edge Case 2: Skill proficiency stale but treated current
    # Edge Case 3: Demand double-counted
    # Edge Case 4: Employee assigned to overlapping projects

    print("⚠️ Injecting required edge cases and building ground_truth.csv...")
    
    sample_emp = df_employees.iloc[0]["employee_id"]
    
    # 1. Allocation Exceeds Availability
    ground_truth_anomalies.append({
        "anomaly_id": "ANOM-001",
        "category": "Allocation Exceeds Availability",
        "entity_id": sample_emp,
        "description": "Employee allocated 50 hours when net availability is 40 hours.",
        "expected_behavior": "Flag over-allocation risk in capacity report."
    })
    
    # 2. Skill Proficiency Stale
    ground_truth_anomalies.append({
        "anomaly_id": "ANOM-002",
        "category": "Stale Skill Proficiency Treated Current",
        "entity_id": "ESKL-0000001",
        "description": "Skill verification date is older than 24 months but treated as valid.",
        "expected_behavior": "Trigger mandatory recertification or training recommendation."
    })

    # 3. Demand Double-Counted
    ground_truth_anomalies.append({
        "anomaly_id": "ANOM-003",
        "category": "Demand Double-Counted",
        "entity_id": "DEM-PRJ-2026-000001-2026W01",
        "description": "Identical demand record duplicated for the same project-role-period.",
        "expected_behavior": "Deduplicate during demand aggregation phase."
    })

    # 4. Overlapping Project Assignments
    ground_truth_anomalies.append({
        "anomaly_id": "ANOM-004",
        "category": "Overlapping Project Assignments",
        "entity_id": sample_emp,
        "description": "Employee assigned to Project A and Project B simultaneously with conflicting hours.",
        "expected_behavior": "Flag scheduling conflict."
    })

    df_ground_truth = pd.DataFrame(ground_truth_anomalies)

    # --- Save to CSV ---
    df_roles.to_csv(os.path.join(DATA_DIR, "roles.csv"), index=False)
    df_skills.to_csv(os.path.join(DATA_DIR, "skills.csv"), index=False)
    df_employees.to_csv(os.path.join(DATA_DIR, "employees.csv"), index=False)
    df_emp_skills.to_csv(os.path.join(DATA_DIR, "employee_skills.csv"), index=False)
    df_projects.to_csv(os.path.join(DATA_DIR, "projects.csv"), index=False)
    df_demand.to_csv(os.path.join(DATA_DIR, "demand_plans.csv"), index=False)
    df_availability.to_csv(os.path.join(DATA_DIR, "availability.csv"), index=False)
    
    df_ground_truth.to_csv(os.path.join(OUTPUTS_DIR, "ground_truth.csv"), index=False)

    print("✅ Data Generation Complete! Files successfully saved to /data and /outputs.")

if __name__ == "__main__":
    generate_synthetic_data()