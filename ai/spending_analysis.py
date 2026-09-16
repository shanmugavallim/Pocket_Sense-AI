def analyze_spending(category_totals):

    recommendations = []

    for category, amount in category_totals.items():

        if amount >= 5000:
            recommendations.append(
                f"Your {category} spending is high. Try reducing it."
            )

        elif amount >= 2000:
            recommendations.append(
                f"Keep an eye on your {category} spending."
            )

        else:
            recommendations.append(
                f"Your {category} spending is under control."
            )

    return recommendations