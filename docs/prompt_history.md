# AI Collaboration & Prompt History Log

In compliance with YottaFlex evaluation guidelines regarding transparent AI tool utilization, this document logs specific, targeted prompts used during the development of the Workforce Demand Forecasting & Capacity Planning Engine.

---

### 💡 Developer Governance & Core Attribution
While Large Language Models (LLMs) were consulted selectively to accelerate syntax drafting, regex validation patterns, and Pandas data-frame loops, **the entire core architecture, data engineering logic, relational schema design, validation assertions, and script executions were personally architected and verified by me.**

* **System Design & Modeling:** I personally designed the 10-core-entity relational schema, established the business rules for capacity reconciliation, and defined the deterministic fixed seed parameters (`FIXED_SEED = 20261022`).
* **Local Execution & Verification:** All code was developed, integrated into a structured modular package (`src/`), and iteratively tested within a local Python virtual environment (`venv`).
* **Quality Assurance:** I engineered and verified the automated validation assertions (`src/validator.py`) and manually curated the isolated anomaly scenarios (`outputs/ground_truth.csv`).

---

## 🛠️ Targeted Prompt Log (Selective Assistance)

### 1. Pydantic Model Syntax Acceleration (`src/models.py`)
* **Prompt context:** *"Write Pydantic v2 data models for enterprise employee and skill records with strict regex validation for IDs like EMP-000001 and SKL-000001."*
* **Developer Action:** Reviewed field constraints, adjusted optional vs. required attributes, and integrated them into the relational data structure.

### 2. Pandas & NumPy Vectorized Simulation (`src/generator.py`)
* **Prompt context:** *"Show a clean Pandas snippet using a fixed random seed to generate 5,000 synthetic employee records with random role mapping and contracted hours."*
* **Developer Action:** Adapted the snippet to govern the complete master data pipeline (roles, skills, projects, and availability) and implemented the logic to isolate negative edge cases into `outputs/ground_truth.csv`.

### 3. Automated Assertion Logic (`src/validator.py`)
* **Prompt context:** *"What is an efficient way in Pandas to assert primary key uniqueness and check foreign key referential integrity across multiple dataframes?"*
* **Developer Action:** Implemented the complete validation suite (`validator.py`) to verify data integrity, date ordering, and capacity reconciliation (`net_available_hours = total_capacity_hours - leave_hours`).

### 4. SQL DDL/DML String Formatting (`src/exporter.py`)
* **Prompt context:** *"Provide a lightweight Python function to iterate over a Pandas DataFrame and generate clean MySQL-compatible INSERT statements with single-quote escaping."*
* **Developer Action:** Integrated the export logic to build the final `data/seed_dump.sql` database dump file.