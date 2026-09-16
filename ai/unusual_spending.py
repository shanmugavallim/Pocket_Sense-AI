def detect_unusual_spending(category_totals):

    unusual = []

    for category, amount in category_totals.items():

        if amount >= 10000:
            unusual.append(
                f"Unusual spending detected in {category}: ₹{amount}"
            )

    return unusual