import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

# Load frontend environment variables
load_dotenv("../.env")

url = os.getenv("VITE_SUPABASE_URL")
key = os.getenv("VITE_SUPABASE_ANON_KEY")

if not url or not key:
    print("Warning: Supabase credentials not found. Ensure .env exists in parent directory")

# Initialize Supabase Client
try:
    supabase: Client = create_client(url, key)
except Exception as e:
    print(f"Failed to initialize Supabase client: {e}")

app = FastAPI(title="WorkforcePro Python Backend")

# Allowing CORS for local Quasar testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Employee Data Model
class Employee(BaseModel):
    epf_no: str | None = None
    full_name: str
    nic_no: str
    sex: str | None = None
    birthday: str | None = None
    designation: str
    department: str
    category: str | None = None
    line: str | None = None
    joined_date: str
    status: str = "Active"
    basic_salary: float | None = 0.0
    bra: float | None = 0.0
    bank_name: str | None = None
    branch: str | None = None
    account_no: str | None = None
    address: str | None = None
    telephone_no: str | None = None
    emergency_contact: str | None = None
    fingerprint_id: str | None = None
    fingerprint_template: str | None = None
    chk_appForm: bool | None = False
    chk_nic: bool | None = False
    chk_birthCert: bool | None = False
    chk_police: bool | None = False
    educational_qualification: str | None = None
    religion: str | None = None
    ethnicity: str | None = None
    previous_employer: str | None = None
    photo_url: str | None = None
    probation_end_date: str | None = None

def extract_nic_details(nic: str):
    """Fallback NIC parsing logic in Backend"""
    nic = nic.strip()
    if len(nic) not in [10, 12]:
        return None, None
    
    if len(nic) == 10:
        year = "19" + nic[0:2]
        days = int(nic[2:5])
    else:
        year = nic[0:4]
        days = int(nic[4:7])

    sex = "Female" if days > 500 else "Male"
    if days > 500:
        days -= 500
    
    # Simple day logic
    if 0 < days <= 366:
        import datetime as dt
        # Start at Jan 1st
        start_date = dt.datetime(int(year), 1, 1)
        dob = start_date + dt.timedelta(days=days - 1)
        # Leap year adjustment for SL NIC standard (always assumes leap year for formula)
        is_leap = (int(year) % 4 == 0 and int(year) % 100 != 0) or (int(year) % 400 == 0)
        if not is_leap and days > 59:
            dob -= dt.timedelta(days=1)
        return sex, dob.strftime("%Y-%m-%d")
    return sex, None

def increment_data_version():
    """Increment the employee_data_version in system_settings"""
    try:
        res = supabase.table("system_settings").select("value").eq("key", "employee_data_version").execute()
        current_version = int(res.data[0]["value"]) if res.data else 0
        new_version = str(current_version + 1)
        supabase.table("system_settings").upsert({"key": "employee_data_version", "value": new_version}).execute()
        return new_version
    except Exception:
        pass

def log_activity(activity_type: str, details: str):
    try:
        supabase.table("activity_log").insert({"activity_type": activity_type, "details": details}).execute()
    except Exception:
        pass


@app.post("/add-employee")
def add_employee(emp: Employee):
    try:
        # 1. Duplicate check by NIC Number
        existing = supabase.table("employees").select("*").eq("nic_no", emp.nic_no.strip()).execute()
        if existing.data and len(existing.data) > 0:
            raise HTTPException(status_code=400, detail="Employee with this NIC already exists!")

        # 2. Auto EPF Generation (E.g. E001, E002...) if strictly required, or numeric
        if not emp.epf_no or emp.epf_no.strip() == "":
            res_epf = supabase.table("employees").select("epf_no").execute()
            epfs = res_epf.data
            max_num = 0
            for e in epfs:
                num_part = re.sub(r'\D', '', e['epf_no'])
                if num_part.isdigit():
                    max_num = max(max_num, int(num_part))
            emp.epf_no = f"EPF{max_num + 1:04d}" # e.g. EPF0001
        
        # Check EPF conflict just in case
        existing_epf = supabase.table("employees").select("*").eq("epf_no", emp.epf_no.strip()).execute()
        if existing_epf.data and len(existing_epf.data) > 0:
            raise HTTPException(status_code=400, detail=f"EPF No {emp.epf_no} already exists!")

        # 3. Auto calculate Sex and DOB if not provided
        if not emp.sex or not emp.birthday:
            sex, dob = extract_nic_details(emp.nic_no)
            if sex: emp.sex = sex
            if dob: emp.birthday = dob

        # 4. Probation End Date Calculation
        if emp.joined_date and not emp.probation_end_date:
            jd = datetime.strptime(emp.joined_date, "%Y-%m-%d")
            ped = jd + relativedelta(months=6) # 6 months probation by default
            emp.probation_end_date = ped.strftime("%Y-%m-%d")

        data = emp.model_dump(exclude_none=True)
        response = supabase.table("employees").insert(data).execute()

        # 5. Data Versioning & Activity Logging
        increment_data_version()
        log_activity("Employee Added", f"New Employee {emp.full_name} ({emp.epf_no}) was registered.")

        return {"success": True, "message": "Employee registered successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get-employees")
def get_employees():
    try:
        response = supabase.table("employees").select("*").order("created_at", desc=True).execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/update-employee/{epf_no}")
def update_employee(epf_no: str, emp: dict):
    try:
        response = supabase.table("employees").update(emp).eq("epf_no", epf_no).execute()
        
        increment_data_version()
        log_activity("Employee Updated", f"Employee details updated for EPF: {epf_no}")

        return {"success": True, "message": "Employee updated successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Welcome to WorkforcePro Backend API"}
