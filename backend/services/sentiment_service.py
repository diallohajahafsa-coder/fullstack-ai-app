import re


POSITIVE_WORDS = {
    "amazing",
    "awesome",
    "best",
    "excellent",
    "good",
    "great",
    "happy",
    "love",
    "wonderful",
}
NEGATIVE_WORDS = {
    "awful",
    "bad",
    "disappointing",
    "hate",
    "poor",
    "sad",
    "terrible",
    "worst",
}


def analyze_sentiment(text):
    words = [re.sub(r"[^a-z]", "", word) for word in text.lower().split()]
    positive_count = sum(word in POSITIVE_WORDS for word in words)
    negative_count = sum(word in NEGATIVE_WORDS for word in words)
    difference = positive_count - negative_count

    if difference > 0:
        label = "positive"
    elif difference < 0:
        label = "negative"
    else:
        label = "neutral"

    matched_count = positive_count + negative_count
    strength = round(abs(difference) / matched_count, 2) if matched_count else 0
    return {"label": label, "strength": strength, "mode": "demo_rules"}
