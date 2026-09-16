def get_chatbot_response(question):

    question = question.lower()

    if "save" in question or "saving" in question:
        return "Try to reduce unnecessary expenses and set a monthly savings goal."

    elif "budget" in question:
        return "Create a monthly budget and compare your expenses with the budget."

    elif "expense" in question or "spending" in question:
        return "Track your daily expenses and check which category consumes more money."

    elif "food" in question:
        return "Try to control food expenses by reducing unnecessary food orders."

    elif "transport" in question:
        return "You can reduce transport expenses by using public transport when possible."

    else:
        return "I can help you with savings, budget, expenses, food spending and transport spending."