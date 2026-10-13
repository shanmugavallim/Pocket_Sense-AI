def get_chatbot_response(question: str) -> str:
    """
    Provide basic personal finance guidance
    based on the user's question.
    """

    question = question.lower().strip()

    if "save" in question or "saving" in question:
        return (
            "Try to reduce unnecessary expenses, "
            "set a monthly savings goal, and save "
            "a small amount regularly."
        )

    elif "budget" in question:
        return (
            "Create a monthly budget and compare your "
            "actual expenses with your planned budget. "
            "Avoid spending more than your budget."
        )

    elif "expense" in question or "spending" in question:
        return (
            "Track your daily expenses and check which "
            "categories consume the most money. "
            "Reduce unnecessary spending where possible."
        )

    elif "food" in question:
        return (
            "Plan your meals and limit unnecessary food "
            "orders to manage your food expenses."
        )

    elif "transport" in question:
        return (
            "Consider public transport or shared travel "
            "when practical to reduce transportation costs."
        )

    elif "shopping" in question:
        return (
            "Make a shopping list, compare prices, and "
            "avoid unnecessary purchases."
        )

    elif "debt" in question or "loan" in question:
        return (
            "Track your repayments and prioritize required "
            "payments. Avoid taking on debt you cannot repay."
        )

    elif "hello" in question or "hi" in question:
        return (
            "Hello! I am your PocketSense AI Finance "
            "Assistant. Ask me about savings, budgeting, "
            "expenses, food spending, or transport costs."
        )

    else:
        return (
            "I can help with basic personal finance topics "
            "such as savings, budgeting, expenses, food "
            "spending, shopping, and transportation. "
            "Please ask a question about one of these topics."
        )
