from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------
# Company
# ------------------------
@app.post("/company/")
def create_company(name: str, db: Session = Depends(get_db)):
    company = models.Company(name=name)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@app.get("/company/")
def get_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()

# ------------------------
# Employee
# ------------------------
@app.post("/employee/")
def create_employee(name: str, company_id: int, salary: float, db: Session = Depends(get_db)):
    employee = models.Employee(name=name, company_id=company_id, salary=salary)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

@app.get("/employee/")
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

# ------------------------
# Sale
# ------------------------
@app.post("/sale/")
def create_sale(company_id: int, amount: float, db: Session = Depends(get_db)):
    sale = models.Sale(company_id=company_id, amount=amount)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

@app.get("/sale/")
def get_sales(db: Session = Depends(get_db)):
    return db.query(models.Sale).all()

# ------------------------
# Compensation
# ------------------------
@app.get("/compensation/{employee_id}")
def calculate_bonus(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        return {"error": "Employee not found"}

    bonus = employee.salary * 0.1
    return {
        "employee": employee.name,
        "salary": employee.salary,
        "bonus": bonus
    }
