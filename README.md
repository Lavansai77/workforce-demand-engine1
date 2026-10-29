# Workforce Demand Forecasting & Capacity Planning Engine

An end-to-end data generation, demand forecasting, and workforce capacity planning system designed for enterprise resource management. This engine simulates large-scale organizational data (5,000 employees, 300 skills, 500 projects), applies complex business rules (leave, part-time capacity, skill expiry), injects labeled edge cases, and provides automated validation and MySQL-compatible SQL seed dumps.

---

## 🚀 Tech Stack
* **Core Language:** Python 3.10+
* **Data Processing & Simulation:** Pandas, NumPy
* **Schema Validation:** Pydantic (v2)
* **Storage & Export Formats:** CSV, JSON, and MySQL-Compatible SQL (`InnoDB`)
* **Reproducibility:** Fixed random seed (`20261022`) with deterministic ID generation.

---

## 📁 Project Directory Structure
```text
workforce-demand-engine/
│
├── data/                    # Generated CSV datasets and MySQL SQL seed dump
│   ├── employees.csv
│   ├── skills.csv
│   ├── roles.csv
│   ├── projects.csv
│   ├── employee_skills.csv
│   ├── demand_plans.csv
│   ├── availability.csv
│   └── seed_dump.sql        # MySQL-compatible DML/DDL seed file
│
├── outputs/                 # Labeled anomaly outputs
│   └── ground_truth.csv     # Isolated edge cases and negative scenarios
│
├── src/                     # Source code package
│   ├── __init__.py
│   ├── models.py            # Pydantic schema definitions & data dictionary
│   ├── generator.py         # Synthetic data generation engine
│   ├── validator.py         # Automated data validation & reconciliation suite
│   └── exporter.py          # MySQL SQL export script
│
├── docs/
│   └── prompt_history.md    # AI prompt transparency history
│
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
⚙️ Setup & Installation Instructions
Clone or Navigate to the Repository:

Bash
cd workforce-demand-engine
Create and Activate a Virtual Environment:

Windows (Command Prompt):

DOS
python -m venv venv
venv\Scripts\activate.bat
macOS / Linux:

Bash
python3 -m venv venv
source venv/bin/activate
Install Dependencies:

Bash
pip install -r requirements.txt
▶️ How to Run the Pipeline
Execute the scripts in the following order:

1. Generate Synthetic Data
Generates the baseline master and transaction records using the fixed seed (20261022) and creates labeled edge cases in outputs/ground_truth.csv.

Bash
python src/generator.py
2. Run Automated Validation Suite
Validates primary key uniqueness, foreign key referential integrity, date ordering logic, and capacity reconciliation.

Bash
python src/validator.py
3. Export to MySQL SQL Seed Dump
Converts CSV datasets into a production-ready MySQL SQL seed dump (data/seed_dump.sql).

Bash
python src/exporter.py
