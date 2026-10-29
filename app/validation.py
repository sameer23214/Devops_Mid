import re

def validate_submission(data):
    if not data or not isinstance(data, dict):
        return False, "Invalid payload"
    
    name = data.get("name", "").strip()
    regNumber = data.get("regNumber", "").strip()
    title = data.get("title", "").strip()
    url = data.get("url", "").strip()

    if not name or not regNumber or not title or not url:
        return False, "All fields (name, registration number, title, url) are required."

    url_pattern = re.compile(
        r'^(https?://)'
        r'([\da-z.-]+)\.([a-z.]{2,6})'
        r'([/\w .-]*)*/?$', re.IGNORECASE
    )
    
    if not url_pattern.match(url):
        return False, "Invalid submission URL format."

    return True, "Valid"
