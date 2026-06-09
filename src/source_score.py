SOURCE_SCORES = {

    "Reuters": 99,
    "Associated Press": 99,
    "BBC News": 97,
    "The Hindu": 96,
    "The Indian Express": 95,
    "Hindustan Times": 93,
    "Times of India": 92,
    "NDTV": 91,
    "India Today": 90,
    "The Print": 90,
    "Mint": 90,
    "Business Standard": 89,
    "Moneycontrol": 89,
    "Financial Express": 88,
    "Firstpost": 87,
    "Scroll": 87,
    "The Wire": 86,
    "Outlook India": 85,
    "PRS India": 95,
    "DD News": 94,
    "Prasar Bharati": 94,
    "Malayala Manorama": 90,
    "Anandabazar Patrika": 90
}


def get_source_score(publisher):

    score = SOURCE_SCORES.get(publisher, 60)

    if score >= 95:
        level = "Very High"

    elif score >= 90:
        level = "High"

    elif score >= 80:
        level = "Moderate"

    else:
        level = "Low"

    return {

        "score": score,

        "level": level

    }