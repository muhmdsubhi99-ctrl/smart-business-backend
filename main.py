from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# تحميل Environment Variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# إعداد قاعدة البيانات
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Smart Business SaaS Backend")

# -----------------------------
# Models
# -----------------------------
class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company_id = Column(Integer)
    salary = Column(Float)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer)
    amount = Column(Float)

# إنشاء الجداول إذا لم توجد
Base.metadata.create_all(bind=engine)

# -----------------------------
# Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def root():
    return {"message": "Smart Business SaaS API Running"}

# Companies
@app.post("/company/")
def create_company(name: str, db: Session = Depends(get_db)):
    db_company = Company(name=name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@app.get("/company/")
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()

# Employees
@app.post("/employee/")
def create_employee(name: str, company_id: int, salary: float, db: Session = Depends(get_db)):
    db_employee = Employee(name=name, company_id=company_id, salary=salary)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employee/")
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

# Sales
@app.post("/sale/")
def create_sale(company_id: int, amount: float, db: Session = Depends(get_db)):
    db_sale = Sale(company_id=company_id, amount=amount)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@app.get("/sale/")
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()

# Smart Compensation (مثال)
@app.get("/compensation/{employee_id}")
def calculate_compensation(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    # مثال: مكافأة 10% على الراتب
    bonus = employee.salary * 0.1
    return {"employee_id": employee.id, "name": employee.name, "salary": employee.salary, "bonus": bonus}
