from utils.logger import logger

def calculate_suitability_score(responses):
    try:
        max_score = len(responses) * 4
        candidate_score = sum(responses)
        suitability_score = (candidate_score / max_score) * 100
        logger.info(f"Calculated suitability score: {suitability_score}%")
        return suitability_score
    except Exception as e:
        logger.error(f"Error calculating suitability score: {e}")
        return 0

def get_suitability_description(score):
    try:
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
    except Exception as e:
        logger.error(f"Error determining suitability description for score {score}: {e}")
        return "Error determining suitability"
