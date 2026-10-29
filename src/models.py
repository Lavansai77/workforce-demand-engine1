from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator

# --- 1. Role Model ---
class Role(BaseModel):
    role_id: str = Field(..., pattern=r"^ROL-\d{3}$")
    role_name: str
    job_family: str
    base_pay_rate: float = Field(..., ge=0.0)

# --- 2. Skill Model ---
class Skill(BaseModel):
    skill_id: str = Field(..., pattern=r"^SKL-\d{6}$")
    skill_name: str
    category: Literal["Technical", "Domain", "Soft Skills", "Certifications"]
    is_active: bool = True

# --- 3. Employee Model ---
class Employee(BaseModel):
    employee_id: str = Field(..., pattern=r"^EMP-\d{6}$")
    full_name: str
    email: EmailStr
    role_id: str = Field(..., pattern=r"^ROL-\d{3}$")
    hire_date: date
    employment_type: Literal["Full-Time", "Part-Time", "Contractor"]
    contracted_hours: float = Field(..., ge=0.0, le=50.0)

# --- 4. EmployeeSkill Model (Bridge Table) ---
class EmployeeSkill(BaseModel):
    emp_skill_id: str
    employee_id: str = Field(..., pattern=r"^EMP-\d{6}$")
    skill_id: str = Field(..., pattern=r"^SKL-\d{6}$")
    proficiency_level: int = Field(..., ge=1, le=5)  # 1 to 5 scale
    last_verified_date: date
    is_certified: bool

# --- 5. Project Model ---
class Project(BaseModel):
    project_id: str = Field(..., pattern=r"^PRJ-\d{4}-\d{6}$")
    project_name: str
    client_name: str
    start_date: date
    end_date: date
    status: Literal["Planning", "Active", "Completed", "On-Hold"]

    @field_validator('end_date')
    @classmethod
    def case_date_order(cls, v: date, info) -> date:
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError("end_date must be greater than or equal to start_date")
        return v

# --- 6. DemandPlan Model ---
class DemandPlan(BaseModel):
    demand_id: str = Field(..., pattern=r"^DEM-.*-2026W\d{2}$")
    project_id: str = Field(..., pattern=r"^PRJ-\d{4}-\d{6}$")
    role_id: str = Field(..., pattern=r"^ROL-\d{3}$")
    skill_id: str = Field(..., pattern=r"^SKL-\d{6}$")
    period: str = Field(..., pattern=r"^2026W\d{2}$")  # e.g., 2026W01
    required_headcount: int = Field(..., ge=1)
    required_hours: float = Field(..., ge=0.0)

# --- 7. Allocation Model ---
class Allocation(BaseModel):
    allocation_id: str = Field(..., pattern=r"^ALLOC-\d{4}-\d{6}$")
    employee_id: str = Field(..., pattern=r"^EMP-\d{6}$")
    demand_id: str
    period: str = Field(..., pattern=r"^2026W\d{2}$")
    allocated_hours: float = Field(..., ge=0.0)
    allocation_percentage: float = Field(..., ge=0.0, le=200.0)  # Allows edge case > 100%
    status: Literal["Proposed", "Confirmed", "Over-Allocated"]

# --- 8. Availability Model ---
class Availability(BaseModel):
    availability_id: str
    employee_id: str = Field(..., pattern=r"^EMP-\d{6}$")
    period: str = Field(..., pattern=r"^2026W\d{2}$")
    total_capacity_hours: float = Field(..., ge=0.0)
    leave_hours: float = Field(..., ge=0.0)
    net_available_hours: float = Field(..., ge=0.0)

# --- 9. Training Model ---
class Training(BaseModel):
    training_id: str
    employee_id: str = Field(..., pattern=r"^EMP-\d{6}$")
    skill_id: str = Field(..., pattern=r"^SKL-\d{6}$")
    training_name: str
    status: Literal["Enrolled", "In-Progress", "Completed", "Dropped"]
    completion_date: Optional[date] = None

# --- 10. GapAnalysis Model ---
class GapAnalysis(BaseModel):
    gap_id: str
    demand_id: str
    project_id: str = Field(..., pattern=r"^PRJ-\d{4}-\d{6}$")
    period: str = Field(..., pattern=r"^2026W\d{2}$")
    demand_hours: float = Field(..., ge=0.0)
    available_supply_hours: float = Field(..., ge=0.0)
    gap_hours: float  # Can be negative if surplus, positive if gap
    action_recommended: Literal["Hire", "Upskill", "Reallocate", "None"]