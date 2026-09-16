from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from database.database import engine, Base, SessionLocal
from models.user_model import User
from models.expense_model import Expense
from models.budget_model import Budget
from models.savings_model import Savings
from ai.spending_analysis import analyze_spending
from ai.unusual_spending import detect_unusual_spending
from ai.expense_prediction import predict_next_month_expense
from ai.spending_classification import classify_spending
import json
from ai.chatbot import get_chatbot_response

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )
@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )
@app.post("/register")
def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    new_user = User(
        name=name,
        email=email,
        password=password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return RedirectResponse(
       url="/login",
       status_code=303
)
@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
   return templates.TemplateResponse(
    request=request,
    name="login.html",
    context={
        "request": request
    }
)
@app.post("/login")
def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    if not user:
        db.close()
        return {"message": "Invalid email or password"}

    if user.password != password:
        db.close()
        return {"message": "Invalid email or password"}

    db.close()
    
    return RedirectResponse(
        url="/dashboard",
        status_code=303
)
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()

    total_expense = db.query(Expense).with_entities(Expense.amount).all()
    total_spent = sum(expense[0] for expense in total_expense)

    category_totals = {}

    expenses = db.query(Expense).all()

    for expense in expenses:

        if expense.category in category_totals:
            category_totals[expense.category] += expense.amount

        else:
            category_totals[expense.category] = expense.amount

    categories_json = json.dumps(list(category_totals.keys()))
    amounts_json = json.dumps(list(category_totals.values()))

    budget = db.query(Budget).order_by(Budget.id.desc()).first()

    savings = db.query(Savings).order_by(Savings.id.desc()).first()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "total_spent": total_spent,
            "budget": budget,
            "savings": savings,
            "category_totals": category_totals,
            "categories_json": categories_json,
            "amounts_json": amounts_json
        }
    )
@app.get("/add-expense", response_class=HTMLResponse)
def add_expense_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add_expense.html",
        context={"request": request}
    )
@app.post("/add-expense")
def add_expense(
    title: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    date: str = Form(...)
):
    db = SessionLocal()

    new_expense = Expense(
        title=title,
        amount=amount,
        category=category,
        date=date
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    db.close()

    return {
        "message": "Expense added successfully",
        "title": new_expense.title,
        "amount": new_expense.amount,
        "category": new_expense.category,
        "date": new_expense.date
    }
@app.get("/expenses", response_class=HTMLResponse)
def view_expenses(request: Request):
    db = SessionLocal()

    expenses = db.query(Expense).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="expenses.html",
        context={
            "request": request,
            "expenses": expenses
        }
    )
@app.get("/budget", response_class=HTMLResponse)
def budget_page(request: Request):
    db = SessionLocal()

    budget = db.query(Budget).order_by(Budget.id.desc()).first()
    
    total_expense = db.query(Expense).with_entities(Expense.amount).all()
    total_spent = sum(expense[0] for expense in total_expense)
    
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="budget.html",
        context={
    "request": request,
    "budget": budget,
    "total_spent": total_spent
}
    )


@app.post("/budget")
def save_budget(
    month: str = Form(...),
    amount: float = Form(...)
):
    db = SessionLocal()

    new_budget = Budget(
        month=month,
        amount=amount
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    db.close()

    return {
        "message": "Budget saved successfully",
        "month": new_budget.month,
        "amount": new_budget.amount
    }
@app.get("/savings", response_class=HTMLResponse)
def savings_page(request: Request):
    db = SessionLocal()

    savings = db.query(Savings).order_by(Savings.id.desc()).first()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="savings.html",
        context={
            "request": request,
            "savings": savings
        }
    )
@app.post("/savings")
def save_savings(
    goal: str = Form(...),
    target_amount: float = Form(...),
    saved_amount: float = Form(...)
):
    db = SessionLocal()

    new_savings = Savings(
        goal=goal,
        target_amount=target_amount,
        saved_amount=saved_amount
    )

    db.add(new_savings)
    db.commit()
    db.refresh(new_savings)

    db.close()

    return {
        "message": "Savings goal saved successfully",
        "goal": new_savings.goal,
        "target_amount": new_savings.target_amount,
        "saved_amount": new_savings.saved_amount
    }
@app.get("/split-expense", response_class=HTMLResponse)
def split_expense_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="split_expense.html",
        context={
            "request": request
        }
    )
@app.post("/split-expense", response_class=HTMLResponse)
def split_expense(
    request: Request,
    expense_name: str = Form(...),
    amount: float = Form(...),
    people: int = Form(...)
):

    each_person = amount / people

    result = {
        "expense_name": expense_name,
        "amount": amount,
        "people": people,
        "each_person": each_person
    }

    return templates.TemplateResponse(
        request=request,
        name="split_expense.html",
        context={
            "request": request,
            "result": result
        }
    )
@app.get("/analysis", response_class=HTMLResponse)
def analysis_page(request: Request):
    db = SessionLocal()

    expenses = db.query(Expense).all()

    category_totals = {}
    classifications = []

    for expense in expenses:

        if expense.category in category_totals:
            category_totals[expense.category] += expense.amount
        else:
            category_totals[expense.category] = expense.amount

        classification = classify_spending(
            expense.category,
            expense.amount
        )

        classifications.append({
            "title": expense.title,
            "category": expense.category,
            "amount": expense.amount,
            "classification": classification
        })

    recommendations = analyze_spending(category_totals)

    unusual_spending = detect_unusual_spending(category_totals)

    predicted_expense = predict_next_month_expense(category_totals)

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="analysis.html",
        context={
            "request": request,
            "category_totals": category_totals,
            "recommendations": recommendations,
            "unusual_spending": unusual_spending,
            "predicted_expense": predicted_expense,
            "classifications": classifications
        }
    )
@app.get("/chatbot", response_class=HTMLResponse)
def chatbot_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="chatbot.html",
        context={
            "request": request
        }
    )


@app.post("/chatbot", response_class=HTMLResponse)
def chatbot(
    request: Request,
    question: str = Form(...)
):

    answer = get_chatbot_response(question)

    return templates.TemplateResponse(
        request=request,
        name="chatbot.html",
        context={
            "request": request,
            "answer": answer
        }
    )