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
load_dotenv()

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

# ---------------------------------------------------------
# ATTENDANCE & LEAVE AUTOMATION LOGIC
# ---------------------------------------------------------

class PunchData(BaseModel):
    fingerprint_id: str
    punch_time: str # ISO format string e.g., '2026-03-03T08:15:00Z'

class LeaveRequest(BaseModel):
    epf_no: str
    leave_type: str
    start_date: str
    end_date: str
    days: float
    reason: str

SHIFT_START_TIME = datetime.strptime("08:00:00", "%H:%M:%S").time()
SHIFT_END_TIME = datetime.strptime("17:00:00", "%H:%M:%S").time()

def deduct_leave(epf_no: str, deduction_amount: float, leave_type: str = "casual_used"):
    """Deduct leave by incrementing the used counter in leave_balances"""
    try:
        current_year = datetime.now().year
        # Get balance
        balance_res = supabase.table("leave_balances").select("*").eq("epf_no", epf_no).eq("year", current_year).execute()
        if balance_res.data:
            current_used = float(balance_res.data[0].get(leave_type, 0))
            new_used = current_used + deduction_amount
            supabase.table("leave_balances").update({leave_type: new_used}).eq("id", balance_res.data[0]["id"]).execute()
        else:
            # Create if not exists
            new_record = {"epf_no": epf_no, "year": current_year, leave_type: deduction_amount}
            supabase.table("leave_balances").insert(new_record).execute()
    except Exception as e:
        print(f"Leave deduction failed: {e}")

@app.post("/attendance/punch")
def hardware_punch(data: PunchData):
    try:
        # 1. Identify Employee
        emp_res = supabase.table("employees").select("epf_no, full_name").eq("fingerprint_id", data.fingerprint_id).execute()
        if not emp_res.data:
            raise HTTPException(status_code=404, detail="Employee not found for this Fingerprint ID")
        
        epf_no = emp_res.data[0]["epf_no"]
        emp_name = emp_res.data[0]["full_name"]
        
        punch_dt = datetime.fromisoformat(data.punch_time.replace("Z", "+00:00"))
        punch_date_str = punch_dt.strftime("%Y-%m-%d")
        punch_time_obj = punch_dt.time()

        # Check existing attendance for the day
        att_res = supabase.table("attendance").select("*").eq("epf_no", epf_no).eq("date", punch_date_str).execute()
        
        if not att_res.data:
            # This is an IN Punch
            late_mins = 0
            calc_status = "Present"
            
            # Auto Status & Late Check
            # Convert both to minutes from midnight for easy diff
            p_mins = punch_time_obj.hour * 60 + punch_time_obj.minute
            s_mins = SHIFT_START_TIME.hour * 60 + SHIFT_START_TIME.minute
            
            if p_mins > s_mins:
                late_mins = p_mins - s_mins
                calc_status = "Late In"
                
                # Auto deduction logic
                if late_mins > 60:
                    deduct_leave(epf_no, 0.5) # Deduct half day if more than 1 hour late
                elif late_mins > 15:
                    deduct_leave(epf_no, 0.25) # Deduct short leave if more than 15 mins late
            
            in_record = {
                "epf_no": epf_no,
                "date": punch_date_str,
                "in_time": data.punch_time,
                "calculated_status": calc_status,
                "late_minutes": late_mins
            }
            res = supabase.table("attendance").insert(in_record).execute()
            log_activity("Hardware Punch IN", f"{emp_name} ({epf_no}) punched IN at {punch_time_obj}")
            return {"success": True, "message": "Punch IN recorded", "data": res.data}
            
        else:
            # This is an OUT Punch (Assumes 1 shift per day for simplicity)
            existing_record = att_res.data[0]
            if existing_record["out_time"]:
                return {"success": False, "message": "Already punched out for the day"}
            
            in_dt = datetime.fromisoformat(existing_record["in_time"].replace("Z", "+00:00"))
            
            # Calc working hours
            diff = punch_dt - in_dt
            working_hours = round(diff.total_seconds() / 3600.0, 2)
            
            # Calc OT Hours & Early Out
            ot_hours = 0
            early_mins = 0
            p_mins = punch_time_obj.hour * 60 + punch_time_obj.minute
            e_mins = SHIFT_END_TIME.hour * 60 + SHIFT_END_TIME.minute
            
            if p_mins > e_mins:
                ot_hours = round((p_mins - e_mins) / 60.0, 2)
            elif p_mins < e_mins:
                early_mins = e_mins - p_mins
                if early_mins > 30:
                    deduct_leave(epf_no, 0.5) # 0.5 day early leave deduction if leaving > 30 mins early
            
            out_update = {
                "out_time": data.punch_time,
                "working_hours": working_hours,
                "ot_hours": ot_hours,
                "early_out_minutes": early_mins
            }
            
            res = supabase.table("attendance").update(out_update).eq("id", existing_record["id"]).execute()
            log_activity("Hardware Punch OUT", f"{emp_name} ({epf_no}) punched OUT at {punch_time_obj}")
            return {"success": True, "message": "Punch OUT recorded", "data": res.data}
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/attendance")
def get_attendance(date: str | None = None):
    try:
        query = supabase.table("attendance").select("*, employees(full_name, department)")
        if date:
            query = query.eq("date", date)
        
        res = query.order("created_at", desc=True).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ManualPunchData(BaseModel):
    epf_no: str
    punch_time: str # ISO string

@app.post("/attendance/manual-punch")
def manual_punch(data: ManualPunchData):
    try:
        # Get employee fingerprint_id to re-use hardware punch logic
        emp_res = supabase.table("employees").select("fingerprint_id").eq("epf_no", data.epf_no).execute()
        if not emp_res.data:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        fingerprint_id = emp_res.data[0].get("fingerprint_id")
        if not fingerprint_id:
             raise HTTPException(status_code=400, detail="Employee does not have a registered fingerprint ID for logic reuse.")
             
        # Reuse existing robust hardware punch logic
        punch_data = PunchData(fingerprint_id=fingerprint_id, punch_time=data.punch_time)
        return hardware_punch(punch_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/attendance/stats/today")
def get_today_stats():
    try:
        today_str = datetime.now().strftime("%Y-%m-%d")
        res = supabase.table("attendance").select("calculated_status").eq("date", today_str).execute()
        
        total_present = 0
        total_late = 0
        
        for r in res.data:
            status = r.get("calculated_status", "")
            if "Present" in status:
                total_present += 1
            elif "Late" in status:
                total_late += 1
                total_present += 1 # Late is also present
                
        # Get active employees count
        emp_res = supabase.table("employees").select("epf_no").eq("status", "Active").execute()
        total_employees = len(emp_res.data) if emp_res.data else 0
        
        # Get leaves today
        leave_res = supabase.table("leaves").select("id").eq("status", "Approved").lte("start_date", today_str).gte("end_date", today_str).execute()
        total_leave = len(leave_res.data) if leave_res.data else 0
        
        return {
            "success": True, 
            "data": {
                "present": total_present,
                "late": total_late,
                "absent": max(0, total_employees - total_present - total_leave),
                "on_leave": total_leave,
                "total": total_employees
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/leaves/apply")
def apply_leave(req: LeaveRequest):
    try:
        # Save leave
        leave_data = {
            "epf_no": req.epf_no,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "leave_type": req.leave_type,
            "days": req.days,
            "reason": req.reason,
            "status": "Pending"
        }
        res = supabase.table("leaves").insert(leave_data).execute()
        
        # Virtual Email Notification
        print(f"EMAIL NOTIFICATION SENT ✉️: Manager to approve {req.days} days {req.leave_type} leave from {req.epf_no}.")
        log_activity("Leave Application Application", f"{req.epf_no} applied for {req.days} days leave.")
        
        return {"success": True, "message": "Leave application sent for approval", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class LeaveAction(BaseModel):
    status: str # 'Approved' or 'Rejected'

@app.put("/leaves/{leave_id}/status")
def update_leave_status(leave_id: str, action: LeaveAction):
    try:
        if action.status not in ["Approved", "Rejected"]:
            raise HTTPException(status_code=400, detail="Invalid status")
            
        # Update leave status
        res = supabase.table("leaves").update({"status": action.status}).eq("id", leave_id).execute()
        
        if res.data:
            leave = res.data[0]
            log_activity("Leave Update", f"Leave {leave_id} was {action.status} for {leave.get('epf_no')}.")
            
            # Virtual Email Notification back to employee
            print(f"EMAIL NOTIFICATION SENT ✉️: Dear Employee {leave.get('epf_no')}, your leave request was {action.status}.")
            
        return {"success": True, "message": f"Leave {action.status.lower()} successfully", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/leaves")
def get_all_leaves():
    try:
        # Fetch with employee details via join
        res = supabase.table("leaves").select("*, employees(full_name, department)").order("created_at", desc=True).execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/dashboard/data")
def get_dashboard_data():
    try:
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        
        # 1. Stats
        active_emps_res = supabase.table("employees").select("epf_no, department, birthday, full_name").eq("status", "Active").execute()
        active_emps = active_emps_res.data if active_emps_res.data else []
        total_employees = len(active_emps)
        
        att_res = supabase.table("attendance").select("calculated_status").eq("date", today_str).execute()
        att_data = att_res.data if att_res.data else []
        total_present = sum(1 for a in att_data if "Present" in a.get("calculated_status", ""))
        total_late = sum(1 for a in att_data if "Late" in a.get("calculated_status", ""))
        total_present += total_late
        
        leaves_res = supabase.table("leaves").select("id, start_date, end_date, employees(full_name, department)").eq("status", "Approved").lte("start_date", today_str).gte("end_date", today_str).execute()
        leaves_today = leaves_res.data if leaves_res.data else []
        total_leave = len(leaves_today)
        
        absent_today = max(0, total_employees - total_present - total_leave)
        
        # 2. Distribution Data
        dept_counts = {}
        today_events = []
        for emp in active_emps:
            dept = emp.get("department", "Unassigned")
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
            
            # Check Birthday
            bday = emp.get("birthday")
            if bday:
                try:
                    b_dt = datetime.strptime(bday, "%Y-%m-%d")
                    if b_dt.month == today.month and b_dt.day == today.day:
                        today_events.append({
                            "id": f"bd-{emp['epf_no']}",
                            "name": emp.get("full_name", ""),
                            "department": dept,
                            "type": "Birthday"
                        })
                except:
                    pass

        dist_labels = list(dept_counts.keys())
        dist_series = list(dept_counts.values())
        
        # Add leave events
        for lv in leaves_today:
            emp_info = lv.get("employees", {})
            today_events.append({
                "id": f"lv-{lv['id']}",
                "name": emp_info.get("full_name", "") if emp_info else "Unknown",
                "department": emp_info.get("department", "Unassigned") if emp_info else "Unassigned",
                "type": "Leave"
            })
            
        # 3. Activities
        acts_res = supabase.table("activity_log").select("*").order("timestamp", desc=True).limit(5).execute()
        
        def time_ago(ts):
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
                diff = today - dt
                if diff.days > 0: return f"{diff.days} days ago"
                if diff.seconds > 3600: return f"{diff.seconds // 3600} hrs ago"
                if diff.seconds > 60: return f"{diff.seconds // 60} mins ago"
                return "Just now"
            except:
                return ""
            
        activities = []
        for act in (acts_res.data if acts_res.data else []):
            color = "primary"
            icon = "info"
            title = act.get("activity_type", "")
            
            if "Leave" in title:
                 color = "positive"
                 icon = "event"
            elif "Update" in title:
                 color = "warning"
                 icon = "edit"
            elif "Added" in title or "Register" in title:
                 color = "Accent"
                 icon = "person_add"
            elif "Punch" in title:
                 color = "info"
                 icon = "fingerprint"
                 
            activities.append({
                "title": title,
                "details": act.get("details", ""),
                "time": time_ago(act.get("timestamp", "")),
                "color": color,
                "icon": icon
            })
            
        return {
            "success": True,
            "data": {
                "stats": {
                    "totalEmployees": total_employees,
                    "presentToday": total_present,
                    "lateArrivals": total_late,
                    "absentToday": absent_today
                },
                "distribution": {
                    "labels": dist_labels,
                    "series": dist_series
                },
                "events": today_events,
                "activities": activities
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
