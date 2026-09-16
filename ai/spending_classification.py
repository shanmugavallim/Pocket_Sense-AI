def classify_spending(category, amount):

    if category.lower() in ["food", "medicine", "education", "transport"]:
        return "Essential Spending"

    elif amount >= 5000:
        return "High Non-Essential Spending"

    else:
        return "Non-Essential Spending"