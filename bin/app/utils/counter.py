def calculate_suitability_score(responses):
    max_score = len(responses) * 4
    candidate_score = sum(responses)
    return (candidate_score / max_score) * 100

def get_suitability_description(score):
    if score >= 75:
        return "Highly Suitable"
    elif score >= 50:
        return "Suitable"
    elif score >= 25:
        return "Moderately Suitable"
    elif score > 0:
        return "Slightly Suitable"
    else:
        return "Not Suitable"
