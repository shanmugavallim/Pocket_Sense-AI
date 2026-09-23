def get_savings_suggestion(total_spent, budget):

    if budget <= 0:
        return "Set a monthly budget to get savings suggestions."

    spending_percentage = (total_spent / budget) * 100

    if spending_percentage >= 90:
        return "Your spending is close to your budget. Try reducing unnecessary expenses."

    elif spending_percentage >= 70:
        return "You are using most of your budget. Try saving a little more this month."

    else:
        return "Your spending is under control. Consider saving the remaining budget amount."