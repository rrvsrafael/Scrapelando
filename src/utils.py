import re


def validate_search_term(search_term):
    if not isinstance(search_term, str):
        raise ValueError("Search term must be a string")
    if not search_term.strip():
        raise ValueError("Search term cannot be empty")
    if len(search_term) > 100:
        raise ValueError("Search term is too long")
    if re.search(r"[<>{}|\\\'`]", search_term):
        raise ValueError("Search term contains invalid characters")
    return search_term.strip().replace(" ", "-")


def validate_min_score(min_score):
    if not isinstance(min_score, int):
        raise ValueError("Minimum score must be an integer")
    if min_score < 0 or min_score > 1000:
        raise ValueError("Minimum score must be between 0 and 1000")
    return min_score
